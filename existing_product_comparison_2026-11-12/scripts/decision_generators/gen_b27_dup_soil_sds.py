"""Eighteenth pass, batch 27: duplicate (category A) coverage of six four-page S-OIL safety data sheets (Ultra-S 2, 3, 4, 6, 8 and
aramcoULTRA 8). Ultra-S 2 / 3 / 4: all four pages read in full (text layer). Ultra-S 6 / 8 and aramcoULTRA 8: targeted reading of
sections 1 (identification), 3 (composition), 9 (physical and chemical properties), 15-16 (regulatory, other) and every revision
line; sections 4-8 and 10-14 were NOT read for these three. Each compared with its own record.
Writes decisions/zzzzzzzzzzzzzzzzzz_b27_dup_soil_sds_eighteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'eighteenth pass, 2026-11-14'
SDSU = 'SDS reported value; statistical basis unspecified (S-OIL SDS section 9 states no basis)'
links, F = [], []
FULL = 'pp.1-4 read in full (all 4 pages; text layer)'
TARGET = 'sections 1, 3, 9, 15-16 and the revision lines read (targeted); sections 4-8 and 10-14 not read'


def link(pid, f, read, ed, cov, extra_note=''):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read} ({T})',
                      coverage=f"assessed by reading (2026-11-14, eighteenth pass) for {'the whole SDS' if read == FULL else 'SDS sections 1, 3, 9, 15-16'} (4 pp., {ed}): {cov}",
                      identity='SHA-256 equal to the cited archive file; product name in section 1 and the page headers', note='Byte duplicate of the cited SDS.' + extra_note))


def row(pid, f, read, path, tier, old, text, reason, action='propose_alternate_entry', outcome='additional', unit='as printed', method='ASTM D 445', cmp='existing: data-sheet typical only', page=2):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=page, new_text=text, unit=unit, form=SDSU + '; printed as a range or bound', qual='SDS reported value', method=method, cond='', basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=f're-read manually: {f} (S-OIL SDS) {read} ({T})', cmp_override=cmp))


ALT = ("SDS section 9 value never recorded. Propose an alternate entry in the SDS class (statistical basis unspecified), kept as printed ({kind}); the data-sheet typical stays selected. The typical {rel}; that is "
       "{what}, not agreement, and no value is derived from the range.")
S = [  # pid, file, read, edition, KV100 range, KV40 range, flash text, RD, record kv100, kv40, flash, extra
    ('S_OIL_ULTRA_S_2', 'DL2-15235.pdf', FULL, 'Rev. 5, June.10. 2015', '1.9 - 2.4', '6.5 - 9', '≥ 150℃ (ASTM D 92)', '0.82 @ 15℃', 2.174, 7.117, 158, "section 15 '67/548/EEC Xn;R65'; CAS 64742-55-8 (light paraffinic) as recorded"),
    ('S_OIL_ULTRA_S_3', 'DL2-15236.pdf', FULL, 'Rev. 5, June.10. 2015', '3.0 - 3.5', '12.0 - 15.0', '≥ 180℃ (ASTM D 92)', '0.827 @ 15℃', 3.315, 13.47, 204, "section 15 '67/548/EEC Not classified' (Ultra-S 2 prints Xn;R65 for the same CAS 64742-55-8), recorded as printed"),
    ('S_OIL_ULTRA_S_4', 'DL2-15139.pdf', FULL, 'Rev. 5, June.10. 2015', '4.0-4.5', '18.0-20.0', '≥ 210℃ (ASTM D 92)', '0.834 @ 15 ℃', 4.247, 19.62, 228, "flammability limits 0.9 % / 7 %; the light-paraffinic header with CAS 64742-54-7 is an existing open question"),
    ('S_OIL_ULTRA_S_6', 'DL2-15237.pdf', TARGET, 'Rev. 5, June.10. 2015', '5.8 - 6.2', '28.0 - 31.0', '≥ 210℃ (ASTM D 92)', '0.841 @ 15℃', 6.0, 33.32, 235, "EINECS 265-157-1; not classified; flammability limits 0.9 % / 7 %; relative density 0.841 beside the existing specific-gravity open question"),
    ('S_OIL_ULTRA_S_8', 'DL2-15238.pdf', TARGET, 'Rev. 5, June.10. 2015', '7.0 - 7.5', '42.0 - 55.0', '240 ~ 260℃ (ASTM D 92)', '0.847 @ 15℃', 7.234, 43.89, 256, "EINECS 265-157-1; not classified"),
]
for pid, f, read, ed, kv100, kv40, flash, rd, r100, r40, rfl, extra in S:
    lo40, hi40 = [float(x) for x in kv40.replace(' ', '').split('-')]
    out40 = not (lo40 <= r40 <= hi40)
    link(pid, f, read, ed, f"section 1 names the grade; section 3 CAS and the chemistry equal the record; section 9 prints relative density {rd} (the record's specific gravity / density come from DL2-11177.pdf and the S-OIL web page), KV '{kv100} cSt @ 100℃' and '{kv40} cSt @ 40℃' (ASTM D 445) and flash '{flash}'. None of the section 9 values is recorded -> SDS alternate-entry rows"
         + (f"; the recorded KV40 typical {r40} lies OUTSIDE the SDS range {kv40} -> conflict row" if out40 else f"; the recorded typicals (KV100 {r100}, KV40 {r40}, flash {rfl}) lie inside the SDS ranges / bounds (logically compatible only)") + f". Also: {extra}.")
    row(pid, f, read, 'kv100', 1, f"Record kv100 {r100} cSt (DL2-11177.pdf, typical).", f"'VISCOSITY {kv100} cSt @ 100℃ (ASTM D 445)'",
        ALT.format(kind='a range', rel=f'{r100} lies inside {kv100}', what='logical compatibility'), unit='cSt')
    if out40:
        row(pid, f, read, 'kv40', 1, f"Record kv40 {r40} cSt (DL2-11177.pdf, typical).", f"'{kv40} cSt @ 40℃ (ASTM D 445)'",
            f"The data-sheet typical {r40} cSt lies outside the SDS range {kv40} cSt printed by the same supplier. Propose recording the difference as a conflict with both values and sources (the SDS range kept as printed, not converted to a point); not resolved, not averaged, and the selected data-sheet value is not replaced. The proposed TDS-SDS screening thresholds are not approved and are not applied.",
            action='propose_record_conflict', outcome='changed_or_conflicting', unit='cSt', cmp=f'existing: kv40 {r40}')
    else:
        row(pid, f, read, 'kv40', 1, f"Record kv40 {r40} cSt (DL2-11177.pdf, typical).", f"'{kv40} cSt @ 40℃ (ASTM D 445)'",
            ALT.format(kind='a range', rel=f'{r40} lies inside {kv40}', what='logical compatibility'), unit='cSt')
    row(pid, f, read, 'flash_point', 2, f"Record flash_point {rfl} °C COC (DL2-11177.pdf, typical).", f"'FLASH POINT (°C) {flash}'",
        ALT.format(kind='a bound' if '≥' in flash else 'a range', rel=f'{rfl} °C lies within it', what='logical compatibility'), unit='°C', method='ASTM D 92')

link('S_OIL_ARAMCO_ULTRA_8', 'DL2-14611.pdf', TARGET, 'Rev. 0, September.7. 2018',
     "the p.4 page header names 'Base Oil aramcoULTRA 8 (250 Neutral)' (the section 1 'PRODUCT NAME' field is empty in the text layer; not checked on the image); section 3 CAS 64742-54-7 and section 9 (relative density 0.847 @ 15℃, KV '7.0 - 7.5' / '42.0 - 55.0 cSt', flash '240 ~ 260℃') are already in the record (specific gravity and alternate entries; the KV40 edition-difference conflict). No new row. These section 9 figures and the CAS are printed identically in the Ultra-S 8 SDS DL2-15238.pdf (Rev. 5, June 2015); that is recorded as printed and does NOT resolve the open identity question ID-01 (aramcoULTRA 8 vs Ultra-S 8), which stays open.",
     extra_note=' Identity question ID-01 stays open; nothing here merges the two records.')

d = dict(batch='duplicate coverage, batch 27: S-OIL SDSs (eighteenth pass)', reviewed_on='2026-11-14 (eighteenth pass)',
         note='Six byte-duplicate links; three SDSs read in full, three read in sections 1, 3, 9 and 15-16 only (stated per link).', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzz_b27_dup_soil_sds_eighteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
