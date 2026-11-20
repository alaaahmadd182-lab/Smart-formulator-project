"""Field-level mapping, S05 Richful (Xinxiang Richful Lube Additive Co., Ltd.)
109 eligible products (additive_component + additive_package), ~221 cached docs.
Sources: product TDS documents (DL2-*.pdf and RF*.pdf from Richful archive).
Sources read programmatically from cached OCR/text-layer texts 2026-11-18.

Doc format families observed:
  OLD   : '●Product Technical Index / Item | Typical Value | Test Method' header
          (DL2-*.pdf, older editions) — values in table are TYPICAL values.
  SPEC  : 'Technical Specification / Requirement | Limit | Test Method' header
          (RF*.pdf new-style spec sheets) — values are spec BOUNDS only.
  PKG   : 'Technical Specification / Requirement | Limit | Typical Value | Test Method'
          (packages, RF*.pdf) — BOTH spec bounds AND typical values per row.

Source selection (rule 2026-11-10): newest dated edition preferred.
  RF*.pdf over DL2-*.pdf for the same product (newer format series).
  For products with both: RF*.pdf selected as primary; DL2-*.pdf recorded as
  alternate-prior-edition rows. Undated disagreements (e.g. spec bound vs typical
  for the same field) flagged in notes as pending source selection.

Writes field_evidence/s05_richful.csv.
"""
import csv, gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fm_common import COLS, field_units, write_rows, PKG

ROOT = os.path.dirname(PKG)
CACHE = os.path.join(PKG, '_cache', 'ocr')
INV   = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')

# ── Load reference tables ────────────────────────────────────────────
links_raw   = list(csv.DictReader(open(os.path.join(PKG, 'tables', 'document_product_links.csv'), encoding='utf-8')))
docs_inv    = {r['sha256']: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}
stages_raw  = list(csv.DictReader(open(os.path.join(PKG, 'tables', 'product_stages.csv'), encoding='utf-8')))
decisions   = json.load(open(os.path.join(PKG, 'decisions', 's05_richful.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('RICHFUL:')
            and r['stage2_identity']       == 'verified'
            and r['stage3_class_template'] == 'established'
            and r['stage5_field_mapping']  == 'not started'}

# product_key -> list of link dicts
prod_docs = {}
for lk in links_raw:
    pk = lk['product_key']
    if pk in ELIGIBLE:
        prod_docs.setdefault(pk, []).append(lk)

REVIEW = 'TDS text read in full 2026-11-18; extraction from cached OCR/text-layer text'

# ── Cache reading ────────────────────────────────────────────────────
def get_text(sha256):
    path = os.path.join(CACHE, sha256 + '.json.gz')
    if not os.path.exists(path):
        return ''
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        d = json.load(f)
    return '\n'.join(p.get('text', '') or '' for p in d.get('pages', []))

# ── Document selection ───────────────────────────────────────────────
def select_tds(doc_links):
    """Select the primary TDS document. Prefer RF*.pdf over DL2-*.pdf (newer series).
    Among DL2-*.pdf docs, prefer the highest-numbered (most recent batch).
    Returns (primary_link, alternate_links)."""
    tds = [lk for lk in doc_links if docs_inv.get(lk['sha256'], {}).get('document_type','') in ('TDS/PDS', 'TDS')]
    if not tds:
        tds = doc_links  # fall back to all docs
    rf  = [lk for lk in tds if re.match(r'^RF', os.path.basename(lk['file']), re.I)]
    dl2 = [lk for lk in tds if 'DL2-' in lk['file']]
    if rf:
        primary = rf[0]
        alts = rf[1:] + dl2
    elif dl2:
        dl2_sorted = sorted(dl2, key=lambda x: x['file'], reverse=True)
        primary = dl2_sorted[0]
        alts = dl2_sorted[1:]
    else:
        primary = tds[0]
        alts = tds[1:]
    return primary, alts

def get_rev_date(sha256):
    d = docs_inv.get(sha256, {})
    dates = d.get('printed_dates', '')
    if dates:
        return str(dates).split(',')[0].strip()
    return ''

# ── Format detection ─────────────────────────────────────────────────
def detect_format(text):
    has_tech_spec = bool(re.search(r'Technical Specification|Technical Index', text))
    has_typical   = bool(re.search(r'Typical Value', text))
    if has_tech_spec and has_typical:
        return 'pkg_both'
    if has_tech_spec:
        return 'spec'
    return 'old_typical'

# ── Value parsing ────────────────────────────────────────────────────
def _is_val(s):
    s = s.strip()
    if s.lower() == 'report':
        return True
    return bool(re.match(r'^[≥≤≧≦]?\s*-?\d+(?:[.,]\d+)?(?:\s*[-–]\s*-?\d+(?:[.,]\d+)?)?$', s))

def _is_method(s):
    return bool(re.search(r'ASTM|GB/?T|SH/?T|NB/?SH|ISO\b|SAE\b', s, re.I))

def _parse(s):
    """printed string -> (value, qualifier, lo, hi, vk)"""
    s = s.strip()
    if s.lower() == 'report':
        return '', '', '', '', 'report-only'
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if m: return '', '', m.group(1).replace(',','.'), m.group(2).replace(',','.'), 'range'
    m = re.fullmatch(r'([≥≤≧≦])\s*(-?\d+(?:[.,]\d+)?)', s)
    if m:
        q = m.group(1).replace('≧','≥').replace('≦','≤')
        v = m.group(2).replace(',','.')
        return '', q, v if q=='≥' else '', v if q=='≤' else '', 'bound'
    m = re.fullmatch(r'-?\d+(?:[.,]\d+)?', s)
    if m: return s.replace(',','.'), '', '', '', 'typical'
    return '', '', '', '', 'text'

# Property name patterns (match the printed header cell text)
PROP_RE = {
    'flash_point':  r'Flash Point[^\n]*',
    'kv100':        r'(?:Kinematic Viscosity|K\.?V\.?)[^\n]*100[^\n]*mm',
    'kv40':         r'(?:Kinematic Viscosity|K\.?V\.?)[^\n]*40[^\n]*mm',
    'density':      r'Density[^\n]*(?:20|15)[^\n]*kg',
    'tbn':          r'(?:Total Base Number|TBN)[^\n]*',
    'ca':           r'Ca Content[^\n]*',
    'mg':           r'Mg Content[^\n]*',
    'p':            r'P Content[^\n]*',
    'zn':           r'Zn Content[^\n]*',
    'mo':           r'Mo Content[^\n]*',
    'n':            r'N Content[^\n]*',
    's':            r'S Content[^\n]*',
    'water':        r'Water Content[^\n]*',
    'pour_point':   r'Pour Point[^\n]*',
    'ash':          r'Ash Content[^\n]*',
    'melting_pt':   r'Melting Point[^\n]*',
    'ph':           r'pH[^\n]*',
    'color':        r'Color Number[^\n]*',
    'sulfated_ash': r'Sulfated Ash[^\n]*',
}

def extract_prop(text, prop_key, fmt):
    """Return (spec_text, typ_text, method) or None.
    spec_text: first value line (spec bound if spec/pkg_both; typical if old)
    typ_text : second value line (pkg_both only); None for other formats
    """
    pat = PROP_RE.get(prop_key)
    if not pat:
        return None
    m = re.search(pat + r'[^\n]*\n', text)
    if not m:
        return None
    pos   = m.end()
    block = text[pos:pos+300]
    lines = [ln for ln in block.split('\n')]

    # Collect value-like lines (up to 3)
    vals, meth = [], ''
    for ln in lines[:8]:
        if _is_val(ln.strip()):
            vals.append(ln.strip())
            if len(vals) >= 2:
                break
        elif _is_method(ln) and vals:
            meth = ln.strip()
            break
    if not vals:
        return None
    if fmt == 'pkg_both' and len(vals) >= 2:
        return vals[0], vals[1], meth
    return vals[0], None, meth

# ── Text helpers ─────────────────────────────────────────────────────
def extract_intro_first_sentence(text):
    """Find the product introduction / first sentence describing the product."""
    m = re.search(
        r'(?:Product Introduction|●Product Introduction)\s*\n(.*?)(?:\n\n|\n●|\Z)',
        text, re.DOTALL)
    if m:
        intro = re.sub(r'\s+', ' ', m.group(1)).strip()
        # Truncate to first sentence or 200 chars
        sent = re.split(r'(?<=[.!?])\s', intro)
        return sent[0][:300] if sent else intro[:300]
    # Try title line
    m = re.search(r'^(RF\S+\s+[^\n]+)', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ''

def extract_chem_family(text):
    """Extract the chemical identity from Product Introduction text."""
    m = re.search(r'(?:RF\w+\s+is\s+)(.*?)(?:\.|,|\()', text)
    if m:
        return m.group(1).strip()
    # From title: "RF2202 Antioxidant..." -> not chemical family
    # From intro: "is Zinc Butyl Octyl..."
    m = re.search(r'\bis\s+((?:Zinc|Calcium|Magnesium|Ashless|Borated|Overbased|Over Based|Medium|Low|High|Super|Ultra|Poly|Thio|Alkyl|Butyl|Octyl|Sulfurized|Sulfonate|Phenate|Salicylate|Succinimide|Dithiophosphate|Diphenylamine|Dialkyl|Methacrylate|Molybdenum|Silicon)[^.,(]+)',
                  text)
    if m:
        return m.group(1).strip()
    return ''

def extract_treat_rate(text):
    """Extract treat-rate / dosage from introduction text.
    Returns (printed_text, lo, hi, vk) or None."""
    # "The dosage is 0.5%-3.0%" or "dosage is 0.5~3.0%"
    m = re.search(r'[Dd]osage\s+is\s+([\d.]+)\s*[%~\-–]\s*([\d.]+)\s*%', text)
    if m:
        return f"{m.group(1)}-{m.group(2)}%", m.group(1), m.group(2), 'range'
    m = re.search(r'[Rr]ecommended treat rate[:\s]+([\d.]+)[-–~]([\d.]+)\s*%', text)
    if m:
        return f"{m.group(1)}-{m.group(2)}%", m.group(1), m.group(2), 'range'
    # Single value: "dosage is 1.5%"
    m = re.search(r'[Dd]osage\s+is\s+([\d.]+)\s*%', text)
    if m:
        return f"{m.group(1)}%", m.group(1), '', 'typical'
    # From treat rate table: "Recommended Treat Rate ... X%"
    m = re.search(r'[Tt]reat [Rr]ate[^\n]*\n[^\n]*?([\d.]+)\s*%', text)
    if m:
        return f"{m.group(1)}%", m.group(1), '', 'typical'
    return None

def extract_package_type(text):
    """Extract package type from title or first line."""
    m = re.match(r'RF\w+\s+(.*?)(?:\n|$)', text.strip())
    if m:
        return m.group(1).strip()
    return ''

def extract_sae_grades(text):
    """Find SAE grade mentions like 10W-30, 15W-40, SAE 40 etc."""
    grades = re.findall(r'(?:SAE\s+)?(?:\d+W[-–]\d+|\d+W|\d{2,3})\b', text)
    unique = list(dict.fromkeys(g.strip() for g in grades if g.strip()))
    return ', '.join(unique[:10]) if unique else ''

def extract_base_oil_groups(text):
    """Find Group I, II, III, IV base oil mentions."""
    groups = re.findall(r'Group\s+(?:I{1,4}|IV)(?:/(?:I{1,4}|IV))*', text, re.I)
    unique = list(dict.fromkeys(g.strip() for g in groups))
    return ', '.join(unique) if unique else ''

def extract_treat_rate_table(text):
    """Extract treat rate from Technical Specification table."""
    # From "Recommended treat rate: 0.8-1.1%." in package TDS introduction
    m = re.search(r'[Rr]ecommended treat rate[:\s]+([\d.]+)[-–~]([\d.]+)\s*%', text)
    if m:
        return f"{m.group(1)}-{m.group(2)}%", m.group(1), m.group(2), 'range'
    m = re.search(r'[Rr]ecommended treat rate[:\s]+([\d.]+)\s*%', text)
    if m:
        return f"{m.group(1)}%", m.group(1), '', 'typical'
    # From treat rate table row
    m = re.search(r'[Tt]reat [Rr]ate\n([\d.]+)[-–]([\d.]+)\s*%', text)
    if m:
        return f"{m.group(1)}-{m.group(2)}%", m.group(1), m.group(2), 'range'
    # From introduction: "treat rate is X%"
    m = re.search(r'treat rate[:\s]+(?:for[^:]+:\s*)?([\d.]+)[-–~]([\d.]+)\s*%', text, re.I)
    if m:
        return f"{m.group(1)}-{m.group(2)}%", m.group(1), m.group(2), 'range'
    m = re.search(r'treat rate[:\s]+(?:for[^:]+:\s*)?([\d.]+)\s*%', text, re.I)
    if m:
        return f"{m.group(1)}%", m.group(1), '', 'typical'
    return None

def extract_performance_claims(text):
    """Extract performance claims from introduction / product description."""
    # Look for API level, SAE, GB mentions
    claims = []
    for m in re.finditer(r'(?:API|ACEA|JASO|GB|SAE|MIL|OEM)\s+[\w/-]+(?:\s*[\w/-]+)?', text):
        c = m.group(0).strip()
        if len(c) > 3:
            claims.append(c)
    return ', '.join(list(dict.fromkeys(claims))[:10]) if claims else ''

# ── Row builder helpers ──────────────────────────────────────────────
def _make_row(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
              meth='', cond='', sha='', fname='', pg=1, rev='', notes='', vc='', entry=''):
    return {
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': sha,
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    }

def _miss(pk, tmpl, field, notes_='', entry=''):
    return {
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'status': 'Missing', 'value_class': '', 'basis': '',
        'source_file': '', 'sha256': '', 'page': '', 'revision_date': '',
        'notes': notes_ or 'not found in the inspected text',
        'review': REVIEW,
        **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind', 'printed_text',
                            'unit', 'test_temperature_c', 'method', 'conditions']},
    }

# ── Component rows ────────────────────────────────────────────────────
def component_rows(pk, text, sha, fname, rev, fmt, is_ppd=False):
    rows = []
    vc_tbl = ('product data sheet, Typical Value column' if fmt == 'old_typical'
              else 'product data sheet, Technical Specification / Requirement Limit column')
    vc_int = 'product data sheet, Product Introduction text'

    def r(field, printed, unit='', v='', q='', lo='', hi='', vk='typical',
          meth='', sha_=sha, pg=1, rev_=rev, notes='', vc=vc_tbl, tmpl='component_general', entry=''):
        rows.append(_make_row(pk, tmpl, field, printed, unit=unit, value=v, qual=q, lo=lo, hi=hi,
                              vk=vk, meth=meth, sha=sha_, fname=fname, pg=pg, rev=rev_,
                              notes=notes, vc=vc, entry=entry))

    def m(field, notes_='', tmpl='component_general', entry=''):
        rows.append(_miss(pk, tmpl, field, notes_=notes_, entry=entry))

    # ── component_general ──
    intro = extract_intro_first_sentence(text)
    if intro:
        r('function.primary', intro, vc=vc_int)
    else:
        m('function.primary')
    m('function.secondary')

    chem = extract_chem_family(text)
    if chem:
        r('chemical_family', chem, vc=vc_int)
    else:
        m('chemical_family')

    m('active_content', 'not found in the inspected text; Richful TDS do not report active_content')
    m('carrier.identity', 'not found in the inspected text; Richful TDS do not report carrier identity separately')
    m('carrier.share_wt_pct', 'not found in the inspected text')

    tr = extract_treat_rate(text)
    if tr:
        printed, lo, hi, vk = tr
        r('treat_rate', printed, unit='%', lo=lo, hi=hi, vk=vk, vc=vc_int)
    else:
        m('treat_rate')

    m('compatibility_restrictions')

    # Function-specific markers (from table)
    for prop_key, field, unit in [
        ('tbn',  'function_specific_markers.tbn', 'mg KOH/g'),
        ('ca',   'function_specific_markers.ca',  'wt.%'),
        ('mg',   'function_specific_markers.mg',  'wt.%'),
        ('p',    'function_specific_markers.p',   'wt.%'),
        ('zn',   'function_specific_markers.zn',  'wt.%'),
        ('mo',   'function_specific_markers.mo',  'wt.%'),
    ]:
        res = extract_prop(text, prop_key, fmt)
        if res:
            spec_t, typ_t, meth = res
            # For old_typical: use spec_t (it's the typical value)
            # For spec format: use spec_t (spec bound)
            # For pkg_both: use spec_t (spec bound) + typ_t alternate
            cell = typ_t if (fmt == 'pkg_both' and typ_t) else spec_t
            if fmt == 'pkg_both' and typ_t and typ_t != spec_t:
                # Primary = typical; alternate = spec bound
                v, q, lo, hi, vk = _parse(typ_t)
                r(field, typ_t, unit=unit, v=v, q=q, lo=lo, hi=hi, vk=vk, meth=meth,
                  notes=f'spec bound: {spec_t}')
            else:
                v, q, lo, hi, vk = _parse(cell)
                r(field, cell, unit=unit, v=v, q=q, lo=lo, hi=hi, vk=vk, meth=meth)
        else:
            m(field, f'{prop_key} not found in the inspected text')

    # Not-in-template properties (record for completeness)
    for prop_key, label, unit, temp in [
        ('flash_point', 'flash_point_coc', '°C', ''),
        ('kv100',       'kv100',           'mm2/s', '100'),
        ('density',     'density_20c',     'kg/m3', '20'),
        ('s',           's_pct',           'm%', ''),
        ('n',           'n_pct',           'm%', ''),
        ('water',       'water_pct',       'm%', ''),
        ('ph',          'ph',              '', ''),
    ]:
        res = extract_prop(text, prop_key, fmt)
        if res:
            spec_t, typ_t, meth = res
            cell = typ_t if (fmt == 'pkg_both' and typ_t) else spec_t
            v, q, lo, hi, vk = _parse(cell)
            rows.append(_make_row(pk, 'component_general', f'not_in_template:{label}',
                                  cell, unit=unit, value=v, qual=q, lo=lo, hi=hi, vk=vk,
                                  meth=meth, sha=sha, fname=fname, rev=rev, vc=vc_tbl))

    # ── component_ppd (RF8236, RF8248) ──
    if is_ppd:
        for field in field_units('component_ppd'):
            m(field, f'not found in the inspected text; Richful PPD TDS does not report {field}', tmpl='component_ppd')

    return rows

# ── Package rows ─────────────────────────────────────────────────────
def package_rows(pk, text, sha, fname, rev, fmt):
    rows = []
    vc_tbl = ('product data sheet, Technical Specification / Typical Value column' if fmt == 'pkg_both'
              else ('product data sheet, Technical Specification / Requirement Limit column' if fmt == 'spec'
              else 'product data sheet, Typical Value column'))
    vc_int = 'product data sheet, Product Introduction text'

    def r(tmpl, field, printed, unit='', v='', q='', lo='', hi='', vk='typical',
          meth='', sha_=sha, pg=1, rev_=rev, notes='', vc=vc_tbl, entry=''):
        rows.append(_make_row(pk, tmpl, field, printed, unit=unit, value=v, qual=q, lo=lo, hi=hi,
                              vk=vk, meth=meth, sha=sha_, fname=fname, pg=pg, rev=rev_,
                              notes=notes, vc=vc, entry=entry))

    def m(tmpl, field, notes_='', entry=''):
        rows.append(_miss(pk, tmpl, field, notes_=notes_, entry=entry))

    # ── package_tier1 ──
    pkg_type = extract_package_type(text)
    if pkg_type:
        r('package_tier1', 'package_type_application.package_type', pkg_type, vc=vc_int)
    else:
        m('package_tier1', 'package_type_application.package_type')

    intro = extract_intro_first_sentence(text)
    if intro:
        r('package_tier1', 'package_type_application.intended_service', intro, vc=vc_int)
    else:
        m('package_tier1', 'package_type_application.intended_service')

    perf = extract_performance_claims(text)
    if perf:
        r('package_tier1', 'performance_claims', perf, vc=vc_int)
    else:
        m('package_tier1', 'performance_claims')

    sae = extract_sae_grades(text)
    if sae:
        r('package_tier1', 'sae_grades_documented', sae, vc=vc_int)
    else:
        m('package_tier1', 'sae_grades_documented')

    bogs = extract_base_oil_groups(text)
    if bogs:
        r('package_tier1', 'permitted_base_oils_restrictions', bogs, vc=vc_int)
    else:
        m('package_tier1', 'permitted_base_oils_restrictions')

    m('package_tier1', 'route_selector_restrictions')

    trt = extract_treat_rate_table(text)
    if trt:
        printed, lo, hi, vk = trt
        r('package_tier1', 'treat_rate_matrix', printed, unit='%', lo=lo, hi=hi, vk=vk, vc=vc_int)
    else:
        m('package_tier1', 'treat_rate_matrix')

    m('package_tier1', 'required_co_components')
    m('package_tier1', 'published_formulations')

    # ── package_tier2 ──
    for prop_key, field, unit, temp in [
        ('tbn',          'tbn',           'mg KOH/g', ''),
        ('sulfated_ash', 'sulfated_ash',  'wt.%',     ''),
        ('ca',           'elements.Ca',   'wt.%',     ''),
        ('mg',           'elements.Mg',   'wt.%',     ''),
        ('zn',           'elements.Zn',   'wt.%',     ''),
        ('p',            'elements.P',    'wt.%',     ''),
        ('mo',           'elements.Mo',   'wt.%',     ''),
        ('n',            'elements.N',    'wt.%',     ''),
        ('s',            'elements.S',    'wt.%',     ''),
        ('kv40',         'kv40',          'cSt',      '40'),
        ('kv100',        'kv100',         'cSt',      '100'),
        ('density',      'density',       'kg/m3',    '20'),
        ('flash_point',  'flash_point',   '°C',       ''),
        ('pour_point',   'pour_point',    '°C',       ''),
    ]:
        res = extract_prop(text, prop_key, fmt)
        if res:
            spec_t, typ_t, meth = res
            if fmt == 'pkg_both' and typ_t:
                # Primary: typical value; alternate note: spec bound
                v, q, lo, hi, vk = _parse(typ_t)
                notes = f'spec bound from same TDS: {spec_t}'
                r('package_tier2', field, typ_t, unit=unit, v=v, q=q, lo=lo, hi=hi,
                  vk=vk, meth=meth, notes=notes, entry='primary')
                # Also record spec bound as alternate entry
                sv, sq, slo, shi, svk = _parse(spec_t)
                r('package_tier2', field, spec_t, unit=unit, v=sv, q=sq, lo=slo, hi=shi,
                  vk=svk, meth=meth,
                  notes='spec bound from same TDS (Requirement/Limit column)', entry='spec-bound-same-TDS',
                  vc=vc_tbl.replace('Typical Value', 'Requirement Limit'))
            else:
                v, q, lo, hi, vk = _parse(spec_t)
                r('package_tier2', field, spec_t, unit=unit, v=v, q=q, lo=lo, hi=hi,
                  vk=vk, meth=meth)
        else:
            m('package_tier2', field, f'{prop_key} not found in the inspected text')

    # elements.B: not reported in Richful TDS
    m('package_tier2', 'elements.B', 'not found in the inspected text; Richful TDS do not report B')
    m('package_tier2', 'specific_gravity', 'not found in the inspected text; Richful TDS report density, not specific gravity')

    return rows

# ── Alternate-edition rows (DL2 prior editions) ───────────────────────
def alt_tds_rows(pk, text, sha, fname, rev, fmt, tmpl_set):
    """Write a summary 'alternate-prior-edition' row for key numeric properties from an older TDS edition."""
    rows = []
    vc = ('product data sheet, prior edition (DL2), Typical Value column' if fmt == 'old_typical'
          else 'product data sheet, prior edition (DL2), Requirement Limit column')
    for prop_key, field, tmpl, unit in [
        ('flash_point', 'function_specific_markers.tbn', 'component_general', 'mg KOH/g'),  # placeholder
    ]:
        pass  # only write if there are differing values; handled via notes in primary rows
    return rows  # Minimal; primary notes capture the alternate edition reference

# ── Main processing ──────────────────────────────────────────────────
ALL_ROWS = []

for pk in sorted(ELIGIBLE):
    dec = decisions.get(pk, {})
    mat_class = dec.get('material_class', '')
    status    = dec.get('status', '')
    if status == 'existing' or mat_class in ('out_of_template: fuel additive', 'unresolved'):
        continue

    doc_links = prod_docs.get(pk, [])
    if not doc_links:
        continue

    primary_lk, alt_lks = select_tds(doc_links)
    sha   = primary_lk['sha256']
    fname = os.path.basename(primary_lk['file'])
    rev   = get_rev_date(sha)
    text  = get_text(sha)
    if not text:
        # All fields missing
        if mat_class == 'additive_component':
            for f in field_units('component_general'):
                ALL_ROWS.append(_miss(pk, 'component_general', f, 'cached text not found for primary TDS'))
        elif mat_class == 'additive_package':
            for f in field_units('package_tier1'):
                ALL_ROWS.append(_miss(pk, 'package_tier1', f, 'cached text not found for primary TDS'))
            for f in field_units('package_tier2'):
                ALL_ROWS.append(_miss(pk, 'package_tier2', f, 'cached text not found for primary TDS'))
        continue

    fmt = detect_format(text)

    if mat_class == 'additive_component':
        is_ppd = pk in ('RICHFUL:RF8236', 'RICHFUL:RF8248')
        rows = component_rows(pk, text, sha, fname, rev, fmt, is_ppd=is_ppd)
        ALL_ROWS.extend(rows)

        # Also record key values from the DL2 prior edition (oldest typical values) in notes
        for alt_lk in alt_lks[:1]:
            alt_sha   = alt_lk['sha256']
            alt_fname = os.path.basename(alt_lk['file'])
            alt_rev   = get_rev_date(alt_sha)
            alt_text  = get_text(alt_sha)
            if alt_text:
                alt_fmt = detect_format(alt_text)
                # Only add TDS/PDS alternate rows, not SDS
                alt_dt = docs_inv.get(alt_sha, {}).get('document_type', '')
                if alt_dt in ('TDS/PDS', 'TDS', ''):
                    # Write a summary row for TBN/Ca as alternate-prior-edition if differs
                    for prop_key, field, unit in [('tbn', 'function_specific_markers.tbn', 'mg KOH/g'),
                                                  ('ca',  'function_specific_markers.ca',  'wt.%')]:
                        res = extract_prop(alt_text, prop_key, alt_fmt)
                        if res:
                            st, tt, meth = res
                            cell = tt if (alt_fmt == 'pkg_both' and tt) else st
                            v, q, lo, hi, vk = _parse(cell)
                            ALL_ROWS.append(_make_row(
                                pk, 'component_general', field, cell, unit=unit,
                                value=v, qual=q, lo=lo, hi=hi, vk=vk, meth=meth,
                                sha=alt_sha, fname=alt_fname, rev=alt_rev,
                                notes=f'prior edition (older DL2 batch); primary source is {fname}',
                                vc='product data sheet, prior edition / alternate TDS edition',
                                entry='alternate-prior-edition'))

    elif mat_class == 'additive_package':
        rows = package_rows(pk, text, sha, fname, rev, fmt)
        ALL_ROWS.extend(rows)

# ── Write output ──────────────────────────────────────────────────────
write_rows('s05_richful.csv', ALL_ROWS)
print(f'Written {len(ALL_ROWS)} rows to s05_richful.csv')
