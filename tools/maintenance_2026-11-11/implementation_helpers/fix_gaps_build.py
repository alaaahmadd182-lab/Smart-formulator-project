"""One-off helper (2026-11-11, gap fixes): edits build_eligibility.py, the co-component scan, and the reviewed
side files. Already applied; do not rerun (each replacement asserts that its target occurs exactly once)."""
import json
R = 'C:\\Users\\windo\\sf-wsA\\'
MP = 'tools\\mandatory_properties\\'


def load(rel):
    return open(R + rel, encoding='utf-8').read()


def save(rel, s):
    open(R + rel, 'w', encoding='utf-8', newline='\n').write(s)


def sub(s, a, b):
    assert s.count(a) == 1, (a[:80], s.count(a))
    return s.replace(a, b)


# ---------------------------------------------------------------- build_eligibility.py
p = MP + 'build_eligibility.py'
s = load(p)
s = sub(s, """  - tools/mandatory_properties/co_component_statements.json: reviewed supplier statements about co-components.
""", """  - tools/mandatory_properties/co_component_statements.json: reviewed supplier statements about co-components.
  - tools/mandatory_properties/co_component_route_evidence.json: reviewed evidence of which recorded co-component
    requirements belong to which route (empty until routes are reviewed; no mapping is derived from role text).
""")
s = sub(s, """                  'calculated', 'reason', 'percentage_basis']""", """                  'calculated', 'reason', 'percentage_basis', 'selection_pending']""")
s = sub(s, """STATEMENTS = os.path.join(HERE, 'co_component_statements.json')
""", """STATEMENTS = os.path.join(HERE, 'co_component_statements.json')
ROUTES = os.path.join(HERE, 'co_component_route_evidence.json')
""")
s = sub(s, """def context(pid, p, pending, basis, page_text, statements=None):
    return R.Context(page_text=page_text, pending=pending, basis_evidence=basis, product=pid, material_class=p['class'],
                     statements=load_statements() if statements is None else statements)
""", """def load_routes():
    with open(ROUTES, encoding='utf-8') as fh:
        return json.load(fh)['routes']


def context(pid, p, pending, basis, page_text, statements=None, routes=None):
    return R.Context(page_text=page_text, pending=pending, basis_evidence=basis, product=pid, material_class=p['class'],
                     statements=load_statements() if statements is None else statements,
                     routes=load_routes() if routes is None else routes)
""")
s = sub(s, """                                 percentage_basis=o.basis or ''))""", """                                 percentage_basis=o.basis or '', selection_pending=o.selection_pending))""")
s = sub(s, """          'mandatory requirement has documented evidence, including valid ranges or bounds (never replaced by a point) and '
          'documented alternatives whose source selection is pending.""",
        """          'mandatory requirement is met, is a valid range or bound (never replaced by a point), or has a pending source '
          'selection on an otherwise complete value. It is derived from the outcome category, so a value that has both a '
          'pending selection and incomplete metadata is counted by its metadata defect; the independent selection status is '
          'the column `selection_pending` of `requirement_outcomes.csv`.""")
save(p, s)

# ---------------------------------------------------------------- reviewed side files
save(MP + 'co_component_route_evidence.json', json.dumps({
    "description": ("Reviewed evidence of co-component ROUTES (policy 2 of 2026-11-11). A route is a supplier-evidenced way of using the "
                    "package (a claim, a grade, a base-oil group) together with the co-components that route requires. An entry names "
                    "the product, a route_id and label, the conditions as printed, the source file and page, the quoted wording, the "
                    "member entries of required_co_components[] (entry_index plus role, name and dose_value, which must still match the "
                    "record) and requirement_list_confirmed: true only if the source review confirmed that the cited passage lists "
                    "every co-component the supplier requires for that route. No route is derived from the role text of a record. "
                    "While this list is empty, the route association of every recorded requirement is 'not established' and the "
                    "completeness of no route is assessed."),
    "review_status": ("No route has been reviewed. Reading note of 2026-11-11: LUBRIZOL_3700 records one booster with a usable dose, "
                      "while its source DL2-10632.pdf p.1 also says 'When formulated with appropriate base oils and viscosity modifier'; "
                      "one usable component therefore does not show that a route is complete."),
    "routes": []}, ensure_ascii=False, indent=2) + '\n')

p = MP + 'co_component_statements.json'
d = json.loads(load(p))
d['description'] = ("Reviewed supplier statements about co-component requirements (policy 2 of 2026-11-11). kind: none_required (the "
                    "supplier says a co-component is not needed). scope: which co-components the statement covers. quote: the supplier "
                    "wording exactly as printed. qualification: any hedge in that wording ('should', 'normally', 'may'), kept as printed. "
                    "A statement makes the product-level requirement met only if its scope is 'all co-components', it has its page and "
                    "quote, and it carries no qualification (requirements.explicit_none_required). Statements were read on the cited "
                    "page (text layer). Supplier requirements with a named co-component are recorded in the product JSON "
                    "(required_co_components[]), not here. An empty record is never recorded here as supplier silence.")
for x in d['statements']:
    x['qualification'] = "'should be needed': the supplier does not state unconditionally that no PPD is needed"
save(p, json.dumps(d, ensure_ascii=False, indent=2) + '\n')

# ---------------------------------------------------------------- co-component scan: what was inspected
p = MP + 'co_component_evidence_scan.py'
s = load(p)
s = sub(s, """An empty co-component list in a record is not evidence of absence.""",
        """The search covers the text layer of every page of the archive files that the package's values cite. It does not cover
files without a text layer, external (URL) sources, or archive files the record does not cite; the output says what was
inspected (documents_inspected, pages_with_text, not_inspected), so "not found" always means "not found in the inspected
text", never "the supplier is silent". An empty co-component list in a record is not evidence of absence.""")
s = sub(s, """REQ = re.compile(r'(?:in\\s+combination\\s+with|together\\s+with|combined\\s+with|used\\s+with|requires?|required|plus|\\+)""",
        """REQ = re.compile(r'(?:in\\s+combination\\s+with|together\\s+with|combined\\s+with|used\\s+with|formulated\\s+with|requires?|required|plus|\\+)""")
s = sub(s, """        files = set()
        for d in p['files'].values():
            for _, n in P.value_objects(d.get('fields', {})):
                f = (n.get('source') or {}).get('file')
                if f and not str(f).lower().startswith('http'):
                    files.add(f)
""", """        files, urls = set(), set()
        for d in p['files'].values():
            for _, n in P.value_objects(d.get('fields', {})):
                f = (n.get('source') or {}).get('file')
                if f and not str(f).lower().startswith('http'):
                    files.add(f)
                elif f:
                    urls.add(f)
""")
s = sub(s, """        hits = []
        for f in sorted(files):
            for i, t in enumerate(ar.pages(f) or []):
                flat = re.sub(r'\\s+', ' ', t)
""", """        hits, with_text, no_text, n_pages = [], [], [], 0
        for f in sorted(files):
            pages = ar.pages(f) or []
            texted = [t for t in pages if (t or '').strip()]
            (with_text if texted else no_text).append(f)
            n_pages += len(texted)
            for i, t in enumerate(pages):
                flat = re.sub(r'\\s+', ' ', t or '')
""")
s = sub(s, """                         finding=('explicit "none required" statement found (covers only the co-component it names)' if none_q else
                                  'co-components named or required by the supplier' if req_q else
                                  'no explicit statement found in the text layer of the cited pages'),""",
        """                         finding=('"none required" wording found (a lead; covers only the co-component it names)' if none_q else
                                  'co-components named or required in the inspected text (a lead)' if req_q else
                                  'not found in the inspected text' if with_text else
                                  'source text unavailable: nothing could be inspected'),
                         documents_inspected='; '.join(with_text), pages_with_text=n_pages,
                         not_inspected='; '.join([f'{f} (no text layer)' for f in no_text] + [f'{u} (external URL)' for u in sorted(urls)]),""")
save(p, s)
print('ok')
