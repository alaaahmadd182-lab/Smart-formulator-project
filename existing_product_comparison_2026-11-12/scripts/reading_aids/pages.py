"""print full text of pages a-b of an archive file: python pages.py FILE a b"""
# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import gzip, json, re, sys
INV = 'incoming_dataset_review_2026-11-12'
ref = json.load(open(f'{INV}/_cache/reference.json', encoding='utf-8'))
mem = {m['name'].split('/')[-1]: m for m in ref['archive']['members']}
f, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
m = mem.get(f) or mem[f.replace('%20', ' ')]
pages = gzip.open(f'{INV}/_cache/ref_text/{m["sha256"]}.txt.gz', 'rt', encoding='utf-8').read().split('\f')
for i in range(a, min(b, len(pages)) + 1):
    print(f'--- {f} p.{i}/{len(pages)} ---', re.sub(r'\s+', ' ', pages[i - 1]))
