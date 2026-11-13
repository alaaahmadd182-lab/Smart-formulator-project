"""Thirteenth pass, batch 5: Infineum D3511 presentation DL2-15388.pdf (2024; 'Last update: 01-Dec-2023'), read in full.
Writes decisions/zzzzzzzzzzzzz_b5_d3511_thirteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = '(thirteenth pass, 2026-11-13)'
F_ = 'DL2-15388.pdf'
SCOPE = 'presentation pp.1-9 text layer read in full; p.5 claims matrix and the p.6 and p.7 formulation tables viewed as images'
o = "re-read manually: DL2-15389.pdf (Infineum D3511 data sheet, Version: 20 September 2023 (2.0), 1 page) whole text (thirteenth pass, 2026-11-13)"
DOC = "Infineum D3511 presentation '© Infineum International Limited 2024', 'Last update: 01-Dec-2023', marked 'Infineum Confidential Information for use by Infineum customers and purchasers of Infineum products only'"
links, F = [], []
links.append(dict(p='INFINEUM_D3511', f=F_, cat='E', status='completed', fields_status=f'{SCOPE} {T}',
                  coverage=(f"assessed by reading (2026-11-13, thirteenth pass) for {SCOPE}: {DOC}. Compared with the JSON (from the 2023 data sheet DL2-15389.pdf): treat rate 13.2 m% and API CK-4 / FA-4 grade claims equal. "
                            "NEW and not recorded: OEM claims matrix with status column (Caterpillar ECF-3, Cummins CES 20081, Daimler DTFR 15C100 (ex. MB 228.31), Detroit Diesel DFS 93K218 = ✓; ACEA E7/E11-2022, MTU 2.1, Mack EOS-4, Renault RLD-3, Volvo VDS-4 = 'Targeted'); "
                            "base-stock coverage (Group II named stocks; Group III up to 30 % named stocks; '*30% Group III required to deliver claim in SAE 10W-40'); viscosity-modifier options (SV261 20 SSI, other SVs, V522 25 SSI, V534 35 SSI, other 25-35 SSI OCPs); "
                            "8 coded formulations (pp.6-7, EHC and Formosa) with HTHS150, KV100 and CCS. The JSON has permitted_base_oils_restrictions, required_co_components and published_formulations Missing. -> rows (all route-bound or claim-status labelled). No property of D3511 itself is printed."),
                  identity="exact: 'Infineum D3511' on every slide", note='Category E (supplier presentation of the same product).'))
for pid, share in [('EXXONMOBIL_EHC_110', "EHC 110 m% 7.1 / 11.9 / 32 / 3.0"), ('EXXONMOBIL_EHC_50', "EHC 50 m% 74 / 73 / 48.8 / 74.4")]:
    links.append(dict(p=pid, f=F_, cat='D', status='completed', fields_status=f'whole presentation read (pp.1-9) and p.6 viewed as an image {T}',
                      coverage=(f"assessed by reading (2026-11-13, thirteenth pass) for the whole presentation: the product appears only as a recipe share in the four Infineum D3511 EHC formulations on p.6 ({share} in IME2304689-A, IME2304692-A, IME2304684-A, IME2304305-A) and as 'ExxonMobil EHC' in the Group II coverage list (pp.3-4). "
                                "No property of the base oil is printed. Recipe shares belong to the D3511 route (recorded there) and are not base-oil properties; nothing proposed for this record."),
                      identity="exact grade name in the formulation table", note='Recipe share in another product\'s document.'))

ROWS = [
 ('performance_claims', 'propose_add_route_bound',
  "p.5 'PERFORMANCE CLAIMS' (viewed as image): columns SAE 10W-30 | SAE 10W-30 | SAE 10W-40* | SAE 15W-40 | Status. API CK-4: ● in 10W-30 (second column), 10W-40, 15W-40, ✓. API FA-4: ● in the first 10W-30 column only, ✓. ACEA E7/E11-2022: ●, ●*, ● Targeted. Caterpillar ECF-3 ✓; Cummins CES 20081 ✓; Daimler DTFR 15C100 (ex. MB 228.31) ●* in 10W-40, ✓; Detroit Diesel DFS 93K218 ●* in 10W-40, ✓; MTU Oil Category 2.1 ●* Targeted; Mack EOS-4, Renault RLD-3, Volvo VDS-4: Targeted. Footnote '*30% Group III required to deliver claim in SAE 10W-40'. 'Formal coverage for some claims require additional bench testing on a customer request basis'.",
  'claims matrix with per-claim status (✓ vs Targeted) and grade-specific footnote', 'per grade column; 10W-40 marks with * require 30 % Group III',
  "Propose adding the OEM claims with the printed status kept per claim: '✓' entries as supplier claims, 'Targeted' entries as targets only (not claims met). The 10W-40 asterisk condition (30 % Group III) is kept with each starred claim. The two 10W-30 columns are kept separate (FA-4 only in the first); the slide does not link these columns to the oil codes on pp.6-7, so no link is inferred."),
 ('permitted_base_oils_restrictions', 'propose_add_route_bound',
  "p.4 'Base stock coverage': 'Group II Capability to cover any Group II including, but not limited to: ExxonMobil EHC, Formosa, Hyundai Shell Bank, CNOOC, Chevron, AramcoPRIMA'; 'Group III Capability to include Group III including: ≤ 30% Yubase, ≤ 30% Shell, ≤ 30% AramcoULTRA, ≤ 30% Nexbase, ≤ 30% Petro-Canada, ≤ 30% BAPCO, ≤ 30% ADNOC'; '*30% Group III may be required to deliver certain claims in specific SAE grades'. p.3: 'Additional base stock coverage is subject to compliance with Base Oil Interchange guidelines.' 'Speak to your Infineum contact to confirm exact base stock and viscosity modifier coverage'.",
  'supplier coverage statement (capability; confirm with supplier)', 'Group II named stocks; Group III up to 30 % of named stocks; BOI guidelines',
  "Fills a Missing field with supplier-printed coverage, kept as printed: Group II named stocks ('including, but not limited to'), Group III limited to ≤ 30 % of the named stocks, BOI compliance for others, and the 'confirm with your Infineum contact' qualifier. Not generalised to all Group II/III base oils."),
 ('required_co_components', 'propose_add_route_bound',
  "p.4 'Viscosity modifier options: Infineum SV261 – 20 SSI; Other Infineum SVs; Infineum V522 – 25 SSI; Infineum V534 – 35 SSI; Other 25 – 35 SSI OCPs'. Formulations pp.6-7: 'Infineum V385, m% 0.3' in all eight; 'Infineum V522, m%' 1.6-9.5.",
  'VM options (supplier list) and the VM / PPD used in the published formulations', 'route-bound: options list p.4; doses only within the coded formulations pp.6-7',
  "Propose a route-bound entry: the VM is an option from the printed list (SSI as printed), not a single required component; V385 (0.3 m%) and V522 appear in the published formulations only. Recipe ingredients are not universal co-components."),
 ('published_formulations', 'propose_add_route_bound',
  "p.6 (image) 'Typical formulations and properties – ExxonMobil EHC': IME2304689-A SAE 10W-30: D3511 13.2, V385 0.3, V522 5.4, EHC 110 7.1, EHC 50 74, Total 100; HTHS150 3.5 cP, KV100 12.0 cSt, CCS at grade 6395. IME2304692-A SAE 10W-30: 13.2, 0.3, 1.6, 11.9, 73, 100; 3.0, 9.5, 6447. IME2304684-A SAE 15W-40: 13.2, 0.3, 5.7, 32, 48.8, 100; 4.0, 14.4, 6064. IME2304305-A SAE 10W-40: 13.2, 0.3, 9.1, 3.0, 74.4, 100; 4.0, 14.9, 6503. p.7 'Formosa': IME2304690-A 10W-30: 13.2, 0.3, V522 6.0, Formosa 150N 78, Formosa 500N 2.5, 100; 3.5, 12.2, 6218. IME2304693-A 10W-30: 13.2, 0.3, 2.3, 76.7, 7.5, 100; 3.0, 9.8, 6196. IME2304685-A 15W-40: 13.2, 0.3, 5.6, 46.2, 34.7, 100; 4.1, 14.6, 6372. IME2304227-A 10W-40: 13.2, 0.3, 9.5, 77, '-', 100; 4.1, 15.1, 6487.",
  'typical formulations (supplier-labelled) with finished-oil properties', 'per coded formulation column; m% (mass %); CCS temperature printed only as "at grade"',
  "Propose eight route-bound formulations identified by oil code, base stock and grade, ingredients in m% as printed and the printed Total 100 (reviewer check: each column's printed shares sum to 100.0). Finished-oil HTHS150 / KV100 / CCS belong to each formulation, not to D3511; the CCS temperature is printed only as 'at grade'. No claim column is attached to any oil code."),
]
for path, act, text, form, cond, reason in ROWS:
    F.append(dict(p='INFINEUM_D3511', tier=1, path=path, old='DL2-15389.pdf (2023 data sheet) prints only the CK-4 / FA-4 performance table, typical inspections and handling text; this field is Missing or holds only the API claims.',
                  new_f=F_, new_p=5 if path == 'performance_claims' else (4 if path in ('permitted_base_oils_restrictions', 'required_co_components') else 6),
                  new_text=text, unit='as printed', form=form, qual='as printed', method='', cond=cond, basis='m% (mass %)' if path == 'published_formulations' else '',
                  outcome='additional', action=act, reason=reason, old_rev=o, cmp_override='existing: Missing' if path != 'performance_claims' else 'existing: API CK-4, API FA-4 only'))
F.append(dict(p='INFINEUM_D3511', tier=1, path='open_questions', old='Not in the cited data sheet.', new_f=F_, new_p=2,
              new_text="p.2: 'Lowest treat rate on the market'; 'Key OEM approvals Including DTFR 15C100, Cummins CES 20081'; 'Global supply from regional sites'. p.9: 'Last update: 01-Dec-2023'; confidentiality and single-copy permission notice.",
              unit='as printed', form='supplier marketing statements and document notices', qual='as printed', method='', cond='', basis='',
              outcome='additional', action='propose_note', reason="Preserve the dating ('Last update: 01-Dec-2023' vs the data sheet's 20 September 2023) and the confidentiality notice with the source; marketing statements are recorded as supplier statements, not claims.",
              old_rev=o, cmp_override='existing: not recorded'))
d = dict(batch='additive partial reviews, batch 5: Infineum D3511 presentation (thirteenth pass)', reviewed_on='2026-11-13 (thirteenth pass)',
         note='DL2-15388.pdf read in full; claims matrix and formulation table viewed as images. Relationship links of EHC 110 / EHC 50 upgraded from first-hit review.',
         documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzz_b5_d3511_thirteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
