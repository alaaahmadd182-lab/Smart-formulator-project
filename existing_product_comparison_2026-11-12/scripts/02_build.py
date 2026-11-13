"""Old-versus-new comparison, step 2: build every result table from the automated candidates, the earlier inventory
links and the reviewed decision files. Read-only on product JSON, archives, reports and the inventory folder.

Statuses are tracked INDEPENDENTLY and never merged into one 'complete' flag.
  per link (progress_ledger.csv):
    relationship_status          completed | unresolved | excluded with reason | not yet assessed
    field_verification_status    what was compared in the document, or 'not yet assessed'
    source_to_json_coverage      whether the document's information was checked against the product JSON
  per proposed field (field_level_comparison.csv):
    document_relationship        the link status above
    new_source_verification      visual (page image read) | text layer | text layer, visual check outstanding
    old_source_review            re-read manually | automated text search only | not available locally
    current_json_comparison      the actual current entries are listed; overlap checked by explicit tokens or not
    action_readiness             ready for reviewer decision | provisional (with every missing part named) | no action

'Automated text search' of an old source is a mechanical search of its text layer for the property or the names; it
is reported with its hits and is NOT a manual reading. A structural pass here is not a scientific verification.

Usage: python existing_product_comparison_2026-11-12/scripts/02_build.py
"""
import collections, csv, glob, gzip, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
T = os.path.join(BASE, 'tables')
X = os.path.join(BASE, 'current_json_excerpts')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'data_policy'))
C = collections.Counter
LIST_FIELDS = ('published_formulations', 'required_co_components', 'performance_claims', 'treat_rate_matrix', 'route_selector_restrictions',
               'permitted_base_oils_restrictions', 'sae_grades_documented')
TERMS = {'tbn': r'base number|\bTBN\b', 'sulfated_ash': r'sul(?:f|ph)ated ash', 'kv40': r'40\s*°?\s*[˚º]?\s*C', 'kv100': r'100\s*°?\s*[˚º]?\s*C', 'density': r'density|specific gravity|lbs',
         'flash_point': r'flash', 'pour_point': r'pour point', 'elements.Ca': r'calcium', 'elements.Zn': r'zinc', 'elements.P': r'phosphorus', 'elements.N': r'nitrogen',
         'elements.S': r'sul(?:f|ph)ur\b', 'elements.B': r'boron', 'elements.Mo': r'molybdenum', 'elements.Mg': r'magnesium', 'published_formulations': r'formulation|oil code',
         'treat_rate_matrix': r'treat rate|recommended|dosage', 'treat_rate': r'treat rate|recommended|dosage', 'function_specific_markers.tbn': r'base number|\bTBN\b'}
TOKEN = re.compile(r'LB[BR][- ]?0?\d{5,6}[- ]?[A-Z]?|OS\d{6}|IME\d{7}-A|HiTEC\s?\d{3,5}[A-Z]{0,2}|Lubrizol\s?\d{4}[A-Z]?|CV\d{4}|Infineum\s?[A-Z]{1,2}\d{3,4}|'
                   r'(?-i:API\s[A-Z]{2}\b)(?:-\d)?(?:\sPlus)?|ACEA\s[A-Z]\d{1,2}(?:-\d\d)?|MB-Approval\s\d{3}\.\d+|MAN\s2\d\d', re.I)



# Tenth-pass correction: an action that proposes a change to the JSON is either 'propose_*' or
# 'capture_from_old_source' (information in a cited source that was never captured). Both are proposals and go
# through the same readiness rules; earlier passes filtered on the prefix only and silently dropped the latter.
PROPOSING_EXTRA = ('capture_from_old_source',)
# Twelfth pass: wording that shows the old source was NOT read (only its quotation in the JSON, or a pointer to an
# earlier comparison without a documented direct-read scope). Such a statement cannot make a proposal ready.
JSON_QUOTED = re.compile(r'(?i)as quoted in the JSON|quoted in the JSON|JSON printed[_ ]text|the JSON printed values|values as compared in|as recorded in the JSON|cited in the JSON|from earlier review files|line as cited|JSON density entry')


def is_proposal(action):
    return action.startswith('propose') or action in PROPOSING_EXTRA

def rd(p):
    with open(p, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def wr(name, rows, cols=None):
    cols = cols or (list(rows[0]) if rows else ['empty'])
    with open(os.path.join(T, name), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
        w.writeheader(); w.writerows(rows)
    return len(rows)


def sha_file(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def node_at(fields, path):
    cur = fields
    for part in re.findall(r'[^.\[\]]+|\[\d+\]', path):
        try:
            cur = cur[int(part[1:-1])] if part.startswith('[') else cur[part]
        except (KeyError, IndexError, TypeError):
            return None
    return cur


def prune(n):
    """Drop empty values and derived *_final keys so that the excerpt shows what the record actually holds."""
    if isinstance(n, dict):
        out = {k: prune(v) for k, v in n.items() if not k.endswith('_final')}
        out = {k: v for k, v in out.items() if v not in (None, '', [], {})}
        if set(out) <= {'status', 'unit', 'source'} and out.get('status') == 'Missing':
            return {'status': 'Missing'}
        return out
    if isinstance(n, list):
        return [prune(v) for v in n]
    return n


def statuses(node, out):
    if isinstance(node, dict):
        if 'status' in node:
            out[str(node.get('status'))] += 1
        for v in node.values():
            statuses(v, out)
    elif isinstance(node, list):
        for v in node:
            statuses(v, out)
    return out


TOP_LEVEL_LISTS = ('open_questions', 'conflicts', 'source_documents')


def current(prods, pid, tier, path):
    """-> json file, compact current content, status summary, kind ('scalar' | 'list' | 'none'), pruned node"""
    p = prods.get(pid)
    if not p:
        return '', '', 'product not found', 'none', None
    for fn, d in p['files'].items():
        if d.get('tier') != tier:
            continue
        n = node_at(d.get('fields', {}), path.split(' (')[0])
        top = path.split(' (')[0].split('[')[0]
        if n is None and top in TOP_LEVEL_LISTS and isinstance(d.get(top), list):
            # A record-level list (open_questions, conflicts, ...), not a template field: a valid destination for notes,
            # open-question updates, conflict entries and citation corrections of conflict entries.
            return fn, f'{len(d[top])} existing {top} entries', f'top-level list ({top}), not a template field', 'none', None
        if n is None:
            return fn, '', 'no such field in the template', 'none', None
        pr = prune(n)
        if isinstance(n, dict) and 'status' in n and not any(k in n for k in ('permitted_api_groups', 'limits', 'allowed_combinations')):
            s = n.get('source') or {}
            v = n.get('value')
            val = f'value={v!r}; unit={n.get("unit")!r}; qualifier={n.get("qualifier")!r}; min={n.get("min")!r}; max={n.get("max")!r}; value_kind={n.get("value_kind")!r}; ' \
                  f'test_temperature_c={n.get("test_temperature_c")!r}; method={n.get("method")!r}; printed_text={n.get("printed_text")!r}; source={s.get("file")!r} p.{s.get("page")} rev {s.get("revision_date")!r}'
            return fn, val, str(n.get('status')), 'scalar', pr
        st = statuses(n, C())
        return fn, json.dumps(pr, ensure_ascii=False), '; '.join(f'{k}: {v}' for k, v in sorted(st.items())) or 'no value objects', 'list', pr
    return '', '', f'no tier {tier} file', 'none', None


class OldSources:
    def __init__(self, ref):
        self.arch = {m['name'].lower(): m for m in ref['archive']['members']}
        with open(os.path.join(ROOT, 'source_registry.json'), encoding='utf-8') as fh:
            self.reg = {s['url']: s for s in json.load(fh)['sources']}
        self.local = {}
        # retrieved_evidence_2026-11-13: registered external sources retrieved read-only on 2026-11-13 (hashes match
        # source_registry.json; see RETRIEVAL_LOG.txt). Only files whose hash equals a registered hash are used.
        for folder in ('reconciliation/audit_evidence', 'reports/data_policy/external_evidence', 'existing_product_comparison_2026-11-12/retrieved_evidence_2026-11-13'):
            for f in sorted(os.listdir(os.path.join(ROOT, folder))):
                p = os.path.join(ROOT, folder, f)
                if os.path.isfile(p):
                    self.local[sha_file(p)] = f'{folder}/{f}'
        self.cache = {}

    def resolve(self, name):
        """-> dict(ref, sha256, where, pages) ; pages None when no text is available locally"""
        if name in self.cache:
            return self.cache[name]
        out = dict(ref=name, sha256='', where='', pages=None)
        m = self.arch.get(str(name).lower())
        if m:
            out.update(sha256=m['sha256'], where='Manual + Data to share.zip:' + m['path'])
            p = os.path.join(INV, '_cache', 'ref_text', m['sha256'] + '.txt.gz')
            if os.path.exists(p):
                with gzip.open(p, 'rt', encoding='utf-8') as fh:
                    out['pages'] = fh.read().split('\f')
            else:
                out['where'] += ' (no text layer: cannot be searched)'
        elif str(name).lower().startswith('http'):
            s = self.reg.get(name)
            if not s:
                out['where'] = 'external URL not in source_registry.json: no hash available'
            else:
                out['sha256'] = s.get('sha256') or ''
                loc = self.local.get(out['sha256'])
                if loc:
                    out['where'] = 'registered external source; local evidence copy ' + loc
                    try:
                        import pymupdf
                        pymupdf.TOOLS.mupdf_display_errors(False)
                        out['pages'] = [pg.get_text() for pg in pymupdf.open(os.path.join(ROOT, loc))]
                    except Exception:
                        out['where'] += ' (text not extractable)'
                else:
                    out['where'] = 'registered external source (source_registry.json, SHA-256 recorded); NO local evidence copy: not available locally, not re-checked'
        else:
            out['where'] = 'not a member of the existing archive and not a registered URL: unavailable'
        self.cache[name] = out
        return out


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    import policy_lib as P
    prods = P.load_products()
    with open(os.path.join(INV, '_cache', 'reference.json'), encoding='utf-8') as fh:
        ref = json.load(fh)
    olds = OldSources(ref)
    man = rd(os.path.join(INV, 'manifest', 'file_manifest.csv'))
    new_sha = {r['filename']: r['sha256'] for r in man}
    # Eleventh pass: registered external sources retrieved read-only (retrieved_evidence_2026-11-13) are cited by some
    # field rows; their SHA-256 is computed from the saved bytes (each equals source_registry.json, RETRIEVAL_LOG.txt).
    retr = os.path.join(BASE, 'retrieved_evidence_2026-11-13')
    for fn in (os.listdir(retr) if os.path.isdir(retr) else []):
        if fn.lower().endswith('.pdf') and fn not in new_sha:
            with open(os.path.join(retr, fn), 'rb') as fh:
                new_sha[fn] = hashlib.sha256(fh.read()).hexdigest()
    cand = rd(os.path.join(T, 'candidate_relationships.csv'))
    inv = rd(os.path.join(INV, 'tables', 'existing_product_matches.csv'))
    with open(os.path.join(BASE, 'decisions', 'inventory_dispositions.json'), encoding='utf-8') as fh:
        disp = json.load(fh)
    groups = disp['file_groups']

    # ---- decisions (later files override the same product/file link; overrides patch field rows) ----
    docs, links, fields, visual, pending_visual, queue, overrides, old_default = {}, {}, [], [], [], [], [], {}
    for path in sorted(glob.glob(os.path.join(BASE, 'decisions', '*.json'))):
        name = os.path.basename(path)
        if name == 'inventory_dispositions.json':
            continue
        with open(path, encoding='utf-8') as fh:
            d = json.load(fh)
        b = d.get('batch', '')
        overrides += d.get('field_overrides', [])
        old_default.update(d.get('old_review_by_decision_file', {}))
        for f, v in d.get('documents', {}).items():
            for g in groups.get(f, [f]):
                docs[g] = dict(v, batch=b)
        for l in d.get('links', []):
            for g in groups.get(l['f'], [l['f']]):
                links[(l['p'], g)] = dict(l, f=g, batch=b, decision_file=name)
        for f in d.get('fields', []):
            fields.append(dict(f, batch=b, decision_file=name))
        visual += [dict(v, batch=b) for v in d.get('visual', [])]
        pending_visual += [dict(v, batch=b) for v in d.get('not_yet_verified_visually', [])]
        queue += [dict(v, batch=b) for v in d.get('new_product_candidates', [])]
    done_visual = {(v['f'], str(v['page'])) for v in visual if v['result'].startswith('confirmed')}
    pending_visual = [v for v in pending_visual if not any((f.strip(), pg.strip()) in done_visual or (f.strip(), 'all') in done_visual
                                                           for f in v['f'].split(' / ') for pg in re.split(r'[,]', str(v['page'])))]
    for o in overrides:
        hit = [f for f in fields if f['p'] == o['p'] and o['path'] in ('*', f['path']) and o['new_f'] in ('*', f['new_f'])]
        if not hit:
            print('  WARNING override matches no field row:', o['p'], o['path'], o['new_f'])
        for f in hit:
            for k, v in o.items():
                if k == 'reason_append':
                    f['reason'] = f['reason'] + ' ' + v
                elif k not in ('p', 'path', 'new_f'):
                    f[k] = v
    for fm in disp['false_revision_matches']:
        f = fm.get('file') or next(n for n in new_sha if n.startswith(fm['file_startswith']))
        links.setdefault((fm['product_id'], f), dict(p=fm['product_id'], f=f, cat='G,D', status='excluded with reason', identity=fm['reason'],
                                                      note=fm['disposition'] + '. Preserved: ' + fm['preserved_link'], fields_status='not yet assessed (preserved formulation link)',
                                                      coverage='not applicable', batch='inventory correction', decision_file='inventory_dispositions.json'))

    # ---- ledger: union of the full-text candidates and ALL earlier inventory links ----
    led = {}
    for r in cand:
        led[(r['product_id'], r['sha256'])] = dict(product_id=r['product_id'], sha256=r['sha256'], file=r['first_path'].rsplit('/', 1)[-1], supplier_key=r['supplier_key'],
                                                    found_by=r.get('found_via') or 'full-text search', inventory_relationship='', suggested_relationship=r['suggested_relationship'],
                                                    hit_pages=r['hit_pages'], document_type=r['document_type'], pages=r['pages'])
    for r in inv:
        k = (r['product_id'], r['sha256'])
        short = r['relationship'].split(':')[0][:90]
        if k in led:
            led[k].update(found_by=led[k]['found_by'] + ' and earlier inventory', inventory_relationship=short)
        else:
            led[k] = dict(product_id=r['product_id'], sha256=r['sha256'], file=r['first_path'].rsplit('/', 1)[-1], supplier_key='', found_by='earlier inventory only',
                          inventory_relationship=short, suggested_relationship='A' if r['match_level'] == 'byte_identical_to_cited_source' else 'not suggested (not found by the text search)',
                          hit_pages='', document_type=r['document_type'], pages='')
    udoc = {r['sha256']: r for r in rd(os.path.join(INV, 'tables', 'unique_documents.csv'))}
    # Sixteenth pass: links known only from the earlier inventory carried no page count. Fill it from the inventory's own
    # measurement of the same SHA-256 (unique_documents.csv 'pages'); nothing is filled where the inventory has none.
    for v in led.values():
        if not v['pages'] and v['sha256'] in udoc and udoc[v['sha256']].get('pages'):
            v['pages'] = udoc[v['sha256']]['pages']
    unsearch = {r['sha256'] for r in rd(os.path.join(T, 'unsearchable_documents.csv'))}
    rows, used_links = [], set()
    for (pid, sha), r in sorted(led.items()):
        names = [x.rsplit('/', 1)[-1] for x in udoc[sha]['paths'].split(' | ')] if sha in udoc else [r['file']]
        hit = next(((pid, n) for n in names if (pid, n) in links), None)
        l = links[hit] if hit else None
        if hit:
            used_links.add(hit)
        if r['found_by'] == 'earlier inventory only':
            r['why_not_found_by_text_search'] = ('the document has no usable text layer; the link rests on the file hash' if sha in unsearch else
                                                 'the text layer does not print the product name in the exact form searched (the link rests on the file hash)'
                                                 if r['suggested_relationship'] == 'A' else 'the earlier first-page match used looser name forms than the exact full-text search')
        else:
            r['why_not_found_by_text_search'] = ''
        if l:
            r.update(reviewed_categories=l['cat'], relationship_status=l['status'], field_verification_status=l.get('fields_status') or 'field rows recorded; see field_level_comparison.csv and visual_verification.csv',
                     source_to_json_coverage=l.get('coverage') or 'not assessed', identity_check=l.get('identity', ''), review_note=l.get('note', ''), batch=l.get('batch', ''))
        elif r['suggested_relationship'].startswith('A'):
            r.update(reviewed_categories='A', relationship_status='completed', field_verification_status='no content comparison needed (identical bytes to an existing archive file)',
                     source_to_json_coverage='not assessed', identity_check='SHA-256 equal to ' + (udoc[sha]['byte_duplicate_of_existing'] if sha in udoc else ''),
                     review_note='Exact byte duplicate. Whether everything in the source was captured in JSON has NOT been assessed.', batch='automatic (hash)')
        else:
            r.update(reviewed_categories='', relationship_status='not yet assessed', field_verification_status='not yet assessed', source_to_json_coverage='not assessed',
                     identity_check='', review_note='', batch='')
        rows.append(r)
    # reviewed links that the automated tables did not contain (e.g. a duplicate copy read under another file name)
    for k in sorted(set(links) - used_links):
        l = links[k]
        rows.append(dict(product_id=k[0], sha256=new_sha.get(k[1], ''), file=k[1], supplier_key='', found_by='manual review only (not in the automated tables)', inventory_relationship='',
                         suggested_relationship='', hit_pages='', document_type='', pages='', why_not_found_by_text_search='link recorded by the reviewer; the automated search did not pair this product and file',
                         reviewed_categories=l['cat'], relationship_status=l['status'], field_verification_status=l.get('fields_status') or 'see field rows',
                         source_to_json_coverage=l.get('coverage') or 'not assessed', identity_check=l.get('identity', ''), review_note=l.get('note', ''), batch=l.get('batch', '')))
    cols = ['product_id', 'supplier_key', 'file', 'sha256', 'document_type', 'pages', 'found_by', 'why_not_found_by_text_search', 'inventory_relationship', 'suggested_relationship',
            'hit_pages', 'reviewed_categories', 'relationship_status', 'field_verification_status', 'source_to_json_coverage', 'identity_check', 'review_note', 'batch']
    wr('progress_ledger.csv', rows, cols)
    wr('document_relationships.csv', [r for r in rows if r['reviewed_categories']], cols)
    link_status = {(r['product_id'], r['file']): r['relationship_status'] for r in rows}
    for (pid, f), l in links.items():
        link_status.setdefault((pid, f), l['status'])

    # ---- reconciliation of the product counts ----
    hash_products = {r['product_id'] for r in inv if r['match_level'] == 'byte_identical_to_cited_source'}
    text_products = {r['product_id'] for r in cand}
    all_ids = sorted(prods)
    rec = []
    for pid in all_ids:
        a, b = pid in hash_products, pid in text_products
        rec.append(dict(product_id=pid, cited_source_hash_link='yes' if a else 'no', found_by_full_text_search='yes' if b else 'no',
                        explanation='' if a and b else 'cited source is in the new archive by hash, but no searched text layer prints the exact name (image-only source or another printed name form)' if a
                        else 'named in the text of new documents, but no cited source of the product is byte-identical to a file of the new archive' if b
                        else 'neither: no cited source by hash and no exact name in the searched text'))
    wr('product_link_reconciliation.csv', rec)

    # ---- field-level comparison with five independent statuses ----
    os.makedirs(X, exist_ok=True)
    for f in glob.glob(os.path.join(X, '*.json')):
        os.remove(f)
    frows, excerpts, old_used = [], {}, {}
    for f in fields:
        pid = f['p']
        fn, cur, st, kind, pr = current(prods, pid, f['tier'], f['path'])
        json_sha = sha_file(os.path.join(ROOT, fn)) if fn else ''
        if fn:
            key = f'{pid}__tier{f["tier"]}__{re.sub(r"[^A-Za-z0-9_.]+", "_", f["path"].split(" (")[0])}'
            excerpts[key] = dict(product_id=pid, json_file=fn, json_file_sha256_working_tree_bytes=json_sha, field_path=f['path'].split(' (')[0], status_summary=st, current_content=pr)
        # old sources: every source file the product record cites
        cited = []
        if pid in prods:
            for d in prods[pid]['files'].values():
                sf = (d.get('product') or {}).get('source_file')
                cited += sf if isinstance(sf, list) else [sf] if sf else []
        cited = list(dict.fromkeys(cited))
        refs, search = [], []
        base_path = f['path'].split(' (')[0].split('[')[0]
        term = f.get('old_terms') or TERMS.get(f['path'].split(' (')[0]) or TERMS.get(base_path)
        tokens = f.get('check_tokens')
        if tokens is None and kind == 'list':
            own = re.sub(r'[^a-z0-9]', '', (prods[pid]['files'][fn]['product'].get('product_name') or '').lower()) if fn else ''
            tokens = [t for t in dict.fromkeys(re.sub(r'\s+', ' ', m.group(0)).strip() for m in TOKEN.finditer(f['new_text'])) if re.sub(r'[^a-z0-9]', '', t.lower()) not in own or t.upper().startswith(('LB', 'OS', 'IME'))][:14]
        available = 0
        for name in cited:
            o = olds.resolve(name)
            old_used[name] = o
            refs.append(f'{name} | sha256 {o["sha256"] or "none recorded"} | {o["where"]}')
            if o['pages'] is None:
                search.append(f'{str(name)[-40:]}: NOT SEARCHED (no text available locally)')
                continue
            available += 1
            pats = ([('property', term)] if term else []) + [('name ' + t, re.escape(t).replace(r'\ ', r'[\s®™-]*')) for t in (tokens or [])][:10]
            for label, pat in pats:
                rx = re.compile(pat, re.I)
                hits = [(i + 1, re.sub(r'\s+', ' ', pg[max(0, m.start() - 30): m.end() + 60]).strip()) for i, pg in enumerate(o['pages']) for m in [rx.search(pg)] if m]
                search.append(f'{str(name)[-40:]}: {label}: ' + ('no hit' if not hits else f'p.{",".join(str(h[0]) for h in hits)} "{hits[0][1][:90]}"'))
        manual = f.get('old_rev') or old_default.get(f['decision_file'], '')
        if manual:
            old_review = manual
        elif not cited:
            old_review = 'no source file recorded in the product record'
        elif available == 0:
            old_review = 'not available locally: the cited old source could not be opened; statement in old_source_statement comes from the record itself, not from the source'
        else:
            old_review = (f'automated text search only ({available} of {len(cited)} cited sources searchable); not a manual reading. '
                          'old_source_statement was written from the record notes unless it says the source was re-read')
        if not manual and cited and 0 < available < len(cited):
            old_review += f'. {len(cited) - available} cited source(s) NOT available locally and not checked (old_source_references)'
        # current JSON comparison
        if kind == 'scalar':
            cmp_ = 'compared: the current value object is shown in current_value'
        elif kind == 'list':
            dump = re.sub(r'[\s®™-]+', '', json.dumps(pr, ensure_ascii=False).lower())
            present = [t for t in (tokens or []) if re.sub(r'[\s®™-]+', '', t.lower()) in dump]
            absent = [t for t in (tokens or []) if t not in present]
            cmp_ = ('current entries listed; no explicit name or code available to test overlap: compare by reading' if not tokens else
                    f'current entries listed and searched for {len(tokens)} names/codes of the new source: ALREADY PRESENT {present or "none"}; not present {absent or "none"}')
        else:
            present, cmp_ = [], 'not compared: ' + st
        if kind != 'list':
            present = []
        # reviewer's entry-by-entry comparison (sixth pass): replaces the token test when the reviewer compared the
        # actual JSON entries; 'overlap_reviewed' records the outcome of resolving a 'possible overlap' flag
        if f.get('cmp_override'):
            cmp_, kind = 'compared entry by entry by the reviewer: ' + f['cmp_override'], 'reviewed'
        if f.get('overlap_reviewed'):
            cmp_ += ' || OVERLAP REVIEWED: ' + f['overlap_reviewed']
            present = []
        vkey = (f['new_f'], str(f['new_p']))
        if vkey in done_visual:
            newver = 'visual: page image read (visual_verification.csv)'
        elif any(f['new_f'] in v['f'] and (str(f['new_p']) in [x.strip() for x in re.split(r'[,]', str(v['page']))] or '-' in str(v['page'])) for v in pending_visual):
            newver = 'text layer; a visual check of this document is outstanding (visual_verification.csv)'
        else:
            newver = f.get('new_ver') or 'text layer (running text or a simple label-value list)'
        rel = link_status.get((pid, f['new_f']), 'no link decision recorded')
        act = f['action']
        why = []
        if not is_proposal(act):
            ready = 'no action proposed'
        else:
            if rel != 'completed':
                why.append('document relationship ' + rel)
            if newver.startswith('text layer; a visual'):
                why.append('visual check outstanding')
            # the reviewer's statement counts as a reading only when it STARTS with 're-read'; a statement that starts
            # with 'not available locally' and mentions a second source being re-read is not a reading of the primary source
            if manual and manual.startswith('re-read manually in part'):
                why.append('old source read only in part')
            elif manual and manual.startswith('not available locally'):
                why.append('primary old source not available locally (' + manual.split(':', 1)[1].strip()[:90] + ')')
            elif manual and JSON_QUOTED.search(manual):
                # twelfth pass: a statement that relies on the JSON's quotation of a source (or on an undocumented
                # earlier comparison) is not a reading of the original source
                why.append('old source not read: the statement relies on the JSON quotation or an earlier comparison, not on the original pages')
            elif manual and manual.startswith('re-read'):
                pass    # the reviewer read the old source; the statement says exactly what was and was not read
            elif 'automated' not in old_review and 're-read' not in old_review:
                why.append('old source not reviewed (' + old_review.split(':')[0] + ')')
            elif 'automated' in old_review:
                why.append('old source only searched automatically, not read' + ('; a cited old source is not available locally' if 'NOT available' in old_review else ''))
            if kind == 'none':
                why.append('current JSON not compared')
            elif kind == 'list' and present:
                why.append('possible overlap with existing entries: ' + ', '.join(present))
            elif kind == 'list' and not tokens:
                why.append('overlap with existing entries not tested')
            why += f.get('provisional_because', [])
            ready = 'ready for reviewer decision' if not why else 'PROVISIONAL: ' + '; '.join(why)
        frows.append(dict(product_id=pid, material_class=prods[pid]['class'] if pid in prods else '', json_file=fn, json_file_sha256=json_sha, tier=f['tier'], field_path=f['path'],
                          current_status=st, current_value=cur[:3000] + (' ...[full text in current_json_excerpts/]' if len(cur) > 3000 else ''),
                          old_source_statement=f.get('old', ''), old_source_references='  ||  '.join(refs) or 'none recorded', old_source_search='  ||  '.join(search),
                          new_source_file=f['new_f'], new_source_sha256=new_sha.get(f['new_f'], ''), new_source_page=f['new_p'], new_source_printed=f['new_text'], unit=f.get('unit', ''),
                          value_form=f.get('form', ''), qualifier=f.get('qual', ''), method=f.get('method', ''), conditions=f.get('cond', ''), percentage_basis=f.get('basis', ''),
                          new_document=docs.get(f['new_f'], {}).get('what', ''), new_document_date_as_printed=docs.get(f['new_f'], {}).get('printed_date', ''),
                          new_document_read_scope=docs.get(f['new_f'], {}).get('read', ''), comparison_outcome=f['outcome'], recommended_action=act, reason=f['reason'],
                          document_relationship=rel, new_source_verification=newver, old_source_review=old_review, current_json_comparison=cmp_, action_readiness=ready,
                          batch=f['batch'], decision_file=f['decision_file']))
    for key, e in excerpts.items():
        with open(os.path.join(X, key + '.json'), 'w', encoding='utf-8') as fh:
            json.dump(e, fh, ensure_ascii=False, indent=1)
    wr('field_level_comparison.csv', frows)
    wr('proposed_json_changes_NOT_APPLIED.csv', [r for r in frows if is_proposal(r['recommended_action'])])
    wr('old_source_references.csv', [dict(reference=n, sha256=o['sha256'], availability=o['where'], text_pages='' if o['pages'] is None else len(o['pages'])) for n, o in sorted(old_used.items(), key=lambda x: str(x[0]))])
    possible = [r for r in frows if r['current_status'] == 'Missing' and re.search(r': property: p\.', r['old_source_search'])]
    wr('existing_source_information_not_captured.csv',
       [dict(r, basis='reviewed') for r in frows if r['comparison_outcome'] == 'in_old_source_not_captured']
       + [dict(r, basis='AUTOMATED LEAD ONLY: the property word occurs in a cited old source while the JSON field is Missing; the hit may be a component name or another product, read old_source_search') for r in possible],
       cols=['basis', 'product_id', 'json_file', 'field_path', 'current_status', 'old_source_search', 'old_source_references', 'old_source_statement'])
    wr('conflicts_and_unresolved.csv', [dict(kind='field', product_id=r['product_id'], item=r['field_path'], file=r['new_source_file'], detail=r['reason']) for r in frows if r['comparison_outcome'] == 'changed_or_conflicting']
       + [dict(kind='relationship', product_id=r['product_id'], item=r['reviewed_categories'], file=r['file'], detail=r['identity_check'] + ' | ' + r['review_note']) for r in rows if r['relationship_status'] == 'unresolved']
       + [dict(kind='visual check outstanding', product_id='', item=f'page {v["page"]}', file=v['f'], detail=v['why']) for v in pending_visual])
    wr('visual_verification.csv', [dict(file=v['f'], sha256=new_sha.get(v['f'], ''), page=v['page'], checked=v['checked'], result=v['result'], detail=v['detail']) for v in visual]
       + [dict(file=v['f'], sha256=new_sha.get(v['f'], ''), page=v['page'], checked=v['why'], result='NOT YET VERIFIED', detail='') for v in pending_visual])
    wr('reviewed_documents.csv', [dict(file=f, sha256=new_sha.get(f, ''), **v) for f, v in sorted(docs.items())], cols=['file', 'sha256', 'batch', 'what', 'kind', 'printed_date', 'read', 'limits'])
    wr('new_product_candidate_queue.csv', queue, cols=['name_as_printed', 'supplier', 'file', 'page', 'evidence', 'batch'])

    # ---- product summary ----
    ps = []
    for pid in all_ids:
        mine = [r for r in rows if r['product_id'] == pid]
        if not mine:
            continue
        mf = [r for r in frows if r['product_id'] == pid]
        nondup = [r for r in mine if r['reviewed_categories'] != 'A']
        ps.append(dict(product_id=pid, material_class=prods[pid]['class'], links=len(mine), exact_duplicates=len(mine) - len(nondup), other_links=len(nondup),
                       reviewed=sum(1 for r in nondup if r['relationship_status'] != 'not yet assessed'), not_yet_assessed=sum(1 for r in nondup if r['relationship_status'] == 'not yet assessed'),
                       unresolved=sum(1 for r in nondup if r['relationship_status'] == 'unresolved'), excluded=sum(1 for r in nondup if r['relationship_status'].startswith('excluded')),
                       substantive_documents=sum(1 for r in nondup if set(r['reviewed_categories'].split(',')) & {'D', 'E', 'F', 'B'} and not r['relationship_status'].startswith('excluded')),
                       mention_only_documents=sum(1 for r in nondup if r['reviewed_categories'] in ('C', 'C,H')),
                       field_rows=len(mf), additional=sum(1 for r in mf if r['comparison_outcome'] == 'additional'), changed_or_conflicting=sum(1 for r in mf if r['comparison_outcome'] == 'changed_or_conflicting'),
                       already_captured=sum(1 for r in mf if r['comparison_outcome'] == 'already_captured'), proposed_changes=sum(1 for r in mf if is_proposal(r['recommended_action'])),
                       proposals_ready=sum(1 for r in mf if r['action_readiness'].startswith('ready')), proposals_provisional=sum(1 for r in mf if r['action_readiness'].startswith('PROVISIONAL'))))
    wr('product_comparison_summary.csv', ps)

    # ---- corrected inventory statistics ----
    strong = [r for r in inv if r['match_level'] in ('name_in_title_lines_and_supplier', 'name_in_product_field_and_supplier')]
    new_strong = [r for r in strong if not r['relationship'].startswith('already')]
    excl = {(k[0], new_sha.get(k[1])) for k, l in links.items() if l['status'].startswith('excluded')}
    after = [r for r in new_strong if (r['product_id'], r['sha256']) not in excl]
    rev = [r for r in inv if r['relationship'].startswith('different')]
    nd = [r for r in rows if r['reviewed_categories'] != 'A']
    stats = {
        'original_statistic': {'links': len(strong), 'documents': len({r['sha256'] for r in strong}), 'products': len({r['product_id'] for r in strong}),
                               'meaning': 'product-document links whose title or product field names an existing product, INCLUDING files byte-identical to the existing archive'},
        'of_which_byte_identical_to_existing_archive': {'links': len(strong) - len(new_strong), 'products': len({r['product_id'] for r in strong} - {r['product_id'] for r in new_strong})},
        'new_documents_only': {'links': len(new_strong), 'documents': len({r['sha256'] for r in new_strong}), 'products': len({r['product_id'] for r in new_strong}),
                               'split': {'additional evidence (provisional)': sum(1 for r in new_strong if r['relationship'].startswith('additional')), 'revision candidates (provisional)': len(rev)}},
        'reviewed_exclusions': [dict(product_id=k[0], file=k[1], reason=l['identity']) for k, l in sorted(links.items()) if l['status'].startswith('excluded') and (k[0], new_sha.get(k[1])) in {(r['product_id'], r['sha256']) for r in new_strong}],
        'new_documents_only_after_reviewed_exclusions': {'links': len(after), 'documents': len({r['sha256'] for r in after}), 'products': len({r['product_id'] for r in after})},
        'revision_candidates': {'original': len(rev), 'after_reviewed_exclusions': sum(1 for r in rev if (r['product_id'], r['sha256']) not in excl)},
        'product_linkage': {'products_total': len(all_ids), 'with_cited_source_byte_identical_in_new_archive': len(hash_products), 'named_in_searched_text_of_new_archive': len(text_products),
                            'both': len(hash_products & text_products), 'hash_only': len(hash_products - text_products), 'text_only': len(text_products - hash_products),
                            'either': len(hash_products | text_products), 'neither': len(set(all_ids) - hash_products - text_products),
                            'note': 'The text search does not replace the hash linkage: both are kept (tables/product_link_reconciliation.csv).'},
        'search_limits': {'unique_documents': len(udoc), 'searched_with_usable_text_layer': len(udoc) - len(unsearch), 'not_searchable_no_text_layer': len(unsearch)},
        'ledger': {'links_total': len(rows), 'found_by': dict(C(r['found_by'] for r in rows)), 'relationship_status': dict(C(r['relationship_status'] for r in rows)),
                   'exact_duplicate_links': len(rows) - len(nd), 'non_duplicate_links': len(nd), 'non_duplicate_by_status': dict(C(r['relationship_status'] for r in nd)),
                   'non_duplicate_by_batch_and_status': {k: dict(v) for k, v in sorted(collections.defaultdict(C, {}).items())}},
        'fields': {'rows': len(frows), 'outcomes': dict(C(r['comparison_outcome'] for r in frows)), 'proposed': sum(1 for r in frows if is_proposal(r['recommended_action'])),
                   'ready_for_reviewer_decision': sum(1 for r in frows if r['action_readiness'].startswith('ready')), 'provisional': sum(1 for r in frows if r['action_readiness'].startswith('PROVISIONAL')),
                   'new_source_verification': dict(C(r['new_source_verification'].split(':')[0].split(';')[0].split(' (')[0] for r in frows)),
                   'old_source_review': dict(C(r['old_source_review'].split(':')[0].split(' (')[0][:60] for r in frows))},
        'wording_corrections': disp['wording_corrections'],
    }
    by = collections.defaultdict(C)
    for r in nd:
        p = r['product_id'].upper()
        by['afton' if 'HITEC' in p else 'lubrizol' if p.startswith('LUBRIZOL') else 'infineum' if p.startswith('INFINEUM') else 'other suppliers'][r['relationship_status']] += 1
    stats['ledger']['non_duplicate_by_batch_and_status'] = {k: dict(v) for k, v in sorted(by.items())}
    with open(os.path.join(T, 'corrected_inventory_statistics.json'), 'w', encoding='utf-8') as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=1)
    ids_txt = rd(os.path.join(T, 'product_identities.csv'))
    wr('inventory_wording_checks.csv', [dict(product_id=p['product_id'], search_aliases=p['search_aliases'],
                                             documents_naming_it_in_searched_text=sum(1 for r in cand if r['product_id'] == p['product_id']),
                                             of_which_not_byte_duplicates=sum(1 for r in cand if r['product_id'] == p['product_id'] and not r['suggested_relationship'].startswith('A')))
                                        for p in ids_txt if re.search(r'3589C|LUBRIZOL_3700|NEXBASE_30[4-8]|ETRO_4$|PRIMA|12204L|12250|8788B', p['product_id'])])
    print(json.dumps({k: stats[k] for k in ('new_documents_only_after_reviewed_exclusions', 'revision_candidates', 'ledger', 'fields')}, indent=1))
    print(f'reviewed documents {len(docs)}; visual checks {len(visual)} done, {len(pending_visual)} outstanding; old sources referenced {len(old_used)}; excerpts {len(excerpts)}')
    for r in frows:
        if (r['current_status'] in ('product not found', 'no such field in the template') or r['current_status'].startswith('no tier')) and not r['field_path'].startswith('('):
            print('  CHECK field path:', r['product_id'], r['tier'], r['field_path'], r['current_status'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
