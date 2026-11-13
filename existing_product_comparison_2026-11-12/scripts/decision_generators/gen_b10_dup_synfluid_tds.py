"""Fourteenth pass, batch 10: coverage of nine duplicate (category A) links to the cited Synfluid data sheets. Each sheet is one
page; it was read in full in the original (this pass, or the thirteenth pass batch 1 where the uncaptured items were listed
in note rows). Writes decisions/zzzzzzzzzzzzzz_b10_dup_synfluid_tds_fourteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
links, F = [], []
B1 = "the uncaptured items are listed in the thirteenth-pass note row (decisions/zzzzzzzzzzzzz_b1_synfluid_thirteenth_pass.json, group (a) 'uncaptured items of the cited data sheet')"
D = [
 ('CHEVRON_SYNFLUID_PAO_4', 'DL2-11914.pdf', 'April 2011', 'thirteenth pass (batch 1), whole page', "KV100 3.9, KV40 16.8, VI 124, pour -68, flash COC 226, Noack 13.4, SG 0.8190 equal the JSON; " + B1),
 ('CHEVRON_SYNFLUID_PAO_6', 'DL2-11915.pdf', 'April 2011', 'thirteenth pass (batch 1), whole page', "KV100 5.9, KV40 30.5, VI 137, pour -61, flash 245, Noack 6.6, SG 0.8278 equal the JSON; " + B1),
 ('CHEVRON_SYNFLUID_PAO_8', 'DL2-11916.pdf', 'April 2011', 'fourteenth pass, whole page (re-read with the JSON beside it)', "KV100 7.8, KV40 46.4, VI 138, pour -56, flash COC 262, Noack 3.5, SG 0.8326 equal the JSON; not captured: KV -40 °C 19,574 cSt, fire point 293 °C, 6.933 lb/gal, TAN <0.03, bromine index <200, colour Pt-Co 0, odour / appearance, handling 65 °C - all already listed in the batch-1 note row"),
 ('CHEVRON_SYNFLUID_MPAO_100', 'DL2-11912.pdf', 'April 2013', 'fourteenth pass, whole page', "KV100 101, KV40 1023, VI 192, pour -44, flash COC 265, SG 0.847 equal the JSON; not captured: 7.069 lb/gal, bromine index <400, colour Pt-Co 0, odour / appearance, handling 65 °C - listed in the batch-1 note row"),
 ('CHEVRON_SYNFLUID_MPAO_150', 'DL2-11913.pdf', 'November 2013', 'thirteenth pass (batch 1), whole page', "KV100 156, KV40 1719, VI 205, pour -39, flash 278, SG 0.849 equal the JSON; " + B1),
 ('CHEVRON_SYNFLUID_MPAO_65', 'DL2-11910.pdf', 'January 2014', 'thirteenth pass (batch 1), whole page (text identical to DL2-15009.pdf)', "KV100 65, KV40 605, VI 181, pour -46, flash '>511 F (266 C)', SG 0.846 equal the JSON; " + B1),
 ('CHEVRON_SYNFLUID_PAO_2', 'DL2-14990.pdf', 'April 2011', 'thirteenth pass (batch 1), whole page', "KV40 5.1 and flash 159 equal the JSON (KV100, SG, pour come from DL2-13192.pdf); " + B1),
 ('CHEVRON_SYNFLUID_PAO_2', 'DL2-13192.pdf', 'December 2008', 'thirteenth pass (batch 1), whole page', "the JSON KV100, SG and pour values are taken from this sheet and equal it; its KV40 5.0 and flash 164 differ from the 2011 sheet used for those fields (recorded in batch 1); " + B1),
 ('CHEVRON_SYNFLUID_MPAO_40', 'DL2-13191.pdf', 'April 2013', 'fourteenth pass, whole page', "KV100 41, KV40 347, VI 172, pour -50, flash COC 244, SG 0.843 equal the JSON; not captured: 7.035 lb/gal, bromine index <400, colour Pt-Co 0, odour / appearance, handling 65 °C -> note row (new)"),
]
for pid, f, ed, when, cov in D:
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'whole page read in the original ({when})',
                      coverage=f"assessed by reading (2026-11-13; read: {when}) for the whole 1-page data sheet ({ed}): {cov}.",
                      identity='SHA-256 equal to the cited archive file', note='Byte duplicate of the cited data sheet.'))
F.append(dict(p='CHEVRON_SYNFLUID_MPAO_40', tier=1, path='open_questions', old="DL2-13191.pdf (cited, April 2013) prints items the JSON does not record: 'Density, lb/gal 7.035'; 'Bromine Index <400'; 'Odor No Foreign Odor'; 'Appearance Clear and Bright'; 'Color, Pt-Co 0'; 'Maximum temperatures of 65 ºC (149 ºF) for handling and ambient for long-term storage are recommended.'",
              new_f='DL2-13191.pdf', new_p=1, new_text='(same file; byte duplicate in the new archive)', unit='as printed', form='typical data and handling statement as printed (data sheet)', qual='as printed', method='', cond='', basis='',
              outcome='in_old_source_not_captured', action='propose_note',
              reason='Old-source information without a template field; preserve with the sheet edition. No mapping to other fields (lb/gal is not converted).',
              old_rev='re-read manually: DL2-13191.pdf (Synfluid mPAO 40 cSt, MSDS # 100000100030, Revision Date April 2013) whole page (fourteenth pass, 2026-11-13)', cmp_override='existing: not recorded'))
d = dict(batch='duplicate coverage, batch 10: cited Synfluid data sheets (fourteenth pass)', reviewed_on='2026-11-13 (fourteenth pass)',
         note='Coverage of byte-duplicate links; each one-page sheet read in full in the original with the JSON beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzz_b10_dup_synfluid_tds_fourteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
