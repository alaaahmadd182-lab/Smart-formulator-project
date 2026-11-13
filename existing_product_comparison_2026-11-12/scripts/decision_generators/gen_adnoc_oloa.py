# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
links, F = [], []


def L(p, f, cat, fs, cov, idn, note=''):
    links.append(dict(p=p, f=f, cat=cat, status='completed', fields_status=fs, coverage=cov, identity=idn, note=note))


def R(p, tier, path, old, nf, np_, nt, unit, form, act, reason, orv, cmp, outc='additional', qual='', meth='', cond='', basis='', ov=''):
    d = dict(p=p, tier=tier, path=path, old=old, new_f=nf, new_p=np_, new_text=nt, unit=unit, form=form, qual=qual, method=meth, cond=cond, basis=basis, outcome=outc, action=act, reason=reason, old_rev=orv, cmp_override=cmp)
    if ov:
        d['overlap_reviewed'] = ov
    F.append(d)


for g in ('2CST', '3CST', '4CST', '6CST', '8CST'):
    L('ADNOC_ADBASE_' + g, 'DL2-12151.pdf', 'B', 'all 10 pages read (text layer); p.5 compared word by word with the cited DL2-12221.pdf (ratio 1.000)',
      "p.5 is the cited specification spread (pp.6-7) word for word: every value of the column is already in the JSON. Other pages: company profile, process (ATIEL Code of Practice, ISO 9001:2015), consistency charts for 4 and 6 cSt (no values), 'Product formulation approvals' for the ADbase family (Part A approved; Parts B and C 'Testing under progress'; no per-grade data and no template field), sellers. Nothing proposed.",
      f"exact: column 'ADbase {g}' (ADNOC brochure)", 'The full ADNOC brochure that contains the cited spread.')
O66 = 'DL2-12453.pdf'
for f, extra in (('DL2-12453.pdf', ''), ('DL2-12452.pdf', ' Same extracted text as DL2-12453.pdf (21,166 characters, identical; different bytes): the field rows cite DL2-12453.pdf.')):
    L('CHEVRON_OLOA_59766', f, 'E', 'slides 1-9, 12, 13, 17, 20, 21, 24, 30, 31, 37 read (text layer); slides 4 and 24 as images; other slides concern OLOA 59770 / 59767 / 59762',
      'compared with the JSON (SDS DL2-11731.pdf only): new claims cascade, treat rates by claim and grade, booster routes, STM/BOI base-oil criteria, VII and PPD, five formulations and the package BN 90; the JSON treat rate 11.2 wt% (SDS) equals the main CI-4 / E7-16 rate',
      "exact: 'OLOA 59766' (Chevron Oronite 'HDEO Cascade', January 2018)", 'Manufacturer presentation; PCMO items marked \'on going\' are not claims.' + extra)
L('CHEVRON_OLOA_59766', 'DL2-11806.pdf', 'C', 'whole page read (text layer)', "OLOA 59770 bulletin (July 11, 2018): '... linked with booster to OLOA 59766 & OLOA 59762'; no OLOA 59766 value; NOT ASSESSED further", "printed 'OLOA 59766' in another product's bulletin")
L('CHEVRON_OLOA_61003', 'DL2-11576.pdf', 'F,E', 'both pages read and compared word by word with the cited DL2-11032.pdf',
  "edition 'Version 1, 13 May, 2009, For GULF' of the cited bulletin (8 January 2009): every claim, the dosage 18.4 mass % and every typical property are identical; differences: date, the heading 'For GULF' and the VI improver 'GA 2140' (cited edition: 'PARATONE 8006')", "exact: 'OLOA 61003'", 'Customer edition; see the co-component row.')
OR = 're-read manually: DL2-11731.pdf (SDS, 2017-01-24) as quoted in the JSON printed_text; the JSON open question states only an SDS is in the archive'
R('CHEVRON_OLOA_59766', 1, 'performance_claims', 'SDS: no claims. JSON performance_claims Missing.', O66, 4,
  "Slide 4 'Cascade Summary' (image checked): OLOA 59766 alone - 11.2 wt%: CI-4 / E7-16; SL, A3/B4-16; VDS3, Cat ECF-1a; 15W-40 20W-50 10W-40 10W-30 (finished BN 10.1); 9.33 wt%: CG-4 (CI-4 in GpII), E7-08; SJ, A3-B3/16; MB 228.3, MAN 3275, MB 229.1; 15W-40 20W-50, 10W-40 (PCMO) (BN 8.4); 8.2 wt%: CF-4, E2; MB 228.1, MAN 271; 15W-40 (BN 7.4); 7.0 wt%: CF-4 multigrade (BN 6.3). With boost: 12.9 wt% CI-4 / E7-16, SL A3/B4-16, Cat ECF-2 (BN 10.4); 15.4 wt% CI-4 / E4-16 / E7-16, MB 228.5, MAN 3277, 10W-40 (BN 12). Slide 13: claims at 11.2 wt% SAE 15W-40 (Gp I & Gp II) incl. GLOBAL DHD-1, MTU Type 2, MAN M3275-1, Renault RLD-2, Mack EO-N/EO-M Plus, Cummins CES 20078, DDC 93K215, Deutz DQC III-10, JASO DH-1 level, Allison C4 level; 'PCMO on going'. Slide 24: claims per formulation column, 'Levels' listed separately.",
  '', 'claims (manufacturer presentation, January 2018)', 'propose_add_route_bound',
  "Propose adding the claims, each bound to its treat rate, grade and base-oil route as printed; booster routes kept separate from OLOA 59766 alone; items marked 'level', 'on going' or 'Performance Potential (may vary with base oils)' are recorded with that wording, not as approvals.",
  OR, 'existing: performance_claims Missing')
R('CHEVRON_OLOA_59766', 1, 'treat_rate_matrix', "DL2-11731.pdf p.8: 'prescribed treatment rate of: 11.2 wt. %' (no claim or grade). JSON one row 11.2 wt%.", O66, 4,
  "Slide 4 rates 11.2 / 9.33 / 8.2 / 7.0 wt% (OLOA 59766 alone) and 12.9 / 15.4 wt% ('59766 + Boost'); slide 8 '11.2wt% + OLOA 65770 @ 1.7wt%' (= 12.9, Full OEM profile, Cat ECF-2); slides 30-31 'Downtreats' (package BN 90): CI-4/CH-4/SL 15W-40 11.2; CG-4 9.33; CF-4 multigrade 7.0; SG level 8.4; SJ/CG-4 9.33; SJ/CH-4 11.2; SG/CF-4 8.4; SG/CF 8.6; SF/CF 8.6; SF/CC 8.3; API CF 8.6; SE/CC and SD/CC 6.3 (mono) / 6.9 (multi); SC/CC and SC/CB 3.0 / 3.4; SB/CB 2.4 / 2.7.",
  'wt%', 'recommended treat rates (manufacturer presentation, January 2018)', 'propose_add_route_bound',
  "The existing 11.2 wt% equals the main CI-4 / E7-16 rate; propose binding it to that claim and grade route and adding the other rows each with its claim and grade. The 15.4 wt% booster is not named on slide 4; it is recorded as '59766 + Boost' without inferring the booster. Mass basis printed ('wt%').",
  OR, 'existing: 11.2 wt% without claim or grade', basis='mass (printed wt%)')
R('CHEVRON_OLOA_59766', 1, 'route_selector_restrictions', 'SDS: none. JSON route_selector_restrictions Missing.', O66, 21,
  "Slide 21 'OLOA 59766 - STM/BOI, Group I and Group II base oil characteristics range': Saturates 75 - 98 %; Sulfur 0.00 - 0.47 wt%; Base Oil KV 100 5,8 (grp II) / 6.3 (grp I) - 8.0 cSt; finished oil VI 91 - 115; NOACK 5 - 11 %; 'Applicable with PARATONE 8006E viscosity index improver.' Slide 20: 15W-40 (GP I & GP II); 10W-40*, 10W-30*, 20W-50 (GP II, III); '*may require formulation adjustment such as alternate Group III content; this may then requires additional engine tests'. Slide 37: 'SL with OLOA 59766 @ 9,33% require 0,2% Anti-Oxidant (DPA) to pass Sequence IIIF'.",
  'as printed', 'manufacturer STM/BOI criteria (presentation, January 2018)', 'propose_add',
  'Propose recording the printed STM/BOI ranges as route limits (base-oil saturates, sulfur, KV100; finished-oil VI and Noack), the VII condition and the two printed formulation conditions; ranges kept as ranges; not generalised beyond STM/BOI claims.',
  OR, 'existing: Missing')
R('CHEVRON_OLOA_59766', 1, 'required_co_components', 'SDS: none. JSON required_co_components Missing.', O66, 24,
  "Slide 24 formulations: 'PARATONE 8006E 8,10% / 6,30% / 8,10% / 8,50% / 10,30%'; 'PPD (OLOA 19803) 0,50% / 0,30% / 0,30% / 0,30% / 0,30%'; slide 21 'Applicable with PARATONE 8006E viscosity index improver.'",
  'wt%', 'components of manufacturer formulations (presentation, January 2018)', 'propose_add_route_bound',
  'Propose recording PARATONE 8006E (VII) and OLOA 19803 (PPD) with their doses per formulation, bound to the STM/BOI route and the five formulations; not universal co-components.',
  OR, 'existing: Missing', cond='OLOA 59766 at 11.2 wt%, formulations OR-F 62616D-A, 70588O-A, 56515D-I, 67741D-A, 67742F-A; STM/BOI route')
R('CHEVRON_OLOA_59766', 1, 'published_formulations', 'SDS: none. JSON published_formulations Missing.', O66, 24,
  "Identity per formulation column (OR-F code; image checked): 62616D-A CVX 15W-40: OLOA 59766 11,20 / PARATONE 8006E 8,10 / PPD 0,50 / Chevron 220R 70,20 / Chevron 600R 10,00; 70588O-A CVX 20W-50: 11,20 / 6,30 / 0,30 / 220R 13,20 / 600R 69; 56515D-I XOM AP/E 15W-40: 11,20 / 8,10 / 0,30 / AP/E 150N 60,30 / AP/E 600N 20,10; 67741D-A XOM EHC 15W-40: 11,20 / 8,50 / 0,30 / EHC50 54 / EHC110 26; 67742F-A XOM EHC 10W-40: 11,20 / 10,30 / 0,30 / EHC50 69,90 / EHC120 8,30 (all '%'; each column adds to 100.0). Finished-oil KV100 / CCS / S. Ash / TBN and claims per column as printed.",
  '%', 'manufacturer formulations (presentation, January 2018)', 'propose_add_route_bound',
  'Propose adding the five formulations by OR-F code, each with its base-oil system, grade and the claims printed under it; finished-oil analyses stay with the formulation (not package properties). Decimal commas kept in printed_text.',
  OR, 'existing: Missing', basis='printed % (wt% per slide title)')
R('CHEVRON_OLOA_59766', 2, 'tbn', 'SDS: TBN not printed. JSON tbn Missing (open question).', O66, 30,
  "Slides 30 and 31 table heading: 'OLOA 59766 Package BN 90'", 'mg KOH/g (unit not printed)', 'typical package value (manufacturer presentation, January 2018; no method, no limits)', 'propose_add',
  "Propose adding the printed package BN 90 as a typical with this source and a note that no unit or method is printed (BN is conventionally mg KOH/g; not stated here). The finished-oil BNs are blend values and are not proposed.",
  OR, 'existing: tbn Missing', qual='typical', meth='not printed')
R('CHEVRON_OLOA_61003', 1, 'required_co_components', "DL2-11032.pdf (8 January 2009) read: 'VI Improver (VII) PARATONE 8006'. JSON: VII PARATONE 8006, dose not printed.", 'DL2-11576.pdf', 1,
  "'Dosage 18.4 mass % / VI Improver (VII) GA 2140' (edition 'Version 1, 13 May, 2009, For GULF')", '', 'co-component named in a customer edition of the bulletin', 'propose_add_route_bound',
  "Propose recording GA 2140 as the VII of the 'For GULF' edition only, alongside (not replacing) PARATONE 8006 of the general edition; no identity between the two is assumed.",
  're-read manually: DL2-11032.pdf both pages (text layer)', 'existing: PARATONE 8006', cond="bulletin edition 'For GULF', 13 May 2009")
d = dict(batch='ADNOC brochure; Chevron Oronite OLOA 59766 cascade deck and OLOA 61003 edition (tenth pass)', reviewed_on='2026-11-13 (tenth pass)',
         note='ADNOC: the full brochure containing the cited specification spread. Chevron: the January 2018 HDEO cascade presentation is the first manufacturer description of OLOA 59766 in the archive (the JSON rests on the SDS); both copies have identical text. OLOA 61003: customer edition of the cited bulletin.',
         documents={'DL2-12151.pdf': dict(what="ADNOC 'ADbase' brochure (10 pp.)", printed_date='not printed', kind='manufacturer brochure', read='all 10 pages (text layer)', limits='charts without values'),
                    'DL2-12453.pdf': dict(what="Chevron Oronite 'A versatile and complete HDEO Cascade: OLOA 59770, 59766, 59767, 59762' (40 slides)", printed_date='January 2018 (© 2018 Chevron)', kind='manufacturer presentation', read='slides 1-9, 12, 13, 17, 20, 21, 24, 30, 31, 37 (text layer); 4 and 24 as images', limits='slides on the other packages not reviewed'),
                    'DL2-12452.pdf': dict(what='copy of DL2-12453.pdf (identical extracted text, different bytes)', printed_date='January 2018', kind='manufacturer presentation', read='text compared in full with DL2-12453.pdf', limits='as DL2-12453.pdf'),
                    'DL2-11576.pdf': dict(what="Chevron Oronite OLOA 61003 bulletin 'Version 1, 13 May, 2009, For GULF'", printed_date='13 May 2009', kind='manufacturer bulletin (customer edition)', read='both pages (text layer)', limits='')},
         links=links, fields=F)
json.dump(d, open('existing_product_comparison_2026-11-12/decisions/zzzzzzzzzz_adnoc_oloa_tenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
