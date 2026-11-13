"""Reading aid (read-only): print one new-archive document's pages beside one product's recorded values.

  python dupcmp.py PRODUCT_ID FILE [pages e.g. 1-3]

For each value object in the product's JSON files: field path, value / min / max / qualifier / value_kind, printed_text, unit, method,
temperature, cited file and page; values citing FILE are marked '*'. Missing fields are listed by name. Open questions and
conflicts that mention FILE are printed. It does not decide anything: the reviewer compares the printed page with the record.
"""
import glob, json, os, re, sys, zipfile
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ZIP = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip'


def walk(k, v, out):
    if isinstance(v, list):
        for i, e in enumerate(v):
            walk(f'{k}[{i}]', e, out)
    elif isinstance(v, dict) and 'status' in v:
        out.append((k, v))
    elif isinstance(v, dict):
        for kk, vv in v.items():
            walk(f'{k}.{kk}', vv, out)


def main():
    pid, f = sys.argv[1], sys.argv[2]
    z = zipfile.ZipFile(ZIP)
    names = {n.rsplit('/', 1)[-1]: n for n in z.namelist()}
    if f in names:
        ext = f.rsplit('.', 1)[-1].lower()
        d = pymupdf.open(stream=z.read(names[f]), filetype='pdf' if ext == 'pdf' else ext.replace('jfif', 'jpg'))
        a, b = (1, len(d)) if len(sys.argv) < 4 else map(int, sys.argv[3].split('-'))
        for i in range(a, b + 1):
            print(f'--- {f} p.{i}/{len(d)} ---', re.sub(r'\s+', ' ', d[i - 1].get_text()))
    else:
        print(f'--- {f}: not in the new archive ---')
    for jf in sorted(glob.glob(os.path.join(ROOT, 'Products_json', '**', pid, '*.json'), recursive=True)):
        j = json.load(open(jf, encoding='utf-8'))
        out = []
        for k, v in j.get('fields', {}).items():
            walk(k, v, out)
        miss = [k for k, v in out if v.get('status') == 'Missing']
        print(f'## {os.path.basename(jf)} (tier {j.get("tier")})')
        for k, v in out:
            if v.get('status') == 'Missing':
                continue
            s = v.get('source') or {}
            mark = '*' if s.get('file') == f else ' '
            print(f" {mark} {k}: {v.get('value')!r} min={v.get('min')!r} max={v.get('max')!r} q={v.get('qualifier')!r} vk={v.get('value_kind')!r} pt={str(v.get('printed_text'))[:70]!r} "
                  f"u={v.get('unit')!r} m={v.get('method')!r} T={v.get('test_temperature_c')!r} [{v.get('status')}] <{str(s.get('file'))[:40]} p{s.get('page')}>"
                  + (f" ALT={len(v['alternate_entries'])}" if v.get('alternate_entries') else ''))
        print('   Missing:', ', '.join(miss))
        for q in j.get('open_questions', []) + j.get('conflicts', []):
            t = q if isinstance(q, str) else json.dumps(q, ensure_ascii=False)
            if f in t or f.split('.')[0] in t:
                print('   OQ/CF:', t[:400])


if __name__ == '__main__':
    main()
