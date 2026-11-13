import json, sys
sys.path.insert(0, r'C:\Users\windo\sf-wsA\tools\data_policy')
sys.stdout.reconfigure(encoding='utf-8')
import policy_lib as P
pr = P.load_products()
T = {'RICHFUL_RF6066': ['flash_point', 'kv100', 'density'], 'RICHFUL_RF6069': ['flash_point', 'density', 'kv100'],
     'RICHFUL_RF6077': ['flash_point', 'density', 'kv100'], 'RICHFUL_RF6078': ['flash_point', 'kv100', 'density'],
     'RICHFUL_RF6079': ['flash_point', 'density', 'kv100'], 'RICHFUL_RF6088': ['flash_point', 'density', 'kv100'],
     'RICHFUL_RF6088F': ['flash_point', 'kv100', 'density'], 'RICHFUL_RF6400': ['flash_point', 'density', 'kv100'],
     'RICHFUL_RF6406': ['flash_point', 'density', 'kv100'], 'INFINEUM_D3424': ['flash_point'],
     'NESTE_NEXBASE_3020': ['kv40', 'kv100', 'density', 'pour_point', 'flash_point', 'viscosity_index']}
for pid, keys in T.items():
    for f, d in pr[pid]['files'].items():
        for k in keys:
            if k in d['fields']:
                n = d['fields'][k]
                print(pid, f.split('/')[-1], k, json.dumps({x: n.get(x) for x in n if x not in ('value_final', 'unit_final', 'min_final', 'max_final', 'unit_conversion')}, ensure_ascii=False)[:700])
        for c in d.get('conflicts') or []:
            s = json.dumps(c, ensure_ascii=False)
            if any(k in s for k in keys):
                print('   CONFLICT', s[:400])
