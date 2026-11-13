"""Scratch: render an archive page (optionally a vertical band) to the scratch folder. Args: file page [y0frac y1frac] [dpi]"""
import sys, pymupdf
sys.path.insert(0, r'C:\Users\windo\sf-wsA\tools\data_policy')
import policy_lib as P
A = P.Archive()
f, pg = sys.argv[1], int(sys.argv[2])
y0, y1 = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (0.0, 1.0)
dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 0
m = A.member(f)
data = A.z.read(m)
out = r'C:\Users\windo\AppData\Local\Temp\claude\c--Users-windo-OneDrive-Desktop-Smart-formulator-project\3f66f328-3708-42fd-ad6b-a350bfb79529\scratchpad\wsA\r_' + f.replace('%', '_').rsplit('.', 1)[0] + f'_p{pg}.png'
if m.lower().endswith('.pdf'):
    doc = pymupdf.open(stream=data, filetype='pdf')
    p = doc[pg - 1]; r = p.rect
    if not dpi:
        dpi = max(40, min(110, int(1100 / (r.width / 72))))
    p.get_pixmap(dpi=dpi, clip=pymupdf.Rect(0, r.height * y0, r.width, r.height * y1)).save(out)
else:
    pix = pymupdf.Pixmap(data)
    doc = pymupdf.open(stream=data, filetype=m.rsplit('.', 1)[1])
    p = doc[0]; r = p.rect
    if not dpi:
        dpi = max(30, min(110, int(1100 / (r.width / 72))))
    p.get_pixmap(dpi=dpi, clip=pymupdf.Rect(0, r.height * y0, r.width, r.height * y1)).save(out)
print(out)
