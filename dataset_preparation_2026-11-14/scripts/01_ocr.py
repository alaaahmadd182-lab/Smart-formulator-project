"""OCR of every page of the incoming archive that has no usable text layer (read-only on the archive).

Inputs : incoming_dataset_review_2026-11-12/tables/unique_documents.csv (readability, kind) and the archive ZIP.
Output : _cache/ocr/<sha256>.json.gz per document: {"sha256", "kind", "pages": [{"page", "source": "text_layer"|"ocr"|"none",
         "text", "mean_conf"}], "tool": {...}} and logs/01_ocr.log. Resumable (documents already cached are skipped).
Scope  : PDF pages whose text layer has fewer than 20 non-space characters are rendered at 150 dpi and OCR'd; JPEG / PNG files
         are OCR'd directly; .docx text is read from word/document.xml; .xls (OLE2) cells are read with xlrd.
OCR text is a reading aid for identity and evidence location. It is NOT authoritative: any value used as evidence must be checked
on the page image (OCR confuses e.g. 'l' and 'I'). Usage: python 01_ocr.py [--limit N]
"""
import csv, gzip, io, json, os, re, sys, time, zipfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
sys.path.insert(0, HERE)
from paths import ARCHIVE_ZIP as ZIP, OCR_CACHE as OUT
DPI = 150


def tool_versions():
    import importlib.metadata as md
    v = {}
    for p in ('rapidocr-onnxruntime', 'onnxruntime', 'pymupdf', 'xlrd', 'numpy', 'pillow'):
        try:
            v[p] = md.version(p)
        except Exception:
            v[p] = 'not installed'
    v['python'] = sys.version.split()[0]
    return v


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None
    os.makedirs(OUT, exist_ok=True)
    import pymupdf
    from rapidocr_onnxruntime import RapidOCR
    from PIL import Image
    ocr = RapidOCR()
    tools = tool_versions()
    with open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8') as fh:
        U = [r for r in csv.DictReader(fh) if r['readability'] != 'text' or r['kind'] in ('docx',)]
    z = zipfile.ZipFile(ZIP)
    log = open(os.path.join(PKG, 'logs', '01_ocr.log'), 'a', encoding='utf-8')
    done = 0
    for r in U:
        out = os.path.join(OUT, r['sha256'] + '.json.gz')
        if os.path.exists(out):
            continue
        if limit is not None and done >= limit:
            break
        t0 = time.time()
        data = z.read('Downloaded lubricants sheets/' + r['first_path'])
        pages = []

        def run(img):
            res, _ = ocr(img)
            if not res:
                return '', None
            return '\n'.join(x[1] for x in res), round(float(np.mean([x[2] for x in res])), 3)
        try:
            if r['kind'] == 'pdf':
                d = pymupdf.open(stream=data, filetype='pdf')
                for i, pg in enumerate(d, 1):
                    t = pg.get_text()
                    if len(re.sub(r'\s', '', t)) >= 20:
                        pages.append(dict(page=i, source='text_layer', text='', mean_conf=None))
                        continue
                    pix = pg.get_pixmap(dpi=DPI)
                    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3]
                    txt, conf = run(img)
                    pages.append(dict(page=i, source='ocr' if txt else 'none', text=txt, mean_conf=conf))
            elif r['kind'] in ('jpeg', 'png'):
                im = Image.open(io.BytesIO(data)).convert('RGB')
                if max(im.size) > 2600:
                    im.thumbnail((2600, 2600))
                txt, conf = run(np.array(im))
                pages.append(dict(page=1, source='ocr' if txt else 'none', text=txt, mean_conf=conf))
            elif r['kind'] == 'docx':
                x = zipfile.ZipFile(io.BytesIO(data)).read('word/document.xml').decode('utf-8', 'replace')
                txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x.replace('</w:p>', '\n'))).strip()
                pages.append(dict(page=1, source='docx_xml', text=txt, mean_conf=None))
            elif r['kind'] == 'ole2':
                import xlrd
                wb = xlrd.open_workbook(file_contents=data)
                for si, sh in enumerate(wb.sheets(), 1):
                    rows = [' | '.join(str(c.value) for c in sh.row(i) if str(c.value).strip()) for i in range(sh.nrows)]
                    pages.append(dict(page=si, source=f'xls sheet {sh.name!r}', text='\n'.join(x for x in rows if x), mean_conf=None))
            status = 'ok'
        except Exception as e:
            status = f'ERROR {type(e).__name__}: {e}'
        json.dump(dict(sha256=r['sha256'], kind=r['kind'], first_path=r['first_path'], status=status, dpi=DPI, pages=pages, tool=tools),
                  gzip.open(out, 'wt', encoding='utf-8'), ensure_ascii=False)
        log.write(f"{r['sha256'][:12]}\t{r['kind']}\t{len(pages)} pages\t{sum(p['source'] == 'ocr' for p in pages)} ocr\t{round(time.time() - t0, 1)} s\t{status}\n")
        log.flush()
        done += 1
    print('documents processed', done)


if __name__ == '__main__':
    main()
