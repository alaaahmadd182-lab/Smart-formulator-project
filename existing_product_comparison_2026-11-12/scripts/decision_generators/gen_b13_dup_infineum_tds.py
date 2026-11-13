"""Fifteenth pass, batch 13: coverage of ten duplicate (category A) links to cited Infineum data sheets (1-2 pages each), read in
full against the JSON. Writes decisions/zzzzzzzzzzzzzzz_b13_dup_infineum_tds_fifteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'fifteenth pass, 2026-11-13'
links, F = [], []
FOOT = "footnotes '(a)Not a specification, (b)Methods typically used by Infineum manufacturing plants'"
# pid, file, pages, version, equal-summary, handling text (None = already proposed), extra uncaptured
D = [
 ('INFINEUM_D3320', 'DL2-12025.pdf', 1, 'Version: 6 February 2015 (1.0)', 'treat rates 13.7 (ACEA E6-12 / API CI-4, 10W-30 and 10W-40), BN 76, density 947, flash 189 (D93), KV100 175, KV40 3829, sulfated ash 7.2 (Calculated), sulfur 1.5 (D6443); mineral oil 48 % in the open questions',
  "Min Load/Unload Temp: 55 °C (131 ° F) Max Load/Unload Temp: 65 °C (149 ° F) Vis @ Min Load/Unload Temp: 1,450 cSt Vis @ Max Load/Unload Temp: 830 cSt Maximum Storage Temperature: 60 °C (140 ° F) Do not reheat above: 65 °C (149 ° F)", "Appearance 'Hazy brown viscous liquid' (ITM 50-022)"),
 ('INFINEUM_D3396', 'DL2-13383.pdf', 2, 'Version: 22 June 2018 (4.0)', "9.45 mass % for API CI-4 and API SL (10W-30, 15W-40, 20W-50; '~ 8.5 Volume %' recorded), BN 90, Ca 1.04, Mg 0.98, Zn 1.38, P 1.25, N 0.79, sulfated ash 10.0, KV40 3526, KV100 158, density 970, flash 188; lb/gal 8.08 in the open questions",
  "Min Load/Unload Temp: 55 °C (131 ° F) Max Load/Unload Temp: 65 °C (149 ° F) Vis @ Min Load/Unload Temp: 1,330 cSt Vis @ Max Load/Unload Temp: 750 cSt Maximum Storage Temperature: 60 °C (140 ° F) Do not reheat above: 65 °C (149 ° F)", "Appearance 'PASS Minimum' (ITM 50-022); 'Claims are base stock and viscosity grade specific.'"),
 ('INFINEUM_D3398', 'DL2-13348.pdf', 1, 'Version: 23 October 2018 (2.0)', '10.2 mass % API CI-4 (10W-30, 15W-40, 20W-50), BN 110, Ca 1.35, Mg 1.28, Zn 1.27, P 1.16, N 0.75, sulfated ash 12.8, KV40 3705, KV100 157, density 979, flash 188; lb/gal 8.15 in the open questions',
  "Min Load/Unload Temp: 55 °C (131 ° F) Max Load/Unload Temp: 65 °C (149 ° F) Vis @ Min Load/Unload Temp: 1,360 cSt Vis @ Max Load/Unload Temp: 770 cSt Maximum Storage Temperature: 65 °C (149 ° F) Do not reheat above: 65 °C (149 ° F)", "Appearance 'Pass'; 'Claims are base stock and viscosity grade specific.'"),
 ('INFINEUM_D3416', 'DL2-15333.pdf', 2, 'Version: 17 January 2024 (4.0)', 'all 11 performance rows (CI-4/SL 8.3 to SD/SC/CC 2.4, MONO / MULTI as printed), BN 101, Ca 1.18, Mg 1.12, Zn 1.57, P 1.42, N 0.81, sulfated ash 11.6 (Calculated), KV40 4534, KV100 176, density 984, flash 184',
  "(p.2) Min Load/Unload Temp: 55 °C (131 ° F) Max Load/Unload Temp: 65 °C (149 ° F) Vis @ Min Load/Unload Temp: 1,625 cSt Vis @ Max Load/Unload Temp: 900 cSt Maximum Storage Temperature: 60 °C (140 ° F) Do not reheat above: 65 °C (149 ° F)", "Appearance 'PASS'"),
 ('INFINEUM_D3417', 'DL2-15335.pdf', 1, 'Version: 10 March 2022 (1.0)', '8.6 mass % API CI-4 and API SL (10W-30, 15W-40), BN 106, KV40 3815, KV100 168, density 985, flash 185 (the elements are taken from the customer specification DL2-15334.pdf, whose targets equal these typicals)',
  "Min Load/Unload Temp: 55 °C (131 ° F) Max Load/Unload Temp: 65 °C (149 ° F) Vis @ Min Load/Unload Temp: 1,430 cSt Vis @ Max Load/Unload Temp: 810 cSt Maximum Storage Temperature: 60 °C (140 ° F) Do not reheat above: 65 °C (149 ° F)", "Appearance 'PASS'"),
 ('INFINEUM_D3417', 'DL2-15334.pdf', 1, "Customer specification 'Printed On : 12-Feb-2024' (customer 'Global - BRENNTAG GROUP')", 'Ca 1.15-1.37 / 1.26, Mg 1.10-1.28 / 1.19, N 0.71-0.87 / 0.79, P 1.26-1.48 / 1.37, Zn 1.39-1.63 / 1.51 (Min / Target / Max, as recorded); BN and KV100 "Test and report results" (in the open questions)',
  None, "'APPROVED ALTERNATE TEST METHODS' (Calcium ASTM D4927, D4951, D5185, D6443; Magnesium D4951, D5185, D6443; Phosphorus and Zinc D4927, D4951, D5185, D6443); 'APPEARANCE: Pass = Brown viscous liquid'; 'Recommended Retest Interval 24 Months'; 'Product Description HDD Detergent Inhibitor Package for API CI-4/SL Quality'"),
 ('INFINEUM_D3451', 'DL2-12029.pdf', 2, 'Version: 8 May 2017 (2.0)', "11.9 mass % API CI-4/SL / ACEA E7-12 (10W-30, 15W-40, 20W-50), 11.9 + Infineum D2367 at 1.2 % for API CH-4/SL / ACEA E7-12 10W-40, 11.0 API CH-4 15W-40; BN 77, Ca 0.89, Mg 0.84, Mo 0.042, N 0.70, P 1.08, S 2.65 (D4294), Zn 1.18, KV40 2985, KV100 146, density 960, flash 182; 'can be downtreated to meet API CG-4 and CF-4' in the open questions",
  "'This product is temperature sensitive. Do not heat over the maximum loading / unloading temperature to avoid possible release of extremely odorous alkyl mercaptans and/or toxic hydrogen sulfide.' Heating systems self-limiting at 120 Deg.C/250 Deg.F ('low pressure steam at 2 bar(g) or 30 psig'). Min Load/Unload Temp: 55 °C (131 ° F) Max Load/Unload Temp: 65 °C (149 ° F) Vis @ Min Load/Unload Temp: 1,150 cSt Vis @ Max Load/Unload Temp: 670 cSt Maximum Storage Temperature: 60 °C (140 ° F) Do not reheat above: 65 °C (149 ° F)", "lb/gal 7.99 lb/USG (ASTM D4052); 'This product can also be used to produce other performance levels'"),
 ('INFINEUM_D3463', 'DL2-13517.pdf', 1, 'Version: 25 October 2016 (1.0)', "13.7 mass % API CI-4 Plus/SL 15W-40 and API CI-4 Plus 10W-30, notes (a) additional claims and (b) '12.5 %Vol' recorded; BN 87, Ca 0.99, Mg 0.93, Zn 1.03, P 0.93, N 0.73, sulfated ash 8.98, KV40 3444, KV100 153, density 964, flash 184; lb/gal 8.02 in the open questions",
  "'This product is temperature sensitive. Do not heat over the maximum loading / unloading temperature to avoid possible release of extremely odorous alkyl mercaptans and/or toxichydrogen sulfide.' Min Load/Unload Temp: 55 °C (131 ° F) Max Load/Unload Temp: 65 °C (149 ° F) Vis @ Min Load/Unload Temp: 1,300 cSt Vis @ Max Load/Unload Temp: 730 cSt Maximum Storage Temperature: 60 °C (140 ° F) Do not reheat above: 65 °C (149 ° F)", "Appearance 'Brown viscous liquid with' (printed truncated)"),
 ('INFINEUM_D3503', 'DL2-11404.pdf', 2, 'Version: 25 May 2016 (3.0)', "14.5 mass % API CK-4 (10W-30, 15W-40) and API FA-4 10W-30, '~13.3 Volume %'; BN 68, Mg 0.69, Mo 0.05 (D4951), N 0.75, P 0.79, sulfated ash 6.9, S 1.99 (D4951), Zn 0.87, KV40 4467, KV100 183, density 961, flash 184; lb/gal 8.00 and the absence of Ca in the open questions", None, None),
 ('INFINEUM_D3511', 'DL2-15389.pdf', 1, 'Version: 20 September 2023 (2.0)', '13.2 mass % API CK-4 (10W-30, 10W-40, 15W-40) and API FA-4 10W-30, BN 80, Ca 0.81, Mg 0.76, Zn 0.96, P 0.87, N 0.95, sulfated ash 7.6 (Calculated), density 959; lb/gal 7.99 in the open questions (whole page re-read: the thirteenth-pass print of this page was cut at 2,500 characters)',
  "Min Load/Unload Temp: 55 °C (131 ° F) Max Load/Unload Temp: 65 °C (149 ° F) Vis @ Min Load/Unload Temp: 1,675 cSt Vis @ Max Load/Unload Temp: 940 cSt Maximum Storage Temperature: 60 °C (140 ° F) Do not reheat above: 65 °C (149 ° F)", "Appearance 'Brown, viscous liquid'"),
]
for pid, f, n, ver, eq, hand, extra in D:
    if hand is None and extra is None:
        tail = "the handling block (Min/Max Load/Unload 60 / 65 °C, 1,210 / 900 cSt, storage 60 °C, reheat 65 °C) is already proposed (twelfth-pass note). No new row."
    else:
        tail = 'not recorded: ' + ('the handling block' if hand else '') + (' and ' if hand and extra else '') + ('other printed items' if extra else '') + ' -> note.'
        F.append(dict(p=pid, tier=1, path='open_questions', old=f"{f} (cited, {ver}) prints (not recorded in the JSON): " + (f"'Handling / Precautions' {hand}" if hand else '') + ('; ' if hand and extra else '') + (extra or '') + f"; {FOOT}." if hand else f"{f} (cited, {ver}) prints (not recorded in the JSON): {extra}.",
                      new_f=f, new_p=n, new_text='(same file; byte duplicate in the new archive)', unit='as printed', form='data-sheet handling instructions and other printed items (no template field)',
                      qual='as printed', method='as printed', cond='loading / unloading / storage' if hand else '', basis='', outcome='in_old_source_not_captured', action='propose_note',
                      reason='Old-source information never captured; no template field. Preserve as printed (temperatures with both units, viscosities at the stated temperatures); nothing is mapped to a property field.',
                      old_rev=f're-read manually: {f} ({ver}) pp.1-{n} whole text ({T})', cmp_override='existing: not recorded'))
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'pp.1-{n} read in full in the original ({T})',
                      coverage=f'assessed by reading (2026-11-13, fifteenth pass) for the whole data sheet ({n} p., {ver}): JSON values equal the sheet ({eq}); {tail}',
                      identity='SHA-256 equal to the cited archive file', note='Byte duplicate of the cited data sheet.'))
d = dict(batch='duplicate coverage, batch 13: cited Infineum data sheets (fifteenth pass)', reviewed_on='2026-11-13 (fifteenth pass)',
         note='Ten byte-duplicate links; each data sheet read in full with the JSON beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzz_b13_dup_infineum_tds_fifteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
