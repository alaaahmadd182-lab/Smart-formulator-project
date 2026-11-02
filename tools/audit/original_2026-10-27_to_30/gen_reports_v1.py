"""Write reconciliation/comprehensive_conflicts_audit.md and .csv from audit/findings.json."""
import collections, csv, io, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A
from audit_compile import CAT  # noqa: E402  (re-runs the compile; read-only)

F = json.load(open(os.path.join(A.SCR, 'audit', 'findings.json'), encoding='utf-8'))
CAND = json.load(open(os.path.join(A.SCR, 'audit', 'candidates.json'), encoding='utf-8'))
OUT = os.path.join(A.REPO, 'reconciliation')
TEAMMATE_TEXT = 'Rawan-Mohammad: `53ed010` and `a38d5ca`, merged as `8a8d875` on 2026-10-24'
CLS = [('base_oil', 'Base oils'), ('additive_package', 'Additive packages'), ('additive_component', 'Additive components')]


def group(f):
    n = f['nature']
    if re.search(r'(?i)explainable|bound vs typical', n): return 'Explainable difference'
    if re.search(r'(?i)edition', n): return 'Edition difference'
    if re.search(r'(?i)data-quality|documentation|derivation|calculated value used|label/unit|unit inconsistency|identity|supplier names|likely transcription', n): return 'Data-quality or documentation inconsistency'
    if re.search(r'(?i)in-house method|units or test conditions|test method', n): return 'Method or condition difference'
    return 'Genuine contradiction'


for f in F: f['group'] = group(f)


def vtext(v, with_src=True):
    parts = [str(v.get('value')) if v.get('value') is not None else '']
    if v.get('unit'): parts.append(str(v['unit']))
    s = ' '.join(p for p in parts if p).strip()
    cond = '; '.join(str(x) for x in (v.get('conditions'), v.get('temperature_c') and f"{v['temperature_c']} °C") if x)
    if cond: s += f' ({cond})'
    if v.get('printed_text') and str(v.get('printed_text')) not in s: s += f' — printed: "{v["printed_text"]}"'
    if with_src and v.get('file'):
        pg = f" p.{v['page']}" if v.get('page') not in (None, '') else ''
        rev = f", {v['revision_date']}" if v.get('revision_date') else ''
        dt = f" [{v['doc_type']}]" if v.get('doc_type') else ''
        s += f' — {v["file"]}{pg}{rev}{dt}'
    return s


def md(s, n=None):
    s = re.sub(r'\s+', ' ', str(s if s is not None else '')).replace('|', '\\|')
    return s if n is None or len(s) <= n else s[:n - 1] + '…'


def tiers(f):
    out = sorted({m.group(1) for p in f['json_paths'] for m in [re.search(r'(tier\d|_tier\d|general|vm)', p)] if m} | ({t for t in re.findall(r'tier\d', f['property'])}))
    return ', '.join(out)


# ------------------------------------------------------------------ CSV
cols = ['conflict_id', 'material_class', 'supplier', 'product', 'record_id', 'property', 'conflict_category', 'finding_type', 'nature',
        'values', 'units_and_conditions', 'source_documents_and_pages', 'json_paths', 'tiers', 'explanation', 'verification_status',
        'resolution_status', 'recommended_next_step', 'provenance', 'affected_by_teammate_changes']
buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n'); w.writerow(cols)
for f in F:
    vals = f['values']
    w.writerow([f['id'], A.CLASS_LABEL[f['material_class']], f['supplier'], f['product'], f['record_id'], f['property'],
                f"{f['category']} {CAT[f['category']]}", f['group'], f['nature'],
                ' || '.join(str(v.get('value')) for v in vals),
                ' || '.join('; '.join(str(x) for x in (v.get('unit'), v.get('conditions'), v.get('temperature_c') and f"{v['temperature_c']} °C", v.get('printed_text') and f'printed: {v["printed_text"]}') if x) for v in vals),
                ' || '.join(f"{v.get('file')}" + (f" p.{v['page']}" if v.get('page') not in (None, '') else '') + (f" ({v['revision_date']})" if v.get('revision_date') else '') + (f" [{v['doc_type']}]" if v.get('doc_type') else '') for v in vals if v.get('file')),
                ' ; '.join(f['json_paths']), tiers(f), f['explanation'], f['verification'], f['resolution'], f['next_step'], f['provenance'], f['teammate']])
open(os.path.join(OUT, 'comprehensive_conflicts_audit.csv'), 'w', encoding='utf-8-sig', newline='').write(buf.getvalue())

# ------------------------------------------------------------------ Markdown
C = collections.Counter
L = []; a = L.append
nprod = len({f['record_id'] for f in F})
new_ = [f for f in F if f['provenance'].startswith('New')]
oqonly = [f for f in F if 'open question only' in f['provenance']]
prev = [f for f in F if f not in new_]
ext_only = [f for f in F if 'relies on source_registry' in f['verification']]
needs_ver = [f for f in F if re.search(r'(?i)as recorded|not machine|JSON-only|not checked|partially', f['verification'])]
reconsider = [f for f in F if f['source_kind'] == 'documented' and f['resolution'] == 'Requires Review']
a('# Comprehensive conflicts audit — lubricant raw-material data')
a('')
a('Audit of the Smart Formulator raw-material database (`Products_json`, 264 products in 706 JSON files) for conflicts, '
  'contradictions and inconsistencies. Prepared on branch `audit/comprehensive-conflicts` from `main` at commit `77ba590` '
  '(2026-10-27). No product JSON, template, coverage matrix or the curated log `open_questions_and_conflicts.md` was changed; '
  'nothing was resolved, averaged or preferred. The structured list is in `comprehensive_conflicts_audit.csv` (one row per finding, same IDs).')
a('')
a('Data rules applied (approved 2026-10-24): conflicting values are never averaged; TDS is never preferred over SDS (or the '
  'reverse) automatically; the validated `status` is reported, never `status_final`.')
a('')
a('## 1. Summary')
a('')
a(f'| | Count |'); a('|---|---|')
a(f'| Findings (unique conflicts, contradictions and inconsistencies) | **{len(F)}** in {nprod} products |')
a(f'| Previously documented in `conflicts[]` and the curated log (all preserved here) | {sum(1 for f in F if f["source_kind"] == "documented")} |')
a(f'| Previously documented only as open questions (not in `conflicts[]`) | {len(oqonly)} |')
a(f'| Previously documented elsewhere (identity review, integration flags) | {len(prev) - sum(1 for f in F if f["source_kind"] == "documented") - len(oqonly)} |')
a(f'| **New in this audit** | **{len(new_)}** |')
a(f'| Requiring further source verification (open-question records, JSON-only checks, image sources) | {len(needs_ver)} |')
a(f'| Archive value verified, external web value not re-fetched (S-OIL and Petro-Canada web tables, registered as verified) | {len(ext_only)} |')
a(f'| Previously marked resolved that need reconsideration | {len(reconsider)} |')
a(f'| Affected by the teammate\'s changes (PR #2) | {sum(1 for f in F if f["teammate"].startswith("Yes"))} |')
a('')
a('By type of finding:'); a(''); a('| Type | Count | Meaning |'); a('|---|---|---|')
meaning = {'Genuine contradiction': 'Documents (or one document) state incompatible values for the same product and property.',
           'Edition difference': 'Values changed between editions of the supplier\'s documents.',
           'Method or condition difference': 'Values differ, but the documents use different methods, conditions or units.',
           'Explainable difference': 'Compatible values (e.g. a lower bound and a typical value); recorded because field selection is inconsistent.',
           'Data-quality or documentation inconsistency': 'A problem in how the JSON or a supplier document records a value, unit, label or rule.'}
for g in meaning:
    a(f'| {g} | {sum(1 for f in F if f["group"] == g)} | {meaning[g]} |')
a('')
a('By material class and category:'); a('')
cats = sorted({f['category'] for f in F})
a('| Category | ' + ' | '.join(l for _, l in CLS) + ' | Total |'); a('|---|' + '---|' * (len(CLS) + 1))
for c in cats:
    row = [sum(1 for f in F if f['category'] == c and f['material_class'] == k) for k, _ in CLS]
    a(f'| {c} {CAT[c]} | ' + ' | '.join(str(x) for x in row) + f' | {sum(row)} |')
a('| **Total** | ' + ' | '.join(str(sum(1 for f in F if f['material_class'] == k)) for k, _ in CLS) + f' | **{len(F)}** |')
a('')
a('Categories with no findings: C07 inconsistency across JSON tiers (product blocks, record IDs and repeated properties agree across tiers), '
  'C08 reported without adequate source evidence (every Reported value cites an archive file with a page, or a verified registry URL), '
  'C11 original vs normalised value (after the 2026-10-24 reconciliation every remaining `*_final` key re-derives from the current value; '
  'the one value_final left null is listed under C04, TIANHE). C12 (teammate changes) is tracked as a column on every finding.')
a('')
a('By resolution status: ' + ', '.join(f'{k} {v}' for k, v in C(f['resolution'] for f in F).most_common()) + '.')
a('')
a('## 2. Repository state and teammate contributions')
a('')
a('`git fetch origin` (2026-10-27) brought no new commits. `origin/main` = `main` = `77ba590` (merge of PR #3, our reconciliation commit '
  '`a107745`; identical tree). The GitHub API lists no other branches, pull requests or forks with newer work. The most recent commits '
  f'by the teammate are those of PR #2 ({TEAMMATE_TEXT}), already reconciled on 2026-10-24. Any newer work by the teammate is not on GitHub '
  'and could not be examined.')
a('')
a('What PR #2 contributed (verified from Git history and diffs): `integrate_products.py` and `build_conflicts_report.py` (both since revised '
  'under the approved rules); normalised `value_final` / `unit_final` / `min_final` / `max_final` / `unit_conversion` / `integration_flags` keys '
  'on value objects (no original value, unit, status or source changed; no new properties or values filled); field-level resolution proposals '
  'and `resolved` / `final_resolution` on conflict entries; `CLAUDE.md`; coverage-matrix changes. Of these, 5,693 normalised value objects and '
  '16 conflict annotations remain; proposals that averaged values or preferred TDS over SDS were not adopted and are kept as text. '
  'Findings touching her work are marked in the CSV column `affected_by_teammate_changes`.')
a('')
a('## 3. Method')
a('')
a('1. Every `conflicts[]` entry in all 706 files (147 entries, 125 unique after removing repeats across tiers, 10 record formats) was normalised and '
  'each recorded value was searched on its cited source page in the archive `Manual + Data to share.zip` (347 PDFs, text extracted page by page).')
a('2. Detectors were run over all value objects: status vs value, Reported without source, value outside its own range, bound labelled typical, '
  'printed temperature vs recorded temperature, unit vs magnitude, density vs specific gravity, KV40 vs KV100, pour vs cloud/flash point, '
  'saturates + aromatics, CCS/MRV temperature order, API group vs VI/sulfur/saturates (API 1509 definitions), cross-tier product blocks, '
  'duplicate names and supplier names, Calculated values vs printed values, and every °F/°C pair in the archive.')
a('3. Cross-document screen: for each key property (KV40, KV100, VI, density, flash point, pour point, Noack, TBN, sulfated ash), every other '
  'archive document naming the product and printing that property was searched for the JSON value in any equivalent form (1,116 '
  'comparisons; 196 candidates). Each candidate was read and classified; multi-grade tables were read column by column.')
a('4. Open questions mentioning a discrepancy (67 unique) were compared with `conflicts[]`.')
a('5. Pages without a usable text layer were rendered and read for the documented values that depend on them (Richful SDS p.5 for RF6066, '
  'RF6069 and RF6078; Shell Risella X 430 SDS p.7; Lubrizol CV1100 product data sheet p.1-2).')
a('')
a('Verification status values: "Verified in source text/visually" — the value was found on the cited page; "Archive value verified; external '
  'web value relies on source_registry.json" — the web page was verified when it was registered and was not re-fetched; "As recorded in the open '
  'question" — the finding is reported as documented and still needs a source check; "JSON-only" — an inconsistency inside the data itself.')
a('')
a('## 4. Most significant unresolved contradictions')
a('')
SIG = ['CHEVRON_SYNFLUID_DIMER_C12', 'ERGON_HYGOLD_L750', 'ARAMCO_LUBEREF_DURA_BS150_YANBU', 'ARAMCO_LUBEREF_PRIMA_70', 'RF6602',
       'RICHFUL_RF6066', 'RICHFUL_RF6069', 'EXXONMOBIL_SPECTRASYN_ELITE_150', 'CHEVRON_SYNFLUID_MPAO_150', 'LUBRIZOL_CV1100', 'LUBRIZOL_CV3515',
       'PETRONAS_ETRO_6_PLUS', 'TIANHE_P_TEC_3232', 'PETRO_CANADA_PURITY_VHVI_2', 'ADNOC_ADBASE_3CST', 'RICHFUL_RF6077', 'MINGLAN_T3161A']
SIGPROP = {'ARAMCO_LUBEREF_DURA_BS150_YANBU': 'sulfur', 'ARAMCO_LUBEREF_PRIMA_70': 'flash', 'RF6602': 'flash', 'RICHFUL_RF6066': 'kv100', 'RICHFUL_RF6069': 'kv100',
           'EXXONMOBIL_SPECTRASYN_ELITE_150': 'flash', 'PETRONAS_ETRO_6_PLUS': 'density', 'INFINEUM_D3424': 'flash', 'RICHFUL_RF6077': 'density', 'MINGLAN_T3161A': 'sulfated_ash'}
a('| ID | Product | Property | Conflicting values | Why it matters | Status |'); a('|---|---|---|---|---|---|')
for rid in SIG:
    cand = [f for f in F if f['record_id'] == rid and (rid not in SIGPROP or SIGPROP[rid] in f['property'].lower()) and f['group'] != 'Explainable difference']
    for f in cand[:1]:
        a(f"| {f['id']} | {md(f['product'])} | {md(f['property'], 60)} | {md(' vs '.join(vtext(v, False) for v in f['values'] if v.get('value') is not None or v.get('printed_text')), 220)} | {md(f['explanation'], 260)} | {f['resolution']} |")
a('')
a('## 5. Findings by material class and category')
a('')
for k, label in CLS:
    sub = [f for f in F if f['material_class'] == k]
    a(f'### 5.{CLS.index((k, label)) + 1} {label} ({len(sub)})')
    a('')
    for c in cats:
        cs = [f for f in sub if f['category'] == c]
        if not cs: continue
        a(f'#### {c} {CAT[c]} ({len(cs)})')
        a('')
        a('| ID | Supplier / product | Property | Values, conditions and sources | Explanation | Type | Verification | Status | Provenance |')
        a('|---|---|---|---|---|---|---|---|---|')
        for f in cs:
            vals = '<br>'.join(md(vtext(v), 300) for v in f['values'])
            prov = f['provenance'] + ('; teammate: ' + f['teammate'] if f['teammate'].startswith('Yes') else '')
            a(f"| {f['id']} | {md(f['supplier'], 40)} / {md(f['product'], 50)} | {md(f['property'], 70)} | {vals} | {md(f['explanation'], 420)} | "
              f"{f['group']} | {md(f['verification'], 140)} | {f['resolution']} | {md(prov, 160)} |")
        a('')
a('## 6. Previously resolved conflicts requiring reconsideration')
a('')
a(f'{sum(1 for f in F if f["source_kind"] == "documented" and (f["resolution"] == "Resolved" or f in reconsider))} conflict records were marked resolved before this audit. '
  f'{len(reconsider)} need reconsideration:')
a('')
for f in reconsider:
    a(f"- **{f['id']} {f['record_id']} `{f['property']}`** — {md(f['explanation'].split('RECONSIDER: ')[-1].split(' final_resolution:')[0], 600)}")
a('')
a('The remaining resolved records rest on a newer dated edition of the same supplier document (HiTEC 12200 MTU 2.0 / DDC 93K215; Lubrizol '
  'CV7540 CES 20076/77/78; NYNAS NS 3 KV40, density, flash point, sulfur), on the 2026-10-18 user decisions for RF6077 KV100 and RF6088F KV100, '
  'or on "no value conflict" (Aramco DURA BS150 density note). They are listed in section 5 with status Resolved.')
a('')
a('## 7. Comparison with `open_questions_and_conflicts.md`')
a('')
a('- All 125 product-level conflicts listed in the curated log (147 tier-level JSON entries) are included here as findings with the same values '
  'and sources; none was dropped or merged. Their categories in the log map as: edition difference → C03; conflicting values between different '
  'documents → C01, C02 or C04 (when the record itself states that methods or bound types differ); unit or test-condition discrepancy → C04; '
  'inconsistency within one document → C01; the PURITY L65 viscosity-index record stored as text → C02.')
a(f'- {len(oqonly)} discrepancies were recorded only as open questions, not as conflict entries; they are listed here with the open-question '
  'text quoted verbatim.')
a('- Corrections to documented records found in this audit (not applied): NYNAS NYFROST 32 KV40 and flash point — the SDS values are on p.7 of '
  'DL2-13444.pdf, not p.6; RICHFUL RF6078 treat-rate conflict — the note is correct and the "files swapped" statement in the preserved PR #2 '
  'proposal is not; ERGON HYGOLD L750 — the uncited SDS DL2-10025.pdf supports the TDS specific gravity; RICHFUL RF6066 KV100 — the SDS prints '
  'the value on its "Viscosity, dynamic" line.')
a('- No duplicated conflict records were found: the 22 apparent duplicates in the JSON are the same entry repeated in several tier files of '
  'one product, counted once.')
a('')
a('## 8. Not counted as conflicts')
a('')
a('Explainable differences screened out (values differ only because of method, bound type, rounding or column assignment):')
a('')
for s in ['ExxonMobil SpectraSyn 2 flash point: TDS 157 °C (ASTM D92, COC) vs SDS DL2-13913/DL2-13919 145 °C (ASTM D93, closed cup).',
          'Aramco DURA BS150 Yanbu flash point: 282 °C (COC, D92) vs 232 °C (PMCC, D93), both on DL2-13944.pdf and DL2-12173.pdf.',
          'Ergon HyGold SDSs (DL2-10023 to DL2-10033): flash points printed as lower bounds (e.g. ">= 162,8 °C") and relative densities rounded to two decimals; compatible with the TDS values.',
          'Neste NEXBASE SDSs: relative-density ranges (e.g. 0,82-0,84) and flash point "> 220 °C" contain the TDS typical values; NEXBASE 3080 KV40 49 (TDS) vs 48 (SDS) is within rounding of a typical value.',
          'ADNOC ADbase 6 cSt distributor specification DL2-13721.pdf: limits (KV100 5.8-6.2, VI min 125, Noack max 8.0, flash min 220 °C) contain the typical values 6.18, 137, 6.8 and 235.',
          'Formosa 150N GII Plus and 500N GII specification limits contain the typical values; SDS pour point "< -12 °C" is compatible with -15 °C.',
          'Lubrizol densities in lb/US gal and lb/Imp gal, ADNOC g/ml vs kg/m3, Ergon HyGold 100 lb/gal vs g/cm3, HiTEC 12210M specific gravity 0.948 vs SDS density 0.95: consistent after unit conversion or rounding.',
          'S-OIL SDS relative densities vs the densities in the JSON (Ultra-S 2, 4, 6): within rounding; Ultra-S 3 (0.8323 vs 0.827) and aramcoULTRA 8 (0.8425 vs 0.847) differ slightly more, but the SDS value is a relative density, not a density.',
          'Petro-Canada PURITY L50 certificate of analysis DL2-13351.pdf density 0.853 kg/L (one batch) vs TDS typical 0.85 kg/L.',
          'Petro-Canada DL2-11262 to DL2-11265 are byte-identical copies of the cited VHVI brochure DL2-11261; Cosan DL2-11241/11242 are copies of DL2-11240.',
          'HiTEC 12204L: TBN 103 and density 0.989 on DL2-11412/DL2-14639 p.2 belong to HiTEC 12200, not 12204L.',
          'Chevron Synfluid PAO 4, 6 and 8, and C10 Dimer: individual TDS values equal the family table DL2-13200.']:
    a(f'- {s}')
a('')
a('Missing properties and incomplete metadata (not conflicts):')
a('')
st = C()
for folder, p in A.load_products().items():
    for t in p['tiers'].values():
        for path, n, _ in A.value_objects(t['doc'].get('fields', {})): st[n.get('status')] += 1
flags = C(CAND['_flags'])
a(f'- Value objects by status: ' + ', '.join(f'{k} {v}' for k, v in st.most_common()) + '. Missing values are gaps, not conflicts.')
a(f'- {len(CAND["_no_final_numeric"])} numeric value objects have no normalised `value_final` (new products and value objects changed by the Task 3 '
  'corrections); they await a reviewed run of `integrate_products.py`.')
a('- Integration flags on normalised values: ' + '; '.join(f'{v} × "{k}"' for k, v in flags.most_common()) + '.')
a('- BETTCHEM BT 3088 tier 2: sulfated ash, Ca, Zn, P, B, N and S have unit "not printed" in the source.')
a('- MINGLAN T3161A treat-rate rows "CF-4/SJ 6.0/6.2" and "CD/SF 4.6/4.8" are Reported without a single value because the meaning of the slash is not printed.')
a('- ADNOC ADbase 4/6/8 cSt flash points: no method printed for the brochure typical values.')
a('- Component layout: AFTON_HITEC_8767B, AFTON_HITEC_12250 and LUBRIZOL_CV6320 keep the seven viscosity-modifier fields in general.json (21 fields) instead of a separate vm.json; `Not Applicable` (7 fields, CV6320) is part of the template status vocabulary.')
a('')
a('## 9. Limitations')
a('')
a(f'- The teammate\'s most recent work, if any, is not on GitHub; this audit covers the repository as of `77ba590`.')
a('- 31 archive PDFs have no text layer and 13 files are images; one PDF (DL2-13731.pdf) has an encoded font. Values on these pages were checked '
  'visually only where a finding depends on them (listed in section 3); the cross-document screen could not read them.')
a('- 32 cited external sources (web pages and archived PDFs) were not re-fetched; their verification status is taken from `source_registry.json`.')
a('- The cross-document screen finds a difference only when the property label and the JSON value can be matched in the text. Tables whose '
  'columns are split across lines were read manually for the products concerned, but values that coincide with another grade\'s value in a '
  'multi-grade table can be missed.')
a('- Physical cross-checks use general relationships only (density decreases with temperature; °F/°C conversion; API 1509 group definitions). '
  'No viscosity index was recalculated, because the ASTM D2270 tables are not in the archive.')
a('- The ASTM D874 sulfated-ash factors and the API 1509 text are not in the archive; findings that depend on them are marked Requires Review.')
a('- Findings recorded only as open questions are reported as documented; their source pages were re-checked only where stated.')
a('')
md_text = '\n'.join(L).replace('{TEAMMATE_TEXT}', 'Rawan-Mohammad: `53ed010` and `a38d5ca`, merged as `8a8d875` on 2026-10-24')
open(os.path.join(OUT, 'comprehensive_conflicts_audit.md'), 'w', encoding='utf-8', newline='\n').write(md_text + '\n')
print('written', len(F), 'findings;', C(f['group'] for f in F))
