"""Field-level mapping, S39 Bettchem — 11 products, 11 sheets.

All sheets read in full (text layer) 2026-11-16.

Products (all additive_package; tier1 + tier2 mapped):
  EXISTING:BETTCHEM_BT_3088   Heavy-duty diesel DI pack, API CI-4/CH-4    DL2-15551
  EXISTING:BETTCHEM_BT_3089   Diesel DI pack (customer specific), low-mid  DL2-15552
  EXISTING:BETTCHEM_BT_3093   Heavy-duty diesel DI pack, API CI-4/CH-4    DL2-15550
  BETTCHEM:BT3090             PCMO DI pack, API SL/SJ + JASO MA2/MB       DL2-15553
  BETTCHEM:BT_3091            Mid-tier gasoline/diesel DI pack             DL2-15549
  BETTCHEM:BT_3095            Gasoline DI pack, API SP through SJ          DL2-15554
  BETTCHEM:BT3096             Premium diesel DI pack, API CK-4/CJ-4+       DL2-15555
  BETTCHEM:BT3097             PCMO DI pack, API SL/CF through CB/SB        DL2-15556
  BETTCHEM:BT3098             Gasoline/diesel DI pack, API SN through CB/SB DL2-15557
  BETTCHEM:BT_55006           High-zinc anti-wear hydraulic oil package     DL2-15558
  BETTCHEM:BT_55050           Multifunction transmission oil package (UTTO) DL2-15548

Date format note: Bettchem TDS dates use inconsistent M/D/YYYY and D/M/YYYY formats
  across the batch. Interpretations based on disambiguation rules (day > 12 → D is day):
  12/12/2024 → 2024-12-12; 9/25/2024 → 2024-09-25; 20/11/2023 → 2023-11-20;
  26/9/2023 → 2023-09-26; 7/19/2024 → 2024-07-19; 6/18/2024 → 2024-06-18;
  9/23/2024 → 2024-09-23. Ambiguous (12/6/2023, 6/12/2023, 8/12/24) treated as M/D.

BT3093 treat rate table anomaly: performance spec labels (API CI-4, CH-4, CF-4/SL)
  appear at the bottom of the page, not as row headers in the treat rate table.
  Rows mapped 8.0% → CI-4, 7.0% → CH-4, 6.0% → CF-4/SL (by position).

BT_3095 zinc anomaly: TDS prints Zn Wt.% min=109, max=147 (physically impossible as wt%;
  likely a decimal omission: 1.09 and 1.47 wt%), typical=1.28. Recorded as printed.

BT_55006 kv100: TDS prints "VISCOSITY at 100℃, cSt: Report" — test method listed but
  no typical value given; recorded as Missing.

Writes field_evidence/s39_bettchem.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    # sha12: (canonical_file, revision_date)
    'b029e6a70b13': ('DL2-15551.pdf', '2024-12-12'), # BT3088 TDS v2.0; Date 12/12/2024
    'ca2e740185f3': ('DL2-15552.pdf', '2024-09-25'), # BT3089 TDS v1.0; Date 9/25/2024 (M/D)
    '0d75064e3d77': ('DL2-15550.pdf', '2023-12-06'), # BT3093 TDS v2.0; Date 12/6/2023 (M/D)
    '56cce0d005f1': ('DL2-15553.pdf', '2023-11-20'), # BT3090 TDS v3.0; Date 20/11/2023 (D/M)
    '803ed354053c': ('DL2-15549.pdf', '2023-12-06'), # BT_3091 TDS v3.0; Date 6/12/2023 (M/D)
    'ed0f2209ebfe': ('DL2-15554.pdf', '2023-09-26'), # BT_3095 TDS v1.0; Date 26/9/2023 (D/M)
    'cf8f2b77e4bf': ('DL2-15555.pdf', '2023-12-06'), # BT3096 TDS v2.0; Date 12/6/2023 (M/D)
    'cce8367f0bd7': ('DL2-15556.pdf', '2024-07-19'), # BT3097 TDS v1.0; Date 7/19/2024 (M/D)
    'be9efdc91993': ('DL2-15557.pdf', '2024-08-12'), # BT3098 TDS v1.0; Date 8/12/24 (M/D)
    '73145f665d6f': ('DL2-15558.pdf', '2024-06-18'), # BT_55006 TDS v1.0; Date 6/18/2024 (M/D)
    '214ac88f7bec': ('DL2-15548.pdf', '2024-09-23'), # BT_55050 TDS v1.0; Date 9/23/2024 (M/D)
}

REVIEW = 'sheet read in full (text layer) 2026-11-16; parsed rows compared with the page text'
VC_TDS       = 'product data sheet, specifications / properties table'
VC_TDS_DESC  = 'product data sheet, description / application section'
VC_TDS_TREAT = 'product data sheet, treat rate table'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='', pg=1, notes='', vc=None, entry=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc or VC_TDS, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


def _m(pk, tmpl, field, notes_='', entry=''):
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'status': 'Missing', 'value_class': '', 'basis': '',
        'source_file': '', 'sha256': '', 'page': '', 'revision_date': '',
        'notes': notes_ or 'not found in the inspected text',
        'review': REVIEW,
        **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind', 'printed_text',
                            'unit', 'test_temperature_c', 'method', 'conditions']},
    })


def _t1_common(pk, sha, pkg_type, intended, claims, sae, treat_rows,
               co_comp_note=None, pg_desc=1, pg_treat=1):
    """Write package_tier1 rows.
    claims: list of str (performance claim labels).
    sae: str or None (None → Missing).
    treat_rows: list of (entry_key, printed_text, value, unit, notes).
    co_comp_note: str or None (None → Missing).
    """
    _r(pk, 'package_tier1', 'package_type_application.package_type',
       pkg_type, vk='text', vc=VC_TDS_DESC, sha=sha, pg=pg_desc)
    _r(pk, 'package_tier1', 'package_type_application.intended_service',
       intended, vk='text', vc=VC_TDS_DESC, sha=sha, pg=pg_desc)
    for cl in claims:
        _r(pk, 'package_tier1', 'performance_claims', cl,
           vk='text', vc=VC_TDS_TREAT, sha=sha, pg=pg_treat,
           entry=cl.replace('/', '_').replace(' ', '_').replace('.', '_').replace('-', '_'))
    if sae:
        _r(pk, 'package_tier1', 'sae_grades_documented', sae,
           vk='text', vc=VC_TDS_TREAT, sha=sha, pg=pg_treat,
           notes='stated in treat rate table viscosity grade column')
    else:
        _m(pk, 'package_tier1', 'sae_grades_documented',
           'not found; no SAE viscosity grade stated in TDS')
    _m(pk, 'package_tier1', 'permitted_base_oils_restrictions',
       'not found; not stated in TDS')
    _m(pk, 'package_tier1', 'route_selector_restrictions',
       'not found; not stated in TDS')
    for ek, pt, val, unit, tnotes in treat_rows:
        _r(pk, 'package_tier1', 'treat_rate_matrix', pt,
           value=val, unit=unit, vk='typical', vc=VC_TDS_TREAT, sha=sha, pg=pg_treat,
           entry=ek, notes=tnotes)
    if co_comp_note:
        _r(pk, 'package_tier1', 'required_co_components', co_comp_note,
           vk='text', vc=VC_TDS_DESC, sha=sha, pg=pg_desc,
           notes='from Application section in TDS; no specific product or dose named')
    else:
        _m(pk, 'package_tier1', 'required_co_components',
           'not found; not stated in TDS')
    _m(pk, 'package_tier1', 'published_formulations',
       'not found; not stated in TDS')


def _t2_common(pk, sha, tbn_row, ash_row, elements, kv40_row, kv100_row,
               sg_row, flash_row, pour_row, pg=1):
    """Write package_tier2 rows.
    tbn_row, ash_row, kv40_row, kv100_row, sg_row, flash_row, pour_row:
      None → Missing; else (printed, value, lo, hi, qual, unit, meth, vk, notes).
    elements: dict field → (printed, value, lo, hi, qual, unit, meth, vk, notes) or None.
    """
    _ELEMENT_FIELDS = ['Ca', 'Mg', 'Zn', 'P', 'B', 'Mo', 'N', 'S']

    def _emit(field, row):
        if row is None:
            _m(pk, 'package_tier2', field)
        else:
            printed, value, lo, hi, qual, unit, meth, vk, notes = row
            _r(pk, 'package_tier2', field, printed,
               value=value, lo=lo, hi=hi, qual=qual, unit=unit,
               meth=meth, vk=vk, sha=sha, pg=pg, notes=notes)

    _emit('tbn', tbn_row)
    _emit('sulfated_ash', ash_row)
    for ef in _ELEMENT_FIELDS:
        _emit(f'elements.{ef}', elements.get(ef))
    _emit('kv40', kv40_row)
    _emit('kv100', kv100_row)
    _emit('density', None)                 # always Missing; Bettchem reports SG not density
    _emit('specific_gravity', sg_row)
    _emit('flash_point', flash_row)
    _emit('pour_point', pour_row)


# helper row constructors for common patterns
def R_typ(printed, value, unit, meth, notes=''):
    return (printed, str(value), '', '', '', unit, meth, 'typical', notes)

def R_rng(printed, lo, hi, unit, meth, notes=''):
    return (printed, '', str(lo), str(hi), '', unit, meth, 'range', notes)

def R_typ_rng(printed, value, lo, hi, unit, meth, notes=''):
    return (printed, str(value), str(lo), str(hi), '', unit, meth, 'typical', notes)

def R_bound_max(printed, hi, qual, unit, meth, notes=''):
    return (printed, '', '', str(hi), qual, unit, meth, 'bound', notes)

def R_bound_min(printed, lo, qual, unit, meth, notes=''):
    return (printed, '', str(lo), '', qual, unit, meth, 'bound', notes)

def _MISS():
    return None   # Missing

MASS = 'mass/wt-%'
ASTM_ELEM = 'ASTM D4951'
ASTM_KV   = 'ASTM D445'
ASTM_FP   = 'ASTM D92'
ASTM_PP   = 'ASTM D97'
ASTM_TBN  = 'ASTM D2896'
ASTM_ASH  = 'ASTM D874'
ASTM_N    = 'ASTM D5762'
ASTM_SG   = 'ASTM D1298'


# ──────────────────────────────────────────────────────────────────────────────
# BT3088  DL2-15551.pdf  sha b029e6a70b13   EXISTING:BETTCHEM_BT_3088
# HEAVY DUTY DIESEL ENGINE OIL ADDITIVE PACKAGE  v2.0  2024-12-12
# API CI-4/CH-4; treat rates 8.0/7.0/6.0 wt%
# ──────────────────────────────────────────────────────────────────────────────
PK = 'EXISTING:BETTCHEM_BT_3088'
S  = 'b029e6a70b13'

_t1_common(PK, S,
    pkg_type='Heavy Duty Diesel Engine Oil Additive Package',
    intended='heavy duty diesel engine oils; API CI-4/CH-4 performance levels',
    claims=['API CI-4', 'API CH-4', 'API CF-4', 'API SG', 'API SJ'],
    sae=None,
    treat_rows=[
        ('API_CI_4',    'API CI-4: 8.0% wt',    '8.0',  '% wt', ''),
        ('API_CH_4_SJ', 'API CH-4/SJ: 7.0% wt', '7.0',  '% wt', ''),
        ('API_CF_4_SG', 'API CF-4/SG: 6.0% wt', '6.0',  '% wt', ''),
    ],
    co_comp_note=None,
)

_t2_common(PK, S,
    tbn_row   = R_typ_rng('BASE NUMBER mg KOH/g: Minimum 112, Maximum 125, Typical 118',
                           118, 112, 125, 'mgKOH/g', ASTM_TBN),
    ash_row   = R_typ_rng('SULPHATED ASH: Minimum 10, Maximum 15, Typical 12.57',
                           12.57, 10, 15, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ_rng('CALCIUM: Minimum 2.90, Maximum 3.40, Typical 3.14',
                         3.14, 2.90, 3.40, MASS, ASTM_ELEM),
        'Mg': _MISS(),
        'Zn': R_typ_rng('ZINC: Minimum 0.90, Maximum 1.40, Typical 1.18',
                         1.18, 0.90, 1.40, MASS, ASTM_ELEM),
        'P':  R_typ_rng('PHOSPHORUS: Minimum 0.75, Maximum 1.20, Typical 0.98',
                         0.98, 0.75, 1.20, MASS, ASTM_ELEM),
        'B':  R_bound_max('BORON: Maximum 0.10 (Minimum Report)', '0.10', '<=', MASS, ASTM_ELEM,
                          notes='min=Report (measured but not disclosed); max 0.10 is upper spec bound'),
        'Mo': _MISS(),
        'N':  R_typ_rng('NITROGEN: Minimum 1.00, Maximum 1.40, Typical 1.21',
                         1.21, 1.00, 1.40, MASS, ASTM_N),
        'S':  R_typ_rng('SULPHUR: Minimum 1.9, Maximum 2.5, Typical 2.26',
                         2.26, 1.9, 2.5, MASS, ASTM_ELEM),
    },
    kv40_row  = R_bound_max('KINEMATIC VISCOSITY AT 40℃cSt: Maximum 4584 (Minimum Report)',
                             '4584', '<=', 'cSt', ASTM_KV,
                             notes='min=Report; 4584 is spec upper bound only'),
    kv100_row = R_typ_rng('KINEMATIC VISCOSITY AT 100℃cSt: Minimum 150, Maximum 250, Typical 198.8',
                           198.8, 150, 250, 'cSt', ASTM_KV),
    sg_row    = R_bound_max('SPECIFIC GRAVITY at 15.6℃: Maximum 0.9881 (Minimum Report)',
                             '0.9881', '<=', '', ASTM_SG,
                             notes='min=Report; 0.9881 is spec upper bound; typical not stated'),
    flash_row = ('FLASH POINT (COC ℃): Minimum 180, Maximum ＞190',
                 '', '180', '190', '', '°C', ASTM_FP, 'range',
                 'upper bound printed as ">190"; recorded as max=190 with open-ended qualifier implied'),
    pour_row  = R_bound_max('POUR POINT ℃: Maximum -9 (Minimum Report)',
                             '-9', '<=', '°C', ASTM_PP,
                             notes='min=Report; -9 is spec upper bound'),
)


# ──────────────────────────────────────────────────────────────────────────────
# BT3089  DL2-15552.pdf  sha ca2e740185f3   EXISTING:BETTCHEM_BT_3089
# DIESEL ENGINE OIL ADDITIVE PACKAGE (CUSTOMER SPECIFIC)  v1.0  2024-09-25
# Low/mid-tier diesel; API CF-4/SJ through CC/SC
# ──────────────────────────────────────────────────────────────────────────────
PK = 'EXISTING:BETTCHEM_BT_3089'
S  = 'ca2e740185f3'

_t1_common(PK, S,
    pkg_type='Diesel Engine Oil Additive Package',
    intended='low and middle tier diesel engine oils; cost-effective solution',
    claims=['API CF-4', 'API SJ', 'API CF', 'API SF', 'API CD', 'API SD', 'API CC', 'API SC'],
    sae=None,
    treat_rows=[
        ('API_CF_4_SJ', 'API CF-4/SJ: 4.8% wt', '4.8', '% wt', ''),
        ('API_CF_SF',   'API CF/SF: 3.5% wt',    '3.5', '% wt', ''),
        ('API_CF_CD',   'API CF/CD: 3.2% wt',    '3.2', '% wt', ''),
        ('API_CD_SD',   'API CD/SD: 2.5% wt',    '2.5', '% wt', ''),
        ('API_CC_SC',   'API CC/SC: 2.2% wt',    '2.2', '% wt', ''),
    ],
    co_comp_note=None,
)

_t2_common(PK, S,
    tbn_row   = R_rng('BASE NUMBER mg KOH/g: Minimum 198, Maximum 233 (no typical)',
                      198, 233, 'mgKOH/g', ASTM_TBN,
                      notes='typical not stated in TDS; spec range only'),
    ash_row   = R_typ_rng('SULPHATED ASH,%mass: Minimum 26.3, Maximum 35.6, Typical 31',
                           31, 26.3, 35.6, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ_rng('CALCIUM,%mass: Minimum 7.3, Maximum 9.88, Typical 8.59',
                         8.59, 7.3, 9.88, MASS, ASTM_ELEM),
        'Mg': _MISS(),
        'Zn': R_typ_rng('ZINC,%mass: Minimum 1.15, Maximum 1.55, Typical 1.35',
                         1.35, 1.15, 1.55, MASS, ASTM_ELEM),
        'P':  R_typ_rng('PHOSPHORUS,%mass: Minimum 1.01, Maximum 1.37, Typical 1.19',
                         1.19, 1.01, 1.37, MASS, ASTM_ELEM),
        'B':  _MISS(),
        'Mo': _MISS(),
        'N':  R_typ_rng('NITROGEN,%mass: Minimum 0.25, Maximum 0.35, Typical 0.3',
                         0.3, 0.25, 0.35, MASS, ASTM_N),
        'S':  R_typ_rng('Sulphur,%mass: Minimum 2.52, Maximum 3.4, Typical 2.96',
                         2.96, 2.52, 3.4, MASS, ASTM_ELEM),
    },
    kv40_row  = R_bound_max('KINEMATIC VISCOSITY AT 40℃cSt: Maximum 2420 (Minimum Report)',
                             '2420', '<=', 'cSt', ASTM_KV,
                             notes='min=Report; 2420 is spec upper bound'),
    kv100_row = R_typ_rng('KINEMATIC VISCOSITY AT 100℃cSt: Minimum 102.7, Maximum 154, Typical 128.4',
                           128.4, 102.7, 154, 'cSt', ASTM_KV),
    sg_row    = R_bound_max('SPECIFIC GRAVITY at 15.6℃: Maximum 1.09 (Minimum Report)',
                             '1.09', '<=', '', ASTM_SG,
                             notes='min=Report; 1.09 is spec upper bound; typical not stated'),
    flash_row = ('FLASH POINT (COC ℃): Minimum 180, Maximum ＞190',
                 '', '180', '190', '', '°C', ASTM_FP, 'range',
                 'upper bound printed as ">190"'),
    pour_row  = R_bound_max('Pour Point ℃: Maximum -12 (Minimum Report)',
                             '-12', '<=', '°C', ASTM_PP,
                             notes='min=Report; -12 is spec upper bound'),
)


# ──────────────────────────────────────────────────────────────────────────────
# BT3093  DL2-15550.pdf  sha 0d75064e3d77   EXISTING:BETTCHEM_BT_3093
# HEAVY DUTY DIESEL ENGINE OIL ADDITIVE PACKAGE (CUSTOMER SPECIFIC)  v2.0  2023-12-06
# API CI-4/CH-4; treat rates 8.0/7.0/6.0 (spec labels at bottom of page)
# ──────────────────────────────────────────────────────────────────────────────
PK = 'EXISTING:BETTCHEM_BT_3093'
S  = '0d75064e3d77'

_t1_common(PK, S,
    pkg_type='Heavy Duty Diesel Engine Oil Additive Package',
    intended='heavy duty diesel engines; API CI-4/CH-4 performance levels in suitable base stocks',
    claims=['API CI-4', 'API CH-4', 'API CF-4', 'API SL'],
    sae=None,
    treat_rows=[
        ('API_CI_4',    'API CI-4: 8.0% wt', '8.0', '% wt',
         'treat rate table has no row-level spec labels; API CI-4 label appears at bottom of page; mapped by position (highest treat rate → highest spec)'),
        ('API_CH_4',    'API CH-4: 7.0% wt', '7.0', '% wt',
         'treat rate label API CH-4 at bottom of page; second treat rate row'),
        ('API_CF_4_SL', 'API CF-4/SL: 6.0% wt', '6.0', '% wt',
         'treat rate label API CF-4/SL at bottom of page; third treat rate row'),
    ],
    co_comp_note=None,
)

_t2_common(PK, S,
    tbn_row   = R_rng('BASE NUMBER mg KOH/g: Minimum 100, Maximum 115 (no typical)',
                      100, 115, 'mgKOH/g', ASTM_TBN,
                      notes='typical not stated in TDS; spec range only'),
    ash_row   = R_typ_rng('SULPHATED ASH, mass/wt-%: Minimum 11.0, Maximum 15.0, Typical 12.7',
                           12.7, 11.0, 15.0, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ_rng('CALCIUM, mass/wt-%: Minimum 1.24, Maximum 1.5, Typical 1.34',
                         1.34, 1.24, 1.5, MASS, ASTM_ELEM),
        'Mg': R_typ_rng('MAGNESIUM, mass/wt-%: Minimum 1.30, Maximum 1.60, Typical 1.36',
                         1.36, 1.30, 1.60, MASS, ASTM_ELEM),
        'Zn': R_typ_rng('ZINC, mass/wt-%: Minimum 1.46, Maximum 1.75, Typical 1.57',
                         1.57, 1.46, 1.75, MASS, ASTM_ELEM),
        'P':  R_typ_rng('PHOSPHORUS, mass/wt-%: Minimum 1.26, Maximum 1.50, Typical 1.34',
                         1.34, 1.26, 1.50, MASS, ASTM_ELEM),
        'B':  _MISS(),
        'Mo': R_bound_max('MOLYBDENUM, mass wt-%: Maximum 0.065 (Minimum Report)',
                           '0.065', '<=', MASS, ASTM_ELEM,
                           notes='min=Report; 0.065 is spec upper bound'),
        'N':  R_typ_rng('NITROGEN, mass/wt-%: Minimum 0.75, Maximum 1.10, Typical 0.91',
                         0.91, 0.75, 1.10, MASS, ASTM_N),
        'S':  R_typ_rng('SULPHUR, mass/wt-%: Minimum 2.60, Maximum 3.49, Typical 3.04',
                         3.04, 2.60, 3.49, MASS, ASTM_ELEM),
    },
    kv40_row  = R_bound_max('KINEMATIC VISCOSITY AT 40℃,cSt: Maximum 3372 (Minimum Report)',
                             '3372', '<=', 'cSt', ASTM_KV,
                             notes='min=Report; 3372 is spec upper bound'),
    kv100_row = R_typ_rng('KINEMATIC VISCOSITY AT 100℃,cSt: Minimum 95, Maximum 155, Typical 148.9',
                           148.9, 95, 155, 'cSt', ASTM_KV),
    sg_row    = R_typ_rng('SPECIFIC GRAVITY at 15.6℃: Minimum 0.9, Maximum 1.1, Typical 0.99',
                           0.99, 0.9, 1.1, '', ASTM_SG),
    flash_row = R_rng('FLASH POINT (COC ℃): Minimum 160, Maximum 198',
                      160, 198, '°C', ASTM_FP),
    pour_row  = None,
)


# ──────────────────────────────────────────────────────────────────────────────
# BT3090  DL2-15553.pdf  sha 56cce0d005f1   BETTCHEM:BT3090
# PASSENGER CAR ENGINE OIL ADDITIVE PACKAGE (CUSTOMER SPECIFIC)  v3.0  2023-11-20
# API SL/CF, SJ/CF, SG/JASO MA2/MB; Group II base oils; needs VM co-component
# ──────────────────────────────────────────────────────────────────────────────
PK = 'BETTCHEM:BT3090'
S  = '56cce0d005f1'

_t1_common(PK, S,
    pkg_type='Passenger Car Engine Oil Additive Package',
    intended='PCMO; API SL/CF, SJ/CF, SG; JASO MA2/MB; Group II base oils',
    claims=['API SL', 'API CF', 'API SJ', 'API SG', 'JASO MA2', 'JASO MB'],
    sae=None,
    treat_rows=[
        ('API_SL_CF',       'API SL/CF: 5.6% wt', '5.6', '% wt', ''),
        ('API_SJ_CF',       'API SJ/CF: 4.8% wt', '4.8', '% wt', ''),
        ('API_SG_MA2_MB',   'API SG/MA2/MB: 4.3% wt', '4.3', '% wt',
         'TDS footnote: extra friction modifier is needed for JASO MB'),
    ],
    co_comp_note='appropriate viscosity modifier',
    pg_desc=1, pg_treat=1,
)

_t2_common(PK, S,
    tbn_row   = R_rng('BASE NUMBER, mg KOH/g: Minimum 110, Maximum 136 (no typical)',
                      110, 136, 'mgKOH/g', ASTM_TBN,
                      notes='typical not stated in TDS; spec range only'),
    ash_row   = R_typ_rng('SULFATED ASH, mass/wt-%: Minimum 15, Maximum 19, Typical 17.48',
                           17.48, 15, 19, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ_rng('CALCIUM, mass/wt-%: Minimum 3.95, Maximum 4.91, Typical 4.4',
                         4.4, 3.95, 4.91, MASS, ASTM_ELEM),
        'Mg': _MISS(),
        'Zn': R_typ_rng('ZINC, mass/wt-%: Minimum 1.60, Maximum 1.96, Typical 1.72',
                         1.72, 1.60, 1.96, MASS, ASTM_ELEM),
        'P':  R_typ_rng('PHOSPHORUS, mass/wt-%: Minimum 1.39, Maximum 1.75, Typical 1.58',
                         1.58, 1.39, 1.75, MASS, ASTM_ELEM),
        'B':  _MISS(),
        'Mo': R_bound_max('MOLYBDENUM, mass/wt-%: Maximum 0.092 (Minimum Report)',
                           '0.092', '<=', MASS, ASTM_ELEM,
                           notes='min=Report; 0.092 is spec upper bound'),
        'N':  R_typ_rng('NITROGEN, mass/wt-%: Minimum 0.74, Maximum 1.00, Typical 0.79',
                         0.79, 0.74, 1.00, MASS, ASTM_N),
        'S':  R_typ_rng('SULPHUR, mass/wt-%: Minimum 2.97, Maximum 4.02, Typical 3.5',
                         3.5, 2.97, 4.02, MASS, ASTM_ELEM),
    },
    kv40_row  = R_bound_max('KINEMATIC VISCOSITY at 40℃: Maximum 2360 (Minimum Report)',
                             '2360', '<=', 'cSt', ASTM_KV,
                             notes='min=Report; 2360 is spec upper bound'),
    kv100_row = R_typ_rng('KINEMATIC VISCOSITY at 100℃: Minimum 80, Maximum 120, Typical 108',
                           108, 80, 120, 'cSt', ASTM_KV),
    sg_row    = R_typ_rng('SPECIFIC GRAVITY at 15.6℃: Minimum 0.9, Maximum 1.15, Typical 1.03',
                           1.03, 0.9, 1.15, '', ASTM_SG),
    flash_row = R_rng('FLASH POINT (COC ℃): Minimum 160, Maximum 204',
                      160, 204, '°C', ASTM_FP),
    pour_row  = None,
)


# ──────────────────────────────────────────────────────────────────────────────
# BT_3091  DL2-15549.pdf  sha 803ed354053c   BETTCHEM:BT_3091
# MID TIER GASOLINE AND DIESEL ENGINE OIL ADDITIVE  v3.0  2023-12-06
# Wide range SJ/CF-4 down to CB/SB; Multi-grade and Mono-grade
# ──────────────────────────────────────────────────────────────────────────────
PK = 'BETTCHEM:BT_3091'
S  = '803ed354053c'

_t1_common(PK, S,
    pkg_type='Mid-tier Gasoline and Diesel Engine Oil Additive',
    intended='mid-tier gasoline and diesel engine oils; wide performance range rationalization',
    claims=['API SJ', 'API CF-4', 'API CF', 'API SG', 'API SF', 'API CD',
            'API SD', 'API CC', 'API SC', 'API CB', 'API SB'],
    sae='Multi-grade and Mono-grade',
    treat_rows=[
        ('API_SJ_CF_4_Multi',  'API SJ/CF-4 Multi-grade: 5.6% wt',  '5.6', '% wt', ''),
        ('API_CF_4_SG_Multi',  'API CF-4/SG Multi-grade: 5.2% wt',  '5.2', '% wt', ''),
        ('API_CF_SG_Multi',    'API CF/SG Multi-grade: 4.3% wt',    '4.3', '% wt', ''),
        ('API_CF_SF_Multi',    'API CF/SF Multi-grade: 3.8% wt',    '3.8', '% wt', ''),
        ('API_CF_Mono',        'API CF Mono-grade: 3.5% wt',        '3.5', '% wt', ''),
        ('API_SF_CD_Multi',    'APISF/CD Multi-grade: 3.8% wt',     '3.8', '% wt',
         'printed as "APISF/CD" (no space between API and SF/CD); recorded as printed'),
        ('API_CD_SD_Mono',     'API CD/SD Mono-grade: 2.7% wt',     '2.7', '% wt', ''),
        ('API_CC_SC_Mono',     'API CC/SC Mono-grade: 2.5% wt',     '2.5', '% wt', ''),
        ('API_CB_SB_Mono',     'API CB/SB Mono-grade: 1.5% wt',     '1.5', '% wt', ''),
    ],
    co_comp_note=None,
)

_t2_common(PK, S,
    tbn_row   = R_rng('TBN mg KOH/g: Minimum 170, Maximum 193 (no typical)',
                      170, 193, 'mgKOH/g', ASTM_TBN,
                      notes='typical not stated in TDS; spec range only'),
    ash_row   = R_typ_rng('SULPHATED ASH,mass/wt-%: Minimum 24.0, Maximum 28.0, Typical 26.0',
                           26.0, 24.0, 28.0, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ_rng('CALCIUM Wt. %: Minimum 6.3, Maximum 7.6, Typical 7.37',
                         7.37, 6.3, 7.6, 'Wt.%', ASTM_ELEM),
        'Mg': _MISS(),
        'Zn': R_typ_rng('ZINC Wt. %: Minimum 1.80, Maximum 2.20, Typical 2.04',
                         2.04, 1.80, 2.20, 'Wt.%', ASTM_ELEM),
        'P':  R_typ_rng('PHOSPHORUS Wt.%: Minimum 1.60, Maximum 1.95, Typical 1.78',
                         1.78, 1.60, 1.95, 'Wt.%', ASTM_ELEM),
        'B':  _MISS(),
        'Mo': _MISS(),
        'N':  R_typ_rng('NITROGEN Wt. %: Minimum 0.21, Maximum 0.38, Typical 0.23',
                         0.23, 0.21, 0.38, 'Wt.%', ASTM_N),
        'S':  R_typ_rng('SULPHUR Wt. %: Minimum 3.6, Maximum 4.88, Typical 4.25',
                         4.25, 3.6, 4.88, 'Wt.%', ASTM_ELEM),
    },
    kv40_row  = R_bound_max('VISCOSITYat 40℃,cSt: Maximum 1070 (Minimum Report)',
                             '1070', '<=', 'cSt', ASTM_KV,
                             notes='min=Report; 1070 is spec upper bound'),
    kv100_row = R_typ_rng('VISCOSITYat 100℃,cSt: Minimum 40, Maximum 80, Typical 60.16',
                           60.16, 40, 80, 'cSt', ASTM_KV),
    sg_row    = None,
    flash_row = R_rng('FLASH POINT,(COC),℃: Minimum 160, Maximum 192',
                      160, 192, '°C', ASTM_FP),
    pour_row  = None,
)


# ──────────────────────────────────────────────────────────────────────────────
# BT_3095  DL2-15554.pdf  sha ed0f2209ebfe   BETTCHEM:BT_3095
# GASOLINE ENGINE OIL ADDITIVE PACKAGE  v1.0  2023-09-26
# API SP/CF through SJ/CF
# BT_3095 Zinc anomaly: TDS prints Zn min=109, max=147 Wt.% (impossible; likely 1.09/1.47)
# ──────────────────────────────────────────────────────────────────────────────
PK = 'BETTCHEM:BT_3095'
S  = 'ed0f2209ebfe'

_t1_common(PK, S,
    pkg_type='Gasoline Engine Oil Additive Package',
    intended='gasoline engine oils; API SP/CF through SJ/CF performance levels in suitable base stocks',
    claims=['API SP', 'API SN', 'API SM', 'API SL', 'API SJ', 'API CF'],
    sae=None,
    treat_rows=[
        ('API_SP_CF', 'API SP/CF: 6.6% wt', '6.6', '% wt', ''),
        ('API_SN_CF', 'API SN/CF: 6.2% wt', '6.2', '% wt', ''),
        ('API_SM_CF', 'API SM/CF: 6.0% wt', '6.0', '% wt', ''),
        ('API_SL_CF', 'API SL/CF: 5.6% wt', '5.6', '% wt', ''),
        ('API_SJ_CF', 'API SJ/CF: 5.2% wt', '5.2', '% wt', ''),
    ],
    co_comp_note=None,
)

_t2_common(PK, S,
    tbn_row   = R_typ_rng('TBN mg KOH/g: Minimum 100, Maximum 140, Typical 124',
                           124, 100, 140, 'mgKOH/g', ASTM_TBN),
    ash_row   = R_typ_rng('SULFATED ASH Wt.%: Minimum 10.4, Maximum 14.2, Typical 12.27',
                           12.27, 10.4, 14.2, 'Wt.%', ASTM_ASH),
    elements={
        'Ca': R_typ_rng('CALCIUM Wt. %: Minimum 1.02, Maximum 1.38, Typical 1.20',
                         1.20, 1.02, 1.38, 'Wt.%', ASTM_ELEM),
        'Mg': R_typ_rng('MAGNESIUM Wt. %: Minimum 1.10, Maximum 1.75, Typical 1.52',
                         1.52, 1.10, 1.75, 'Wt.%', ASTM_ELEM),
        'Zn': R_typ_rng('ZINC Wt. %: Minimum 109, Maximum 147, Typical 1.28',
                         1.28, 109, 147, 'Wt.%', ASTM_ELEM,
                         notes='apparent printing error: min=109 and max=147 are impossible as wt%; '
                               'likely 1.09 and 1.47 (decimal omitted); typical=1.28 wt% is physically plausible; '
                               'recorded as printed; resolution deferred to JSON conversion'),
        'P':  R_typ_rng('PHOSPHORUS Wt.%: Minimum 0.97, Maximum 1.21, Typical 1.14',
                         1.14, 0.97, 1.21, 'Wt.%', ASTM_ELEM),
        'B':  _MISS(),
        'Mo': ('MOLYBDENUM Wt. %: Minimum 0.05, Typical 0.10',
                '0.10', '0.05', '', '', 'Wt.%', ASTM_ELEM, 'typical',
                'min 0.05 printed; no max stated; typical 0.10'),
        'N':  R_typ_rng('NITROGEN Wt. %: Minimum 1.04, Maximum 1.40, Typical 1.22',
                         1.22, 1.04, 1.40, 'Wt.%', ASTM_N),
        'S':  R_typ_rng('SULPHUR Wt. %: Minimum 2.39, Maximum 3.24, Typical 2.82',
                         2.82, 2.39, 3.24, 'Wt.%', ASTM_ELEM),
    },
    kv40_row  = None,
    kv100_row = R_typ_rng('VISCOSITY at 100℃,cSt: Minimum 85, Maximum 135, Typical 104',
                           104, 85, 135, 'cSt', ASTM_KV),
    sg_row    = None,
    flash_row = ('FLASH POINT,(COC),℃: Minimum 160, Typical >190',
                 '>190', '160', '', '', '°C', ASTM_FP, 'typical',
                 'max not stated; printed typical is ">190" (open bound); min=160'),
    pour_row  = None,
)


# ──────────────────────────────────────────────────────────────────────────────
# BT3096  DL2-15555.pdf  sha cf8f2b77e4bf   BETTCHEM:BT3096
# PREMIUM DIESEL ENGINE OIL ADDITIVE PACKAGE (CUSTOMER SPECIFIC)  v2.0  2023-12-06
# API CK-4/CJ-4+/CI-4+; typical-only table (no min/max); soot dispersant incorporated
# ──────────────────────────────────────────────────────────────────────────────
PK = 'BETTCHEM:BT3096'
S  = 'cf8f2b77e4bf'

_t1_common(PK, S,
    pkg_type='Premium Diesel Engine Oil Additive Package',
    intended='modern premium heavy-duty diesel engine oils; API CK-4/CJ-4 Plus; incorporates special soot dispersant',
    claims=['API CK-4', 'API CJ-4 Plus', 'API CI-4 Plus'],
    sae=None,
    treat_rows=[
        ('API_CK_4',       'API CK-4: 11% wt',              '11',  '% wt', ''),
        ('API_CJ_4_CI_4p', 'API CJ-4/API CI-4 PLUS: 9.7% wt', '9.7', '% wt', ''),
    ],
    co_comp_note=None,
)

_t2_common(PK, S,
    tbn_row   = R_typ('BASE NUMBER mg KOH/g: 97', 97, 'mgKOH/g', ASTM_TBN),
    ash_row   = R_typ('SULPHATED ASH: 8', 8, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ('CALCIUM: 1.55', 1.55, MASS, ASTM_ELEM),
        'Mg': R_typ('MAGNESIUM: 0.36', 0.36, MASS, ASTM_ELEM),
        'Zn': R_typ('ZINC: 0.67', 0.67, MASS, ASTM_ELEM),
        'P':  R_typ('PHOSPHORUS: 0.6', 0.6, MASS, ASTM_ELEM),
        'B':  R_typ('BORON: 0.034', 0.034, MASS, ASTM_ELEM),
        'Mo': R_typ('Mo: 0.037', 0.037, MASS, ASTM_ELEM),
        'N':  R_typ('NITROGEN: 1.49', 1.49, MASS, ASTM_N),
        'S':  R_typ('Sulphur: 1.33', 1.33, MASS, ASTM_ELEM),
    },
    kv40_row  = R_typ('KINEMATIC VISCOSITY AT 40℃: 3595', 3595, 'cSt', ASTM_KV),
    kv100_row = R_typ('KINEMATIC VISCOSITY AT 100℃: 144.5', 144.5, 'cSt', ASTM_KV),
    sg_row    = R_typ('SPECIFIC GRAVITY at 15.6℃: 0.9675', 0.9675, '', ASTM_SG),
    flash_row = R_bound_min('FLASH POINT (COC ℃): ≥180', '180', '>=', '°C', ASTM_FP),
    pour_row  = R_typ('Pour Point ℃: 6', 6, '°C', ASTM_PP),
)


# ──────────────────────────────────────────────────────────────────────────────
# BT3097  DL2-15556.pdf  sha cce8367f0bd7   BETTCHEM:BT3097
# PASSENGER CAR ENGINE OIL ADDITIVE PACKAGE (CUSTOMER SPECIFIC)  v1.0  2024-07-19
# API SL/CF-4 through CB/SB; 10 treat rate rows; typical-only table
# ──────────────────────────────────────────────────────────────────────────────
PK = 'BETTCHEM:BT3097'
S  = 'cce8367f0bd7'

_t1_common(PK, S,
    pkg_type='Passenger Car Engine Oil Additive Package',
    intended='PCMO; API SL/CF through CB/SB; JASO MA2/MB; Group II base oils; needs viscosity modifier',
    claims=['API SL', 'API CF-4', 'API SJ', 'API CF', 'API SG', 'JASO MA2', 'JASO MB',
            'API SF', 'API CD', 'API SD', 'API CC', 'API SC', 'API CB', 'API SB'],
    sae=None,
    treat_rows=[
        ('API_SL_CF_4',      'API SL/CF-4: 5.6% wt',                 '5.6', '% wt', ''),
        ('API_SJ_CF_4',      'API SJ/CF-4: 5.2% wt',                 '5.2', '% wt', ''),
        ('API_SJ_CF',        'API SJ/CF: 5.2% wt',                   '5.2', '% wt', ''),
        ('API_CF_SG_MA2_MB', 'API CF/SG/JASO MA2/MB: 4.3% wt',      '4.3', '% wt', ''),
        ('API_CF_SF',        'API CF/SF: 3.8% wt',                   '3.8', '% wt', ''),
        ('API_CF',           'API CF: 3.5% wt',                       '3.5', '% wt', ''),
        ('API_SF_CD',        'API SF/CD: 3.8% wt',                   '3.8', '% wt', ''),
        ('API_CD_SD',        'API CD/SD: 2.7% wt',                   '2.7', '% wt', ''),
        ('API_CC_SC',        'API CC/SC: 2.5% wt',                   '2.5', '% wt', ''),
        ('API_CB_SB',        'API CB/SB: 1.5% wt',                   '1.5', '% wt', ''),
    ],
    co_comp_note='appropriate viscosity modifier',
    pg_desc=1, pg_treat=1,
)

_t2_common(PK, S,
    tbn_row   = R_typ('BASE NUMBER mg KOH/g: 147', 147, 'mgKOH/g', ASTM_TBN),
    ash_row   = R_typ('SULPHATED ASH: 19', 19, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ('CALCIUM: 4.98', 4.98, MASS, ASTM_ELEM),
        'Mg': _MISS(),
        'Zn': R_typ('ZINC: 1.6', 1.6, MASS, ASTM_ELEM),
        'P':  R_typ('PHOSPHORUS: 1.38', 1.38, MASS, ASTM_ELEM),
        'B':  _MISS(),
        'Mo': _MISS(),
        'N':  R_typ('NITROGEN: 0.64', 0.64, MASS, ASTM_N),
        'S':  R_typ('Sulphur: 3.16', 3.16, MASS, ASTM_ELEM),
    },
    kv40_row  = R_typ('KINEMATIC VISCOSITY AT 40℃: 2791', 2791, 'cSt', ASTM_KV),
    kv100_row = R_typ('KINEMATIC VISCOSITY AT 100℃: 141.1', 141.1, 'cSt', ASTM_KV),
    sg_row    = R_typ('SPECIFIC GRAVITY at 15.6℃: 1.026', 1.026, '', ASTM_SG),
    flash_row = R_bound_min('FLASH POINT (COC ℃): ≥180', '180', '>=', '°C', ASTM_FP),
    pour_row  = R_typ('Pour Point ℃: 6', 6, '°C', ASTM_PP),
)


# ──────────────────────────────────────────────────────────────────────────────
# BT3098  DL2-15557.pdf  sha be9efdc91993   BETTCHEM:BT3098
# GASOLINE AND DIESEL ENGINE OIL ADDITIVE PACKAGE  v1.0  2024-08-12
# API SN through CB/SB; 11 treat rate rows; min/max/typical table
# ──────────────────────────────────────────────────────────────────────────────
PK = 'BETTCHEM:BT3098'
S  = 'be9efdc91993'

_t1_common(PK, S,
    pkg_type='Gasoline and Diesel Engine Oil Additive Package',
    intended='gasoline and diesel engine oils; wide performance range; needs appropriate viscosity modifier',
    claims=['API SN', 'API SL', 'API CF-4', 'API SJ', 'API CF', 'API SG', 'JASO MA2', 'JASO MB',
            'API SF', 'API CD', 'API SD', 'API CC', 'API SC', 'API CB', 'API SB'],
    sae=None,
    treat_rows=[
        ('API_SN',           'API SN: 6.2% wt',                '6.2', '% wt', ''),
        ('API_SL_CF_4',      'API SL/CF-4: 5.6% wt',           '5.6', '% wt', ''),
        ('API_SJ_CF_4',      'API SJ/CF-4: 5.2% wt',           '5.2', '% wt', ''),
        ('API_SJ_CF',        'API SJ/CF: 4.8% wt',             '4.8', '% wt', ''),
        ('API_CF_SG_MA2_MB', 'API CF/SG/JASO MA2/MB: 4.3% wt', '4.3', '% wt', ''),
        ('API_CF_SF',        'API CF/SF: 3.8% wt',             '3.8', '% wt', ''),
        ('API_CF',           'API CF: 3.5% wt',                '3.5', '% wt', ''),
        ('API_SF_CD',        'API SF/CD: 3.8% wt',             '3.8', '% wt', ''),
        ('API_CD_SD',        'API CD/SD: 2.7% wt',             '2.7', '% wt', ''),
        ('API_CC_SC',        'API CC/SC: 2.5% wt',             '2.5', '% wt', ''),
        ('API_CB_SB',        'API CB/SB: 1.5% wt',             '1.5', '% wt', ''),
    ],
    co_comp_note='appropriate viscosity modifier',
    pg_desc=1, pg_treat=1,
)

_t2_common(PK, S,
    tbn_row   = R_rng('BASE NUMBER mg KOH/g: Minimum 122, Maximum 144 (no typical)',
                      122, 144, 'mgKOH/g', ASTM_TBN,
                      notes='typical not stated in TDS; spec range only'),
    ash_row   = R_typ_rng('SULPHATED ASH, mass/wt-%: Minimum 14.5, Maximum 19.9, Typical 17.2',
                           17.2, 14.5, 19.9, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ_rng('CALCIUM, mass/wt-%: Minimum 3.8, Maximum 5.2, Typical 4.50',
                         4.50, 3.8, 5.2, MASS, ASTM_ELEM),
        'Mg': _MISS(),
        'Zn': R_typ_rng('ZINC, mass/wt-%: Minimum 1.22, Maximum 1.66, Typical 1.44',
                         1.44, 1.22, 1.66, MASS, ASTM_ELEM),
        'P':  R_typ_rng('PHOSPHORUS, mass/wt-%: Minimum 1.06, Maximum 1.44, Typical 1.25',
                         1.25, 1.06, 1.44, MASS, ASTM_ELEM),
        'B':  _MISS(),
        'Mo': _MISS(),
        'N':  R_typ_rng('NITROGEN, mass/wt-%: Minimum 0.76, Maximum 1.05, Typical 0.9',
                         0.9, 0.76, 1.05, MASS, ASTM_N),
        'S':  R_typ_rng('SULPHUR, mass/wt-%: Minimum 2.1, Maximum 3.54, Typical 2.82',
                         2.82, 2.1, 3.54, MASS, ASTM_ELEM),
    },
    kv40_row  = R_bound_max('KINEMATIC VISCOSITY AT 40℃,cSt: Maximum 2312 (Minimum Report)',
                             '2312', '<=', 'cSt', ASTM_KV,
                             notes='min=Report; 2312 is spec upper bound'),
    kv100_row = R_typ_rng('KINEMATIC VISCOSITY AT 100℃,cSt: Minimum 84, Maximum 139, Typical 111.4',
                           111.4, 84, 139, 'cSt', ASTM_KV),
    sg_row    = R_bound_max('SPECIFIC GRAVITY AT 15.6℃: Maximum 1.0209 (Minimum Report)',
                             '1.0209', '<=', '', ASTM_SG,
                             notes='min=Report; 1.0209 is spec upper bound; typical not stated'),
    flash_row = ('FLASH POINT (COC ℃): Minimum 180, Maximum ＞190',
                 '', '180', '190', '', '°C', ASTM_FP, 'range',
                 'upper bound printed as ">190"'),
    pour_row  = R_bound_max('POUR POINT ℃: Maximum 0 (Minimum Report)',
                             '0', '<=', '°C', ASTM_PP,
                             notes='min=Report; 0°C is spec upper bound'),
)


# ──────────────────────────────────────────────────────────────────────────────
# BT_55006  DL2-15558.pdf  sha 73145f665d6f   BETTCHEM:BT_55006
# HIGH ZINC ANTI-WEAR HYDRAULIC OIL ADDITIVE PACKAGE  v1.0  2024-06-18
# Non-engine-oil package; GB/ISO/DIN/Parker Denison specs; typical-only table
# kv100 "Report" (method stated, typical not disclosed)
# ──────────────────────────────────────────────────────────────────────────────
PK = 'BETTCHEM:BT_55006'
S  = '73145f665d6f'

_t1_common(PK, S,
    pkg_type='High Zinc Anti-wear Hydraulic Oil Additive Package',
    intended='anti-wear hydraulic oils; GB 11118.1 HM; ISO 11158 HM/HV; DIN 51524-2/3; Parker Denison HF-2',
    claims=['GB 11118.1 HM', 'ISO 11158 HM', 'ISO 11158 HV',
            'DIN 51524-2', 'DIN 51524-3', 'Parker Denison HF-2'],
    sae=None,
    treat_rows=[
        ('HM_HV_std',    'GB 11118.1 HM / ISO 11158 HM/HV / DIN 51524-2/3 / Parker Denison HF-2: 0.65-0.8% wt',
         '', '% wt',
         'treat rate is a range: 0.65-0.8 wt%; multiple specs share the same row'),
        ('hydraulic_tx', 'Hydraulic transmission: 1.0% wt', '1.0', '% wt', ''),
    ],
    co_comp_note=None,
)

# Fix treat rate entry: the first row is a range (0.65-0.8), not a single value.
# Patch the last treat_rate_matrix row in ROWS that has entry 'HM_HV_std'
for _row in reversed(ROWS):
    if _row.get('field') == 'treat_rate_matrix' and _row.get('entry') == 'HM_HV_std':
        _row['printed_text'] = 'GB 11118.1 HM / ISO 11158 HM/HV / DIN 51524-2/3 / Parker Denison HF-2: 0.65-0.8% wt'
        _row['min'] = '0.65'; _row['max'] = '0.8'; _row['value'] = ''; _row['value_kind'] = 'range'
        break

_t2_common(PK, S,
    tbn_row   = None,
    ash_row   = None,
    elements={
        'Ca': _MISS(),
        'Mg': _MISS(),
        'Zn': R_typ('ZINC Wt. %: 7.40', 7.40, 'Wt.%', ASTM_ELEM),
        'P':  R_typ('PHOSPHORUS Wt.%: 6.40', 6.40, 'Wt.%', ASTM_ELEM),
        'B':  _MISS(),
        'Mo': _MISS(),
        'N':  _MISS(),
        'S':  R_typ('SULPHUR Wt. %: 13.00', 13.00, 'Wt.%', ASTM_ELEM),
    },
    kv40_row  = None,
    kv100_row = None,  # TDS prints "VISCOSITY at 100℃, cSt: Report" — method stated, value not disclosed
    sg_row    = None,
    flash_row = R_bound_min('FLASH POINT,(COC),℃: ＞110', '110', '>', '°C', ASTM_FP),
    pour_row  = None,
)
# kv100: add Missing with specific note (overrides default)
ROWS.append({
    'product_key': PK, 'template': 'package_tier2', 'field': 'kv100', 'entry': '',
    'status': 'Missing', 'value_class': '', 'basis': '',
    'source_file': '', 'sha256': '', 'page': '', 'revision_date': '',
    'notes': 'TDS prints "VISCOSITY at 100℃, cSt: Report" — test method ASTM D445 is listed '
             'but no typical value is disclosed; value not found in inspected text',
    'review': REVIEW,
    **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind', 'printed_text',
                        'unit', 'test_temperature_c', 'method', 'conditions']},
})


# ──────────────────────────────────────────────────────────────────────────────
# BT_55050  DL2-15548.pdf  sha 214ac88f7bec   BETTCHEM:BT_55050
# MULTIFUNCTION TRANSMISSION OIL ADDITIVE PACKAGE  v1.0  2024-09-23
# UTTO / Hydraulic+Transmission; farm machinery + construction machinery
# ──────────────────────────────────────────────────────────────────────────────
PK = 'BETTCHEM:BT_55050'
S  = '214ac88f7bec'

_t1_common(PK, S,
    pkg_type='Multifunction Transmission Oil Additive Package',
    intended='UTTO; hydraulic, transmission and brake fluid; farm machinery (combine-harvesters, tractors) and construction machinery',
    claims=['UTTO'],
    sae=None,
    treat_rows=[
        ('UTTO',          'UTTO: 5% wt',                     '5', '% wt', ''),
        ('hydraulic_tx',  'Hydraulic & Transmission: 2% wt', '2', '% wt', ''),
    ],
    co_comp_note=None,
)

_t2_common(PK, S,
    tbn_row   = R_typ('BASE NUMBER MG KOH/g: 94.9', 94.9, 'mgKOH/g', ASTM_TBN),
    ash_row   = R_typ('SULPHATED ASH: 16.48', 16.48, MASS, ASTM_ASH),
    elements={
        'Ca': R_typ('CA, MASS%: 3.1', 3.1, 'MASS%', ASTM_ELEM),
        'Mg': _MISS(),
        'Zn': R_typ('ZN, MASS%: 4.1', 4.1, 'MASS%', ASTM_ELEM),
        'P':  R_typ('P, MASS%: 4.4', 4.4, 'MASS%', ASTM_ELEM),
        'B':  _MISS(),
        'Mo': _MISS(),
        'N':  R_typ('N, MASS%: 0.65', 0.65, 'MASS%', ASTM_N),
        'S':  R_typ('S, MASS%: 7.85', 7.85, 'MASS%', ASTM_ELEM),
    },
    kv40_row  = R_typ('KINEMATIC VISCOSITY AT 40℃, MM²/S: 474.09', 474.09, 'MM²/S', ASTM_KV),
    kv100_row = R_typ('KINEMATIC VISCOSITY AT 100℃, MM²/S: 30.53', 30.53, 'MM²/S', ASTM_KV),
    sg_row    = R_typ('SPECIFIC GRAVITY AT 15.6℃: 1.07', 1.07, '', ASTM_SG),
    flash_row = R_bound_min('FLASH POINT, (COC)℃: ＞160', '160', '>', '°C', ASTM_FP),
    pour_row  = R_typ('POUR POINT ℃: -31', -31, '°C', ASTM_PP),
)


# ──────────────────────────────────────────────────────────────────────────────
write_rows('s39_bettchem.csv', ROWS)
if __name__ == '__main__':
    print(f's39_bettchem: {len(ROWS)} rows written to field_evidence/s39_bettchem.csv')
