"""print full text of pages a-b of a NEW-archive file: python ztext.py NAME a b"""
# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import re, sys, zipfile, pymupdf
z = zipfile.ZipFile(r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip')
n, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = pymupdf.open(stream=z.read('Downloaded lubricants sheets/' + n), filetype='pdf')
for i in range(a, min(b, len(d)) + 1):
    print(f'--- {n} p.{i}/{len(d)} ---', re.sub(r'\s+', ' ', d[i - 1].get_text()))
