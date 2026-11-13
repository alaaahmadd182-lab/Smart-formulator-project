"""Incoming dataset inventory, pass 3: classify every file, compare with the existing sources and products, list leads
(read-only; nothing is ingested, and no production file is read for writing).

Inputs: _cache/members.jsonl and _cache/text/ (pass 1), _cache/reference.json and _cache/ref_text/ (pass 2),
reports/data_policy/document_classes.csv (classes of the existing cited pages; read only).

EVERY classification made here is AUTOMATED and PROVISIONAL unless its basis column says otherwise:
  document type     from phrases on the first two pages (the matched phrase is recorded). No phrase -> unresolved.
  supplier          from supplier names / trade names on the first two pages (all hits are recorded). Not a reading.
  product as printed  the text of a 'Product name' / 'Trade name' / 'Product:' field where one is printed; otherwise
                    the first lines of the first page are kept as title_lines and no product is asserted.
  existing product  a product of Products_json is linked to a document only when its exact name - every token and
                    grade suffix, bounded so that '12204' never matches '12204L' - is printed in the document's product
                    field or title lines AND the document also names the product's supplier. Level:
                      name_in_product_field_and_supplier   strongest automated level (still not a human reading)
                      name_in_title_lines_and_supplier
                      name_on_first_pages_and_supplier     the name occurs on page 1-2 outside the field/title
                    A name that occurs only deeper in the text, or without the supplier, is a mention, not a match.
                    File names are never used for matching.
  byte duplicate    SHA-256 equality (exact).
  same text         equality of the SHA-256 of the whitespace-normalised extracted text of all pages (exact for the
                    text layer; says nothing about images or layout). Only for documents with >= 200 text characters.
An image-only file was NOT read (no OCR engine is installed). It is reported as unread, never as empty.

Usage: python incoming_dataset_review_2026-11-12/scripts/03_classify_compare.py
"""
import collections, csv, gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)
CACHE = os.path.join(BASE, '_cache')
TOP = 'Downloaded lubricants sheets/'

DOC_TYPES = [  # (subtype, class reported, phrases searched in the first two pages, in this order)
    ('certificate_of_analysis', 'other', r'certificate of analysis|certificate of quality|analysis certificate|inspection certificate|quality certificate|\bcoa\b|test report\b[\s\S]{0,200}batch'),
    ('shipping_or_commercial', 'other', r'packing list|delivery note|bill of lading|commercial invoice|proforma invoice|purchase order|certificate of origin|to whom it may concern'),
    ('safety_data_sheet', 'SDS', r'safety data sheet|material safety data|\bmsds\b|sicherheitsdatenblatt|fiche de donn[ée]es de s[ée]curit|ficha de datos de seguridad|section 1[.:]? identification|hazards? identification'),
    ('formulation_or_performance_data', 'other', r'candidate data package|\bcdp\b|bench test performance|oil code|formulation (?:guide|data|details)|blend(?:ing)? (?:study|formulation)|engine test (?:results|summary)|performance data package|this report contains engine testing|\bip report no|properties and performance in lubricants'),
    ('technical_or_product_data_sheet', 'TDS/PDS', r'technical data sheet|product data sheet|product datasheet|technical datasheet|product information|technical information|t ?e ?c ?h ?n ?i ?c ?a ?l d ?a ?t ?a|product bulletin|product specification|sales specification|selling spec|typical properties|typical characteristics|typical inspections|typical data|\btds\b|\bpds\b|data sheet|specification|product introduction'),
    ('brochure_or_presentation', 'brochure', r'brochure|product (?:range|portfolio|guide|catalog(?:ue)?)|portfolio|presentation|solutions for|confidential and proprietary|confidential information|company introduct|all rights reserved'),
]
SUPPLIERS = [  # (supplier label, pattern). Trade names are included because many sheets print only the brand.
    ('Afton Chemical', r'afton|hitec\s*®?\s*\d'), ('Lubrizol', r'lubrizol|ultrazol|anglamol'), ('Infineum', r'infineum'),
    ('Chevron Oronite', r'oronite|oloa\s*®?\s*\d|paratone'), ('Chevron Phillips Chemical', r'chevron phillips|synfluid'),
    ('Chevron (base oils)', r'chevron (?:base oil|neutral oil|products company|lubricants)|chevron\b.{0,30}\b\d{3}r\b'),
    ('ExxonMobil', r'exxonmobil|exxon mobil|spectrasyn|esterex|synesstic'), ('BASF', r'\bbasf\b|irganox|irgalube|irgamet|irgaflo|breox|synative|plurasafe'),
    ('Clariant', r'clariant|hostacor|polyglykol'), ('LANXESS / Rhein Chemie', r'lanxess|rhein chemie|additin'),
    ('Vanderbilt Chemicals', r'vanderbilt|vanlube|molyvan|cuvan'), ('BRB International', r'\bbrb\b|viscotech|petrolad|thixocal'),
    ('Richful', r'richful|\brf\s?\d{4}[a-z]?\b'), ('INEOS', r'\bineos\b|durasyn|indopol'), ('Evonik', r'evonik|viscoplex|viscobase'),
    ('Croda', r'\bcroda\b|priolube|perfad'), ('Neste', r'\bneste\b|nexbase'), ('SK (YUBASE)', r'yubase|sk lubricants|sk enmove'),
    ('S-OIL', r's-oil|ultra-s\b|aramcoultra'), ('PETRONAS', r'petronas|\betro\s?\d'), ('Shell', r'\bshell\b|risella'), ('Nynas', r'\bnynas\b|nyfrost|nytex|nyflex'),
    ('Ergon', r'\bergon\b|hygold|hyprene'), ('Petro-Canada', r'petro-canada|purity\s?(?:vhvi|\d)'), ('Saudi Aramco / Luberef', r'aramco|luberef'),
    ('ADNOC', r'\badnoc\b|adbase'), ('Bapco', r'\bbapco\b|bapbase'), ('Formosa Petrochemical', r'formosa'), ('GS Caltex', r'gs caltex|kixx lubo'),
    ('Sama Lubricants', r'samalubricants|sama lubricants'), ('Lubimax / Coraplus', r'lubimax|coraplus'), ('Tianhe Chemicals', r'tianhe'),
    ('Minglan Chemical', r'minglan'), ('Eni', r'\beni\b spa|\beni mx\b|\beni\b'), ('Dow', r'\bdow\b|dowsyn|\bucon\b'), ('Italmatch', r'italmatch'),
    ('King Industries', r'king industries|na-sul|k-corr|na-lube'), ('Dorf Ketal', r'dorf ketal'), ('Wuxi South Petroleum Additive', r'wxnfcn|\bwx\s?\d{4}'),
    ('Goncord', r'goncord'), ('FRAGOL', r'fragol'), ('Pertamina', r'pertamina'), ('Indian Additives', r'indian additives'), ('TotalEnergies', r'totalenergies|\btotal\b (?:lubrifiants|additifs)'),
    ('Hyrax Oil', r'hyrax'), ('Bettchem', r'bettchem'), ('Jinzhou Donggong', r'jinzhou'), ('KangTai', r'kangtai'), ('Sasol', r'\bsasol\b'), ('H&R', r'h&r (?:group|wasag)|hansen & rosenthal'),
    ('Repsol', r'repsol'), ('Kemipex', r'kemipex'), ('Functional Products', r'functional products'), ('Chemtura / SI Group', r'chemtura|si group|naugalube'),
    ('Yasho Industries', r'yasho|yalub'), ('Kusa Chemicals', r'kusa chem'), ('Songwon', r'songwon|songnox'), ('Kraton', r'kraton'),
    ('Elco', r'\belco\b'), ('NYCO', r'nycobase|\bnyco\b'), ('Tanee Chemical', r'tanee'), ('Plasmoil', r'plasmoil'), ('Cristol', r'cristol'),
    ('Shenyang Great Wall', r'shenyang great wall'), ('Mingyue', r'mingyue|\bmy-t\d'), ('Turkmenbashy refinery', r'turkmenbashy'),
    ('Solvay', r'\bsolvay\b'), ('Huntsman', r'huntsman'), ('Arkema', r'arkema'), ('Emery / Oleon', r'emery oleochemicals|\boleon\b'), ('Tree Trading', r'tree trading'),
]
PRODUCT_SUPPLIER_KEY = [  # supplier text of a product record -> pattern the document must also contain
    ('afton', r'afton|hitec'), ('lubrizol', r'lubrizol'), ('infineum', r'infineum'), ('oronite', r'oronite|oloa'), ('chevron phillips', r'chevron phillips|synfluid'),
    ('chevron', r'chevron'), ('exxon', r'exxon'), ('petro-canada', r'petro-canada|petro canada'), ('ergon', r'ergon'), ('nynas', r'nynas'), ('s-oil', r's-oil'),
    ('aramco', r'aramco|luberef'), ('richful', r'richful'), ('petronas', r'petronas'), ('caltex', r'caltex'), ('adnoc', r'adnoc'), ('neste', r'neste'),
    ('yubase', r'yubase|sk '), ('bapco', r'bapco'), ('bettchem', r'bettchem'), ('formosa', r'formosa'), ('shell', r'shell'), ('indian additives', r'indian additives'),
    ('eni', r'\beni\b'), ('minglan', r'minglan'), ('brb', r'\bbrb\b'), ('jinzhou', r'jinzhou'), ('kangtai', r'kangtai'), ('mingyue', r'mingyue'), ('tianhe', r'tianhe'),
    ('tree trading', r'tree trading'),
]
FIELD = re.compile(r'(?im)^\s*(?:ghs product identifier|product identifier(?: used on the label)?|product name|trade ?name(?:/designation)?|commercial name|product|material name|material|product description)\s*[:：]\s*(\S[^\n]{1,90})$')
DATE_LABEL = re.compile(r'(?i)(revision date|date of revision|revised(?: on)?|date ?/ ?revised|issue date|date of issue|issued|version date|effective(?: date)?|published on|edition date|print date|date of print|sds date|version|revision(?: no\.?| number)?|ver\.|date)\s*[:.]?\s*([0-9A-Za-z][0-9A-Za-z ,./\-]{3,28})')
HAS_DATE = re.compile(r'(?:19|20)\d{2}|\b\d{1,2}[./-]\d{1,2}[./-]\d{2}\b')
LEADS = [  # (topic, label, pattern)
    ('HiTEC 12204L / 8788B', 'HiTEC 12204L', r'hitec\W{0,3}12204\W?l\b'), ('HiTEC 12204L / 8788B', 'HiTEC 8788B', r'hitec\W{0,3}8788\W?b\b'),
    ('HiTEC 12204L / 8788B', 'HiTEC 12250 (booster of the 12204L premix)', r'hitec\W{0,3}12250\b'),
    ('pending source selection', 'NEXBASE 3043 / 3050 / 3060 / 3080', r'nexbase\W{0,3}30(?:43|50|60|80)\b'), ('pending source selection', 'PETRONAS ETRO 4', r'\betro\W{0,2}4\b(?!\s*\+)'),
    ('pending source selection', 'aramcoPRIMA 110 / 230 / 500', r'prima\W{0,3}(?:110|230|500)\b'), ('pending source selection', 'Formosa 150N / 500N', r'formosa[\s\S]{0,400}?\b(?:150|500)\s?n\b'),
    ('pending source selection', 'Richful RF6066 / RF6069', r'\brf\s?606[69]\b'), ('pending source selection', 'Lubrizol CV2301', r'\bcv\s?2301\b'),
    ('co-component dose / route', 'Infineum D3354 / D3384 / D3451', r'\bd\s?3(?:354|384|451)\b'), ('co-component dose / route', 'Lubrizol 3589C / 3700 / 3700D', r'lubrizol\W{0,3}(?:3589c|3700d?)\b'),
    ('co-component dose / route', 'Lubrizol CV1100 / CV1103', r'\bcv\s?110[03]\b'), ('co-component dose / route', 'Infineum SV261', r'\bsv\s?261\b'),
    ('co-component dose / route', 'Infineum boosters D2332 / D2333 / D2334 / D2353 / D2358 / D2359 / D2367 / C9274', r'\b(?:d\s?23(?:32|33|34|53|58|59|67)|c\s?9274)\b'),
    ('co-component dose / route', 'Lubrizol CV6320', r'\bcv\s?6320\b'), ('co-component dose / route', 'Lubrizol 7077 performance polymer', r'lubrizol\W{0,3}7077'),
    ('co-component dose / route', 'HiTEC 5748 (viscosity modifier)', r'hitec\W{0,3}5748'),
]
FORMULATION = re.compile(r'(?i)(?:viscosity (?:modifier|index improver)|\bvii?\b)[\s\S]{0,400}?(?:base (?:stock|oil)|group i{1,3})[\s\S]{0,400}?(?:%|wt|mass)')


def norm_name(x):
    return re.sub(r'\s+', ' ', re.sub(r'[®™©]', ' ', str(x or ''))).strip()


def alias_regex(name):
    """Regex for an exact product name: every token and suffix, tolerant only of spacing / hyphen / trademark signs."""
    toks = re.findall(r'[A-Za-z0-9+]+', norm_name(name))
    if not toks:
        return None
    body = r'[\s\-®™]*'.join(re.escape(t) for t in toks)
    return re.compile(r'(?<![A-Za-z0-9])' + body + r'(?![A-Za-z0-9+])', re.I)


def read_text(folder, sha):
    p = os.path.join(CACHE, folder, sha + '.txt.gz')
    if not os.path.exists(p):
        return ''
    with gzip.open(p, 'rt', encoding='utf-8') as fh:
        return fh.read()


def write(rel, rows, cols):
    p = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({c: ('' if r.get(c) is None else r.get(c)) for c in cols})
    return len(rows)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    with open(os.path.join(CACHE, 'members.jsonl'), encoding='utf-8') as fh:
        members = [json.loads(l) for l in fh]
    with open(os.path.join(CACHE, 'reference.json'), encoding='utf-8') as fh:
        ref = json.load(fh)
    ex_by_sha = collections.defaultdict(list)
    for m in ref['archive']['members']:
        ex_by_sha[m['sha256']].append(m)
    ex_by_text = collections.defaultdict(list)
    for m in ref['archive']['members']:
        if m.get('text_sha256') and m.get('text_chars', 0) >= 200:
            ex_by_text[m['text_sha256']].append(m)
    local_sha = {e['sha256']: e['path'] for e in ref['local_evidence']}
    reg_sha = {e['sha256']: e['url'] for e in ref['registry']}
    cited = ref['cited_files']
    ex_class = collections.defaultdict(set)
    with open(os.path.join(ROOT, 'reports', 'data_policy', 'document_classes.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            ex_class[r['file']].add(r['class'])
    products = []
    for p in ref['products']:
        name = norm_name(p['product_name'])
        core = re.sub(r'(?i)\s+(performance additive|additive package|package)$', '', name)
        sup = str(p['supplier'] or '').lower()
        key = next((pat for k, pat in PRODUCT_SUPPLIER_KEY if k in sup), None)
        if not key and p['product_id'].startswith(('HiTEC', 'AFTON')):
            key = r'afton|hitec'
        products.append(dict(p, name=core, rx=alias_regex(core), supplier_rx=re.compile(key, re.I) if key else None))
    files_of_product = collections.defaultdict(set)
    for f, pids in cited.items():
        for pid in pids:
            files_of_product[pid].add(f)

    by_sha = collections.defaultdict(list)
    for m in members:
        by_sha[m['sha256']].append(m)
    docs, matches, leads = [], [], []
    for sha, group in by_sha.items():
        m = group[0]
        text = read_text('text', sha) if m['text_chars'] else ''
        pages = text.split('\f') if text else []
        first2 = '\n'.join(pages[:2])
        low2 = first2.lower()
        lines = [l.strip() for l in (pages[0] if pages else '').splitlines() if l.strip()]
        title = ' ¦ '.join(lines[:6])[:300]
        subtype, cls, basis = 'unresolved', 'unresolved', ''
        sample = re.sub(r'\s', '', first2[:3000])
        legible = not sample or sum(ch.isalpha() for ch in sample) / len(sample) >= 0.5
        if m['text_chars'] >= 40 and not legible:
            basis = 'text layer present but not legible (encoded font, or mostly numbers and symbols): not machine-read; type not established'
            first2 = low2 = ''
            lines, title = [], '(text layer not legible)'
        elif m['text_chars'] >= 40:
            for st, c, pat in DOC_TYPES:
                hit = re.search(pat, low2)
                if hit:
                    subtype, cls, basis = st, c, f'phrase {hit.group(0)!r} on page 1-2 (automated, provisional)'
                    break
            else:
                basis = 'text layer present, no document-type phrase recognised on page 1-2'
        else:
            basis = 'no usable text layer: not machine-read (no OCR); type not established'
        sup_hits = [(re.search(pat, low2).start(), lab) for lab, pat in SUPPLIERS if re.search(pat, low2)]
        sup_hits.sort()
        field = FIELD.search(first2)
        printed = norm_name(field.group(1))[:90] if field else ''
        dates = []
        for dm in DATE_LABEL.finditer(first2[:6000]):
            if HAS_DATE.search(dm.group(2)) or dm.group(1).lower().startswith(('version', 'revision', 'ver')):
                dates.append(f'{dm.group(1).strip()}: {dm.group(2).strip()}')
            if len(dates) >= 3:
                break
        ex_same = ex_by_sha.get(sha, [])
        ex_text = [] if ex_same else (ex_by_text.get(m['text_sha256'], []) if m['text_sha256'] and m['text_chars'] >= 200 else [])
        doc = dict(sha256=sha, copies_in_batch=len(group), paths=' | '.join(g['path'][len(TOP):] for g in group), first_path=m['path'][len(TOP):],
                   kind=m['kind'], size=m['size'], pages=m['pages'], pages_with_text=m['pages_with_text'], readability=m['readability'],
                   text_chars=m['text_chars'], text_sha256=m['text_sha256'], document_type=cls, document_subtype=subtype, type_basis=basis,
                   supplier_provisional=sup_hits[0][1] if sup_hits else '', supplier_all_hits='; '.join(dict.fromkeys(l for _, l in sup_hits)),
                   product_as_printed=printed, title_lines=title, printed_dates='; '.join(dates), pdf_creation_date=m['meta_creation'],
                   byte_duplicate_of_existing='; '.join(x['name'] for x in ex_same), same_text_as_existing='; '.join(x['name'] for x in ex_text),
                   local_evidence_copy=local_sha.get(sha, ''), registry_source=reg_sha.get(sha, ''), existing_products='', relationship='')
        # ---- existing product identities
        linked = {}
        for x in ex_same:   # exact copy of a file the records already cite: the link is the existing citation
            for pid in cited.get(x['name'], []):
                linked[pid] = 'byte_identical_to_cited_source'
        for x in ex_text:
            for pid in cited.get(x['name'], []):
                linked.setdefault(pid, 'same_text_as_cited_source')
        zone_field, zone_title = printed, ' '.join(lines[:6])
        for p in products:
            if not p['rx'] or not p['supplier_rx'] or not low2:
                continue
            if not p['supplier_rx'].search(first2):
                continue
            if zone_field and p['rx'].search(zone_field):
                lvl = 'name_in_product_field_and_supplier'
            elif p['rx'].search(zone_title):
                lvl = 'name_in_title_lines_and_supplier'
            elif p['rx'].search(first2):
                lvl = 'name_on_first_pages_and_supplier'
            else:
                continue
            linked.setdefault(p['product_id'], lvl)
        for pid, lvl in sorted(linked.items()):
            have = sorted(files_of_product.get(pid, []))
            same_class = [f for f in have if (cls == 'SDS' and 'SDS' in ex_class.get(f, ())) or (cls == 'TDS/PDS' and 'TECHNICAL' in ex_class.get(f, ()))]
            if lvl == 'byte_identical_to_cited_source':
                rel = 'exact byte duplicate of a source the product already cites'
            elif lvl == 'same_text_as_cited_source':
                rel = 'same extracted text as a cited source, different bytes'
            elif ex_same:
                rel = 'already in the existing archive (byte-identical file, not cited by a value of this product): not a new document'
            elif ex_text:
                rel = 'same extracted text as an existing archive file, different bytes: not a new document by its text'
            elif lvl == 'name_on_first_pages_and_supplier':
                # verified on samples 2026-11-12: this level also catches documents ABOUT another product that only mention
                # this one (for example a formulation sheet that lists it as a base oil). It is a mention, not a match.
                rel = 'mention only: the product is named on the first pages of a document that may be about another product (needs reading)'
            elif cls in ('SDS', 'TDS/PDS') and same_class:
                rel = 'different document of a class the product already cites: revision candidate (NOT assumed newer; provisional)'
            else:
                rel = 'additional evidence for an existing product (provisional)'
            matches.append(dict(product_id=pid, match_level=lvl, relationship=rel, sha256=sha, first_path=doc['first_path'], document_type=cls,
                                document_subtype=subtype, product_as_printed=printed, title_lines=title, printed_dates=doc['printed_dates'],
                                existing_cited_files='; '.join(have), existing_files_of_same_class='; '.join(same_class)))
        doc['existing_products'] = '; '.join(f'{pid} ({lvl})' for pid, lvl in sorted(linked.items()))
        if ex_same:
            doc['relationship'] = 'exact byte duplicate of an existing archive file'
        elif ex_text:
            doc['relationship'] = 'same extracted text as an existing archive file, different bytes'
        elif any(l in ('name_in_product_field_and_supplier', 'name_in_title_lines_and_supplier') for l in linked.values()):
            doc['relationship'] = 'names an existing product in its product field or title (automated match; provisional)'
        elif linked:
            doc['relationship'] = 'mentions an existing product on its first pages (weak; may be about another product)'
        elif m['text_chars'] < 40 or not legible:
            doc['relationship'] = 'unresolved: not machine-read'
        elif not printed and not sup_hits:
            doc['relationship'] = 'unresolved: no product field and no known supplier recognised'
        else:
            doc['relationship'] = 'no existing product identified: other product or material (provisional; not a reading)'
        docs.append(doc)
        # ---- leads (all pages)
        if text:
            lowp = [p.lower() for p in pages]
            for topic, label, pat in LEADS:
                rx = re.compile(pat, re.I)
                hit_pages = [i + 1 for i, p in enumerate(lowp) if rx.search(p)]
                if hit_pages:
                    i = hit_pages[0] - 1
                    mm = rx.search(lowp[i])
                    snip = re.sub(r'\s+', ' ', pages[i][max(0, mm.start() - 110): mm.end() + 150]).strip()
                    leads.append(dict(topic=topic, lead=label, sha256=sha, first_path=doc['first_path'], document_type=cls, document_subtype=subtype,
                                      supplier_provisional=doc['supplier_provisional'], pages_with_hit=','.join(map(str, hit_pages[:12])),
                                      n_pages_with_hit=len(hit_pages), already_in_existing_archive='yes' if ex_same else 'no', snippet=snip[:300],
                                      status='lead only: not verified, no record changed'))
            if subtype == 'formulation_or_performance_data' or FORMULATION.search(text[:20000]):
                named = sorted({p['product_id'] for p in products if p['material_class'] == 'additive_package' and p['rx'] and p['rx'].search(text[:20000])
                                and p['supplier_rx'] and p['supplier_rx'].search(text[:20000])})
                if subtype == 'formulation_or_performance_data' or named:
                    leads.append(dict(topic='possible finished-oil formulation or performance data', lead='; '.join(named) or '(no existing package named)',
                                      sha256=sha, first_path=doc['first_path'], document_type=cls, document_subtype=subtype,
                                      supplier_provisional=doc['supplier_provisional'], pages_with_hit='', n_pages_with_hit='',
                                      already_in_existing_archive='yes' if ex_same else 'no', snippet=title[:300], status='lead only: not verified, no record changed'))

    # ---------------------------------------------------------------- outputs
    doc_of = {d['sha256']: d for d in docs}
    manifest = []
    for m in sorted(members, key=lambda x: x['path']):
        d = doc_of[m['sha256']]
        manifest.append(dict(archive_path=m['path'], filename=m['path'][len(TOP):], extension=m['extension'], file_type_by_content=m['kind'], size_bytes=m['size'],
                             crc32=m['crc32'], sha256=m['sha256'], pdf_pages=m['pages'], pdf_pages_with_text=m['pages_with_text'], readability=m['readability'],
                             image_size=m['image_size'], copies_of_this_hash_in_batch=d['copies_in_batch'], document_type=d['document_type'],
                             document_subtype=d['document_subtype'], type_basis=d['type_basis'], supplier_provisional=d['supplier_provisional'],
                             product_as_printed=d['product_as_printed'], title_lines=d['title_lines'], printed_dates=d['printed_dates'],
                             pdf_creation_date=m['meta_creation'], relationship=d['relationship'], existing_products=d['existing_products']))
    n = {}
    n['file_manifest'] = write('manifest/file_manifest.csv', manifest, list(manifest[0]))
    write('tables/unique_documents.csv', sorted(docs, key=lambda d: d['first_path']), list(docs[0]))
    dup = [dict(sha256=s, copies=len(g), size_bytes=g[0]['size'], redundant_copies=len(g) - 1, paths=' | '.join(x['path'][len(TOP):] for x in g),
                document_type=doc_of[s]['document_type'], title_lines=doc_of[s]['title_lines']) for s, g in by_sha.items() if len(g) > 1]
    n['dup_groups'] = write('tables/duplicate_groups_within_batch.csv', sorted(dup, key=lambda r: -r['copies']), list(dup[0]) if dup else ['sha256'])
    exd = [dict(new_file=m['path'][len(TOP):], sha256=m['sha256'], existing_archive_member=' | '.join(x['path'] for x in ex_by_sha[m['sha256']]),
                same_filename='yes' if m['path'][len(TOP):] in {x['name'] for x in ex_by_sha[m['sha256']]} else 'no',
                cited_by_products='; '.join(sorted({pid for x in ex_by_sha[m['sha256']] for pid in cited.get(x['name'], [])})))
           for m in sorted(members, key=lambda x: x['path']) if m['sha256'] in ex_by_sha]
    n['dup_existing_files'] = write('tables/duplicates_of_existing_archive.csv', exd, list(exd[0]) if exd else ['new_file'])
    tx = collections.defaultdict(list)
    for d in docs:
        if d['text_sha256'] and d['text_chars'] >= 200:
            tx[d['text_sha256']].append(d)
    same_text = []
    for t, g in tx.items():
        exm = ex_by_text.get(t, [])
        ex_other = [x for x in exm if x['sha256'] not in {d['sha256'] for d in g}]
        if len(g) > 1 or ex_other:
            same_text.append(dict(text_sha256=t, new_documents=len(g), new_paths=' | '.join(d['first_path'] for d in g), sizes=' | '.join(str(d['size']) for d in g),
                                  existing_archive_members_with_same_text=' | '.join(x['name'] for x in ex_other), text_chars=g[0]['text_chars'],
                                  document_type=g[0]['document_type'], title_lines=g[0]['title_lines'],
                                  basis='identical whitespace-normalised text layer of all pages; images and layout not compared'))
    n['same_text_groups'] = write('tables/same_text_different_bytes.csv', sorted(same_text, key=lambda r: -r['new_documents']), list(same_text[0]) if same_text else ['text_sha256'])
    n['product_matches'] = write('tables/existing_product_matches.csv', sorted(matches, key=lambda r: (r['product_id'], r['first_path'])), list(matches[0]))
    rev = [r for r in matches if r['relationship'].startswith('different document of a class')]
    n['revision_candidates'] = write('tables/revision_candidates.csv', sorted(rev, key=lambda r: (r['product_id'], r['first_path'])), list(matches[0]))
    n['leads'] = write('tables/evidence_leads.csv', sorted(leads, key=lambda r: (r['topic'], r['lead'], r['first_path'])), list(leads[0]) if leads else ['topic'])
    unread = [d for d in docs if d['document_type'] == 'unresolved' or d['relationship'].startswith('unresolved')]
    n['unreadable_or_unclassified'] = write('tables/unreadable_or_unclassified.csv', sorted(unread, key=lambda d: d['first_path']),
                                            ['first_path', 'sha256', 'kind', 'size', 'pages', 'pages_with_text', 'readability', 'text_chars', 'document_type',
                                             'type_basis', 'supplier_provisional', 'title_lines', 'relationship', 'copies_in_batch'])
    new_sha = set(by_sha)
    cov = [dict(existing_member=m['path'], sha256=m['sha256'], in_new_batch='yes' if m['sha256'] in new_sha else 'no',
                cited_by_products='; '.join(cited.get(m['name'], []))) for m in ref['archive']['members']]
    write('tables/existing_archive_coverage.csv', cov, list(cov[0]))
    sup = collections.defaultdict(lambda: collections.Counter())
    for d in docs:
        s = d['supplier_provisional'] or '(no supplier recognised)'
        sup[s]['unique_documents'] += 1
        sup[s][d['document_type']] += 1
        sup[s]['subtype:' + d['document_subtype']] += 1
        sup[s]['byte_duplicates_of_existing'] += bool(d['byte_duplicate_of_existing'])
        sup[s]['names_existing_product'] += bool(d['existing_products'])
        sup[s]['image_only_or_unread'] += d['relationship'] == 'unresolved: not machine-read'
    srows = [dict(supplier_provisional=s, unique_documents=c['unique_documents'], tds_pds=c['TDS/PDS'], sds=c['SDS'], brochure=c['brochure'], other=c['other'],
                  unresolved=c['unresolved'], certificates_of_analysis=c['subtype:certificate_of_analysis'], shipping_or_commercial=c['subtype:shipping_or_commercial'],
                  formulation_or_performance_data=c['subtype:formulation_or_performance_data'], byte_duplicates_of_existing=c['byte_duplicates_of_existing'],
                  documents_naming_an_existing_product=c['names_existing_product'], image_only_or_unread=c['image_only_or_unread']) for s, c in sup.items()]
    write('tables/supplier_summary.csv', sorted(srows, key=lambda r: -r['unique_documents']), list(srows[0]))

    C = collections.Counter
    stats = dict(
        files=len(members), unique_hashes=len(by_sha), redundant_copies_within_batch=len(members) - len(by_sha), duplicate_groups=len(dup),
        file_types=dict(C(m['kind'] for m in members)), readability_files=dict(C(m['readability'] for m in members)), pdf_pages=sum(m['pages'] or 0 for m in members),
        document_type_unique=dict(C(d['document_type'] for d in docs)), document_subtype_unique=dict(C(d['document_subtype'] for d in docs)),
        document_type_files=dict(C(doc_of[m['sha256']]['document_type'] for m in members)),
        files_byte_identical_to_existing_archive=len(exd), unique_documents_byte_identical_to_existing=sum(1 for d in docs if d['byte_duplicate_of_existing']),
        existing_archive_members=len(ref['archive']['members']), existing_archive_unique_hashes=len(ex_by_sha),
        existing_archive_unique_hashes_present_in_new_batch=len(set(ex_by_sha) & new_sha),
        same_text_groups=len(same_text), same_text_groups_involving_existing=sum(1 for r in same_text if r['existing_archive_members_with_same_text']),
        local_evidence_copies=sum(1 for d in docs if d['local_evidence_copy']), registry_hash_matches=sum(1 for d in docs if d['registry_source']),
        relationship_unique=dict(C(d['relationship'] for d in docs)),
        match_rows=len(matches), match_levels=dict(C(r['match_level'] for r in matches)), match_relationships=dict(C(r['relationship'] for r in matches)),
        existing_products_linked=len({r['product_id'] for r in matches}), existing_products_total=len(products),
        existing_products_linked_by_new_document=len({r['product_id'] for r in matches if not r['match_level'].startswith(('byte', 'same_text'))}),
        existing_products_with_new_document_naming_them_in_field_or_title=len({r['product_id'] for r in matches if r['match_level'] in
                                                                             ('name_in_product_field_and_supplier', 'name_in_title_lines_and_supplier')}),
        new_documents_naming_existing_product_in_field_or_title=len({r['sha256'] for r in matches if r['match_level'] in
                                                                   ('name_in_product_field_and_supplier', 'name_in_title_lines_and_supplier')}),
        existing_products_with_byte_identical_source=len({r['product_id'] for r in matches if r['match_level'] == 'byte_identical_to_cited_source'}),
        documents_naming_existing_product=len({r['sha256'] for r in matches}),
        documents_naming_more_than_one_existing_product=sum(1 for s, k in C(r['sha256'] for r in matches).items() if k > 1),
        suppliers_recognised=len([s for s in sup if not s.startswith('(')]), documents_without_recognised_supplier=sup['(no supplier recognised)']['unique_documents'],
        distinct_printed_product_names_not_linked=len({d['product_as_printed'].lower() for d in docs if d['product_as_printed'] and not d['existing_products']}),
        leads=dict(C(r['topic'] for r in leads)), leads_by_label=dict(C(r['lead'] for r in leads if not r['topic'].startswith('possible'))),
        unreadable_or_unclassified=len(unread), tables=n)
    with open(os.path.join(BASE, 'tables', 'inventory_statistics.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
