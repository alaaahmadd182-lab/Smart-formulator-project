# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
SDSU = 'SDS reported value; statistical basis unspecified (CPChem SDS section 9 gives no statistical basis)'
T = '(thirteenth pass, 2026-11-13)'
links, F = [], []
# pid, sds file, sds date/version, sds pages read, cited TDS + its text, conflicts [(path, sds printed, tds printed, method note)], alternates, sds-only info, tds-uncaptured info
D = [
 ('CHEVRON_SYNFLUID_PAO_4', 'DL2-11904.PDF', 'Version 3.4, Revision Date 2018-08-03, SDS 100000010950; 10 pages', 'sections 2-3 and 9 (pp.2-6) in full',
  'DL2-11914.pdf', 'MSDS # 3332, Revision Date April 2011', [('flash_point', 2, "Flash point : 219 C (426 F) Method: Cleveland Open Cup", "Flash Point (COC) 438 F (226 C)")], [],
  "Section 3: '1-Decene, homopolymer, hydrogenated', CAS 68037-01-4, 100 wt%, classification Asp. Tox. 1; H304. Section 9: autoignition 343 C; boiling point / range 414 C; vapour pressure 1,70 mmHg at 177 C; relative density 0,82 at 15,6 C (already captured as an alternate SG entry); 'Viscosity, kinematic : 16 cSt at 37,8 C (100,0 F)' (a 37.8 C value, not comparable with KV40)",
  "KV -40 C 2,498 cSt; fire point COC 253 C; density 6.820 lb/gal; TAN < 0.03; bromine index < 200; colour Pt-Co 0; max handling 65 C"),
 ('CHEVRON_SYNFLUID_PAO_6', 'DL2-11907.pdf', 'Version 1.8, Revision Date 2016-03-07, SDS 100000010952; 11 pages', 'sections 2-3 and 9 (pp.2-5) in full',
  'DL2-11915.pdf', 'MSDS # 3333, Revision Date April 2011', [('flash_point', 2, "Flash point : 238 C (460 F) Method: Cleveland Open Cup", "Flash Point (COC) 473 F (245 C)")], [],
  "Section 3: '1-Decene Homopolymer Hydrogenated', CAS 68037-01-4, 100 wt%; 'Contains no hazardous ingredients according to GHS'. Section 9: autoignition 354 C; boiling 419 C; vapour pressure 0.70 mmHg at 149 C; relative density 0.83 at 15.6 C (captured as alternate); KV40 30.5 cSt (equal to the data sheet); relative vapour density 10",
  "KV -40 C 7,712 cSt; fire point 276 C; density 6.893 lb/gal; TAN < 0.03; bromine index < 200; colour 0; max handling 65 C"),
 ('CHEVRON_SYNFLUID_PAO_8', 'DL2-11905.PDF', 'Version 2.5, Revision Date 2016-05-31, SDS 100000062776; 37 pages (multi-country annexes)', 'sections 2-3 and 9 (pp.2-6) in full; annex pages not read',
  'DL2-11916.pdf', 'MSDS # 3334, Revision Date April 2011 (read in full, tenth pass)', [('flash_point', 2, "Flash point : 257 C (495 F) Method: Cleveland Open Cup", "Flash Point (COC) 504 F (262 C)")], [],
  "Section 2: not a hazardous substance or mixture. Section 3: '1-Decene Homopolymer ...' (continues on p.3; CAS not re-read). Section 9: autoignition 369 C; boiling 430 C; vapour pressure 0,10 mmHg at 232 C; relative density 0,83 at 15,6 C (captured as alternate); 'Viscosity, kinematic : 46 cSt at 40 C' (data sheet 46.4: consistent at the printed precision); relative vapour density 10",
  "KV -40 C 19,574 cSt; fire point 293 C; density 6.933 lb/gal; TAN < 0.03; bromine index < 200; colour 0; max handling 65 C"),
 ('CHEVRON_SYNFLUID_MPAO_100', 'DL2-11906.PDF', 'Version 2.0, Revision Date 2017-07-10, SDS 100000100031; 9 pages', 'sections 2-3 and 9 (pp.2-5) in full',
  'DL2-11912.pdf', 'Revision Date April 2013 (read in full, tenth pass)', [('kv40', 1, "Viscosity, kinematic : 1014 cSt at 40 C (104 F)", "KV40 1023 cSt")],
  [('flash_point', 2, "Flash point : 255 C (491 F)  (no method printed)", "Flash Point (COC) 509 F (265 C)")],
  "Section 2: not hazardous (EC 1272/2008). Section 3: '1-Octene Homopolymer, Hydrogenated', CAS 70693-43-5, 100 wt%. Section 9: ignition temperature 310 C; freezing point -44 C (a different property from the pour point, not used as one); boiling point > 250 C; density 0,84 g/cm3 (no temperature)",
  "density 7.069 lb/gal; bromine index < 400; colour; max handling 65 C (sheet as read in the tenth pass)"),
 ('CHEVRON_SYNFLUID_MPAO_65', 'DL2-11908.PDF', 'Version 2.0, Revision Date 2017-07-10, SDS 100000102086; 9 pages', 'sections 2-3, 5 and 9 (pp.2-5) in full',
  'DL2-11910.pdf', 'MSDS #100000102086, Revision Date January 2014 (read in full, this pass)', [], [],
  "Section 3: '1-Octene Homopolymer, Hydrogenated', CAS 70693-43-5, 100 wt%; not hazardous. Section 9: flash 270 C (ASTM D-92) (already captured as an alternate entry); ignition 310 C; freezing point -47 C (not a pour point); boiling > 250 C; density 0,84 g/cm3 (no temperature); KV100 65 cSt (equal)",
  "max handling 82 C; density 7.060 lb/gal; bromine index < 400; colour Pt-Co 0; the flash point is printed as a bound '>511 F (266 C)' (COC)"),
 ('CHEVRON_SYNFLUID_MPAO_150', 'DL2-11909.PDF', 'Version 2.0, Revision Date 2017-07-10, SDS 100000102070; 9 pages', 'sections 2-3 and 9 (pp.2-5) in full',
  'DL2-11913.pdf', 'MSDS # 100000102070, Revision Date November 2013', [('flash_point', 2, "Flash point : 250 C (482 F) Method: ASTM D-92", "Flash Point (COC) 532 F (278 C)"), ('kv40', 1, "Viscosity, kinematic : 1700 cSt at 40 C (104 F)", "KV40 1719 cSt")], [],
  "Section 3: '1-Octene Homopolymer, Hydrogenated', CAS 70693-43-5, 100 wt%; not hazardous. Section 9: ignition 310 C; freezing point -39 C (not a pour point); boiling > 250 C; density 0,84 g/cm3 (no temperature)",
  "max handling 82 C; density 7.085 lb/gal; bromine index < 400; colour 0"),
 ('CHEVRON_SYNFLUID_PAO_2', 'DL2-14991.pdf', 'Version 1.9, Revision Date 2016-05-31, SDS 100000010948; 48 pages (multi-country annexes)', 'sections 2-3 and 9-11 (pp.2-7) in full; annex pages not read',
  'DL2-14990.pdf', 'MSDS # 3331, Revision Date April 2011 (the JSON takes KV40 5.1 and flash 159 from it; KV100, SG and pour from DL2-13192.pdf, December 2008, which prints KV40 5.0 and flash 164)', [('flash_point', 2, "Flash point : 160 C (320 F) Method: Cleveland Open Cup", "Flash Point (COC) 317 F (159 C) [2011]; 327 F (164 C) [2008]")], [],
  "Section 2: Aspiration hazard Category 1, H304; Acute toxicity Category 4, H332 (harmful if inhaled; LC50 1,17 mg/l, 4 h, rat). Section 3: '1-Decene, Dimer, Hydrogenated', CAS 68649-11-6. Section 9: autoignition 324 C; freezing point -73 C (not a pour point); boiling 223 C; vapour pressure 1,00 mmHg at 75 C; relative density 0,8 at 15,6 C; density 795,7 g/l (no temperature)",
  "KV -40 C 260 cSt [2011] / 255 cSt [2008]; fire point 178 C [2011] / 176 C [2008]; density 6.646 lb/gal; TAN < 0.03; bromine index < 200; colour 0; max handling 65 C"),
]
for pid, sds, ver, scope, tds, tdsd, confl, alts, sdsonly, tdsunc in D:
    orv = f're-read manually: {tds} ({tdsd}) whole page {T}'
    cov = (f"assessed by reading (2026-11-13, thirteenth pass) for {scope}: CPChem SAFETY DATA SHEET ({ver}). Compared with the JSON (cited data sheet {tds}): "
           + ('conflicting SDS values: ' + '; '.join(f'{c[0]} SDS {c[2]!r} vs data sheet {c[3]!r}' for c in confl) + ' (conflict rows). ' if confl else '')
           + ('method-unstated SDS values: ' + '; '.join(f'{a[0]} {a[2]!r}' for a in alts) + ' (alternate-entry rows). ' if alts else '')
           + f"SDS-only information (new-source evidence, mostly no template field; note row): {sdsonly}. Uncaptured items of the cited data sheet itself (old-source information, no template field): {tdsunc}. SDS values carry no statistical basis.")
    links.append(dict(p=pid, f=sds, cat='A', status='completed', fields_status=f'{scope} (text layer); compared value by value with the JSON and the cited data sheet {T}', coverage=cov,
                      identity=f"exact: product name on every page; SHA-256 equal to the archive file {sds}", note='Byte duplicate of an archive SDS; cited in the record only for the specific-gravity / flash alternate entries (or not at all).'))
    for path, tier, sp, tp in confl:
        F.append(dict(p=pid, tier=tier, path=path, old=f'{tds} ({tdsd}): {tp}. JSON equals the data sheet.', new_f=sds, new_p=5 if pid != 'CHEVRON_SYNFLUID_PAO_2' else 6, new_text=f"'{sp}' (SDS section 9, {ver.split(';')[0]})", unit='C' if 'flash' in path else 'cSt',
                      form=SDSU, qual='SDS reported value', method='Cleveland Open Cup / ASTM D-92 as printed' if 'flash' in path else 'not printed', cond='', basis='', outcome='changed_or_conflicting', action='propose_record_conflict',
                      reason='The SDS prints a different value' + (' by the same open-cup method' if 'flash' in path and 'Cleveland' in sp or 'D-92' in sp else '') + ' than the cited data sheet. Propose recording the conflict with both sources, dates and methods; the SDS value keeps its class (statistical basis unspecified) and is not promoted; JSON unchanged; not averaged.',
                      old_rev=orv, cmp_override=f'existing: {tp}'))
    for path, tier, sp, tp in alts:
        F.append(dict(p=pid, tier=tier, path=path, old=f'{tds}: {tp}. JSON equals the data sheet.', new_f=sds, new_p=4, new_text=f"'{sp}'", unit='C', form=SDSU, qual='SDS reported value (method not printed)', method='not printed', cond='', basis='',
                      outcome='additional', action='propose_alternate_entry', reason='The SDS flash point has no printed method, so it is not compared with the COC value as a conflict; propose an alternate entry attributed to the SDS with its class; the COC value stays selected.', old_rev=orv, cmp_override=f'existing: {tp}'))
    F.append(dict(p=pid, tier=1, path='open_questions', old=f'{tds} prints items the JSON does not record: {tdsunc}.', new_f=sds, new_p=3, new_text=sdsonly, unit='as printed', form=f'{SDSU}; SDS composition and hazard statements', qual='SDS reported value', method='as printed', cond='', basis='',
                  outcome='additional', action='propose_note',
                  reason='No template field holds these. Propose preserving them in a note, keeping two groups apart: (a) uncaptured items of the cited data sheet (old-source information) and (b) SDS-only information (new-source evidence, statistical basis unspecified); nothing is mapped to another field (e.g. freezing point is not a pour point).',
                  old_rev=orv, cmp_override='existing: not recorded'))
links.append(dict(p='CHEVRON_SYNFLUID_MPAO_100', f='DL2-14992.pdf', cat='A', status='completed', fields_status=f'full text compared with DL2-11906.PDF: identical extracted text (16,356 characters) {T}',
                  coverage='assessed by reading (2026-11-13, thirteenth pass): same SDS as DL2-11906.PDF (identical extracted text, different bytes); see that link and its rows (not duplicated here).', identity='identical text to DL2-11906.PDF'))
links.append(dict(p='CHEVRON_SYNFLUID_MPAO_65', f='DL2-15009.pdf', cat='A', status='completed', fields_status=f'whole page read; text identical to the cited DL2-11910.pdf (January 2014) {T}',
                  coverage="assessed by reading (2026-11-13, thirteenth pass): the cited data sheet itself (identical text to DL2-11910.pdf). Every typical captured (KV100 65, KV40 605, VI 181, pour -46, flash COC '>511 F (266 C)' captured as '>' 266, SG 0.846). Not captured (old-source information, no template field): max handling 82 C, density 7.060 lb/gal, bromine index < 400, colour Pt-Co 0 - listed in the DL2-11908.PDF note row.", identity="exact: 'Synfluid mPAO 65 cSt'"))
d = dict(batch='never-cited duplicates, batch 1: Synfluid SDS (thirteenth pass)', reviewed_on='2026-11-13 (thirteenth pass)',
         note='Nine never-cited duplicate links (eight documents). SDS sections 2-3 and 9 read in full against the JSON and the cited data sheets (read in the original). SDS values keep the class "SDS reported value; statistical basis unspecified".',
         documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzz_b1_synfluid_thirteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
