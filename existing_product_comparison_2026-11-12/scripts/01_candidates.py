"""Old-versus-new comparison, step 1: candidate relationships between existing products and the documents of the new
archive, from a search of the FULL extracted text (every page), read-only.

Inputs (read only): incoming_dataset_review_2026-11-12/_cache (extracted text and reference data of the inventory),
its tables/unique_documents.csv, and reports/data_policy/document_classes.csv.

A candidate is a (product, unique document) pair in which an exact identity of the product is printed somewhere in
the document. Exact means every token and grade suffix: 'HiTEC 12204' never matches 'HiTEC 12204L', 'ETRO 4' never
matches 'ETRO 4+' or 'ETRO 4 Plus', and where two products match at the same place the longer name wins. Names that
are too generic to search on their own ('150N', 'NS 3', 'M500', ...) count only when the supplier is named on the same
page. File names are never used.

The relationship written here is a SUGGESTION from the context of the hit pages. The reviewed relationship is recorded
in decisions/relationship_decisions.json and applied by step 2. Documents without a usable text layer cannot be
searched: they are listed in tables/unsearchable_documents.csv, and no absence is claimed for them.

Outputs: tables/product_identities.csv, tables/candidate_relationships.csv, tables/unsearchable_documents.csv
"""
import collections, csv, gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')

SUPPLIER_KEY = [('afton', r'afton|hitec'), ('lubrizol', r'lubrizol'), ('infineum', r'infineum'), ('oronite', r'oronite|oloa'),
                ('chevron phillips', r'chevron phillips|cpchem|synfluid'), ('chevron', r'chevron'), ('exxon', r'exxon'),
                ('petro-canada', r'petro-canada|petro canada'), ('ergon', r'ergon'), ('nynas', r'nynas'), ('s-oil', r's-oil|s oil'),
                ('aramco', r'aramco|luberef'), ('richful', r'richful'), ('petronas', r'petronas'), ('caltex', r'caltex|kixx'), ('adnoc', r'adnoc'),
                ('neste', r'neste'), ('yubase', r'yubase|\bsk\b'), ('bapco', r'bapco'), ('bettchem', r'bettchem'), ('formosa', r'formosa|fpcc'),
                ('shell', r'shell'), ('indian additives', r'indian additives'), ('eni', r'\beni\b'), ('minglan', r'minglan'), ('brb', r'\bbrb\b'),
                ('jinzhou', r'jinzhou'), ('kangtai', r'kangtai'), ('mingyue', r'mingyue'), ('tianhe', r'tianhe'), ('tree trading', r'tree trading'),
                ('wuxi', r'wuxi|wxnfcn'), ('sama', r'sama')]
ID_SUPPLIER = [('AFTON_', 'afton'), ('HiTEC_', 'afton'), ('WUXI_', 'wuxi'), ('SAMA_', 'sama'), ('RF6602', 'richful'), ('CHEVRON_OLOA', 'oronite'),
               ('CHEVRON_SYNFLUID', 'chevron phillips'), ('YUBASE', 'yubase'), ('JINZHOU_KANGTAI', 'kangtai')]
EXTRA_ALIASES = {  # reviewed alternative spellings of the SAME product (never of a neighbouring grade)
    'PETRONAS_ETRO_4_PLUS': ['ETRO 4 Plus'], 'PETRONAS_ETRO_6_PLUS': ['ETRO 6 Plus'],
    'S_OIL_ARAMCO_ULTRA_8': ['aramcoULTRA 8', 'Aramco Ultra 8'], 'FORMOSA_150N_GII_PLUS': ['150N GII+'], 'FORMOSA_500N_GII': ['500N GII'],
}
TAIL = re.compile(r'(?i)\s+(performance additive|additive package|package|base oil|polymethacrylate.*|c[fhijk]-4.*|ci-4.*|ck-4.*|acea.*|api .*|diesel engine.*|'
                  r'universal type.*|extended edi.*)$')


def norm_name(x):
    return re.sub(r'\s+', ' ', re.sub(r'[®™©]', ' ', str(x or ''))).strip()


def alias_regex(name):
    toks = re.findall(r'[A-Za-z0-9]+|\+', norm_name(name))
    if not toks:
        return None
    body = ''
    for i, t in enumerate(toks):
        body += (r'[\s\-®™/]*' if i else '') + re.escape(t)
    # not inside a longer token; not followed by a letter, digit, '+', or the word 'plus' (a different grade)
    return re.compile(r'(?<![A-Za-z0-9])' + body + r'(?![A-Za-z0-9+])(?!\s*(?:plus\b|\+))', re.I)


def identities(products):
    out = []
    for p in products:
        name = norm_name(p['product_name'])
        core = name.split('(')[0].strip() if not name.startswith('(') and '(' in name and not name.upper().startswith('WX') else name
        if p['product_id'].startswith('WUXI_'):
            core = name.split('(')[0]
        for _ in range(3):
            core = TAIL.sub('', core).strip()
        aliases = [core]
        m = re.fullmatch(r'(.*?)\s+cSt(\s+.*)?', core)
        if m:
            aliases.append((m.group(1) + (m.group(2) or '')).strip())
        if core.lower().startswith('chevron base oil '):
            aliases.append('Chevron ' + core.split()[-1])
        if core.lower().startswith('aramco'):
            aliases.append(re.sub(r'(?i)^aramco(prima|dura|ultra)', r'Aramco \1', core))
        aliases += EXTRA_ALIASES.get(p['product_id'], [])
        aliases = list(dict.fromkeys(a for a in aliases if a))
        sup = str(p['supplier'] or '').lower()
        skey = next((k for pre, k in ID_SUPPLIER if p['product_id'].startswith(pre)), None) or next((k for k, _ in SUPPLIER_KEY if k in sup), None)
        srx = dict(SUPPLIER_KEY).get(skey)
        generic = [a for a in aliases if len(re.sub(r'[^A-Za-z0-9]', '', a)) <= 6 and not re.search(r'(?i)hitec|oloa|yubase|etro|ehc', a)]
        out.append(dict(product_id=p['product_id'], material_class=p['material_class'], supplier=p['supplier'], product_name=p['product_name'],
                        aliases=aliases, generic_aliases=generic, supplier_key=skey or '', supplier_rx=re.compile(srx, re.I) if srx else None,
                        rxs=[(a, alias_regex(a), a in generic) for a in aliases]))
    return out


FORMULATION = re.compile(r'(?i)formulation|composition|treat(?:ed)? (?:rate|at)|blend(?:ed|ing)?\b|recipe|%\s?(?:wt|w/w|m\b|mass|b\.w)|wt\.?\s?%|mass\s?%|base (?:oil|stock)s?\b.{0,40}\d')
PROPERTY = re.compile(r'(?i)typical|specification|density|viscosity|flash point|pour point|base number|\btbn\b|sulfated ash|calcium|phosphorus|kv\s?100')
NUM = re.compile(r'\d+\.\d+')


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    with open(os.path.join(INV, '_cache', 'reference.json'), encoding='utf-8') as fh:
        ref = json.load(fh)
    with open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8') as fh:
        docs = list(csv.DictReader(fh))
    cited = ref['cited_files']
    files_of = collections.defaultdict(set)
    for f, pids in cited.items():
        for pid in pids:
            files_of[pid].add(f)
    ex_class = collections.defaultdict(set)
    with open(os.path.join(ROOT, 'reports', 'data_policy', 'document_classes.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            ex_class[r['file']].add(r['class'])
    ids = identities(ref['products'])
    os.makedirs(os.path.join(BASE, 'tables'), exist_ok=True)
    with open(os.path.join(BASE, 'tables', 'product_identities.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['product_id', 'material_class', 'supplier', 'product_name', 'search_aliases', 'aliases_needing_supplier_on_the_same_page', 'supplier_key'])
        for p in ids:
            w.writerow([p['product_id'], p['material_class'], p['supplier'], p['product_name'], ' | '.join(p['aliases']), ' | '.join(p['generic_aliases']), p['supplier_key']])
    # Reviewed exceptions to the same-page supplier rule (tenth pass): a generic alias is admitted only on the listed
    # pages of the listed document (by SHA-256) after a reviewer verified ownership and context; nothing else changes.
    with open(os.path.join(HERE, 'reviewed_generic_alias_pairs.json'), encoding='utf-8') as fh:
        reviewed_generic = {(x['product_id'], x['sha256']): set(x['pages']) for x in json.load(fh)['reviewed_pairs']}
    via_mapping = set()
    rows, unsearch = [], []
    for d in docs:
        legible = 'not legible' not in d['type_basis'] and int(d['text_chars']) >= 40
        if not legible:
            unsearch.append(dict(sha256=d['sha256'], first_path=d['first_path'], kind=d['kind'], pages=d['pages'], readability=d['readability'],
                                 byte_duplicate_of_existing=d['byte_duplicate_of_existing'],
                                 reason='no usable text layer (no OCR engine): not searched; nothing is concluded about its content'))
            continue
        with gzip.open(os.path.join(INV, '_cache', 'text', d['sha256'] + '.txt.gz'), 'rt', encoding='utf-8') as fh:
            pages = fh.read().split('\f')
        low_doc = '\n'.join(pages).lower()
        title_zone = ' '.join(l.strip() for l in pages[0].splitlines() if l.strip())[:400] + ' ' + d['product_as_printed']
        hits = collections.defaultdict(lambda: collections.defaultdict(list))   # pid -> page -> [(start, end, alias)]
        for p in ids:
            first = re.findall(r'[a-z0-9]+', p['aliases'][0].lower())
            if not any(re.findall(r'[a-z0-9]+', a.lower())[-1] in low_doc for a in p['aliases']):
                continue
            for i, t in enumerate(pages):
                for a, rx, generic in p['rxs']:
                    for m in rx.finditer(t):
                        if generic and not (p['supplier_rx'] and p['supplier_rx'].search(t)):
                            if i + 1 not in reviewed_generic.get((p['product_id'], d['sha256']), ()):
                                continue
                            via_mapping.add((p['product_id'], d['sha256']))
                        hits[p['product_id']][i].append((m.start(), m.end(), a))
        # the longer identity wins where two products match at the same place
        spans = [(i, s, e, pid) for pid, pg in hits.items() for i, lst in pg.items() for s, e, _ in lst]
        drop = set()
        for i, s, e, pid in spans:
            for j, s2, e2, pid2 in spans:
                if i == j and pid != pid2 and s2 <= s and e2 >= e and (e2 - s2) > (e - s):
                    drop.add((i, s, e, pid))
        by_id = {p['product_id']: p for p in ids}
        for pid, pg in hits.items():
            kept = {i: [(s, e, a) for s, e, a in lst if (i, s, e, pid) not in drop] for i, lst in pg.items()}
            kept = {i: v for i, v in kept.items() if v}
            if not kept:
                continue
            p = by_id[pid]
            in_title = any(rx.search(title_zone) for _, rx, _ in p['rxs'])
            sup_in_doc = bool(p['supplier_rx'] and p['supplier_rx'].search(low_doc))
            form_pages = [i + 1 for i in kept if FORMULATION.search(pages[i]) and len(NUM.findall(pages[i])) >= 4]
            prop_pages = []
            for i, lst in kept.items():
                s = lst[0][0]
                if PROPERTY.search(pages[i][max(0, s - 700): s + 900]):
                    prop_pages.append(i + 1)
            i0 = min(kept)
            s0, e0, _ = kept[i0][0]
            snippet = re.sub(r'\s+', ' ', pages[i0][max(0, s0 - 140): e0 + 220]).strip()
            have = sorted(files_of.get(pid, []))
            dup = d['byte_duplicate_of_existing']
            dup_cited = [x for x in dup.split('; ') if x in cited and pid in cited[x]] if dup else []
            cls = d['document_type']
            same_class = [f for f in have if (cls == 'SDS' and 'SDS' in ex_class.get(f, ())) or (cls == 'TDS/PDS' and 'TECHNICAL' in ex_class.get(f, ()))]
            if dup:
                sug = 'A' + ('' if dup_cited else ' (archive file not cited by a value of this product)')
            elif d['same_text_as_existing']:
                sug = 'B candidate'
            elif in_title and sup_in_doc and d['document_subtype'] == 'certificate_of_analysis':
                sug = 'E candidate (batch certificate)'
            elif in_title and sup_in_doc and same_class:
                sug = 'F candidate'
            elif in_title and sup_in_doc:
                sug = 'E candidate'
            elif form_pages:
                sug = 'D candidate'
            else:
                sug = 'C candidate'
            rows.append(dict(product_id=pid, material_class=p['material_class'], supplier_key=p['supplier_key'], sha256=d['sha256'], first_path=d['first_path'],
                             copies_in_batch=d['copies_in_batch'], document_type=cls, document_subtype=d['document_subtype'], doc_supplier_provisional=d['supplier_provisional'],
                             pages=d['pages'], hit_pages=','.join(str(i + 1) for i in sorted(kept)), n_hit_pages=len(kept),
                             aliases_matched=' | '.join(sorted({a for lst in kept.values() for _, _, a in lst})),
                             name_in_title_or_product_field='yes' if in_title else 'no', product_supplier_named_in_document='yes' if sup_in_doc else 'no',
                             formulation_context_pages=','.join(map(str, form_pages)), property_context_pages=','.join(map(str, prop_pages)),
                             byte_duplicate_of_existing=dup, duplicate_is_cited_by_this_product='yes' if dup_cited else ('no' if dup else ''),
                             same_text_as_existing=d['same_text_as_existing'], printed_dates=d['printed_dates'], title_lines=d['title_lines'][:200],
                             existing_cited_files='; '.join(have), existing_cited_files_same_class='; '.join(same_class), suggested_relationship=sug,
                             snippet=snippet[:380],
                             found_via='full-text search + reviewed generic-alias mapping (supplier not on the hit page; scripts/reviewed_generic_alias_pairs.json)'
                             if (pid, d['sha256']) in via_mapping else 'full-text search'))
    rows.sort(key=lambda r: (r['supplier_key'], r['product_id'], r['first_path']))
    with open(os.path.join(BASE, 'tables', 'candidate_relationships.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    with open(os.path.join(BASE, 'tables', 'unsearchable_documents.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(unsearch[0]), lineterminator='\n')
        w.writeheader(); w.writerows(unsearch)
    C = collections.Counter
    print(f'unique documents: {len(docs)}; searched (usable text layer): {len(docs) - len(unsearch)}; not searchable: {len(unsearch)}')
    print(f'candidate (product, document) pairs: {len(rows)}; products with a candidate: {len({r["product_id"] for r in rows})} of {len(ids)}; '
          f'documents with a candidate: {len({r["sha256"] for r in rows})}')
    print('suggested relationship:', dict(C(r['suggested_relationship'] for r in rows)))
    print('by supplier key:', dict(C(r['supplier_key'] for r in rows)))
    nodoc = [p['product_id'] for p in ids if p['product_id'] not in {r['product_id'] for r in rows}]
    print(f'products with no candidate in the searched text: {len(nodoc)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
