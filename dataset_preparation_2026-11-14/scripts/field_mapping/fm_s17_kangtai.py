"""Field-level mapping, batch S17 KangTai (39 products, 39 product sheets; every sheet read in full on 2026-11-14).

Sources: one KangTai product sheet per product (1-2 pages, text layer; no date or revision is printed on any sheet, so
revision_date stays empty). The 'PRODUCT CHARACTERISTICS' table is parsed line by line (item / value / method); every parsed
row was compared with the page text read by the reviewer. Dosage tables, statements and co-component mentions are transcribed
in this file from the page text (DL2-12971 dosage table also viewed as an image: 'CF-4/SG 6.8' is one cell across both columns).

Value class: the table column is headed 'TYPICAL VALUE' / 'Typical Data', yet most cells print a bound ('180 min', '30 max') or a
range. They are recorded exactly as printed with value_kind 'bound' / 'range' and value_class 'product sheet, column headed
Typical Value'; whether a bound is a specification limit is NOT decided here (open question for the value-form review).
'Report' cells are Missing values (the property is listed without a number). Percentages: 'wt%' as printed in the unit or in the
'DOSAGE RECOMMENDED (WT%)' heading.

Recorded printed inconsistencies (kept, not resolved):
- BD C010: title 'TBN=MAX10' vs table 'TBN, mg KOH/g 30 max' (both rows written; conflict flagged).
- KT30100: test methods printed crosswise (flash point 'GB/T 265', kinematic viscosity 'GB/T 3536'): kept as printed, flagged.
- KT620: the footnote names the product 'T620' ('adding 10% T620 into 150SN Dalian base oil').
The KangTai SDSs (KTC-150, KTSA-250) and the catalogue belong to other products / are multi-product: not used here.
Writes field_evidence/s17_kangtai.csv."""
import csv, json, os, re
from fm_common import PKG, pages, parse_value, write_rows

DEC = json.load(open(os.path.join(PKG, 'decisions', 's17_kangtai.json'), encoding='utf-8'))
U = {r['sha256'][:12]: r for r in csv.DictReader(open(os.path.join(os.path.dirname(PKG), 'incoming_dataset_review_2026-11-12', 'tables', 'unique_documents.csv'), encoding='utf-8'))}
REVIEW = 'sheet read in full (text layer) 2026-11-14; parsed rows compared with the page text'
VC = 'product sheet, column headed Typical Value'
METHOD = re.compile(r'^(S?SH/T|GB/T|Q/SY|Visual inspection)')
VALUE = re.compile(r'^(-?\d[\d.]*\s*(-\s*\d[\d.]*)?\s*(min|max)?(\s*\(.*\))?|Report|Trace|Narrow|White or yellowish powder|\d[\d.]*max)$', re.I)
# printed item (lower-case prefix) -> (package tier2 field, component marker field)
ITEM = [('tbn', 'tbn', 'function_specific_markers.tbn'), ('sulphate ash', 'sulfated_ash', None), ('calcium', 'elements.Ca', 'function_specific_markers.ca'),
        ('zinc', 'elements.Zn', 'function_specific_markers.zn'), ('phosphorus', 'elements.P', 'function_specific_markers.p'), ('nitrogen', 'elements.N', None),
        ('sulfur', 'elements.S', None), ('sulphur', 'elements.S', None), ('boron', 'elements.B', None), ('kinemati', 'kv100', None), ('density', 'density', None),
        ('flash point', 'flash_point', None)]
PKG_T1 = {  # transcribed from the page text: treat-rate rows (performance level, oil type / condition, printed dose), statements
    'KT33169': dict(rows=[('CNG/LNG/CF-4/SJ', '', '8.5')]),
    'KT3069': dict(rows=[('SJ/LPG/CF', 'Mono', '/'), ('SJ/LPG/CF', 'Multi', '9.0'), ('SF', 'Mono', '5'), ('SF', 'Multi', '5.5'), ('SE', 'Mono', '4.2'), ('SE', 'Multi', '4.5')]),
    'KT30090': dict(rows=[('SL/CF', '', '7.2'), ('SJ/CF', '', '6.8'), ('SG/CD', '', '5.8'), ('SF/CC', '', '5.5')]),
    'KT30100': dict(rows=[('SN/CF-4', '', '7.6'), ('SM', '', '7.28'), ('SL/CF', '', '7.0')],
                    base='Blending KT30100 with suitable VII into group II and group III base oil can meet the requirements of SN/SM/SL.', co=[('VII (unnamed)', "'with suitable VII'", '')]),
    'KT31048': dict(rows=[('CJ-4/SM', 'Multi', '16'), ('CI-4/SM', 'Multi', '14'), ('CF-4/SL', 'Multi', '5')],
                    base='Blending KT31048 with suitable OCP VII into group II base oil can meet the requirements of CJ-4/CI-4/SM/SL.',
                    co=[('OCP VII (unnamed)', "'with suitable OCP VII'", ''), ('BD C300 + KT Z2048', "column 'BD C300+KT Z2048': CJ-4/SM '/', CI-4/SM '/', CF-4/SL '1.5+0.5'", '1.5+0.5')]),
    'KT31050': dict(rows=[('CJ-4/SM', 'Multi', '14.8'), ('CI-4/SM', 'Multi', '14'), ('CF-4/SL', 'Multi', '5.0')],
                    base='Blending KT31050 with suitable OCP VII into group II base oil can meet the requirements of CJ-4/CI-4/CF/SM. Has good compatibility with group II, group III and synthetic oil.',
                    co=[('OCP VII (unnamed)', "'with suitable OCP VII'", ''), ('BD C300 + KT Z2048', "column 'BD C300+KT Z2048': CJ-4/SM '/', CI-4/SM '/', CF-4/SL '1.5+0.5'", '1.5+0.5')]),
    'KT31140': dict(rows=[('CF-4/SG', '', '5.8'), ('CD/SF', '', '4.0'), ('CC/SE', '', '2.8')], base="It's a cost effective engine oil additive package designed for deep hydrogenation oils market."),
    'KT33070': dict(rows=[('SL', '', '7.8'), ('SJ', '', '5.5'), ('SF', '', '4.5')]),
    'KT33070A': dict(rows=[('SL', '', '6.6'), ('SJ', '', '5.5'), ('SF', '', '4.5')]),
    'KT33133': dict(rows=[('CD/CF', 'Multi', '6.0'), ('CD/CF', 'Mono', '5.5'), ('CC/SC', 'Multi', '3.0'), ('CC/SC', 'Mono', '2.8'), ('CB/SB', 'Mono', '1.5+0.2% ZDDP'), ('CD/SF', 'Multi', '4.5'),
                          ('CC/SD', 'Multi', '3.8'), ('CF-4', '', '6.6'), ('CF-2', '', '6.4')], co=[('ZDDP (unnamed)', "CB/SB Mono: '1.5+0.2% ZDDP'", '0.2')]),
    'KT33158': dict(rows=[('CF-4', 'Mono', '9.0'), ('CF-4', 'Multi', '9.6'), ('SG/CF', 'Mono', '6.8'), ('SG/CF', 'Multi', '7.2'), ('CD', 'Mono', '5.8'), ('CD', 'Multi', '6.2')]),
    'KT33160A': dict(rows=[('CI-4/SL', 'base oil API II/III', '13.0'), ('CH-4/SL', 'base oil API II', '11.5'), ('CH-4/SL', 'base oil API I', '11.5')],
                     base='Has good compatibility with group II, group III and synthetic oil.', note="the two CH-4/SL rows (API II, API I) are printed twice in the table"),
    'KT33161': dict(rows=[('CI-4,CH-4/SL', 'Mono', '/'), ('CI-4,CH-4/SL', 'Multi', '12'), ('CF-4/SL', 'Mono', '/'), ('CF-4/SL', 'Multi', '7.5'), ('CF-4/SJ', 'Mono', '6.0'), ('CF-4/SJ', 'Multi', '6.2'),
                          ('CF', 'Mono', '5.8'), ('CF', 'Multi', '6.0'), ('CD/SF', 'Mono', '4.6'), ('CD/SF', 'Multi', '4.8')], base='Has good compatibility with group II, group III and synthetic oil.'),
    'KT33162': dict(rows=[('CG/SJ', '', '6.8'), ('CF-4/SJ', '', '6.2'), ('CF-4/SG', '', '6.0'), ('CD/SF', '', '4.6'), ('CC', '', '3.2')], base='Has good compatibility with group II, group III and synthetic oil.'),
    'KT33210': dict(rows=[('CH-4', '', '6%+1.5% KT D2361+1%BD P250'), ('SJ', '', '5.5%+1.5% KT D2361'), ('CF-4/SG', '', '6.0%'), ('CE', '', '4.5%'), ('SF/CD', '', '4.2%'), ('CD', '', '4.0%')],
                    co=[('KT D2361', "CH-4: '+1.5% KT D2361'; SJ: '+1.5% KT D2361'", '1.5'), ('BD P250', "CH-4: '+1%BD P250'", '1')]),
    'KT33303': dict(rows=[('FC', 'fuel:oil 75-90:1; various emission air cooled two-stroke engine', '5.7'), ('FB', 'fuel:oil 35-50:1; 50ml emission air cooled two-stroke engine', '4.0')]),
    'KT33232': dict(rows=[('SF/CD', 'Multi', '5.0'), ('SF/CD', 'Mono', '5.0'), ('CD', 'Multi', '4.5'), ('CD', 'Mono', '4.0'), ('SE/CD', 'Multi', '4.0'), ('SE/CD', 'Mono', '4.0'), ('SC/SD/CC', 'Multi', '3.5'),
                          ('SC/SD/CC', 'Mono', '3.3'), ('CF-4/SG', 'one cell across the Multi and Mono columns (page image viewed)', '6.8')]),
    'KT33303A': dict(rows=[('EGE', '', '10'), ('EGD', '', '8'), ('FC EGC', '', '5')],
                     formulation='Preference formulation of two-stroke engine oil: base oil 35%, PIB 30%, KT33303A 5-10%,KT8602 0.5%, kerosene(the rest percentage).',
                     co=[('PIB (unnamed)', "preference formulation: 'PIB 30%'", '30'), ('KT8602', "preference formulation: 'KT8602 0.5%'", '0.5')]),
}


def blocks(txt):
    """Split a sheet page into its printed sections."""
    heads = ['PRODUCT DESCRIPTION', 'PRODUCT FEATURE', 'PRODUCT APPLICATIONS', 'DOSAGE RECOMMENDED (WT%)', 'PRODUCT CHARACTERISTICS', 'PACKING, STORAGE AND TRANSPORTATION']
    pos = sorted((txt.find(h), h) for h in heads if txt.find(h) >= 0)
    out = {'HEAD': txt[:pos[0][0]] if pos else txt}
    for (a, h), nxt in zip(pos, pos[1:] + [(len(txt), '')]):
        out[h] = txt[a + len(h):nxt[0]]
    return out


def table(body):
    """'PRODUCT CHARACTERISTICS' lines -> [(item, value, method)]. Lines are classified as method / value / item text."""
    lines = [l.strip() for l in body.split('\n') if l.strip()]
    lines = [l for l in lines if l.upper() not in ('ITEM', 'TYPICAL VALUE', 'TEST METHOD', 'TYPICAL DATA') and 'WWW.JZKANGTAI' not in l and not l.startswith('KangTai')]
    rows, item = [], ''
    for l in lines:
        m2 = re.match(r'^(Orange to amber transparent liquid) (Visual inspection)$', l)
        if l.startswith('The Pour point depression effect'):
            rows.append(['(footnote)', l, '']); continue
        if m2:
            rows.append([item, m2.group(1), m2.group(2)]); item = ''
        elif METHOD.match(l) and rows and not rows[-1][2] and not item:
            rows[-1][2] = l
        elif VALUE.match(l) and item:
            rows.append([item, l, '']); item = ''
        else:
            item = (item + ' ' + l).strip()
    return rows


R = []
for sha12, v in DEC['documents'].items():
    if not v['products']:
        continue
    key = v['products'][0]
    prod = DEC['products'][key]
    code = key.split(':')[1]
    is_pkg = prod['material_class'] == 'additive_package'
    src = U[sha12]
    pg = pages(src['sha256'])
    B, tpage = {}, 1
    for n, p in enumerate(pg, 1):
        b = blocks(p)
        if 'PRODUCT CHARACTERISTICS' in b:
            tpage = n
        for h, t in b.items():
            B.setdefault(h, (t, n))
    base = dict(product_key=key, source_file=src['first_path'], sha256=src['sha256'], revision_date='', review=REVIEW, basis='printed on the cited page')

    def add(template, field, status='Reported', page=1, **kw):
        R.append(dict(base, template=template, field=field, status=status, page=page if status == 'Reported' else '', **kw))

    head = [l.strip() for l in B['HEAD'][0].split('\n') if l.strip() and 'KangTai' not in l and 'WWW.' not in l]
    title, klass = (head[1] if len(head) > 1 else ''), (head[2] if len(head) > 2 else '')
    desc = re.sub(r'\s+', ' ', B.get('PRODUCT DESCRIPTION', ('', 1))[0]).strip()
    apps = re.sub(r'\s+', ' ', B.get('PRODUCT APPLICATIONS', ('', 1))[0]).strip()
    trows = table(B['PRODUCT CHARACTERISTICS'][0])
    used = set()
    # ---- numeric table
    T2 = 'package_tier2' if is_pkg else 'component_general'
    for item, val, meth in trows:
        if item == '(footnote)':
            add('component_vm', 'not_in_template:pour point depression effect (footnote)', page=tpage, printed_text=val, value_kind='text', value_class=VC,
                conditions='10% in 150SN Dalian base oil', notes="footnote names the product 'T620' (sheet title: KT620)")
            continue
        value, q, lo, hi, kind = parse_value(val)
        il = item.lower()
        hit = next((x for x in ITEM if il.startswith(x[0])), None)
        field = (hit[1] if is_pkg else hit[2]) if hit else None
        unit = (re.search(r'(mg ?KOH/g|wt ?%|mm²/s|°C|℃|kg/m³|%|JTU|rating|No\.)', item) or [None])[0] if re.search(r'(mg ?KOH/g|wt ?%|mm²/s|°C|℃|kg/m³|%|JTU|rating|No\.)', item) else ''
        unit = re.search(r'(mg ?KOH/g|wt ?%|mm²/s|kg/m³|JTU|rating|°C|℃|%)', item)
        unit = unit.group(1) if unit else ''
        temp = re.search(r'\((\d+)\s?[°℃]', item)
        notes = ''
        if code == 'KT30100' and il.startswith(('flash', 'kinemati')):
            notes = 'test methods are printed crosswise on this sheet (flash point GB/T 265, viscosity GB/T 3536): kept as printed'
        if code == 'BDC010' and il.startswith('tbn'):
            notes = "CONFLICT inside the sheet: the title prints 'TBN=MAX10', the table '30 max' (unresolved)"
        status = 'Missing' if kind == 'report-only' else 'Reported'
        if kind == 'report-only':
            notes = (notes + '; ' if notes else '') + "the sheet lists the property with 'Report' (no value printed)"
        kw = dict(value=value, qualifier=q, min=lo, max=hi, value_kind=kind, printed_text=item + ' | ' + val, unit=unit, method=meth, test_temperature_c=temp.group(1) if temp and not il.startswith('flash') else '',
                  value_class=VC, notes=notes)
        if field:
            used.add(field)
            if status == 'Missing':
                R.append(dict(base, template=T2, field=field, status='Missing', page='', printed_text='', value_kind='report-only', method=meth, notes=notes + f" (page {tpage}: '{item} | {val}')", value_class=VC))
            else:
                add(T2, field, page=tpage, **kw)
        else:
            add(T2, 'not_in_template:' + re.sub(r'[,(].*', '', item).strip().lower(), status='Reported' if status == 'Reported' else 'Missing', page=tpage, **kw)
    if code == 'BDC010':
        add('component_general', 'function_specific_markers.tbn', page=1, value='', qualifier='<=', max='10', value_kind='bound', printed_text=title, unit='(none printed)',
            value_class='product sheet title', notes="CONFLICT inside the sheet: title 'TBN=MAX10' vs table 'TBN, mg KOH/g 30 max' (unresolved)")
    # ---- templates' remaining fields
    if is_pkg:
        t1 = PKG_T1[code]
        add('package_tier1', 'package_type_application.package_type', printed_text=title, value_kind='text', value_class='product sheet title')
        add('package_tier1', 'package_type_application.intended_service', printed_text=desc, value_kind='text', value_class='product sheet description', page=B['PRODUCT DESCRIPTION'][1])
        dpage = B.get('DOSAGE RECOMMENDED (WT%)', ('', 1))[1]
        for i, (lvl, cond, dose) in enumerate(t1['rows'], 1):
            num = dose if re.fullmatch(r'\d+(\.\d+)?', dose) else (dose[:-1] if re.fullmatch(r'\d+(\.\d+)?%', dose) else '')
            note = t1.get('note', '')
            if dose == '/':
                note = "printed '/' (no dose given for this oil type)"
            elif not num:
                note = 'dose printed with co-components: kept as printed, not split into a single number'
            add('package_tier1', 'treat_rate_matrix', entry=i, page=dpage, value=num, value_kind='typical' if num else 'text', printed_text=f'{lvl} | {cond} | {dose}'.replace('|  |', '|'), unit='wt%',
                conditions=(cond + '; ' if cond else '') + 'performance level ' + lvl, value_class="recommended dosage (table 'DOSAGE RECOMMENDED (WT%)')", notes=note)
            if dose != '/':
                add('package_tier1', 'performance_claims', entry=i, page=dpage, printed_text=f"Performance Level '{lvl}' at {dose}{'' if '%' in dose else ' wt%'}" + (f' ({cond})' if cond else ''), value_kind='text',
                    value_class='supplier dosage recommendation for a stated performance level (not an approval or licence)')
        if t1.get('base'):
            add('package_tier1', 'permitted_base_oils_restrictions', printed_text=t1['base'], value_kind='text', value_class='product sheet statement', page=B['PRODUCT DESCRIPTION'][1],
                notes='statement as printed; it is not a list of permitted or excluded base oils')
        else:
            add('package_tier1', 'permitted_base_oils_restrictions', status='Missing', notes='no base-oil statement on the sheet (all pages read)')
        for i, (comp, txt, dose) in enumerate(t1.get('co', []), 1):
            add('package_tier1', 'required_co_components', entry=i, page=dpage if 'column' in txt or ':' in txt else B['PRODUCT DESCRIPTION'][1], printed_text=txt, value=dose if re.fullmatch(r'[\d.]+', dose) else '', unit='wt%' if dose else '',
                value_kind='text', value_class='co-component named on the product sheet', conditions=comp,
                notes='named co-component; the sheet does not state that the list is complete (route completeness not assessed)')
        if not t1.get('co'):
            add('package_tier1', 'required_co_components', status='Missing', notes="no co-component is named on the sheet (all pages read); this is 'not recorded on this sheet', not a statement that none is required")
        if t1.get('formulation'):
            add('package_tier1', 'published_formulations', entry=1, printed_text=t1['formulation'], value_kind='text', value_class='finished-oil formulation example', page=B['PRODUCT DESCRIPTION'][1] if False else dpage,
                notes="percentages printed without a basis in the sentence ('%'): basis unspecified")
        else:
            add('package_tier1', 'published_formulations', status='Missing', notes='no formulation example on the sheet (all pages read)')
        add('package_tier1', 'sae_grades_documented', status='Missing', notes="no SAE viscosity grade is printed (only 'Mono' / 'Multi' where shown)")
        add('package_tier1', 'route_selector_restrictions', status='Missing', notes='no limits or exclusions printed on the sheet')
        for f in ('tbn', 'sulfated_ash', 'elements.Ca', 'elements.Mg', 'elements.Zn', 'elements.P', 'elements.B', 'elements.Mo', 'elements.N', 'elements.S', 'kv40', 'kv100', 'density', 'specific_gravity', 'flash_point', 'pour_point'):
            if f not in used:
                n = 'not printed on the sheet (all pages read)'
                if code == 'KT33161' and f in ('elements.Mg', 'elements.B', 'elements.Mo'):
                    n = "the description prints 'Contains magnesium, boron and molybdenum' but gives no content: value Missing"
                add('package_tier2', f, status='Missing', notes=n)
    else:
        vm = 'Viscosity Index' in klass or 'Viscosity Index' in title
        add('component_general', 'function.primary', printed_text=klass or title, value_kind='text', value_class='product sheet title')
        add('component_general', 'function.secondary', status='Missing', notes='secondary function not stated as such (features are listed in PRODUCT FEATURE; not mapped to a function)')
        if klass:
            add('component_general', 'chemical_family', printed_text=title, value_kind='text', value_class='product sheet title')
        else:
            add('component_general', 'chemical_family', status='Missing', notes='chemistry not printed on the sheet (title gives the function only)')
        add('component_general', 'active_content', status='Missing', notes='not printed on the sheet (all pages read)')
        add('component_general', 'carrier.identity', status='Missing', notes='not printed on the sheet')
        add('component_general', 'carrier.share_wt_pct', status='Missing', notes='not printed on the sheet')
        ds = re.findall(r'(?:Dosage recommended \(wt%\):|Recommend dosage:|Engine oil:|Marine cylinder oil:)\s*([\d.]+)\s*-\s*([\d.]+)%', apps)
        labels = re.findall(r'(Dosage recommended \(wt%\):|Recommend dosage:|Engine oil:|Marine cylinder oil:)\s*[\d.]+\s*-', apps)
        for i, ((lo, hi), lab) in enumerate(zip(ds, labels), 1):
            add('component_general', 'treat_rate', entry=i, page=B['PRODUCT APPLICATIONS'][1], min=lo, max=hi, value_kind='range', printed_text=f'{lab} {lo}-{hi}%', unit='wt%' if 'wt%' in apps else '%',
                value_class='recommended dosage', conditions='' if lab.startswith(('Dosage', 'Recommend')) else lab.strip(':'),
                notes='' if 'wt%' in apps else "printed 'Recommend dosage: ...%' without a basis: percentage basis unspecified")
        if not ds and code != 'KT6614':
            add('component_general', 'treat_rate', status='Missing', notes='no dosage printed on the sheet')
        if code == 'KT6614':
            add('component_general', 'treat_rate', status='Missing', notes='no general dosage; the sheet gives dosage by SAE grade (see component_vm.treat_range_by_sae_grade)')
        if code == 'KTZ2048':
            add('component_general', 'compatibility_restrictions', page=B['PRODUCT APPLICATIONS'][1], value_kind='text', value_class='product sheet statement',
                printed_text="But it can't be used to blend the lubricants for the mechine with the argentum parts.", notes='exclusion as printed (argentum = silver)')
        elif code == 'KT3321':
            add('component_general', 'compatibility_restrictions', page=1, value_kind='text', value_class='product sheet statement', printed_text='good compatibility with containing phosphorus compounds',
                notes='a compatibility statement, not a restriction')
        else:
            add('component_general', 'compatibility_restrictions', status='Missing', notes='no restriction printed on the sheet')
        for f in ('tbn', 'ca', 'mg', 'p', 'zn', 'mo'):
            if 'function_specific_markers.' + f not in used:
                add('component_general', 'function_specific_markers.' + f, status='Missing', notes='not printed on the sheet (all pages read)')
        if vm:
            add('component_vm', 'polymer_chemistry.type', **(dict(printed_text=title, value_kind='text', value_class='product sheet title') if klass else dict(status='Missing', notes='polymer chemistry not printed')))
            form = re.search(r'(White transparent block colloid|Clear light yellow liquid|Transparent liquid)', desc)
            add('component_vm', 'polymer_chemistry.form', **(dict(printed_text=form.group(1) + ('' if 'SOLID' not in title else " (title: 'SOLID')"), value_kind='text', value_class='product sheet description') if form else dict(status='Missing', notes='physical form not printed')))
            for f in ('active_polymer.wt_pct', 'active_polymer.carrier_identity', 'active_polymer.carrier_share_wt_pct', 'thickening_response', 'post_shear_blend_behaviour.post_shear_kv100',
                      'post_shear_blend_behaviour.hths_150c', 'post_shear_blend_behaviour.ccs_impact', 'post_shear_blend_behaviour.mrv_impact', 'post_shear_blend_behaviour.low_temp_gelation',
                      'dissolution_blend_temperature.temperature_c', 'dissolution_blend_temperature.procedure'):
                add('component_vm', f, status='Missing', notes='not printed on the sheet (all pages read)')
            ssi = [r for r in R if r['product_key'] == key and 'shear' in r['field'] and r['field'].startswith('not_in_template')]
            for r in ssi:
                r['template'], r['field'] = 'component_vm', 'shear_stability'
                r['notes'] = (r['notes'] + '; ' if r['notes'] else '') + 'SSI as printed; reference oil and dose are not printed'
            if not ssi:
                add('component_vm', 'shear_stability', status='Missing', notes='not printed')
            if code == 'KT6614':
                for i, (g, d, kv) in enumerate([('5W/30', '8-10', '3.5-4.5'), ('10W/30', '8-9', '5.0-5.5'), ('10W/40', '7-8', '4.0-5.0'), ('15W/40', '6-7', '6.0-7.0')], 1):
                    lo, hi = d.split('-')
                    add('component_vm', 'treat_range_by_sae_grade', entry=i, page=1, min=lo, max=hi, value_kind='range', unit='wt%', printed_text=f'{g} | {d} | {kv}',
                        conditions=f'SAE {g}; kinematic viscosity of base oil (100°C) {kv} mm2/s', value_class='recommended dosage by SAE grade')
            else:
                add('component_vm', 'treat_range_by_sae_grade', status='Missing', notes='no dosage by SAE grade printed')
write_rows('s17_kangtai.csv', R)
from collections import Counter
print(len(R), 'rows', Counter(r['status'] for r in R), len({r['product_key'] for r in R}), 'products')
print(Counter(r['field'] for r in R if r['field'].startswith('not_in_template')).most_common())
