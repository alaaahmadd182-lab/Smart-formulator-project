"""Supplier batches S25 Wuxi South Petroleum Additives (26 documents), S26 Functional Products Inc. (23), S27 Oleon (20).
Read: compact listings; page-1 text after the letterhead for every document (name + printed descriptor); for Functional
Products every product name in the full text with its sentence context; for Oleon the 'Chemical name' line and certificate header.

S25 Wuxi. Subject = printed code. The three web-page printouts (wxnfcn.cn, 7/3/2021) and two 'PRODUCT SPECIFICATION' sheets are
manufacturer documents. 'T109A' (web page) and 'WX109A' (specification, 'TBN 160 Calcium Alkyl Salicylate') are different printed
codes: NOT merged (possible alias, no document states it). DL2 'NOVAD B700' is a Multisol France (Brenntag group) product data
sheet filed under the Wuxi label: distributor / issuer Multisol France, manufacturer not printed. Existing: WUXI_WX3118, WUXI_WX3326.

S26 Functional Products. The SUBJECT is the product in the sheet title. Other products named in the text are linked as mentions
with the printed relation, never as subjects and never merged:
  'recommended alternative' (e.g. 'Where higher temperatures are encountered, FUNCTIONAL V-188 is recommended instead'),
  'combination partner' ('Combine with FUNCTIONAL MG-1000 or MG-3000'), 'variant named' ("FUNCTIONAL '515' VARIANTS: V-516"),
  'named in an example formulation' (RD-540, PD-585, V-521).
'Paratac XT' (TDS + SDS, manufacturer Functional Products, Inc. printed on the SDS) is a separate product from every FUNCTIONAL V-
grade. 'PARATAC 178' is described on a Tri-iso Inc. sheet (issuer / distributor Tri-iso; manufacturer not printed): it is NOT
merged with 'FUNCTIONAL V-178' (similar number only).

S27 Oleon. Subject = 'RADIALUBE nnnn' / 'RADIA nnnn'. RADIALUBE 7361, 7364 and 7563 all print 'Trimethylolpropane trioleate'
(same CAS No.): three separate products, not merged. Issuers kept apart: Oleon nv (Ertvelde) TDS / SDS, OLEON N.V. (Oelegem)
and Oleon Port Klang Sdn. Bhd. certificates. Esters -> class unresolved (base fluid vs component; no API group in the template).
Identity only. Writes decisions/s25_wuxi.json, s26_functional_products.json, s27_oleon.json."""
import re
from dec_common import rows, page_text, top, doc, prod, write

C, P, U = 'additive_component', 'additive_package', 'unresolved'

# ---------------------------------------------------------------- S25 Wuxi
SUP = 'Wuxi South Petroleum Additives Co., Ltd.'
EX = {'WX3118': 'WUXI_WX3118', 'WX3326': 'WUXI_WX3326'}
WEB = {'5e30e32799': ('T109A', "Salicylate: 'T109 Calcium Alkyl Salicylate is a lubricating detergent'"), 'ebb43ba4bb': ('T121', "Phenate: 'mid base sulfurized calcium phenate'"),
       '4a00566f32': ('T747', "Rust and Corrosion Inhibitors: 'alkenyl succinic acid half ester anti-rust additive'"), '4964b72473': ('WX8135', "High Temperature Antioxidants: '100% active liquid hindered Phenol antioxidant'"),
       '116d8a765d': ('WX109C', "'TBN320 Salicylate Detergent'"), '8107ef29d7': ('WX109A', "'TBN 160 Calcium Alkyl Salicylate'")}
D, PK = {}, {}
for r in rows(lambda s: s.startswith('Wuxi'), 's25_wuxi.json'):
    sha, p10, f = r['sha256'], r['sha256'][:10], top(r)
    if p10 == '2eb12e3fb8':
        k = 'MULTISOL:NOVAD B700'
        doc(D, sha, 'product data sheet (TDS/PDS)', 'Multisol France (Brenntag group)', [k], 'page-1 text', distributor='Multisol France', issuer='Multisol France',
            note="'NOVAD B700 is a performance additive package optimized to formulate single and multigrade gasoline and diesel ...'; filed under the Wuxi label by the automated supplier field; manufacturer not printed on page 1")
        prod(PK, k, 'NOVAD B700', 'Multisol France (distributor; manufacturer not printed)', P, "printed: 'performance additive package' for gasoline and diesel engine oils")
        continue
    if p10 in WEB:
        code, d = WEB[p10]
        typ = 'product specification' if p10 in ('116d8a765d', '8107ef29d7') else 'manufacturer web-page printout'
    else:
        i = f.index('WWW.WXNFCN.CN/EN')
        code, d = re.match(r'[A-Z]{1,2}\d{3,4}[A-Z]?', f[i + 1]).group(0), ' / '.join(f[i + 1:i + 3])
        typ = 'product data sheet (TDS/PDS)'
    k = 'WUXI:' + code
    doc(D, sha, typ, SUP, [k], 'page-1 text (code + printed descriptor)', manufacturer=SUP, issuer=SUP)
    prod(PK, k, code, SUP, P if re.search(r'(?i)package', d) else C, 'printed: ' + d, existing=EX.get(code, ''))
PK['WUXI:T109A']['notes'] += "; 'T109A' (web page) and 'WX109A' (specification) are different printed codes: not merged"
PK['WUXI:WX109A']['notes'] += "; not merged with 'T109A' (no document states the alias)"
write('s25_wuxi.json', 'S25 Wuxi South (identity)', '26 documents with provisional supplier Wuxi South Petroleum Additive', PK, D)

# ---------------------------------------------------------------- S26 Functional Products
SUP = 'Functional Products Inc.'
NAME = re.compile(r'(?i)FUNCTIONAL\s?([A-Z]{1,3})\s?[-–]\s?(\d{2,5}[A-Z]?)')
MENTION = {('1be2d23a7e', 'V-188'): 'mentioned (recommended alternative for higher temperatures)', ('4ffbc23159', 'V-188'): 'mentioned (recommended alternative for higher temperatures)',
           ('b4712b75f8', 'V-188'): 'mentioned (recommended alternative for higher temperatures)', ('b74cc4aee5', 'V-188'): 'mentioned (recommended alternative for higher temperatures)',
           ('09303daeb9', 'MG-1000'): 'mentioned (combination partner)', ('09303daeb9', 'MG-3000'): 'mentioned (combination partner)',
           ('9cdb4bbb9f', 'V-422'): 'mentioned (recommended alternative for moderate shear)', ('ab2af43a8b', 'MG-3000'): 'mentioned (recommended alternative for multi-grade gear oils)',
           ('936d2ea33a', 'PD-585'): 'mentioned (named co-additive with a printed dose range)', ('54b78a186a', 'V-584'): 'mentioned (recommended alternative when more tack is required)',
           ('54b78a186a', 'V-521'): 'mentioned (named in a treat-rate table heading)', ('54b78a186a', 'RD-540'): 'mentioned (named in an example formulation)',
           ('54b78a186a', 'V-516'): "mentioned (variant named under 'FUNCTIONAL 515 VARIANTS')"}
D, PK, DESC = {}, {}, {}
for r in rows(lambda s: s.startswith('Functional'), 's26_functional_products.json'):
    sha, p10 = r['sha256'], r['sha256'][:10]
    full = page_text(sha, 99)
    sds = 'SAFETY DATA SHEET' in full[:400]
    if p10 in ('b74cc4aee5', '5a5edff94d'):
        subj, d = 'PARATAC XT', "SDS: 'Product Use Tackifier - Lubricant Additive', 'Polymeric Hydrocarbon In Mineral Oil'; 'Manufacturer: Functional Products, Inc.'"
    elif p10 == '1449c15591':
        subj, d = 'PARATAC 178', "'tackifier based on a high molecular weight polyisobutylene (PIB) dissolved in oil' (Tri-iso Inc. sheet)"
    else:
        m = NAME.search(full)
        subj = f'FUNCTIONAL {m.group(1).upper()}-{m.group(2).upper()}'
        d = re.split(r'\s+APPLICATION:|\s+Chemical Family', full[m.end():m.end() + 140])[0].strip()
    keys, roles = ['FUNCTIONALPRODUCTS:' + subj], {'FUNCTIONALPRODUCTS:' + subj: 'subject'}
    for (p, g), role in MENTION.items():
        if p == p10:
            keys.append('FUNCTIONALPRODUCTS:FUNCTIONAL ' + g); roles[keys[-1]] = role
    tri = p10 == '1449c15591'
    doc(D, sha, 'SDS' if sds else 'product data sheet (TDS/PDS)', 'Tri-iso Inc. (distributor sheet)' if tri else SUP, keys, 'full text: title and every product name with its sentence', roles=roles,
        manufacturer='' if tri else SUP, distributor='Tri-iso Inc.' if tri else '', issuer='Tri-iso Inc.' if tri else SUP,
        note='manufacturer not printed on this sheet; not merged with FUNCTIONAL V-178' if tri else '')
    if not sds or subj not in DESC:
        DESC[subj] = d
for k in dict.fromkeys(p for v in D.values() for p in v['products']):
    n = k.split(':', 1)[1]
    d = DESC.get(n)
    if d is None:
        prod(PK, k, n, SUP, U, 'named only as an alternative / partner / variant on other products\' sheets: no document of its own in the batch (candidate detected only)',
             evidence='printed name in the text of another product\'s sheet')
    else:
        vm = re.search(r'(?i)viscosity (?:index|modifier)|V\.I\.', d)
        prod(PK, k, n, 'Tri-iso Inc. (distributor; manufacturer not printed)' if n == 'PARATAC 178' else SUP, C, 'printed: ' + d + (' (VM subtype)' if vm else ' (tackifier / thickener: component general)'))
write('s26_functional_products.json', 'S26 Functional Products (identity)', '23 documents with provisional supplier Functional Products', PK, D)

# ---------------------------------------------------------------- S27 Oleon
SUP = 'Oleon NV'
D, PK = {}, {}
for r in rows(lambda s: s.startswith('Emery'), 's27_oleon.json'):
    sha = r['sha256']
    t = page_text(sha, 2)
    name = re.sub(r'\s+', ' ', re.search(r'RADIA(?:LUBE)?\s?\d{4}[A-Z]?', t).group(0))
    k = 'OLEON:' + name
    if 'Safety Data Sheet' in t[:300]:
        typ, issuer = 'SDS', 'Oleon nv'
    elif 'Results of analys' in t:
        typ, issuer = 'certificate of analysis (batch)', 'Oleon Port Klang Sdn. Bhd.' if 'Port Klang' in t[:200] else 'OLEON N.V. (Oelegem)'
    else:
        typ, issuer = 'product data sheet (TDS/PDS)', 'Oleon nv (Ertvelde)'
    ed = re.search(r'Edition date: (\d{2}/\d{2}/\d{4})', t)
    doc(D, sha, typ, SUP, [k], 'page-1 text (name, chemical name, certificate header)', manufacturer=SUP, issuer=issuer, date=ed.group(1) if ed else '')
    ch = re.search(r'Chemical name : (.+?) (?:CAS No|EC no|Origin|Qualifications|IUPAC)', t)
    if k not in PK or (ch and 'Chemical name' not in PK[k]['notes']):
        PK.pop(k, None)
        prod(PK, k, name, SUP, U, ("printed 'Chemical name : " + ch.group(1) + "'; " if ch else '') + 'ester: base fluid vs component to confirm; base_oil template has no API group for esters')
for k in ('OLEON:RADIALUBE 7361', 'OLEON:RADIALUBE 7364', 'OLEON:RADIALUBE 7563'):
    PK[k]['notes'] += '; 7361 / 7364 / 7563 print the same chemical name: separate products, not merged'
write('s27_oleon.json', 'S27 Oleon (identity)', '20 documents with provisional supplier Emery / Oleon', PK, D)
