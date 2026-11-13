"""Render pages of a document of the NEW archive to PNG for visual verification (read-only on the archive).

  python render.py <file name> <page> [dpi] [x0,y0,x1,y1 as fractions of the page]
Writes _cache/render/<file>_p<page>.png (cache folder, ignored by Git) and prints the path.
"""
import os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ZIP = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip'


def main():
    import pymupdf
    name, page = sys.argv[1], int(sys.argv[2])
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 80
    out = os.path.join(BASE, '_cache', 'render')
    os.makedirs(out, exist_ok=True)
    with zipfile.ZipFile(ZIP) as z:
        data = z.read('Downloaded lubricants sheets/' + name)
    d = pymupdf.open(stream=data, filetype='pdf')
    pg = d[page - 1]
    clip = None
    if len(sys.argv) > 4:
        a, b, c, e = [float(x) for x in sys.argv[4].split(',')]
        r = pg.rect
        clip = pymupdf.Rect(r.x0 + a * r.width, r.y0 + b * r.height, r.x0 + c * r.width, r.y0 + e * r.height)
    tag = '' if clip is None else '_' + sys.argv[4].replace(',', '-').replace('.', '')
    p = os.path.join(out, f'{name}_p{page}{tag}.png')
    pg.get_pixmap(dpi=dpi, clip=clip).save(p)
    print(p)


if __name__ == '__main__':
    main()
