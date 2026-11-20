"""Field-level mapping, S16 KUSA (Kusa Chemicals Pvt. Ltd.).
13 eligible: 13 additive_component (antioxidants, VMs, PPDs).

Doc format: numbered PARAMETERS / SPECIFICATIONS list (single format, all 13 products).
  PRODUCT: <NAME>
  No.  PARAMETERS                      SPECIFICATIONS
  1. APPEARANCE                         Clear Viscous Liquid
  3. VISCOSITY@100 C (ASTM D445)       850-1350 CST    <- sometimes next line
  5. FLASH POINT (COC) C (ASTM D3278)  150 min          <- or same line

Values: ranges (850-1350), nnn min (>=150), nnn max, typical (0.93 Typical),
       typical-with-range (0.91 Typ. (0.88-0.94 range)).
Parens content stripped before extraction; Typical/Typ. trimmed by _extract_num.

Chemical family detected from product name prefix:
  KUNOX -> antioxidant; KUSACRYL/VICOL -> viscosity modifier; KUSAPOUR -> PPD.
Treat rate from "Recommended dosage" or "Recommended Dosage" text.

Writes field_evidence/s16_kusa.csv.
"""
import csv, gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fm_common import COLS, field_units, write_rows, PKG

ROOT  = os.path.dirname(PKG)
CACHE = os.path.join(PKG, '_cache', 'ocr')
INV   = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')

links_raw  = list(csv.DictReader(open(os.path.join(PKG, 'tables', 'document_product_links.csv'), encoding='utf-8')))
docs_inv   = {r['sha256']: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}
stages_raw = list(csv.DictReader(open(os.path.join(PKG, 'tables', 'product_stages.csv'), encoding='utf-8')))

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('KUSA:')
            and r['stage2_identity']       == 'verified'
            and r['stage3_class_template'] == 'established'
            and r['stage5_field_mapping']  == 'not started'}

prod_docs = {}
for lk in links_raw:
    pk = lk['product_key']
    if pk in ELIGIBLE:
        prod_docs.setdefault(pk, []).append(lk)

REVIEW = 'TDS text read in full 2026-11-19; extraction from cached text-layer'

def get_text(sha256):
    path = os.path.join(CACHE, sha256 + '.json.gz')
    if not os.path.exists(path):
        return ''
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        d = json.load(f)
    return '\n'.join(p.get('text', '') or '' for p in d.get('pages', []))

DOC_RANK = {'TDS/PDS': 0, 'TDS': 0, 'SDS': 1, 'brochure': 2, 'other': 2, 'unresolved': 3}

def select_best_doc(doc_links):
    scored = []
    for lk in doc_links:
        sha = lk['sha256']
        d   = docs_inv.get(sha, {})
        t   = get_text(sha)
        rank = DOC_RANK.get(d.get('document_type', ''), 4)
        scored.append((rank, -len(t), lk, t))
    if not scored:
        return None, ''
    scored.sort(key=lambda x: (x[0], x[1]))
    return scored[0][2], scored[0][3]

def get_rev_date(sha256):
    d = docs_inv.get(sha256, {})
    dates = d.get('printed_dates', '')
    return str(dates).split(',')[0].strip() if dates else ''

# ── Numeric extraction ────────────────────────────────────────────────
def _extract_num_minmax(s):
    s = s.strip()
    s = re.sub(r'\([^)]*\)', '', s).strip()
    mm = re.match(r'(-?\d+(?:\.\d+)?)\s*(min|max)\b', s, re.I)
    if mm:
        v, suffix = mm.group(1), mm.group(2).lower()
        return f'{"≥" if suffix == "min" else "≤"}{v}'
    # Remove trailing Typical/Typ before number extraction
    s2 = re.sub(r'\s+[Tt]yp(?:ical|\.?).*$', '', s).strip()
    m = re.match(r'([<>≥≤]?=?\s*-?\d[\d.,]*)(?:\s*[-–]\s*-?\d[\d.,]*)?', s2)
    if m:
        return m.group(0).strip()
    return ''

def _wrap(pat):
    return r'(?:' + pat + r')'

def find_prop(block, label_pat):
    m = re.search(_wrap(label_pat), block, re.I)
    if not m:
        return None
    label_line = m.group(0).strip()
    rest_of_line = block[m.end():].split('\n')[0]
    rest_clean = re.sub(r'^[\t:\s]+', '', rest_of_line).strip()
    if rest_clean:
        v = _extract_num_minmax(rest_clean)
        if v:
            return v, label_line
    after = block[m.end():]
    for ln in after.split('\n')[1:16]:
        s = ln.strip().rstrip('\t').strip()
        if not s:
            continue
        if re.match(r'^\(', s):
            continue
        # Skip method/standard lines
        if re.match(r'^(?:ASTM|GB|SH|Q/|DIN|IP|ISO|EN|CEC|SAE)\s', s, re.I):
            continue
        if re.match(r'^[Nn]ot\s+(?:available|established|applicable)', s):
            continue
        v = _extract_num_minmax(s)
        if v:
            return v, label_line
        if len(s) > 25 and re.match(r'^[A-Za-z]', s) and not re.search(r'\d', s):
            break
    return None

def _parse(s):
    s = s.strip()
    s = re.sub(r'\([^)]*\)', '', s).strip()
    um = re.search(r'\s+([a-zA-Z°%][a-zA-Z/°%\s2*]*)\s*$', s)
    unit_v = um.group(1).strip() if um else ''
    if um:
        s = s[:um.start()].strip()
    mr = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if mr:
        return '', '', mr.group(1).replace(',', '.'), mr.group(2).replace(',', '.'), 'range', unit_v
    mb = re.fullmatch(r'([<>≥≤]=?)\s*(-?\d+(?:[.,]\d+)?)', s)
    if mb:
        sym, v = mb.group(1), mb.group(2).replace(',', '.')
        q = {'<': '≤', '>': '≥', '>=': '≥', '<=': '≤', '≥': '≥', '≤': '≤'}.get(sym, sym)
        return '', q, v if q == '≥' else '', v if q == '≤' else '', 'bound', unit_v
    mn = re.fullmatch(r'-?\d+(?:[.,]\d+)?', s)
    if mn:
        return s.replace(',', '.'), '', '', '', 'typical', unit_v
    return '', '', '', '', 'text', unit_v

# ── Text-field extractors ─────────────────────────────────────────────
def extract_chem_family(pk, text):
    pk_up = pk.upper()
    if 'KUNOX' in pk_up:
        return 'antioxidant'
    if 'KUSACRYL' in pk_up or 'VICOL' in pk_up:
        return 'viscosity modifier'
    if 'KUSAPOUR' in pk_up:
        return 'pour point depressant'
    # Fallback from text
    for pat, label in [
        (r'[Vv]iscosity\s+[Mm]odifier', 'viscosity modifier'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep', 'pour point depressant'),
        (r'[Aa]ntioxidant', 'antioxidant'),
    ]:
        if re.search(pat, text[:2000], re.I):
            return label
    return ''

def extract_treat_rate(text):
    for pat in [
        r'[Rr]ecommended\s+[Dd]osage\s+(?:is\s+)?([\d.]+)\s*[-–]\s*([\d.]+)\s*wt%',
        r'[Rr]ecommended\s+[Dd]osage\s+(?:is\s+)?([\d.]+)\s*[-–]\s*([\d.]+)\s*%',
        r'[Rr]ecommended\s+[Dd]osage\s+([\d.]+)\s*[-–]\s*([\d.]+)\s*%',
        r'[Rr]ecommended\s+[Dd]osage\s+is\s+([\d.]+)\s*wt%\s+to\s+([\d.]+)',
        r'[Dd]osage\s+(?:is\s+)?([\d.]+)\s*[-–]\s*([\d.]+)\s*(?:wt)?%',
    ]:
        m = re.search(pat, text[:3000], re.I)
        if m:
            groups = [g for g in m.groups() if g]
            vals = []
            for g in groups:
                try:
                    vals.append(float(g.replace(',', '.')))
                except Exception:
                    pass
            if vals:
                vmin, vmax = min(vals), max(vals)
                if 0.05 <= vmin <= 40:
                    if len(vals) >= 2 and vmax != vmin:
                        return f'{vmin}-{vmax}%'
                    return f'{vmin}%'
    return ''

# ── Row builders ──────────────────────────────────────────────────────
def _missing(pk, tmpl, field, src_file, sha, rev):
    return {'product_key': pk, 'template': tmpl, 'field': field,
            'entry': 'primary', 'value': '', 'qualifier': '', 'min': '', 'max': '',
            'value_kind': '', 'printed_text': '', 'unit': '',
            'test_temperature_c': '', 'method': '', 'conditions': '',
            'status': 'Missing', 'value_class': 'numeric',
            'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '1',
            'revision_date': rev, 'notes': '', 'review': REVIEW}

def _reported(pk, tmpl, field, printed, unit, qual, lo, hi, vk, temp,
              src_file, sha, rev, notes=''):
    val = lo if (vk == 'bound' and qual == '≥') else hi if (vk == 'bound' and qual == '≤') else printed
    return {'product_key': pk, 'template': tmpl, 'field': field,
            'entry': 'primary', 'value': val, 'qualifier': qual, 'min': lo, 'max': hi,
            'value_kind': vk, 'printed_text': printed, 'unit': unit,
            'test_temperature_c': temp, 'method': '', 'conditions': '',
            'status': 'Reported', 'value_class': 'numeric',
            'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '1',
            'revision_date': rev, 'notes': notes, 'review': REVIEW}

def _text_field(pk, tmpl, field, text_val, src_file, sha, rev):
    return {'product_key': pk, 'template': tmpl, 'field': field,
            'entry': 'primary', 'value': '', 'qualifier': '', 'min': '', 'max': '',
            'value_kind': 'text', 'printed_text': text_val, 'unit': '',
            'test_temperature_c': '', 'method': '', 'conditions': '',
            'status': 'Reported', 'value_class': 'text',
            'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '1',
            'revision_date': rev, 'notes': '', 'review': REVIEW}

COMP_GEN_FIELDS = [
    'function.primary', 'function.secondary', 'chemical_family',
    'active_content', 'carrier.identity', 'carrier.share_wt_pct',
    'treat_rate', 'compatibility_restrictions',
    'function_specific_markers.tbn', 'function_specific_markers.ca',
    'function_specific_markers.mg', 'function_specific_markers.p',
    'function_specific_markers.zn', 'function_specific_markers.mo',
]

def component_rows(pk, text, sha, fname, rev):
    rows = []
    chem = extract_chem_family(pk, text)
    tr   = extract_treat_rate(text)

    for f in COMP_GEN_FIELDS:
        if f == 'chemical_family':
            rows.append(_text_field(pk, 'component_general', f, chem, fname, sha, rev)
                        if chem else _missing(pk, 'component_general', f, fname, sha, rev))
        elif f == 'treat_rate':
            if tr:
                v_num = tr.replace('%', '').strip().split('-')[0].strip()
                rows.append(_reported(pk, 'component_general', f, tr, '%', '', v_num, '', 'typical', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, 'component_general', f, fname, sha, rev))
        else:
            rows.append(_missing(pk, 'component_general', f, fname, sha, rev))

    return rows

def main():
    rows   = []
    n_done = 0

    for pk in sorted(ELIGIBLE):
        doc_links = prod_docs.get(pk, [])

        if not doc_links:
            for f in COMP_GEN_FIELDS:
                rows.append(_missing(pk, 'component_general', f, '', '', ''))
            n_done += 1
            continue

        link, text = select_best_doc(doc_links)
        if link is None:
            link_fallback = doc_links[0]
            sha   = link_fallback['sha256']
            fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
            rev   = get_rev_date(sha)
            for f in COMP_GEN_FIELDS:
                rows.append(_missing(pk, 'component_general', f, fname, sha, rev))
            n_done += 1
            continue

        sha   = link['sha256']
        fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
        rev   = get_rev_date(sha)

        rows.extend(component_rows(pk, text, sha, fname, rev))
        n_done += 1

    write_rows('s16_kusa.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
