"""Write open_questions_and_conflicts.md = our HEAD log + an 'Integration of origin/main' section.

Usage: python log_section.py <repo> <resolve_report.json> <integrate_products.py>
"""
import collections, importlib.util, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
repo, rep_path, ip_path = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('ip', ip_path); ip = importlib.util.module_from_spec(spec); spec.loader.exec_module(ip)
rep = json.load(open(rep_path, encoding='utf-8'))
head = subprocess.run(['git', 'show', 'HEAD:open_questions_and_conflicts.md'], cwd=repo, capture_output=True, check=True).stdout.decode('utf-8')


def load(f):
    with open(ip.long_path(os.path.normpath(os.path.join(repo, f))), encoding='utf-8') as fh:
        return json.load(fh)


def cell(v, n=None):
    s = '–' if v in (None, '', []) else (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v))
    s = re.sub(r'\s+', ' ', s).replace('|', '\\|')
    return s if n is None or len(s) <= n else s[:n - 1] + '…'


def prod(f):
    return f.split('/')[-2]


def node_at(doc, path):
    out = {}
    def rec(n, p):
        if isinstance(n, dict):
            if 'status' in n and 'value' in n and not isinstance(n['status'], dict): out[p] = n
            for k, v in n.items():
                if k not in ('source', 'alternate_entries') and k not in ip.OWN_KEYS: rec(v, f'{p}.{k}' if p else k)
        elif isinstance(n, list):
            for i, v in enumerate(n): rec(v, f'{p}[{i}]')
    rec(doc.get('fields', {}), '')
    return out.get(path)


L = []
w = L.append
cd, od = rep['conflict_decisions'], rep['override_decisions']
cc = collections.Counter(d['decision'] for d in cd)
w('\n## Integration of origin/main (data-integration PR #2), 2026-10-24\n')
w('`origin/main` (commits 53ed010 and a38d5ca) added `integrate_products.py`, `build_conflicts_report.py` and the '
  'output of `integrate_products.py` to every product JSON file that existed at the time. That output is additive: '
  'normalised `value_final` / `unit_final` / `min_final` / `max_final`, `unit_conversion` and `integration_flags` keys, '
  'field-level resolutions, and `resolved` / `final_resolution` on conflict entries. It was computed from the data before '
  'the Task 3 corrections on this branch. It was reconciled against the validated Task 3 data under the data rules '
  'approved on 2026-10-24:\n')
w('1. Conflicting datasheet values are never averaged automatically; both values and sources are kept and the conflict '
  'stays unresolved unless authoritative evidence supports a resolution.')
w('2. TDS is never preferred over SDS automatically, nor the reverse; measurement conditions, test methods, revision '
  'dates, source reliability and comparability are evaluated.')
w('3. The coverage matrix reports the validated `status`; `status_final` is never substituted for it.\n')
w('No original key (value, printed text, unit, test temperature, method, status, source, notes, conflicts, open '
  'questions) was changed. The report generated on `origin/main` from the pre-correction data is kept in the history of '
  'that branch; `build_conflicts_report.py` is kept for review and has not replaced this log.\n')

w('### Conflict annotations from origin/main\n')
w(f"{len(cd)} conflict entries matched a rule in `integrate_products.py` ({len(ip.CONFLICTS)} rules; some entries are "
  f"repeated in several tier files): {cc['accepted (resolved)']} accepted as resolved, "
  f"{cc['accepted (kept unresolved)']} accepted as unresolved, {cc['not adopted (left unresolved)']} not adopted "
  "(left unresolved, `resolved: false`, with the proposal kept in `final_resolution`). Accepted resolutions rest on a "
  "newer dated edition of the same supplier document, or on a user decision recorded on 2026-10-18; both need "
  "confirmation (see Human review). Conflict entries that match no rule carry no `resolved` key and remain as recorded "
  "above.\n")
w('| Product | Tier | Conflict | Decision | resolved | final_resolution |')
w('|---|---|---|---|---|---|')
for d in cd:
    doc = load(d['file']); c = doc['conflicts'][d['index']]
    w(f"| {prod(d['file'])} | {doc.get('tier')} | {cell(c.get('field') or c.get('property'), 60)} | {d['decision']} | "
      f"{str(c.get('resolved')).lower()} | {cell(c.get('final_resolution'), 400)} |")

w('\n### Field-level resolutions proposed on origin/main\n')
w('Each of the 33 overrides in `integrate_products.py` was checked against the current field. The validated field '
  '(value, unit, status, source) is unchanged in every case.\n')
w('- **Rejected, value-changing (12):** the proposal replaced the field value in `value_final` by an average '
  '(`Calculated`) or by choosing one document type or a typical value over a bound. No `*_final` keys are kept on '
  'these value objects.')
w('- **Resolution text not adopted (11):** the field value is unchanged, but the justification relies on preferring TDS '
  'over SDS or another document. The `resolution` text was dropped from the value object (it is kept in the conflict '
  "entry's `final_resolution` proposal); normalised keys were kept only where they match the current value.")
w('- **Accepted annotations (10):** value unchanged and the reasoning rests on a newer dated edition, a recorded '
  '2026-10-18 user decision, or explicitly leaves the conflict unresolved.\n')
w('| Product | Tier | Property | Decision | Proposed value_final | Validated value (unit) | Proposal |')
w('|---|---|---|---|---|---|---|')
for d in od:
    doc = load(d['file']); n = node_at(doc, d['path']) or {}
    tier = doc.get('tier'); ov = ip.OVERRIDES[(prod(d['file']), tier, d['path'])]
    proposed = ov.get('value', '(field value)')
    if 'value' in ov and ov.get('status_final'): proposed = f"{proposed} ({ov['status_final']})"
    w(f"| {prod(d['file'])} | {tier} | `{d['path']}` | {d['decision']} | {cell(proposed)} | "
      f"{cell(n.get('value'))} ({cell(n.get('unit'))}) | {cell(ov.get('resolution'), 400)} |")

stale = rep['stale_dropped']
w('\n### Normalised keys\n')
w(f"- Kept where re-deriving them from the current value object with the same normalisation rules gives the identical "
  f"result: {rep['kept_nodes']} value objects.")
w(f"- Removed as stale: {len(stale)} value objects in {len({s['file'] for s in stale})} files, where a Task 3 "
  "correction changed the value, unit, bounds or printed text (for example the specific-gravity separation, corrected "
  "inequality bounds, density provenance and units). They were not recomputed; they are absent until "
  "`integrate_products.py` has been reviewed and re-run.")
w(f"- Absent: {rep['no_main_counterpart']} value objects added on this branch inside existing files (for example "
  "`specific_gravity`), and every value object of the 32 JSON files added on this branch.\n")
w('| Product | Tier | Property | Validated value (unit) | Stale value_final (unit_final) on origin/main |')
w('|---|---|---|---|---|')
for s in stale:
    doc = load(s['file'])
    w(f"| {prod(s['file'])} | {doc.get('tier')} | `{s['path']}` | {cell(s['our_value'])} ({cell(s['our_unit'])}) | "
      f"{cell(s['main'].get('value_final'))} ({cell(s['main'].get('unit_final'))}) |")

w('\n### Human review\n')
w('- Confirm the accepted resolutions: AFTON_HITEC_12200 (08/18 bulletin over 05/18), LUBRIZOL_CV7540 (2022 sheet over '
  '2020), NYNAS_NS_3 (2024 edition over 2016), RICHFUL_RF6077 and RICHFUL_RF6088F (user decisions of 2026-10-18), and '
  'the ARAMCO_LUBEREF_DURA_BS150_YANBU density note (no value conflict).')
w('- Decide the unresolved conflicts listed above as "not adopted" on their evidence (methods, temperatures, dates, '
  'reliability), in particular RICHFUL_RF6066 (two undated TDS differing by about 20 % in KV100; fields hold values '
  'from the supplier web page), PETRONAS_ETRO_6_PLUS density (TDS 0.8429 kg/L with no temperature vs SDS 0.8486 '
  'g/cm³ at 15 °C), INFINEUM_D3424 flash point (TDS typical 190 °C vs SDS bound >110 °C) and RICHFUL_RF6078 (the '
  'proposal states that the conflict note has the two files swapped; check against both PDFs).')
for fl in rep['review_flags']:
    w(f"- {prod(fl['file'])} `{fl['path']}`: printed '{fl['printed_text']}' with unit {fl['unit']}; the normalised "
      "density is out of range, so `value_final` is null and flagged. Check the printed unit.")
w('- PETRO_CANADA_PURITY_L65: the viscosity-index conflict is stored as text, so it carries no `resolved` key; the '
  'proposal on origin/main (keep the TDS value 92 over the brochure value 104) was not adopted.')
w('- Revise `integrate_products.py` (its override and conflict tables still average values and prefer TDS over SDS) and '
  'add rules for the conflict entries recorded on this branch before it is run again.')

with open(os.path.join(repo, 'open_questions_and_conflicts.md'), 'w', encoding='utf-8', newline='') as fh:
    fh.write(head.rstrip('\n') + '\n' + '\n'.join(L) + '\n')
print('written', len(L), 'lines appended')
