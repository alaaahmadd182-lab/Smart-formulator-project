"""Automated identity extraction for every unique document of the incoming archive (read-only).

For each of the 4,186 unique documents it records, with the evidence text and page:
  * labelled product fields (product name / identifier / trade name ... in several languages; value on the same line or the next line),
  * brand + code tokens on page 1 (e.g. 'HiTEC 12200', 'OLOA 262', 'Priolube 2738', 'RF6163'),
  * company / manufacturer / supplier lines, and the supplier names recognised anywhere on pages 1-2,
  * the decoded file name when it is not a 'DL2-' number (weak hint only).
It then proposes ONE primary identity per document with a confidence:
  high   - a labelled product field agrees with a brand/code token or the title line,
  medium - a labelled field alone, or a brand/code token in the first lines of page 1,
  low    - file name or a single later mention only,
  none   - nothing identifiable (image without OCR text, empty, non-product paper).
Everything here is AUTOMATED and PROVISIONAL: it is a reading aid that the supplier batches confirm or correct
(decisions/*.json). Text source: the incoming inventory's text-layer cache, else the OCR cache of 01_ocr.py.
Output: tables/document_identity_auto.csv. Usage: python 02_identify.py
"""
import csv, gzip, json, os, re, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
sys.path.insert(0, os.path.join(INV, 'scripts'))

LABELS = (r'ghs product identifier|product identifier(?: used on the label)?|product name|name of (?:the )?product|trade ?name(?:/designation)?|'
          r'commercial (?:name|product name)|brand name|material name|product designation|product|material|sample name|sample|'
          r'produktname|handelsname|nom (?:du produit|commercial)|nombre (?:del producto|comercial)|nome (?:del prodotto|commerciale)|'
          r'产品名称|产品名|商品名称|品名|样品名称|製品名|商品名|제품명')
FIELD_SAME = re.compile(r'(?im)^[\s\d.]*(?:' + LABELS + r')\s*[:：]\s*(\S[^\n]{1,100})$')
FIELD_NOCOLON = re.compile(r'(?m)^[\s\d.]*(?i:product name|trade name|product identifier)\s{1,4}([A-Z0-9][^\n:]{1,60})$')
FIELD_NEXT = re.compile(r'(?im)^[\s\d.]*(?:' + LABELS + r')\s*[:：]?\s*$\n\s*(\S[^\n]{1,100})$')
COMPANY = re.compile(r'(?im)^[\s\d.]*(?:company(?: name)?|manufacturer|supplier|producer|company identification|details of the supplier[^\n]*|'
                     r'name of (?:the )?(?:company|supplier|manufacturer)|生产(?:厂家|商|企业)|供应商)\s*[:：]?\s*(\S[^\n]{2,90})?$')
BRANDS = (r'hitec|oloa|paratone|infineum|lubrizol|anglamol|additin|irganox|irgalube|irgamet|irgafos|irgaflo|viscoplex|viscotech|priolube|perfad|synative|'
          r'vanlube|molyvan|hostacor|durasyn|indopol|synfluid|spectrasyn|esterex|synesstic|nexbase|yubase|etro|risella|nyflex|nytex|nyfrost|hygold|hyprene|'
          r'purity|aramcoprima|aramcoultra|ultra[- ]?s|adbase|bapbase|kixx\s?lubo|naugalube|songnox|ethanox|na-sul|na-lube|k-corr|synnaph|aclube|geolube|'
          r'emkarox|emery|breox|plurasafe|polyglykol|ucon|dowsyn|chemtura|tianhe|dongfang|t\d{3}|kangtai|mingyue|my-t|goncord|elco|nycobase|ketjenlube|'
          r'lubricant additive|zddp|wx|kusa|yalub|bettchem|petrolad|thixocal|hitec|ecostar|cristol|plasmoil|fragol|lanxess|rhein chemie|ultrazol|'
          r'rf|pmae?|lz|bt|c-tec|pibsa|slf')
CODE = re.compile(r'(?i)(?<![A-Za-z0-9])((?:' + BRANDS + r')[\s®™]*[-\s]?[A-Z]{0,3}[\s-]?\d{2,6}[A-Z0-9+/-]{0,6})(?![A-Za-z0-9])')
DL2 = re.compile(r'(?i)^dl2-\d+')


def norm(x):
    x = re.sub(r'[®™©Ò]', ' ', str(x or ''))
    return re.sub(r'\s+', ' ', x).strip(' :-|')


def key(x):
    return re.sub(r'[^A-Z0-9+]', '', norm(x).upper())


def pages_for(sha):
    p = os.path.join(INV, '_cache', 'text', sha + '.txt.gz')
    tl = gzip.open(p, 'rt', encoding='utf-8').read().split('\f') if os.path.exists(p) else []
    o = os.path.join(PKG, '_cache', 'ocr', sha + '.json.gz')
    if os.path.exists(o):
        d = json.load(gzip.open(o, 'rt', encoding='utf-8'))
        for pg in d['pages']:
            i = pg['page'] - 1
            if pg['source'] != 'text_layer' and pg['text']:
                while len(tl) <= i:
                    tl.append('')
                if len(re.sub(r'\s', '', tl[i])) < 20:
                    tl[i] = pg['text']
        return tl, 'text layer + OCR' if any(pg['source'] == 'ocr' for pg in d['pages']) else 'text layer'
    return tl, 'text layer' if tl else 'none'


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    import importlib.util
    spec = importlib.util.spec_from_file_location('cc', os.path.join(INV, 'scripts', '03_classify_compare.py'))
    cc = importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)
    with open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8') as fh:
        U = list(csv.DictReader(fh))
    rows = []
    for r in U:
        pages, src = pages_for(r['sha256'])
        p1 = pages[0] if pages else ''
        first2 = '\n'.join(pages[:2])
        low2 = first2.lower()
        fields = []
        for rx in (FIELD_SAME, FIELD_NEXT, FIELD_NOCOLON):
            for m in rx.finditer(first2[:8000]):
                v = norm(m.group(1))
                if v and not re.match(r'(?i)^(?:code|number|no\.?|use|identifier|type|information|data|description|name|product(?: name| form| type| code| identifier)?|trade name|synonyms?)\b', v) and len(v) > 1:
                    fields.append(v)
        fields = list(dict.fromkeys(fields))[:4]
        lines = [norm(x) for x in p1.split('\n') if norm(x)]
        top = ' | '.join(lines[:12])
        codes = list(dict.fromkeys(norm(m.group(1)) for m in CODE.finditer(' \n'.join(lines[:40]))))[:6]
        comp = [norm(m.group(1)) for m in COMPANY.finditer(first2[:8000]) if m.group(1)][:2]
        sups = sorted({lab for lab, pat in cc.SUPPLIERS if re.search(pat, low2)})
        fname = urllib.parse.unquote(r['first_path'])
        fhint = '' if DL2.match(fname) else norm(re.sub(r'\.[A-Za-z0-9]{2,5}$', '', fname))
        # primary identity
        prim, conf, basis = '', 'none', ''
        fkeys = [key(f) for f in fields]
        code_in_field = next((c for c in codes if any(key(c) and key(c) in fk for fk in fkeys)), None)
        if fields and (code_in_field or any(key(f)[:6] and key(f)[:6] in key(top) for f in fields[:1])):
            prim, conf, basis = fields[0], 'high', 'labelled product field agrees with a page-1 title or code token'
        elif fields:
            prim, conf, basis = fields[0], 'medium', 'labelled product field only'
        elif codes:
            prim, conf, basis = codes[0], 'medium', 'brand/code token in the first lines of page 1'
        elif fhint:
            prim, conf, basis = fhint, 'low', 'file name only'
        else:
            basis = 'no identity found in the text read' if pages else 'no text (image without OCR text, or unread format)'
        rows.append(dict(sha256=r['sha256'], first_path=r['first_path'], copies_in_batch=r['copies_in_batch'], kind=r['kind'], pages=r['pages'],
                         text_source=src, document_type_provisional=r['document_type'], document_subtype_provisional=r['document_subtype'],
                         supplier_provisional=r['supplier_provisional'], suppliers_named_p1_2='; '.join(sups), company_lines='; '.join(comp)[:200],
                         labelled_fields='; '.join(fields)[:300], code_tokens_p1='; '.join(codes)[:200], filename_hint=fhint[:120], top_lines=top[:400],
                         primary_identity=prim[:120], primary_key=key(prim)[:80], identity_confidence=conf, identity_basis=basis,
                         byte_duplicate_of_existing=r['byte_duplicate_of_existing'], existing_products_auto=r['existing_products']))
    cols = list(rows[0].keys())
    with open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(len(rows), Counter(r['identity_confidence'] for r in rows), Counter(r['text_source'] for r in rows))


if __name__ == '__main__':
    main()
