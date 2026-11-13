import json, os, sys
R = r'C:\Users\windo\sf-wsA'
sys.path.insert(0, os.path.join(R, 'tools', 'data_policy'))

# 1. source_selection.py: drop the duplicate CONFLICT_ADDS entry and reword the pending reason
p = os.path.join(R, 'tools', 'data_policy', 'source_selection.py')
s = open(p, encoding='utf-8').read()
start = s.index("    ('S_OIL_ARAMCO_ULTRA_8', 'S_OIL_ARAMCO_ULTRA_8_tier1.json', dict(\n        id='EVR-2026-11-11-ULTRA8-kv40'")
end = s.index("the field stays pending.')),\n", start) + len("the field stays pending.')),\n")
s = s[:start] + s[end:]
a = "the KV40 typical 41.10 lies below the SDS range (conflict EVR-2026-11-11-ULTRA8-kv40).'"
b = "the KV40 typical 41.10 lies below the SDS range 42.0-55.0 (already recorded as an unresolved conflict by the 2026-10 audit).'"
assert s.count(a) == 1
s = s.replace(a, b)
assert 'ULTRA8-kv40' not in s
open(p, 'w', encoding='utf-8', newline='\n').write(s)

# 2. product JSON: remove the entry with that id (written with the tool's own serializer)
import policy_lib as P  # noqa: E402
import source_selection as S  # noqa: E402
rel = 'Products_json/Base_oils_json/S_OIL/S_OIL_ARAMCO_ULTRA_8/S_OIL_ARAMCO_ULTRA_8_tier1.json'
d = P.load(rel)
before = len(d['conflicts'])
d['conflicts'] = [c for c in d['conflicts'] if not (isinstance(c, dict) and c.get('id') == 'EVR-2026-11-11-ULTRA8-kv40')]
assert len(d['conflicts']) == before - 1
S.write_json(rel, d)

# 3. external review decisions: point to the existing conflict
p = os.path.join(R, 'tools', 'data_policy', 'external_review_decisions.json')
s = open(p, encoding='utf-8').read()
reps = [
    ("the external typical 41.10 lies below the SDS range: logically incompatible, recorded as conflict EVR-2026-11-11-ULTRA8-kv40",
     "the external typical 41.10 lies below the SDS range: logically incompatible; already recorded as an unresolved edition-difference conflict by the 2026-10 audit (tier-1 conflicts[], 41.1 vs 42.0 - 55.0)"),
    ('"change": "conflict recorded (not resolved)"', '"change": "none (the conflict already exists)"'),
]
for a, b in reps:
    assert s.count(a) == 1, a[:50]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='\n').write(s)

# 4. test: two new conflicts, not three
p = os.path.join(R, 'tools', 'data_policy', 'tests', 'test_data_policy.py')
s = open(p, encoding='utf-8').read()
a = """        for pid, cid in (('ARAMCO_LUBEREF_PRIMA_230', 'EVR-2026-11-11-230-noack'), ('ARAMCO_LUBEREF_PRIMA_230', 'EVR-2026-11-11-230-density-external'),
                         ('S_OIL_ARAMCO_ULTRA_8', 'EVR-2026-11-11-ULTRA8-kv40')):"""
b = """        for pid, cid in (('ARAMCO_LUBEREF_PRIMA_230', 'EVR-2026-11-11-230-noack'), ('ARAMCO_LUBEREF_PRIMA_230', 'EVR-2026-11-11-230-density-external')):"""
assert s.count(a) == 1
s = s.replace(a, b)
s = s.replace("""            self.assertIs(hits[0]['resolved'], False)

    def test_review_states_partition_the_ledger(self):""", """            self.assertIs(hits[0]['resolved'], False)
        # the aramcoULTRA 8 KV40 disagreement was already a conflict (2026-10 audit); it is not recorded twice
        u8 = [c for d in prods['S_OIL_ARAMCO_ULTRA_8']['files'].values() for c in d.get('conflicts') or []
              if isinstance(c, dict) and 'kv40' in str(c.get('field'))]
        self.assertEqual(len(u8), 1)

    def test_review_states_partition_the_ledger(self):""", 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
