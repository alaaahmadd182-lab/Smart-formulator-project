"""Fifteenth pass, batch 14: coverage of 15 duplicate (category A) links to cited Richful data sheets and one SDS, each read in full
against the JSON. Writes decisions/zzzzzzzzzzzzzzz_b14_dup_richful_tds_fifteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'fifteenth pass, 2026-11-13'
H45 = "'The long-term storage temperature shall not exceed 45℃, and the loading/unloading or blending temperature shall not exceed 65℃' and 'Packed in 200L iron drums or as required by customers'"
B2 = 'the handling paragraph is already proposed (thirteenth-pass batch 2 note)'
links, F = [], []


def link(pid, f, n, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'pp.1-{n} read in full in the original ({T})',
                      coverage=f'assessed by reading (2026-11-13, fifteenth pass) for the whole document ({n} p., {ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file', note='Byte duplicate of the cited source.'))


def o(f, ed, n=1):
    return f're-read manually: {f} ({ed}) pp.1-{n} whole text ({T})'


def src_add(pid, tier, path, f, printed, web):
    F.append(dict(p=pid, tier=tier, path=path, old=f"The JSON value cites only the supplier web page ({web}); the archived data sheet {f} p.1 prints the identical figures.", new_f=f, new_p=1,
                  new_text=f"'{printed}'", unit='as printed', form='typical value (TDS Typical Value column) with its index range, as printed', qual='as printed', method='as printed', cond='', basis='',
                  outcome='already_captured', action='propose_source_addition',
                  reason='Same value, range and method as the recorded web-page entry. Propose adding the archived data sheet as a second, document-based source; the value is unchanged and nothing is selected or merged.',
                  old_rev=o(f, 'undated TDS'), cmp_override='existing: same value, web source only'))


def handling(pid, f, extra=''):
    F.append(dict(p=pid, tier=1, path='open_questions', old=f"{f} (cited, undated TDS) prints (not recorded in the JSON): {H45}{extra}.", new_f=f, new_p=1, new_text='(same file; byte duplicate in the new archive)',
                  unit='as printed', form='data-sheet handling statement (not a property value)', qual='as printed', method='', cond='storage / loading-unloading-blending', basis='',
                  outcome='in_old_source_not_captured', action='propose_note', reason='Old-source handling information never captured; no template field.', old_rev=o(f, 'undated TDS'), cmp_override='existing: not recorded'))


link('RICHFUL_RF6066', 'DL2-15451.pdf', 1, 'undated TDS', "treat rates 10.5 % (CI-4) / 8.5 % (CH-4), grades, P / Mo / N and flash equal the JSON (cited here); TBN, Ca, Zn, KV100 and density are recorded from the supplier web page with identical figures -> source-addition rows; handling already in route_selector_restrictions.")
for path, tier, pr, in [('tbn', 2, 'Total Base Number, mgKOH/g 97-119 108 SH/T 0251, ASTM D2896'), ('elements.Ca', 2, 'Ca Content, m% 2.82-3.44 3.15 GB/T 17476, ASTM D4951'),
                        ('elements.Zn', 2, 'Zn Content, m% 1.13-1.38 1.24 GB/T 17476, ASTM D4951'), ('kv100', 2, 'Kinematic Viscosity (100℃), mm2/s Report 185 GB/T 265, ASTM D445'),
                        ('density', 2, 'Density (20℃), kg/m3 968-1008 988 SH/T 0604, ASTM D4052')]:
    src_add('RICHFUL_RF6066', tier, path, 'DL2-15451.pdf', pr, 'richful.com catalogueDetail id=112')
link('RICHFUL_RF6069', 'DL2-15618.pdf', 1, 'undated TDS', f"every TDS value equals the JSON except KV100: the TDS prints 'Report 118' while the field holds 142 from the web page / SDS - already an unresolved conflict; the CF-4 '4.1%+1.9%RF0206' route is recorded; {B2}.")
link('RICHFUL_RF6077', 'DL2-15536.pdf', 1, 'undated TDS', f"every value, the 8.76 % CI-4 treat rate and 'OCP VII in Group II base oil' (Group II recorded) equal the JSON; {B2}.")
link('RICHFUL_RF6078', 'DL2-15832.pdf', 1, 'undated TDS', f"values equal the JSON; the ACEA E7/API CI-4 11.85 % vs 10.85 % disagreement with the other TDS is an existing unresolved conflict; density is recorded from the web page with the identical figure -> source-addition row; China V / 60,000 km statements recorded; {B2}.")
src_add('RICHFUL_RF6078', 2, 'density', 'DL2-15832.pdf', 'Density (20℃), kg/m3 952-992 972 GB/T 13377, ASTM D4052', 'richful.com catalogueDetail id=109')
link('RICHFUL_RF6079', 'DL2-15535.pdf', 1, 'undated TDS', f"every value and the 9.15 / 9.50 % treat rates equal the JSON; {B2}.")
link('RICHFUL_RF6088', 'DL2-15452.pdf', 1, 'undated TDS', f"every value and the 13.8 % API CK-4 / ACEA E11 treat rate equal the JSON; {B2}.")
link('RICHFUL_RF6088F', 'DL2-15839.pdf', 1, 'undated TDS', f"every value (incl. sulfated ash '≯8.33 / 8.04' and flash index '≮180', as printed) equals the JSON; {B2}.")
link('RICHFUL_RF6400', 'DL2-15849.pdf', 1, 'undated TDS', f"every value, the 8 treat-rate rows and the grade list equal the JSON; {B2}.")
link('RICHFUL_RF6080', 'DL2-15834.pdf', 2, 'Issue Date:2025/5/9', f"every value and '9.30wt% (including anti-foam agent)' equal the JSON; {B2}.")
link('RICHFUL_RF6081', 'DL2-15836.pdf', 2, 'Issue Date:2025/5/13', f"every value and '9.60wt% (including anti-foam agent)' equal the JSON; {B2}.")
link('RICHFUL_RF6071L', 'RF6071L.pdf', 1, 'undated TDS', "every value and the 15.8 % CI-4 10W-40 treat rate equal the JSON; not recorded: the handling paragraph -> note.")
handling('RICHFUL_RF6071L', 'RF6071L.pdf', " (printed 'shall not excess 65℃')")
link('RICHFUL_RF6406', 'DL2-15456.pdf', 1, 'undated TDS', "every value and the 11 treat-rate rows equal the JSON; TBN and the CF/SF 4.1 % row are recorded from the web page with identical figures -> source-addition rows; not recorded: the handling paragraph -> note.")
src_add('RICHFUL_RF6406', 2, 'tbn', 'DL2-15456.pdf', 'Total Base Number, mgKOH/g 168-198 185 SH/T0251, ASTM D2896', 'richful.com catalogueDetail id=130')
src_add('RICHFUL_RF6406', 1, 'treat_rate_matrix[10].treat_rate_wt_pct', 'DL2-15456.pdf', 'CF/SF Multi 4.1%', 'richful.com catalogueDetail id=130')
handling('RICHFUL_RF6406', 'DL2-15456.pdf')
link('RICHFUL_RF6406', 'RF6406.pdf', 10, 'SDS version 1.1, issue 11/26/2021, revision 04/21/2025', "section 9 values (flash '≥180 °C (COC)', KV '72 mm2/s (100 ℃)', density '1.06 g/cm³ (20 °℃)') are recorded as alternate entries; the section 3 shares are in the open questions; section 7.2 prints 'Storage temperature : No information available'. Not recorded: classification and composition detail -> note.")
F.append(dict(p='RICHFUL_RF6406', tier=1, path='open_questions', old='Not in the cited data sheets (SDS-only information).', new_f='RF6406.pdf', new_p=2,
              new_text="Section 2: Skin Irrit. 2 H315, Eye Irrit. 2 H319; GHS07 'Warning'. Section 3: one share '10 - 59.9' printed across four base-oil rows (CAS 64742-54-7, 64742-65-0, 64742-55-8, 64742-56-9); overbased Ca phenate 68784-26-9 1 - 14.9 (Aquatic Chronic 3 H412); ZDDP 68649-42-3 3 - 29.9 (Skin Irrit. 2 H315, Eye Irrit. 2 H319). Section 1.3 supplier blank. Section 7.2: 'Storage temperature : No information available'. Section 9: Log Kow ZDDP 14.876 (25 °C). Section 15: Netherlands SZW lists as printed; Switzerland storage class LK 10/12.",
              unit='as printed', form='SDS reported value; statistical basis unspecified; SDS classification and composition statements', qual='SDS reported value', method='as printed', cond='', basis='component share ranges (not element contents)',
              outcome='additional', action='propose_note', reason='New-source evidence without a template field; preserve attributed to the SDS; shares stay shares.', old_rev=o('DL2-15456.pdf', 'undated TDS'), cmp_override='existing: shares only'))
link('RICHFUL_RF6408', 'DL2-15534.pdf', 1, 'undated TDS', "every value and the 5.88 % CF-4 treat rate equal the JSON; not recorded: the handling paragraph and the printed engine-test statement ('passed Mack T-8A, Caterpillar 1K, Sequence VIII and Mack T-9 engine tests and all bench tests' with Group II base oil and OCP VM) -> note.")
handling('RICHFUL_RF6408', 'DL2-15534.pdf', "; and 'The 10W-30, 15W-40 and 20W-50 diesel engine oils formulated with this package, Group II base oil and OCP viscosity modifier passed Mack T-8A, Caterpillar 1K, Sequence VIII and Mack T-9 engine tests and all bench tests'")
link('RF6602', 'DL2-14874.pdf', 1, 'undated TDS', "the thickening and shear tables equal the JSON; the KV100 / flash / colour / density, the applications and the storage statements are in the open questions. No new row.")
d = dict(batch='duplicate coverage, batch 14: cited Richful data sheets (fifteenth pass)', reviewed_on='2026-11-13 (fifteenth pass)',
         note='Fifteen byte-duplicate links; each document read in full with the JSON beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzz_b14_dup_richful_tds_fifteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
