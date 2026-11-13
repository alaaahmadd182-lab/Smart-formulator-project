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


# ---------------------------------------------------------------- basis evidence: schema of policy 3
p = MP + 'treat_rate_basis_evidence.json'
raw = load(p)
d = json.loads(raw)
d['description'] = ("Reviewed evidence (2026-11-10; schema extended 2026-11-11 for policy 3) that establishes the basis of a treat "
                    "rate or dose recorded with a bare '%'. Each entry gives basis_class (mass or volume), evidence_kind (unit, "
                    "heading, footnote, text or document_convention), scope (value, table or document), the page and the quoted "
                    "wording. Only cases where the source states the basis for the recorded number are listed; the basis is never "
                    "guessed, and the recorded unit in the product JSON stays as printed.")
d['document_wide_conventions'] = ("Searched 2026-11-11: the text layers of all 20 archive documents that carry an unspecified-basis "
                                  "dose were searched, on every page, for a document-wide statement of the percentage basis (for "
                                  "example 'all percentages are by weight'). 19 have a text layer; DL2-10218.pdf is image-only and "
                                  "was read on its render on 2026-11-10. None was found. The two external sources (Afton HiTEC "
                                  "12250 data sheet, not obtained; Richful page 130) are outside that search.")
KIND = {'INFINEUM_D3384': ('heading', 'table'), 'INFINEUM_D3451': ('heading', 'table'), 'AFTON_HITEC_12360': ('text', 'value')}
for e in d['evidence']:
    e['basis_class'] = 'mass'
    e['evidence_kind'], e['scope'] = KIND[e['product']]
save(p, json.dumps(d, ensure_ascii='\\u' in raw, indent=2) + '\n')

# ---------------------------------------------------------------- reviewed co-component statements (policy 2)
save(MP + 'co_component_statements.json', json.dumps({
    "description": ("Reviewed supplier statements about co-component requirements (policy 2 of 2026-11-11). kind: none_required "
                    "(the supplier states that a co-component is not needed). scope: which co-components the statement covers; "
                    "only scope 'all co-components' makes the product-level requirement met. A statement about one co-component "
                    "type covers that type only. Statements were read on the cited page (text layer); the leads came from "
                    "co_component_evidence_scan.py. Supplier requirements WITH a named co-component are recorded in the product "
                    "JSON (required_co_components[]), not here. Silence is never recorded as a statement."),
    "statements": [
        {"product": "AFTON_HITEC_12210", "kind": "none_required", "scope": "pour point depressant (PPD)", "source_file": "DL2-11418.pdf",
         "page": 2, "quote": "HiTEC® 12210 already contains a pour point depressant (PPD) so no supplemental PPD should be needed to meet low temperature properties.",
         "conditions": "as printed: for the package's listed API CK-4 / FA-4 grades; says nothing about a viscosity modifier or booster",
         "read_on": "text layer, 2026-11-11"},
        {"product": "AFTON_HITEC_12210M", "kind": "none_required", "scope": "pour point depressant (PPD)", "source_file": "DL2-15568.pdf",
         "page": 2, "quote": "HiTEC® 12210M already contains a pour point depressant (PPD) so no supplemental PPD should be needed to meet low temperature properties.",
         "conditions": "as printed: for the package's listed API CK-4 / FA-4 grades; says nothing about a viscosity modifier or booster",
         "read_on": "text layer, 2026-11-11"}]}, ensure_ascii=False, indent=2) + '\n')

# ---------------------------------------------------------------- build_eligibility.py
p = MP + 'build_eligibility.py'
s = load(p)
s = sub(s, """  - tools/mandatory_properties/treat_rate_basis_evidence.json: reviewed page evidence of a mass basis for bare '%'.
""", """  - tools/mandatory_properties/treat_rate_basis_evidence.json: reviewed source evidence of the basis of a bare '%'.
  - tools/mandatory_properties/co_component_statements.json: reviewed supplier statements about co-components.
""")
s = sub(s, """DETAIL_COLUMNS = ['product_id', 'material_class', 'product_name', 'requirement', 'category', 'blocking', 'representation',
                  'calculated', 'reason']""", """DETAIL_COLUMNS = ['product_id', 'material_class', 'product_name', 'requirement', 'category', 'blocking', 'representation',
                  'calculated', 'reason', 'percentage_basis']""")
s = sub(s, """BASIS = os.path.join(HERE, 'treat_rate_basis_evidence.json')
""", """BASIS = os.path.join(HERE, 'treat_rate_basis_evidence.json')
STATEMENTS = os.path.join(HERE, 'co_component_statements.json')
""")
s = sub(s, """def evaluate(pid, p, snapshot, pending, basis, page_text):
    ctx = R.Context(page_text=page_text, pending=pending, basis_evidence=basis, product=pid)""",
        """def load_statements():
    with open(STATEMENTS, encoding='utf-8') as fh:
        return json.load(fh)['statements']


def context(pid, p, pending, basis, page_text, statements=None):
    return R.Context(page_text=page_text, pending=pending, basis_evidence=basis, product=pid, material_class=p['class'],
                     statements=load_statements() if statements is None else statements)


def evaluate(pid, p, snapshot, pending, basis, page_text, statements=None):
    ctx = context(pid, p, pending, basis, page_text, statements)""")
s = sub(s, """    page_text = page_text or PageText()
    rows, outcomes = [], []
    for pid in sorted(prods):
        row, outs = evaluate(pid, prods[pid], snapshot, pending, basis, page_text)""",
        """    page_text = page_text or PageText()
    statements = load_statements()
    rows, outcomes = [], []
    for pid in sorted(prods):
        row, outs = evaluate(pid, prods[pid], snapshot, pending, basis, page_text, statements)""")
s = sub(s, """                                 representation=o.representation or '', calculated=o.calculated, reason=o.reason))""",
        """                                 representation=o.representation or '', calculated=o.calculated, reason=o.reason,
                                 percentage_basis=o.basis or ''))""")
s = sub(s, """          '"Documented" (companion measure, `documentation_coverage.csv`) is NOT completeness: it counts products for which every '
          'mandatory requirement has some documented information, including ranges or bounds still awaiting a use-specific '
          'decision and values whose source selection is pending.', '',""",
        """          '"Documented" (companion measure, `documentation_coverage.csv`) is NOT completeness: it counts products for which every '
          'mandatory requirement has documented evidence, including valid ranges or bounds (never replaced by a point) and '
          'documented alternatives whose source selection is pending. Evidence documentation, value selection, value form, '
          'percentage basis and verification status are reported as separate attributes by '
          '`python tools/mandatory_properties/build_readiness.py` (`property_attributes.csv`).', '',""")
s = sub(s, """           '## Interpretations used (provisional; need reviewer confirmation)', '']""",
        """           '## Interpretations and approved policies in force', '',
           'Entries marked "Approved policy" were approved on 2026-11-11; the others remain provisional.', '']""")
save(p, s)
print('ok')
