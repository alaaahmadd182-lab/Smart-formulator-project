"""Write reconciliation/comprehensive_conflicts_audit.md and .csv from audit/findings.json (quality-reviewed version)."""
import collections, csv, io, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A
from audit_compile import CAT, BASIS  # noqa: E402  (re-runs the compile; read-only on the repository)

F = json.load(open(os.path.join(A.SCR, 'audit', 'findings.json'), encoding='utf-8'))
CAND = json.load(open(os.path.join(A.SCR, 'audit', 'candidates.json'), encoding='utf-8'))
OLD28 = json.load(open(os.path.join(A.SCR, 'audit', 'old28.json'), encoding='utf-8'))
OUT = os.path.join(A.REPO, 'reconciliation')
CLS = [('base_oil', 'Base oils'), ('additive_package', 'Additive packages'), ('additive_component', 'Additive components')]
TYPES = ['Genuine contradiction', 'Edition difference', 'Explainable difference', 'Data-quality issue']
C = collections.Counter


def md(s, n=None):
    s = re.sub(r'\s+', ' ', str(s if s is not None else '')).replace('|', '\\|')
    return s if n is None or len(s) <= n else s[:n - 1] + '…'


def vtext(v, with_src=True):
    s = ' '.join(x for x in (str(v.get('value')) if v.get('value') is not None else '', str(v.get('unit') or '')) if x).strip()
    cond = '; '.join(str(x) for x in (v.get('conditions'), v.get('temperature_c') and f"{v['temperature_c']} °C") if x)
    if cond: s += f' ({cond})'
    if v.get('printed_text') and str(v['printed_text']) not in s: s += f' — printed: "{v["printed_text"]}"'
    if with_src and v.get('file'):
        s += f" — {v['file']}" + (f" p.{v['page']}" if v.get('page') not in (None, '') else '') + \
             (f", {v['revision_date']}" if v.get('revision_date') else '') + (f" [{v['doc_type']}]" if v.get('doc_type') else '')
    return s


def tiers(f):
    return ', '.join(sorted({m.group(1) for p in f['json_paths'] for m in [re.search(r'(tier\d|general|vm)', p)] if m}))


def ext(f):
    return 'PC' if 'mascherpa' in f['verification'] else 'SOIL' if 'registered in source_registry' in f['verification'] else ''


# ------------------------------------------------------------------ CSV
cols = ['conflict_id', 'material_class', 'supplier', 'product', 'record_id', 'property', 'conflict_category', 'finding_type', 'finding_type_basis',
        'nature', 'values', 'units_and_conditions', 'source_documents_and_pages', 'json_paths', 'tiers', 'explanation', 'verification_status',
        'verification_priority', 'resolution_status', 'recommended_next_step', 'provenance', 'affected_by_teammate_changes']
buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n'); w.writerow(cols)
for f in F:
    vals = f['values']
    w.writerow([f['id'], A.CLASS_LABEL[f['material_class']], f['supplier'], f['product'], f['record_id'], f['property'],
                f"{f['category']} {CAT[f['category']]}", f['group'], f['group_basis'], f['nature'],
                ' || '.join(str(v.get('value')) for v in vals),
                ' || '.join('; '.join(str(x) for x in (v.get('unit'), v.get('conditions'), v.get('temperature_c') and f"{v['temperature_c']} °C",
                                                         v.get('printed_text') and f'printed: {v["printed_text"]}') if x) for v in vals),
                ' || '.join(f"{v.get('file')}" + (f" p.{v['page']}" if v.get('page') not in (None, '') else '') + (f" ({v['revision_date']})" if v.get('revision_date') else '')
                            + (f" [{v['doc_type']}]" if v.get('doc_type') else '') for v in vals if v.get('file')),
                ' ; '.join(f['json_paths']), tiers(f), f['explanation'], f['verification'], f['verification_priority'], f['resolution'],
                f['next_step'], f['provenance'], f['teammate']])
open(os.path.join(OUT, 'comprehensive_conflicts_audit.csv'), 'w', encoding='utf-8-sig', newline='').write(buf.getvalue())

# ------------------------------------------------------------------ numbers used in the text
n_doc = sum(1 for f in F if f['source_kind'] == 'documented')
n_new = sum(1 for f in F if f['provenance'].startswith('New'))
n_oq = sum(1 for f in F if 'open question only' in f['provenance'])
n_notes = sum(1 for f in F if f['provenance'].startswith('Previously recorded in field notes'))
n_else = len(F) - n_doc - n_new - n_oq - n_notes
n_pc = sum(1 for f in F if ext(f) == 'PC'); n_soil = sum(1 for f in F if ext(f) == 'SOIL')
open_checks = [f for f in F if f['verification_priority'] and not ext(f)]
pr = C(f['verification_priority'].split(':')[0] for f in open_checks)
reconsider = [f for f in F if f['source_kind'] == 'documented' and f['resolution'] == 'Requires Review']
types = C(f['group'] for f in F)
nprod = len({f['record_id'] for f in F})
settled = OLD28.get('Settled in this review', [])
SIG = [('CHEVRON_SYNFLUID_DIMER_C12', 'pour'), ('ERGON_HYGOLD_L750', 'density'), ('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'sulfur'),
       ('ARAMCO_LUBEREF_PRIMA_70', 'tier2.flash'), ('RF6602', 'flash'), ('RICHFUL_RF6066', 'kv100'), ('RICHFUL_RF6069', 'kv100'),
       ('EXXONMOBIL_SPECTRASYN_ELITE_150', 'flash'), ('CHEVRON_SYNFLUID_MPAO_150', 'flash'), ('LUBRIZOL_CV1100', 'sulfated'),
       ('LUBRIZOL_CV3515', 'sulfated'), ('PETRONAS_ETRO_6_PLUS', 'kv40'), ('NYNAS_NYFROST_32', 'flash'), ('TIANHE_P_TEC_3232', 'density'),
       ('PETRO_CANADA_PURITY_VHVI_2', 'api'), ('ADNOC_ADBASE_3CST', 'api'), ('RICHFUL_RF6077', 'density'), ('MINGLAN_T3161A', 'sulfated')]
sig = []
for rid, kw in SIG:
    m = [f for f in F if f['record_id'] == rid and kw in f['property'].lower()]
    if m: sig.append(m[0])

L = []; a = L.append
a('# Comprehensive conflicts audit — lubricant raw-material data')
a('')
a('Smart Formulator raw-material database (`Products_json`: 264 products, 706 JSON files). Branch `audit/comprehensive-conflicts`, from `main` '
  'at commit `77ba590`; audit and quality review 2026-10-27. No product JSON, template, coverage matrix or the curated log '
  '`open_questions_and_conflicts.md` was changed, and no conflict was resolved, averaged or settled by preferring one document type. '
  'Every finding is listed, with the same ID, in `comprehensive_conflicts_audit.csv`.')
a('')
a('## Executive summary')
a('')
a('**Scope and method.** All 706 records were examined. The 147 conflict entries already recorded in the data (125 distinct conflicts) were '
  'checked value by value against the cited pages of the supplier documents in the project archive (347 PDFs and 13 images). Independent checks '
  'then looked for unrecorded problems: every value object was screened for internal inconsistencies (status, units, ranges, temperatures, '
  'physical plausibility, API group definitions), and each key property was compared with every other archive document that names the same '
  'product (1,116 comparisons). Each candidate was read in the source; pages without a text layer were checked visually where a finding depends '
  'on them. Nothing was resolved: both values and their sources are kept for every conflict.')
a('')
a(f'**Findings.** {len(F)} distinct findings in {nprod} products, in four types:')
a('')
a('| Type | Count | What it means |'); a('|---|---|---|')
for t in TYPES: a(f'| {t} | {types[t]} | {BASIS[t]} |')
a('')
a(f'{n_doc} findings were already recorded as conflicts (all preserved here unchanged), {n_oq} were recorded only as open questions, {n_notes} were '
  f'noted only in field notes, {n_else} were recorded elsewhere (identity review, integration flags), and **{n_new} are new**. '
  f'{len(reconsider)} conflicts previously marked resolved need reconsideration.')
a('')
a('**Most important open contradictions.** A pour point probably misread from a mislabelled °F/°C header (Synfluid C12 Dimer: stored −63 °C, '
  'the printed pair is only consistent as −53 °C); a density that contradicts the specific gravity on the same sheet (Ergon HyGold L750); '
  'a sulfur value printed as 1.3 ppm in one sheet and 1.3 wt.% in the other (aramcoDURA BS150); safety-data-sheet flash points below the '
  'product\'s own specification minimum (aramcoPRIMA 70; Richful RF6602); calculated sulfated-ash values that contradict the printed values '
  '(Lubrizol CV1100, CV3515) and two different zinc factors across 26 calculated values; three API group labels that conflict with the '
  'reported viscosity index; and undocumented TDS vs SDS flash-point differences of 5–31 °C (Chevron Phillips Synfluid, ExxonMobil SpectraSyn Elite 150).')
a('')
a(f'**Outstanding verification before submission.** (1) {n_pc} Petro-Canada PURITY edition differences rest on the 2023.03 LUB3213E brochure, '
  'read from a distributor-hosted copy that is neither registered in `source_registry.json` nor archived; registering and archiving this one '
  f'document is the most important remaining step. (2) {n_soil} S-OIL edition differences rely on the S-OIL web page registered as verified on '
  f'2026-10-22; a dated spot check is sufficient. (3) {len(open_checks)} other findings need a check or confirmation: {pr.get("High", 0)} high '
  '(API 1509 and ASTM D874 texts, supplier confirmation, one image-only source), '
  f'{pr.get("Medium", 0)} medium and {pr.get("Low", 0)} low (section 4).')
a('')
a('**Limitations.** 31 archive PDFs have no text layer and 13 files are images (one PDF uses an encoded font); 32 external sources were not '
  're-fetched; the ASTM D874, D2270 and API 1509 texts are not in the archive; a value that coincides with another grade\'s value in a multi-grade '
  'table can escape the automated comparison. Any work by the teammate that is not yet on GitHub is not covered.')
a('')
a('## 1. Summary tables')
a('')
a('| | Count |'); a('|---|---|')
a(f'| Findings | **{len(F)}** in {nprod} products |')
a(f'| Already recorded in `conflicts[]` and the curated log (preserved unchanged) | {n_doc} |')
a(f'| Recorded only as open questions | {n_oq} |')
a(f'| Recorded only in field notes (not as conflicts) | {n_notes} |')
a(f'| Recorded elsewhere (identity review, integration flags) | {n_else} |')
a(f'| **New in this audit** | **{n_new}** |')
a(f'| Need a source check or confirmation (excluding the two external-source groups) | {len(open_checks)} (High {pr.get("High", 0)}, Medium {pr.get("Medium", 0)}, Low {pr.get("Low", 0)}) |')
a(f'| Petro-Canada edition differences resting on an unregistered external copy | {n_pc} |')
a(f'| S-OIL edition differences resting on a registered web page | {n_soil} |')
a(f'| Previously marked resolved, needing reconsideration | {len(reconsider)} |')
a(f'| Involving the teammate\'s changes (PR #2) | {sum(1 for f in F if f["teammate"].startswith("Yes"))} |')
a('')
a('By type and material class:'); a('')
a('| Type | ' + ' | '.join(l for _, l in CLS) + ' | Total |'); a('|---|' + '---|' * (len(CLS) + 1))
for t in TYPES:
    row = [sum(1 for f in F if f['group'] == t and f['material_class'] == k) for k, _ in CLS]
    a(f'| {t} | ' + ' | '.join(map(str, row)) + f' | {sum(row)} |')
a('| **Total** | ' + ' | '.join(str(sum(1 for f in F if f['material_class'] == k)) for k, _ in CLS) + f' | **{len(F)}** |')
a('')
cats = sorted({f['category'] for f in F})
a('By category and type:'); a('')
a('| Category | ' + ' | '.join(TYPES) + ' | Total |'); a('|---|' + '---|' * (len(TYPES) + 1))
for c in cats:
    row = [sum(1 for f in F if f['category'] == c and f['group'] == t) for t in TYPES]
    a(f'| {c} {CAT[c]} | ' + ' | '.join(map(str, row)) + f' | {sum(row)} |')
a('')
a('Categories with no findings: C07 inconsistency across JSON tiers (product blocks, record IDs and repeated properties agree across tiers); '
  'C08 reported without adequate source evidence (every Reported value cites an archive file with a page, or a registered URL); C11 original '
  'vs normalised value (every remaining `*_final` key re-derives from the current value; the one `value_final` left null is TIANHE, under C04). '
  'C12 (teammate changes) is a column on every finding. By resolution status: ' + ', '.join(f'{k} {v}' for k, v in C(f['resolution'] for f in F).most_common()) + '.')
a('')
a('## 2. Most significant unresolved contradictions')
a('')
a('| ID | Product | Property | Conflicting values | Why it matters | Type | Verification |'); a('|---|---|---|---|---|---|---|')
for f in sig:
    a(f"| {f['id']} | {md(f['product'])} | {md(f['property'], 50)} | {md(' vs '.join(vtext(v, False) for v in f['values'] if v.get('value') is not None or v.get('printed_text')), 230)} | "
      f"{md(f['explanation'], 260)} | {f['group']} | {md(f['verification'], 90)} |")
a('')
a('## 3. Repository state, teammate contributions and method')
a('')
a('`git fetch origin` (2026-10-27) brought no new commits. `origin/main` = `main` = `77ba590` (merge of PR #3, identical tree to our reconciliation '
  'commit `a107745`). The GitHub API lists no other branches, pull requests or forks with newer work. The teammate\'s most recent commits are '
  'PR #2 (Rawan-Mohammad: `53ed010` and `a38d5ca`, merged as `8a8d875` on 2026-10-24), already reconciled. That work added `integrate_products.py`, '
  '`build_conflicts_report.py` and `CLAUDE.md`, normalised `*_final` keys beside the original values (no original value, unit, status or source '
  'changed; no property added; no missing value filled), and resolution proposals on conflict entries; proposals that averaged values or preferred '
  'one document type were not adopted and are kept as text. Findings touching that work are marked in the CSV column `affected_by_teammate_changes`.')
a('')
a('Method: (1) normalise all 147 conflict entries (10 record formats) and look up every recorded value on its cited page; (2) run detectors over all '
  'value objects (status vs value, Reported without source, ranges, bound vs typical labels, printed vs recorded temperature, unit vs magnitude, '
  'density vs specific gravity, KV40 vs KV100, pour/cloud/flash order, saturates + aromatics, CCS/MRV order, API 1509 group definitions, '
  'cross-tier blocks, names and suppliers, Calculated vs printed values, every °F/°C pair in the archive); (3) compare each key property with '
  'every other archive document naming the product (1,116 comparisons, 196 candidates, each read; multi-grade tables read column by column); '
  '(4) compare open questions that mention a discrepancy with the conflict records; (5) read image or vector pages visually where a finding '
  'depends on them.')
a('')
a('## 4. Verification status and priorities')
a('')
a('Verification labels state how each value was checked: "in source text" (found on the cited page of the archive PDF), "visually" (image or '
  'vector page read on screen), "as recorded" (taken from the existing record, not re-checked), or "JSON-only" (an inconsistency inside the data). '
  'No finding is labelled verified on the basis of the JSON alone.')
a('')
a('### 4.1 Findings that still need a source check or confirmation')
a('')
a('| Priority | ID | Product | Property | What is needed |'); a('|---|---|---|---|---|')
for lvl in ('High', 'Medium', 'Low'):
    for f in [x for x in open_checks if x['verification_priority'].startswith(lvl)]:
        a(f"| {lvl} | {f['id']} | {md(f['product'], 40)} | {md(f['property'], 50)} | {md(f['verification_priority'].split(': ', 1)[-1], 160)} |")
a('')
a(f'Of the 28 findings marked as needing a source check in the first version of this report, {len(settled)} were checked against the archive '
  'during the quality review (text or visual) and are now verified: ' + ', '.join(settled) + f'. The other {28 - len(settled)} remain in the table '
  'above. The review also re-labelled 8 findings whose conclusion depends on a standard, a supplier confirmation or an image-only page (the three '
  'API group findings, aramcoPRIMA 70 flash point, Synfluid C12 Dimer, Infineum D3375, PURITY L65 brochure value, Ultra-S 8 identity).')
a('')
a('### 4.2 Findings that depend on external web sources')
a('')
a(f'- **Petro-Canada PURITY ({n_pc} edition differences).** The archive side (LUB3213E 2015.07, DL2-10020.pdf) is verified. The 2023.03 values were '
  'read, according to each record, from a distributor-hosted copy (`mascherpa.it`) because the Petro-Canada server blocks automated retrieval. '
  'Neither that URL nor the cited Petro-Canada URL is in `source_registry.json`, and no copy or checksum is kept, so these values cannot be '
  'verified from the repository. **Additional verification is needed before submission**: obtain the 2023.03 LUB3213E/IM-1809E document, '
  'register it (publisher, edition, retrieval date, SHA-256) and spot-check the 61 values; until then they should be presented as '
  '"reported in a later edition; external copy not archived".')
a(f'- **S-OIL Ultra-S / aramcoULTRA ({n_soil} edition differences).** The archive side (DL2-11177.pdf and the SDSs) is verified. The newer values come '
  'from https://www.s-oil.com/en/energy/LubeBaseOil.aspx, registered as a verified manufacturer page on 2026-10-22 (HTML, undated, no stored copy). '
  'Web pages can change without notice; a dated spot check of a few values, or a saved copy of the page, before submission is sufficient.')
a('')
a('## 5. Findings by type, material class and category')
a('')
for ti, t in enumerate(TYPES, 1):
    sub_t = [f for f in F if f['group'] == t]
    a(f'### 5.{ti} {t} ({len(sub_t)})'); a(''); a(BASIS[t]); a('')
    for k, label in CLS:
        sub = [f for f in sub_t if f['material_class'] == k]
        if not sub: continue
        a(f'#### {label} ({len(sub)})'); a('')
        a('| ID | Category | Supplier / product | Property | Values, conditions and sources | Explanation | Verification | Status | Provenance |')
        a('|---|---|---|---|---|---|---|---|---|')
        for f in sorted(sub, key=lambda x: (x['category'], x['id'])):
            vals = '<br>'.join(md(vtext(v), 300) for v in f['values'])
            prov = f['provenance'] + ('; teammate: ' + f['teammate'] if f['teammate'].startswith('Yes') else '')
            a(f"| {f['id']} | {f['category']} | {md(f['supplier'], 40)} / {md(f['product'], 50)} | {md(f['property'], 70)} | {vals} | {md(f['explanation'], 420)} | "
              f"{md(f['verification'], 180)} | {f['resolution']} | {md(prov, 170)} |")
        a('')
a('## 6. Previously resolved conflicts requiring reconsideration')
a('')
a(f'14 conflict records were marked resolved before this audit; {len(reconsider)} need reconsideration:'); a('')
for f in reconsider:
    a(f"- **{f['id']} {f['record_id']} `{f['property']}`** — {md(f['explanation'].split('RECONSIDER: ')[-1].split(' final_resolution:')[0], 600)}")
a('')
a('The other 12 rest on a newer dated edition of the same supplier document (HiTEC 12200 MTU 2.0 / DDC 93K215; Lubrizol CV7540 CES 20076/77/78; '
  'NYNAS NS 3 KV40, density, flash point, sulfur), on the 2026-10-18 user decisions for RF6077 and RF6088F KV100, or on "no value conflict" '
  '(aramcoDURA BS150 density note).')
a('')
a('## 7. Comparison with `open_questions_and_conflicts.md` and preservation check')
a('')
a('- All 147 conflict entries in the JSON (125 distinct conflicts) appear in the CSV with their JSON paths, and all 125 conflict lines of the curated '
  'log map to a finding. Values, notes and resolution flags are identical to the records, except two records that list sources without values '
  '(aramcoDURA BS150 sulfur, Ergon HyGold L750): for these the values read from the sources are shown, and the finding says so.')
a('- Curated-log types map as: edition difference → C03; conflicting values between different documents → C01, C02 or C04; unit or test-condition '
  'discrepancy → C04; inconsistency within one document → C01; the PURITY L65 record stored as text → C02.')
a(f'- {n_oq} discrepancies recorded only as open questions are listed with the question text quoted verbatim; {n_notes} findings were recorded only in '
  'field notes (Richful flash points: the calculation_note quotes the TDS line, including its typical value, as "Same value in").')
a(f'- The {n_new} new findings were checked against every product\'s open questions, notes, calculation notes and conflict entries, the curated log '
  'and the `reconciliation/` files: none duplicates an existing record. DL2-11240.pdf (Ultra-S 6) is listed in `inventory_reconciliation.csv` as a '
  'register document, but its values were never compared.')
a('- Corrections to existing records found in this audit (not applied): NYNAS NYFROST 32 — the SDS values are on p.7 of DL2-13444.pdf, not p.6; '
  'RF6078 treat-rate conflict — the note is correct and the "files swapped" statement in the kept PR #2 proposal is not; Ergon HyGold L750 — the '
  'uncited SDS DL2-10025.pdf supports the specific gravity; RF6066 KV100 — the SDS prints the value on its "Viscosity, dynamic" line.')
a('- No duplicated conflict records: the 22 repeated JSON entries are the same conflict in several tier files of one product, counted once.')
a('')
a('## 8. Not counted as conflicts')
a('')
a('Explainable differences screened out (values differ only by method, bound type, rounding or column assignment):'); a('')
for s in ['ExxonMobil SpectraSyn 2 flash point: TDS 157 °C (ASTM D92, open cup) vs SDS DL2-13913/DL2-13919 145 °C (ASTM D93, closed cup).',
          'aramcoDURA BS150 Yanbu flash point: 282 °C (COC, D92) vs 232 °C (PMCC, D93), both on DL2-13944.pdf and DL2-12173.pdf.',
          'Ergon HyGold SDSs (DL2-10023 to DL2-10033): flash points printed as lower bounds and relative densities rounded to two decimals; compatible with the TDS values.',
          'Neste NEXBASE SDSs: relative-density ranges and "> 220 °C" flash points contain the TDS typical values; NEXBASE 3080 KV40 49 vs 48 is within rounding.',
          'ADNOC ADbase 6 cSt distributor specification DL2-13721.pdf: limits contain the typical values (KV100 6.18, VI 137, Noack 6.8, flash point 235 °C).',
          'Formosa 150N GII Plus and 500N GII specification limits contain the typical values; SDS pour point "< -12 °C" is compatible with -15 °C.',
          'Lubrizol densities in lb/US gal and lb/Imp gal, ADNOC g/ml vs kg/m3, Ergon HyGold 100 lb/gal vs g/cm3, HiTEC 12210M specific gravity 0.948 vs SDS density 0.95: consistent after conversion or rounding.',
          'S-OIL SDS relative densities vs the JSON densities (Ultra-S 2, 4, 6) within rounding; Ultra-S 3 (0.8323 vs 0.827) and aramcoULTRA 8 (0.8425 vs 0.847) compare a density with a relative density.',
          'Petro-Canada PURITY L50 certificate of analysis DL2-13351.pdf density 0.853 kg/L (one batch) vs TDS typical 0.85 kg/L.',
          'Byte-identical copies: Petro-Canada DL2-11262 to DL2-11265 (= DL2-11261); Cosan DL2-11241, DL2-11242 (= DL2-11240).',
          'HiTEC 12204L: the TBN 103 and density 0.989 on DL2-11412/DL2-14639 p.2 belong to HiTEC 12200.',
          'Chevron Synfluid PAO 4, 6, 8 and C10 Dimer: individual TDS values equal the family table DL2-13200.']:
    a(f'- {s}')
a('')
a('Missing properties and incomplete metadata (gaps, not conflicts):'); a('')
st = C()
for folder, p in A.load_products().items():
    for t in p['tiers'].values():
        for path, n, _ in A.value_objects(t['doc'].get('fields', {})): st[n.get('status')] += 1
a('- Value objects by status: ' + ', '.join(f'{k} {v}' for k, v in st.most_common()) + '.')
a(f'- {len(CAND["_no_final_numeric"])} numeric value objects have no normalised `value_final` (new products and value objects changed by the Task 3 corrections).')
a('- Integration flags on normalised values: ' + '; '.join(f'{v} × "{k}"' for k, v in C(CAND['_flags']).most_common()) + '.')
a('- BETTCHEM BT 3088 tier 2: units "not printed" in the source for sulfated ash, Ca, Zn, P, B, N and S.')
a('- MINGLAN T3161A: treat-rate rows "CF-4/SJ 6.0/6.2" and "CD/SF 4.6/4.8" are Reported without a single value (meaning of the slash not printed).')
a('- ADNOC ADbase 4/6/8 cSt flash points: no method printed for the brochure typical values.')
a('- Component layout: AFTON_HITEC_8767B, AFTON_HITEC_12250 and LUBRIZOL_CV6320 keep the seven viscosity-modifier fields in general.json (21 fields) instead of a separate vm.json; `Not Applicable` (7 fields, CV6320) is part of the template status vocabulary.')
a('')
a('## 9. Limitations')
a('')
for s in ['Any work by the teammate that is not yet on GitHub is not covered; this audit covers the repository at `77ba590`.',
          '31 archive PDFs have no text layer and 13 files are images; DL2-13731.pdf uses an encoded font. Values on such pages were checked visually only where a finding depends on them. DL2-13224.jpeg (an S-OIL TDS covering five products) could not be compared automatically.',
          '32 cited external sources were not re-fetched. The Petro-Canada 2023.03 brochure behind 61 findings is neither registered nor archived (section 4.2).',
          'The cross-document comparison finds a difference only when the property label and the JSON value can be matched in the text; a value that coincides with another grade\'s value in a multi-grade table can be missed.',
          'Physical checks use general relationships only (density falls as temperature rises; °F/°C conversion; API 1509 group definitions). No viscosity index was recalculated; ASTM D874, D2270 and API 1509 are not in the archive.',
          'Findings recorded only as open questions were re-checked in the archive where their verification label says so; the others are reported as recorded.']:
    a(f'- {s}')
a('')
a('## 10. Quality review (2026-10-27)')
a('')
for s in ['Evidence: every value with an archive file and page was searched again on that page; values on image or vector pages were confirmed visually, and values on image-only PDFs that were not viewed are labelled as not checked. Labels were corrected where a value had been checked visually, where the page differed from the citation (NYNAS NYFROST 32: p.7, not p.6), or where only the JSON had been compared (Infineum D3375).',
          'Document types are taken from the document itself: an SDS is identified by its title block and numbered sections, not by a footer that mentions an SDS (this corrected TDS labels for Shell Risella and Richful RF6081).',
          f'Types: two findings moved from genuine contradiction to explainable difference because the values are compatible (Infineum D3424 flash point, RF6406 TBN); method or condition differences are part of "explainable differences" ({types["Explainable difference"]} in all).',
          f'Novelty: 9 Richful flash-point findings were reclassified from "new" to "recorded only in field notes"; {n_new} new findings remain, none duplicating an existing record.',
          'Preservation: 147/147 conflict entries and 125/125 curated-log lines are represented; values, notes and resolution flags are unchanged.',
          'Corrected page or value details: Synfluid PAO 8 SDS pages (3 and 5); Richful SDS flash-point pages taken from each record; RF6079 TDS value shown as typical only.',
          'External sources: the Petro-Canada 2023.03 source is not in `source_registry.json`; the earlier wording "relies on source_registry.json" was incorrect for these 61 findings.']:
    a(f'- {s}')
a('')
open(os.path.join(OUT, 'comprehensive_conflicts_audit.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('written', len(F), 'findings;', dict(types), '| open checks', dict(pr), '| new', n_new, '| PC', n_pc, '| SOIL', n_soil)
