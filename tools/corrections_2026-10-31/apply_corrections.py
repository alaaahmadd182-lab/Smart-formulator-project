"""Apply the approved source-backed corrections (CF-136, CF-142/143 + Zn/S, CF-159, CF-180). Asserts the current state first."""
import copy, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
REPO = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project'
os.chdir(REPO)
PJ = 'Products_json/'
TODAY = '2026-10-31'


def load(f):
    raw = open(f, encoding='utf-8', newline='').read()
    return raw, json.loads(raw)


def save(f, raw, d):
    nl = '\r\n' if '\r\n' in raw else '\n'
    tail = '\n' if raw.endswith(('\n', '\r\n')) else ''
    out = (json.dumps(d, ensure_ascii=False, indent=2) + tail).replace('\n', nl)
    assert out != raw
    open(f, 'w', encoding='utf-8', newline='').write(out)
    print('written', f)


def src(file, page, rev):
    return {'file': file, 'page': page, 'revision_date': rev}


# ---- CF-136: Synfluid Dimer C12 pour point -------------------------------------------------------
f = PJ + 'Base_oils_json/CHEVRON/CHEVRON_SYNFLUID_DIMER_C12/CHEVRON_SYNFLUID_DIMER_C12__base_oil_tier2_verification.json'
raw, d = load(f)
pp = d['fields']['pour_point']
assert (pp['value'], pp['printed_text'], pp['unit'], pp['source']['file'], pp['source']['page']) == (-63, '-63', '°C', 'DL2-13202.pdf', 1)
assert pp['calculation_note'] is None and 'notes' not in pp and not d['conflicts']
pp.update(
    value=-53,
    printed_text='Pour Point, °F, °C -53 (-63)',
    calculation_note=(
        "'Typical Properties' table, p.1 (sheet dated 'Revision Date April 2011'). The row label reads '°F, °C' "
        "but the pair is printed '-53 (-63)'. Read in label order this would be -53 °F with -63 °C, which do not "
        "convert (-53 °F is about -47 °C; -63 °C is about -81 °F). The pair is consistent only as -53 °C (-63 °F): "
        "-53 × 1.8 + 32 = -63.4. The other °F, °C rows of this sheet are consistent in label order (Flash Point "
        "(COC) 362 (183), Fire Point (COC) 396 (202)). The C12 Dimer column of the Synfluid C12 table "
        "DL2-13200.pdf p.1 prints 'Pour Point, °C (°F) -53 (-63)', and the Chevron Phillips 'Synfluid® Dimer C12' "
        "data sheet (revision June 2012; copy in reconciliation/audit_evidence) prints 'Pour Point, °C (°F) "
        "ASTM D5950 -53 (-63)'. DL2-13202.pdf prints no method, so method is left null."),
)
keys = list(pp)
pp_new = {}
for k in keys:
    if k == 'value_final':
        pp_new['notes'] = (f"Correction {TODAY} (audit CF-136): this field previously stored -63 °C with printed_text '-63', "
                           "taking the second number of the pair in the row-label order (°F, °C). Corrected to -53 °C "
                           "on the evidence in calculation_note; the full printed row is quoted in printed_text.")
    pp_new[k] = pp[k]
pp_new['value_final'], pp_new['unit_final'] = -53, '°C'
d['fields']['pour_point'] = pp_new
save(f, raw, d)

# ---- CF-142 / CF-143: Lubrizol sulfated ash + omitted Zn and S ---------------------------------
LUB = {
    'CV1100': dict(file='DL2-11503.pdf', rev='2017-11-08', ash=7, old=5.8, ca=1.705,
                   zn=(0.778, 0.7, 0.856, 'ZINC 0.700 0.778 0.856'), s=(2.35, 'SULFUR 2.35')),
    'CV3515': dict(file='DL2-15722.pdf', rev='2017-10-09', ash=10, old=9.2, ca=2.706,
                   zn=(0.772, 0.695, 0.85, 'ZINC 0.695 0.772 0.850'), s=(2.4, 'SULFUR 2.4')),
}
TABLE = ("Chemical Characteristics table: header 'Minimum % Weight | Typical | Maximum % Weight' on p.1; "
         "the table continues on p.2 without a new header (rows in alphabetical order after PHOSPHORUS on p.1).")
for prod, x in LUB.items():
    f = PJ + f'Additive_packages_json/Lubrizol/LUBRIZOL_{prod}/tier2_numeric_contribution.json'
    raw, d = load(f)
    F = d['fields']
    sa, zn, s = F['sulfated_ash'], F['elements']['Zn'], F['elements']['S']
    assert sa['value'] == x['old'] and sa['status'] == 'Calculated' and sa['source']['file'] is None and 'alternate_entries' not in sa
    assert f"{x['ca']} (Ca)" in sa['calculation_note'] and 'Mg/Zn not reported' in sa['calculation_note']
    for e in (zn, s):
        assert e['status'] == 'Missing' and e['value'] is None and e['source']['file'] is None and e['unit'] == 'wt.%'
    # historical estimate kept as an alternate (no *_final keys: alternates are not normalised)
    alt = {k: copy.deepcopy(v) for k, v in sa.items() if not k.endswith('_final')}
    alt['notes'] = (sa['notes'] + f" Historical estimate, superseded {TODAY} (audit CF-142/CF-143): it took Zn as 0 "
                    f"('Mg/Zn not reported'), but this data sheet prints ZINC {x['zn'][0]} typical (p.2). It is a "
                    "calculation, not a reported measurement, and is kept for provenance only.")
    F['sulfated_ash'] = {
        'value': x['ash'], 'qualifier': None, 'min': None, 'max': None, 'value_kind': 'typical',
        'printed_text': f"SULFATED ASH {x['ash']}", 'unit': 'wt.%', 'test_temperature_c': None, 'method': None,
        'status': 'Reported',
        'calculation_note': f"Column 'Typical'; no Minimum/Maximum printed for this row. {TABLE} No test method printed.",
        'source': src(x['file'], 2, x['rev']),
        'notes': (f"Correction {TODAY} (audit CF-142/CF-143): this field previously held the calculated estimate "
                  f"{x['old']} wt.% (status Calculated), now kept in alternate_entries. The product data sheet prints a "
                  "typical sulfated ash, recorded here as Reported."),
        'alternate_entries': [alt],
        'value_final': x['ash'], 'unit_final': 'wt.%',
    }
    v, lo, hi, pt = x['zn']
    F['elements']['Zn'] = {
        'value': v, 'qualifier': None, 'min': lo, 'max': hi, 'value_kind': 'typical', 'printed_text': pt,
        'unit': 'wt.%', 'test_temperature_c': None, 'method': None, 'status': 'Reported',
        'calculation_note': f"Column 'Typical' with Minimum/Maximum limits. {TABLE} No test method printed.",
        'source': src(x['file'], 2, x['rev']),
        'notes': f"Added {TODAY} (audit CF-142/CF-143 follow-up): printed on p.2 but previously recorded as Missing.",
        'value_final': v, 'unit_final': 'wt.%', 'min_final': lo, 'max_final': hi,
    }
    v, pt = x['s']
    F['elements']['S'] = {
        'value': v, 'qualifier': None, 'min': None, 'max': None, 'value_kind': 'typical', 'printed_text': pt,
        'unit': 'wt.%', 'test_temperature_c': None, 'method': None, 'status': 'Reported',
        'calculation_note': f"Column 'Typical'; no Minimum/Maximum printed for this row. {TABLE} No test method printed.",
        'source': src(x['file'], 2, x['rev']),
        'notes': f"Added {TODAY} (audit CF-142/CF-143 follow-up): printed on p.2 but previously recorded as Missing.",
        'value_final': v, 'unit_final': 'wt.%',
    }
    save(f, raw, d)

# ---- CF-159: RF6066 KV100 conflict note ------------------------------------------------------------
f = PJ + 'Additive_packages_json/Richful/RICHFUL_RF6066/tier2_numeric_contribution.json'
raw, d = load(f)
c = d['conflicts'][1]
assert c['field'] == 'tier2.kv100' and c['resolved'] is False
assert c['note'] == 'At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.'
assert c['values'][3]['printed_text'] == 'Viscosity, dynamic : 185 mm²/s (100 °C)' and d['fields']['kv100']['value'] == 185
c['note'] += (f" [Review {TODAY}, audit CF-159: (1) 'field left null' describes the archive documents only; since "
              "2026-10-17 fields.kv100 holds 185 mm²/s from the Richful product page (open question 6, fields.kv100.notes). "
              "The conflict between the documents is still unresolved. (2) DL2-15831.pdf p.5 (SDS, 2021-09-02, read "
              "visually) prints 185 on its 'Viscosity, dynamic' line with the kinematic unit mm²/s (100 °C), while its "
              "'Viscosity, kinematic' line reads 'Not available'. Label and unit disagree, so it is uncertain whether this "
              "SDS value is a kinematic viscosity; the value is kept as printed. Confirm with Richful.]")
save(f, raw, d)

# ---- CF-180: RF6078 treat-rate conflict, incorrect statement in the kept PR #2 proposal -----------
f = PJ + 'Additive_packages_json/Richful/RICHFUL_RF6078/tier1_route_defining.json'
raw, d = load(f)
c = d['conflicts'][0]
claim = "The 'values' in this entry are correct; the note text has the two files swapped."
assert c['field'] == 'tier1.treat_rate_matrix (ACEA E7/API CI-4)' and c['resolved'] is False and claim in c['final_resolution']
c['final_resolution'] += (f" [Review {TODAY}, audit CF-180: the statement \"{claim}\" was checked against both PDFs and is "
                          "incorrect. DL2-15832.pdf p.1 prints 'ACEA E7/API CI-4 11.85%' and 'API CI-4 10.85%'; "
                          "'RF6078 - TDS.pdf' p.1 prints 'ACEA E7/API CI-4 10.85%' and 'API CI-4 Plus 11.85%'. The note "
                          "and the values are both correct. The conflict remains unresolved.]")
save(f, raw, d)
