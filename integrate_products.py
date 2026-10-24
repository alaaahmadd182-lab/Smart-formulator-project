#!/usr/bin/env python3
"""Data integration: add a normalised value and unit beside every product property, without changing it.

Usage: python integrate_products.py [--input Products_json] [--write]
Without --write nothing is written (dry run). With --write, files are written only if the whole run passes
every check; on any error nothing is written and the exit code is 1.

Adds keys next to the existing data; never removes or edits an existing key:
  value_final, unit_final, min_final, max_final   every value object (numeric ones converted)
  unit_conversion                                 how value_final was derived from the printed unit
  integration_flags                               anything the conversion could not settle
  resolution                                      reviewed note on properties listed in ANNOTATIONS
  resolved, final_resolution                      on conflict entries listed in CONFLICTS
Keys this script adds are dropped and re-derived on every run, so they cannot go stale. Conflict entries
are never restructured (a conflict stored as a string stays a string), and an existing resolved /
final_resolution annotation is never overwritten: a differing rule is an error, and so is an entry marked
resolved that no rule in CONFLICTS supports. Entries without a rule keep exactly what they record.

Unit rules (unit change only, no estimated values):
  viscosity cSt; density g/cm3 at the printed temperature (not corrected to 15 C);
  temperatures C; CCS/MRV/HTHS mPa.s; mass fractions wt.% (ppm / 10000).
  Specific gravity / relative density and bare '%' (basis not printed) are kept as printed and flagged.
  A density whose value and printed unit disagree is flagged and value_final left null; it is never
  replaced by a number read from the printed text.

Data rules (approved 2026-10-24):
  1. Conflicting datasheet values are never averaged. Both values and sources stay as recorded and the
     conflict stays unresolved unless authoritative evidence supports a resolution.
  2. TDS is never preferred over SDS, nor the reverse, automatically: measurement conditions, test methods,
     revision dates, source reliability and comparability are evaluated case by case.
  3. Coverage reports the validated status; this script never writes status_final or source_final.
So ANNOTATIONS may only attach a reviewed note to a property (never a value, status or source), and each
one names the field values it was reviewed against: if the field has changed since, the run fails.
"""
import argparse, copy, json, os, re, sys
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
    'visc': {u: ('cSt', '1') for u in ('cst', 'mm2/s', 'mm²/s', 'mm2/sec')},
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
# Every key this script has ever added (older runs also wrote the *_final keys after value_final); all are
# dropped before re-deriving, so a run on data from an older version removes them.
OWN_KEYS = ('value_final', 'unit_final', 'min_final', 'max_final', 'unit_conversion', 'integration_flags',
            'resolution', 'status_final', 'source_final', 'qualifier_final', 'method_final', 'test_temperature_c_final')
CONFLICT_KEYS = ('resolved', 'final_resolution')

NEWEST = 'Same document type; newest edition used'
# (product, tier, path) -> reviewed note. 'expect' lists the original keys of the field as they were when the
# note was reviewed (2026-10-24); 'source' compares source.file. Only 'expect' and 'resolution' are allowed.
ANNOTATIONS = {
    ('RICHFUL_RF6077', 2, 'density'): dict(
        expect=dict(value=0.991, unit='g/cm³', test_temperature_c=15, source='DL2-15542.pdf'),
        resolution="User decision of 2026-10-18 kept (SDS DL2-15542.pdf 0.991 g/cm³ at 15 °C); it overrides the "
                   "TDS-preferred rule, which would give TDS DL2-15536.pdf 998 kg/m³ at 20 °C."),
    ('RICHFUL_RF6077', 2, 'kv100'): dict(
        expect=dict(value=150, unit='mm²/s', test_temperature_c=100, source='DL2-15542.pdf'),
        resolution="User decision of 2026-10-18 kept (SDS DL2-15542.pdf 150 cSt); it overrides the TDS-preferred "
                   "rule, which would give TDS DL2-15536.pdf 160 cSt."),
    ('RICHFUL_RF6088F', 2, 'density'): dict(
        expect=dict(value=963.0, unit='kg/m³', test_temperature_c=20, source='DL2-15839.pdf'),
        resolution="User decision of 2026-10-18 kept (TDS DL2-15839.pdf 963 kg/m³ at 20 °C); agrees with TDS preferred over SDS "
                   "(SDS DL2-15840.pdf relative density 0.958 not used)."),
    ('RICHFUL_RF6088F', 2, 'kv100'): dict(
        expect=dict(value=178.2, unit='mm²/s', test_temperature_c=100, source='DL2-15840.pdf'),
        resolution="User decision of 2026-10-18 kept (SDS DL2-15840.pdf 178.2 cSt); it overrides the TDS-preferred "
                   "rule, which would give TDS DL2-15839.pdf 177 cSt."),
    ('NYNAS_NS_3', 1, 'kv40'): dict(
        expect=dict(value=2.92, unit='cSt', test_temperature_c=40, source='DL2-15474.pdf'),
        resolution=f"{NEWEST}: 2024 edition DL2-15474.pdf 2.92 cSt over 2016 edition DL2-12382.pdf 2.84 cSt."),
    ('NYNAS_NS_3', 1, 'density'): dict(
        expect=dict(value=0.863, unit='kg/dm3', test_temperature_c=15, source='DL2-15474.pdf'),
        resolution=f"{NEWEST}: 2024 edition DL2-15474.pdf 0.863 over 2016 edition DL2-12382.pdf 0.860."),
    ('NYNAS_NS_3', 2, 'flash_point'): dict(
        expect=dict(value=95, unit='°C', source='DL2-15474.pdf'),
        resolution=f"{NEWEST}: 2024 edition DL2-15474.pdf 95 °C over 2016 edition DL2-12382.pdf 94 °C."),
    ('NYNAS_NS_3', 3, 'sulfur'): dict(
        expect=dict(value=10, unit='ppm', source='DL2-15474.pdf'),
        resolution=f"{NEWEST}: 2024 edition DL2-15474.pdf 'Typical < 10 ppm' over 2016 edition DL2-12382.pdf "
                   "30 ppm. '<10 ppm' is a typical result below the reporting limit, not a specification bound, "
                   "so the measured-beats-bound rule does not apply."),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', 3, 'sulfur'): dict(
        expect=dict(value=1.3, unit='wt.%', source='DL2-12173.pdf'),
        resolution="UNRESOLVED: DL2-13944.pdf prints '1.3 ppm' and DL2-12173.pdf prints 'Max WT% 1.3'. Same number, "
                   "units 10,000x apart, so one sheet is almost certainly misprinted. The rules cannot pick between them; "
                   "confirm with Aramco. value_final shows the field as it stands."),
    ('ERGON_HYGOLD_L750', 1, 'density'): dict(
        expect=dict(value=0.854, unit='g/cm3', test_temperature_c=15.6, source='DL2-10414.pdf'),
        resolution="UNRESOLVED: a single TDS (DL2-10414.pdf) prints density 0.854 g/cm³ and specific gravity 0.9183 at "
                   "15.6 °C, which contradict each other. This is not a two-document conflict, so the rules do not apply; "
                   "confirm with Ergon. value_final shows the density as printed."),
}

# (product, substring of the conflict entry, resolved?, basis, note). Only these entries are annotated; every
# other conflict entry is left exactly as recorded (including any annotation already on it).
# resolved=True is allowed only on the bases in RESOLVING_BASES.
RESOLVING_BASES = {'newer dated edition of the same document', 'user decision 2026-10-18', 'no value conflict'}
CONFLICTS = [
    ('AFTON_HITEC_12200', 'MTU 2.0', True, 'newer dated edition of the same document',
     f'{NEWEST} (08/18 bulletin: not claimed); text value, not averaged. Fields already hold it.'),
    ('AFTON_HITEC_12200', 'DDC 93K215', True, 'newer dated edition of the same document',
     f'{NEWEST} (08/18 bulletin: claimed); text value, not averaged. Fields already hold it.'),
    ('LUBRIZOL_CV7540', 'CES 20076', True, 'newer dated edition of the same document', f"{NEWEST} (2022 sheet: 'A - Approved'); text value, not averaged."),
    ('LUBRIZOL_CV7540', 'CES 20077', True, 'newer dated edition of the same document', f"{NEWEST} (2022 sheet: 'A - Approved'); text value, not averaged."),
    ('LUBRIZOL_CV7540', 'CES 20078', True, 'newer dated edition of the same document', f"{NEWEST} (2022 sheet: 'A - Approved'); text value, not averaged."),
    ('RICHFUL_RF6077', 'tier2.density', True, 'user decision 2026-10-18', 'User decision of 2026-10-18 kept; see fields.density.resolution.'),
    ('RICHFUL_RF6077', 'tier2.kv100', True, 'user decision 2026-10-18', 'User decision of 2026-10-18 kept; see fields.kv100.resolution.'),
    ('RICHFUL_RF6088F', 'tier2.density', True, 'user decision 2026-10-18', 'User decision of 2026-10-18 kept; see fields.density.resolution.'),
    ('RICHFUL_RF6088F', 'tier2.kv100', True, 'user decision 2026-10-18', 'User decision of 2026-10-18 kept; see fields.kv100.resolution.'),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', '"field": "density"', True, 'no value conflict',
     'No value conflict: a note that the density is at 15.6 °C, not 15 °C.'),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', '"field": "sulfur"', False, 'unresolved', 'UNRESOLVED; see tier3 fields.sulfur.resolution.'),
    ('ERGON_HYGOLD_L750', 'density_at_15_6_c', False, 'unresolved', 'UNRESOLVED; see tier1 fields.density.resolution.'),
    ('NYNAS_NS_3', '"property": "kv40"', True, 'newer dated edition of the same document', f'{NEWEST}; see tier1 fields.kv40.resolution.'),
    ('NYNAS_NS_3', '"property": "density"', True, 'newer dated edition of the same document', f'{NEWEST}; see tier1 fields.density.resolution.'),
    ('NYNAS_NS_3', '"property": "flash_point"', True, 'newer dated edition of the same document', f'{NEWEST}; see tier2 fields.flash_point.resolution.'),
    ('NYNAS_NS_3', '"property": "sulfur"', True, 'newer dated edition of the same document', f'{NEWEST}; see tier3 fields.sulfur.resolution.'),
]


def check_tables():
    """Refuse to start if a table could set a value, status or source, or resolve on an unapproved basis."""
    errors = []
    for key, a in ANNOTATIONS.items():
        if set(a) != {'expect', 'resolution'}:
            errors.append(f'annotation {key} may only carry expect + resolution, has {sorted(a)}')
    for p, sub, resolved, basis, note in CONFLICTS:
        if resolved and basis not in RESOLVING_BASES:
            errors.append(f'conflict rule {p} {sub!r}: resolved=True on basis {basis!r}')
    return errors


def family(path):
    keys = [k for k in re.split(r'[.\[\]]', path) if k and not k.isdigit()]
    return FAMILY.get(keys[-1]) if keys else None


def scale(v, factor, places=None):
    out = Decimal(str(v)) * Decimal(factor)
    if places is not None:
        out = round(out, places)
    out = out.normalize()
    return int(out) if out == out.to_integral_value() else float(out)


def normalise(node, path):
    """Add value_final / unit_final (and min/max_final) to one value object."""
    for k in OWN_KEYS:  # re-run: drop only what a run of this script added
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


def noted(node, path, out):
    """Paths of value objects that already carry a resolution note (read-only)."""
    if isinstance(node, dict):
        if 'status' in node and 'value' in node and not isinstance(node['status'], dict) and node.get('resolution'):
            out.add(path)
        for k, v in node.items():
            if k not in ('source', 'alternate_entries') and k not in OWN_KEYS:
                noted(v, f'{path}.{k}' if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            noted(v, f'{path}[{i}]', out)


def original(d):
    """The document without any key this script adds; must be identical before and after a run."""
    d = copy.deepcopy(d)
    def rec(n):
        if isinstance(n, dict):
            for k in OWN_KEYS:
                n.pop(k, None)
            for v in n.values(): rec(v)
        elif isinstance(n, list):
            for v in n: rec(v)
    rec(d.get('fields', {}))
    return d


def long_path(p):
    """Windows extended-length path so files beyond the 260-character limit are never skipped."""
    s = os.path.normpath(os.path.abspath(str(p)))
    return '\\\\?\\' + s if os.name == 'nt' and not s.startswith('\\\\?\\') else s


def discover(root):
    """Every .json file under root (os.walk on the extended-length path, so long paths are not missed)."""
    found = []
    for dirpath, _, filenames in os.walk(long_path(root)):
        found += [os.path.join(dirpath, f) for f in filenames if f.lower().endswith('.json')]
    return sorted(found)


def fmt_of(raw):
    return dict(ensure_ascii='\\u' in raw, tail='\n' if raw.endswith(('\n', '\r\n')) else '',
                nl='\r\n' if '\r\n' in raw else '\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--input', default='Products_json', help='product JSON folder (default: Products_json)')
    ap.add_argument('--write', action='store_true', help='write the files (default: dry run, nothing is written)')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if not os.path.isdir(args.input):
        sys.exit(f'input folder not found: {args.input}')
    errors = check_tables()
    if errors:
        print('\n'.join('  TABLE ERROR ' + e for e in errors))
        return 1
    files = discover(args.input)
    used_annotations, used_conflicts, kept_annotations, flag_count, pending = set(), set(), 0, {}, []
    for f in files:
        with open(f, encoding='utf-8', newline='') as fh:
            raw = fh.read()
        d = json.loads(raw)
        before = original(d)
        product, tier = os.path.basename(os.path.dirname(f)), d.get('tier')
        existing = set()
        noted(d.get('fields', {}), '', existing)
        for path in sorted(existing):
            if (product, tier, path) not in ANNOTATIONS:
                errors.append(f'{f}: {path} carries a resolution note that is not in ANNOTATIONS; it would be lost')
        nodes = {}
        walk(d.get('fields', {}), '', nodes)
        for (p, t, path), a in ANNOTATIONS.items():
            if p != product or t != tier:
                continue
            node = nodes.get(path)
            if node is None:
                errors.append(f'annotation path not found: {p} tier {t} {path}')
                continue
            src = node.get('source') if isinstance(node.get('source'), dict) else {}
            now = {k: (src.get('file') if k == 'source' else node.get(k)) for k in a['expect']}
            if now != a['expect']:
                errors.append(f'annotation {p} tier {t} {path} was reviewed against {a["expect"]}, field now {now}; review it again')
                continue
            node['resolution'] = a['resolution']
            used_annotations.add((p, t, path))
        for i, c in enumerate(d.get('conflicts', [])):
            if not isinstance(c, dict):
                continue  # a conflict stored as text is left exactly as recorded
            text = json.dumps({k: v for k, v in c.items() if k not in CONFLICT_KEYS}, ensure_ascii=False)
            hit = [x for x in CONFLICTS if x[0] == product and x[1] in text]
            if len(hit) > 1:
                errors.append(f'{f}: conflict {i} matches {len(hit)} rules')
                continue
            if not hit:
                if c.get('resolved') is True:
                    errors.append(f'{f}: conflict {i} is marked resolved but no reviewed rule in CONFLICTS supports it')
                elif any(k in c for k in CONFLICT_KEYS):
                    kept_annotations += 1  # unresolved, with its recorded note; kept as it is
                continue
            want = {'resolved': hit[0][2], 'final_resolution': hit[0][4]}
            have = {k: c[k] for k in CONFLICT_KEYS if k in c}
            if have and have != want:
                errors.append(f'{f}: conflict {i} already carries a different annotation {have}; not overwritten')
                continue
            c.update(want)
            used_conflicts.add(hit[0][:2])
        if original(d) != before:
            errors.append(f'{f}: an original key would change; nothing written')
        for n in nodes.values():
            for fl in n.get('integration_flags', []):
                key = re.sub(r"[-\d.]+ °C|'[^']*'|\d[\d.]*", '#', fl)
                flag_count[key] = flag_count.get(key, 0) + 1
        fm = fmt_of(raw)
        new = (json.dumps(d, indent=2, ensure_ascii=fm['ensure_ascii']) + fm['tail']).replace('\n', fm['nl'])
        if new != raw:
            pending.append((f, new))
    errors += [f'unused annotation {x}' for x in sorted(set(ANNOTATIONS) - used_annotations)]
    errors += [f'unused conflict rule {x}' for x in sorted({x[:2] for x in CONFLICTS} - used_conflicts)]
    write = args.write and not errors
    if write:
        for f, new in pending:
            with open(f, 'w', encoding='utf-8', newline='') as fh:
                fh.write(new)
    print(f"{'WRITTEN' if write else 'DRY RUN (nothing written)'}: files {len(files)}, would change {len(pending)}, "
          f"annotations applied {len(used_annotations)}/{len(ANNOTATIONS)}, conflict rules used "
          f"{len(used_conflicts)}/{len(CONFLICTS)}, other annotated conflicts kept {kept_annotations}")
    for k, v in sorted(flag_count.items(), key=lambda x: -x[1]):
        print(f'  flag x{v}: {k}')
    for e in errors:
        print('  ERROR', e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
