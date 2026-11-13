"""Thirteenth pass, batch 6: Infineum D3320 presentation DL2-13079.pdf ('© INFINEUM INTERNATIONAL LIMITED 2015'), read in full.
Writes decisions/zzzzzzzzzzzzz_b6_d3320_2015_thirteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = '(thirteenth pass, 2026-11-13)'
F_ = 'DL2-13079.pdf'
SCOPE = 'presentation pp.1-22 text layer read in full; p.7 formulations, p.8 claims set and p.10 typical inspections (image only, no text layer) viewed as images; pp.11, 14-17 charts not digitised'
o = "re-read manually: DL2-12025.pdf (Infineum D3320 data sheet, 2015-02-06) pp.1-2 typical inspections and performance table (thirteenth pass, 2026-11-13)"
links, F = [], []
links.append(dict(p='INFINEUM_D3320', f=F_, cat='E', status='completed', fields_status=f'{SCOPE} {T}',
                  coverage=(f"assessed by reading (2026-11-13, thirteenth pass) for {SCOPE}: Infineum D3320 presentation (2015). p.10 Typical Inspections (image) equal the cited data sheet and the JSON (BN 76, density 947, flash 189 D93, KV100 175, KV40 3829, sulfated ash 7.2, sulfur 1.5 D6443; 'Mineral Oil 48 %(m) Calculated' already in an open question). "
                            "p.7 'Final Formulations' IME1402170-D (10W-30) / IME1405260-A (10W-40) equal the columns proposed in the twelfth pass from DL2-13796.pdf p.11 (same ingredients, viscometrics and finished-oil inspections). "
                            "NEW: the 2015 claims set (p.8 = p.21) with approval status: ACEA E6-12, E7-12, API CI-4 in both grades; MB-Approval 228.51, MAN M 3477, Deutz DQC III-10 LA, Volvo VDS-3, Mack EO-N, Renault RLD-2, MTU Category 3.1 marked '* Verbally approved, formal paperwork being completed'; Cummins CES 20076/77 'Pending' ('** engine and bench tests completed – data being submitted'). "
                            "Also technology statements (p.12: salicylate detergent, TPP free, SV star VM; p.4: detergent system from Infineum D3336) -> historical-note and note rows. Engine-test charts (pp.14-17) carry no readable numbers and are not digitised."),
                  identity="exact: 'Infineum D3320' on every slide", note='Category E (supplier presentation of the same product, 2015).'))
for pid, txt in [('CHEVRON_GROUP_II_220R', "Chevron 220R %m 57.7 (IME1402170-D) / 53.1 (IME1405260-A) on p.7; p.12 'Over 50% of Chevron 220R Group II cut used in the formulation'"),
                 ('YUBASE_4', "YUBASE 4 %m 24.0 / 26.0 on p.7; p.12 'Group III (Yubase 4 cSt)'")]:
    links.append(dict(p=pid, f=F_, cat='D', status='completed', fields_status=f'whole presentation read (pp.1-22); p.7 viewed as an image {T}',
                      coverage=(f"assessed by reading (2026-11-13, thirteenth pass) for the whole presentation: the base oil appears only as a recipe share of the two D3320 formulations ({txt}). "
                                "No property of the base oil is printed; the recipe shares belong to the D3320 route (already proposed there) and are not base-oil properties. Nothing proposed for this record."),
                      identity='exact grade name in the formulation table', note="Recipe share in another product's document."))
F.append(dict(p='INFINEUM_D3320', tier=1, path='performance_claims', old="DL2-12025.pdf (2015-02-06) performance table: ACEA E6-12 / API CI-4 in 10W-30 and 10W-40 at 13.7 mass % (as recorded). The twelfth pass proposed the 2019 claim set (DL2-13796.pdf p.11).",
              new_f=F_, new_p=8,
              new_text="p.8 (= p.21) 'Infineum D3320 – Platform and Claims Set' (image): SAE 10W-30 and SAE 10W-40 both ●: ACEA E6-12, E7-12; API CI-4; MB '*MB-Approval 228.51'; MAN '*M 3477'; Deutz '*DQC III-10 LA'; Volvo '*VDS-3'; Mack '*EO-N'; Renault '*RLD-2'; MTU '*Category 3.1'; Cummins '**CES 20076/77' 'Pending' in both grades. Footnotes: '* Verbally approved, formal paperwork being completed'; '**Cummins engine and bench tests completed – data being submitted to Cummins'.",
              unit='as printed', form='claims set with approval status as printed (2015)', qual='as printed', method='', cond='per grade; status per footnote', basis='',
              outcome='additional', action='propose_historical_note',
              reason="A 2015 claim snapshot with explicit status: the OEM entries were only 'verbally approved' and Cummins was 'pending'. Propose a historical note dated 2015 keeping each status as printed; it is not merged with the 2019 claim set and does not upgrade any claim to approved.",
              old_rev=o, cmp_override='existing: ACEA E6-12, API CI-4 (2015 data sheet)'))
F.append(dict(p='INFINEUM_D3320', tier=1, path='open_questions', old='Not in the cited data sheet.', new_f=F_, new_p=12,
              new_text="p.12 'Features': 'Formulated with only two cuts of high quality base oil: Group III (Yubase 4 cSt) and Group II (Chevron 220R)'; 'Utilises proven Infineum SV star VM technology'; 'Contains salicylate detergent technology'; 'TPP free formulation'. p.4: 'Utilises detergent system from Infineum D3336, a global and universal top tier ACEA E6-12 / API CJ-4 approved formulation'. p.5: positioning 'PART SYNTHETIC Group II / III'. p.18: 'ACEA E6-12 data set is complete with passing results achieved in all engines' (OM 501 LA, OM 646 LA, Mack T-12).",
              unit='as printed', form='supplier technology and positioning statements (2015 presentation)', qual='as printed', method='', cond='', basis='',
              outcome='additional', action='propose_note',
              reason='Preserve the chemistry and test-programme statements with the source and date; they are supplier statements, not measured properties, and the base-oil pair belongs to the published formulations only.',
              old_rev=o, cmp_override='existing: not recorded'))
d = dict(batch='additive partial reviews, batch 6: Infineum D3320 2015 presentation (thirteenth pass)', reviewed_on='2026-11-13 (thirteenth pass)',
         note='DL2-13079.pdf read in full; layout-dependent slides viewed as images. Relationship links of Chevron 220R / Yubase 4 upgraded from first-hit review.',
         documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzz_b6_d3320_2015_thirteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
