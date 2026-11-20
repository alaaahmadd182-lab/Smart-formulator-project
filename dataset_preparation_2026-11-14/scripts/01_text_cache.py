"""Extract text from text-layer PDFs linked to eligible products (not in OCR cache).

Reads every unique PDF with readability='text' that is linked to an eligible product
(stage2=verified, stage3=established, field_mapping not started) from the archive ZIP
and writes to _cache/ocr/<sha256>.json.gz in the same format as 01_ocr.py output,
with source='text_layer'.

Also handles readability='partial_text' PDFs (some image pages + some text pages):
the OCR cache already has them for image pages (source='ocr'); this script skips any
sha256 already in the cache.

Usage: python 01_text_cache.py [--all]

Without --all: only processes documents linked to eligible products.
With --all   : processes all text-layer PDFs in unique_documents.csv.
"""
import csv, gzip, json, os, re, sys, time, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG  = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
ZIP  = os.path.join(ROOT, 'Downloaded lubricants sheets.zip')
OUT  = os.path.join(PKG, '_cache', 'ocr')
LOG  = os.path.join(PKG, 'logs', '01_text_cache.log')


def eligible_shas():
    """sha256s linked to eligible (verified+established, not started) products."""
    stages = list(csv.DictReader(open(os.path.join(PKG,'tables','product_stages.csv'),encoding='utf-8')))
    pkeys = {r['product_key'] for r in stages
             if r['stage2_identity']=='verified'
             and r['stage3_class_template']=='established'
             and r['stage5_field_mapping']=='not started'}
    links = list(csv.DictReader(open(os.path.join(PKG,'tables','document_product_links.csv'),encoding='utf-8')))
    return {lk['sha256'] for lk in links if lk['product_key'] in pkeys}


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    all_mode = '--all' in sys.argv
    limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None

    import pymupdf

    os.makedirs(OUT, exist_ok=True)
    cached = {f.replace('.json.gz','') for f in os.listdir(OUT) if f.endswith('.json.gz')}

    udocs = list(csv.DictReader(open(os.path.join(INV,'tables','unique_documents.csv'),encoding='utf-8')))
    # target: text-layer PDFs (and partial-text that aren't already cached)
    if all_mode:
        targets = [r for r in udocs if r['kind']=='pdf' and r['readability'] in ('text','partial_text')]
    else:
        wanted = eligible_shas()
        targets = [r for r in udocs
                   if r['sha256'] in wanted
                   and r['kind'] in ('pdf','pptx')
                   and r['readability'] in ('text','partial_text')]

    # skip already cached
    targets = [r for r in targets if r['sha256'] not in cached]
    total = len(targets)
    print(f'Text-layer documents to cache: {total}')

    z = zipfile.ZipFile(ZIP)
    log = open(LOG, 'a', encoding='utf-8')
    done = 0

    for r in targets:
        if limit is not None and done >= limit:
            break
        out_path = os.path.join(OUT, r['sha256'] + '.json.gz')
        t0 = time.time()
        pages = []
        status = 'ok'
        try:
            data = z.read('Downloaded lubricants sheets/' + r['first_path'])
            if r['kind'] == 'pdf':
                doc = pymupdf.open(stream=data, filetype='pdf')
                for i, pg in enumerate(doc, 1):
                    txt = pg.get_text()
                    if len(re.sub(r'\s', '', txt)) >= 20:
                        pages.append(dict(page=i, source='text_layer', text=txt, mean_conf=None))
                    else:
                        # image page within a partial-text PDF — no OCR here; mark as none
                        pages.append(dict(page=i, source='none', text='', mean_conf=None))
            elif r['kind'] == 'pptx':
                # read pptx slide text via zip
                import io
                pz = zipfile.ZipFile(io.BytesIO(data))
                slide_files = sorted(n for n in pz.namelist() if re.match(r'ppt/slides/slide\d+\.xml', n))
                for si, sf in enumerate(slide_files, 1):
                    xml = pz.read(sf).decode('utf-8', 'replace')
                    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', xml)).strip()
                    pages.append(dict(page=si, source='pptx_xml', text=txt, mean_conf=None))
        except Exception as e:
            status = f'ERROR {type(e).__name__}: {e}'

        json.dump(
            dict(sha256=r['sha256'], kind=r['kind'], first_path=r['first_path'],
                 status=status, dpi=None, pages=pages, tool={'extractor': 'text_layer'}),
            gzip.open(out_path, 'wt', encoding='utf-8'),
            ensure_ascii=False
        )
        elapsed = round(time.time() - t0, 2)
        log.write(f"{r['sha256'][:12]}\t{r['kind']}\t{len(pages)} pages\t{elapsed}s\t{status}\n")
        log.flush()
        done += 1
        if done % 50 == 0:
            print(f'  {done}/{total} done', flush=True)

    print(f'Done: {done} documents cached')


if __name__ == '__main__':
    main()
