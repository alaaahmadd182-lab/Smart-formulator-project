"""Nineteenth pass, batch 32: duplicate (category A) coverage of nine long SDSs (HiTEC 12010, 12200, 8799B, 8788B, 12210M; Infineum
D3384, D3451; NEXBASE 3020, 3043). Targeted reading of section 1 (identification) and section 9 (physical and chemical properties)
only, located by their headings, for the property comparison; section 3 and all other sections were NOT read in this pass (the
records' existing composition statements were not re-verified). Writes decisions/zzzzzzzzzzzzzzzzzzz_b32_dup_long_sds_nineteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'nineteenth pass, 2026-11-14'
links, F = [], []


def link(pid, f, n, s9, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed',
                      fields_status=f'section 1 (p.1) and section 9 ({s9}) read in full; section 3 and sections 2, 4-8, 10-16 not read (of {n} pages) ({T})',
                      coverage=f'assessed by reading (2026-11-14, nineteenth pass) for SDS sections 1 and 9 only ({ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file; product name in section 1', note='Byte duplicate of the cited SDS (targeted reading for the property comparison).'))


link('AFTON_HITEC_12010', 'DL2-15021.pdf', 16, 'pp.6-7', 'Version 1.02, date of revision 3/25/2021', "section 9 values recorded from this SDS equal it (density '1.044 g/cm³ [59°F (15°C)]', KV 'Kinematic (40°C): 13.13 cm2/s (1313 cSt)' / '64 cSt @ 100°C', flash 'Closed cup: 135°C (275°F) [Pensky-Martens. Minimum]'). No new row.")
link('AFTON_HITEC_12200', 'DL2-12074.pdf', 21, 'p.7', 'date of issue 16 July 2019', "section 9 prints relative density 0.989 (recorded), KV '4100 cSt at 40°C' / '190 cSt @ 100°C' and flash 'Closed cup: 135°C ... Minimum' (equal to the bulletin values recorded), and 'Density : 0.989 g/cm³ [60.1°F (15.6°C)]' -> note on the reference temperature.")
F.append(dict(p='AFTON_HITEC_12200', tier=2, path='density', old="Record density 0.989 g/ml at 15 °C (bulletin DL2-14639.pdf 'Density at 15°C, g/ml: 0.989').", new_f='DL2-12074.pdf', new_p=7,
              new_text="'Density : 0.989 g/cm³ [60.1°F (15.6°C)]' (section 9)", unit='g/cm³', form='SDS reported value; statistical basis unspecified (Afton SDS section 9)', qual='SDS reported value', method='not printed', cond='15.6 °C', basis='',
              outcome='additional', action='propose_note',
              reason="The SDS prints the same figure 0.989 at a different reference temperature (15.6 °C) from the bulletin (15 °C). Recorded as printed for the reviewer; the two are not compared numerically and no temperature is corrected. No value changes.",
              old_rev=f're-read manually: DL2-12074.pdf (sections 1 and 9) ({T})', cmp_override='existing: 0.989 at 15 °C'))
link('AFTON_HITEC_8799B', 'DL2-15017.pdf', 21, 'p.7', 'date of issue 3 December 2018', "section 9 values recorded from this SDS equal it (relative density 0.958, density 0.956 g/cm³ at 15 °C, KV 3000 cSt at 40 °C / 145 cSt @ 100C, flash closed cup 135 °C minimum). No new row.")
link('AFTON_HITEC_8788B', 'DL2-15016.pdf', 23, 'p.7', 'date of issue 4 November 2019', "section 9 values recorded from this SDS equal it (density 0.958 g/cm³ at 15 °C, KV 2850 / 145 cSt, flash closed cup 135 °C minimum). No new row.")
link('AFTON_HITEC_12210M', 'DL2-15569.pdf', 24, 'pp.7-8 (p.8 also viewed as an image)', 'Version 3.03, date of revision 10/11/2022',
     "section 9 values recorded from this SDS equal it: on the page image 'Minimum' stands on the KV row ('Kinematic (40°C): 1997 mm²/s (1997 cSt) ... Minimum'), as recorded; density '0.95 g/cm³ [59°F (15°C)]'; relative density 0.948 and '108 cSt @ 100°C' equal the bulletin values recorded; flash closed cup 135 °C minimum. No new row.")
link('INFINEUM_D3384', 'DL2-15274.pdf', 26, 'pp.11-13', 'Version 7.0, Revision Date 21.12.2022', "section 9 ('Typical physical and chemical properties are given below') prints relative density 0,974 at 15,6 °C (recorded), density 0,974 g/cm3 at 15 °C, flash 180 °C PMCC (ASTM D93), KV 164 / 3701 mm2/s (ASTM D 445) and 'Pour point : not determined', all equal to the TDS values recorded. No new row.")
link('INFINEUM_D3451', 'DL2-13720.pdf', 40, 'pp.10-12', 'Version 3.1, Revision Date 12.04.2017', "section 9 prints relative density 0,961 at 15,6 °C (recorded), density 0,96 g/cm3 at 15 °C, flash 182 °C PMCC (ASTM D93), KV 146 / 2985 mm2/s and 'Pour point : not determined', equal to the TDS values recorded. No new row.")
link('NESTE_NEXBASE_3020', 'DL2-14513.pdf', 106, 'pp.4-5', 'Revision date 16/06/2020', "section 9 prints 'Kinematic viscosity typical value 7,5 mm2/s @ 40°C' (equal to the TDS typical), pour '≤ -42°C', flash '> 150°C (ASTM D-93)', relative density 0,82 @ 15°C (recorded); the TDS / SDS alternates already exist. Pages 6-106 (sections 10-16 and the exposure-scenario annex) were not read. No new row.")
link('NESTE_NEXBASE_3043', 'DL2-15010.pdf', 153, 'pp.4-5', 'Revision date 28/10/2021', "section 9 prints 'Kinematic viscosity typical value 20 mm2/s @ 40°C' (equal to the TDS typical 20), pour '≤ -12°C', flash '> 220°C (ASTM D-92)', relative density '0,82-0,84 @ 15°C' (recorded). Pages 6-153 (sections 10-16 and the exposure-scenario annex) were not read. No new row.")

d = dict(batch='duplicate coverage, batch 32: long SDSs (nineteenth pass)', reviewed_on='2026-11-14 (nineteenth pass)',
         note='Nine byte-duplicate links; sections 1 and 9 only (section 3 and the rest not read; stated per link).', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzzz_b32_dup_long_sds_nineteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
