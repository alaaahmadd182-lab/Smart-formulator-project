"""Self-relaunching OCR daemon for Windows.

Spawns 01_ocr.py --limit BATCH as a detached subprocess, waits for it,
then immediately spawns the next batch. Writes progress to daemon.log.
Exits cleanly once all documents are cached.

Usage: python 01_ocr_daemon.py [--batch N]
"""
import csv, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PKG  = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
OUT  = os.path.join(PKG, '_cache', 'ocr')
SCRIPT = os.path.join(HERE, '01_ocr.py')
LOGFILE = os.path.join(PKG, 'logs', 'daemon.log')

batch = int(sys.argv[sys.argv.index('--batch') + 1]) if '--batch' in sys.argv else 30

U = [r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))
     if r['readability'] != 'text' or r['kind'] in ('docx',)]
total = len(U)

def cached_count():
    return sum(1 for f in os.listdir(OUT) if f.endswith('.json.gz'))

def log(msg):
    ts = time.strftime('%H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    with open(LOGFILE, 'a', encoding='utf-8') as fh:
        fh.write(line + '\n')

log(f'daemon started: total={total} batch={batch}')
run = 0
while True:
    n = cached_count()
    if n >= total:
        log(f'ALL DONE: {n}/{total} cached')
        break
    run += 1
    log(f'run {run}: {n}/{total} cached, spawning batch={batch}')
    t0 = time.time()
    # Use subprocess.run with a generous timeout — detached not needed since
    # we wait synchronously; the daemon itself is the long-lived process.
    try:
        proc = subprocess.run(
            [sys.executable, '-I', SCRIPT, '--limit', str(batch)],
            cwd=HERE,
            timeout=1800,   # 30 min hard cap per batch
        )
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        rc = -1
        log(f'run {run}: subprocess timed out after 1800s')
    n2 = cached_count()
    added = n2 - n
    elapsed = round(time.time() - t0, 1)
    log(f'run {run}: +{added} cached in {elapsed}s (rc={rc}), total={n2}/{total}')
    if added == 0 and n2 < total:
        log('WARNING: no progress — stopping')
        break
