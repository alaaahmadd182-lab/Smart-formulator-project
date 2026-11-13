"""Eighteenth pass, batch 28: duplicate (category A) coverage of BRB Petrolad 8099 (3 pp.), the Bettchem 'Technical Judgement for
BT 3088' (4 pp.) and the distributor SDS 'Yubase_6-SDS.pdf' (6 pp., Hilditch Pty Ltd), each read in full (text layer; the Petrolad
performance table also viewed as an image). Writes decisions/zzzzzzzzzzzzzzzzzz_b28_dup_brb_bt3088tj_yubase6sds_eighteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'eighteenth pass, 2026-11-14'
SDSU = 'SDS reported value; statistical basis unspecified (distributor SDS section 9: "Typical values only - consult specification sheet")'
links, F = [], []


def link(pid, f, n, ed, cov, ident='SHA-256 equal to the cited source; product name on every page'):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'pp.1-{n} read in full (all {n} pages; text layer) ({T})',
                      coverage=f'assessed by reading (2026-11-14, eighteenth pass) for the whole document ({n} pp., {ed}): {cov}', identity=ident, note='Byte duplicate of a cited or registered source.'))


link('BRB_PETROLAD_8099', 'DL2-11053.pdf', 3, 'Issue date: May 31, 2016',
     "the 15 performance rows at 11.2 % wt (the two Cummins lines share one 11.2 cell on the image, as recorded), the claim types, the optional 'Viscotech 6540 VI improver' (existing open question: optional, not required) and the typicals (density 15.6 °C 0.99 kg/L, flash '>170', KV100 110, Ca 3.22, P 0.99, N 0.58, Zn 1.10, TBN 87) equal the record. No new row.")
link('BETTCHEM_BT_3088', 'DL2-15578.pdf', 4, 'Version 1.0/ME, Date: 12/3/2025',
     "'Technical Judgement for BT 3088': API CI-4 at 8 %, API CH-4 at 7 % and API SL at 8 %, each engine test with 'Passing results are predicted' / 'A pass is predicted'. The record already holds these three claims (cited to DL2-15620.pdf) as claim_type 'other' with evidence class 'Predicted' and the note that they are predictions; nothing in this copy changes that. No new row; the claims stay predictions, not test results.")
Y = "Safety Data Sheet 'Yubase 6', Reference No HIL0045, Version 5.0, Issued 2021-09-28, supplier Hilditch Pty Ltd (Australian distributor)"
O = f're-read manually: Yubase_6-SDS.pdf ({Y}) pp.1-6 whole text ({T})'
link('YUBASE_6', 'Yubase_6-SDS.pdf', 6, Y,
     "section 3 ('Distillates, petroleum, hydrotreated heavy paraffinic 64742-54-7 100 % (w/w)'; 'DMSO extract (IP 346) <3 %') is the record's chemistry source (registered URL). Section 9 ('Typical values only - consult specification sheet') prints Specific Gravity 0.825 (no temperature), Flash Point (°C) 220 (no method) and Viscosity 6.5 cSt @ 100 °C; none is recorded -> SDS alternate-entry rows (KV100; flash 220 with the SDS method not printed, so not called a conflict) and an open-question row (SG).",
     ident="SHA-256 equal to the registered external source '.../search_api/Yubase_6-SDS.pdf' (the record's chemistry source); 'Product Name: Yubase 6' on every page")
F.append(dict(p='YUBASE_6', tier=1, path='kv100', old='Record kv100 6.52 cSt (DL2-11306.pdf, NARMAK TRADE distributor sheet).', new_f='Yubase_6-SDS.pdf', new_p=3,
              new_text="'Viscosity: 6.5 cSt @ 100 °C' ('Typical values only - consult specification sheet')", unit='cSt', form=SDSU, qual='SDS reported value', method='not printed', cond='', basis='',
              outcome='additional', action='propose_alternate_entry',
              reason='SDS section 9 value never recorded. Propose an alternate entry in the SDS class; the record keeps its value. 6.5 and 6.52 are not compared under any threshold (the proposed thresholds are not approved).',
              old_rev=O, cmp_override='existing: kv100 6.52 only'))
F.append(dict(p='YUBASE_6', tier=2, path='flash_point', old='Record flash_point 240 °C (DL2-11306.pdf, ASTM D92).', new_f='Yubase_6-SDS.pdf', new_p=3,
              new_text="'Flash Point (°C): 220' (no method; 'Typical values only - consult specification sheet')", unit='°C', form=SDSU, qual='SDS reported value', method='not printed', cond='', basis='',
              outcome='additional', action='propose_alternate_entry',
              reason="Comparability checked (nineteenth pass): same property and unit (flash point, °C) and grade name; the METHOD of the SDS value is not printed (the property sheet prints ASTM D92, open cup), the editions differ (SDS 2021-09-28; NARMAK sheet undated) and the value classes differ (SDS 'Typical values only'; property sheet single 'VALUE' column). Because the SDS method is unknown, 220 vs 240 cannot be called a direct conflict. Propose keeping the SDS value as an alternate entry in the SDS class, with the missing method stated, and keeping the question open (which method the SDS used); the record keeps 240, nothing is averaged, and no method is assumed. (First proposed as a conflict entry in the eighteenth pass; revised here.)",
              old_rev=O, cmp_override='existing: flash_point 240'))
F.append(dict(p='YUBASE_6', tier=1, path='open_questions', old='Record density Missing (mandatory Tier 1); the record has no specific-gravity entry.', new_f='Yubase_6-SDS.pdf', new_p=3,
              new_text="'Specific Gravity: 0.825' (no temperature; 'Typical values only - consult specification sheet')", unit='dimensionless (as printed)', form=SDSU, qual='SDS reported value', method='not printed', cond='', basis='',
              outcome='additional', action='propose_open_question_update',
              reason="A specific gravity without a reference temperature, from a distributor SDS, is not a density and is not used to fill the mandatory density. It also differs from the NARMAK sheet's 'Specific gravity at 15 °C g/m3 0,8423' (itself an open question for its label and unit). Propose listing both in the density open question for SK; nothing is converted.",
              old_rev=O, cmp_override='existing: density Missing'))

d = dict(batch='duplicate coverage, batch 28: BRB 8099, BT 3088 technical judgement, YUBASE 6 distributor SDS (eighteenth pass)', reviewed_on='2026-11-14 (eighteenth pass)',
         note='Three byte-duplicate links, each read in full with the record beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzz_b28_dup_brb_bt3088tj_yubase6sds_eighteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
