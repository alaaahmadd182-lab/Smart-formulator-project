"""Index the text of every PDF page in the archive, reading members in memory (no extraction).
Usage: python index_pdfs.py <zip> <index.json>"""
import json, os, sys, zipfile
import pymupdf
zp, idx = sys.argv[1:3]
z = zipfile.ZipFile(zp); index = {}
for info in z.infolist():
    name = info.filename
    if name.endswith('/'): continue
    base = os.path.basename(name); entry = {'path': name, 'size': info.file_size}
    if base.lower().endswith('.pdf'):
        try:
            doc = pymupdf.open(stream=z.read(name), filetype='pdf'); pages = [p.get_text() for p in doc]
            entry.update(pages=pages, chars=sum(len(p.strip()) for p in pages), npages=len(pages),
                         images=sum(len(p.get_images()) for p in doc))
        except Exception as e:
            entry['error'] = str(e)
    index.setdefault(base, []).append(entry)
json.dump(index, open(idx, 'w', encoding='utf-8'), ensure_ascii=False)
pdfs = [e for v in index.values() for e in v if e['path'].lower().endswith('.pdf')]
print('files', sum(len(v) for v in index.values()), '| pdfs', len(pdfs), '| pdfs with no text layer', sum(1 for e in pdfs if not e.get('chars')),
      '| errors', sum(1 for e in pdfs if 'error' in e), '| duplicate basenames', [k for k, v in index.items() if len(v) > 1][:10])
