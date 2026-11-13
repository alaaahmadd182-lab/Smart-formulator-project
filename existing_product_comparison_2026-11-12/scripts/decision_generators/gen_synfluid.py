# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
links, F, queue = [], [], []


def L(p, f, cat, fs, cov, idn, note=''):
    links.append(dict(p=p, f=f, cat=cat, status='completed', fields_status=fs, coverage=cov, identity=idn, note=note))


def R(p, tier, path, old, nf, np_, nt, unit, form, act, reason, orv, cmp, outc='additional', qual='', meth='', cond=''):
    F.append(dict(p=p, tier=tier, path=path, old=old, new_f=nf, new_p=np_, new_text=nt, unit=unit, form=form, qual=qual, method=meth, cond=cond, basis='', outcome=outc, action=act, reason=reason, old_rev=orv, cmp_override=cmp))


M = 'DL2-13198.pdf'
L('CHEVRON_SYNFLUID_MPAO_100', M, 'F,E', 'both pages read (text layer); mPAO 100 column compared with DL2-11912.pdf (April 2013) and the JSON',
  'earlier edition (© 2011) of the typical properties: KV100 100 (2013: 101), KV40 992 (1023), VI 194 (192), pour -44 (= ), flash > 250 (2013: 265, consistent with the bound), SG 0.847 (=), fire point > 300, density 7.04 lb/gal (2013: 7.069), RPVOT 3,889 min (with 0.5 wt% antioxidant; no field)',
  "exact: 'Synfluid mPAO 100 cSt' (Chevron Phillips Chemical, © 2011)", 'Earlier edition; see the historical-note rows.')
L('CHEVRON_SYNFLUID_MPAO_40', M, 'F,E', 'both pages read (text layer); mPAO 40 column compared with DL2-13191.pdf (April 2013) and the JSON',
  'earlier edition (© 2011): KV100 40 (2013: 41), KV40 348 (347), VI 170 (172), pour -50 (=), flash > 250 (2013: 244 - outside the earlier bound), SG 0.838 (0.843), density 6.98 lb/gal (7.035), RPVOT 3,577 min (no field)',
  "exact: 'Synfluid mPAO 40 cSt'", 'Earlier edition; see the historical-note rows.')
O13 = 're-read manually: {} (CPChem typical-properties sheet, Revision Date April 2013) whole page (text layer)'
for pid, old, rows in (('CHEVRON_SYNFLUID_MPAO_100', 'DL2-11912.pdf', [('kv100', 'mm2/s', '101', '100'), ('kv40', 'mm2/s', '1023', '992'), ('viscosity_index', '', '192', '194')]),
                       ('CHEVRON_SYNFLUID_MPAO_40', 'DL2-13191.pdf', [('kv100', 'mm2/s', '41', '40'), ('kv40', 'mm2/s', '347', '348'), ('viscosity_index', '', '172', '170'),
                                                                      ('flash_point', 'C', '471 F (244 C)', '> 250 C'), ('specific_gravity', '', '0.843', '0.838')])):
    for path, unit, v13, v11 in rows:
        R(pid, 2 if path == 'flash_point' else 1, path, f"{old} (April 2013) read: typical {v13}. JSON equals the 2013 sheet.", M, 1, f"typical {v11} (sheet © 2011 Chevron Phillips Chemical Company LP)", unit,
          'typical (manufacturer data sheet, earlier edition © 2011)', 'propose_historical_note',
          f"An earlier edition (© 2011) printed {v11}; the cited April 2013 sheet prints {v13}. Propose a historical note with both values and dates; the JSON value is not changed by date preference or averaging." +
          (" For flash point the 2013 typical (244 C) lies outside the earlier bound '> 250 C'; recorded, not resolved." if path == 'flash_point' else ''),
          O13.format(old), f'existing: {v13} (April 2013)', outc='changed_or_conflicting', qual='typical')
S2, S8 = 'DL2-14993.pdf', 'DL2-14966.pdf'
L('CHEVRON_SYNFLUID_PAO_2', S2, 'E', 'whole page read (text layer)',
  "CPChem 'Sales Specification - Europe', approved January 6, 2017, Beringen: limits for KV100 1.6-1.8, KV -40 C max 300 (D7042), pour max -66 (D7346), flash min 150, fire min 170, colour max 15, density 15 C 793-803 kg/m3, water max 50 mg/kg, bromine index max 400; the JSON typicals (DL2-13192.pdf, December 2008) lie inside every limit",
  "exact: 'Synfluid PAO 2 cSt'", 'Specification limits are a different value class from the typicals; see field rows.')
L('CHEVRON_SYNFLUID_PAO_8', S8, 'E', 'whole page read (text layer)',
  "Sales Specification - Europe (January 6, 2017, Beringen): KV100 7.7-8.0, KV40 46.1-50.5, KV -18 C max 1800, KV -40 C max 24000, VI min 130, Noack max 4 (CEC L-40-93b), pour max -54 (D97), flash min 245, odour pass, colour max 15, water max 50 ppmw, density 15 C 820-840 kg/m3, Br-index max 400; JSON typicals (DL2-11916.pdf, April 2011) inside every limit",
  "exact: 'Synfluid PAO 8 cSt'")
L('CHEVRON_SYNFLUID_PAO_8', 'DL2-13195.pdf', 'G', 'whole page read (text layer)', 'not applicable (another product)',
  "DIFFERENT PRODUCT: 'Synfluid PAO 8 cSt Blend' (MSDS #8014, Revision Date March, 2004): VI 145, Noack 2.5, pour -45 C, flash 266 C differ from 'Synfluid PAO 8 cSt' (VI 138, Noack 3.5, pour -56, flash 262); listed in the new-product queue")
L('CHEVRON_SYNFLUID_PAO_6', 'DL2-13197.pdf', 'G', 'whole page read (text layer)', 'not applicable (another product)',
  "DIFFERENT PRODUCT: 'Synfluid PAO 6 cSt HVI' (MSDS # 100000101638, June 2012): VI 150, Noack 4.9, pour -44, KV40 29.1 differ from 'Synfluid PAO 6 cSt' in the JSON (VI 137, Noack 6.6, pour -61, KV40 30.5); listed in the new-product queue")
queue += [dict(name_as_printed='Synfluid PAO 8 cSt Blend', supplier='Chevron Phillips Chemical Company LP', file='DL2-13195.pdf', page=1, evidence='typical-properties sheet, MSDS #8014, March 2004; distinct from Synfluid PAO 8 cSt'),
          dict(name_as_printed='Synfluid PAO 6 cSt HVI', supplier='Chevron Phillips Chemical Company LP', file='DL2-13197.pdf', page=1, evidence='typical-properties sheet, June 2012; distinct from Synfluid PAO 6 cSt')]
SPECS = {'CHEVRON_SYNFLUID_PAO_2': (S2, 'DL2-13192.pdf (December 2008)', [('kv100', 'mm2/s', 'Min 1.6 / Max 1.8 (ASTM D-445)', 'typical 1.7'), ('pour_point', 'C', 'Max -66 (ASTM D-7346)', 'typical -73'),
                                                                         ('flash_point', 'C', 'Min 150 (ASTM D-92)', 'typical 159'), ('density', 'kg/m3', 'Density, 15 C Min 793 / Max 803 (ASTM D-4052)', 'Missing (SG 0.7981 at 15.6 C only)')]),
         'CHEVRON_SYNFLUID_PAO_8': (S8, 'DL2-11916.pdf (April 2011)', [('kv100', 'mm2/s', 'Min 7.7 / Max 8.0 (ASTM D-445)', 'typical 7.8'), ('kv40', 'mm2/s', 'Min 46.1 / Max 50.5 (ASTM D-445)', 'typical 46.4'),
                                                                      ('viscosity_index', '', 'Min 130 (ASTM D-2270)', 'typical 138'), ('noack_volatility', 'wt%', 'Max 4 (CEC L-40-93b)', 'typical 3.5'),
                                                                      ('pour_point', 'C', 'Max -54 (ASTM D-97)', 'typical -56'), ('flash_point', 'C', 'Min 245 (ASTM D-92)', 'typical 262'),
                                                                      ('density', 'kg/m3', 'Density, 15 C Min 820 / Max 840 (ASTM D-4052)', 'Missing (SG 0.8326 at 15.6 C only)')])}
for pid, (nf, oldd, rows) in SPECS.items():
    for path, unit, spec, cur in rows:
        tier = 1 if path in ('kv100', 'kv40', 'viscosity_index', 'density') else 2
        missing = cur.startswith('Missing')
        R(pid, tier, path, f"{oldd} read: {cur}; no specification limits printed. JSON: {cur}.", nf, 1, f"'Sales Specification - Europe', approved January 6, 2017, Beringen: {spec}", unit,
          'specification limits (manufacturer sales specification, 2017)', 'propose_add' if missing else 'propose_alternate_entry',
          ('Density at 15 C is Missing (only a specific gravity at 15.6 C is recorded); propose adding the specification range as a range (not a point) with this source.' if missing else
           f'The JSON typical ({cur}) lies inside the printed specification. Propose recording the limits as a specification entry beside the typical (a different value class); the typical is unchanged.'),
          f're-read manually: {oldd.split(" ")[0]} whole page (text layer)', f'existing: {cur}', qual='specification range' if '/' in spec else 'specification limit', meth=spec.split('(')[-1].rstrip(')'), cond='15 C' if path == 'density' else '')
d = dict(batch='Chevron Phillips Chemical Synfluid: earlier edition, 2017 sales specifications, two different products (tenth pass)', reviewed_on='2026-11-13 (tenth pass)',
         note='Cited sheets re-read: DL2-11912.pdf and DL2-13191.pdf (April 2013), DL2-13192.pdf (December 2008), DL2-11916.pdf (April 2011). Specification limits and typicals are kept as separate value classes; an earlier edition is recorded as history, not preferred or averaged.',
         documents={M: dict(what='CPChem Synfluid mPAO 100 cSt and mPAO 40 cSt typical properties (2 pp.)', printed_date='© 2011', kind='manufacturer data sheet (earlier edition)', read='both pages (text layer)', limits=''),
                    S2: dict(what="CPChem 'Sales Specification - Europe' Synfluid PAO 2 cSt", printed_date='approved January 6, 2017', kind='manufacturer sales specification', read='whole page (text layer)', limits=''),
                    S8: dict(what="CPChem 'Sales Specification - Europe' Synfluid PAO 8 cSt", printed_date='approved January 6, 2017', kind='manufacturer sales specification', read='whole page (text layer)', limits="appearance row prints unit 'mm2/S' (layout error, noted)"),
                    'DL2-13195.pdf': dict(what="CPChem 'Synfluid PAO 8 cSt Blend' typical properties", printed_date='March 2004 (MSDS #8014)', kind='manufacturer data sheet (other product)', read='whole page', limits=''),
                    'DL2-13197.pdf': dict(what="CPChem 'Synfluid PAO 6 cSt HVI' typical properties", printed_date='June 2012', kind='manufacturer data sheet (other product)', read='whole page', limits='')},
         links=links, fields=F, new_product_candidates=queue)
json.dump(d, open('existing_product_comparison_2026-11-12/decisions/zzzzzzzzzz_synfluid_tenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
