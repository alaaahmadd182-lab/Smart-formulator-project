"""Thirteenth pass, batch 7: Infineum D3503 presentation DL2-15685.pdf ('© Infineum International Limited 2023', 'Last update: 3/2023'),
read in full. Writes decisions/zzzzzzzzzzzzz_b7_d3503_thirteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = '(thirteenth pass, 2026-11-13)'
F_ = 'DL2-15685.pdf'
SCOPE = ('presentation pp.1-39 text layer read in full; pp.4, 5, 6 (claims) and pp.30, 31, 32 (formulation tables, whose text layer is scrambled) viewed as images; '
         'field-test and engine-test charts (pp.16-26, 35-38) read as text only, numbers on chart axes not digitised')
o = "re-read manually: DL2-11404.pdf (Infineum D3503 data sheet, Version 25 May 2016 (3.0), 2 pages) whole text (twelfth pass, documented in decisions/zzzzzzzzzzzz_corrections_twelfth_pass.json)"
links, F = [], []
links.append(dict(p='INFINEUM_D3503', f=F_, cat='E', status='completed', fields_status=f'{SCOPE} {T}',
                  coverage=(f"assessed by reading (2026-11-13, thirteenth pass) for {SCOPE}: Infineum D3503 presentation 2023 ('Last update: 3/2023'). The JSON (from the 2016 data sheet) holds API CK-4 / FA-4 at 14.5 % and the package typicals. "
                            "NEW, not recorded: (a) CK-4 claims matrix p.5 and FA-4 matrix p.6 (images) with grade marks, '−' and '(2) Meets engine test requirements' for JASO DH-2, footnotes and the CK-4 / FA-4 mutual-exclusivity note; (b) monograde treat rates p.7; "
                            "(c) base stock and VM coverage p.8; (d) ten typical formulations pp.30-32 (images) incl. three printed anomalies kept as printed; (e) finished-oil element levels at 14.5 % m p.4 (not package contents). "
                            "OEM specification and drain-interval tables (pp.10-11) are third-party OEM information, preserved in a note, not D3503 claims. -> rows."),
                  identity="exact: 'Infineum D3503' on the slides", note='Category E (supplier presentation of the same product, 2023).'))
for pid, txt in [('EXXONMOBIL_EHC_50', "EHC 50 (Group II) mass % 52.8 / 47.8 / 76.4 / 29.8 in the p.30 formulations"),
                 ('EXXONMOBIL_EHC_120', "EHC 120 (Group II) mass % 26.0 / 18.2 / 6.6 / 17.0 in the p.30 formulations"),
                 ('YUBASE_4', "Yubase 4 (Group III) mass % 15.0 / 30.0 (p.30) and 15.0 / 30.0 (p.31); '30% Yubase' Group III coverage p.8")]:
    links.append(dict(p=pid, f=F_, cat='D', status='completed', fields_status=f'whole presentation read (pp.1-39); pp.30-31 viewed as images {T}',
                      coverage=(f"assessed by reading (2026-11-13, thirteenth pass) for the whole presentation: the base oil appears only as a recipe share of D3503 formulations ({txt}). "
                                "No property of the base oil is printed; recipe shares belong to the D3503 route and are not base-oil properties. Nothing proposed for this record."),
                      identity='exact grade name in the formulation tables', note="Recipe share in another product's document."))


def add(path, act, page, text, form, cond, reason, cur='existing: Missing', basis='', outcome='additional'):
    F.append(dict(p='INFINEUM_D3503', tier=1, path=path, old='DL2-11404.pdf (2016 data sheet, cited) prints the CK-4 / FA-4 performance table (14.5 %), typical inspections and handling data only; this item is not in it.',
                  new_f=F_, new_p=page, new_text=text, unit='as printed', form=form, qual='as printed', method='', cond=cond, basis=basis,
                  outcome=outcome, action=act, reason=reason, old_rev=o, cmp_override=cur))


add('performance_claims', 'propose_add_route_bound', 5,
    "p.5 'API CK-4 and Additional Performance Claims' (image), columns SAE 15W-40 | 10W-40 | 10W-30: API CK-4, CJ-4, CI-4 PLUS, CI-4, CH-4 ✓✓✓; API(1) SN, SM, SL, SJ ✓ ✓ −; ACEA E11-2022, E7-2022 ✓✓✓; Mack EOS-4.5, EO-O Premium Plus, EO-N ✓✓✓; Volvo VDS-4.5, VDS-4, VDS-3 ✓✓✓; Caterpillar ECF-3, ECF-2 ✓✓✓; Cummins CES 20086, CES 20081 ✓✓✓; Detroit Diesel DFS 93K222, DFS 93K218 ✓✓✓; Daimler MB 228.31 ✓✓✓; Ford WSS M2C171-F1 ✓✓✓; MAN M3775 ✓✓✓; MTU Category 2.1 ✓✓✓; Deutz DQC III-18 LA ✓✓✓; Allison TES 439 ✓ − −; JASO DH-2 (2)(2)(2); Renault RLD-4, RLD-3 ✓✓✓. Footnotes '(1) API S claims for ILSAC viscosity grades must follow phosphorus content requirements of the API S category', '(2) Meets engine test requirements'. p.6 (image) SAE 10W-30: API FA-4 ✓; API(1) SN, SM, SL, SJ '-'; Cummins CES 20087 ✓; Detroit Diesel DFS 93K223 ✓. Notes: 'SAE 10W-30 API FA-4 claims and corresponding OEM claims are mutually exclusive with API CK-4 claims and their corresponding OEM specs'; 'Several OEMs do not allow the use of API FA-4 engine oils'; 'Specific formulations may need additional bench testing for formal claims'.",
    'claims matrix per grade as printed (2023)', "per grade; '−' = not claimed; JASO DH-2 only 'meets engine test requirements'; FA-4 and CK-4 claims mutually exclusive",
    "Propose adding the 2023 claims per grade exactly as marked, keeping '−' cells unclaimed, JASO DH-2 as engine-test-only, the API S phosphorus footnote, and the FA-4 / CK-4 mutual-exclusivity condition. The 2016 data sheet claims stay as recorded (no merge by date).",
    cur='existing: API CK-4, API FA-4 only')
add('treat_rate_matrix', 'propose_add_route_bound', 7,
    "p.7 'Monograde Recommendations': 'API CF/CF-2/SG | 30, 40, 50 | 10.2% mass | 9.3% volume'; 'API CF/SG | 10W | 10.2% | 9.3%'. Notes: 'Monograde recommendations are provided as a suitable logistic option if a more cost-effective option is not available'; 'Monogrades normally do not carry any licensable claims'; 'Infineum recommends against using a monograde and a higher phosphorus product in a modern gasoline engine'. p.4: '@ 14.5 % m (~13.3 % vol)'.",
    'supplier treat-rate recommendation (mass % and volume % as printed)', 'monogrades only; logistic option; no licensable claims',
    "Propose route-bound monograde treat rates (10.2 mass % / 9.3 volume %) with their printed caveats; volume % is kept separately from mass %. The 14.5 % multigrade rate is already recorded.",
    cur='existing: 14.5 % CK-4 / FA-4 multigrade rows', basis='mass % and volume % as printed')
add('permitted_base_oils_restrictions', 'propose_add_route_bound', 8,
    "p.8 'Base Stock Coverage': 'Group II Calumet Heartland, Chevron, Crystal Clean, Excel, Safety-Kleen, aramcoPRIMA, Petro-Canada, EHC'; 'Group III 30% Yubase, 30% aramcoULTRA P, 30% Neste, 30% aramcoULTRA U, 30% Petro-Canada, 30% ADNOC'; 'Additional basestock and VM coverage may be possible. Contact your Infineum representative'. p.3: 'Extensive basestock and viscosity modifier coverage in SAE 15W-40, 10W-40, and 10W-30'.",
    'supplier coverage statement (named stocks)', 'Group II named stocks; Group III at 30 % of named stocks',
    'Fills a Missing field with the named coverage as printed (not generalised to all Group II / III); the 30 % Group III figures are kept per named stock.')
add('required_co_components', 'propose_add_route_bound', 8,
    "p.8 'Viscosity Modifier Options': 'Infineum SV260 (solid) / SV261, SV261L (liquid) – 20 SSI'; 'Infineum SV200 (solid) / SV 203, SV201 (liquid) – 5 SSI'. Formulations pp.30-32: Infineum V385 0.2 mass % in all ten; SV261L, SV261 or SV201 as VM.",
    'VM options (supplier list) and the VM / PPD of the published formulations', 'route-bound: VM is one option from the list; doses only within the coded formulations',
    'Propose a route-bound VM-options entry (SSI as printed) and V385 as the PPD used in the published formulations only; not universal co-components.')
add('published_formulations', 'propose_add_route_bound', 30,
    "Typical Formulations (images; mass % and volume % columns): p.30 'ExxonMobil EHC/Yubase, Infineum SV261L': 15W-40 CK-4 mass D3503 14.5 / V385 0.2 / SV261L 6.5 / EHC 50 52.8 / EHC 120 26.0 / Yubase 4 - / TOTAL 100.0, volume 13.2 / 6.8 / 0.2 / 53.9 / 25.9 / - / 100.0; 10W-30 CK-4 mass 14.5 / 0.2 / 4.3 / 47.8 / 18.2 / 15.0 / 100.0, volume 13.1 / 0.2 / 4.4 / 48.6 / 18.1 / 15.6 / 100.0; 10W-30 FA-4 mass 14.5 / 0.2 / 2.3 / 76.4 / 6.6 / - / 100.0, volume 13.1 / 0.2 / 2.4 / 77.7 / 6.6 / - / 100.0; 10W-40 CK-4 mass 14.5 / 0.2 / 8.5 / 29.8 / 17.0 / 30.0, volume 13.1 / 0.2 / 8.7 / 30.1 / 16.8 / 31.1, TOTAL cells blank; KV100 16.1 / 12.1 / 9.8 / 15.6 cSt; HTHS150 4.2 / 3.5 / 3.0 / 4.0 cP; Noack 9 / 10 / 12 / 10 %wt; 'CCS @Temp.°C, cP' 4899 / 6044 / 5448 / 5139. "
    "p.31 'Chevron RLOP / Yubase, Infineum SV261L' (all CK-4): 15W-40 mass 14.5 / 0.2 / 6.5 / CHEV100R - / CHEV220R 78.8 / Yubase 4 - / 100.0 (volume 13.4 / 0.2 / 6.8 / - / 79.6 / - / 100.0); 10W-30 14.5 / 0.2 / 4.7 / 5.0 / 60.6 / 15.0 / 100.0 (13.2 / 0.2 / 4.9 / 5.1 / 60.8 / 15.8 / 100.0); 10W-40 14.5 / 0.2 / 9.0 / 3.0 / 43.3 / 30.0 / 100.0 (13.1 / 0.2 / 9.3 / 3.0 / 43.1 / 31.3 / 100.0); KV100 15.7 / 12.2 / 15.9; HTHS 4.1 / 3.5 / 4.0; Noack 10 / 10 / 11; CCS 5191 / 6528 / 4866. "
    "p.32 'Sinopec, Infineum SV261/SV201': 15W-40 CK-4 mass 14.5 / V385 0.2 / SV261 6.5 / SV201 - / Sinopec HVI II 6 68.8 / HVI II 10 10.0 / 100.0 (volume 13.1 / 0.2 / 6.5 / - / 70.2 / 10.0 / 100.0); 10W-30 CK-4 14.5 / 0.2 / - / 4.3 / 81.0 / - / 100.0 (13.0 / 0.2 / - / 4.3 / 82.5 / - / 100.0); 10W-30 FA-4 14.5 / 0.2 / 2.0 / - / 83.3 / - / 100.0 (13.0 / 0.2 / 2.0 / - / 84.8 / - / 100.0); KV100 15.0 / 12.3 / 9.9; HTHS150 '43.9' / 3.5 / 3.1 cP; Noack 9 / 9 / 10; CCS 4055 / 6141 / 5679.",
    'typical formulations (supplier-labelled) with finished-oil properties; mass % and volume % columns', 'per grade / API category column and base-stock set; CCS temperature printed only as "@Temp."',
    "Propose ten route-bound formulations identified by base-stock set, grade and API category (no oil codes printed), with mass % and volume % kept separately. Reviewer check: every printed mass % and volume % column sums to 100.0. Three printed anomalies are kept AS PRINTED and flagged, not corrected: p.30 15W-40 volume % column prints V385 6.8 and SV261L 0.2 (the same rows print mass % 0.2 and 6.5); no corrected figure is inferred; p.30 10W-40 TOTAL cells are blank; p.32 15W-40 HTHS150 is printed '43.9' cP (no corrected figure is inferred). Finished-oil properties belong to each formulation, not to D3503.",
    basis='mass % (and volume % as printed)')
add('open_questions', 'propose_note', 4,
    "p.4 'Product Attributes' (image): 'Oil Parameter | Infineum D3503 @ 14.5 % m (~13.3 % vol)': Calcium 1050 ppm, Magnesium 1000 ppm, Molybdenum 66 ppm, Nitrogen 1050 ppm, Phosphorus 1150 ppm, Zinc 1270 ppm, Total Base Number (D4739) 8.5, Total Base Number (D2896) 10.",
    'finished-oil contribution at the stated treat rate (not package contents)', 'at 14.5 % m (~13.3 % vol) in finished oil',
    "These are finished-oil levels contributed at 14.5 % m. They are NOT package element contents and must not be back-calculated into the package Ca / Mg / Mo fields (the JSON Ca stays Missing). Propose a note preserving them with the treat-rate condition.",
    cur='existing: package typicals from the 2016 data sheet; Ca Missing')
add('open_questions', 'propose_note', 10,
    "pp.10-11 OEM specification summary (Cummins CES 20086 / 20087, Detroit DFS 93K222 / 93K223, Mack EOS-4.5 / EOS-5, Volvo VDS-4.5 / VDS-5 (5W-30), Caterpillar, Navistar, PACCAR, GM Duramax, Ford WSS M2C171-F1; factory-fill grades) and OEM drain-interval summary ('Refer to OEM service literature for official oil drain details'). p.34: '27 million highway miles' of field testing. p.39: 'Last update: 3/2023'.",
    'third-party OEM information and supplier field-test statements', 'not D3503 claims',
    'Preserve as context attributed to the presentation; OEM drain intervals and specification grades are OEM information, not properties or claims of D3503; field-test chart values are not digitised.',
    cur='existing: not recorded')
d = dict(batch='additive partial reviews, batch 7: Infineum D3503 2023 presentation (thirteenth pass)', reviewed_on='2026-11-13 (thirteenth pass)',
         note='DL2-15685.pdf read in full; claims and formulation slides viewed as images. Relationship links of EHC 50 / EHC 120 / Yubase 4 upgraded from first-hit review.',
         documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzz_b7_d3503_thirteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
