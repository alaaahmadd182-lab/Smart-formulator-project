"""Write the version-3 reconciliation/comprehensive_conflicts_audit.md and .csv from audit/findings_v3.json."""
import collections, csv, io, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

CAT = {'C01': 'Conflicting values for the same product', 'C02': 'Contradiction between document types (TDS/PDS/SDS/COA/specification)',
       'C03': 'Edition or revision difference', 'C04': 'Test method, temperature, unit or condition difference', 'C05': 'Typical value vs specification, limit or range',
       'C06': 'Classification contradiction (API group, chemistry, function)', 'C07': 'Inconsistency across JSON tiers', 'C08': 'Reported without adequate source evidence',
       'C09': 'Status inconsistent with available evidence', 'C10': 'Unsupported assumption, conversion or derived value', 'C11': 'Original value vs normalised *_final value',
       'C13': 'Product identity, supplier or reference mismatch', 'C14': 'Documentation omitted, incorrectly resolved or duplicated'}
TYPES = ['Genuine contradiction', 'Edition difference', 'Explainable difference', 'Data-quality issue']
BASIS = {'Genuine contradiction': 'Values for the same product and property that cannot both be right as printed, with no documented method, condition or edition that explains them.',
         'Edition difference': 'Values (or claims) that differ between dated editions, or editions of one document series, of the supplier\'s documents.',
         'Explainable difference': 'Values that differ, but the documents themselves state a different method, condition, unit, bound type or classification basis.',
         'Data-quality issue': 'A problem in how the JSON or a supplier document records a value, unit, label, derivation rule or identity.'}
F = json.load(open(os.path.join(A.SCR, 'audit', 'findings_v3.json'), encoding='utf-8'))
V2 = {r['conflict_id']: r for r in csv.DictReader(open(os.path.join(A.SCR, 'backup_v2', 'comprehensive_conflicts_audit.csv'), encoding='utf-8-sig'))}
LOG = json.load(open(os.path.join(A.SCR, 'audit', 'corrections_v3.json'), encoding='utf-8'))
CAND = json.load(open(os.path.join(A.SCR, 'audit', 'candidates.json'), encoding='utf-8'))
OUT = os.path.join(A.REPO, 'reconciliation')
CLS = [('base_oil', 'Base oils'), ('additive_package', 'Additive packages'), ('additive_component', 'Additive components')]
C = collections.Counter


def level(f):
    l = f['verification'].lower()
    if l.startswith('pending'): return 'Pending'
    if l.startswith('partially'): return 'Partially verified'
    if 'json-only' in l or 'json printed_text only' in l: return 'JSON-only'
    return 'Verified'


def md(s, n=None):
    s = re.sub(r'\s+', ' ', str(s if s is not None else '')).replace('|', '\\|')
    return s if n is None or len(s) <= n else s[:n - 1] + '…'


def vtext(v, src=True):
    s = ' '.join(x for x in (str(v.get('value')) if v.get('value') is not None else '', str(v.get('unit') or '')) if x).strip()
    cond = '; '.join(str(x) for x in (v.get('conditions'), v.get('temperature_c') and f"{v['temperature_c']} °C") if x)
    if cond: s += f' ({cond})'
    if v.get('printed_text') and str(v['printed_text']) not in s: s += f' — printed: "{v["printed_text"]}"'
    if src and v.get('file'):
        s += f" — {v['file']}" + (f" p.{v['page']}" if v.get('page') not in (None, '') else '') + (f", {v['revision_date']}" if v.get('revision_date') else '') + \
             (f" [{v['doc_type']}]" if v.get('doc_type') else '')
    return s


uncertain = lambda f: f['comparability'].startswith(('Uncertain', 'Partly uncertain'))
# ------------------------------------------------------------------ CSV
cols = ['conflict_id', 'material_class', 'supplier', 'product', 'record_id', 'property', 'conflict_category', 'finding_type', 'finding_type_basis', 'comparability',
        'nature', 'values', 'units_and_conditions', 'source_documents_and_pages', 'json_paths', 'tiers', 'explanation', 'verification_level', 'verification_status',
        'verification_priority', 'resolution_status', 'recorded_decision', 'outstanding_action', 'duplicate_of', 'related_ids', 'recommended_next_step', 'provenance',
        'affected_by_teammate_changes', 'changed_in_v3']
changed = collections.defaultdict(list)
for x in LOG: changed[x['id']].append(x['field'])
buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n'); w.writerow(cols)
for f in F:
    vals = f['values']
    w.writerow([f['id'], A.CLASS_LABEL[f['material_class']], f['supplier'], f['product'], f['record_id'], f['property'], f"{f['category']} {CAT[f['category']]}",
                f['group'], BASIS[f['group']], f['comparability'], f['nature'], ' || '.join(str(v.get('value')) for v in vals),
                ' || '.join('; '.join(str(x) for x in (v.get('unit'), v.get('conditions'), v.get('temperature_c') and f"{v['temperature_c']} °C", v.get('printed_text') and f'printed: {v["printed_text"]}') if x) for v in vals),
                ' || '.join(f"{v.get('file')}" + (f" p.{v['page']}" if v.get('page') not in (None, '') else '') + (f" ({v['revision_date']})" if v.get('revision_date') else '') + (f" [{v['doc_type']}]" if v.get('doc_type') else '') for v in vals if v.get('file')),
                ' ; '.join(f['json_paths']), ', '.join(sorted({m.group(1) for p in f['json_paths'] for m in [re.search(r'(tier\d|general|vm)', p)] if m})),
                f['explanation'], level(f), f['verification'], f['verification_priority'], f['resolution'], f['recorded_decision'], f['outstanding_action'],
                f['duplicate_of'], f['related_ids'], f['next_step'], f['provenance'], f['teammate'], ', '.join(sorted(set(changed.get(f['id'], [])) - {'verification_priority'})) or ''])
open(os.path.join(OUT, 'comprehensive_conflicts_audit.csv'), 'w', encoding='utf-8-sig', newline='').write(buf.getvalue())

# ------------------------------------------------------------------ numbers
types = C(f['group'] for f in F); v2types = C(r['finding_type'] for r in V2.values())
res = C(f['resolution'] for f in F); v2res = C(r['resolution_status'] for r in V2.values())
lv = C(level(f) for f in F)
n_doc = sum(1 for f in F if f['source_kind'] == 'documented'); n_new = sum(1 for f in F if f['provenance'].startswith('New'))
n_oq = sum(1 for f in F if 'open question only' in f['provenance']); n_notes = sum(1 for f in F if f['provenance'].startswith('Previously recorded in field notes'))
pend = [f for f in F if f['verification_priority']]; pr = C(f['verification_priority'].split(':')[0] for f in pend)
supplier_actions = [f for f in F if f['outstanding_action'].startswith('Supplier')]
gen_conf = [f for f in F if f['group'] == 'Genuine contradiction' and not uncertain(f)]; gen_unc = [f for f in F if f['group'] == 'Genuine contradiction' and uncertain(f)]
decisions = [f for f in F if f['recorded_decision'] and not f['recorded_decision'].startswith('PR #2')]
pc = [f for f in F if 'IM-1809E' in f['verification']]; so = [f for f in F if 'S-OIL web table' in f['verification']]
type_changes = [(x['id'], x['old'], x['new'], x['reason']) for x in LOG if x['field'] == 'group']
res_changes = [(x['id'], x['old'], x['new']) for x in LOG if x['field'] == 'resolution']

L = []; a = L.append
a('# Comprehensive conflicts audit — lubricant raw-material data')
a('')
a('Smart Formulator raw-material database (`Products_json`: 264 products, 706 JSON files). Branch `audit/comprehensive-conflicts` from `main` at `77ba590` '
  '(no newer commits on GitHub on 2026-10-30). Audit 2026-10-27, quality review 2026-10-27, source-verification review 2026-10-30 (this version). '
  'No product JSON, template, coverage workbook, integration script or the curated log `open_questions_and_conflicts.md` was changed; no conflict was '
  'resolved, averaged or settled by preferring one document type. Every finding is listed with the same ID in `comprehensive_conflicts_audit.csv`; '
  'evidence copies and hashes are in `audit_evidence/` (see `audit_evidence/evidence_manifest.md`).')
a('')
a('## Supervisor summary')
a('')
a('**What was examined.** All 706 records of the raw-material database. The 147 conflict entries already recorded (125 distinct conflicts) were checked '
  'against the exact pages and product columns of the cited supplier documents; independent checks then searched for unrecorded problems (internal '
  'consistency of every value, physical plausibility, API base-oil group definitions, and 1,116 comparisons with every other archive document naming '
  'the same product). Multi-product tables were read column by column; pages without a text layer were read on screen. External sources were '
  'obtained and archived with hashes: the Petro-Canada 2023.03 brochure, the S-OIL base-oil page, API 1509 Annex E, a Chevron Phillips data sheet, '
  'the ADNOC specification, PubChem registry records and archived Afton data sheets.')
a('')
a(f'**What was found.** {len(F)} findings (IDs CF-001 to CF-{len(F):03d}) in {len({f["record_id"] for f in F})} products, of which one pair records the same '
  f'disagreement twice, so {len(F) - sum(1 for f in F if f["duplicate_of"])} distinct issues:')
a('')
a('| Type | Count | Meaning |'); a('|---|---|---|')
a(f'| Genuine contradiction | {types["Genuine contradiction"]} ({len(gen_conf)} with comparable conditions confirmed, {len(gen_unc)} where comparability is uncertain) | {BASIS["Genuine contradiction"]} |')
for t in TYPES[1:]: a(f'| {t} | {types[t]} | {BASIS[t]} |')
a('')
a(f'{n_doc} findings were already recorded as conflicts (all preserved), {n_oq} only as open questions, {n_notes} only in field notes, '
  f'{len(F) - n_doc - n_new - n_oq - n_notes} elsewhere (identity review, integration flags); **{n_new} are new**.')
a('')
a('**Most important open contradictions.**')
for s in ['Synfluid C12 Dimer pour point: the archive sheet heads the column "°F, °C" but the values only fit °C (°F); the manufacturer\'s own sheet prints −53 °C (−63 °F), whereas the database stores −63 °C.',
          'Ergon HyGold L750: one data sheet prints density 0.854 g/cm³ and specific gravity 0.9183 at the same temperature; the SDS (0.92) supports the specific gravity.',
          'Lubrizol CV1100 and CV3515: calculated sulfated-ash values (5.8 and 9.2 wt.%) contradict the typical values printed in the products\' own data sheets (7 and 10 % weight); the database uses two different zinc factors across 26 calculated values.',
          'Richful RF6066, RF6069, RF6077: TDS and SDS kinematic viscosities differ by up to 42 mm²/s at 100 °C (same method); RF6077 density is lower at 15 °C than at 20 °C.',
          'Undocumented TDS vs SDS flash-point differences of 5–31 °C by the same open-cup method (Chevron Phillips Synfluid PAO 4/6/8, mPAO 150; ExxonMobil SpectraSyn Elite 150).',
          'S-OIL Ultra-S 4 SDS: the chemical name ("hydrotreated light paraffinic") and the CAS number (registered as "hydrotreated heavy paraffinic") do not match.',
          'aramcoPRIMA 70: the specification heading says Group II but allows a viscosity index below the API 1509 Group II minimum (76 vs 80).']:
    a(f'- {s}')
a('')
a(f'**Verification status.** {lv["Verified"]} findings verified in the product-specific source: the value, the product (and, in multi-product tables, the '
  f'column) for every finding, and the unit, qualifier, method, temperature and edition date wherever the comparison depends on them; '
  f'{lv["Partially verified"]} partially verified and {lv["Pending"]} pending. All {len(pc) - 1} Petro-Canada edition differences (plus the duplicate CF-093) and '
  f'all {len(so)} S-OIL edition differences, which rested on external web sources, are now verified column by column against archived copies. '
  f'{len(pend)} items still need evidence that could not be obtained (High {pr.get("High", 0)}, Medium {pr.get("Medium", 0)}, Low {pr.get("Low", 0)}; section 4), '
  f'and {len(supplier_actions)} unresolved findings can only be settled by the suppliers, who were not contacted.')
a('')
a(f'**Resolution labels.** No finding is scientifically resolved. Of the {len(decisions)} records the database marks as resolved, {len(decisions) - 1} hold a '
  'working value (a newer dated edition, or a user decision of 2026-10-18) and one is a temperature note; this audit keeps the decisions but lists the '
  'underlying disagreements as unresolved (section 6). Three records are not value conflicts (the temperature note and two sets of claims added or '
  'removed between bulletin editions).')
a('')
a('**Limitations.** ASTM D874 is not accessible, so the sulfated-ash factors are unchecked; two Afton editions could not be retrieved; product identity '
  'questions and missing test methods need the suppliers; 31 archive PDFs have no text layer (checked visually only where a finding depends on them); '
  'values that coincide with another grade\'s value in a multi-grade table can escape automated comparison.')
a('')
a('## 1. Summary tables')
a('')
a('| Type | ' + ' | '.join(l for _, l in CLS) + ' | Total |'); a('|---|' + '---|' * 4)
for t in TYPES:
    row = [sum(1 for f in F if f['group'] == t and f['material_class'] == k) for k, _ in CLS]; a(f'| {t} | ' + ' | '.join(map(str, row)) + f' | {sum(row)} |')
a('| **Total** | ' + ' | '.join(str(sum(1 for f in F if f['material_class'] == k)) for k, _ in CLS) + f' | **{len(F)}** |')
a('')
a('| Category | ' + ' | '.join(TYPES) + ' | Total |'); a('|---|' + '---|' * 5)
for c in sorted({f['category'] for f in F}):
    row = [sum(1 for f in F if f['category'] == c and f['group'] == t) for t in TYPES]; a(f'| {c} {CAT[c]} | ' + ' | '.join(map(str, row)) + f' | {sum(row)} |')
a('')
a('| Resolution status | Count |'); a('|---|---|')
for k, v in res.most_common(): a(f'| {k} | {v} |')
a('')
a('| Verification level | Count |'); a('|---|---|')
for k, v in lv.most_common(): a(f'| {k} | {v} |')
a('')
a('No findings in C07 (cross-tier), C08 (Reported without evidence) or C11 (stale normalised values). C12 (teammate changes) is a column on every finding.')
a('')
a('## 2. Repository state and the teammate\'s changes')
a('')
a('`origin/main` = `main` = `77ba590` (PR #3, identical tree to our reconciliation commit `a107745`); no newer commits, branches, pull requests or forks. '
  'PR #2 (Rawan-Mohammad: `53ed010`, `a38d5ca`, merged as `8a8d875`, 2026-10-24) added normalised `*_final` keys, resolution proposals and two scripts; '
  'PR #3 kept the normalised keys that still matched the validated values, removed 138 stale ones, and kept the 23 averaging or TDS-preference proposals '
  'as text marked "not adopted". This audit reports current problems only: stale keys removed in PR #3 are not findings, and the kept proposal texts are '
  'mentioned only where they are wrong (CF-180) or where the record still says resolved.')
a('')
a('## 3. Most significant unresolved contradictions')
a('')
SIG = [('CHEVRON_SYNFLUID_DIMER_C12', 'pour'), ('ERGON_HYGOLD_L750', 'density'), ('LUBRIZOL_CV1100', 'sulfated'), ('LUBRIZOL_CV3515', 'sulfated'),
       ('RICHFUL_RF6069', 'kv100'), ('RICHFUL_RF6066', 'tier2.kv100'), ('RICHFUL_RF6077', 'tier2.density'), ('EXXONMOBIL_SPECTRASYN_ELITE_150', 'flash'),
       ('CHEVRON_SYNFLUID_MPAO_150', 'flash'), ('S_OIL_ULTRA_S_4', 'CAS'), ('ARAMCO_LUBEREF_PRIMA_70', 'api_group'), ('PETRONAS_ETRO_6_PLUS', 'kv40'),
       ('NYNAS_NYFROST_32', 'flash'), ('MINGLAN_T3161A', 'sulfated'), ('TIANHE_P_TEC_3232', 'density'), ('ARAMCO_LUBEREF_PRIMA_70', 'tier2.flash'), ('RF6602', 'flash')]
a('| ID | Product | Property | Conflicting values | Type | Comparability | Verification |'); a('|---|---|---|---|---|---|---|')
for rid, kw in SIG:
    m = [f for f in F if f['record_id'] == rid and kw.lower() in f['property'].lower()]
    if not m: continue
    f = m[0]
    a(f"| {f['id']} | {md(f['product'])} | {md(f['property'], 45)} | {md(' vs '.join(vtext(v, False) for v in f['values'] if v.get('value') is not None or v.get('printed_text')), 230)} | "
      f"{f['group']} | {md(f['comparability'], 110)} | {md(f['verification'], 120)} |")
a('')
a('## 4. Items still pending')
a('')
a('| Priority | ID | Product | Property | What is missing | Outstanding action |'); a('|---|---|---|---|---|---|')
for lvl in ('High', 'Medium', 'Low'):
    for f in [x for x in pend if x['verification_priority'].startswith(lvl)]:
        a(f"| {lvl} | {f['id']} | {md(f['product'], 40)} | {md(f['property'], 45)} | {md(f['verification_priority'].split(': ', 1)[-1], 150)} | {md(f['outstanding_action'], 80)} |")
a('')
a(f'Beyond these, {len(supplier_actions)} unresolved findings are fully verified but can only be settled by the supplier (not contacted). The 16 checks left '
  'open by the previous version were completed where evidence was accessible: API 1509 Annex E (CF-145, CF-146, CF-147), the manufacturer\'s Dimer C12 '
  'sheet (CF-136), PubChem records for the CAS number (CF-171), the Ultra-S 6 catalog column (CF-172), the Infineum D3375 page (CF-158), the HiTEC 12200 '
  'and 12210M bulletins (CF-166, CF-167), the RF6602 product feed (CF-162), the Richful supplier spellings (CF-179), the PURITY L65 brochure (CF-093) and '
  'two of four HiTEC 5748 editions (CF-164). Still open: ASTM D874 (CF-144, not accessible), supplier-only questions (CF-140, CF-146, CF-147, CF-177, '
  'CF-178), two HiTEC 5748 editions (CF-164) and a low-priority confirmation (CF-145).')
a('')
a('## 5. Findings by type, comparability, material class and category')
a('')
groups = [('Genuine contradiction — comparability confirmed', gen_conf), ('Genuine contradiction — comparability uncertain (not a confirmed contradiction)', gen_unc)] + \
         [(t, [f for f in F if f['group'] == t]) for t in TYPES[1:]]
for gi, (title, sub_t) in enumerate(groups, 1):
    a(f'### 5.{gi} {title} ({len(sub_t)})'); a('')
    for k, label in CLS:
        sub = [f for f in sub_t if f['material_class'] == k]
        if not sub: continue
        a(f'#### {label} ({len(sub)})'); a('')
        a('| ID | Cat. | Supplier / product | Property | Values, conditions and sources | Comparability | Explanation | Verification | Status / recorded decision | Provenance |')
        a('|---|---|---|---|---|---|---|---|---|---|')
        for f in sorted(sub, key=lambda x: (x['category'], x['id'])):
            vals = '<br>'.join(md(vtext(v), 280) for v in f['values'])
            st = f['resolution'] + (f"; decision: {f['recorded_decision']}" if f['recorded_decision'] and not f['recorded_decision'].startswith('PR #2') else '')
            extra = (f"; duplicate of {f['duplicate_of']}" if f['duplicate_of'] else '') + (f"; related: {f['related_ids']}" if f['related_ids'] else '')
            prov = f['provenance'] + extra + ('; teammate: ' + f['teammate'] if f['teammate'].startswith('Yes') else '')
            a(f"| {f['id']} | {f['category']} | {md(f['supplier'], 35)} / {md(f['product'], 45)} | {md(f['property'], 60)} | {vals} | {md(f['comparability'], 160)} | "
              f"{md(f['explanation'], 380)} | {level(f)}: {md(f['verification'], 220)} | {md(st, 220)} | {md(prov, 180)} |")
        a('')
a('## 6. Resolution labels and recorded decisions')
a('')
a('Selecting a working value for a field is a recorded decision, not a scientific resolution of disagreeing sources. The database (JSON `resolved: true`) '
  'still marks the records below as resolved; this audit keeps those decisions and reports the underlying disagreement separately.')
a('')
a('| ID | Product | Property | Audit status | Recorded decision |'); a('|---|---|---|---|---|')
for f in decisions:
    a(f"| {f['id']} | {md(f['product'], 40)} | {md(f['property'], 50)} | {f['resolution']} | {md(f['recorded_decision'], 300)} |")
a('')
for f in [x for x in F if x['source_kind'] == 'documented' and 'RECONSIDER: ' in x['explanation']]:
    a(f"- **{f['id']} reconsideration:** {md(f['explanation'].split('RECONSIDER: ')[-1].split(' final_resolution:')[0], 500)}")
a('')
a('## 7. Preservation, duplicates and novelty')
a('')
a(f'- All 147 conflict entries in the JSON (125 distinct conflicts) appear in the CSV with their JSON paths; all 125 conflict lines of the curated log map '
  'to a finding; values, notes and the recorded `resolved` flags are unchanged in the data. Two records that list sources without values (CF-024, CF-025) '
  'show the values read from those sources.')
a(f'- Duplicate: CF-093 (PURITY L65 viscosity index, stored as text: "brochure reports 104") and CF-096 (structured edition difference, LUB3213E 2015.07 '
  'VI 92 vs 2023.03 VI 104) record the same disagreement; the "brochure" value is printed in the 2023.03 edition. Both IDs are kept; 179 distinct issues.')
a('- Related but distinct: CF-159 is a label/unit issue inside the SDS value used in CF-009; CF-180 concerns the proposal text attached to CF-016; CF-141 '
  'adds a third source to the documented Ultra-S 6 conflicts CF-116 to CF-120 and to CF-172.')
a(f'- The {n_new} new findings were re-checked against every open question, note, calculation note and conflict entry of the product, the curated log, '
  'the README and the `reconciliation/` files: the documents involved are listed in the inventory register, but none of the discrepancies is described '
  'anywhere. The 9 Richful flash-point findings remain classed as recorded in field notes.')
a('')
a('## 8. Correction log (version of 2026-10-27 → this version)')
a('')
a(f'IDs CF-001 to CF-{len(F):03d} are unchanged; no finding was added or removed. {len(LOG)} field changes were made; every change is listed with its reason '
  'in the CSV column `changed_in_v3` (field names) and summarised here.')
a('')
a('| Count | Before | After | Reason |'); a('|---|---|---|---|')
for t in TYPES: a(f'| {t} | {v2types.get(t, 0)} | {types[t]} | see type changes below |')
for k in sorted(set(v2res) | set(res)): a(f'| Resolution: {k} | {v2res.get(k, 0)} | {res.get(k, 0)} | working values are not resolutions; three records are not value conflicts |')
a(f'| Distinct issues | 180 | {len(F) - sum(1 for f in F if f["duplicate_of"])} | duplicate pair CF-093 / CF-096 |')
a(f'| Pending or partially verified checks (excluding external-source groups) | 16 | {len(pend)} | sources obtained and read |')
a(f'| External-source findings not verifiable from the repository | 61 (Petro-Canada) + 24 (S-OIL, spot check) | 0 | brochure archived and both sources read column by column |')
a('')
a('Type changes:'); a('')
for i, o, n, r in type_changes: a(f'- {i}: {o} → {n}. {r}')
a('')
a('Resolution changes:'); a('')
for i, o, n in res_changes: a(f'- {i}: {o} → {n}')
a('')
a('Other substantive corrections:'); a('')
for s in [f'Verification of {len(pc)} Petro-Canada findings: from "not verifiable from the repository" to verified in both editions, column and row (LUB3213E 2015.07 and 2023.03).',
          f'Verification of {len(so)} S-OIL findings: from "registered web page, not re-fetched" to verified column by column (DL2-11177 catalog or SDS DL2-14611, and the live page = Internet Archive capture 2026-06-10). CF-102 compares an SDS range with a web typical, not two editions.',
          'CF-145: the manufacturer\'s Group II classification rests on a specification VI minimum of 100 (ADNOC spec 8230); a typical VI of 120 does not contradict it.',
          'CF-024: a typical "1.3 ppm" does not contradict a maximum of "1.3 wt.%"; the issue is a suspected unit misprint.',
          'CF-157, CF-158: the "110 min." flash points are printed inside "Typical Inspections" tables marked "Not a specification"; the JSON follows the table heading.',
          'CF-164, CF-167: the records themselves state that comparability is not established (SSI) or that the changes are additions (claims); the earlier wording overstated them.',
          f'Comparability was added to every finding; {len(gen_unc)} genuine contradictions are now labelled "comparability uncertain" (missing method or temperature, label/unit mismatch, family-level classification, provisional typicals or undated tables with different methods).',
          'Previously "verified" labels that relied only on the JSON or on a number match were re-checked for product identity, column, unit, method, temperature and edition date; revision dates match the printed dates in every case (formats differ).']:
    a(f'- {s}')
a('')
a('## 9. Not counted as conflicts')
a('')
for s in ['Method differences: SpectraSyn 2 flash point 157 °C (COC) vs 145 °C (PMCC); aramcoDURA BS150 282 °C (COC) vs 232 °C (PMCC).',
          'Bounds and ranges that contain the typical values (Ergon and Neste SDSs, ADNOC 6 cSt and Formosa specifications); rounding (Lubrizol, ADNOC, Ergon unit conversions; S-OIL SDS relative densities; PURITY L50 certificate of analysis).',
          'Byte-identical copies (Petro-Canada DL2-11262 to DL2-11265; Cosan DL2-11241, DL2-11242); column misattributions screened out (HiTEC 12204L / 12200).',
          f'Metadata gaps: value objects by status {dict(C(n.get("status") for p in A.load_products().values() for t in p["tiers"].values() for _, n, _ in A.value_objects(t["doc"].get("fields", {}))))}; {len(CAND["_no_final_numeric"])} numeric value objects without `value_final`; BT 3088 units not printed; MINGLAN T3161A slash values; ADNOC 4/6/8 flash methods not printed; the VM-field layout of three components.']:
    a(f'- {s}')
a('')
a('## 10. Limitations')
a('')
for s in ['ASTM D874-23 (sulfated-ash factors) is sold by ASTM and was not accessed; CAS Common Chemistry requires an API key (PubChem used instead).',
          'Suppliers were not contacted; identity questions, missing SDS test methods and grade-level API groups remain open.',
          'Two Afton HiTEC 5748 editions (03/18, 04/21) could not be retrieved: the Internet Archive search was temporarily offline on 2026-10-30.',
          '31 archive PDFs have no text layer and 13 files are images; DL2-13731.pdf uses an encoded font. These were read visually only where a finding depends on them.',
          'The automated comparison can miss a value that coincides with another grade\'s value in a multi-grade table.',
          'Physical checks use general relationships only (density falls with temperature; °F/°C conversion; API 1509 definitions); no viscosity index was recalculated.']:
    a(f'- {s}')
a('')
open(os.path.join(OUT, 'comprehensive_conflicts_audit.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('written', len(F), dict(types), '| genuine confirmed/uncertain', len(gen_conf), len(gen_unc), '| res', dict(res), '| levels', dict(lv), '| pending', dict(pr))
