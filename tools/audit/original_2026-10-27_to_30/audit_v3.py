"""Version 3 review (2026-10-30): apply source-verified corrections on top of findings.json (v2).
Writes audit/findings_v3.json and audit/corrections_v3.json. Finding IDs are preserved."""
import copy, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

F = json.load(open(os.path.join(A.SCR, 'audit', 'findings.json'), encoding='utf-8'))
PC = json.load(open(os.path.join(A.SCR, 'audit', 'verify_pc.json'), encoding='utf-8'))
SO = json.load(open(os.path.join(A.SCR, 'audit', 'verify_soil.json'), encoding='utf-8'))
BY = {f['id']: f for f in F}
LOG = []


def fid(rid, prop_sub, src_kind=None):
    m = [f for f in F if f['record_id'] == rid and prop_sub in f['property'] and (src_kind is None or f['source_kind'] == src_kind)]
    if len(m) > 1: m = [f for f in m if f['property'] == prop_sub] or m
    assert len(m) == 1, (rid, prop_sub, [x['id'] for x in m]); return m[0]


def change(f, field, new, why):
    old = f.get(field)
    if old != new:
        LOG.append(dict(id=f['id'], record_id=f['record_id'], field=field, old=old, new=new, reason=why)); f[field] = new


for f in F:
    f.setdefault('comparability', ''); f.setdefault('recorded_decision', ''); f.setdefault('related_ids', ''); f.setdefault('duplicate_of', '')
    f.setdefault('outstanding_action', '')
    f['verification_v2'] = f['verification']

PCEV = ('LUB3213E/IM-1809E (2023.03) p.2, official Petro-Canada file archived by the Internet Archive on 2025-12-15 '
        '(SHA-1 H22LVUZOUJCM24UVOA6USLVFG4GZOT6G, identical to the mascherpa.it mirror cited in the record); saved as '
        'reconciliation/audit_evidence/PetroCanada_PURITY_LUB3213E_2023-03__wayback_20251215051152.pdf')
for o in PC['findings']:
    f = BY[o['id']]; c = next(x for x in o['checks'] if x['match_2015'] or x['match_2023'])
    row = c['row'].replace('_', ' ')
    txt = (f"Verified at column level in both editions: DL2-10020.pdf p.2 (LUB3213E 2015.07) prints {c['printed_2015'][0]} and {PCEV} prints "
           f"{c['printed_2023'][0]}, both in column {c['col']}, row '{row}', method {c['printed_2015'][1]}.")
    change(f, 'verification', txt, 'Petro-Canada 2023.03 brochure obtained and read column by column (task 5).')
    change(f, 'comparability', 'Confirmed: same document series (LUB3213E), same grade column, same property row and test method', 'Column-level check.')
    change(f, 'verification_priority', '', 'Verification complete.')
l65_text = next(f for f in F if f['record_id'] == 'PETRO_CANADA_PURITY_L65' and f['property'] == 'viscosity_index')
l65_struct = next(f for f in F if f['record_id'] == 'PETRO_CANADA_PURITY_L65' and f['property'] == 'tier1.viscosity_index')
change(l65_text, 'group', 'Edition difference', 'The "brochure" value 104 is printed in the L65 column of LUB3213E 2023.03; the 92 is LUB3213E 2015.07.')
change(l65_text, 'group_basis', 'Values differ between dated editions (or editions of one document series) of the supplier\'s documents.', 'Type changed.')
change(l65_text, 'nature', 'Edition difference (LUB3213E 2015.07: VI 92; LUB3213E 2023.03: VI 104); recorded as text in the JSON', 'Type changed.')
change(l65_text, 'duplicate_of', l65_struct['id'], f'Same disagreement as {l65_struct["id"]} (structured edition-difference entry for L65 VI).')
change(l65_text, 'values', [dict(value=92, file='DL2-10020.pdf', page=2, revision_date='2015.07', printed_text='Viscosity Index | D2270 | - | - | - | - | 87 | 92 (L65 column)', doc_type='TDS/PDS (LUB3213E 2015.07)', source_check='verified in source text'),
                            dict(value=104, file='PetroCanada_PURITY_LUB3213E_2023-03__wayback_20251215051152.pdf', page=2, revision_date='2023.03', printed_text='Viscosity Index | D2270 | - | - | - | - | 80 | 104 (L65 column)', doc_type='TDS/PDS (LUB3213E/IM-1809E 2023.03)', source_check='verified in source text')], 'Values attached from both editions.')

# ---- S-OIL
for o in SO['findings']:
    f = BY[o['id']]
    if o['match_archive'] and o['match_web']:
        txt = (f"Verified at column level: DL2-11177.pdf p.1 (S-OIL Ultra-S catalog, undated) column Ultra-S {o['grade']} prints {o['archive_cell'][0]} "
               f"({o['archive_cell'][2]}, {o['archive_cell'][1]}); the S-OIL web table (Ultra-S and aramcoULTRA tables identical; live page retrieved "
               f"2026-10-30, identical to the Internet Archive capture of 2026-06-10) column {o['grade']} prints {o['web_cell'][0]} ({o['web_cell'][2]}, {o['web_cell'][1]}).")
        change(f, 'comparability', 'Confirmed: same grade column, same property and method', 'Column-level check.')
    else:
        txt = ('Verified: SDS DL2-14611.pdf p.2 (Base Oil aramcoULTRA 8 (250 Neutral), revision date September 7, 2018) prints "42.0 - 55.0 cSt @ 40℃ (ASTM D 445)"; '
               'the S-OIL web table (live 2026-10-30 = capture 2026-06-10) column aramcoULTRA 8 prints 41.10 (D445).')
        change(f, 'group', 'Genuine contradiction', 'Not an edition difference: an SDS range is compared with a web typical value from a different document type.')
        change(f, 'group_basis', 'Incompatible values for the same product and property; no documented method, condition or edition explains them.', 'Type changed.')
        change(f, 'nature', 'Web typical KV40 41.10 cSt lies below the SDS range 42.0 - 55.0 cSt', 'Type changed.')
        change(f, 'comparability', 'Uncertain: the SDS prints a range without stating whether it is a specification or a typical band', 'Comparability review.')
    change(f, 'verification', txt, 'S-OIL source re-checked column by column (task 5).')
    change(f, 'verification_priority', '', 'Verification complete.')
# ---- comparability for the remaining findings (source-checked in this review)
UNC = {
    ('RICHFUL_RF6066', 'tier2.kv100'): 'Partly uncertain: three values are kinematic viscosity at 100 °C (D445/GB/T 265); the 2021 SDS prints its 185 mm²/s on the "Viscosity, dynamic" line',
    ('RICHFUL_RF6088F', 'tier2.density'): 'Uncertain: the SDS prints "Relative density : 0.958 g/cm3@20℃" (relative-density label with a density unit)',
    ('PETRONAS_ETRO_6_PLUS', 'density'): 'Uncertain: the TDS prints no measurement temperature (SDS: 15 °C)',
    ('CHEVRON_SYNFLUID_MPAO_100', 'tier2.flash_point'): 'Uncertain: neither SDS (DL2-11906, DL2-14992) prints a flash-point method; the TDS value is COC',
    ('CHEVRON_SYNFLUID_PAO_5', 'viscosity_index'): 'Uncertain: the individual TDS (December 2008) prints no test methods; the family table is undated and uses ASTM D7042 for viscosity, so an edition or method difference cannot be excluded',
    ('CHEVRON_SYNFLUID_PAO_7', 'kv40'): 'Uncertain: the individual TDS (December 2008) prints no test methods; the family table is undated and uses ASTM D7042 for viscosity, so an edition or method difference cannot be excluded',
    ('CHEVRON_SYNFLUID_PAO_9', 'kv40'): 'Uncertain: the individual TDS (December 2008) prints no test methods; the family table is undated and uses ASTM D7042 for viscosity, so an edition or method difference cannot be excluded',
    ('ARAMCO_LUBEREF_PRIMA_70', 'tier2.flash_point'): 'Uncertain: the SDS (revision 2.0, 5/05/2021) prints no flash-point method anywhere; the specification minimum is COC (ASTM D-92)',
    ('RF6602', 'flash_point'): 'Uncertain: the SDS prints no flash-point method; the TDS values are COC',
    ('PETRO_CANADA_PURITY_VHVI_2', 'tier1.api_group'): 'Uncertain: the Group III label is a family/refinery statement, not a grade-level classification',
    ('ARAMCO_LUBEREF_PRIMA_110', 'density'): 'Uncertain: DL2-12172 prints no unit; the brochure marks the aramcoPRIMA 110 typicals "subject to confirmation upon startup of the new Group II plant"',
    ('ARAMCO_LUBEREF_PRIMA_230', 'density'): 'Uncertain: DL2-12172 prints no unit; the brochure marks the aramcoPRIMA 230 typicals "subject to confirmation upon startup of the new Group II plant"',
    ('ARAMCO_LUBEREF_PRIMA_500', 'density'): 'Partly confirmed: both typical at 15 °C by D4052; DL2-12172 prints no unit',
    ('AFTON_HITEC_5748', 'shear_stability'): 'Uncertain: no document prints the SSI test method, cycle count or base oil (as the record itself states)',
    ('S_OIL_ULTRA_S_6', 'specific gravity'): 'Partly confirmed: catalog DL2-11177 and Cosan DL2-11240 both print Sp.Gravity 15/4 °C by D1298 (0.843 vs 0.840); the SDS relative-density basis is not stated; the catalogs are undated, so an edition change cannot be excluded',
    ('RICHFUL_RF6066', 'storage / blending'): 'Partly confirmed: the loading/unloading and blending limits are comparable (60 vs 65 ℃); "storage" (≤ 50 ℃) and "long-term storage" (≤ 45 ℃) are not worded identically',
    ('RICHFUL_RF6077', 'tier2.density'): 'Confirmed for direction: 998 kg/m³ at 20 °C vs 0.991 g/cm³ at 15 °C; density falls as temperature rises, so the temperature difference cannot explain the lower value at the lower temperature',
    ('RICHFUL_RF6406', 'tier1.treat_rate'): 'Confirmed: same row (CF/SF Multi) in two undated TDS',
    ('RICHFUL_RF6078', 'tier1.treat_rate_matrix (ACEA'): 'Confirmed for the first row; the second-row labels differ between the two TDS (API CI-4 vs API CI-4 Plus)',
}
for f in F:
    if f['comparability']: continue
    for (rid, sub), txt in UNC.items():
        if f['record_id'] == rid and f['property'].startswith(sub):
            change(f, 'comparability', txt, 'Comparability review (task 2).')
for f in F:
    if f['comparability']: continue
    if f['group'] == 'Genuine contradiction': change(f, 'comparability', 'Confirmed: same property, compatible conditions and method (or method not relevant)', 'Comparability review (task 2).')
    elif f['group'] == 'Edition difference': change(f, 'comparability', 'Confirmed: same document series or same product line, values differ between dated editions', 'Comparability review.')
    elif f['group'] == 'Explainable difference': change(f, 'comparability', 'Not comparable as printed: different method, condition, unit or bound type (stated in the documents)', 'Comparability review.')
    else: change(f, 'comparability', 'Not applicable (recording or documentation issue)', 'Comparability review.')

# ---- individual corrections from the source checks of this review
f = fid('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'sulfur', 'documented')
change(f, 'group', 'Data-quality issue', 'A typical 1.3 ppm does not exceed a specification maximum of 1.3 wt.%; the values are not incompatible as printed.')
change(f, 'nature', 'Suspected unit misprint: the same number 1.3 is printed as a typical in ppm (DL2-13944, D2622) and as a specification maximum in WT% (DL2-12173, D4294)', 'Type changed.')
change(f, 'comparability', 'Uncertain: a typical value is compared with a specification maximum, and the units are 10,000 times apart; which unit is intended cannot be established from the documents', 'Comparability review.')
f = fid('ADNOC_ADBASE_3CST', 'api_group', 'new')
change(f, 'group', 'Explainable difference', 'The manufacturer classifies the grade by its specification (VI minimum 100), which is within the Group II VI range.')
change(f, 'nature', 'Borderline, not a confirmed contradiction: ADNOC specification 8230 (August 2020) heads the grade "ADBASE 3CST (GROUP II)" with a VI minimum of 100; the typical VI 120 in DL2-12221 is at the Group III threshold of API 1509 Annex E', 'Type changed.')
change(f, 'verification', ('Verified: ADNOC Base Oil Specifications (Group II and Group III), last update August 2020, PDF p.3 "ADBASE 3CST (GROUP II)", spec no. 8230, '
                           'VISCOSITY INDEX min 100 (ASTM D2270) — archived copy (Internet Archive 2022-08-15, digest matching the registered URL) saved in audit_evidence; '
                           'DL2-12221.pdf p.1 typical VI 120; API 1509 21st edition Annex E, E.1.3: Group II VI ≥ 80 and < 120, Group III VI ≥ 120 (api.org PDF saved in audit_evidence).'), 'Sources obtained (task 6).')
change(f, 'comparability', 'Not comparable as a contradiction: classification by a specification minimum vs a typical value', 'Comparability review.')
change(f, 'resolution', 'Requires Review', 'Kept for a low-priority confirmation of the current typical VI.')
for rid in ('ARAMCO_LUBEREF_PRIMA_70', 'PETRO_CANADA_PURITY_VHVI_2'):
    f = fid(rid, 'api_group', 'new')
    change(f, 'verification', f['verification'].split(';')[0] + '; the definition was checked in API 1509 21st edition Annex E, E.1.3 (Group II: ≥ 90 % saturates, ≤ 0.03 % sulfur, VI ≥ 80 and < 120; Group III: VI ≥ 120), api.org PDF saved in audit_evidence.',
           'API 1509 Annex E obtained (task 6).')
for rid in ('INFINEUM_D3354', 'INFINEUM_D3375'):
    f = fid(rid, 'flash_point', 'new')
    change(f, 'nature', 'Source ambiguity, not a JSON error: the minimum ("110 min." / "110 Minimum") is printed in a "Typical Inspections" table whose footnote says "(a) Not a specification"; the JSON value_kind "typical" follows the table heading', 'Re-read in the source (task 1).')
    change(f, 'verification', ('Verified visually: DL2-10217.pdf (Infineum D3375, version 10 March 2015 (4.0)) "Flash Point Deg C | 110 Minimum | °C | ASTM D93" under "Typical Inspections", footnote "(a) Not a specification".'
                               if rid.endswith('3375') else 'Verified in source text: DL2-10203.pdf p.1 (Infineum D3354, version 12th December 2005 (3.2)) "Flash Point (PM) | 110 min. | °C" under "Typical Inspections", footnote "(a) Not a specification".'), 'Source checked (task 6).')
    change(f, 'verification_priority', '', 'Verification complete.')
    change(f, 'next_step', 'Data owner to decide how to label a minimum printed in a typical table; not a source conflict.', 'Re-read.')
f = fid('CHEVRON_SYNFLUID_DIMER_C12', 'pour_point', 'new')
change(f, 'verification', ('Verified: archive DL2-13202.pdf p.1 (April 2011) prints "Pour Point, °F, °C | -53 (-63)"; DL2-13200.pdf prints "Pour Point, °C (°F) | -53 (-63)"; '
                           'the current Chevron Phillips data sheet (cpchem.com, "Synfluid® Dimer C12", revision date June 2012) prints "Pour Point, °C (°F) | ASTM D5950 | -53 (-63)". '
                           'Copy saved in audit_evidence. The 2012 sheet also prints KV40 8.11 cSt (archive 7.7) and COC flash point 181 °C (archive 183): later-edition values, noted only.'), 'Manufacturer source obtained (task 6).')
change(f, 'verification_priority', '', 'Verification complete; a data-owner decision remains.')
change(f, 'outstanding_action', 'Data owner: review the stored -63 °C (not changed by this audit).', 'Action, not verification.')
f = fid('S_OIL_ULTRA_S_4', 'chemistry', None)
change(f, 'verification', ('Verified: DL2-15139.pdf p.1 (revision date June 10, 2015) prints "Distillates (petroleum), hydrotreated light paraffinic" with CAS 64742-54-7. '
                           'PubChem (NIH) substance records name CAS 64742-54-7 "Distillates (petroleum), hydrotreated heavy paraffinic" (7 records, no "light"), while '
                           '"hydrotreated light paraffinic" is the name recorded for CAS 64742-55-8 (5 records). Responses saved in audit_evidence. CAS Common Chemistry itself '
                           'requires an API key and was not consulted.'), 'Registry evidence obtained (task 6).')
change(f, 'verification_priority', '', 'Verification complete (registry evidence).')
change(f, 'group', 'Genuine contradiction', 'Confirmed contradiction within one supplier document.')
change(f, 'comparability', 'Confirmed: name and CAS number in the same SDS line', 'Comparability review.')
f = fid('S_OIL_ULTRA_S_6', 'specific gravity', None)
change(f, 'values', [dict(value='0.843', file='DL2-11177.pdf', page=1, printed_text='Sp.Gravity, 15/4 °C | D 1298 | 0.820 | 0.827 | 0.834 | 0.843 | 0.847 (Ultra-S 6 = 4th column)', doc_type='S-OIL catalog', source_check='verified in source text')] + f['values'][1:], 'Catalog value isolated by column.')
change(f, 'verification', 'Verified at column level: 0.843 (DL2-11177 p.1, Ultra-S 6 column), 0.841 (SDS DL2-15237 p.2, revision June 10, 2015), 0.840 (Cosan DL2-11240 p.1, Ultra-S 6 column).', 'Task 6.')
change(f, 'verification_priority', '', 'Verification complete.')
f = fid('PETRO_CANADA_PURITY_L65', 'viscosity_index', 'documented') if False else l65_text
change(f, 'verification', 'Verified at column level: DL2-10020.pdf p.2 (LUB3213E 2015.07) L65 VI 92; ' + PCEV + ' L65 VI 104. The record calls the second source the "World-Class Base Oils brochure"; the same value is printed in LUB3213E 2023.03.', 'Brochure obtained (task 6).')
change(f, 'verification_priority', '', 'Verification complete.')
change(f, 'comparability', 'Confirmed: same document series, same column and row', 'Comparability review.')
f = fid('AFTON_HITEC_5748', 'shear_stability', None)
change(f, 'values', [dict(value='Shear Stability Index %: 22', file='Afton_HiTEC-5748_PDS_05-23__wayback_20241005085229.pdf', page=None, revision_date='05/23', doc_type='PDS (Internet Archive original bytes)', source_check='verified in source text'),
                     dict(value='"It is based on 23 SSI polymer"', file='Afton_HiTEC-5748_PDS_07-11__wayback_20120503020512.pdf', page=None, revision_date='07/11', doc_type='PDS (Internet Archive original bytes)', source_check='verified in source text'),
                     dict(value='"HiTEC® 5748 25SSI OCP" / "25SSI viscosity modifier"', file='DL2-13692.pdf', page=2, revision_date='07/20', doc_type='HiTEC 12360 bulletin', source_check='verified in source text')], 'Editions obtained.')
change(f, 'verification', 'Partially verified: 05/23 PDS "Shear Stability Index %: 22", 07/11 PDS "based on 23 SSI polymer" (Internet Archive copies saved in audit_evidence) and DL2-13692.pdf p.2 "25SSI" verified; the 03/18 and 04/21 editions could not be retrieved (Internet Archive search temporarily offline on 2026-10-30) and remain as recorded.', 'Task 6.')
change(f, 'verification_priority', 'Low: two further editions to retrieve; comparability cannot be established from any edition.', 'Task 6.')
change(f, 'outstanding_action', 'Supplier confirmation of SSI and method (not contacted).', 'Action.')
f = fid('AFTON_HITEC_12200', 'performance_claims / treat_rate_matrix', None)
change(f, 'group', 'Edition difference', 'The record states these are additions between editions, not disagreements.')
change(f, 'nature', 'Edition change (rows, columns and a footnote added in the 08/18 bulletin); not a disagreement', 'Type changed.')
change(f, 'verification', 'Verified in source text: DL2-14639.pdf p.2 (08/18) has API SN, MB 229.3, RN 0700 and footnote "11.15% HiTEC® 12252 = 10.8% HiTEC® 12200 + 0.35% HiTEC® 9552"; DL2-11412.PDF p.2 (05/18) has none of these and carries "Formulations, available in Q2 2018".', 'Task 6.')
change(f, 'verification_priority', '', 'Verification complete.')
change(f, 'resolution', 'Not a value conflict', 'Additions between editions; nothing to resolve.')
f = fid('AFTON_HITEC_12210M', 'performance_claims', None)
change(f, 'nature', 'Edition change (claims columns added and removed between the 05/18 and 04/22 bulletins); not a disagreement about a value', 'Re-read.')
change(f, 'verification', 'Verified in source text, except one column: MTU 2.1, Deutz DQC III-10LA, ACEA E9-16 and Ford WSS-M2C214-B1 are in 05/18 (DL2-11796.pdf) and absent from 04/22 (DL2-15568.pdf); ACEA E11-22, MAN 3775 and Deutz DQC III-18LA are only in 04/22. Checked visually: the 04/22 claims table (DL2-15568.pdf p.2) has no API CJ-4 column; "CJ-4" appears there only in the text ("backwards compatible … to API CJ-4") and in a chart legend.', 'Task 6 (visual check of p.2).')
change(f, 'verification_priority', '', 'Verification complete.')
change(f, 'resolution', 'Not a value conflict', 'Claims changes between editions.')
f = fid('RF6602', 'storage temperature', None)
change(f, 'values', [dict(value='short-term storage and transportation ≤ 75 ℃; long-term storage ≤ 45 ℃', file='DL2-14874.pdf', page=1, doc_type='TDS (undated)', source_check='verified in source text'),
                     dict(value='short-term storage and transportation ≤ 60 ℃; long-term ≤ 45 ℃', file='https://www.richful.com/rfapi/api/product/getproductbyid?productId=105', doc_type='Richful product data feed (product 105, RF6602), retrieved 2026-10-30, saved in audit_evidence', source_check='verified')], 'Product page obtained.')
change(f, 'verification', 'Verified: TDS DL2-14874.pdf p.1 (75 ℃ / 45 ℃) and the Richful product data feed for product 105 (60 ℃ / 45 ℃), retrieved 2026-10-30.', 'Task 6.')
change(f, 'comparability', 'Confirmed: both state the short-term storage and transportation limit', 'Comparability review.')
change(f, 'verification_priority', '', 'Verification complete.')
f = fid('RICHFUL_RF6406', 'product.supplier', None)
change(f, 'verification', 'Verified: the JSON spells the supplier "Xinxiang Richful Lube Additive Co., Ltd." in 11 records and without the final period in RF6602; it is null in RF6071L, RF6406 and RF6408; the archive documents print "Xinxiang Richful Lube Additive Co." followed by a varying suffix.', 'Task 6.')
change(f, 'verification_priority', '', 'Verification complete.')
f = fid('FORMOSA_150N_GII_PLUS', 'product identity', None)
change(f, 'verification', 'Partially verified: DL2-12108.jpeg read visually — "Specification of FPCC API GII Base Oil" with Specification and Typical (2017 AUG) columns 70N, 150N and 500N. Whether these columns are FORMOSA_150N_GII_PLUS and FORMOSA_500N_GII cannot be established from the documents.', 'Task 6.')
change(f, 'verification_priority', 'Medium: identity needs the supplier (not contacted).', 'Task 6.')
change(f, 'outstanding_action', 'Supplier confirmation of product identity (not contacted).', 'Action.')
f = fid('S_OIL_ULTRA_S_8', 'product identity', None)
change(f, 'verification', 'Partially verified: the S-OIL web page (live 2026-10-30) prints identical typical-property tables for "Ultra-S" and "aramcoULTRA" grades 2-8, and both SDSs name the product "(250 Neutral)" with the same KV ranges (DL2-15238.pdf, 2015; DL2-14611.pdf, 2018). No document states that the two names designate one product.', 'Task 6.')
change(f, 'verification_priority', 'Medium: identity needs the supplier (not contacted).', 'Task 6.')
change(f, 'outstanding_action', 'Supplier confirmation of product identity (not contacted).', 'Action.')
f = fid('ARAMCO_LUBEREF_PRIMA_70', 'tier2.flash_point', 'new')
change(f, 'verification', 'Verified: DL2-12172.pdf p.1 "Flash Point, COC | ASTM D-92 | Min | 175" (aramcoPRIMA 70 column); DL2-15448.pdf p.5 (revision 2.0, issue date 5/05/2021) "Flash point : 168 °C". The whole SDS was searched: no flash-point method is printed.', 'Task 6.')
change(f, 'verification_priority', 'Medium: the SDS test method is needed (supplier; not contacted).', 'Task 6.')
change(f, 'outstanding_action', 'Supplier: flash-point method of the SDS value (not contacted).', 'Action.')
f = fid('MINGLAN_T3161A', 'sulfated_ash', 'new')
change(f, 'verification', 'Pending: JSON-only inconsistency confirmed (zinc factor 1.24 in 25 records, 1.5 in MINGLAN_T3161A, which also adds Mo and B terms). ASTM D874-23 is not freely accessible (ASTM store), so which factor set is correct could not be checked.', 'Task 6.')
change(f, 'verification_priority', 'High: obtain ASTM D874-23 (Appendix) to check the factors; affects all 26 Calculated sulfated-ash values.', 'Task 6.')
change(f, 'outstanding_action', 'Access to ASTM D874-23.', 'Action.')
for rid in ('ARAMCO_LUBEREF_PRIMA_70', 'PETRO_CANADA_PURITY_VHVI_2'):
    f = fid(rid, 'api_group', 'new')
    change(f, 'verification_priority', 'Medium: definition verified; the grade-level group needs the supplier (not contacted).', 'Task 6.')
    change(f, 'outstanding_action', 'Supplier: grade-level API group (not contacted).', 'Action.')
f = fid('ADNOC_ADBASE_3CST', 'api_group', 'new')
change(f, 'verification_priority', 'Low: confirm the current typical VI of ADbase 3 cSt.', 'Task 6.')
for f in F:
    if f['record_id'] in ('ARAMCO_LUBEREF_PRIMA_110', 'ARAMCO_LUBEREF_PRIMA_230', 'ARAMCO_LUBEREF_PRIMA_500') and f['property'] == 'density':
        change(f, 'verification_priority', '', 'Verified in the previous review.')

# ---- resolution labels: separate recorded decisions from scientific resolution
for f in F:
    if f['source_kind'] != 'documented': continue
    raw = next((x for x in [f.get('explanation', '')] if x), '')
    fr = re.search(r'final_resolution: (.*)$', raw)
    if f['resolution'] in ('Resolved', 'Requires Review') and fr:
        dec = fr.group(1)
        if 'User decision of 2026-10-18' in dec or 'User decision of 2026-10-18' in raw:
            change(f, 'recorded_decision', 'User decision of 2026-10-18: working value selected for the field (' + dec[:200] + '); this is a working choice, not a scientific resolution of the source disagreement', 'Task 4.')
        elif 'newest edition' in dec:
            change(f, 'recorded_decision', 'Working value: newer dated edition of the same supplier document (' + dec[:160] + '); the older edition\'s value is not shown to be wrong', 'Task 4.')
        elif 'No value conflict' in dec:
            change(f, 'recorded_decision', 'Note only: ' + dec, 'Task 4.')
        if 'No value conflict' in dec:
            change(f, 'resolution', 'Not a value conflict', 'The entry records a measurement-temperature note, not a disagreement.')
        elif f['resolution'] == 'Resolved':
            change(f, 'resolution', 'Unresolved', 'A working value was selected, but the source disagreement itself is not resolved (task 4). The JSON still carries resolved: true.')
for f in F:
    if f['source_kind'] == 'documented' and f['resolution'] == 'Unresolved' and not f['recorded_decision']:
        m = re.search(r'final_resolution: (Not resolved\..*)$', f['explanation'])
        if m: f['recorded_decision'] = 'PR #2 proposal not adopted (kept as text in final_resolution)'
# ---- duplicates and related findings
REL = {(fid('RICHFUL_RF6066', 'tier2.kv100', 'documented')['id']): fid('RICHFUL_RF6066', 'tier2.kv100 (SDS value)', 'new')['id'],
       fid('RICHFUL_RF6078', 'tier1.treat_rate_matrix (ACEA', 'documented')['id']: fid('RICHFUL_RF6078', 'final_resolution', 'new')['id']}
for a, b in REL.items():
    change(BY[a], 'related_ids', b, 'Cross-reference (task 3).'); change(BY[b], 'related_ids', a, 'Cross-reference (task 3).')
u6 = fid('S_OIL_ULTRA_S_6', 'kv40, kv100', 'new')
rel = [f['id'] for f in F if f['record_id'] == 'S_OIL_ULTRA_S_6' and f['id'] != u6['id']]
change(u6, 'related_ids', ', '.join(rel), 'Adds a third source to the documented Ultra-S 6 conflicts and to the specific-gravity question (task 3).')
change(l65_struct, 'related_ids', l65_text['id'], 'Duplicate pair (task 3).')
for x in (fid('AFTON_HITEC_12200', 'MTU 2.0', 'documented'), fid('AFTON_HITEC_12200', 'DDC 93K215', 'documented')):
    pass
# ---- outstanding actions for unresolved scientific findings (supplier contact not done)
for f in F:
    if not f['outstanding_action'] and f['resolution'] in ('Unresolved', 'Requires Review') and f['group'] in ('Genuine contradiction', 'Edition difference'):
        f['outstanding_action'] = 'Supplier confirmation (not contacted in this audit)'
json.dump(F, open(os.path.join(A.SCR, 'audit', 'findings_v3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
json.dump(LOG, open(os.path.join(A.SCR, 'audit', 'corrections_v3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
import collections
C = collections.Counter
print('findings', len(F), '| corrections', len(LOG), C(x['field'] for x in LOG))
print('types', C(f['group'] for f in F)); print('resolution', C(f['resolution'] for f in F))
print('comparability', C(f['comparability'].split(':')[0] for f in F))
print('pending priority', C(f['verification_priority'].split(':')[0] for f in F if f['verification_priority']))
print('duplicates', [(f['id'], f['duplicate_of']) for f in F if f['duplicate_of']])
