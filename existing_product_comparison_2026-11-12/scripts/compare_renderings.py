"""Compare two documents of the new archive page by page as rendered images (read-only).

Identical extracted text does not establish identical content (figures, marks and colours are not text). This renders
every page of both files at the same resolution and reports, per page, the share of pixels that differ by more than a
small tolerance and the largest difference. Usage: python compare_renderings.py <file A> <file B> [dpi]
"""
import sys, zipfile

ZIP = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip'


def main():
    import pymupdf
    from PIL import Image, ImageChops
    a, b = sys.argv[1], sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    with zipfile.ZipFile(ZIP) as z:
        da = pymupdf.open(stream=z.read('Downloaded lubricants sheets/' + a), filetype='pdf')
        db = pymupdf.open(stream=z.read('Downloaded lubricants sheets/' + b), filetype='pdf')
    print(f'{a}: {da.page_count} pages; {b}: {db.page_count} pages; rendered at {dpi} dpi')
    worst, differing = 0.0, []
    for i in range(min(da.page_count, db.page_count)):
        pa, pb = da[i].get_pixmap(dpi=dpi, alpha=False), db[i].get_pixmap(dpi=dpi, alpha=False)
        if (pa.width, pa.height) != (pb.width, pb.height):
            differing.append((i + 1, 'different page size'))
            continue
        ia, ib = Image.frombytes('RGB', (pa.width, pa.height), pa.samples), Image.frombytes('RGB', (pb.width, pb.height), pb.samples)
        d = ImageChops.difference(ia, ib).convert('L')
        hist = d.histogram()
        over = sum(hist[9:]) / (pa.width * pa.height)
        mx = max(i2 for i2, c in enumerate(hist) if c)
        worst = max(worst, over)
        if over > 0:
            differing.append((i + 1, f'{over:.4%} of pixels differ by more than 8/255 (max difference {mx})'))
    print(f'pages compared: {min(da.page_count, db.page_count)}; pages with any pixel difference above tolerance: {len(differing)}; largest share {worst:.4%}')
    for p, t in differing[:40]:
        print(f'  page {p}: {t}')


if __name__ == '__main__':
    main()
