"""Reading aid (read-only): print chosen numbered sections of an SDS from the new archive, with the pages they span.

  python sdssec.py FILE [sections, default 1,3,9]

A section runs from its heading ('SECTION 9', 'Section 9:', '9. PHYSICAL ...', '9 PHYSICAL ...') to the next section heading.
It prints the page range of each section so the reading scope can be stated exactly. Headings it cannot find are reported as
'NOT FOUND' (then read the pages directly). It decides nothing.
Known limitation (nineteenth pass): on layouts whose page header prints 'Page : 1 / 9' the number pattern can match the
header and give wrong boundaries (seen on the Luberef SDSs); check the printed page range and read the pages directly when it is
implausible.
"""
import re, sys, zipfile
import pymupdf

ZIP = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip'


def head(n):
    return re.compile(r'(?:SECTION|Section)\s*%d\s*[:.]?\s|(?<![\d.,/])\b%d\s?\.?\s+(?=(?:[A-Z][A-Za-z/&,\- ]{3,}))' % (n, n))


def main():
    f = sys.argv[1]
    secs = [int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else '1,3,9').split(',')]
    z = zipfile.ZipFile(ZIP)
    names = {n.rsplit('/', 1)[-1]: n for n in z.namelist()}
    d = pymupdf.open(stream=z.read(names[f]), filetype='pdf')
    pages = [re.sub(r'\s+', ' ', p.get_text()) for p in d]
    text, starts = '', []
    for i, t in enumerate(pages):
        starts.append(len(text))
        text += t + ' '

    def page_of(pos):
        return max(i for i, s in enumerate(starts) if s <= pos) + 1

    def find(n, after=0):
        m = head(n).search(text, after)
        return m.start() if m else None

    print(f'=== {f}: {len(d)} pages')
    for n in secs:
        a = find(n)
        if a is None:
            print(f'--- section {n}: NOT FOUND')
            continue
        b = find(n + 1, a + 5)
        b = b if b is not None else len(text)
        print(f'--- section {n} (pp.{page_of(a)}-{page_of(b)}):', text[a:b].strip())


if __name__ == '__main__':
    main()
