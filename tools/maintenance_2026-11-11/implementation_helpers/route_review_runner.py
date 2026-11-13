"""One-off helper (2026-11-12): snapshot scope and two runner steps. Already applied; do not rerun."""
R = 'C:\\Users\\windo\\sf-wsA\\'


def edit(rel, reps):
    p = R + rel
    s = open(p, encoding='utf-8').read()
    for a, b in reps:
        assert s.count(a) == 1, (rel, a[:60], s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


edit('tools\\data_policy\\make_review_snapshot.py', [
    ("'Coverage_Matrix.xlsx', 'reports', 'docs/data_policy_mandatory_review']", "'Coverage_Matrix.xlsx', 'reports', 'docs/data_policy_mandatory_review', 'Products_json']"),
    ("Not copied: .git, __pycache__, earlier snapshots, the source archive (referenced by its SHA-256), the product JSON\n"
     "(referenced by its fingerprint; the files are in the repository), and anything outside the listed paths.",
     "The product JSON is copied too, because two of its files differ from the last commit. Not copied: .git, __pycache__,\n"
     "earlier snapshots, the source archive (referenced by its SHA-256), and anything outside the listed paths."),
    ("JSON files, not copied into the snapshot',", "JSON files, copied into the snapshot',"),
    ("the source archive, the product JSON, earlier snapshots, and any dataset", "the source archive, earlier snapshots, and any dataset"),
    ("code, policy inputs, reports, documentation and test results, made by", "code, policy inputs, product JSON, reports, documentation and test results, made by"),
])
B = 'docs/data_policy_mandatory_review/baselines/'
edit('tools\\data_policy\\run_checks.py', [
    ("    ('compare_eligibility', ['tools/mandatory_properties/compare_eligibility.py'], 'zero', r'interface columns identical: True'),\n",
     "    ('compare_eligibility', ['tools/mandatory_properties/compare_eligibility.py'], 'zero', r'interface columns identical: True'),\n"
     "    ('compare_eligibility_pre_route_review', ['tools/mandatory_properties/compare_eligibility.py',\n"
     f"      '--before-eligibility', '{B}pre_route_review_2026-11-12/reports/mandatory_properties/product_eligibility.csv',\n"
     f"      '--before-outcomes', '{B}pre_route_review_2026-11-12/reports/mandatory_properties/requirement_outcomes.csv',\n"
     f"      '--out', '{B}eligibility_changes__route_review_2026-11-12.csv'], 'zero', r'interface columns identical: True'),\n"),
])
print('ok')
