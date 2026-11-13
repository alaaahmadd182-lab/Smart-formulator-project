# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
OV = []


def ov(p, path, new_f, **kw):
    OV.append(dict(p=p, path=path, new_f=new_f, **kw))


T = '(twelfth pass, 2026-11-13)'
# OLOA 59766: SDS DL2-11731.pdf read (sections 1-3, 9; section 11 treatment-rate sentence)
O66 = (f"re-read manually: DL2-11731.pdf (Chevron Oronite SDS 23738, Revision Number 14, January 24, 2017; 11 pages) sections 1-3 and 9 in full and the section 11 skin-sensitization paragraph {T}: "
       "no claims, grades, base oils, co-components, formulations, TBN or KV100 are printed; section 9 'Attention: the data below are typical values and do not constitute a specification': flash (Cleveland Open Cup) 180 C Minimum, relative density 0.9918 at 15.6 C, density 0.9929 kg/l at 15 C, viscosity 2486 mm2/s at 40 C; section 3 component shares only")
for path in ('performance_claims', 'treat_rate_matrix', 'route_selector_restrictions', 'required_co_components', 'published_formulations', 'tbn', 'kv40'):
    ov('CHEVRON_OLOA_59766', path, '*', old_rev=O66)
ov('CHEVRON_OLOA_59766', 'treat_rate_matrix', 'DL2-12453.pdf', reason_append="Context of the existing 11.2 wt% (read on the SDS, twelfth pass): it is printed in section 11 as the basis of the skin-sensitization assessment ('not expected to cause allergic skin reactions when formulated in a finished oil at the prescribed treatment rate of: 11.2 wt. %'), not as a usage recommendation with claim or grade; the deck supplies the claim and grade routes.")
# RF6089: SDS DL2-15841 (1).pdf
R89 = (f"re-read manually: DL2-15841 (1).pdf (Richful RF6089 SDS, REACH format, issue and revision 07/25/2025, version 1.0; 12 pages) sections 1-3 and 9 in full (text layer) {T}: "
       "use 'Blend diesel engine oil'; no claims, treat rate, base oils, TBN or element contents; section 9 (no statistical basis stated): flash point 213 C (COC), kinematic viscosity 92 mm2/s (100 C), density 0.953 g/cm3 (20 C); section 1.3 supplier details are blank in the text layer (not re-checked on the image)")
for path in ('performance_claims', 'treat_rate_matrix', 'package_type_application.package_type', 'permitted_base_oils_restrictions', 'tbn', 'elements.Ca', 'elements.Zn', 'elements.P', 'elements.N', 'elements.B', 'kv100', 'flash_point', 'density'):
    ov('RICHFUL_RF6089', path, 'DL2-15813.pdf', old_rev=R89)
for p, f, d, rate, claims in (('RICHFUL_RF6080', 'DL2-15834.pdf', '2025/5/9', '9.30wt% (including anti-foam agent)', 'API CI-4 and ACEA E7'), ('RICHFUL_RF6081', 'DL2-15836.pdf', '2025/5/13', '9.60wt% (including anti-foam agent)', 'API CI-4, ACEA E7 and JASO DH-1')):
    for path in ('performance_claims', 'package_type_application.package_type'):
        ov(p, path, 'DL2-15813.pdf', old_rev=f"re-read manually: {f} (Richful TDS, Issue Date {d}; 2 pages) whole text {T}: 'meets all {claims} certification requirements'; 'Recommended treat rate is {rate}. It covers viscosity grades 15W-40 and 20W-50'; Group II base oils with VII and PPD; no API SL, no OEM approvals, no composition statement")
ov('ENI_MX_5212', 'route_selector_restrictions', 'DL2-11130.PDF', old_rev=f"re-read manually: DL2-14981.pdf (Eni MX 5212, 02/2017, EN 5023-01; 2 pages) whole text {T}: '6.95% + 1.20% Eni MX 5612A CF-4/SM', '6.95% + 0.50% Eni MX 5612A CF-4/SL', '6.95% CF-4/SJ' ... '1.80% SB/CB'; 'can be used alone or with a specific booster (Eni MX 5612 A) to have a cascade system'; no part-package (5612B / 5612C) equivalence")
ov('BRB_PETROLAD_8099', 'route_selector_restrictions', 'DL2-11052.pdf', old_rev=f"re-read manually: DL2-11053.pdf (BRB Petrolad 8099, issue date May 31, 2016; 3 pages) whole text {T}: claims at 11.2 % wt (CI-4 in a GRII formulation, CH-4 CF-4/SJ, ACEA E7-12, ... Allison C4); 'It can be used in formulations combined with our Viscotech 6540 VI improver'; no booster route")
for p, f, code, ref in (('BAPCO_BAPBASE_6', 'DL2-12888.jfif', 'B-760B', 'REFIN/TS/PRODSPEC/GENE/84'), ('BAPCO_BAPBASE_8', 'DL2-13093.jpg', 'B-780B', 'REFIN/TS/PRODSPEC/GENE/85')):
    ov(p, 'density', '*', old_rev=f"re-read manually: {f} viewed as an image {T}: 'Controlled Bapco Document', {ref}, Issue Status 1.0, 17 August 2017, 'BAHRAIN REFINERY PRODUCT SPECIFICATION CODE NO. {code}'",
       old=f"{f} (Bapco product specification {code}, 17 August 2017; image) prints 'Density at 15 C, kg/m3 | ASTM D 4052 or ASTM D1298 | To be reported' - a density row without limit or value. JSON density Missing. (Correction: the tenth-pass statement 'no density row', taken from the JSON quotation, was wrong.)",
       reason_append="Correction (twelfth pass): the specification lists density as 'To be reported' (no limit); the certificate value is the reported batch result for that item. It remains batch evidence and cannot fill the field as a specification or typical.")
U = (f"re-read manually: DL2-11177.pdf (S-OIL Ultra-S series spread 'Lube base oil 08 | 09'; 1 page) whole text {T}: Ultra-S 6 column Sp.Gravity 15/4 C (D 1298) 0.843, KV40 33.32, KV100 6.0 (D 445), VI 127, flash COC 235, pour (D 5950) -20, Noack 8.0, sulfur < 1.0 wt ppm, saturates > 99")
for path in ('kv40', 'kv100', 'viscosity_index', 'flash_point', 'pour_point', 'noack_volatility', 'specific_gravity'):
    ov('S_OIL_ULTRA_S_6', path, 'DL2-11240.pdf', old_rev=U)
ov('S_OIL_ULTRA_S_6', 'pour_point', 'DL2-11240.pdf', reason_append='Method note (twelfth pass): the cited spread prints the pour point by ASTM D 5950; the Cosan sheet prints D 97.')
for path in ('kv40', 'flash_point', 'api_group_chemistry.chemistry'):
    ov('EXXONMOBIL_SPECTRASYN_2', path, 'DL2-13913.pdf', old_rev=f"re-read manually: DL2-11328.pdf (ExxonMobil Product Datasheet SpectraSyn 2, Revision Date 07/30/2015; 2 pages) whole text {T}: KV100 1.7, KV40 5.0 (D445), pour -66 (D5950/D97), flash COC 157 (D92), SG 0.798 at 15.6 C (D4052); chemistry 'Polyalphaolefin (PAO) Fluid'; no CAS number; footnote 2 marks the -40 C / -54 C viscosities and other single / two-sample items")
for path in ('kv40', 'kv100', 'flash_point'):
    ov('EXXONMOBIL_SPECTRASYN_ELITE_150', path, 'DL2-11849.pdf', old_rev=f"re-read manually: DL2-11378.pdf (ExxonMobil Product Datasheet SpectraSyn Elite 150, Revision Date 01/07/2015; 1 page) whole text {T}: KV100 156, KV40 1649 (D445), VI 210, pour -33, flash COC 277 (D92), SG 0.849 at 15.6 C; 'Typical properties: these are not to be construed as specifications'")
EHCR = (f"re-read manually: DL2-11785.pdf (ExxonMobil 'EHC Series' web print 4/29/2019, edition 03-2019; 3 pages) whole text, compared field by field with all five EHC records {T}; and DL2-11327.pdf (06-2018) both pages")
for p in ('EXXONMOBIL_EHC_45', 'EXXONMOBIL_EHC_50', 'EXXONMOBIL_EHC_65', 'EXXONMOBIL_EHC_110'):
    ov(p, 'kv100', 'DL2-11327.pdf', old_rev=EHCR, reason_append="Field-by-field result (twelfth pass): every limit of DL2-11785.pdf equals the JSON; the same representation issue applies to the viscosity-index range (list in 'value'); colour, appearance and the certification notes ('certified on release', ASTM E 29 rounding, '(a) alternate test methods may be used') have no template field.")
ov('INFINEUM_D3503', 'open_questions', 'DL2-11679.pdf',
   old_rev=f"re-read manually: DL2-11404.pdf (Infineum D3503 data sheet, Version 25 May 2016 (3.0); 2 pages) whole text {T}",
   old="DL2-11404.pdf (cited) ALREADY prints the handling data: 'Min Load/Unload Temp: 60 C', 'Max Load/Unload Temp: 65 C', 'Vis @ Min Load/Unload Temp: 1,210 cSt', 'Vis @ Max Load/Unload Temp: 900 cSt', 'Maximum Storage Temperature: 60 C', 'Do not reheat above: 65 C'; footnotes '(a) Not a specification', '(b) Methods typically used by Infineum manufacturing plants'. The JSON records none of these (its open questions cover Ca, B and pour point only). (Correction: the eleventh-pass statement 'no handling viscosity' in the TDS was wrong.)",
   outcome='in_old_source_not_captured',
   reason_append="Correction (twelfth pass): the handling data are in the cited data sheet itself and were never captured; the SDS repeats them as a range (900-1,210 cSt at 60-65 C). Propose preserving them from the cited source (no template field), with the data-sheet footnotes '(a) Not a specification' and '(b) Methods typically used by Infineum manufacturing plants'.")
ov('PETRONAS_ETRO_6_PLUS', 'density', 'DL2-14915.pdf', old_rev=f"re-read manually: DL2-14610.pdf (ETRO 6+ SDS, Malaysia format, Version 1.2, release 24.03.2020) pp.1 and 4 {T}: 'Relative density : 0.8486 (15 C)', 'Density : 0.8486 g/cm3 (15 C) Method: ASTM D 4052'; and DL2-10234.pdf (ETRO 6+ TDS) density row 'ASTM D 1298/D 4052 | kg/L | - | 0.8429' (typical column; no temperature printed)")
SDSF = "SDS reported value; statistical basis unspecified (SDS section 9: 'Physical and chemical properties are provided for safety, health and environmental considerations only and may not fully represent product specifications')"
for p, f, paths in (('EXXONMOBIL_ESTEREX_P81', 'DL2-12989.pdf', ('kv40', 'kv100', 'pour_point')), ('EXXONMOBIL_SPECTRASYN_2', 'DL2-13913.pdf', ('kv40', 'flash_point')), ('EXXONMOBIL_SPECTRASYN_ELITE_150', 'DL2-11849.pdf', ('kv40', 'kv100', 'flash_point'))):
    for path in paths:
        ov(p, path, f, form=SDSF, qual='SDS reported value (upper bound, printed < -34)' if path == 'pour_point' else 'SDS reported value',
           reason_append="Classification corrected (twelfth pass): the SDS states no statistical basis (not 'typical', not a specification); the value is classed 'SDS reported value; statistical basis unspecified' and must not be promoted to a manufacturer typical or specification.")
links = [dict(p=p, f='DL2-11786.pdf', cat='A', status='completed', fields_status=f'text of each of its 3 pages compared by machine, word by word, with the cited DL2-11785.pdf (identical text, ratio 1.000; a text comparison, not a reading of this file - wording corrected in the sixteenth pass so that it is not counted as a full read); DL2-11785.pdf read in full and compared field by field {T}',
              coverage="assessed by reading (2026-11-13, twelfth pass): identical text to the cited DL2-11785.pdf (03-2019), whose every limit for EHC 45 / 50 / 65 / 110 / 120 equals the JSON (KV100 and VI ranges, flash min, pour max, Noack max Procedure B, CCS max at -25 / -20 C, Group II). Not captured, no template field: ASTM colour max (L0.5 / 0.5), appearance, the certification notes. Representation issue: KV100 and VI ranges stored as lists in 'value' (min / max empty, printed_text '[a, b]'); flash minimum and pour maximum stored in 'value' with value_kind only.",
              identity="exact: 'EHC Series' (identical text to the cited source)", note='Coverage now assessed by reading (field by field).') for p in ('EXXONMOBIL_EHC_45', 'EXXONMOBIL_EHC_50', 'EXXONMOBIL_EHC_65', 'EXXONMOBIL_EHC_110', 'EXXONMOBIL_EHC_120')]
fields = [dict(p='EXXONMOBIL_EHC_120', tier=1, path='kv100', old="DL2-11785.pdf (cited, 03-2019) prints 'Kinematic Viscosity @ 100 C, mm2/s | ASTM D445 | Min- Max | 11.1- 12.7', 'Viscosity Index | Min- Max | 105- 115', 'Flash Point ... Min 255', 'Pour Point ... Max -15'. JSON: KV100 and VI ranges stored as lists in 'value' with min / max null; flash / pour limits stored in 'value' with value_kind only.",
               new_f='DL2-11786.pdf', new_p=2, new_text="'Kinematic Viscosity @ 100 C, mm2/s ASTM D445 Min- Max ... 11.1- 12.7' (EHC 120 column; identical text to the cited DL2-11785.pdf)", unit='mm2/s', form='specification limits (manufacturer sales specification)',
               qual='specification range', method='ASTM D445', cond='', basis='', outcome='already_captured', action='propose_note',
               reason="Values captured but not in the agreed form (ranges in min / max kept as ranges; printed qualifier 'Min', 'Max', 'Min-Max'; printed_text = printed text). Propose a representation correction note; no value changes.",
               old_rev=EHCR, cmp_override='existing: range as a list in value')]
d = dict(batch='twelfth-pass corrections: original-source review and SDS value class; EHC field-by-field', reviewed_on='2026-11-13 (twelfth pass)',
         note="Statements that relied on the JSON quotation of a source ('as quoted in the JSON', 'as recorded in the JSON', 'values as compared in ...', 'line as cited') are not readings. The original pages were read in this pass and the statements replaced with their exact scope; two statements turned out to be wrong (BAPBASE spec has a density row 'To be reported'; the D3503 TDS prints handling viscosities). SDS values whose SDS states no statistical basis are re-classed 'SDS reported value; statistical basis unspecified'.",
         documents={}, links=links, fields=fields, field_overrides=OV)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzz_corrections_twelfth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(OV), len(links), len(fields))
