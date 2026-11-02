"""Write version 5 (revision 2026-11-02) of reconciliation/comprehensive_conflicts_audit.md and .csv.

Derived from the 2026-10-30 generator gen_reports_v4.py (preserved unchanged in tools/audit/original_2026-10-27_to_30/):
same layout and same rendering of every finding. Changes: repository-relative paths; input
tools/audit/review_2026-11-02/output/findings_v5.json (written by revise_findings.py); a revision header; corrected
summary statements; CSV columns changed_in_v5 and later_state_2026_10_31; correction-log sections 8.3 and 8.4; the
section-9 status counts frozen at the snapshot commit e6617ca; a longer comparability excerpt in the Markdown tables.

Usage: python tools/audit/review_2026-11-02/gen_report_v5.py [--outdir DIR]   (default: reconciliation/)
"""
import argparse, collections, csv, io, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.stdout.reconfigure(encoding='utf-8')
import review_lib as RL

ORIG = os.path.join(RL.ROOT, 'tools', 'audit', 'original_2026-10-27_to_30', 'intermediate')
CLASS_LABEL = {'base_oil': 'Base oil', 'additive_package': 'Additive package', 'additive_component': 'Additive component'}
ap = argparse.ArgumentParser(); ap.add_argument('--outdir', default=os.path.join(RL.ROOT, 'reconciliation')); ARGS = ap.parse_args()

CAT = {'C01': 'Conflicting values for the same product', 'C02': 'Contradiction between document types (TDS/PDS/SDS/COA/specification)',
       'C03': 'Edition or revision difference', 'C04': 'Test method, temperature, unit or condition difference', 'C05': 'Typical value vs specification, limit or range',
       'C06': 'Classification contradiction (API group, chemistry, function)', 'C09': 'Status inconsistent with available evidence',
       'C10': 'Unsupported assumption, conversion or derived value', 'C13': 'Product identity, supplier or reference mismatch',
       'C14': 'Documentation omitted, incorrectly resolved or duplicated'}
CONF, POT = 'Confirmed contradiction', 'Potential contradiction (comparability uncertain)'
TYPES = [CONF, POT, 'Edition difference', 'Explainable difference', 'Data-quality issue']
BASIS = {CONF: 'Values for the same product and property that cannot both be right as printed, compared under comparable conditions, with no documented method, condition or edition that explains them.',
         POT: 'Values that appear to disagree, but the documents do not state enough (method, temperature, quantity, basis, date or grade level) to confirm that they are comparable. Not a confirmed contradiction and not an explained difference.',
         'Edition difference': 'Values (or claims) that differ between dated editions, or editions of one document series, of the supplier\'s documents.',
         'Explainable difference': 'Values that differ, but the documents themselves state a different method, condition, unit, bound type or classification basis.',
         'Data-quality issue': 'A problem in how the JSON or a supplier document records a value, unit, label, derivation rule or identity.'}
FU = ['Supplier clarification', 'Edition-selection policy', 'Correctable from existing evidence (data owner)', 'Data-owner decision (field-selection rule)',
      'Standard or further source needed', 'No follow-up needed beyond documentation']
FU_DEF = {'Supplier clarification': 'The documents cannot settle the question; the finding-specific reason states what only the supplier can provide. Suppliers were not contacted.',
          'Edition-selection policy': 'Values differ between editions; a documented rule is needed for which edition supplies the working value. Supplier contact is not required unless an older value must be confirmed as obsolete.',
          'Correctable from existing evidence (data owner)': 'The evidence already in the archive or the evidence folder is sufficient for the data owner to correct or annotate the record. Not done by this audit.',
          'Data-owner decision (field-selection rule)': 'Values are compatible; the data owner should choose one consistent rule for which value the field holds.',
          'Standard or further source needed': 'A standard (ASTM D874) or a further dated document is needed before the finding can be completed.',
          'No follow-up needed beyond documentation': 'Not a disagreement, or a difference the documents themselves explain; both values stay documented.'}
F = json.load(open(os.path.join(RL.HERE, 'output', 'findings_v5.json'), encoding='utf-8'))
F4 = {f['id']: f for f in json.load(open(os.path.join(ORIG, 'findings_v4.json'), encoding='utf-8'))}
F3 = {f['id']: f for f in json.load(open(os.path.join(ORIG, 'findings_v3.json'), encoding='utf-8'))}
V2 = {r['conflict_id']: r for r in csv.DictReader(open(os.path.join(ORIG, 'comprehensive_conflicts_audit_v2_2026-10-27.csv'), encoding='utf-8-sig'))}
L3 = json.load(open(os.path.join(ORIG, 'corrections_v3.json'), encoding='utf-8'))
L4 = json.load(open(os.path.join(ORIG, 'corrections_v4.json'), encoding='utf-8'))
CAND = json.load(open(os.path.join(ORIG, 'candidates.json'), encoding='utf-8'))
CHG = list(csv.DictReader(open(os.path.join(RL.ROOT, 'docs', 'audit_review_2026-11-02', 'finding_changes.csv'), encoding='utf-8-sig')))
# every verification figure comes from the complete source inventory written by verification_ledger.py
LEDGER = json.load(open(os.path.join(RL.ROOT, 'docs', 'audit_review_2026-11-02', 'verification_results', 'ledger_summary.json'), encoding='utf-8'))
_K = LEDGER['by_kind']
COMPLETE = ('**Verification complete: yes**' if LEDGER['complete'] else
            f'**Verification complete: no** — {LEDGER["E"]} unresolved and {LEDGER["D"]} text-presence-only of {LEDGER["total"]} sources')
UNRES = '; '.join(f'{u["id"]}: {u["source"]}' for u in LEDGER['unresolved'])
OUT = ARGS.outdir
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


# ------------------------------------------------------------------ CSV
ch3, ch4 = collections.defaultdict(set), collections.defaultdict(set)
for x in L3: ch3[x['id']].add(x['field'])
for x in L4: ch4[x['id']].add(x['field'])
cols = ['conflict_id', 'material_class', 'supplier', 'product', 'record_id', 'property', 'conflict_category', 'finding_type', 'finding_type_definition', 'comparability',
        'nature', 'values', 'units_and_conditions', 'source_documents_and_pages', 'json_paths', 'tiers', 'explanation', 'verification_level', 'verification_status',
        'verification_priority', 'resolution_status', 'recorded_decision', 'follow_up_category', 'follow_up_reason', 'duplicate_of', 'related_ids',
        'recommended_next_step', 'provenance', 'affected_by_teammate_changes', 'changed_in_v3', 'changed_in_v4', 'changed_in_v5',
        'later_state_2026_10_31']
buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n'); w.writerow(cols)
for f in F:
    vals = f['values']
    w.writerow([f['id'], CLASS_LABEL[f['material_class']], f['supplier'], f['product'], f['record_id'], f['property'], f"{f['category']} {CAT[f['category']]}",
                f['group'], BASIS[f['group']], f['comparability'], f['nature'], ' || '.join(str(v.get('value')) for v in vals),
                ' || '.join('; '.join(str(x) for x in (v.get('unit'), v.get('conditions'), v.get('temperature_c') and f"{v['temperature_c']} °C", v.get('printed_text') and f'printed: {v["printed_text"]}') if x) for v in vals),
                ' || '.join(f"{v.get('file')}" + (f" p.{v['page']}" if v.get('page') not in (None, '') else '') + (f" ({v['revision_date']})" if v.get('revision_date') else '') + (f" [{v['doc_type']}]" if v.get('doc_type') else '') for v in vals if v.get('file')),
                ' ; '.join(f['json_paths']), ', '.join(sorted({m.group(1) for p in f['json_paths'] for m in [re.search(r'(tier\d|general|vm)', p)] if m})),
                f['explanation'], level(f), f['verification'], f['verification_priority'], f['resolution'], f['recorded_decision'], f['follow_up_category'],
                f['follow_up_reason'], f['duplicate_of'], f['related_ids'], f['next_step'], f['provenance'], f['teammate'],
                ', '.join(sorted(ch3.get(f['id'], set()) - {'verification_priority'})), ', '.join(sorted(ch4.get(f['id'], set()))),
                ', '.join(f['changed_in_v5']), f['later_state']])
open(os.path.join(OUT, 'comprehensive_conflicts_audit.csv'), 'w', encoding='utf-8-sig', newline='').write(buf.getvalue())

# ------------------------------------------------------------------ numbers
types = C(f['group'] for f in F); res = C(f['resolution'] for f in F); lv = C(level(f) for f in F); fu = C(f['follow_up_category'] for f in F)
n_doc = sum(1 for f in F if f['source_kind'] == 'documented'); n_new = sum(1 for f in F if f['provenance'].startswith('New'))
n_oq = sum(1 for f in F if 'open question only' in f['provenance']); n_notes = sum(1 for f in F if f['provenance'].startswith('Previously recorded in field notes'))
n_dup = sum(1 for f in F if f['duplicate_of'])
pend = [f for f in F if f['verification_priority']]; pr = C(f['verification_priority'].split(':')[0] for f in pend)
decisions = [f for f in F if f['recorded_decision'] and not f['recorded_decision'].startswith('PR #2')]
pc = [f for f in F if 'IM-1809E' in f['verification']]; pc_dup = sum(1 for f in pc if f['duplicate_of'])
so = [f for f in F if 'S-OIL web table' in f['verification']]; so_ed = sum(1 for f in so if f['group'] == 'Edition difference'); so_pot = [f['id'] for f in so if f['group'] == POT]
assert (len(pc), len(pc) - pc_dup, len(so), so_ed, so_pot) == (62, 61, 24, 23, ['CF-102']), (len(pc), pc_dup, len(so), so_ed, so_pot)

L = []; a = L.append
n_chg_ids = len({c['id'] for c in CHG})
a('# Comprehensive conflicts audit — lubricant raw-material data')
a('')
a('**Version 5 — revision of 2026-11-02 (current version).** Original audit: 2026-10-27 (quality review the same day); source-verification '
  'review and reporting corrections: 2026-10-30 (version 4, published in PR #4 at commit `e6617ca`). This revision corrects the reporting only: '
  f'{len(CHG)} field changes in {n_chg_ids} findings, every one listed with its before and after text, reason and evidence in '
  '`docs/audit_review_2026-11-02/finding_changes.csv` and summarised in section 8.3. The version-4 report and CSV are preserved in Git history '
  '(`git show e6617ca:reconciliation/comprehensive_conflicts_audit.md`).')
a('')
a('**Database state described.** The findings describe `Products_json` as it stood at the audit snapshot (`e6617ca`, 2026-10-30). Five product records '
  'were corrected or annotated afterwards (2026-10-31, commit `28265fd`); those later states are listed in section 8.4 and in the CSV column '
  '`later_state_2026_10_31`, and do not change the values recorded in the findings.')
a('')
a('Smart Formulator raw-material database (`Products_json`: 264 products, 706 JSON files). The audit was made on branch `audit/comprehensive-conflicts` '
  'from `main` at `77ba590` (no newer commits on GitHub on 2026-10-30). Neither the audit nor this revision changed any product JSON, template, coverage '
  'workbook, integration script or the curated log `open_questions_and_conflicts.md`; no conflict was resolved, averaged or settled by preferring one '
  'document type. Every finding is listed with the same ID in `comprehensive_conflicts_audit.csv`; evidence copies and hashes are in `audit_evidence/` '
  '(see `audit_evidence/evidence_manifest.md`).')
a('')
a('## Supervisor summary')
a('')
a('**What was examined.** All 706 records of the raw-material database. The 147 conflict entries already recorded in the JSON (125 distinct conflicts) were checked '
  'against the exact pages and product columns of the cited supplier documents; independent checks then searched for unrecorded problems (internal consistency of '
  'every value, physical plausibility, API base-oil group definitions, and 1,116 comparisons with every other archive document naming the same product). '
  'Multi-product tables were read column by column; pages without a text layer were read on screen. External sources were obtained and archived with hashes '
  '(Petro-Canada 2023.03 brochure, S-OIL base-oil page, API 1509 Annex E, a Chevron Phillips data sheet, the ADNOC specification, PubChem registry records, '
  'archived Afton data sheets, a Richful product feed).')
a('')
a(f'**What was found.** {len(F)} finding records (IDs CF-001 to CF-{len(F):03d}) in {len({f["record_id"] for f in F})} products. One pair records the same disagreement '
  f'twice (CF-093 duplicates CF-096), so there are {len(F) - n_dup} distinct issues.')
a('')
a('| Type | Records | Meaning |'); a('|---|---|---|')
for t in TYPES: a(f'| {t} | {types[t]} | {BASIS[t]} |')
a(f'| **Total** | **{len(F)}** | {len(F) - n_dup} distinct issues |')
a('')
a(f'{n_doc} records were already recorded as conflicts (all preserved), {n_oq} only as open questions, {n_notes} only in field notes, '
  f'{len(F) - n_doc - n_new - n_oq - n_notes} elsewhere (identity review, integration flags); **{n_new} are new**. Two source groups deserve mention: '
  f'**Petro-Canada PURITY** — {len(pc)} records representing {len(pc) - pc_dup} distinct issues (61 edition differences between LUB3213E 2015.07 and 2023.03; '
  'CF-093 duplicates CF-096); **S-OIL** — 24 records = 23 edition differences + 1 potential contradiction (CF-102: an SDS range compared with a web typical).')
a('')
a('**Most important open issues.**')
for s in ['Synfluid C12 Dimer pour point (data-quality): the archive sheet heads the column "°F, °C" but the values only fit °C (°F); the manufacturer\'s own sheet prints −53 °C (−63 °F), whereas the database stored −63 °C at the snapshot (corrected to −53 °C on 2026-10-31; section 8.4).',
          'Ergon HyGold L750 (confirmed contradiction): one data sheet prints density 0.854 g/cm³ and specific gravity 0.9183 at the same temperature; the SDS (0.92) supports the specific gravity.',
          'Richful RF6069 and RF6077 (confirmed contradictions): TDS and SDS kinematic viscosities at 100 °C differ with the same method (RF6069 118 vs 142 mm²/s), and RF6077 density is lower at 15 °C than at 20 °C. Richful RF6066 (potential contradiction, CF-009): the two undated TDS print 227 and 185 mm²/s, and the 2021 SDS prints its 185 mm²/s on a "Viscosity, dynamic" line.',
          'Undocumented TDS vs SDS flash-point differences of 5–31 °C by the same open-cup method (confirmed: Chevron Phillips Synfluid PAO 4/6/8, mPAO 150; ExxonMobil SpectraSyn Elite 150).',
          'S-OIL Ultra-S 4 SDS (confirmed): the chemical name ("hydrotreated light paraffinic") and the CAS number (registered as "hydrotreated heavy paraffinic") do not match.',
          'aramcoPRIMA 70 (potential contradiction): the specification heading says Group II, but its viscosity-index minimum (76) lies below the API 1509 Group II floor (80). No measured or typical VI is printed, so this shows only that the specification does not guarantee the Group II VI criterion; it does not show that the product\'s VI is below 80 or that the label is wrong.',
          'Sulfated ash (data-quality): at the snapshot, the 26 estimated values used two different zinc factors — an inconsistent calculation method, which does not by itself show which factor or estimate is wrong; for Lubrizol CV1100 and CV3515 the estimates (5.8 and 9.2 wt.%) differed from the typical values printed in the products\' own data sheets (7 and 10 % weight). Since 2026-10-31 those two records hold the printed values and 24 estimates remain (section 8.4).']:
    a(f'- {s}')
a('')
a(f'**Verification.** "Verified" means the evidence stated for the finding was checked in the source; it does not mean the disagreement was scientifically resolved or that '
  f'every follow-up action is complete (definition in section 4). {lv["Verified"]} records are verified, {lv["Partially verified"]} partially verified and {lv["Pending"]} pending. '
  f'{pend.__len__()} items still need evidence that could not be obtained (High {pr.get("High", 0)}, Medium {pr.get("Medium", 0)}, Low {pr.get("Low", 0)}; section 4). '
  f'At source level (version 5): {LEDGER["total"]} sources examined (every value citation, every document cited in an explanation and every source named in '
  f'a finding text); {LEDGER["verified"]} fully verified ({LEDGER["A"]} by automated checks, {LEDGER["B"]} visually, {LEDGER["C"]} by context review of the text); '
  f'{LEDGER["D"]} rest on an automated text-presence check alone; {LEDGER["E"]} unresolved; {LEDGER["N"]} named only as not consulted. {COMPLETE}.')
a('')
a('**Follow-up needed.** No finding is resolved by this audit. The follow-up differs by finding; each record states its own reason:')
a('')
a('| Follow-up | Records | Meaning |'); a('|---|---|---|')
for k in FU: a(f'| {k} | {fu[k]} | {FU_DEF[k]} |')
a('')
a(f'**Resolution labels.** Of the {len(decisions)} records the database marks as resolved, {len(decisions) - 1} hold a working value (a newer dated edition, or a user '
  'decision of 2026-10-18) and one is a temperature note. The audit keeps these decisions but reports the underlying disagreements as unresolved (section 6). Three records '
  'are not value conflicts (the temperature note and two sets of claims changed between bulletin editions).')
a('')
a('**Limitations.** ASTM D874 was not accessed, so the sulfated-ash calculation cannot be validated; two Afton editions could not be retrieved; suppliers were not contacted; '
  '31 archive PDFs have no text layer (checked visually only where a finding depends on them); a value that coincides with another grade\'s value in a multi-grade table '
  'can escape automated comparison.')
a('')
a('## 1. Summary tables')
a('')
a('| Type | ' + ' | '.join(l for _, l in CLS) + ' | Total |'); a('|---|' + '---|' * 4)
for t in TYPES:
    row = [sum(1 for f in F if f['group'] == t and f['material_class'] == k) for k, _ in CLS]; a(f'| {t} | ' + ' | '.join(map(str, row)) + f' | {sum(row)} |')
a('| **Total** | ' + ' | '.join(str(sum(1 for f in F if f['material_class'] == k)) for k, _ in CLS) + f' | **{len(F)}** |')
a('')
a('| Category | ' + ' | '.join(TYPES) + ' | Total |'); a('|---|' + '---|' * 6)
for c in sorted({f['category'] for f in F}):
    row = [sum(1 for f in F if f['category'] == c and f['group'] == t) for t in TYPES]; a(f'| {c} {CAT[c]} | ' + ' | '.join(map(str, row)) + f' | {sum(row)} |')
a('')
a('| Follow-up | ' + ' | '.join(TYPES) + ' | Total |'); a('|---|' + '---|' * 6)
for k in FU:
    row = [sum(1 for f in F if f['follow_up_category'] == k and f['group'] == t) for t in TYPES]; a(f'| {k} | ' + ' | '.join(map(str, row)) + f' | {sum(row)} |')
a('')
a('| Resolution status | Records |'); a('|---|---|')
for k, v in res.most_common(): a(f'| {k} | {v} |')
a('')
a('| Verification level | Records |'); a('|---|---|')
for k, v in lv.most_common(): a(f'| {k} | {v} |')
a('')
a('No findings in C07 (cross-tier), C08 (Reported without evidence) or C11 (stale normalised values). C12 (teammate changes) is a column on every finding.')
a('')
a('## 2. Repository state and the teammate\'s changes')
a('')
a('`origin/main` = `main` = `77ba590` (PR #3, identical tree to our reconciliation commit `a107745`); no newer commits, branches, pull requests or forks. PR #2 '
  '(Rawan-Mohammad: `53ed010`, `a38d5ca`, merged as `8a8d875`, 2026-10-24) added normalised `*_final` keys, resolution proposals and two scripts; PR #3 kept the '
  'normalised keys that still matched the validated values, removed 138 stale ones, and kept the 23 averaging or TDS-preference proposals as text marked "not adopted". '
  'This audit reports current problems only: stale keys removed in PR #3 are not findings, and the kept proposal texts are mentioned only where they are wrong (CF-180) '
  'or where the record still says resolved.')
a('')
a('## 3. Most significant open issues')
a('')
SIG = [('CHEVRON_SYNFLUID_DIMER_C12', 'pour'), ('ERGON_HYGOLD_L750', 'density'), ('RICHFUL_RF6069', 'kv100'), ('RICHFUL_RF6077', 'tier2.density'),
       ('EXXONMOBIL_SPECTRASYN_ELITE_150', 'flash'), ('CHEVRON_SYNFLUID_MPAO_150', 'flash'), ('S_OIL_ULTRA_S_4', 'CAS'), ('ARAMCO_LUBEREF_PRIMA_70', 'api_group'),
       ('PETRONAS_ETRO_6_PLUS', 'kv40'), ('NYNAS_NYFROST_32', 'flash'), ('LUBRIZOL_CV1100', 'sulfated'), ('LUBRIZOL_CV3515', 'sulfated'), ('MINGLAN_T3161A', 'sulfated'),
       ('TIANHE_P_TEC_3232', 'density'), ('RICHFUL_RF6066', 'tier2.kv100'), ('ARAMCO_LUBEREF_PRIMA_70', 'tier2.flash'), ('RF6602', 'flash')]
a('| ID | Product | Property | Values | Type | Comparability | Follow-up |'); a('|---|---|---|---|---|---|---|')
for rid, kw in SIG:
    m = [f for f in F if f['record_id'] == rid and kw.lower() in f['property'].lower()]
    if not m: continue
    f = m[0]
    a(f"| {f['id']} | {md(f['product'])} | {md(f['property'], 45)} | {md(' vs '.join(vtext(v, False) for v in f['values'] if v.get('value') is not None or v.get('printed_text')), 220)} | "
      f"{f['group']} | {md(f['comparability'], 110)} | {f['follow_up_category']} |")
a('')
a('## 4. Verification: definition, status and pending items')
a('')
a('**Definition.** "Verified" means that the evidence stated in the finding\'s verification text was checked in the cited source: the value, the product (and, in '
  'multi-product tables, the column), and the unit, qualifier, method, temperature and edition date wherever the comparison depends on them. It does **not** mean that '
  'the disagreement was scientifically resolved, that comparability is confirmed (see the comparability column), or that every follow-up action is complete. '
  '"Partially verified" means some of the stated evidence could not be obtained; "Pending" means the check could not be done; "JSON-only" means the issue lies in the '
  'data itself.')
a('')
a('| Priority | ID | Product | Property | What is missing | Follow-up |'); a('|---|---|---|---|---|---|')
for lvl in ('High', 'Medium', 'Low'):
    for f in [x for x in pend if x['verification_priority'].startswith(lvl)]:
        a(f"| {lvl} | {f['id']} | {md(f['product'], 40)} | {md(f['property'], 45)} | {md(f['verification_priority'].split(': ', 1)[-1], 150)} | {f['follow_up_category']} |")
a('')
a('Checks completed in the 2026-10-30 review where evidence was accessible: API 1509 Annex E (CF-145, CF-146, CF-147), the manufacturer\'s Dimer C12 sheet (CF-136), '
  'PubChem records (CF-171), the Ultra-S 6 catalog column (CF-172), the Infineum D3375 page (CF-158), the HiTEC 12200 and 12210M bulletins (CF-166, CF-167), the RF6602 '
  'product feed (CF-162), the Richful supplier spellings (CF-179), the PURITY L65 brochure (CF-093) and two of four HiTEC 5748 editions (CF-164). Still open: ASTM D874 '
  '(CF-144), supplier-only questions (CF-140, CF-146, CF-147, CF-177, CF-178), two HiTEC 5748 editions (CF-164) and the value kind of the ADbase 3 cSt VI 120 '
  '(CF-145). In version 5 (2026-11-02) the SDS flash-point bounds of CF-150 and CF-152 to CF-156, which version 4 had quoted from the JSON, were read on their '
  'cited pages.')
a('')
a('**Source-level verification (version 5, 2026-11-02).** Every source used by a finding was classified by how it was actually verified '
  '(ledger: `docs/audit_review_2026-11-02/verification_results/citation_ledger.csv`). The inventory covers each value citation, each document cited only in '
  'an explanation, and each source a finding names in its explanation, verification, comparability or follow-up text (for example API 1509, PubChem, '
  'ASTM D874, the identity review, Internet Archive captures). A number that merely appears on the cited page does not count as verified, and nothing is '
  'verified by default: only an automated column/row check or an explicit reviewer verdict counts; an "incomplete" or "unavailable" verdict stays unresolved.')
a('')
a('| Source category | Sources |'); a('|---|---|')
a(f'| Sources examined | {LEDGER["total"]} (in {LEDGER["findings"]} findings: {_K.get("value citation", 0)} value citations, '
  f'{_K.get("document cited in the explanation", 0)} documents cited in explanations, {_K.get("referenced source", 0)} sources named in finding texts) |')
a(f'| Fully verified: automated check (multi-grade table columns, capture comparison, quotation comparison) | {LEDGER["A"]} |')
a(f'| Fully verified: visual check (page render, image, vector claims matrix) | {LEDGER["B"]} |')
a(f'| Fully verified: context review of the text (row label, unit, condition, column) | {LEDGER["C"]} |')
a(f'| **Fully verified, total** | **{LEDGER["verified"]}** |')
a(f'| Automated text-presence check only (association not established) | {LEDGER["D"]} |')
a(f'| Unresolved | {LEDGER["E"]} |')
a(f'| Named only as not consulted (no evidence role) | {LEDGER["N"]} |')
a('')
a(f'{COMPLETE}.' + (f' Unresolved sources: {UNRES}.' if UNRES else ''))
a('')
a('')
a('## 5. Findings by type, material class and category')
a('')
for gi, t in enumerate(TYPES, 1):
    sub_t = [f for f in F if f['group'] == t]
    a(f'### 5.{gi} {t} ({len(sub_t)})'); a(''); a(BASIS[t]); a('')
    for k, label in CLS:
        sub = [f for f in sub_t if f['material_class'] == k]
        if not sub: continue
        a(f'#### {label} ({len(sub)})'); a('')
        a('| ID | Cat. | Supplier / product | Property | Values, conditions and sources | Comparability | Explanation | Verification | Status / recorded decision | Follow-up | Provenance |')
        a('|---|---|---|---|---|---|---|---|---|---|---|')
        for f in sorted(sub, key=lambda x: (x['category'], x['id'])):
            vals = '<br>'.join(md(vtext(v), 280) for v in f['values'])
            st = f['resolution'] + (f"; decision: {f['recorded_decision']}" if f['recorded_decision'] and not f['recorded_decision'].startswith('PR #2') else '')
            extra = (f"; duplicate of {f['duplicate_of']}" if f['duplicate_of'] else '') + (f"; related: {f['related_ids']}" if f['related_ids'] else '')
            prov = f['provenance'] + extra + ('; teammate: ' + f['teammate'] if f['teammate'].startswith('Yes') else '')
            a(f"| {f['id']} | {f['category']} | {md(f['supplier'], 35)} / {md(f['product'], 45)} | {md(f['property'], 60)} | {vals} | {md(f['comparability'], 520)} | "
              f"{md(f['explanation'], 380)} | {level(f)}: {md(f['verification'], 220)} | {md(st, 200)} | {f['follow_up_category']}: {md(f['follow_up_reason'], 220)} | {md(prov, 170)} |")
        a('')
a('## 6. Resolution labels and recorded decisions')
a('')
a('Selecting a working value for a field is a recorded decision, not a scientific resolution of disagreeing sources. The database (JSON `resolved: true`) still marks the '
  'records below as resolved; this audit keeps those decisions and reports the underlying disagreement separately.')
a('')
a('| ID | Product | Property | Audit status | Recorded decision | Follow-up |'); a('|---|---|---|---|---|---|')
for f in decisions:
    a(f"| {f['id']} | {md(f['product'], 40)} | {md(f['property'], 50)} | {f['resolution']} | {md(f['recorded_decision'], 280)} | {f['follow_up_category']} |")
a('')
for f in [x for x in F if x['source_kind'] == 'documented' and 'RECONSIDER: ' in x['explanation']]:
    a(f"- **{f['id']} reconsideration:** {md(f['explanation'].split('RECONSIDER: ')[-1].split(' final_resolution:')[0], 500)}")
a('')
a('## 7. Preservation, duplicates and novelty')
a('')
a('- All 147 conflict entries in the JSON (125 distinct conflicts) appear in the CSV with their JSON paths; all 125 conflict lines of the curated log map to a finding; '
  'values, notes, recorded user decisions and the `resolved` flags are unchanged in the data. Two records that list sources without values (CF-024, CF-025) show the '
  'values read from those sources.')
a('- Duplicate: CF-093 (PURITY L65 viscosity index, stored as text: "brochure reports 104") and CF-096 (structured edition difference, LUB3213E 2015.07 VI 92 vs 2023.03 '
  f'VI 104) record the same disagreement. Both IDs are kept; {len(F) - n_dup} distinct issues; Petro-Canada: {len(pc)} records, {len(pc) - pc_dup} distinct issues.')
a('- Related but distinct: CF-159 is a label/unit issue inside the SDS value used in CF-009; CF-180 concerns the proposal text attached to CF-016; CF-141 adds a third '
  'source to the documented Ultra-S 6 conflicts CF-116 to CF-120 and to CF-172.')
a(f'- The {n_new} new findings were re-checked against every open question, note, calculation note and conflict entry of the product, the curated log, the README and the '
  '`reconciliation/` files: the documents involved are listed in the inventory register, but none of the discrepancies is described anywhere. The 9 Richful flash-point '
  'findings remain classed as recorded in field notes.')
a('')
a('## 8. Correction log')
a('')
a(f'IDs CF-001 to CF-{len(F):03d} are unchanged in every version; no finding was added or removed. Field-level changes are listed per finding in the CSV columns '
  '`changed_in_v3`, `changed_in_v4` and `changed_in_v5`. Sections 8.1 and 8.2 are the version-4 log, kept as written; their counts refer to version 4.')
a('')
v2t = C(r['finding_type'] for r in V2.values()); v3t = C(f['group'] for f in F3.values()); v4t = C(f['group'] for f in F4.values())
pend4 = [f for f in F4.values() if f['verification_priority']]
a('| Count | 2026-10-27 | 2026-10-30 source review | 2026-10-30 version 4 | 2026-11-02 version 5 (this version) |'); a('|---|---|---|---|---|')
a(f"| Contradiction records | {v2t['Genuine contradiction']} (one group) | {v3t['Genuine contradiction']} (one group) | {v4t[CONF]} confirmed + {v4t[POT]} potential | {types[CONF]} confirmed + {types[POT]} potential |")
for t in TYPES[2:]: a(f'| {t} | {v2t.get(t, 0)} | {v3t.get(t, 0)} | {v4t[t]} | {types[t]} |')
a(f"| Resolution: Resolved | {sum(1 for r in V2.values() if r['resolution_status'] == 'Resolved')} | 0 | 0 | 0 |")
a(f'| Distinct issues | 180 | {len(F) - n_dup} | {len(F) - n_dup} | {len(F) - n_dup} |')
a(f'| Pending or partially verified (excluding external-source groups) | 16 | 8 | {len(pend4)} | {len(pend)} |')
a('')
a('### 8.1 Source-verification review (2026-10-30)')
a('')
for s in ['Petro-Canada: 62 records (61 distinct issues) moved from "not verifiable from the repository" to verified in both editions, column and row (LUB3213E 2015.07 and 2023.03; archived official file, SHA-1 identical to the mirror cited in the records).',
          'S-OIL: 24 records = 23 edition differences verified column by column (catalog DL2-11177 and the S-OIL web table, live page identical to the Internet Archive capture of 2026-06-10) + 1 potential contradiction (CF-102: SDS DL2-14611 range "42.0 - 55.0 cSt" vs web typical 41.10; reclassified from edition difference).',
          'CF-145: Group II classification explained by the ADNOC specification (VI minimum 100); reclassified as explainable. CF-024: suspected unit misprint (typical 1.3 ppm vs maximum 1.3 wt.%); reclassified as data-quality.',
          'CF-093: reclassified as edition difference and marked as a duplicate of CF-096.',
          'CF-157, CF-158: the "110 min." flash points are printed in "Typical Inspections" tables marked "Not a specification"; JSON follows the table heading.',
          'CF-164, CF-167: wording aligned with the records (comparability not established; claims additions). Resolution labels: 12 "Resolved" became Unresolved (working value recorded) or "Not a value conflict" (3 records in all).',
          'Comparability added to every finding; 13 contradiction records found to have uncertain comparability. Revision dates, product identity and table columns re-checked for every archive value.']:
    a(f'- {s}')
a('')
fu4 = C(f['follow_up_category'] for f in F4.values())
a('### 8.2 Reporting corrections (version 4, 2026-10-30)')
a('')
for s in ['S-OIL summary corrected everywhere to "24 records = 23 edition differences + 1 potential contradiction (CF-102)"; the earlier text "all 24 S-OIL edition differences" was wrong.',
          f'Contradiction records split into {v4t[CONF]} confirmed contradictions and {v4t[POT]} potential contradictions (comparability uncertain) in the CSV `finding_type`, the definitions, headings, summary tables and totals. IDs, evidence and uncertainty notes unchanged; no uncertain comparison was moved to "explainable".',
          'The statement that 145 findings "can only be settled by suppliers" was removed. Every record now has a `follow_up_category` and a finding-specific `follow_up_reason`: '
          + ', '.join(f'{k} {fu4[k]}' for k in FU) + '. Supplier clarification is assigned only where the documents cannot settle the question, with the reason stated.',
          'CF-144 tightened: the two zinc factors show an inconsistent calculation method; they do not by themselves show which factor or estimate is wrong. The 26 values are estimates from element contents, not measured sulfated ash; validation against the applicable ASTM D874 provisions stays pending. CF-142 and CF-143 now distinguish the estimate from the printed typical value.',
          '"Verified" defined (section 4): the stated evidence was checked; it does not mean the disagreement is resolved, that comparability is confirmed, or that follow-up is complete.',
          'The CSV `nature` text of 31 contradiction records began "Genuine contradiction"; it now begins with the record\'s type ("Confirmed contradiction" or "Potential contradiction (comparability uncertain)"), so no description contradicts its classification.',
          'Most-significant table: the Richful viscosity statement now gives the TDS-vs-SDS difference (24 mm²/s, RF6069) separately from the difference between the two undated RF6066 TDS (42 mm²/s).']:
    a(f'- {s}')
a('')
a('### 8.3 Reporting corrections (version 5, 2026-11-02)')
a('')
a('A review of all 180 findings against the report, the CSV, the product JSON at `e6617ca` and the cited sources (method and results: '
  '`docs/audit_review_2026-11-02/`). Every changed field, with its before and after text, reason and evidence, is in '
  '`docs/audit_review_2026-11-02/finding_changes.csv`.')
a('')
for s in [f'Classification: CF-146, CF-170 and CF-172 changed from confirmed to potential contradiction, CF-141 and CF-164 from edition difference to potential '
          f'contradiction, and CF-145 from explainable difference to potential contradiction. Counts: confirmed {v4t[CONF]} → {types[CONF]}, potential {v4t[POT]} → '
          f'{types[POT]}, edition difference {v4t["Edition difference"]} → {types["Edition difference"]}, explainable {v4t["Explainable difference"]} → '
          f'{types["Explainable difference"]}; data-quality unchanged.',
          'CF-145 (ADbase 3 cSt): version 4 explained the Group II label as "a specification minimum vs a typical value", but DL2-12221 prints VI 120 as a single value '
          'under "PRODUCT SPECIFICATIONS" with no min/max/typical label and no date. Whether 120 is a typical, minimum or maximum value is not stated, so comparability is '
          'uncertain. Follow-up: a dated ADNOC document stating the value kind (standard or further source needed); supplier contact is optional in every field.',
          'CF-146 (aramcoPRIMA 70): the VI 76 is a specification minimum, not a measured VI, and the archive prints no typical VI for this grade. The finding now states that '
          'the comparison with the API 1509 Group II floor (VI 80) shows only that the specification does not guarantee the Group II VI criterion; it does not show '
          'that the product\'s VI is below 80 or that the Group II label is wrong.',
          'CF-170 (aramcoPRIMA 500 density): one value has no printed unit and neither document is dated; the record\'s own open question calls it "not a confirmed numerical '
          'contradiction". Classified like CF-168 and CF-169, which compare the same two documents; the unit is not assumed.',
          'CF-172 (Ultra-S 6 specific gravity): the comparability now separates the two specific-gravity tables (catalog 0.843 and Cosan sheet 0.840, same stated '
          'quantity, temperatures and method, both undated) from the SDS value 0.841, whose method and water reference temperature are not stated.',
          'CF-141 (Ultra-S 6, Cosan sheet): version 4 said the values differ "between dated editions", but neither archive sheet prints a date (PDF file metadata only: '
          '2009-06-01 and 2012-08-27) and the web table is undated; follow-up changed from edition-selection policy to standard or further source needed (dated editions).',
          'CF-164 (HiTEC 5748 SSI): comparability is uncertain (no edition prints the SSI method) and one value comes from another product\'s bulletin, so the finding is a '
          'potential contradiction rather than an edition difference; the evidence pages (p.2 of both saved Afton data sheets) were added.',
          'Page references: CF-031 and CF-032 now give the verified SDS page (DL2-13444.pdf p.7) beside the JSON citation (p.6); CF-033 to CF-036 add p.1 for the '
          'one-page TDS DL2-10234.pdf, which the JSON cites without a page. The JSON citations are unchanged.',
          'Verification: version 4 marked CF-150 and CF-152 to CF-156 "Verified" while stating that their SDS flash-point bounds were quoted from the JSON and not re-read. '
          'Each bound was read on its cited page on 2026-11-02 (text layer, or a page render for DL2-15541.pdf), so the "Verified" level is now supported.',
          f'Follow-up and next steps: pending items {len(pend4)} → {len(pend)} (the item of CF-145 now names the missing value kind). The CSV-only `recommended_next_step` contradicted the follow-up category in '
          f'{sum(1 for c in CHG if c["field"] == "next_step" and c["id"] not in ("CF-141", "CF-145"))} '
          'records (for example, edition-selection records required supplier contact, and CF-015 and CF-020 said "none required" under supplier clarification); each '
          'now agrees with its category, as do the revised next steps of CF-141 and CF-145.',
          'Claims matrices: the dots of the Afton HiTEC 12200 and 12210M claims tables are drawings, not text. They were extracted (each mark assigned to its row and '
          'column label through the cell separators of the table) and read on 300 dpi renders: CF-001, CF-002 and CF-167 are confirmed cell by cell, and the statement '
          'in CF-166 that the dots agree in the columns present in both tables holds for all 45 shared cells. CF-005 to CF-007 (Lubrizol CV7540 claim codes "L" '
          'and "A") were read by word position with their legends. Their verification texts now state these checks.',
          'CF-024: the printed text of the aramcoDURA BS150 sulfur value is completed: the row prints "ASTM D5453" in its method column and the value carries the '
          'note "‡ - D 2622"; version 4 quoted only the note.',
          f'Source-level verification (section 4): every source a finding uses (value citations, documents cited in explanations, and sources named in the '
          f'finding texts such as API 1509, PubChem and ASTM D874) is classified from explicit evidence only. Of {LEDGER["total"]} sources, {LEDGER["verified"]} are '
          f'fully verified, {LEDGER["D"]} rest on text presence alone and {LEDGER["E"]} are unresolved ({UNRES or "none"}); the verification is '
          f'{"complete" if LEDGER["complete"] else "therefore not complete"}.',
          'CF-163: the comparability states that the confirmed contradiction rests on the blending limit (60 vs 65 ℃); the differently worded storage limits are not part of it.',
          'Summary statements corrected: the Richful bullet no longer calls RF6066 a confirmed contradiction (CF-009 is potential); the aramcoPRIMA 70 bullet follows CF-146; '
          'the Dimer C12 and sulfated-ash bullets state the snapshot state and point to the later corrections.']:
    a(f'- {s}')
a('')
a('### 8.4 Later data corrections (2026-10-31, after the snapshot)')
a('')
a('These product-data corrections were made after the audit (commit `28265fd`, log `comprehensive_conflicts_audit_corrections_2026-10-31.md`). The findings '
  'keep the values recorded at the snapshot; the current state is:')
a('')
a('| ID | State after 2026-10-31 |'); a('|---|---|')
for f in F:
    if f['later_state']:
        a(f"| {f['id']} | {md(f['later_state'])} |")
a('')
a('## 9. Not counted as conflicts')
a('')
ST_SNAPSHOT = "{'Reported': 3664, 'Missing': 2537, 'Not Applicable': 7, 'Calculated': 38, 'Not Required': 11}"  # e6617ca, as printed in version 4
for s in ['Method differences: SpectraSyn 2 flash point 157 °C (COC) vs 145 °C (PMCC); aramcoDURA BS150 282 °C (COC) vs 232 °C (PMCC).',
          'Bounds and ranges that contain the typical values (Ergon and Neste SDSs, ADNOC 6 cSt and Formosa specifications); rounding (Lubrizol, ADNOC, Ergon unit conversions; S-OIL SDS relative densities; PURITY L50 certificate of analysis).',
          'Byte-identical copies (Petro-Canada DL2-11262 to DL2-11265; Cosan DL2-11241, DL2-11242); column misattributions screened out (HiTEC 12204L / 12200).',
          f'Metadata gaps (at the snapshot `e6617ca`): value objects by status {ST_SNAPSHOT}; {len(CAND["_no_final_numeric"])} numeric value objects without `value_final`; BT 3088 units not printed; MINGLAN T3161A slash values; ADNOC 4/6/8 flash methods not printed; the VM-field layout of three components.']:
    a(f'- {s}')
a('')
a('## 10. Limitations')
a('')
for s in ['ASTM D874-23 (sulfated ash) is sold by ASTM and was not accessed; CAS Common Chemistry requires an API key (PubChem used instead).',
          'Suppliers were not contacted; the records marked "Supplier clarification" state what each would need to provide.',
          'Two Afton HiTEC 5748 editions (03/18, 04/21) could not be retrieved: the Internet Archive search was temporarily offline on 2026-10-30.',
          '31 archive PDFs have no text layer and 13 files are images; DL2-13731.pdf uses an encoded font. These were read visually only where a finding depends on them.',
          'The automated comparison can miss a value that coincides with another grade\'s value in a multi-grade table.',
          'Physical checks use general relationships only (density falls with temperature; °F/°C conversion; API 1509 definitions); no viscosity index was recalculated.']:
    a(f'- {s}')
a('')
open(os.path.join(OUT, 'comprehensive_conflicts_audit.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('written', len(F), dict(types), '| follow-up', dict(fu), '| levels', dict(lv), '| pending', dict(pr))
