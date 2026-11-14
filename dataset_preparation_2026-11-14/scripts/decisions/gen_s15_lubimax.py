"""Supplier batch S15: Lubimax / Coraplus (47 documents; certificates issued by CHEMXO FZE / Chemxo Trading FZE, Dubai).
Read: compact page-1 listing (product name + printed descriptor on every TDS / SDS); longer cards for 4 certificates; DL2-15524
page 1 viewed (name 'LUBIMAX 411K' printed in the image only; Chemxo Trading FZE letterhead).
Rules: subject = printed name; 'LUBIMAX(TM)' and 'LUBIMAX' are the same brand mark; 'PIB 2400 SA' = 'PIB 2400SA' (spacing) but
'PIB 2400' is a separate product; 'Base Oil SN150' (TDS, 'Group I') and 'Base Oil 150' (SDS) are NOT merged (different printed
names); 'P50l' / 'P135l' kept as printed (final character printed as 'l'). Coraplus-branded sheets (base oils, XONOX L 57) are
recorded under supplier 'Coraplus' with key prefix LUBIMAX: for consolidation (same website family on the sheets: coraplus.com /
lubimax.com) - the corporate relation is not asserted. The Lubimax 5524 TDS (sha 42ea0cf987) carries an existing-comparison link to
CHEVRON_GROUP_II_100R from the earlier workstream; it is kept as recorded there (not reinterpreted here).
Classes from the printed descriptor. Identity only. Writes decisions/s15_lubimax.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Lubimax')]
OV = {'48e2efd90c': ('LUBIMAX 5522', 'certificate of analysis (batch)', 'CHEMXO FZE certificate, March 2020'),
      '779979a695': ('LUBIMAX PIB 2400', 'certificate of analysis (batch)', 'certificate, February 2020'),
      '25ed3e4bbf': ('LUBIMAX PIB 2400', 'certificate of analysis (batch)', 'certificate, February 2020 (different batch)'),
      '51badddcd7': ('LUBIMAX 411K', 'certificate of analysis (batch)', "Chemxo Trading FZE certificate, January 2024 (name read on the page image)"),
      'd8c0fdd76b': ('LUBIMAX BC 2200N', 'SDS', ''), '8bc6ea874c': ('LUBIMAX 411K', 'SDS', '')}
DESC = {}


def cls(k, d):
    if re.search(r'(?i)Group I+\+?|API Group|^Base Oil$', d) or k.startswith('BASE OIL'): return 'base_oil', d
    if re.search(r'(?i)Poly ?Alpha ?Olefin', d): return 'base_oil', d + ' (PAO, Group IV)'
    if re.search(r'(?i)Polyalkylene Glycol', d): return 'base_oil', d + ' (template fit to confirm: no API group)'
    if re.search(r'(?i)package', d): return 'additive_package', d
    if re.search(r'(?i)biocide', d): return 'additive_component', d + ' (water-based / metalworking use: scope question)'
    if re.search(r'(?i)PolyIsoButene', d): return 'unresolved', d + ' (polybutene: role not stated)'
    if re.search(r'(?i)succinimide|dithio|viscosity index|pour point|sulphonate|antioxidant|VII', d): return 'additive_component', d
    return 'unresolved', d


D, PK = {}, {}
for r in A:
    sha, t = r['sha256'], r['top_lines'].replace('\n', ' | ')
    p10 = sha[:10]
    if p10 in OV:
        key, typ, note = OV[p10]
        d = ''
    else:
        m = re.search(r'(?:Data Sheet|Safety Data Sheet) \| ((?:LUBIMAX\S*|XONOX|Base Oil)\s*[^|]+?) \| ([^|]+)', t)
        name, d = m.group(1).strip(), m.group(2).strip()
        key = re.sub(r'^LUBIMAX(?:TM|™)?\s*', 'LUBIMAX ', name.upper())
        key = key.replace('PIB 2400 SA', 'PIB 2400SA').replace('AW1720', 'AW 1720')
        key = re.sub(r'\s*\(GROUP I\)\s*-?$', '', key)
        typ = 'SDS' if 'Safety Data Sheet' in t else 'product data sheet (TDS/PDS)'
        ver = re.search(r'(V(?:er)?\.?\s?\d[\d./]*\s?(?:\(\d{4}-\d{2}\))?)', t)
        note = ('edition ' + ver.group(1)) if ver else ''
    if d:
        DESC.setdefault(key, d)
    sup = 'Coraplus' if ('coraplus' in t.lower()) else 'Lubimax (CHEMXO FZE)'
    D[sha[:12]] = dict(doc_type=typ, supplier=sup, products=['LUBIMAX:' + key], roles={'LUBIMAX:' + key: 'subject'}, relation='product',
                       read='page-1 listing' + ('; longer card' if p10 in ('48e2efd90c', '779979a695', '25ed3e4bbf') else '') + ('; page image viewed' if p10 == '51badddcd7' else ''),
                       note=note, next_action='')
for key in dict.fromkeys(p for v in D.values() for p in v['products']):
    k = key.split(':', 1)[1]
    mc, n = cls(k, DESC.get(k, ''))
    sup = 'Coraplus' if k.startswith(('BASE OIL', 'XONOX')) else 'Lubimax (CHEMXO FZE)'
    PK[key] = dict(name=k, supplier=sup, material_class=mc, existing_record='', status='new_candidate', notes=('printed: ' + n) if n else 'descriptor not printed on the documents linked',
                   identity_evidence='printed product name on the documents linked in this batch',
                   template={'base_oil': 'base_oil tier1-3', 'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype)'}.get(mc, 'not determined'))
for k in ('LUBIMAX:BASE OIL 150', 'LUBIMAX:BASE OIL SN150'):
    PK[k]['notes'] += "; 'Base Oil 150' (SDS) and 'Base Oil SN150' (TDS) are not merged (different printed names)"
out = dict(batch='S15 Lubimax / Coraplus (identity)', reviewed_on='2026-11-14', scope='47 documents with provisional supplier Lubimax / Coraplus', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's15_lubimax.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['material_class'] for p in PK.values()))
for k, v in sorted(PK.items()): print(k.ljust(32), v['material_class'].ljust(18), v['notes'][:70])
