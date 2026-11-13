"""One-off helper (2026-11-11, gap fixes): version .5, older tests adjusted to the route-level co-component rule.
Already applied; do not rerun (each replacement asserts that its target occurs exactly once)."""
R = 'C:\\Users\\windo\\sf-wsA\\'


def edit(rel, reps):
    p = R + rel
    s = open(p, encoding='utf-8').read()
    for a, b in reps:
        assert s.count(a) == 1, (rel, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


edit('tools\\mandatory_properties\\requirements.py', [
    ("REQUIREMENTS_VERSION = 'mandatory-tier1-2026-11-10.4'", "REQUIREMENTS_VERSION = 'mandatory-tier1-2026-11-10.5'"),
    ("Policies approved on 2026-11-11 (version .4; requirements_review.md section 4):",
     "Policies approved on 2026-11-11 (version .4; corrected in .5 the same day; requirements_review.md section 4a):"),
])
edit('tools\\mandatory_properties\\tests\\test_requirements.py', [
    ("self.assertEqual(R.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.4')", "self.assertEqual(R.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.5')"),
    ("""        stmt = vo('no additional co-component required', unit=None)
        self.assertEqual(cats(R.additive_package_requirements(pk(co_component_requirement_statement=stmt)))['required_co_components'], R.MET)
""", """        stmt = vo('no additional co-component required', unit=None)   # free text is not an explicit, applicable statement (.5)
        self.assertEqual(cats(R.additive_package_requirements(pk(co_component_requirement_statement=stmt)))['required_co_components'], R.META)
"""),
    ("""        outs = R.additive_package_requirements(pk(required_co_components=[e]), ctx(basis=basis))
        self.assertEqual(cats(outs)['required_co_components'], R.MET)""",
     """        outs = R.additive_package_requirements(pk(required_co_components=[e]), ctx(basis=basis))
        # the dose is usable (mass basis from evidence), but one usable component is not a complete route (.5)
        self.assertEqual(cats(outs)['required_co_components'], R.ROUTE)
        self.assertEqual(R.co_component_entries(dict(required_co_components=[e]), ctx(basis=basis))[0]['state'], 'required_usable_dose')"""),
])
edit('tools\\data_policy\\tests\\test_data_policy.py', [
    ("self.assertEqual(REQ.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.4')", "self.assertEqual(REQ.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.5')"),
])
print('ok')
