"""Incoming dataset inventory, pass 1: read every member of the new archive (read-only; nothing is ingested).

Reads 'Downloaded lubricants sheets.zip' in place, one member at a time, in memory. The archive is never modified and
the collection is never extracted to disk. For every file it records the archive-relative path, the type by content
(magic bytes), size, CRC and SHA-256, and for PDFs the page count, how many pages have a text layer, the document
metadata dates and a hash of the normalised text. The extracted text is kept in a local cache (_cache/, ignored by
Git) so that the later passes can classify and compare without reading the archive again.

Readability of a PDF:
  text          every page has a text layer
  partial_text  some pages have a text layer
  image_only    no page has a text layer (no OCR engine is installed: such a file is NOT read, which is not the same
                as containing no information)
  encrypted / error

Usage: python incoming_dataset_review_2026-11-12/scripts/01_extract.py [--zip PATH] [--workers N]
Outputs: _cache/members.jsonl (one line per archive member) and _cache/text/<sha256>.txt.gz (one per unique file with text)
"""
import argparse, concurrent.futures as cf, gzip, hashlib, io, json, os, re, sys, time, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
CACHE = os.path.join(BASE, '_cache')
DEFAULT_ZIP = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip'
MAGIC = [(b'%PDF', 'pdf'), (b'\xff\xd8\xff', 'jpeg'), (b'\x89PNG', 'png'), (b'PK\x03\x04', 'zip_container'), (b'\xd0\xcf\x11\xe0', 'ole2'),
         (b'GIF8', 'gif'), (b'Rar!', 'rar'), (b'7z\xbc\xaf', '7z'), (b'<!DOCTYPE', 'html'), (b'<html', 'html')]


def kind_of(data, name):
    head = data[:1024].lstrip()
    for m, k in MAGIC:
        if head.startswith(m):
            if k == 'zip_container':
                try:
                    names = zipfile.ZipFile(io.BytesIO(data)).namelist()
                except Exception:
                    return 'zip_unreadable'
                if any(n.startswith('xl/') for n in names):
                    return 'xlsx'
                if any(n.startswith('word/') for n in names):
                    return 'docx'
                if any(n.startswith('ppt/') for n in names):
                    return 'pptx'
                return 'zip_archive'
            return k
    if b'%PDF' in data[:2048]:
        return 'pdf'
    return 'unknown'


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def office_text(data, kind):
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
        parts = []
        for n in z.namelist():
            if n.endswith('.xml') and (n.startswith('word/document') or n.startswith('ppt/slides/slide') or n == 'xl/sharedStrings.xml'):
                parts.append(re.sub(r'<[^>]+>', ' ', z.read(n).decode('utf-8', 'replace')))
        return norm(' '.join(parts))
    except Exception as e:
        return ''


def process(args):
    zpath, name = args
    import pymupdf
    pymupdf.TOOLS.mupdf_display_errors(False)
    with zipfile.ZipFile(zpath) as z:
        info = z.getinfo(name)
        data = z.read(name)
    sha = hashlib.sha256(data).hexdigest()
    kind = kind_of(data, name)
    rec = dict(path=name, size=info.file_size, crc32=f'{info.CRC:08x}', sha256=sha, extension=os.path.splitext(name)[1].lower(), kind=kind,
               pages=None, pages_with_text=None, readability='', text_chars=0, text_sha256='', meta_creation='', meta_mod='', meta_title='',
               meta_producer='', image_size='', error='')
    text_pages = None
    try:
        if kind == 'pdf':
            d = pymupdf.open(stream=data, filetype='pdf')
            if d.needs_pass:
                rec.update(readability='encrypted', pages=d.page_count)
            else:
                text_pages = [p.get_text() for p in d]
                with_text = sum(1 for t in text_pages if len(t.strip()) >= 20)
                m = d.metadata or {}
                rec.update(pages=d.page_count, pages_with_text=with_text, meta_creation=m.get('creationDate') or '', meta_mod=m.get('modDate') or '',
                           meta_title=(m.get('title') or '')[:200], meta_producer=(m.get('producer') or '')[:80],
                           readability='text' if with_text == d.page_count and d.page_count else 'partial_text' if with_text else 'image_only')
        elif kind in ('jpeg', 'png', 'gif'):
            from PIL import Image
            im = Image.open(io.BytesIO(data))
            rec.update(image_size=f'{im.width}x{im.height}', readability='image_only')
        elif kind in ('xlsx', 'docx', 'pptx'):
            t = office_text(data, kind)
            text_pages = [t]
            rec['readability'] = 'text' if t else 'no_text_extracted'
        else:
            rec['readability'] = 'not_read'
    except Exception as e:
        rec.update(readability='error', error=repr(e)[:200])
    if text_pages is not None:
        full = '\f'.join(text_pages)
        n = norm(full)
        rec['text_chars'] = len(n)
        if n:
            rec['text_sha256'] = hashlib.sha256(n.encode('utf-8')).hexdigest()
            p = os.path.join(CACHE, 'text', sha + '.txt.gz')
            if not os.path.exists(p):
                with gzip.open(p, 'wt', encoding='utf-8') as fh:
                    fh.write(full)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip', default=DEFAULT_ZIP)
    ap.add_argument('--workers', type=int, default=8)
    a = ap.parse_args()
    os.makedirs(os.path.join(CACHE, 'text'), exist_ok=True)
    t0 = time.time()
    with zipfile.ZipFile(a.zip) as z:
        infos = z.infolist()
        names = [i.filename for i in infos if not i.is_dir()]
        dirs = [i.filename for i in infos if i.is_dir()]
    print(f'archive: {a.zip}\nsize: {os.path.getsize(a.zip)} bytes; entries {len(infos)}; files {len(names)}; directories {len(dirs)}: {dirs}', flush=True)
    out = os.path.join(CACHE, 'members.jsonl')
    done = 0
    with cf.ProcessPoolExecutor(a.workers) as ex, open(out, 'w', encoding='utf-8') as fh:
        for rec in ex.map(process, [(a.zip, n) for n in names], chunksize=8):
            fh.write(json.dumps(rec, ensure_ascii=False) + '\n')
            done += 1
            if done % 500 == 0:
                print(f'  {done}/{len(names)} after {time.time() - t0:.0f} s', flush=True)
    print(f'done: {done} members in {time.time() - t0:.0f} s -> {out}')


if __name__ == '__main__':
    sys.exit(main())
