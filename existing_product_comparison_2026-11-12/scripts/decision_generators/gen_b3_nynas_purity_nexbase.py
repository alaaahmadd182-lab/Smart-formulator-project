"""Thirteenth pass, batch 3: never-cited duplicates of Nynas S 3B / NS 3 / Nyfrost 32, Neste NEXBASE 3020 and
Petro-Canada PURITY L50. Writes decisions/zzzzzzzzzzzzz_b3_nynas_purity_nexbase_thirteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = '(thirteenth pass, 2026-11-13)'
SDSU = 'SDS reported value; statistical basis unspecified'
links, F = [], []


def link(pid, f, scope, cov, ident, note=''):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{scope} {T}', coverage=f'assessed by reading (2026-11-13, thirteenth pass) for {scope}: {cov}', identity=ident, note=note))


def row(**k):
    base = dict(unit='as printed', method='as printed', cond='', basis='', cmp_override='existing: not recorded')
    base.update(k)
    F.append(base)


# ---------------- NYNAS S 3B ----------------
o = 're-read manually: DL2-12819.pdf (NYNAS S 3B product data sheet, issuing date 2019-05-29) pp.1-2 whole text (thirteenth pass, 2026-11-13)'
link('NYNAS_S_3B', 'DL2-13379.pdf',
     'SDS pp.1-13 (sections 1-16) text layer read in full; p.8 (section 9) also viewed as an image because the text layer separates labels from values; pp.14-36 (exposure-scenario annex) identified by their headings only, not compared',
     "Nynas SDS version 2, 2019-08-20 (previous issue 2019-05-20). Section 9 (verified on the image): melting/freezing point '<-60°C', initial boiling point '>200°C', flash 'Closed cup: >100°C [Pensky-Martens.]', density '0,86 g/cm³ [15°C]', log Kow '>4', auto-ignition '>200°C', decomposition '>270°C', 'Kinematic (40°C): 0,03 cm2/s (3 cSt)'. The JSON open questions already compare KV40, flash and density with the data sheet. Not recorded: identity statement CAS 64742-46-7 'Distillates (petroleum), hydrotreated middle' 100 % (preserved beside the data sheet's 'hydrotreated naphthenic' / API Group V description; not treated as a conflict); classification Acute Tox. 4 H332, Skin Irrit. 2 H315, Asp. Tox. 1 H304, Aquatic Chronic 2 H411, 'Danger' (expert judgment); Nota N; DNELs; UN3082 environmentally hazardous; Seveso E2; storage class 10. -> note row. The cited data sheet itself has uncaptured items, incl. 'Aromatic Content Wt % UOP 495 <1.0' while the aromatics field is Missing -> capture row.",
     "exact: 'NYNAS® S 3B' on every page")
row(p='NYNAS_S_3B', tier=1, path='open_questions', old='Not in the cited data sheet (SDS-only information); the data sheet describes a hydrotreated naphthenic base oil, API Group V.', new_f='DL2-13379.pdf', new_p=3,
    new_text="Section 3: 'Distillates (petroleum), hydrotreated middle EC: 265-148-2 CAS: 64742-46-7 100 Acute Tox. 4, H332 Skin Irrit. 2, H315 Asp. Tox. 1, H304 Aquatic Chronic 2, H411'; 'Nota N applies'. Section 2: signal word 'Danger'. Section 9: melting/freezing point <-60°C (not a pour point), boiling >200°C, auto-ignition >200°C, decomposition >270°C, log Kow >4. Section 8: DNEL long-term inhalation 16,4 mg/m³, dermal 2,91 mg/kg bw/day (workers). Sections 14-15: UN3082 class 9 PG III; Seveso E2; storage class (TRGS 510) 10.",
    form=f'{SDSU}; SDS identity and classification statements', qual='SDS reported value', outcome='additional', action='propose_note',
    reason="New-source evidence without a template field. Both descriptions are preserved as printed: the SDS registration identity (CAS 64742-46-7, 'Distillates (petroleum), hydrotreated middle') and the data sheet's 'hydrotreated naphthenic' / API Group V description. They are not inherently contradictory (a distillate-range registration name and a hydrocarbon-type description can apply to the same oil), so no conflict is claimed and neither is used to change api_group_chemistry. Freezing point is not mapped to pour point.",
    old_rev=o, cmp_override='existing: KV40 / flash / density comparisons recorded; identity and classification not recorded')
row(p='NYNAS_S_3B', tier=3, path='aromatics', old="DL2-12819.pdf p.2 prints 'Aromatic Content Wt % UOP 495 <1.0' (typical data column; no specification limit). The JSON aromatics field is Missing.", new_f='DL2-12819.pdf', new_p=2,
    new_text="'Aromatic Content | Wt % | UOP 495 | | | <1.0'", unit='wt %', form='typical data (data-sheet TYPICAL DATA column; upper bound as printed)', qual='<', method='UOP 495', basis='wt %',
    outcome='in_old_source_not_captured', action='capture_from_old_source',
    reason="Old-source value never captured. Propose recording '<1.0' wt % (UOP 495) as printed with qualifier '<'. The IR-method CA 1.6 % and ASTM D2140 CA <1 / CN 59 / CP 41 % are carbon-type percentages, not aromatic content by mass, and are not used for this field (kept in the note row).",
    old_rev=o, cmp_override='existing: Missing')
row(p='NYNAS_S_3B', tier=1, path='open_questions', old="DL2-12819.pdf p.2 also prints: Viscosity 20°C 5.25 mm²/s (D 445); 100°F 36.1 SUS (D 2161); copper strip 3 hrs 1 (max 1); aniline point 68-76, typical 72 °C (D 611); refractive index 20 °C 1.466 (D 1747); colour Saybolt min +20, typical +30 (D 156); D 1500 <0.5; TAN max 0.03, typical <0.01 (D 974); IR-method CA 1.6 %; ASTM D2140* (modified) CA <1, CN 59, CP 41 %; distillation D86 IBP 242, FBP 278 °C; IP 346 'NA**'; footnotes on EU 2015/326 PAH limits and US FDA 178.3620 (B).", new_f='DL2-12819.pdf', new_p=2,
    new_text='(cited data sheet; items listed in the old-source statement)', form='typical data and specification limits as printed (data sheet)', qual='as printed', outcome='in_old_source_not_captured', action='propose_note',
    reason='Old-source information without a template field. Propose preserving it with methods, edition (2019-05-29) and footnotes; carbon-type percentages stay distinct from aromatic content.', old_rev=o)

# ---------------- NYNAS NS 3 ----------------
o = 're-read manually: DL2-15474.pdf (NYNAS NS 3 product data sheet, issuing date 30-05-2024) pp.1-2 whole text (thirteenth pass, 2026-11-13)'
link('NYNAS_NS_3', 'DL2-12382.pdf', 'PDS pp.1-2 text layer read in full; p.2 table also viewed as an image (column layout)',
     "Nynas NS 3 product data sheet, issuing date 2016-11-01 (older edition of the cited 2024 sheet). KV40 2.84, density 0.860, PM flash 94, sulphur 30 ppm are already recorded as edition differences (conflicts marked resolved by edition supersession in the JSON; unchanged here). Limits equal in both editions (density 0.850-0.875, KV40 2.70-3.10, flash min 90, pour max -60, aniline 61-69, Saybolt min +15, TAN max 0.03). Present ONLY in the 2016 edition and not recorded: refractive index 20 °C 1.469 (D 1747) and IR-method CN 57 % / CP 37 % (the 2024 sheet prints only IR CA 6 %). Copper strip printed '3 hrs' (2016) vs '100°C, 3 hrs' (2024). -> note row.",
     "exact: 'NS 3' (2016 sheet title 'Nynas NS grades NS 3')")
row(p='NYNAS_NS_3', tier=1, path='open_questions', old="DL2-12382.pdf (2016-11-01) is cited only through the edition-difference conflicts; its refractive index and IR carbon-type rows are not recorded.", new_f='DL2-12382.pdf', new_p=2,
    new_text="2016 edition, TYPICAL DATA column: 'Refractive Index, 20 °C | D 1747 | 1.469'; 'Hydrocarbon Type Analysis | IR-method | CA % 6, CN % 57, CP % 37'; 'Carbon-Type Composition | D 2140 | CA/CN/CP NA'; 'Aniline Point °C D 611 61 69 65'; 'Copper Strip, 3 hrs D 130 1 1'; 'Viscosity, 100°F SUS D 2161 36'; 'DMSO extractible compounds Wt % IP 346 NA'. 2024 edition (DL2-15474.pdf p.2): IR-method 'Ca % 6' only; no refractive-index row; 'Copper Strip, 100°C, 3 hrs'.",
    form='typical data (2016 data-sheet edition) with methods as printed', qual='as printed', outcome='in_old_source_not_captured', action='propose_note',
    reason="Old-source information without a template field and absent from the newer edition. Propose preserving it attributed to the 2016 edition with its methods (D 1747 at 20 °C; IR method). IR carbon-type percentages are not aromatic content by mass and are not mapped to the aromatics field. The edition is identified, not preferred.",
    old_rev=o)

# ---------------- NYNAS NYFROST 32 ----------------
o = ("re-read manually: DL2-11510.pdf (NYFROST 32 product data sheet, issuing date 2016-11-01) p.2 whole table (thirteenth pass, 2026-11-13): "
     "KV40 28.8-35.2 / 32, PM flash min 174 / 176, COC 190, pour max -30 / -45, density 0.896-0.916 / 0.905; also DL2-13444.pdf pp.6-7 page assignment "
     "checked in the text layer and on the p.7 image")
link('NYNAS_NYFROST_32', 'DL2-13444.pdf', 'SDS pp.1-3 and 6-8 (sections 1-11.1) text layer read in full; p.7 (section 9) also viewed as an image; pp.4-5, 9-12 not read',
     "Nynas SDS version 3.01, 2020-05-23. Section 9 is on p.7 (p.6 holds sections 7-8): KV40 'Kinematic (40°C): 0,31 cm2/s (31 cSt)' and flash 'Closed cup: >180°C [Pensky-Martens.]' are in the two unresolved conflicts, which cite 'p.6' -> citation-correction row. Not recorded: melting/freezing point -39°C (not a pour point; data-sheet pour typical -45), boiling >250°C, auto-ignition >270°C, decomposition >280°C, vapour pressure <0,01 kPa, log Kow 2 to 6, density 0,9 g/cm³ [15°C], 'DMSO extractable compounds ... IP346 < 3%'; CAS 64742-52-5 hydrotreated heavy naphthenic 100 %, not classified, Nota L. -> note row.",
     "exact: 'NYFROST™ 32'")
row(p='NYNAS_NYFROST_32', tier=1, path='conflicts', old="Conflict entries for kv40 and flash_point cite 'source_b': 'DL2-13444.pdf p.6 (2020-05-23)' in the tier-1, tier-2 and tier-3 files.", new_f='DL2-13444.pdf', new_p=7,
    new_text="p.7 (footer '7/12'): 'SECTION 9 ... Flash point Closed cup: >180°C [Pensky-Martens.] ... Viscosity Kinematic (40°C): 0,31 cm2/s (31 cSt)'. p.6 contains sections 7 and 8 only.",
    form=f'{SDSU}; citation page reference', qual='SDS reported value', method='', outcome='changed_or_conflicting', action='propose_citation_correction',
    reason="Citation error: the SDS values are printed on p.7, not p.6. Propose correcting the page reference in both conflict entries (all three tier files). Values, sources and the unresolved status stay unchanged; production JSON is not edited here.",
    old_rev=o, cmp_override="existing: 'DL2-13444.pdf p.6'")
row(p='NYNAS_NYFROST_32', tier=1, path='open_questions', old='Not in the cited data sheet (SDS-only information).', new_f='DL2-13444.pdf', new_p=7,
    new_text="Section 9: melting/freezing point -39°C; initial boiling point >250°C; vapour pressure (calculated) <0,01 kPa [room temperature]; density 0,9 g/cm³ [15°C]; log Kow 2 to 6; auto-ignition >270°C; decomposition >280°C; DMSO extractable compounds (IP346) < 3%. Sections 2-3: CAS 64742-52-5 'Distillates (petroleum), hydrotreated heavy naphthenic' 100 %, 'Not classified', 'No signal word', Nota L.",
    form=f'{SDSU}; SDS identity and classification statements', qual='SDS reported value', outcome='additional', action='propose_note',
    reason='New-source evidence without a template field; preserved attributed to the SDS. The freezing point is a different property from the data-sheet pour point and is not compared with it as a conflict.', old_rev=o)

row(p='NYNAS_NYFROST_32', tier=1, path='open_questions', old="DL2-11510.pdf (2016-11-01) p.2 prints items the JSON does not record: Colour D 1500 max 1, typical 0.5; Floc point R12 (DIN 51351) -36 °C; Floc point R600A (DIN 51351) -50 °C (R22 / ASHRAE 86 and U-tube cold flow DIN 51568 rows blank); Copper strip 100 °C 3 hrs max 1 / 1; Neutralization value max 0.03 / <0.01 mg KOH/g (D 974); IR-method CA 15 %; Carbon-type composition CA 10 / CN 42 / CP 48 %; Breakdown voltage (IEC 156) min 40 / >45 kV; 'Nyfrost 32 is a naphthenic based refrigerating oil meeting specification BS 2626:1992'.",
    new_f='DL2-11510.pdf', new_p=2, new_text='(cited data sheet; items listed in the old-source statement)', form='typical data and specification limits as printed (data sheet)', qual='as printed',
    outcome='in_old_source_not_captured', action='propose_note',
    reason='Old-source information without a template field. Propose preserving it with methods and the BS 2626:1992 statement; carbon-type percentages are not aromatic content by mass and are not mapped to the aromatics field.', old_rev=o)

# ---------------- NESTE NEXBASE 3020 ----------------
o = 're-read manually: DL2-14513.pdf (NEXBASE 3020 SDS, revision 16/06/2020, 106 pages) pp.1-9 compared page by page (thirteenth pass, 2026-11-13); pp.10-106 not read'
link('NESTE_NEXBASE_3020', 'DL2-14514.pdf', 'SDS pp.1-9 text layer read in full and compared page by page with the cited DL2-14513.pdf',
     "DL2-14514.pdf is a 9-page file whose pages 1-9 are text-identical to pages 1-9 of the cited 106-page DL2-14513.pdf (same revision 16/06/2020; footers read '1/106' ... '9/106'). It is therefore a PARTIAL copy: it does not contain DL2-14513 pp.10-106 (not read in this pass), so the two complete documents are not equivalent. Section 9 values (pour '≤ -42°C (ASTM D-97)', flash '> 150°C (ASTM D-93)', KV40 'typical value 7,5 mm2/s', relative density '0,82 @ 15°C') are already in the JSON as alternate entries / specific_gravity from DL2-14513. Not recorded: CAS 72623-86-0 100 %, Asp. Tox. 1 H304 'Danger', 'DMSO < 3% (IP 346)', boiling range 270-380°C, vapour pressure < 0,1 hPa @ 20°C, log Kow > 6, dynamic viscosity ~12 mPa s @ +20°C and ~50 mPa s @ -8°C, oil-mist limits. -> note row.",
     "exact: 'NEXBASE™ 3020' on every page", note='Partial copy (first 9 of 106 pages) of the cited SDS; not a complete duplicate.')
row(p='NESTE_NEXBASE_3020', tier=1, path='open_questions', old='Not in the cited data sheet DL2-10962.pdf; the cited SDS DL2-14513.pdf contains the same text on pp.1-9.', new_f='DL2-14514.pdf', new_p=5,
    new_text="p.2: 'Lubricating oils (petroleum), C15-30, hydrotreated neutral oil-based 100 % CAS number: 72623-86-0 ... Asp. Tox. 1 - H304'; 'DMSO < 3% (IP 346)'. p.4-5: 'Initial boiling point and range 270-380°C'; 'Vapour pressure < 0,1 hPa @ 20°C'; 'log Kow: > 6'; 'Dynamic viscosity ~ 12 mPa s @ +20°C'; 'Dynamic viscosity ~ 50 mPa s @ - 8°C'. p.4: oil mist 5 mg/m3 (8h) HTP 2018/FIN; DNEL workers inhalation 5,4 mg/m³.",
    form=f'{SDSU}; SDS identity, classification and physical statements', qual='SDS reported value (dynamic viscosities printed as approximate)', outcome='additional', action='propose_note',
    reason="New-source evidence without a template field (the dynamic viscosities are approximate '~' values at temperatures with no template field). Preserve attributed to the SDS revision 16/06/2020 with a statement that DL2-14514.pdf is a 9-page partial copy of DL2-14513.pdf.", old_rev=o)

# ---------------- PETRO-CANADA PURITY L50 ----------------
o = 're-read manually: DL2-10020.pdf (Petro-Canada PURITY brochure LUB3213E (2015.07)) p.2 L50 column whole table (thirteenth pass, 2026-11-13)'
link('PETRO_CANADA_PURITY_L50', 'DL2-13351.pdf', 'PDS p.1 (only page) text layer read in full and viewed as an image (SPECIFICATION / TYPICAL VALUE columns)',
     "Petro-Canada 'Product Data Sheet - PURITY L50 BASE OIL', 'Last Reviewed: May 2020'. The JSON mentions this file only for 'prints no CCS'; none of its values or limits is recorded. Typicals differ from the cited 2015.07 brochure (density 0.853 vs 0.85; KV40 5.5 vs 5.2; KV100 1.78 vs 1.7; SUS 45 vs 44; COC 152 vs 151; PM 142 vs 147; pour -12 vs -6). It also prints specification limits (KV40 4.5-6.5; COC 140 min; PM 120 min; pour -3 max; colour 0.5 max) and the footnotes 'The above values represent typical production data, and may not appear on a Certificate of Analysis', 'Expiry Date: Product properties should be reconfirmed if over 5 years old', 'This is not a controlled document', SAP code PL50. -> conflict / alternate / note rows; no edition is preferred.",
     "exact: 'Product Data Sheet - PURITY L50 BASE OIL'")
FOOT = "PDS footnote: 'The above values represent typical production data, and may not appear on a Certificate of Analysis.'"
for tier, path, b15, p20, spec, unit, meth in [
        (1, 'kv40', "'VISCOSITY @ 40°C, cSt D445 ... 5.2' (L50 column)", "'Kinematic Viscosity, cSt @ 40°C | D445 | 4.5-6.5 | 5.5'", 'specification 4.5-6.5', 'cSt', 'D445'),
        (1, 'kv100', "'@ 100°C, cSt D445 ... 1.7'", "'Kinematic Viscosity, cSt @ 100°C | D445 | Report | 1.78'", "specification 'Report'", 'cSt', 'D445'),
        (2, 'pour_point', "'Pour Point, °C (°F) D5950 ... -6 (21)'", "'Pour Point, °C (°F) | D5950 | -3 max | -12'", 'specification -3 max', '°C', 'D5950'),
        (2, 'flash_point', "'Flash Point, COC, °C (°F) D92 ... 151 (304)'", "'Flash Point, COC °C (°F) | D92 | 140 min | 152'", 'specification 140 min', '°C', 'D92 (COC)')]:
    row(p='PETRO_CANADA_PURITY_L50', tier=tier, path=path, old=f"DL2-10020.pdf (2015.07) p.2: {b15}. JSON equals the brochure.", new_f='DL2-13351.pdf', new_p=1, new_text=f"{p20} (Last Reviewed: May 2020)", unit=unit,
        form=f'typical value (PDS TYPICAL VALUE column) with {spec} (SPECIFICATION column); {FOOT}', qual='as printed', method=meth, outcome='changed_or_conflicting', action='propose_record_conflict',
        reason=f"The May 2020 data sheet prints a different typical than the 2015 brochure, plus a {spec}. Propose recording an edition difference with both documents and dates, and the specification limit as a separately labelled entry. Not averaged; neither edition is preferred by date alone; the JSON conflicts with the 2023.03 web brochure stay as recorded.",
        old_rev=o, cmp_override='existing: 2015 brochure value; this PDS not recorded')
row(p='PETRO_CANADA_PURITY_L50', tier=1, path='density', old="DL2-10020.pdf (2015.07) p.2: 'Density @ 15°C, kg/L D4052 ... 0.85'. JSON equals the brochure.", new_f='DL2-13351.pdf', new_p=1, new_text="'Density, kg/L @ 15°C | D4052 | Report | 0.853'", unit='kg/L',
    form=f"typical value (PDS TYPICAL VALUE column); specification 'Report'; {FOOT}", qual='as printed', method='D4052', cond='15 °C', outcome='additional', action='propose_alternate_entry',
    reason='0.853 is consistent with the brochure 0.85 at the brochure precision (two decimals), so it is not recorded as a conflict; propose an alternate entry attributed to the May 2020 PDS with its three decimals.', old_rev=o, cmp_override='existing: 0.85 (2015 brochure)')
row(p='PETRO_CANADA_PURITY_L50', tier=2, path='flash_point', old="DL2-10020.pdf (2015.07) p.2 also prints 'Flash Point, PM, °C (°F) D93 ... 147 (297)' for L50; the JSON records only the COC value.", new_f='DL2-13351.pdf', new_p=1,
    new_text="'Flash Point, PM °C (°F) | D93 | 120 min | 142'", unit='°C', form=f'typical value (PDS) with specification 120 min; {FOOT}', qual='as printed', method='D93 (Pensky-Martens)', outcome='additional', action='propose_alternate_entry',
    reason='A different method (PM, D93) from the selected COC value: propose alternate entries for PM 142 (May 2020 PDS, min 120) and PM 147 (2015 brochure, never captured); the two PM typicals differ and are recorded side by side, not resolved.', old_rev=o, cmp_override='existing: COC 151 only')
row(p='PETRO_CANADA_PURITY_L50', tier=1, path='open_questions', old="DL2-10020.pdf (2015.07) p.2 L50 column also prints 'SUS @ 100°F D2161 44' and 'Colour, ASTM D1500 <0.5' (not recorded).", new_f='DL2-13351.pdf', new_p=1,
    new_text="'Saybolt Universal Viscosity, sus at 1[00°F] | D2161 | Report | 45'; 'Colour, ASTM | ASTM D1500 | 0.5 max | <0.5'; 'Appearance | LORM 004 | Clear & Bright | Clear & Bright'; 'The above values represent typical production data, and may not appear on a Certificate of Analysis.'; '- Expiry Date: Product properties should be reconfirmed if over 5 years old.'; 'SAP Material Order Code: PL50'; 'Last Reviewed: May 2020'; 'Note: This is not a controlled document'.",
    form='typical values, specification limits and footnotes as printed (PDS)', qual='as printed', outcome='in_old_source_not_captured', action='propose_note',
    reason="Items without a template field (SUS, colour, appearance) and the PDS qualifying footnotes. Propose preserving them; the SUS label is truncated on the page ('sus at 1') and is quoted as printed. The 'not a controlled document' and 5-year expiry statements are recorded with the values they qualify.", old_rev=o)

d = dict(batch='never-cited duplicates, batch 3: Nynas, Neste, Petro-Canada (thirteenth pass)', reviewed_on='2026-11-13 (thirteenth pass)',
         note='Five never-cited duplicate links. Tables whose meaning depends on layout were viewed as images (S 3B and Nyfrost 32 SDS section 9, NS 3 2016 table, PURITY L50 table).',
         documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzz_b3_nynas_purity_nexbase_thirteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
