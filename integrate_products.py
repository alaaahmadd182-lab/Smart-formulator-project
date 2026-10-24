#!/usr/bin/env python3
"""Data integration: give every product property one final value in a consistent unit.

Usage: python integrate_products.py [--input Products_json] [--dry-run]

Adds keys next to the existing data; never removes or edits an existing key:
  value_final, unit_final, min_final, max_final   every value object (numeric ones converted)
  unit_conversion                                 how value_final was derived from the printed unit
  integration_flags                               anything the conversion could not settle
  resolution, status_final, source_final, ...     properties where a recorded conflict was resolved
  final_resolution, resolved                      on each entry of the conflicts[] arrays
Only exception: a conflict entry stored as a bare string is wrapped as {"note": <string>}.

Unit rules (unit change only, no estimated values):
  viscosity cSt; density g/cm3 at the printed temperature (not corrected to 15 C);
  temperatures C; CCS/MRV/HTHS mPa.s; mass fractions wt.% (ppm / 10000).
  Specific gravity / relative density and bare '%' (basis not printed) are kept as printed and flagged.

Conflict rules (user decision 2026-10-24):
  1. TDS (also PDS / product bulletin / spec sheet) preferred over SDS.
  2. Same document type: newest dated edition; average (Calculated) only when the dates
     cannot be compared. Text values (claim codes, claim dots) always take the newest.
  3. A measured / typical number beats a bound ('>110', '>=180') whichever document it is in.
  4. Decisions the user already made on 2026-10-18 (RF6077, RF6088F) are kept.
"""
import argparse, glob, json, os, re, sys
from decimal import Decimal

ELEMENTS = {'Ca', 'Mg', 'Zn', 'P', 'B', 'Mo', 'N', 'S', 'ca', 'mg', 'zn', 'p', 'mo'}
FAMILY = {}
for fam, keys in {
    'visc': {'kv40', 'kv100', 'delta_kv100_cst'},
    'density': {'density'},
    'temp': {'flash_point', 'pour_point', 'cloud_point', 'temperature_c', 'blend_temperature_c', 'pour_point_change_c'},
    'lowtemp': {'ccs', 'ccs_viscosity', 'mrv', 'mrv_viscosity', 'hths'},
    'pa': {'yield_stress'},
    'tbn': {'tbn'},
    'vi': {'viscosity_index'},
    'mass': {'noack_volatility', 'saturates', 'aromatics', 'wax_content', 'sulfur', 'sulfated_ash', 'active_content',
             'wt_pct', 'share_wt_pct', 'carrier_share_wt_pct', 'treat_rate', 'treat_rate_wt_pct', 'treat_range_wt_pct',
             'dose_wt_pct', 'tested_dose_range_wt_pct'} | ELEMENTS,
}.items():
    for k in keys:
        FAMILY[k] = fam

# family -> {printed unit (lower case): (final unit, factor)}
UNITS = {
    'visc': {u: ('cSt', '1') for u in ('cst', 'mm2/s', 'mm²/s', 'mm2/sec', 'mm/s2')},
    'density': {**{u: ('g/cm³', '1') for u in ('g/cm³', 'g/cm3', 'g/ml', 'kg/l', 'kg/dm3')},
                'kg/m3': ('g/cm³', '0.001'), 'kg/m³': ('g/cm³', '0.001'), 'lbs/gal': ('g/cm³', '0.119826427')},
    'temp': {u: ('°C', '1') for u in ('c', '°c', 'deg c', '℃')},
    'lowtemp': {u: ('mPa·s', '1') for u in ('mpas', 'mpa.s', 'mpa·s', 'cp')},
    'pa': {'pa': ('Pa', '1')},
    'tbn': {u: ('mg KOH/g', '1') for u in ('mg koh/g', 'mgkoh/g')},
    'mass': {**{u: ('wt.%', '1') for u in ('wt.%', 'wt%', 'mass%', 'mass %', '%m/m', 'wt.% loss', 'wt.% as printed', 'm%')},
             **{u: ('wt.%', '0.0001') for u in ('ppm', 'mg/kg', 'wt ppm')}},
}
NOT_CONVERTED = {'specific gravity (dimensionless)': 'specific gravity', 'relative density': 'relative density'}
OWN_KEYS = ('value_final', 'unit_final', 'min_final', 'max_final', 'unit_conversion', 'integration_flags',
            'resolution', 'status_final', 'source_final', 'qualifier_final', 'method_final', 'test_temperature_c_final')


def src(file, page, rev=None):
    return {'file': file, 'page': page, 'revision_date': rev}


TDS_SDS = 'TDS preferred over SDS'
SAME_NEWEST = 'Same document type; newest edition used'
SAME_AVG = 'Same document type, editions undated so the newest cannot be determined; average taken'
# (product, tier, path) -> override. 'value' is already in the final unit; no 'value' = field already holds the result.
OVERRIDES = {
    ('INFINEUM_D3424', 2, 'flash_point'): dict(
        value=190, qualifier_final=None, method_final='ASTM D 93 (PM)', status_final='Reported',
        source_final=src('DL2-10204.pdf', 1, '2004-11-09'),
        resolution=f"{TDS_SDS}: TDS typical 190 °C (DL2-10204.pdf p.1, 2004) chosen over SDS lower bound '>110 °C' "
                   "(p.6, 2008), which was in the field under the old newest-document rule."),
    ('RICHFUL_RF6066', 2, 'density'): dict(
        value=0.989, status_final='Calculated', test_temperature_c_final=20,
        source_final=[src('DL2-13819.pdf', 1), src('DL2-15451.pdf', 1)],
        resolution=f"{SAME_AVG}: TDS DL2-13819.pdf 990 kg/m³ and TDS DL2-15451.pdf 988 kg/m³ (both at 20 °C) -> "
                   f"989 kg/m³ = 0.989 g/cm³. SDS values (990 kg/m³, 0.988 g/cm³) not used: {TDS_SDS}."),
    ('RICHFUL_RF6066', 2, 'kv100'): dict(
        value=206, status_final='Calculated', source_final=[src('DL2-13819.pdf', 1), src('DL2-15451.pdf', 1)],
        resolution=f"{SAME_AVG}: TDS 227 and 185 cSt -> 206 cSt. The two TDS differ by about 20 %, so this average is "
                   f"weak; check with Richful. SDS values (200, 185) not used: {TDS_SDS}."),
    ('RICHFUL_RF6066', 2, 'tbn'): dict(
        value=107, status_final='Calculated', source_final=[src('DL2-13819.pdf', 1), src('DL2-15451.pdf', 1)],
        resolution=f"{SAME_AVG}: TDS 106 and 108 mg KOH/g -> 107. SDS value (106) not used: {TDS_SDS}."),
    ('RICHFUL_RF6066', 2, 'elements.Zn'): dict(
        value=1.27, status_final='Calculated', source_final=[src('DL2-13819.pdf', 1), src('DL2-15451.pdf', 1)],
        resolution=f"{SAME_AVG}: TDS 1.3 and 1.24 wt.% -> 1.27 wt.%."),
    ('RICHFUL_RF6066', 2, 'elements.Ca'): dict(
        value=3.075, status_final='Calculated', source_final=[src('DL2-13819.pdf', 1), src('DL2-15451.pdf', 1)],
        resolution=f"{SAME_AVG}: TDS 3.0 and 3.15 wt.% -> 3.075 wt.%."),
    ('RICHFUL_RF6069', 2, 'kv100'): dict(
        value=118, status_final='Reported', source_final=src('DL2-15618.pdf', 1),
        resolution=f"{TDS_SDS}: TDS DL2-15618.pdf 118 cSt chosen over SDS DL2-15619.pdf 142 cSt (2022-01-04)."),
    ('RICHFUL_RF6077', 2, 'density'): dict(
        resolution="User decision of 2026-10-18 kept (SDS DL2-15542.pdf 0.991 g/cm³ at 15 °C); it overrides the "
                   "TDS-preferred rule, which would give TDS DL2-15536.pdf 998 kg/m³ at 20 °C."),
    ('RICHFUL_RF6077', 2, 'kv100'): dict(
        resolution="User decision of 2026-10-18 kept (SDS DL2-15542.pdf 150 cSt); it overrides the TDS-preferred "
                   "rule, which would give TDS DL2-15536.pdf 160 cSt."),
    ('RICHFUL_RF6078', 1, 'treat_rate_matrix[0].treat_rate_wt_pct'): dict(
        value=11.35, status_final='Calculated',
        source_final=[src('DL2-15832.pdf', 1), src('RF6078%20-%20TDS.pdf', 1)],
        resolution=f"{SAME_AVG}: row 'ACEA E7/API CI-4' is 11.85 % in DL2-15832.pdf and 10.85 % in "
                   "'RF6078 - TDS.pdf' -> 11.35 %. The two sheets label their second row differently "
                   "('API CI-4' vs 'API CI-4 Plus'), so the average is weak; check with Richful."),
    ('RICHFUL_RF6078', 2, 'density'): dict(
        value=0.972, status_final='Reported', source_final=[src('DL2-15832.pdf', 1), src('RF6078%20-%20TDS.pdf', 1)],
        resolution=f"{TDS_SDS}: both TDS print 972 kg/m³ at 20 °C (= 0.972 g/cm³); SDS DL2-15833.pdf 975 kg/m³ not used."),
    ('RICHFUL_RF6081', 2, 'kv100'): dict(
        resolution=f"{TDS_SDS}: TDS DL2-15836.pdf 132 cSt kept over SDS DL2-15837.pdf 130 cSt (the TDS is also newer)."),
    ('RICHFUL_RF6088F', 2, 'density'): dict(
        resolution=f"User decision of 2026-10-18 kept (TDS DL2-15839.pdf 963 kg/m³ at 20 °C); agrees with {TDS_SDS} "
                   "(SDS DL2-15840.pdf relative density 0.958 not used)."),
    ('RICHFUL_RF6088F', 2, 'kv100'): dict(
        resolution="User decision of 2026-10-18 kept (SDS DL2-15840.pdf 178.2 cSt); it overrides the TDS-preferred "
                   "rule, which would give TDS DL2-15839.pdf 177 cSt."),
    ('RICHFUL_RF6406', 1, 'treat_rate_matrix[10].treat_rate_wt_pct'): dict(
        value=3.9, status_final='Calculated', source_final=[src('DL2-15456.pdf', 1), src('DL2-14746.pdf', 1)],
        resolution=f"{SAME_AVG}: row 'CF/SF Multi' is 4.1 % in DL2-15456.pdf and 3.7 % in DL2-14746.pdf -> 3.9 %."),
    ('RICHFUL_RF6406', 2, 'tbn'): dict(
        value=185, status_final='Reported', source_final=src('DL2-15456.pdf', 1),
        resolution="Measured value beats a bound: TDS DL2-15456.pdf typical 185 mg KOH/g chosen over TDS "
                   "DL2-14746.pdf '≥180' (a minimum, not a measurement)."),
    ('FORMOSA_150N_GII_PLUS', 2, 'flash_point'): dict(
        resolution=f"{TDS_SDS}: specification sheet DL2-10001.pdf 'Min 210 C' kept over SDS DL2-10011.pdf '>230 C'. "
                   "Both are bounds, so there is no single measured value."),
    ('NYNAS_NS_3', 1, 'kv40'): dict(resolution=f"{SAME_NEWEST}: 2024 edition DL2-15474.pdf 2.92 cSt over 2016 edition DL2-12382.pdf 2.84 cSt."),
    ('NYNAS_NS_3', 1, 'density'): dict(resolution=f"{SAME_NEWEST}: 2024 edition DL2-15474.pdf 0.863 over 2016 edition DL2-12382.pdf 0.860."),
    ('NYNAS_NS_3', 2, 'flash_point'): dict(resolution=f"{SAME_NEWEST}: 2024 edition DL2-15474.pdf 95 °C over 2016 edition DL2-12382.pdf 94 °C."),
    ('NYNAS_NS_3', 3, 'sulfur'): dict(
        resolution=f"{SAME_NEWEST}: 2024 edition DL2-15474.pdf 'Typical < 10 ppm' over 2016 edition DL2-12382.pdf "
                   "30 ppm. '<10 ppm' is a typical result below the reporting limit, not a specification bound, "
                   "so the measured-beats-bound rule does not apply."),
    ('NYNAS_NYFROST_32', 1, 'kv40'): dict(resolution=f"{TDS_SDS}: PDS DL2-11510.pdf 32 cSt kept over SDS DL2-13444.pdf 31 cSt."),
    ('NYNAS_NYFROST_32', 2, 'flash_point'): dict(
        resolution=f"{TDS_SDS}: PDS DL2-11510.pdf typical 176 °C (Pensky-Martens) kept over SDS DL2-13444.pdf bound '>180 °C'."),
    ('PETRONAS_ETRO_6_PLUS', 1, 'kv40'): dict(resolution=f"{TDS_SDS}: TDS DL2-10234.pdf 32.55 cSt kept over SDS DL2-14610.pdf 34.79 cSt."),
    ('PETRONAS_ETRO_6_PLUS', 1, 'density'): dict(
        value=0.8429, status_final='Reported', test_temperature_c_final=None, method_final='ASTM D 1298/D 4052',
        source_final=src('DL2-10234.pdf', 1),
        resolution=f"{TDS_SDS}: TDS DL2-10234.pdf 0.8429 kg/L chosen over SDS DL2-14610.pdf 0.8486 g/cm³ at 15 °C, "
                   "which was in the field. The TDS prints no measurement temperature."),
    ('PETRONAS_ETRO_6_PLUS', 2, 'flash_point'): dict(
        resolution=f"{TDS_SDS}: TDS DL2-10234.pdf 240 °C (ASTM D92, COC) kept over SDS DL2-14610.pdf 228 °C "
                   "(ASTM D93, PMCC). Different methods, so the two values are not directly comparable."),
    ('PETRONAS_ETRO_6_PLUS', 2, 'noack_volatility'): dict(resolution=f"{TDS_SDS}: TDS DL2-10234.pdf 5.7 wt.% kept over SDS DL2-14610.pdf 5.3 wt.%."),
    ('PETRO_CANADA_PURITY_L65', 1, 'viscosity_index'): dict(
        resolution="TDS DL2-10020.pdf 92 kept over the Petro-Canada marketing brochure (104), which is neither a TDS "
                   "nor an SDS and is not in the archive."),
    ('SHELL_RISELLA_X_415', 1, 'density'): dict(resolution=f"{TDS_SDS}: TDS DL2-13728.pdf 806 kg/m³ kept over SDS DL2-13729.pdf 803.5 kg/m³."),
    ('SHELL_RISELLA_X_420', 1, 'density'): dict(resolution=f"{TDS_SDS}: TDS DL2-13726.pdf 816 kg/m³ kept over SDS DL2-13730.pdf 813.8 kg/m³."),
    ('SHELL_RISELLA_X_430', 1, 'density'): dict(resolution=f"{TDS_SDS}: TDS DL2-13727.pdf 828 kg/m³ kept over SDS DL2-13731.pdf 824.8 kg/m³."),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', 3, 'sulfur'): dict(
        resolution="UNRESOLVED: DL2-13944.pdf prints '1.3 ppm' and DL2-12173.pdf prints 'Max WT% 1.3'. Same number, "
                   "units 10,000x apart, so one sheet is almost certainly misprinted. The rules cannot pick between them; "
                   "confirm with Aramco. value_final shows the field as it stands."),
    ('ERGON_HYGOLD_L750', 1, 'density'): dict(
        resolution="UNRESOLVED: a single TDS (DL2-10414.pdf) prints density 0.854 g/cm³ and specific gravity 0.9183 at "
                   "15.6 °C, which contradict each other. This is not a two-document conflict, so the rules do not apply; "
                   "confirm with Ergon. value_final shows the density as printed."),
}

# (product, substring of the conflict entry) -> (resolved?, note). Every conflict entry must match one.
CONFLICTS = [
    ('AFTON_HITEC_12200', 'MTU 2.0', True, f'{SAME_NEWEST} (08/18 bulletin: not claimed); text value, not averaged. Fields already hold it.'),
    ('AFTON_HITEC_12200', 'DDC 93K215', True, f'{SAME_NEWEST} (08/18 bulletin: claimed); text value, not averaged. Fields already hold it.'),
    ('INFINEUM_D3424', 'flash_point', True, 'TDS preferred over SDS; see fields.flash_point.resolution.'),
    ('LUBRIZOL_CV7540', 'CES 20076', True, f"{SAME_NEWEST} (2022 sheet: 'A - Approved'); text value, not averaged."),
    ('LUBRIZOL_CV7540', 'CES 20077', True, f"{SAME_NEWEST} (2022 sheet: 'A - Approved'); text value, not averaged."),
    ('LUBRIZOL_CV7540', 'CES 20078', True, f"{SAME_NEWEST} (2022 sheet: 'A - Approved'); text value, not averaged."),
    ('RICHFUL_RF6066', 'tier2.density', True, 'See fields.density.resolution.'),
    ('RICHFUL_RF6066', 'tier2.kv100', True, 'See fields.kv100.resolution.'),
    ('RICHFUL_RF6066', 'tier2.tbn', True, 'See fields.tbn.resolution.'),
    ('RICHFUL_RF6066', 'elements.Zn', True, 'See fields.elements.Zn.resolution.'),
    ('RICHFUL_RF6066', 'elements.Ca', True, 'See fields.elements.Ca.resolution.'),
    ('RICHFUL_RF6069', 'tier2.kv100', True, 'See fields.kv100.resolution.'),
    ('RICHFUL_RF6077', 'tier2.density', True, 'User decision of 2026-10-18 kept; see fields.density.resolution.'),
    ('RICHFUL_RF6077', 'tier2.kv100', True, 'User decision of 2026-10-18 kept; see fields.kv100.resolution.'),
    ('RICHFUL_RF6078', 'treat_rate_matrix', True, "See fields.treat_rate_matrix[0].treat_rate_wt_pct.resolution. The 'values' "
                                                   "in this entry are correct; the note text has the two files swapped."),
    ('RICHFUL_RF6078', 'tier2.density', True, 'See fields.density.resolution.'),
    ('RICHFUL_RF6081', 'tier2.kv100', True, 'See fields.kv100.resolution.'),
    ('RICHFUL_RF6088F', 'tier2.density', True, 'User decision of 2026-10-18 kept; see fields.density.resolution.'),
    ('RICHFUL_RF6088F', 'tier2.kv100', True, 'User decision of 2026-10-18 kept; see fields.kv100.resolution.'),
    ('RICHFUL_RF6406', 'treat_rate_matrix', True, 'See fields.treat_rate_matrix[10].treat_rate_wt_pct.resolution.'),
    ('RICHFUL_RF6406', 'tier2.tbn', True, 'See fields.tbn.resolution.'),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', '"field": "density"', True, 'No value conflict: a note that the density is at 15.6 °C, not 15 °C.'),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', '"field": "sulfur"', False, 'UNRESOLVED; see tier3 fields.sulfur.resolution.'),
    ('ERGON_HYGOLD_L750', 'density_at_15_6_c', False, 'UNRESOLVED; see tier1 fields.density.resolution.'),
    ('FORMOSA_150N_GII_PLUS', 'flash_point', True, 'TDS preferred over SDS; see tier2 fields.flash_point.resolution.'),
    ('NYNAS_NS_3', '"property": "kv40"', True, f'{SAME_NEWEST}; see tier1 fields.kv40.resolution.'),
    ('NYNAS_NS_3', '"property": "density"', True, f'{SAME_NEWEST}; see tier1 fields.density.resolution.'),
    ('NYNAS_NS_3', '"property": "flash_point"', True, f'{SAME_NEWEST}; see tier2 fields.flash_point.resolution.'),
    ('NYNAS_NS_3', '"property": "sulfur"', True, f'{SAME_NEWEST}; see tier3 fields.sulfur.resolution.'),
    ('NYNAS_NYFROST_32', '"property": "kv40"', True, 'TDS preferred over SDS; see tier1 fields.kv40.resolution.'),
    ('NYNAS_NYFROST_32', '"property": "flash_point"', True, 'TDS preferred over SDS; see tier2 fields.flash_point.resolution.'),
    ('PETRONAS_ETRO_6_PLUS', '"property": "kv40"', True, 'TDS preferred over SDS; see tier1 fields.kv40.resolution.'),
    ('PETRONAS_ETRO_6_PLUS', '"property": "flash_point"', True, 'TDS preferred over SDS; see tier2 fields.flash_point.resolution.'),
    ('PETRONAS_ETRO_6_PLUS', '"property": "noack_volatility"', True, 'TDS preferred over SDS; see tier2 fields.noack_volatility.resolution.'),
    ('PETRONAS_ETRO_6_PLUS', '"property": "density"', True, 'TDS preferred over SDS; see tier1 fields.density.resolution.'),
    ('PETRO_CANADA_PURITY_L65', 'Viscosity index', True, 'TDS kept; see tier1 fields.viscosity_index.resolution.'),
    ('SHELL_RISELLA_X_415', '"field": "density"', True, 'TDS preferred over SDS; see tier1 fields.density.resolution.'),
    ('SHELL_RISELLA_X_420', '"field": "density"', True, 'TDS preferred over SDS; see tier1 fields.density.resolution.'),
    ('SHELL_RISELLA_X_430', '"field": "density"', True, 'TDS preferred over SDS; see tier1 fields.density.resolution.'),
]


def family(path):
    keys = [k for k in re.split(r'[.\[\]]', path) if k and not k.isdigit()]
    return FAMILY.get(keys[-1]) if keys else None


def scale(v, factor, places=None):
    out = Decimal(str(v)) * Decimal(factor)
    if places is not None:
        out = round(out, places)
    out = out.normalize()
    return int(out) if out == out.to_integral_value() else float(out)


def first_number(text):
    m = re.search(r'-?\d+(?:\.\d+)?', str(text or '').replace(',', ''))
    return float(m.group(0)) if m else None


def normalise(node, path):
    """Add value_final / unit_final (and min/max_final) to one value object."""
    if 'value_final' in node:  # re-run: drop only what an earlier run added
        for k in OWN_KEYS:
            node.pop(k, None)
    fam, unit, flags = family(path), node.get('unit'), []
    numeric = any(isinstance(node.get(k), (int, float)) and not isinstance(node.get(k), bool) for k in ('value', 'min', 'max'))
    node['value_final'] = node.get('value')
    if not fam or 'unit' not in node:
        return flags
    if fam == 'vi':
        node['unit_final'] = 'unitless'
        return flags
    rule = UNITS[fam].get(str(unit).strip().lower()) if unit else None
    if rule is None:
        node['unit_final'] = unit
        if numeric:
            if str(unit).strip().lower() in NOT_CONVERTED:
                flags.append(f'{NOT_CONVERTED[str(unit).strip().lower()]} is not a density; kept as printed, not converted to g/cm³')
            elif str(unit).strip() == '%':
                flags.append("printed '%' with no mass/volume basis; kept as '%', not converted to wt.%")
            else:
                flags.append(f'unit {unit!r} not recognised or not printed; kept as printed')
    else:
        final_unit, factor = rule
        places = 4 if factor == '0.119826427' else None
        node['unit_final'] = final_unit
        for k in ('value', 'min', 'max'):
            v = node.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                node[f'{k}_final'] = scale(v, factor, places)
        if numeric and factor != '1':
            node['unit_conversion'] = f'{unit} -> {final_unit} (x{factor})'
        if fam == 'density' and isinstance(node.get('value_final'), (int, float)) and not 0.6 <= node['value_final'] <= 1.3:
            printed = first_number(node.get('printed_text'))
            fixed = scale(printed, factor) if printed is not None else None
            if fixed is not None and 0.6 <= fixed <= 1.3:
                node['value_final'] = fixed
                node['unit_conversion'] = (f"value field {node.get('value')} does not match printed text "
                                           f"{node.get('printed_text')!r} in {unit}; value_final taken from the printed text")
            else:
                flags.append(f"converted density {node['value_final']} g/cm³ is outside 0.6-1.3, so the printed number "
                             f"and unit disagree; value_final left null until checked")
                node['value_final'] = None
    if fam == 'density' and numeric and node.get('test_temperature_c') != 15:
        t = node.get('test_temperature_c')
        flags.append('density printed with no temperature' if t is None else
                     f'density is at {t} °C, not 15 °C; not temperature-corrected')
    return flags


def walk(node, path, out):
    if isinstance(node, dict):
        if 'status' in node and 'value' in node and not isinstance(node['status'], dict):
            flags = normalise(node, path)
            if flags:
                node['integration_flags'] = flags
            out[path] = node
        for k, v in node.items():
            if k not in ('source', 'alternate_entries') and k not in OWN_KEYS:
                walk(v, f'{path}.{k}' if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f'{path}[{i}]', out)


def long_path(p):
    """Windows extended-length path so files beyond the 260-character limit are never skipped."""
    s = str(p)
    return '\\\\?\\' + s if os.name == 'nt' and not s.startswith('\\\\?\\') else s


def fmt_of(raw):
    return dict(ensure_ascii='\\u' in raw, tail='\n' if raw.endswith(('\n', '\r\n')) else '',
                nl='\r\n' if '\r\n' in raw else '\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--input', default='Products_json', help='product JSON folder (default: Products_json)')
    ap.add_argument('--dry-run', action='store_true', help='report what would change without writing')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if not os.path.isdir(args.input):
        sys.exit(f'input folder not found: {args.input}')
    files = sorted(glob.glob(os.path.join(os.path.abspath(args.input), '**', '*.json'), recursive=True))
    used_overrides, used_conflicts, unmatched, flag_count, changed = set(), set(), [], {}, 0
    for f in files:
        raw = open(long_path(f), encoding='utf-8', newline='').read()
        d = json.loads(raw)
        product, tier = os.path.basename(os.path.dirname(f)), d.get('tier')
        nodes = {}
        walk(d.get('fields', {}), '', nodes)
        for (p, t, path), ov in OVERRIDES.items():
            if p == product and t == tier:
                node = nodes.get(path)
                if node is None:
                    sys.exit(f'override path not found: {p} tier {t} {path}')
                if 'value' in ov:  # a range from the replaced source must not sit next to the chosen value
                    node.pop('min_final', None)
                    node.pop('max_final', None)
                for k, v in ov.items():
                    node['value_final' if k == 'value' else k] = v
                used_overrides.add((p, t, path))
        for i, c in enumerate(d.get('conflicts', [])):
            if isinstance(c, str):
                c = d['conflicts'][i] = {'note': c}
            text = json.dumps({k: v for k, v in c.items() if k not in ('final_resolution', 'resolved')}, ensure_ascii=False)
            hit = [x for x in CONFLICTS if x[0] == product and x[1] in text]
            if len(hit) != 1:
                unmatched.append((f, text[:120], len(hit)))
                continue
            c['resolved'], c['final_resolution'] = hit[0][2], hit[0][3]
            used_conflicts.add(hit[0][:2])
        for n in nodes.values():
            for fl in n.get('integration_flags', []):
                key = re.sub(r"[-\d.]+ °C|'[^']*'|\d[\d.]*", '#', fl)
                flag_count[key] = flag_count.get(key, 0) + 1
        fm = fmt_of(raw)
        new = (json.dumps(d, indent=2, ensure_ascii=fm['ensure_ascii']) + fm['tail']).replace('\n', fm['nl'])
        if new != raw:
            changed += 1
            if not args.dry_run:
                with open(long_path(f), 'w', encoding='utf-8', newline='') as fh:
                    fh.write(new)
    missing_ov = set(OVERRIDES) - used_overrides
    missing_cf = {x[:2] for x in CONFLICTS} - used_conflicts
    print(f"{'DRY RUN: ' if args.dry_run else ''}files {len(files)}, changed {changed}, "
          f"overrides applied {len(used_overrides)}/{len(OVERRIDES)}, conflict rules used {len(used_conflicts)}/{len(CONFLICTS)}")
    for k, v in sorted(flag_count.items(), key=lambda x: -x[1]):
        print(f'  flag x{v}: {k}')
    for x in unmatched:
        print('  UNMATCHED CONFLICT', x)
    for x in sorted(missing_ov) + sorted(missing_cf):
        print('  UNUSED RULE', x)
    return 1 if unmatched or missing_ov or missing_cf else 0


if __name__ == '__main__':
    sys.exit(main())
