"""Seventeenth pass, batch 24: duplicate (category A) coverage of six two-page Afton HDEO bulletins (HiTEC 12200, 12208, 12210,
12210M, 12360, 12400), each read in full (text layer) with its record, including the claim list, booster / VM rows and typicals.
Writes decisions/zzzzzzzzzzzzzzzzz_b24_dup_afton_bulletins_seventeenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'seventeenth pass, 2026-11-14'
links, F = [], []
NOTE = 'Old-source items without a template field, preserved as printed; nothing is mapped to a field.'
PPD = "The PPD sentence ('already contains a pour point depressant (PPD) so no supplemental PPD should be needed to meet low temperature properties') is already a reviewed statement in tools/mandatory_properties/co_component_statements.json (Part A), with its qualification 'should be needed' kept; no new row."


def link(pid, f, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'pp.1-2 read in full (all 2 pages; text layer) ({T})', coverage=f'assessed by reading (2026-11-14, seventeenth pass) for the whole bulletin (2 pp., {ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file; product name on both pages', note='Byte duplicate of the cited bulletin.'))


def row(pid, f, ed, old, reason=NOTE, path='open_questions', action='propose_note', outcome='in_old_source_not_captured', form='bulletin statements as printed (no template field)', new_text='(same file; byte duplicate in the new archive)', cmp='existing: not recorded', tier=1):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=2, new_text=new_text, unit='as printed', form=form, qual='as printed', method='as printed', cond='', basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=f're-read manually: {f} ({ed}) pp.1-2 whole text ({T})', cmp_override=cmp))


link('AFTON_HITEC_12200', 'DL2-14639.pdf', '08/18', "the 'Approvals' table (32 claims, incl. the footnote-5 'Meets requirements of' columns MB 228.1, MB 229.1 and MAN 3275 recorded as 'meets'), the 17 treat-rate rows with base-oil group and SAE grade, the booster doses (HiTEC 12250 4.2, 12260 0.9, 12255 5.0, 9552 0.35 / 0.6) and the typicals (density 0.989 g/ml, flash PMCC 135 min, KV40 4100, KV100 190, TBN 103) equal the record; the edition differences with 05/18 are existing conflicts. Not recorded: handling, the field-test sentence -> note.")
row('AFTON_HITEC_12200', 'DL2-14639.pdf', '08/18', "DL2-14639.pdf p.2 prints (not recorded): 'Handling Information Max Handling Temp: 70˚C Shelf Life: 24 months at ambient temperature'; 'HiTEC® 12200 has been field tested to 50,000km and was still performing strongly.'; bar charts vs 'API CI-4 Limit' (Mack T-12, Cat 1K, Seq IIIF, T8E) without values for a named formulation.")
link('AFTON_HITEC_12208', 'DL2-15364.pdf', '04/23', "claims (API CK-4, API FA-4, Cummins CES 20081, CES 20086 under 'Approvals', 13.7 % wt in SAE 10W-30 GP II, 10W-40 GP II/III, 15W-40 GP II) and typicals (density 0.9572 g/ml, flash PMCC 135 min, KV100 110 cSt, TBN 62) equal the record. Not recorded: appearance, handling, the FA-4 HTHS sentence -> note.")
row('AFTON_HITEC_12208', 'DL2-15364.pdf', '04/23', "DL2-15364.pdf p.2 prints (not recorded): 'Appearance Dark brown viscous liquid'; 'Recommended Handling and Storage Temperature: 40-45°C Maximum Handling Temperature (<24 hours): 70°C Shelf Life: 12 months at ambient temperature'; 'HiTEC® 12208 can also be formulated into API FA-4 lubricant with a high temperature high shear (HTHS) range of 2.9 - 3.2 cP'; 'It can also meet Cummins approvals. Please contact your Afton Chemical representative for specific recommendations.'",
    NOTE + ' The HTHS range is a property of the finished FA-4 oil, not of the package.')
link('AFTON_HITEC_12210', 'DL2-11418.pdf', '05/16', "claims (API CK-4 15W-40 / 10W-30, FA-4 10W-30, ACEA E9 self-certifying, backward CJ-4 / CI-4+ / CI-4 / CH-4, OEM list), 18.0 % wt, the VM 'HiTEC® 5748A' named without a dose, and the typicals (7.90 lbs/gal, SG 0.948, KV100 108, flash PMCC 135 min, TBN 55) equal the record. " + PPD + " Not recorded: appearance, handling -> note.")
row('AFTON_HITEC_12210', 'DL2-11418.pdf', '05/16', "DL2-11418.pdf p.2 prints (not recorded): 'Appearance Dark brown viscous liquid'; 'Max Handling Temp: 70°C Shelf Life: 3 months @ 45°C 36 months @ ambient (10-40°C)'.")
link('AFTON_HITEC_12210M', 'DL2-15568.pdf', '04/22', "the 21 claim entries ('API SN' is printed twice in the table and recorded once), 18.0 % wt, the VM statement 'HiTEC® 5748A or HiTEC® 5748' (no dose) and the typicals equal the record; the 05/18 edition differences are existing open questions. " + PPD + " Not recorded: handling and the claims caveat -> note.")
row('AFTON_HITEC_12210M', 'DL2-15568.pdf', '04/22', "DL2-15568.pdf p.2 prints (not recorded): 'Max Handling Temp: 70°C Shelf Life: 3 months @ 45°C, 36 months @ ambient (10-40°C)'; 'Approvals/Claims are speciﬁc for each formulation. Any change in the base oil/additive percentage could aﬀect the accuracy of these approvals/claims. Contact Afton's customer technical service for further information.'",
    NOTE + ' The caveat limits every recorded claim to the formulation behind it.')
link('AFTON_HITEC_12360', 'DL2-13692.pdf', '07/20', "the 15 claims (MAN 3677 and Scania LDF-4 '* Approvals pending' recorded as 'other'), 16.1 % in SAE 15W-40 GP II / 10W-40 GP II/III / 5W-30 GP III, the VM 'HiTEC® 5748 25SSI' (already in the HiTEC 5748 SSI open question) and the typicals (0.951 g/ml, flash PMCC 150, KV100 133, TBN 61) equal the record. The sentence 'HiTEC® 12360 contains 1% ash content' while sulfated_ash is Missing -> open-question row. Not recorded: handling -> note.")
row('AFTON_HITEC_12360', 'DL2-13692.pdf', '07/20', "DL2-13692.pdf p.2 prints (not recorded): 'Max Handling Temp: 70˚C Shelf Life: 24 months at ambient temperature'; drain-interval example '*Source: Kline **Based on average drain interval of 100k KM for MB 228.31 and 150K KM for MB 228.51'.")
row('AFTON_HITEC_12360', 'DL2-13692.pdf', '07/20', "Record sulfated_ash Missing (tier 2). DL2-13692.pdf p.2: '• Assists in emission reductions HiTEC® 12360 contains 1% ash content so it is compatible with after treatment devices fitted to today's modern trucks'.",
    "The sentence gives '1% ash content' without a method, without 'sulfated', and without saying whether it describes the package or the finished oil at 16.1 % (the context, after-treatment compatibility, suggests the finished oil). It is not used to fill the package's sulfated ash. Propose an open question quoting it.",
    action='propose_open_question_update', outcome='additional', form='marketing statement of an ash level (basis not stated)', new_text="'HiTEC® 12360 contains 1% ash content so it is compatible with after treatment devices'", cmp='existing: sulfated_ash Missing')
link('AFTON_HITEC_12400', 'DL2-15365.pdf', '06/21', "the claim matrix (22 symbol columns, 21 header labels and the unlabelled column 22 as recorded; ACEA E4 rows with '+ HiTEC® 611'), 16.1 % wt and the typicals (0.951 g/ml, flash PMCC 150, KV100 133, TBN 61; the same figures as the HiTEC 12360 bulletin, as printed) equal the record; the OCP VM is mentioned without a name ('OCP viscosity modifier allowing efficiency across Engine Oils portfolio'), as recorded. Not recorded: handling, the fuel-economy chart -> note.")
row('AFTON_HITEC_12400', 'DL2-15365.pdf', '06/21', "DL2-15365.pdf p.2 prints (not recorded): 'Max Handling Temp: 70°C Shelf Life: 24 months at ambient temperature'; 'OM501LA Fuel Economy, % 19 % better' vs 'MB228.51 Limits'; '- Choice of Group lll coverage allowing for base oil flexibility'; '- Booster approach to cover full SAPS extended drain products'; 'Pending completion of Field Trial, * Scania LDF-4 and MAN M3677 OEM approvals require Field Trial Approval pending'.",
    NOTE + " 'Choice of Group lll coverage' names no specific base oil and is not a base-oil restriction.")

d = dict(batch='duplicate coverage, batch 24: Afton HDEO bulletins (seventeenth pass)', reviewed_on='2026-11-14 (seventeenth pass)',
         note='Six byte-duplicate links; each two-page bulletin read in full with the record (claims, boosters, VM, typicals) beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzz_b24_dup_afton_bulletins_seventeenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
