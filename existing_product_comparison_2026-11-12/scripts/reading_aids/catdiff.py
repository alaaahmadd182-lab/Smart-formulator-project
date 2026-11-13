# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import subprocess, sys, re
S = 'existing_product_comparison_2026-11-12/scripts/show.py'
def text(side, f, pages):
    out = subprocess.run([sys.executable, S, side, f, pages, '9000'], capture_output=True, text=True, encoding='utf-8').stdout
    return re.sub(r'\s+', ' ', out.split('---', 1)[-1] if '---' in out else out)
def page_of(f, pid):
    out = subprocess.run([sys.executable, S, 'grep', 'new', f, pid + r'\s*[A-Z]{2}-?\d.*(Package|Additive)'], capture_output=True, text=True, encoding='utf-8').stdout
    ps = sorted({int(m) for m in re.findall(r'^p(\d+):', out, re.M) if int(m) > 2})
    return ps
nums = lambda t: re.findall(r'(?<![\w.])[≥≤<>]?-?\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?%?', t)
for cat, pid, old_side, old in [x.split('|') for x in sys.argv[1:]]:
    ps = page_of(cat, pid)
    c = text('new', cat, ','.join(map(str, ps)))
    o = text(old_side, old, '1')
    print(f'===== {pid}: {cat} pages {ps} vs {old} ({old_side})')
    print('NEW:', c[:2600]); print('OLD:', o[:2600])
    cn, on = nums(c), nums(o)
    print('only in NEW:', [n for n in cn if n not in on]); print('only in OLD:', [n for n in on if n not in cn])
