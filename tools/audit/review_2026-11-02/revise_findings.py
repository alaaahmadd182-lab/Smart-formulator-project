"""Version 5 (revision of 2026-11-02): reporting corrections to the comprehensive conflicts audit.

Reads the structured findings of the 2026-10-30 snapshot (version 4,
tools/audit/original_2026-10-27_to_30/intermediate/findings_v4.json), applies the reviewed changes declared in
CHANGES below and writes:
    tools/audit/review_2026-11-02/output/findings_v5.json   the revised structured findings
    docs/audit_review_2026-11-02/finding_changes.csv        one row per changed field: before, after, reason, evidence

Every change states the exact text it replaces; the script stops if a "before" value does not match, so a change can
never be applied to a finding it was not reviewed against. No product data is read or written. IDs are unchanged and
no finding is added or removed.

Usage: python tools/audit/review_2026-11-02/revise_findings.py
"""
import copy, csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import review_lib as R

OUT_JSON = os.path.join(R.HERE, 'output', 'findings_v5.json')
OUT_LOG = os.path.join(R.ROOT, 'docs', 'audit_review_2026-11-02', 'finding_changes.csv')
POT = R.POT
SR = 'source_reading_log.csv'

# ---------------------------------------------------------------- recurring texts
ED_NEXT_OLD = 'Confirm with the supplier which edition is current; keep both editions documented.'
ED_NEXT_NEW = ('Apply the documented edition-selection rule to choose the working value; keep both editions documented. '
               'Supplier contact is optional (only to confirm that the older value is obsolete).')
ED_NEXT_REASON = ('The follow-up category (Edition-selection policy) says supplier contact is not required unless an older value '
                  'must be confirmed as obsolete; the CSV-only next step required supplier contact.')
VERIF_OLD = ('Finding verified: the TDS typical was found in source text; the SDS bound is quoted from the JSON record '
             '(image/vector SDS page, not re-read in this audit)')
SDS_READ = {  # id: (file, how read, printed text) -- read 2026-11-02
    'CF-150': ('DL2-15542.pdf p.5 (revision date 11/16/2023)', 'text layer', 'Flash point : >= 180 °C (ASTM D92)'),
    'CF-152': ('DL2-15541.pdf p.5', 'page render (no text layer)', 'Flash point : ≥180 ℃'),
    'CF-153': ('DL2-15838.pdf p.5', 'text layer', 'Flash point : ≥180 ℃'),
    'CF-154': ('DL2-15840.pdf p.5', 'text layer', 'Flash point : ≥180 ℃'),
    'CF-155': ('DL2-15850.pdf p.5 (revision date 6/7/2023)', 'text layer', 'Flash point : >= 180 °C (ASTM D92, Open cup)'),
    'CF-156': ('RF6406.pdf p.5', 'text layer', 'Flash point : ≥180 °C (COC)'),
}

C = []  # (id, field, before, after, reason, evidence)


def ch(fid, field, before, after, reason, evidence=''):
    C.append((fid, field, before, after, reason, evidence))


# ---------------------------------------------------------------- CF-146 (classification; spec minimum vs measured VI)
ch('CF-146', 'group', R.CONF, POT,
   'The recorded VI 76 is a specification minimum, not a measured or typical VI; a limit and a classification label are not the '
   'same property measured under comparable conditions, so the comparison cannot confirm a contradiction.',
   'DL2-12172.pdf p.1 (VI row "Min", aramcoPRIMA 70 column 76); DL2-11773.pdf (image-only brochure) has no aramcoPRIMA 70 column; '
   'archive text search for "PRIMA 70" finds only DL2-12172 and the SDS DL2-15448 (no VI)')
ch('CF-146', 'comparability', 'Confirmed: same property, compatible conditions and method (or method not relevant)',
   'Uncertain: the only VI for aramcoPRIMA 70 in the archive is the specification minimum (VI ≥ 76, DL2-12172); no measured or '
   'typical VI is printed (the aramcoPRIMA brochure DL2-11773 has no aramcoPRIMA 70 column), so the product\'s actual VI cannot be '
   'compared with the API 1509 Group II range',
   'A specification minimum and a classification are not comparable as values.', 'as above')
ch('CF-146', 'nature', 'Classification contradicts reported properties (API 1509 definition)',
   'Specification VI minimum (76) below the API 1509 Group II VI floor (80); no measured VI printed',
   'The earlier wording presented the specification limit as a reported property contradicting the class.', 'as above')
ch('CF-146', 'explanation',
   'Group II with a specification VI minimum of 76. The specification allows a VI below 80, the API 1509 lower limit for Group II; '
   'the printed value is a minimum, not a measurement.',
   'Group II heading with a specification VI minimum of 76. API 1509 Annex E (E.1.3) sets VI ≥ 80 and < 120 for Group II. The '
   'comparison establishes only that the specification limit lies below the Group II VI floor: the specification by itself does not '
   'guarantee that every lot meets the Group II VI criterion. It does not show that any lot, or the product\'s typical VI, is below 80, '
   'and it does not show that the Group II label is wrong; a specification minimum is a limit, not a measurement.',
   'States precisely what the Group II threshold comparison establishes and what it does not.',
   'API_1509_21st_Edition_Annex_E.pdf (audit_evidence), E.1.3')
ch('CF-146', 'follow_up_reason',
   'The specification heading (Group II) and its VI minimum (76) are inconsistent with the API 1509 Group II definition; the '
   'grade-level group can only come from the supplier.',
   'The specification (Group II heading) permits a VI (minimum 76) below the API 1509 Group II floor (80), and the archive holds no '
   'measured or typical VI; a typical VI or a grade-level classification can only come from the supplier.',
   'Aligned with the corrected explanation.')
ch('CF-146', 'verification_priority', 'Medium: definition verified; the grade-level group needs the supplier (not contacted).',
   'Medium: definition verified; a measured or typical VI, or the grade-level group, needs the supplier (not contacted).',
   'Aligned with the corrected explanation.')

# ---------------------------------------------------------------- CF-170 (classification; unit not printed)
ch('CF-170', 'group', R.CONF, POT,
   'One value has no printed unit and neither document is dated; the record itself (verbatim open question) says "not a confirmed '
   'numerical contradiction". Classified like CF-168 and CF-169, which compare the same two documents.',
   'DL2-12172.pdf p.1 density row "Density @ 15 oC" (no unit), 4th column 0.867; DL2-11773.pdf brochure (visual) aramcoPRIMA 500 0.8720 Kg/L')
ch('CF-170', 'comparability', 'Partly confirmed: both typical at 15 °C by D4052; DL2-12172 prints no unit',
   'Uncertain: both are typical values at 15 °C by D 4052, but DL2-12172 prints no unit for 0.867 and neither document is dated; '
   'the unit is not assumed',
   'The comparison depends on a unit that is not printed.', 'as above')
ch('CF-170', 'nature', 'Difference between documents (unit not printed in one)',
   'Difference between documents (0.867 with no unit printed vs 0.8720 kg/L); not a confirmed numerical contradiction',
   'Consistent with the record\'s own open question.')
ch('CF-170', 'follow_up_reason',
   'Both documents print a typical density at 15 °C by D4052 (0.867 vs 0.8720) and neither is dated relative to the other.',
   'DL2-12172 prints no unit for 0.867 and neither document is dated; only the supplier can state the unit and which value is '
   'current. The unit is not assumed.',
   'States the missing unit as the reason for the follow-up.')

# ---------------------------------------------------------------- CF-172 (classification; two comparisons)
ch('CF-172', 'group', R.CONF, POT,
   'The two specific-gravity tables share stated conditions but are both undated, and CF-141 shows the Cosan sheet differs from the '
   'catalog for every Ultra-S 6 property while matching it for Ultra-S 4 and 8, so an edition change cannot be excluded; the SDS '
   'comparison has an unspecified reference basis.',
   'DL2-11177.pdf p.1 and DL2-11240.pdf p.1 (Sp.Gravity 15/4 °C, D 1298; no printed date; PDF creation dates 2009-06-01 and '
   '2012-08-27 in file metadata only); DL2-15237.pdf p.2 "RELATIVE DENSITY 0.841 @ 15℃"')
ch('CF-172', 'comparability',
   'Partly confirmed: catalog DL2-11177 and Cosan DL2-11240 both print Sp.Gravity 15/4 °C by D1298 (0.843 vs 0.840); the SDS '
   'relative-density basis is not stated; the catalogs are undated, so an edition change cannot be excluded',
   'Uncertain, two comparisons: (1) catalog DL2-11177 vs Cosan sheet DL2-11240 — same quantity, reference temperatures and method as '
   'printed (Sp.Gravity 15/4 °C, D 1298), 0.843 vs 0.840, but neither sheet prints a date and the Cosan sheet differs from the '
   'catalog for every Ultra-S 6 property (CF-141), so an edition change cannot be excluded; (2) SDS DL2-15237 "RELATIVE DENSITY 0.841 '
   '@ 15℃" — no method and no water reference temperature, so it is not established that 0.841 is comparable with the 15/4 °C values',
   'Distinguishes the matching-condition table comparison from the SDS comparison with an unspecified basis.', 'as above')
ch('CF-172', 'nature', 'Difference between documents (0.843 vs 0.841; the Cosan sheet prints 0.840)',
   'Difference between documents: catalog 0.843 vs Cosan sheet 0.840 (same stated conditions); SDS 0.841 (basis not stated)',
   'Names which pair shares stated conditions.')
ch('CF-172', 'follow_up_reason',
   'The catalog (0.843) and the Cosan sheet (0.840) are undated; dating them would show whether this is an edition change. The SDS '
   'relative-density basis is not stated.',
   'Dated editions of the catalog (0.843) and the Cosan sheet (0.840) are needed to tell an edition change from a contradiction; the '
   'SDS relative-density basis (method, water reference temperature) is not stated.',
   'Aligned with the two comparisons.')

# ---------------------------------------------------------------- CF-141 (classification; editions not dated)
ch('CF-141', 'group', 'Edition difference', POT,
   'Classed as a difference between dated editions, but neither archive sheet prints a date and the web table is undated; the same '
   'document pair is compared in CF-172. A different edition is suggested, not established.',
   'DL2-11177.pdf p.1 and DL2-11240.pdf p.1 (no printed date); PDF metadata: created 2009-06-01 (catalog), 2012-08-27 (Cosan)')
ch('CF-141', 'comparability', 'Confirmed: same document series or same product line, values differ between dated editions',
   'Uncertain: the three value sets come from an undated catalog (DL2-11177), an undated distributor sheet (DL2-11240; PDF file '
   'metadata only: created 2012-08-27, catalog 2009-06-01) and the undated current web table; the Cosan sheet matches the catalog for '
   'Ultra-S 4 and 8 but not for Ultra-S 6, which suggests but does not establish a different edition of the Ultra-S 6 data',
   'The documents are not dated editions.', 'as above')
ch('CF-141', 'follow_up_category', 'Edition-selection policy', 'Standard or further source needed',
   'An edition-selection rule needs dated editions; none of the three sources is dated.')
ch('CF-141', 'follow_up_reason',
   'Values differ between editions of the same supplier document series (DL2-11177.pdf and DL2-11240.pdf and S-OIL web table); a '
   'documented rule for which edition supplies the working value is needed. Supplier contact is not required unless the older value '
   'must be confirmed as obsolete.',
   'Dated editions of the catalog and the Cosan sheet are needed to establish whether the Ultra-S 6 values changed between editions; '
   'the edition-selection rule can then be applied.',
   'Aligned with the corrected classification.')
ch('CF-141', 'next_step',
   'Add the Cosan values to the existing Ultra-S 6 conflicts as a third source; confirm the current edition with S-OIL.',
   'Add the Cosan values to the existing Ultra-S 6 conflicts as a third source; obtain dated editions (S-OIL is a possible source) '
   'before applying the edition-selection rule.',
   'Aligned with the corrected follow-up.')

# ---------------------------------------------------------------- CF-164 (classification; comparability uncertain)
ch('CF-164', 'group', 'Edition difference', POT,
   'The record states that no edition prints the SSI method, cycle count or base oil, and one value comes from another product\'s '
   'bulletin (HiTEC 12360), not from an edition of the HiTEC 5748 data sheet; uncertain comparability is classed as a potential '
   'contradiction (the rule applied to CF-102 in version 4).',
   'Afton_HiTEC-5748_PDS_05-23 p.2, Afton_HiTEC-5748_PDS_07-11 p.2 (audit_evidence); DL2-13692.pdf p.2')
for i, txt in ((0, 'Afton_HiTEC-5748_PDS_05-23__wayback_20241005085229.pdf'), (1, 'Afton_HiTEC-5748_PDS_07-11__wayback_20120503020512.pdf')):
    ch('CF-164', f'values[{i}].page', None, 2, 'No page was cited; the quoted text is on p.2 of the saved evidence copy.', f'{txt} p.2')

# ---------------------------------------------------------------- CF-163 (comparability wording)
ch('CF-163', 'comparability',
   'Partly confirmed: the loading/unloading and blending limits are comparable (60 vs 65 ℃); "storage" (≤ 50 ℃) and "long-term '
   'storage" (≤ 45 ℃) are not worded identically',
   'Confirmed for the loading/unloading and blending limit (≤ 60 ℃ vs ≤ 65 ℃, same wording in both undated TDS); the storage limits '
   '("storage" ≤ 50 ℃ vs "long-term storage" ≤ 45 ℃) are worded differently and are not part of the confirmed contradiction',
   'States which part the "Confirmed contradiction" type rests on.', 'DL2-13819.pdf p.1; DL2-15451.pdf p.1')

# ---------------------------------------------------------------- CF-031 / CF-032 / CF-033..036 (page references)
for fid in ('CF-031', 'CF-032'):
    ch(fid, 'values[1].page', 6, '7 (cited in the JSON as p.6)',
       'The SDS values are printed on p.7 (folio 7/12, Section 9); the JSON conflict entry cites p.6. The source column now gives the '
       'verified page and keeps the original citation; the JSON is unchanged.',
       'DL2-13444.pdf p.7: "Kinematic (40°C): 0,31 cm2/s (31 cSt)", "Closed cup: >180°C [Pensky-Martens.]"; p.6 is Sections 7-8')
for fid in ('CF-033', 'CF-034', 'CF-035', 'CF-036'):
    ch(fid, 'values[0].page', None, '1 (no page in the JSON citation)',
       'The JSON cites DL2-10234.pdf without a page; the one-page TDS prints the value on p.1.', 'DL2-10234.pdf p.1')

# ---------------------------------------------------------------- CF-150, 152-156 (verification now done)
for fid, (where, how, printed) in SDS_READ.items():
    ch(fid, 'verification', VERIF_OLD,
       f'Verified: the TDS typical in source text; the SDS bound read on {where} ({how}, 2026-11-02): "{printed}". Version 4 had quoted the '
       'SDS bound from the JSON record without re-reading it.',
       'The "Verified" level was not supported for the SDS value in version 4; the value has now been read on the cited page.',
       where)

# ---------------------------------------------------------------- CF-145 (value kind of VI 120 not printed; supplier contact optional)
E145 = ('DL2-12221.pdf p.1: page headed "PRODUCT SPECIFICATIONS" ("*The product specifications listed within the table are all accurate on '
        'the date of publishing"), ADbase 3CST column: KV100 3.05, VI 120, no min/max/typical label, no date; ADNOC spec 8230 (August 2020, '
        'audit_evidence) p.3: "ADBASE 3CST (GROUP II)", VISCOSITY INDEX MIN 100, KV100 2.9-3.1')
ch('CF-145', 'group', 'Explainable difference', POT,
   'Version 4 explained the finding as "a specification minimum vs a typical value", but DL2-12221 does not say that VI 120 is a typical '
   'value: it prints single values under "PRODUCT SPECIFICATIONS" without identifying them as typical, minimum or maximum. The explanation therefore rests on an unstated value kind, so '
   'comparability is uncertain.', E145)
ch('CF-145', 'comparability', 'Not comparable as a contradiction: classification by a specification minimum vs a typical value',
   'Uncertain: the Group II label comes with a specification VI minimum of 100 (ADNOC specification 8230, August 2020); DL2-12221 prints VI '
   '120 under "PRODUCT SPECIFICATIONS" as a single value, without identifying it as a typical, minimum or maximum value, and without a date, '
   'so its relation to the Group II specification and to the API 1509 Group III threshold (VI ≥ 120) cannot be established',
   'States the value kind as not printed instead of assuming "typical".', E145)
ch('CF-145', 'nature',
   'Borderline, not a confirmed contradiction: ADNOC specification 8230 (August 2020) heads the grade "ADBASE 3CST (GROUP II)" with a VI '
   'minimum of 100; the typical VI 120 in DL2-12221 is at the Group III threshold of API 1509 Annex E',
   'Borderline, not a confirmed contradiction: ADNOC specification 8230 (August 2020) heads the grade "ADBASE 3CST (GROUP II)" with a VI '
   'minimum of 100; DL2-12221 (undated, headed "PRODUCT SPECIFICATIONS") prints VI 120, at the Group III threshold of API 1509 Annex E, '
   'without identifying it as a typical, minimum or maximum value',
   '"Typical" is not printed in DL2-12221.', E145)
ch('CF-145', 'explanation',
   'Group II with VI 120. API 1509 places VI 80 to < 120 in Group II and VI >= 120 in Group III; a VI of exactly 120 falls in Group III by that definition.',
   'Group II with VI 120. API 1509 places VI 80 to < 120 in Group II and VI >= 120 in Group III; a VI of exactly 120 falls in Group III by '
   'that definition. DL2-12221 does not identify 120 as a typical, minimum or maximum value.',
   'Adds the missing qualifier information.', E145)
ch('CF-145', 'verification',
   'Verified: ADNOC Base Oil Specifications (Group II and Group III), last update August 2020, PDF p.3 "ADBASE 3CST (GROUP II)", spec no. 8230, '
   'VISCOSITY INDEX min 100 (ASTM D2270) — archived copy (Internet Archive 2022-08-15, digest matching the registered URL) saved in '
   'audit_evidence; DL2-12221.pdf p.1 typical VI 120; API 1509 21st edition Annex E, E.1.3: Group II VI ≥ 80 and < 120, Group III VI ≥ 120 '
   '(api.org PDF saved in audit_evidence).',
   'Verified: ADNOC Base Oil Specifications (Group II and Group III), last update August 2020, PDF p.3 "ADBASE 3CST (GROUP II)", spec no. 8230, '
   'VISCOSITY INDEX min 100 (ASTM D2270) — archived copy (Internet Archive 2022-08-15, digest matching the registered URL) saved in '
   'audit_evidence; DL2-12221.pdf p.1, ADbase 3CST column, VI 120 printed as a single value under "PRODUCT SPECIFICATIONS" (value kind not '
   'stated; re-read 2026-11-02); API 1509 21st edition Annex E, E.1.3: Group II VI ≥ 80 and < 120, Group III VI ≥ 120 (api.org PDF saved in '
   'audit_evidence).',
   'Version 4 called the printed value "typical"; the page prints no such label.', E145)
ch('CF-145', 'follow_up_category', 'No follow-up needed beyond documentation', 'Standard or further source needed',
   'What kind of value VI 120 is (typical, minimum or maximum) decides whether the finding is explained; a further dated document is needed.')
ch('CF-145', 'follow_up_reason',
   'Explained by the manufacturer specification (VI minimum 100, Group II); an optional low-priority check of the current typical VI.',
   'A dated ADNOC document identifying the VI 120 of ADbase 3CST in DL2-12221 as a typical, minimum or maximum value is needed. '
   'ADNOC is one possible source, so supplier contact is optional, not required.',
   'Supplier contact stays optional, consistently with the next step.')
ch('CF-145', 'next_step', 'Ask the supplier for the grade-specific API group; keep the recorded label and VI as printed.',
   'Obtain a dated ADNOC document (for example a typical-properties sheet) that identifies the VI 120 as a typical, minimum or maximum value; supplier contact is '
   'optional. Keep the Group II label and the VI 120 as printed.',
   'The version-4 next step required supplier contact while the category said no follow-up was needed.')
ch('CF-145', 'verification_priority', 'Low: confirm the current typical VI of ADbase 3 cSt.',
   'Low: DL2-12221 does not identify the VI 120 as a typical, minimum or maximum value.',
   'The pending item now names the evidence that is actually missing.', E145)

# ---------------------------------------------------------------- CF-024 (printed text completed)
ch('CF-024', 'values[0].printed_text', 'Sulfur Content ppm 1.3‡ (‡ D2622)',
   'Sulfur Content | ppm | ASTM D5453 | 1.3‡ (note: "‡ - D 2622")',
   'The row\'s method column prints ASTM D5453; the ‡ mark refers the value to D 2622. Version 4 quoted only the note.',
   'DL2-13944.pdf p.1 (word positions): "Sulfur Content ppm ASTM D5453 1.3‡"; "Notes: * - D 97 | ‡ - D 2622"')

# ---------------------------------------------------------------- claims matrices: verification stated precisely
MX = ' (afton_matrices.py: vector marks assigned to row and column labels by the table\'s cell separators; read on 300 dpi renders, 2026-11-02)'
ch('CF-001', 'verification', 'Verified in source documents',
   'Verified: DL2-11412.PDF p.2 (05/18) row "10.3% | 5.0% HiTEC® 12255 | SAE 15W-40 | GP I" has a dot under MTU 2.0; DL2-14639.pdf p.2 (08/18), '
   'same row, has none' + MX,
   'Version 4 gave no detail; the dots are drawings, not text.', 'verification_results/afton/')
ch('CF-002', 'verification', 'Verified in source documents',
   'Verified: DL2-11412.PDF p.2 (05/18) row "11.7% | 0.9% HiTEC® 12260 | SAE 10W-30 | GP II" has no dot under DDC 93K215; DL2-14639.pdf p.2 '
   '(08/18), same row, has one' + MX,
   'Version 4 gave no detail; the dots are drawings, not text.', 'verification_results/afton/')
for fid, code in (('CF-005', '20076'), ('CF-006', '20077'), ('CF-007', '20078')):
    ch(fid, 'verification', 'Verified in source documents',
       f'Verified: DL2-14638.pdf p.1 (published 20 Jan, 2020) prints "L" in the row "Cummins CES {code}" (legend "L - Licensable-Licensable '
       f'against an active API category"); DL2-15581.pdf p.1 (published 13 May, 2022) prints "A" in the same row (legend p.2 "A - Approved-Formal '
       f'written approval ...") (word positions, 2026-11-02)',
       'Version 4 gave no detail.', 'DL2-14638.pdf p.1; DL2-15581.pdf p.1-2')
ch('CF-166', 'verification',
   'Verified in source text, except one column: MTU 2.1, Deutz DQC III-10LA, ACEA E9-16 and Ford WSS-M2C214-B1 are in 05/18 (DL2-11796.pdf) and '
   'absent from 04/22 (DL2-15568.pdf); ACEA E11-22, MAN 3775 and Deutz DQC III-18LA are only in 04/22. Checked visually: the 04/22 claims table '
   '(DL2-15568.pdf p.2) has no API CJ-4 column; "CJ-4" appears there only in the text ("backwards compatible … to API CJ-4") and in a chart legend.',
   'Verified: columns only in 05/18 (DL2-11796.pdf p.2): API CJ-4, Ford WSS-M2C214-B1, ACEA E7-16, ACEA E9-16, MTU 2.1, Deutz DQC III-10LA; '
   'only in 04/22 (DL2-15568.pdf p.2): ACEA E7-22, ACEA E11-22, MAN 3775, Deutz DQC III-18LA, Allison TES 439; row API CK-4 10W-40 only in '
   '04/22. In the 45 cells shared by both tables (3 rows x 15 columns) the dots agree' + MX,
   'The statement "for the columns present in both, the dots agree" had not been checked dot by dot; it is now, and holds.',
   'verification_results/afton/DL2-11796_p2_matrix.csv, DL2-15568_p2_matrix.csv')
ch('CF-167', 'verification',
   'Verified in source text: DL2-14639.pdf p.2 (08/18) has API SN, MB 229.3, RN 0700 and footnote "11.15% HiTEC® 12252 = 10.8% HiTEC® 12200 + '
   '0.35% HiTEC® 9552"; DL2-11412.PDF p.2 (05/18) has none of these and carries "Formulations, available in Q2 2018".',
   'Verified in source text: DL2-14639.pdf p.2 (08/18) has API SN, MB 229.3, RN 0700 and footnote "11.15% HiTEC® 12252 = 10.8% HiTEC® 12200 + '
   '0.35% HiTEC® 9552"; DL2-11412.PDF p.2 (05/18) has none of these and carries "Formulations, available in Q2 2018". Dots of the two added '
   'rows confirmed: "10.8% | 0.9% HiTEC® 12260 | SAE 10W-30" marks API CI-4 and API SL; "10.8% | 0.6% HiTEC® 9552 | SAE 10W-40" marks API SN, '
   'API SL, API SJ, ACEA A3/B4-16, MB 229.3 and RN 0700' + MX,
   'The row contents were stated from the open question without a dot-level check.', 'verification_results/afton/DL2-14639_p2_matrix.csv')

# ---------------------------------------------------------------- next steps aligned with follow-up categories
NEXT = {
    'CF-093': ('Ask the supplier which document is authoritative for this property; keep both values.',
               'No separate action: duplicate of CF-096, handled with it under the edition-selection rule; keep both values documented.'),
    'CF-131': ('Confirm the current value with Chevron Phillips; record the older TDS and the SDS values as a conflict.',
               'Apply the edition-selection rule; record the older TDS and the SDS values as a conflict. Supplier contact is optional.'),
    'CF-015': ('None required; confirm the recorded basis (newer dated edition / recorded user decision) is still accepted.',
               'Ask the supplier which value is correct; meanwhile the 2026-10-18 user decision stays the recorded working value and both '
               'values stay documented.'),
    'CF-020': ('None required; confirm the recorded basis (newer dated edition / recorded user decision) is still accepted.',
               'Ask the supplier which value is correct; meanwhile the 2026-10-18 user decision stays the recorded working value and both '
               'values stay documented.'),
    'CF-024': ('Compare methods/conditions on both documents; keep both values with their conditions.',
               'Ask the supplier which unit is intended for 1.3 (ppm or wt.%); keep both values as printed.'),
    'CF-003': ('Confirm the correct value with the supplier; keep both values until then.',
               'None required: keep the TDS typical and the SDS lower bound with their bound types documented.'),
    'CF-022': ('Confirm the correct value with the supplier; keep both values until then.',
               'None required: keep the typical value and the "≥180" bound with their bound types documented.'),
    'CF-138': ('Record as a conflict with methods noted; confirm with ExxonMobil if needed.',
               'Record as a conflict with methods noted; supplier contact is optional.'),
    'CF-136': ('Confirm with Chevron Phillips; if confirmed, the field value -63 °C should be reviewed by the data owner (not changed by this audit).',
               'Data owner reviews the stored -63 °C against DL2-13200 and the manufacturer\'s June 2012 sheet; supplier contact is not '
               'required (not changed by this audit).'),
    'CF-159': ('Note the label/unit inconsistency in the RF6066 KV100 conflict; confirm with Richful.',
               'Note the label/unit inconsistency in the RF6066 KV100 conflict (data owner); supplier confirmation of the SDS label is '
               'optional.'),
}
for fid, (old, new) in NEXT.items():
    ch(fid, 'next_step', old, new,
       'The CSV-only next step contradicted the follow-up category (supplier contact required where the category says it is not, or '
       '"none required" where the category is supplier clarification).')

# ---------------------------------------------------------------- later state (2026-10-31 data corrections)
LATER = {
    'CF-136': 'Corrected 2026-10-31 (commit 28265fd): fields.pour_point now -53 °C, printed_text "Pour Point, °F, °C -53 (-63)"; '
              'see comprehensive_conflicts_audit_corrections_2026-10-31.md.',
    'CF-142': 'Corrected 2026-10-31 (commit 28265fd): sulfated_ash now 7 (typical, Reported, DL2-11503.pdf p.2); the 5.8 estimate kept '
              'as a historical alternate; Zn 0.778 and S 2.35 added.',
    'CF-143': 'Corrected 2026-10-31 (commit 28265fd): sulfated_ash now 10 (typical, Reported, DL2-15722.pdf p.2); the 9.2 estimate kept '
              'as a historical alternate; Zn 0.772 and S 2.4 added.',
    'CF-144': 'After the 2026-10-31 corrections, 24 selected sulfated-ash values are Calculated (23 with Zn factor 1.24, 1 with 1.5) '
              'plus 2 historical alternates; the finding stands for the 24.',
    'CF-159': 'Annotated 2026-10-31 (commit 28265fd): a dated review note was appended to the RF6066 KV100 conflict note; the conflict '
              'stays unresolved.',
    'CF-180': 'Annotated 2026-10-31 (commit 28265fd): a dated review note marks the "swapped" statement as incorrect; the conflict '
              'stays unresolved.',
}
for fid, txt in LATER.items():
    ch(fid, 'later_state', None, txt, 'Distinguishes the 2026-10-30 database state described by the finding from the later correction.',
       'comprehensive_conflicts_audit_corrections_2026-10-31.md')


def get(f, field):
    m = re.fullmatch(r'values\[(\d+)\]\.(\w+)', field)
    return f['values'][int(m.group(1))].get(m.group(2)) if m else f.get(field)


def put(f, field, v):
    m = re.fullmatch(r'values\[(\d+)\]\.(\w+)', field)
    if m:
        f['values'][int(m.group(1))][m.group(2)] = v
    else:
        f[field] = v


def main():
    F = json.load(open(R.SNAPSHOT_FINDINGS, encoding='utf-8'))
    by = {f['id']: f for f in F}
    new = copy.deepcopy(F); nby = {f['id']: f for f in new}
    for f in new:
        f.setdefault('later_state', '')
    log = []
    # recurring edition-selection next step (84 records)
    for f in new:
        if f['follow_up_category'] == 'Edition-selection policy' and f['next_step'] == ED_NEXT_OLD:
            C.append((f['id'], 'next_step', ED_NEXT_OLD, ED_NEXT_NEW, ED_NEXT_REASON, ''))
    seen = set()
    for fid, field, before, after, reason, ev in C:
        assert (fid, field) not in seen, f'duplicate change {fid} {field}'
        seen.add((fid, field))
        cur = get(nby[fid], field) if field != 'later_state' else None
        assert cur == before, f'{fid} {field}: before does not match.\n  expected: {before!r}\n  found:    {cur!r}'
        put(nby[fid], field, after)
        log.append(dict(id=fid, field=field, before='' if before is None else before, after=after, reason=reason, evidence=ev))
    for f in new:
        f['changed_in_v5'] = sorted({x['field'].split('[')[0].split('.')[0] for x in log if x['id'] == f['id']})
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True); os.makedirs(os.path.dirname(OUT_LOG), exist_ok=True)
    json.dump(new, open(OUT_JSON, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    with open(OUT_LOG, 'w', encoding='utf-8-sig', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['id', 'field', 'before', 'after', 'reason', 'evidence'], lineterminator='\r\n')
        w.writeheader(); w.writerows(log)
    ids = sorted({x['id'] for x in log})
    print(f'changes: {len(log)} field changes in {len(ids)} findings')
    import collections
    print('type counts v4:', dict(collections.Counter(f['group'] for f in F)))
    print('type counts v5:', dict(collections.Counter(f['group'] for f in new)))


if __name__ == '__main__':
    main()
