"""Nineteenth pass, batch 33: duplicate (category A) coverage of the last two byte-duplicate links, the image-only Indian Additives Ltd.
(Chevron Oronite) MSDSs of N216 (DL2-12493.pdf, 6 pp) and N204 (DL2-12494.pdf, 8 pp). The pages that carry the recorded values were viewed
as page images (no text layer); the other pages were not viewed in this pass (stated per link). Writes
decisions/zzzzzzzzzzzzzzzzzzz_b33_dup_chevron_n216_n204_nineteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'nineteenth pass, 2026-11-14'
links, F = [], []


def link(pid, f, read, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read} ({T})',
                      coverage=f'assessed by reading (page images viewed; 2026-11-14, nineteenth pass) for the pages stated ({ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file; product name in section 1 (page image)',
                      note='Byte duplicate of the cited image-only MSDS (targeted reading of the pages carrying the recorded values; see scope).'))


link('CHEVRON_N216', 'DL2-12493.pdf',
     'pp.1, 2, 4 and 6 viewed as page images in full (sections 1-2 and start of 3; end of 3 to start of 6; end of 8 to start of 11; end of 15 and 16); pp.3 and 5 not viewed (of 6 pages)',
     'Revision Number 3, Revision Date October 03, 2018, MSDS 44378',
     "the page images show the values recorded from this MSDS: p.1 'Product Use: Automotive lubricant additive', Indian Additives Ltd. as company and the four section 2 shares (in the open question, not element contents); "
     "p.2 'Flashpoint: (Cleveland Open Cup) 180 °C (356 °F) Minimum'; p.4 section 9 ('the data below are typical values and do not constitute a specification') 'Density: 0.9902 kg/l @ 15°C (59°F)', 'Viscosity: 3320 cSt @ 40°C (104°F)', "
     "'Coefficient of Therm. Expansion / °F: 0.000360' (open question) and 'prescribed treatment rate of: 11.95 wt. %' (section 11); p.6 revision statement 'SECTION 09 - Physical/Chemical Properties information was deleted.' (open question). All equal the record. No new row.")
link('CHEVRON_N204', 'DL2-12494.pdf',
     'pp.1, 3, 5 and 6 viewed as page images in full (sections 1-2; 5 to start of 7; end of 8 to start of 11; end of 11 to 13); pp.2, 4, 7 and 8 not viewed (of 8 pages)',
     'Revision Number 0, Revision Date November 01, 2017, MSDS 46286',
     "the page images show the values recorded from this MSDS: p.1 'Product Use: Automotive lubricant additive', Indian Additives Ltd. as company and the four section 2 shares (in the open question; printed identical to N216's, which is recorded, not interpreted); "
     "p.3 'Flashpoint: (Cleveland Open Cup) 180 °C (356 °F) Minimum'; p.5 section 9 (typical values, not a specification) 'Specific Gravity: 0.9850 @ 15.6°C (60°F)', 'Density: 0.9850 kg/l @ 15°C (59°F)', 'Viscosity: 3890 cSt @ 40°C (104°F)', "
     "'Coefficient of Therm. Expansion / °F: No data available'; p.6 'prescribed treatment rate of: 12.9 wt. %' (section 11). All equal the record. No new row.")

d = dict(batch='duplicate coverage, batch 33: N216 / N204 image-only MSDSs (nineteenth pass)', reviewed_on='2026-11-14 (nineteenth pass)',
         note='Last two byte-duplicate links; page images viewed for the pages stated per link; the other pages not viewed.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzzz_b33_dup_chevron_n216_n204_nineteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
