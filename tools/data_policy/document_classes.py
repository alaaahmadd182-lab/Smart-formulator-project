"""Classify every document page that Products_json cites, by purpose and content (not by file name).

Classes used by the source-selection policy (Rule 1):
  SDS        safety data sheet (also MSDS); identified by a "Safety Data Sheet" / "Material Safety Data Sheet"
             heading. A page inside a file that opens as an SDS is SDS unless the page carries its own technical
             heading (combined TDS + SDS files, e.g. DL2-10204.pdf: p.1 TDS, p.3-8 SDS).
  TECHNICAL  every supplier technical document that states product properties for use, subdivided by purpose:
               tds            technical / product data sheet (PDS), typical properties or typical inspections
               specification  sales specification with limits (min / max); a technical document, but its values
                              are limits, so value_kind must be kept
               bulletin       technical bulletin or product brochure with performance claims / typical data
               catalog        multi-product catalog or brochure table
  COA        certificate of analysis (one batch)
  EXTERNAL   a URL (source_registry.json); classified separately by its registry entry
  UNKNOWN    no basis to classify; such a page is never treated as TDS or SDS

For the TDS-first rule, TECHNICAL documents count as "TDS"; the subclass and the value's value_kind stay recorded so
that a specification limit is never compared with a typical value as if they were the same kind.

Pages without a text layer and image files are classified from a reviewed manual table (MANUAL), each entry
recording how the page was read.

Usage: python tools/data_policy/document_classes.py [--out reports/data_policy/document_classes.csv]
Writes only the --out file. Exit code 0; 1 if a cited archive page has no class.
"""
import argparse, collections, csv, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P

SDS_HEAD = re.compile(r'safety\s+data\s+sheet|material\s+safety\s+data|fiche\s+de\s+donn[ée]es|sicherheitsdatenblatt', re.I)
SDS_SECTION = re.compile(r'hazards?\s+identification|first[- ]aid\s+measures|composition\s*/\s*information\s+on\s+ingredients|'
                         r'physical\s+and\s+chemical\s+properties|fire[- ]?fighting\s+measures|exposure\s+controls|'
                         r'section\s*1\b|identification\s+of\s+the\s+(substance|product)', re.I)
TECH_HEAD = re.compile(r'technical\s+data\s+sheet|product\s+data\s+sheet|typical\s+(properties|characteristics|data|inspections|analysis|values?)|'
                       r'product\s+information|data\s+sheet', re.I)
SPEC = re.compile(r'specification', re.I)
LIMIT_COLS = re.compile(r'\b(min\.?|max\.?|minimum|maximum|limits?)\b', re.I)
TYPICAL = re.compile(r'typical', re.I)
BULLETIN = re.compile(r'bulletin|key\s+performance\s+benefits|performance\s+(benefits|comparison)|recommended\s+dosage|'
                      r'E\s?N\s?G\s?I\s?N\s?E\s+O\s?I\s?L\s?S|additives?\s+package|technical\s+judg(e)?ment', re.I)
CATALOG = re.compile(r'catalog|brochure|series|product\s+range|premium\s+series', re.I)
COA = re.compile(r'certificate\s+of\s+analysis', re.I)

# Pages without a text layer and image files, read on renders on 2026-11-10 (or in the v5 review where stated).
MANUAL = {
    'DL2-10217.pdf': ('TECHNICAL', 'tds', 'Infineum D3375 sheet: "Typical Inspections" table (render, v5 review)'),
    'DL2-10218.pdf': ('TECHNICAL', 'tds', 'Infineum D3384 sheet: Description, Performance, Typical Inspections (render)'),
    'DL2-10220.pdf': ('TECHNICAL', 'tds', 'Infineum D3453 sheet: Description, Performance, "Typical Inspections" (render)'),
    'DL2-10962.pdf': ('TECHNICAL', 'tds', 'Neste "Technical Data Sheet BASE OILS NEXBASE", edition 8 (render)'),
    'DL2-11173.pdf': ('TECHNICAL', 'catalog', 'S-OIL "PREMIUM SERIES" catalog page with a multi-grade table (render)'),
    'DL2-11190.pdf': ('TECHNICAL', 'tds', 'ExxonMobil SpectraSyn Ultra 1000 product sheet: "Typical Value" table (render)'),
    'DL2-11197.pdf': ('TECHNICAL', 'tds', 'ExxonMobil SpectraSyn Ultra 300 product sheet: "Typical Value" table (render)'),
    'DL2-11773.pdf': ('TECHNICAL', 'catalog', 'aramcoPRIMA brochure, printed pp. 8-9, Group II "Typical" table (render, v5 review)'),
    'DL2-12108.jpeg': ('TECHNICAL', 'specification', 'FPCC "Specification of FPCC API GII Base Oil": Specification and Typical (2017 AUG) columns (image)'),
    'DL2-12370.pdf': ('TECHNICAL', 'tds', 'Nynas T 110 product sheet (render)'),
    'DL2-12371.pdf': ('TECHNICAL', 'tds', 'Nynas T 22 product sheet (render)'),
    'DL2-12420.jpg': ('TECHNICAL', 'specification', 'scanned ADNOC product specification ADbase 4 cSt (image; record doc_type)'),
    'DL2-12421.jpg': ('TECHNICAL', 'specification', 'scanned ADNOC product specification ADbase 6 cSt (image; record doc_type)'),
    'DL2-12468.jpg': ('TECHNICAL', 'specification', 'scanned ADNOC product specification ADbase 8 cSt (image; record doc_type)'),
    'DL2-12475.pdf': ('TECHNICAL', 'tds', 'PETRONAS "ETRO 4 & ETRO 6 Group III base oil - Technical Data Sheet" (render)'),
    'DL2-12493.pdf': ('SDS', 'sds', 'Chevron "Material Safety Data Sheet" (render of p.1 and p.4)'),
    'DL2-12494.pdf': ('SDS', 'sds', 'Chevron "Material Safety Data Sheet" (render of p.1)'),
    'DL2-12888.jfif': ('TECHNICAL', 'specification', 'Bapco BAPBASE 6 product specification (image; record doc_type)'),
    'DL2-13092.jpg': ('TECHNICAL', 'specification', 'Bapco BAPBASE 4 product specification (image; record doc_type)'),
    'DL2-13093.jpg': ('TECHNICAL', 'specification', 'Bapco BAPBASE 8 product specification (image; record doc_type)'),
}


# SDS-specific section topics. Generic topics that technical sheets also print as boilerplate (handling and storage,
# transport information, regulatory information) are deliberately excluded.
SDS_TOPICS = [r'stability\s+and\s+reactivity', r'hazardous\s+decomposition', r'first[- ]aid', r'eye\s+contact', r'skin\s+contact',
              r'fire[- ]?fighting|fire\s*&\s*explosion|extinguishing\s+media', r'toxicological\s+information',
              r'ecological\s+information', r'disposal\s+considerations', r'hazards?\s+identification', r'accidental\s+release',
              r'exposure\s+controls|personal\s+protection']
TECH_DATA_HEAD = re.compile(r'technical\s+data|typical\s+(properties|inspections|characteristics)', re.I)


def sds_heading(t):
    """True when the page is part of a safety data sheet: "Safety Data Sheet" is a heading (near the top of the page
    or on a short line of its own; a sentence such as "see the Material Safety Data Sheet (MSDS)" is not), or the page
    covers at least two distinct SDS section topics (for SDS pages whose text layer is out of order)."""
    if SDS_HEAD.search(t[:300]):
        return True
    # a heading line is the phrase on its own (optionally with a product name), not a sentence wrapped onto a line
    # ("...see the related Material / Safety Data Sheet." ends with a full stop and is not a heading)
    for line in t.splitlines():
        s = line.strip()
        if SDS_HEAD.search(s) and len(s) <= 60 and not s.endswith('.') and not re.search(r'\b(see|refer|the|per)\b', s, re.I):
            return True
    return sum(1 for p in SDS_TOPICS if re.search(p, t, re.I)) >= 2 and not TECH_DATA_HEAD.search(t)


def classify_page(pages, i):
    """(class, subclass, basis) for page index i (0-based) of a document with text pages."""
    t = pages[i]
    first = pages[0]
    file_is_sds = sds_heading(first) and bool(SDS_SECTION.search(' '.join(pages[:3])) or
                                              re.search(r'REACH|Regulation\s*\(E[CU]\)|revision\s+date|issue\s+date', first, re.I))
    page_sds_head = sds_heading(t)
    page_tech_head = bool(TECH_HEAD.search(t)) and not page_sds_head
    if COA.search(t):
        return 'COA', 'coa', 'heading "Certificate of Analysis"'
    if page_sds_head or (file_is_sds and not page_tech_head):
        why = ('"Safety Data Sheet" heading or SDS section structure on the page' if page_sds_head
               else 'page of a file that opens as a Safety Data Sheet')
        return 'SDS', 'sds', why
    if SPEC.search(t) and LIMIT_COLS.search(t) and not TYPICAL.search(t):
        return 'TECHNICAL', 'specification', 'specification with min/max limits, no typical column'
    if BULLETIN.search(t) and not re.search(r'typical\s+(properties|inspections)', t, re.I):
        return 'TECHNICAL', 'bulletin', 'technical bulletin (performance claims / dosage)'
    if CATALOG.search(t) and len(re.findall(r'\n', t)) > 40 and not re.search(r'data\s+sheet', t, re.I):
        return 'TECHNICAL', 'catalog', 'catalog / brochure table'
    if TECH_HEAD.search(t) or TYPICAL.search(t):
        return 'TECHNICAL', 'tds', 'technical / product data sheet (typical properties)'
    if re.search(r'\b(kinematic\s+viscosity|viscosity\s+index|flash\s+point|pour\s+point|density)\b', t, re.I):
        return 'TECHNICAL', 'tds', 'property table without a heading (no safety-sheet structure)'
    # a page without its own signal takes the class of the document it belongs to
    for j, other in enumerate(pages):
        if j != i and other.strip() and not sds_heading(other):
            c, s, _ = _own(other)
            if c == 'TECHNICAL':
                return c, s, f'continuation page of a technical document (p.{j + 1}: {s})'
    return 'UNKNOWN', '', 'no heading or property table recognised'


def _own(t):
    """Class of a single page from its own text only (used for the page a continuation page inherits from)."""
    if sds_heading(t):
        return 'SDS', 'sds', ''
    if SPEC.search(t) and LIMIT_COLS.search(t) and not TYPICAL.search(t):
        return 'TECHNICAL', 'specification', ''
    if BULLETIN.search(t) and not re.search(r'typical\s+(properties|inspections)', t, re.I):
        return 'TECHNICAL', 'bulletin', ''
    if TECH_HEAD.search(t) or TYPICAL.search(t):
        return 'TECHNICAL', 'tds', ''
    return 'UNKNOWN', '', ''


def cited_pages(prods):
    """{(file, page): count} of every page cited anywhere in the records (values, alternates, conflicts, source_documents)."""
    out = collections.Counter()
    for p in prods.values():
        for d in p['files'].values():
            def rec(n):
                if isinstance(n, dict):
                    f = n.get('file')
                    if isinstance(f, str) and f:
                        pg = n.get('page')
                        pgs = n.get('pages') if isinstance(n.get('pages'), list) else [pg]
                        for x in pgs:
                            out[(f, x if isinstance(x, int) else None)] += 1
                    for v in n.values():
                        rec(v)
                elif isinstance(n, list):
                    for v in n:
                        rec(v)
            rec(d)
    return out


def classify_all(prods=None, ar=None):
    prods = prods or P.load_products()
    ar = ar or P.Archive()
    rows = {}
    for (f, pg), n in sorted(cited_pages(prods).items(), key=lambda x: (str(x[0][0]), x[0][1] or 0)):
        if str(f).lower().startswith(('http://', 'https://')):
            rows[(f, pg)] = ('EXTERNAL', '', 'URL; see source_registry.json')
            continue
        pages = ar.pages(f)
        base = os.path.basename(str(f)).replace('%20', ' ')
        if pages is None:
            rows[(f, pg)] = ('UNKNOWN', '', 'not in the archive')
        elif base in MANUAL or not pages or not any(x.strip() for x in pages):
            rows[(f, pg)] = MANUAL.get(base, ('UNKNOWN', '', 'image or no text layer, not reviewed'))
        elif pg is None:
            sub = [classify_page(pages, i) for i in range(len(pages))]
            cls = {s[0] for s in sub}
            rows[(f, pg)] = (sub[0] if len(cls) == 1 else ('MIXED', '/'.join(sorted(cls)), 'pages differ; cite a page'))
        elif 1 <= pg <= len(pages) and pages[pg - 1].strip():
            rows[(f, pg)] = classify_page(pages, pg - 1)
        else:
            rows[(f, pg)] = ('UNKNOWN', '', 'cited page out of range or without text')
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(P.REPORTS, 'data_policy', 'document_classes.csv'))
    a = ap.parse_args()
    rows = classify_all()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['file', 'page', 'class', 'subclass', 'basis'])
        for (f, pg), (c, s, why) in rows.items():
            w.writerow([f, '' if pg is None else pg, c, s, why])
    C = collections.Counter(v[0] for v in rows.values())
    print('cited (file, page) pairs:', len(rows), dict(C))
    print('subclasses:', dict(collections.Counter((v[0], v[1]) for v in rows.values())))
    unknown = [k for k, v in rows.items() if v[0] == 'UNKNOWN']
    for k in unknown[:30]:
        print('UNKNOWN', k, rows[k][2])
    return 1 if unknown else 0


if __name__ == '__main__':
    sys.exit(main())
