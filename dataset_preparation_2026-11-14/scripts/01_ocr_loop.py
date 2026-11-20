"""Run 01_ocr.py in repeated subprocesses until every document is cached.

Each subprocess is limited to --limit N so it stays inside a reasonable memory
window; the outer loop restarts until the cache count reaches the expected total.
Usage: python 01_ocr_loop.py [--batch N]   (default batch = 50)
"""
import csv, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
OUT = os.path.join(PKG, '_cache', 'ocr')
SCRIPT = os.path.join(HERE, '01_ocr.py')

batch = int(sys.argv[sys.argv.index('--batch') + 1]) if '--batch' in sys.argv else 50

U = [r for r in csv.DictReader(open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))
     if r['readability'] != 'text' or r['kind'] in ('docx',)]
total = len(U)
print(f'Total needing OCR: {total}', flush=True)

run = 0
while True:
    cached = sum(1 for f in os.listdir(OUT) if f.endswith('.json.gz'))
    if cached >= total:
        print(f'All {cached}/{total} cached. Done.', flush=True)
        break
    run += 1
    remaining = total - cached
    this_batch = min(batch, remaining)
    print(f'[run {run}] {cached}/{total} cached, running batch of {this_batch}...', flush=True)
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, '-I', SCRIPT, '--limit', str(this_batch)],
        cwd=HERE,
        timeout=900,
    )
    elapsed = round(time.time() - t0, 1)
    cached_after = sum(1 for f in os.listdir(OUT) if f.endswith('.json.gz'))
    added = cached_after - cached
    print(f'[run {run}] +{added} cached in {elapsed}s (rc={result.returncode})', flush=True)
    if added == 0 and cached_after < total:
        print('WARNING: no progress in this run — stopping to avoid infinite loop', flush=True)
        break
