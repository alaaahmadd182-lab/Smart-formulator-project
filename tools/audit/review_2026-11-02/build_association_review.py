"""Record the reviewer's verdict for every citation that the number check accepted only by text presence.

The verdicts below were made by reading the output of citation_context.py (2026-11-02) and, where noted, the page
itself (word positions, renders, column headers). Every presence-only citation gets an entry; the default verdict
applies only to citations whose context was read and found to need no further note. Writes
tools/audit/review_2026-11-02/association_review.json, which verification_ledger.py reads.

Usage: python tools/audit/review_2026-11-02/build_association_review.py
"""
import csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import citation_context as CC
import review_lib as R

ROW = ('row context: the number is on its own row together with the property label, unit and condition (word positions), '
       'in a document for this product only')
CTX = 'context review (text layer, word positions)'
SDS_METHODS = ('. SDS method lines checked: DL2-11909 "Method: ASTM D-92" (p.3, p.4); DL2-11904, DL2-11905, DL2-11907 and DL2-14991 '
               '"Method: Cleveland Open Cup"; DL2-11906 and DL2-14992 print no flash-point method. The SDS sentence "Flashpoints for the '
               'material may vary slightly between the SDS and the bill of lading" concerns the bill of lading, not the TDS')

SPECIAL = {
    'CF-001#0#DL2-11412.PDF': 'matrix', 'CF-001#1#DL2-14639.pdf': 'matrix', 'CF-002#0#DL2-11412.PDF': 'matrix', 'CF-002#1#DL2-14639.pdf': 'matrix',
    'CF-012#0#DL2-13819.pdf': ROW + '; of the two matches of "3.0" the second is the Ca row ("Ca Content,%（m/m） 3.0")',
    'CF-022#1#DL2-14746.pdf': 'row "Total Base Number，mgKOH/g ≥180" (a lower bound, as the finding states); the other 180 on the page is the flash-point row',
    'CF-023#0#DL2-13944.pdf': 'row "Density @ 15.6 0C kg/L ASTM D4052 0.894" on the single-product aramcoDURA BS150 sheet',
    'CF-024#0#DL2-13944.pdf': ('row "Sulfur Content ppm ASTM D5453 1.3‡" with the note "‡ - D 2622": the row\'s method column prints ASTM D5453 '
                               'while the ‡ mark refers the value to D 2622; the finding quoted only the note (completed in version 5)'),
    'CF-024#1#DL2-12173.pdf': ('two tables on the page; the upper one (aramcoDURA 150 / 500) also prints 1.3 for the 500 grade. The value is '
                               'the lower table\'s only column, headed "aramcoDURA BS150": "Sulfur Content Max. WT% ASTM-D 4294 1.3"'),
    'CF-026#0#DL2-10001.pdf': 'single-product specification "Product Name：Base Oil 150N GII+": row "8. Flash Point ℃ 210 D92" in the Min. column',
    'CF-027#0#DL2-15474.pdf': 'Typical Data column (x=487; Min 2.7, Max 3.1); issuing date 30-05-2024',
    'CF-027#1#DL2-12382.pdf': 'TYPICAL column (x=492; limits 2.70-3.10); issuing date 2016-11-01',
    'CF-028#0#DL2-15474.pdf': 'Typical Data column: 0.863 kg/dm³, 15 °C, ASTM D4052',
    'CF-028#1#DL2-12382.pdf': 'TYPICAL column prints 0.860; the JSON and the finding record 0.86 (same number, printed form differs)',
    'CF-029#0#DL2-15474.pdf': 'Typical column: Flash Point, PM °C ASTM D93 95 (Min 90)',
    'CF-029#1#DL2-12382.pdf': 'TYPICAL column: Flash Point, PM °C D 93A 94 (Min 90)',
    'CF-030#0#DL2-15474.pdf': '"< 10" in the Typical Data column (x=487): Sulfur ppm ASTM D2622',
    'CF-030#1#DL2-12382.pdf': '30 in the TYPICAL column (x=492): Sulphur ppm D 2622; the other 30 on the page is the Saybolt colour row',
    'CF-031#0#DL2-11510.pdf': 'typical column (x=492; limits 28.8-35.2): "Viscosity, 40°C mm2/s (cSt) D 445 28.8 35.2 32"',
    'CF-032#0#DL2-11510.pdf': 'row "Flash Point, PM °C D 93 174 176": 174 is the specification minimum, 176 the typical (x=491)',
    'CF-034#0#DL2-10234.pdf': 'row "ASTM D 92 °C ≥ 220 240" (the label "Flash Point" is on the line above): typical 240, specification ≥ 220',
    'CF-036#0#DL2-10234.pdf': 'row "Density ASTM D 1298/D 4052 kg/L - 0.8429": no temperature printed, as the finding states',
    'CF-036#1#DL2-14610.pdf': ('two rows print 0.8486: "Relative density : 0.8486 (15 °C)" and "Density : 0.8486 g/cm3 (15 °C)" with '
                               '"Method: ASTM D 4052"; the finding cites the density row'),
    'CF-133#0#DL2-13193.pdf': 'Typical Value column: VI 144; "Pour Point, °F, °C -49 (-45)" (-45 °C, consistent with -49 °F); Noack 5.5',
    'CF-133#1#DL2-13200.pdf': '5 cSt column (3rd of the C12 table): VI 145; pour -46 (-50); Noack 5.6',
    'CF-134#0#DL2-13194.pdf': 'Typical Value column: KV40 37.3; VI 148; pour "-44 (-42)"; flash "504 (262)"; Noack 3.3',
    'CF-134#1#DL2-13200.pdf': '7 cSt column (4th): KV40 37.7; VI 146; pour -43 (-45); flash 264 (507); Noack 3.7',
    'CF-135#0#DL2-13196.pdf': 'Typical Value column: KV100 9.0; KV40 53.9; pour "-33 (-36)"; flash "529 (276)"; Noack 2.2',
    'CF-135#1#DL2-13200.pdf': '9 cSt column (5th): KV100 8.9; KV40 53.4; pour -34 (-29); flash 280 (536); Noack 2.4',
    'CF-136#1#DL2-13200.pdf': 'C12 Dimer column (1st): "Pour Point, °C (°F) -53 (-63)", method column ASTM D 5950',
    'CF-138#0#DL2-11378.pdf': 'rows "212°F (100°C) 156 cSt 156 mm²/s" and "104°F (40°C) 1649 cSt 1649 mm²/s"',
    'CF-139#0#DL2-12120.pdf': 'rows "212°F (100°C) 8.3 cSt" and "104°F (40°C) 2 84 cSt 84 mm²/s" (2 is a footnote mark)',
    'CF-140#0#DL2-12172.pdf': 'aramcoPRIMA 70 column (1st of 4): "Flash Point, COC ASTM D-92 Min 175 204 220 240"',
    'CF-142#1#DL2-11503.pdf': ('p.2 "SULFATED ASH 7" at x=347, the "Typical" column of the p.1 header "Minimum % Weight | Typical | '
                               'Maximum % Weight"; no method printed'),
    'CF-143#1#DL2-15722.pdf': 'p.2 "SULFATED ASH 10" at x=347, the "Typical" column of the p.1 header; no method printed',
    'CF-145#1#DL2-12221.pdf': ('qualifier', 'ADbase 3CST column (x=446): "Viscosity Index 115 120 130 137 137". The page is headed "PRODUCT '
                               'SPECIFICATIONS" and prints no min/max/typical label; the finding called 120 a "typical VI" (corrected in version 5)'),
    'CF-102#0#DL2-14611.pdf': ('SDS "Base Oil aramcoULTRA 8 (250 Neutral)", revision September.7. 2018: row "42.0 - 55.0 cSt @ 40℃ (ASTM D 445)" '
                               '(the 100 °C row above prints 7.0 - 7.5 cSt); the SDS does not say whether the range is a specification or a typical band'),
    'CF-146#1#DL2-12172.pdf': 'aramcoPRIMA 70 column: "VI ASTM D-2270 Min 76 105 105 105"',
    'CF-147#1#DL2-11261.pdf': 'PURITY VHVI 2 column (1st of VHVI 2/3/4/6/8): "Viscosity Index D2270 100 120 127 127 128"',
    'CF-161#0#DL2-14874.pdf': 'row "Flash Point (COC), ℃ ≮180 210 ASTM D92": ≮180 in the index (specification) column, 210 in the typical column',
    'CF-168#0#DL2-12172.pdf': 'aramcoPRIMA 110 column (2nd): density row "Typical Report 0.8500 0.8630 0.867", no unit printed',
    'CF-169#0#DL2-12172.pdf': 'aramcoPRIMA 230 column (3rd), no unit printed',
    'CF-170#0#DL2-12172.pdf': 'aramcoPRIMA 500 column (4th), no unit printed',
    'CF-172#0#DL2-11177.pdf': 'Ultra-S 6 = 4th of 5 values in "Sp.Gravity, 15/4 °C D 1298" (also checked by check_columns.py)',
    'CF-172#2#DL2-11240.pdf': 'Cosan Ultra-S 6 column (also checked by check_columns.py)',
}


ROW_CONTEXT_KEYS = [
    'CF-003#0#DL2-10204.pdf',
    'CF-003#1#DL2-10204.pdf',
    'CF-004#0#DL2-13065.pdf',
    'CF-004#1#DL2-13713.pdf',
    'CF-008#0#DL2-13819.pdf',
    'CF-008#1#DL2-15451.pdf',
    'CF-008#2#DL2-13820.pdf',
    'CF-009#0#DL2-13819.pdf',
    'CF-009#1#DL2-15451.pdf',
    'CF-009#2#DL2-13820.pdf',
    'CF-010#0#DL2-13819.pdf',
    'CF-010#1#DL2-15451.pdf',
    'CF-010#2#DL2-13820.pdf',
    'CF-011#0#DL2-13819.pdf',
    'CF-011#1#DL2-15451.pdf',
    'CF-012#1#DL2-15451.pdf',
    'CF-013#0#DL2-15618.pdf',
    'CF-014#0#DL2-15536.pdf',
    'CF-014#1#DL2-15542.pdf',
    'CF-015#0#DL2-15536.pdf',
    'CF-015#1#DL2-15542.pdf',
    'CF-016#0#DL2-15832.pdf',
    'CF-016#1#RF6078%20-%20TDS.pdf',
    'CF-017#0#DL2-15832.pdf',
    'CF-017#1#RF6078%20-%20TDS.pdf',
    'CF-018#0#DL2-15836.pdf',
    'CF-018#1#DL2-15837.pdf',
    'CF-019#0#DL2-15839.pdf',
    'CF-019#1#DL2-15840.pdf',
    'CF-020#0#DL2-15839.pdf',
    'CF-020#1#DL2-15840.pdf',
    'CF-021#0#DL2-15456.pdf',
    'CF-021#1#DL2-14746.pdf',
    'CF-022#0#DL2-15456.pdf',
    'CF-025#0#DL2-10414.pdf',
    'CF-025#1#DL2-10414.pdf',
    'CF-025#2#DL2-10025.pdf',
    'CF-026#1#DL2-10011.pdf',
    'CF-031#1#DL2-13444.pdf',
    'CF-032#1#DL2-13444.pdf',
    'CF-033#0#DL2-10234.pdf',
    'CF-033#1#DL2-14610.pdf',
    'CF-034#1#DL2-14610.pdf',
    'CF-035#0#DL2-10234.pdf',
    'CF-035#1#DL2-14610.pdf',
    'CF-099#0#DL2-13728.pdf',
    'CF-099#1#DL2-13729.pdf',
    'CF-100#0#DL2-13726.pdf',
    'CF-100#1#DL2-13730.pdf',
    'CF-101#0#DL2-13727.pdf',
    'CF-126#0#DL2-11912.pdf',
    'CF-127#0#DL2-11913.pdf',
    'CF-128#0#DL2-11914.pdf',
    'CF-129#0#DL2-11915.pdf',
    'CF-130#0#DL2-11916.pdf',
    'CF-131#0#DL2-14990.pdf',
    'CF-131#1#DL2-13192.pdf',
    'CF-132#0#DL2-14990.pdf',
    'CF-132#1#DL2-13192.pdf',
    'CF-136#0#DL2-13202.pdf',
    'CF-137#0#DL2-11378.pdf',
    'CF-137#1#DL2-11849.pdf',
    'CF-138#1#DL2-11849.pdf',
    'CF-139#1#DL2-12989.pdf',
    'CF-140#1#DL2-15448.pdf',
    'CF-148#1#DL2-15451.pdf',
    'CF-149#1#DL2-15618.pdf',
    'CF-150#0#DL2-15542.pdf',
    'CF-150#1#DL2-15536.pdf',
    'CF-151#1#DL2-15832.pdf',
    'CF-151#1#RF6078 - TDS.pdf',
    'CF-152#1#DL2-15535.pdf',
    'CF-152#1#RF6079 Diesel Engine Oil Additive Package.pdf',
    'CF-153#0#DL2-15838.pdf',
    'CF-153#1#DL2-15452.pdf',
    'CF-154#0#DL2-15840.pdf',
    'CF-154#1#DL2-15839.pdf',
    'CF-155#0#DL2-15850.pdf',
    'CF-155#1#DL2-15849.pdf',
    'CF-155#1#RF6400 TDS.pdf',
    'CF-156#0#RF6406.pdf',
    'CF-156#1#DL2-15456.pdf',
    'CF-157#0#DL2-10203.pdf',
    'CF-160#0#DL2-12939.pdf',
    'CF-161#1#RF6602.pdf',
    'CF-162#0#DL2-14874.pdf',
    'CF-163#0#DL2-13819.pdf',
    'CF-163#1#DL2-15451.pdf',
    'CF-164#0#Afton_HiTEC-5748_PDS_05-23__wayback_20241005085229.pdf',
    'CF-164#1#Afton_HiTEC-5748_PDS_07-11__wayback_20120503020512.pdf',
    'CF-164#2#DL2-13692.pdf',
    'CF-172#1#DL2-15237.pdf',
    'CF-173#0#DL2-11303.pdf',
    'CF-174#0#DL2-11304.pdf',
    'CF-175#0#DL2-11305.pdf',
    'CF-176#0#DL2-11306.pdf',
]
SDS_METHOD_KEYS = [
    'CF-126#1#DL2-11906.PDF',
    'CF-126#1#DL2-14992.pdf',
    'CF-127#1#DL2-11909.PDF',
    'CF-128#1#DL2-11904.PDF',
    'CF-129#1#DL2-11907.pdf',
    'CF-130#1#DL2-11905.PDF',
    'CF-131#2#DL2-14991.pdf',
]

# citations without a numeric value, and external sources, read on 2026-11-02 (previously classified by fixed text in the ledger)
OTHER_CITATIONS = {
    'CF-005#0#DL2-14638.pdf': 'claim-code column x=239: "L" in the row "Cummins CES 20076"; legend p.1 "L - Licensable-Licensable against an active API category"',
    'CF-005#1#DL2-15581.pdf': '"A" in the row "Cummins CES 20076"; legend p.2 "A - Approved-Formal written approval provided from a governing body ..."',
    'CF-006#0#DL2-14638.pdf': '"L" in the row "Cummins CES 20077" (legend as for CF-005)',
    'CF-006#1#DL2-15581.pdf': '"A" in the row "Cummins CES 20077" (legend as for CF-005)',
    'CF-007#0#DL2-14638.pdf': '"L" in the row "Cummins CES 20078" (legend as for CF-005)',
    'CF-007#1#DL2-15581.pdf': '"A" in the row "Cummins CES 20078" (legend as for CF-005)',
    'CF-146#0#DL2-12172.pdf': 'label "LUBEREF GII Product Specifications*" heading the table with the column "aramcoPRIMA 70 Spec."',
    'CF-147#0#DL2-11261.pdf': 'p.1 family statements "the only Group III refinery in North America" and "Group III – Cold Crank Simulator"',
    'CF-145#0#https://www.adnoc.ae/-/media/adnoc-v2/files/our-products/adnoc-base-oil-spec-group-ii--group-iii.ashx?hash=E8C7E60F6ED980EDDDB910B5EB2375E21F42336C&la=en':
        'saved Internet Archive copy (audit_evidence), PDF p.3: "ADBASE 3CST (GROUP II)", spec no. 8230, VISCOSITY INDEX MIN 100, last update August 2020',
    'CF-162#1#https://www.richful.com/rfapi/api/product/getproductbyid?productId=105':
        'saved product feed record (audit_evidence): "shall not exceed 60℃ in short term"; long-term storage 45 ℃',
}


def main():
    rows = list(csv.DictReader(open(os.path.join(R.ROOT, 'docs', 'audit_review_2026-11-02', 'verification_results', 'source_checks_v5.csv'),
                                    encoding='utf-8')))
    known = {f"{r['id']}#{r['value_index']}#{r['file']}" for r in rows}
    out = {}
    for k in ROW_CONTEXT_KEYS:
        out[k] = {'verdict': 'verified', 'basis': CTX, 'note': ROW}
    for k in SDS_METHOD_KEYS:
        out[k] = {'verdict': 'verified', 'basis': CTX, 'note': ROW + SDS_METHODS}
    for k, sp in SPECIAL.items():
        if sp == 'matrix':
            out[k] = {'verdict': 'verified', 'basis': 'matrix extraction + visual check',
                      'note': ('claims matrix: the number check had matched unrelated text; the cell was verified by afton_matrices.py '
                               '(vector dots assigned to row and column labels by the cell separators) and on a 300 dpi render with the cell outlined')}
        elif isinstance(sp, tuple):
            out[k] = {'verdict': 'verified, qualifier corrected', 'basis': CTX, 'note': sp[1]}
        else:
            out[k] = {'verdict': 'verified', 'basis': CTX, 'note': sp}
    for k, note in OTHER_CITATIONS.items():
        out[k] = {'verdict': 'verified', 'basis': CTX, 'note': note}
    stale = sorted(set(out) - known)
    assert not stale, f'verdicts for citations that no longer exist: {stale}'
    F = {f['id']: f for f in json.load(open(os.path.join(R.HERE, 'output', 'findings_v5.json'), encoding='utf-8'))}
    missing = [f"{r['id']}#{r['value_index']}#{r['file']}" for r in CC.presence_only(rows, F)
               if f"{r['id']}#{r['value_index']}#{r['file']}" not in out]
    with open(os.path.join(R.HERE, 'association_review.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f'{len(out)} explicit verdicts written; presence-only citations without a verdict: {len(missing)} {missing[:5]}')


if __name__ == '__main__':
    main()
