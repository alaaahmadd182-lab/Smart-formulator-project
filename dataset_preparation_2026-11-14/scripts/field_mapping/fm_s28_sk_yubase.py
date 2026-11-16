"""Field-level mapping, S28 SK Yubase / Ocean Chemical / DOWPOL — 3 products, 4 documents.

Products:
  SK:YUBASE_4P              — SK Enmove YUBASE 4 Plus (Group III+ 4 cSt base oil)
    base_oil (tiers 1–3); 1 doc: YUBASE_SDS_GLOBAL_UN_4_PLUS.pdf (SDS GHS Rev.10 2026-06-30)
  OCEANCHEMICAL:HC6247      — Ocean Chemical HC6247 star-type hydro-diene polymer VII
    additive_component (component_general); 2 docs: DL2-15502 (TDS 4pp), DL2-15503 (TDS 1pp)
  DOWPOL:NEOFLEX_680        — DOWPOL NeoFlex 680 pour point depressant
    additive_component (component_general); 1 doc: DL2-15627 (TDS April 2018)

Document notes:
  YUBASE_SDS_GLOBAL_UN_4_PLUS.pdf (SDS, GHS UN Rev.10, version 4.0, revision 2026-06-30):
    Only document available for SK:YUBASE_4P — no TDS in the reviewed batch.
    Section 1 chemical name: "Distillates (petroleum), hydrotreated heavy paraffinic; Base oil
    - IP 346 < 3%, ≤ 20.5 cSt @40°C", CAS 64742-54-7 (100%). API group not stated explicitly;
    document does not use "Group III" or "Group II"; hydrotreating + IP 346 <3% rules out
    Group I but does not distinguish Group II from III.
    Section 9: specific gravity 0.828 (no temperature stated); kv40 "19 mm²/s (calculated
    value)" @40°C; flash point 220°C (COC); density "Not available"; no kv100, no VI,
    no pour point in Section 9. Most Tier 1 properties are Missing.
  DL2-15502 (HC6247 TDS, 4pp) and DL2-15503 (HC6247 TDS, 1pp): same content, 1pp is a
    subset. Disclaimer: "The data is typical value, it could not be applied to the development
    of product specifications." Characteristics table on p.1; viscosity-concentration data
    and formulation example on p.2–3; engine oil test results on p.3–4; both docs use same
    typical values and are treated as one consistent source.
  DL2-15627 (NEOFLEX 680 TDS, April 2018): 2pp; "Neo Synthetic Hydrocarbon chemistry"
    (proprietary PPD); typical properties and performance tables in multiple Group II/III/I
    base oils at 0.2% and 0.4% dose.

Writes field_evidence/s28_sk_yubase.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '8d54d874b4bc': ('YUBASE_SDS_GLOBAL_UN_4_PLUS.pdf', '2026-06-30'),  # YUBASE 4P SDS
    'b9233a17f398': ('DL2-15502.pdf', ''),                               # HC6247 TDS 4pp
    '55be2fa8cbdd': ('DL2-15503.pdf', ''),                               # HC6247 TDS 1pp
    'f4170e38995a': ('DL2-15627.pdf', '2018-04-01'),                     # NEOFLEX_680 TDS
}

REVIEW_YU  = ('sheet read in full (text layer) 2026-11-16; '
              '1 doc: SDS YUBASE_SDS_GLOBAL_UN_4_PLUS.pdf (GHS UN Rev.10 v4.0 2026-06-30); '
              'no TDS available in the reviewed batch')
REVIEW_HC  = ('sheets read in full (text layer) 2026-11-16; '
              '2 docs: TDS DL2-15502 (4pp), DL2-15503 (1pp same content); '
              'both docs consistent; 4pp is primary source')
REVIEW_NEO = ('sheet read in full (text layer) 2026-11-16; '
              '1 doc: TDS DL2-15627 (Revision April 2018)')

VC_TDS = 'product data sheet (TDS/PDS), typical properties table'
VC_SDS = 'safety data sheet (SDS), Section 9 physical properties'
VC_SDS3 = 'safety data sheet (SDS), Section 3 composition'

YU  = 'SK:YUBASE_4P'
HC  = 'OCEANCHEMICAL:HC6247'
NEO = 'DOWPOL:NEOFLEX_680'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='', pg=1, notes='', entry='', vc=VC_TDS, review=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': review,
    })


def _m(pk, tmpl, field, notes_='', review=''):
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': '',
        'status': 'Missing', 'value_class': '', 'basis': '',
        'source_file': '', 'sha256': '', 'page': '', 'revision_date': '',
        'notes': notes_ or 'not found in the inspected text',
        'review': review,
        **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind',
                            'printed_text', 'unit', 'test_temperature_c',
                            'method', 'conditions']},
    })


def _nit(pk, prop, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
         meth='', cond='', sha='', pg=1, notes='', vc=VC_TDS, review=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': 'not_in_template:' + prop, 'field': prop, 'entry': '',
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': review,
    })


# ===========================================================================
# SK:YUBASE_4P — base_oil tiers 1–3 (SDS only)
# ===========================================================================

_r(YU, 'base_oil_tier1', 'api_group_chemistry',
   'Distillates (petroleum), hydrotreated heavy paraffinic; Base oil - IP 346 < 3%, '
   '≤ 20.5 cSt @40℃',
   vk='text', sha='8d54d874b4bc', pg=2, vc=VC_SDS3, review=REVIEW_YU,
   notes='SDS Section 3 composition name; IP 346 <3% (DMSO extract <3%) rules out Group I '
         '(typically >3%) and is consistent with Group II or III; document does not state '
         '"Group II", "Group III", or "Group III+" explicitly; brand YUBASE is associated '
         'with Group III+ by SK designation, but that is not printed in this SDS')

_r(YU, 'base_oil_tier1', 'kv40',
   'Viscosity, kinematic (calculated value) (40 °C): 19 mm²/s',
   unit='mm2/s', value='19', vk='typical',
   cond='40°C',
   sha='8d54d874b4bc', pg=4, vc=VC_SDS, review=REVIEW_YU,
   notes='SDS Section 9 labels this as "(calculated value)" — not a direct measurement; '
         'SDS Section 3 also states "≤ 20.5 cSt @40°C" in the substance name, consistent')

_m(YU, 'base_oil_tier1', 'kv100',
   'not found in SDS; Section 9 does not list kv100', review=REVIEW_YU)
_m(YU, 'base_oil_tier1', 'viscosity_index',
   'not found in SDS; Section 9 does not list VI', review=REVIEW_YU)
_m(YU, 'base_oil_tier1', 'density',
   'SDS Section 9 states "Density: Not available"', review=REVIEW_YU)

_r(YU, 'base_oil_tier1', 'specific_gravity',
   'Specific Gravity: 0.828',
   value='0.828', vk='typical',
   sha='8d54d874b4bc', pg=4, vc=VC_SDS, review=REVIEW_YU,
   notes='from SDS Section 9; no temperature stated for the specific gravity measurement')

_m(YU, 'base_oil_tier1', 'ccs',
   'not found in SDS; CCS not in Section 9', review=REVIEW_YU)

# Tier 2
_m(YU, 'base_oil_tier2', 'mrv',
   'not found in SDS; MRV not in Section 9', review=REVIEW_YU)
_m(YU, 'base_oil_tier2', 'noack_volatility',
   'not found in SDS; Noack not in Section 9', review=REVIEW_YU)
_m(YU, 'base_oil_tier2', 'pour_point',
   'not found in SDS; pour point not listed in Section 9', review=REVIEW_YU)

_r(YU, 'base_oil_tier2', 'flash_point',
   'Flash point: 220 °C (COC)',
   unit='°C', value='220', vk='typical',
   meth='COC', sha='8d54d874b4bc', pg=4, vc=VC_SDS, review=REVIEW_YU)

# Tier 3
_m(YU, 'base_oil_tier3', 'sulfur',
   'not found in SDS; sulfur content not in Section 9', review=REVIEW_YU)
_m(YU, 'base_oil_tier3', 'saturates',
   'not found in SDS; saturates not in Section 9', review=REVIEW_YU)
_m(YU, 'base_oil_tier3', 'aromatics',
   'not found in SDS; aromatics not in Section 9', review=REVIEW_YU)
_m(YU, 'base_oil_tier3', 'cloud_point',
   'not found in SDS; cloud point not in Section 9', review=REVIEW_YU)
_m(YU, 'base_oil_tier3', 'wax_content',
   'not found in SDS; wax content not in Section 9', review=REVIEW_YU)


# ===========================================================================
# OCEANCHEMICAL:HC6247 — component_general (VII, solid polymer)
# ===========================================================================

_r(HC, 'component_general', 'function.primary',
   'HC6247 is a star type hydro-diene polymer ... With excellent shear stability (SSI<5), '
   'the product can meet the stringent performance requirements of top diesel and engine oils.',
   vk='text', sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC)

_m(HC, 'component_general', 'function.secondary',
   'not found; no secondary function stated; primary function is viscosity modification',
   review=REVIEW_HC)

_r(HC, 'component_general', 'chemical_family',
   'star type hydro-diene polymer',
   vk='text', sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC,
   notes='printed description; "hydro-diene polymer" = hydrogenated diene block copolymer '
         '(HSBC type); "star type" refers to star/radial polymer architecture; '
         'TDS does not state exact monomer chemistry (SBS, SIS, SEBS, etc.)')

_m(HC, 'component_general', 'active_content',
   'not found; product is a solid polymer in block/pallet form; no active content % stated; '
   'TDS disclaimer: "data is typical value, it could not be applied to the development '
   'of product specifications"',
   review=REVIEW_HC)
_m(HC, 'component_general', 'carrier.identity',
   'not found; product is a solid polymer (semi-transparent adhesive block) with no carrier',
   review=REVIEW_HC)
_m(HC, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated', review=REVIEW_HC)

_r(HC, 'component_general', 'treat_rate',
   'Testing data shows 7.30% HC6247 in a finished 0W-20 C5 gasoline engine oil formulation.',
   unit='wt%', value='7.30', vk='typical',
   sha='b9233a17f398', pg=3, vc=VC_TDS, review=REVIEW_HC,
   notes='from TESTING DATA OF HC6247 IN BASE OIL FORMULATION table (page 3): '
         '7.30% in a 0W-20 formulation with P5005 10.10%, P8201 0.30%, Yubase4 43.30%, '
         'Yubase6 39%; this is a formulation example dose, not a recommended treat range; '
         'dissolving example uses 14% dry polymer to make a liquid adhesive solution')

_r(HC, 'component_general', 'compatibility_restrictions',
   'HC6247 has good solubility in all kinds of base oils, easily soluble in solvent '
   'refined mineral oil and hydrogenation base oil, and also has good solubility in '
   'synthetic base oil.',
   vk='text', sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC,
   notes='no compatibility restrictions stated; Group I-IV solubility confirmed positively')

_m(HC, 'component_general', 'function_specific_markers.tbn',
   'not found; hydro-diene VII — TBN not stated', review=REVIEW_HC)
_m(HC, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_HC)
_m(HC, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_HC)
_m(HC, 'component_general', 'function_specific_markers.p',   'not found', review=REVIEW_HC)
_m(HC, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_HC)
_m(HC, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_HC)

# not_in_template for HC6247
_nit(HC, 'specific_gravity',
     'Specific gravity: 0.86',
     value='0.86', vk='typical',
     meth='GB/T 1033-2010',
     sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC,
     notes='of the solid polymer; no temperature stated; GB/T 1033 is CN standard for plastic density')
_nit(HC, 'shear_stability_index',
     'SSI<5 (product description); SSI (90 Cycles): 3.8 (dissolving example, 10% solution)',
     unit='%', value='3.8', qual='<', hi='5', vk='typical',
     meth='SH/T 0622 Appendix C (90 cycles)',
     sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC,
     notes='two SSI references: (1) product description states "SSI<5" as a characteristic; '
           '(2) dissolving-example table gives SSI=3.8 at 10% liquid adhesive in Yubase4 — '
           'this is a solution SSI, not a pure-product SSI')
_nit(HC, 'toluene_viscosity',
     'Toluene viscosity (25℃, 20wt%): 2200',
     value='2200', vk='typical',
     meth='GB/T 2794-2013', cond='25°C, 20 wt% in toluene',
     sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC,
     notes='solution viscosity at 20 wt% in toluene; indicator of molecular weight/architecture')
_nit(HC, 'melt_flow_index',
     'Melting index (230℃, 5kg): 20',
     value='20', vk='typical',
     meth='GB/T 3682-2000', cond='230°C, 5 kg load',
     sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC)
_nit(HC, 'volatility',
     'Volatility, wt%: 0.25',
     unit='wt%', value='0.25', vk='typical',
     meth='GB/T 24131-2018',
     sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC)
_nit(HC, 'ash_content',
     'Ash content, wt%: 0.15',
     unit='wt%', value='0.15', vk='typical',
     meth='GB/T 9345-2008',
     sha='b9233a17f398', pg=1, vc=VC_TDS, review=REVIEW_HC)


# ===========================================================================
# DOWPOL:NEOFLEX_680 — component_general (PPD)
# ===========================================================================

_r(NEO, 'component_general', 'function.primary',
   'NeoFlex 680 Pour Point Depressant is based on the Neo Synthetic Hydrocarbon chemistry. '
   'It delivers good low-temperature performance that adapts to a variety of base oils for '
   'use in automotive and industrial lubricants.',
   vk='text', sha='f4170e38995a', pg=1, vc=VC_TDS, review=REVIEW_NEO)

_m(NEO, 'component_general', 'function.secondary',
   'not found; no secondary function stated', review=REVIEW_NEO)

_r(NEO, 'component_general', 'chemical_family',
   'Neo Synthetic Hydrocarbon (proprietary)',
   vk='text', sha='f4170e38995a', pg=1, vc=VC_TDS, review=REVIEW_NEO,
   notes='chemical family from product description; "Neo Synthetic Hydrocarbon" is a '
         'proprietary/trademarked chemistry name; exact polymer type not disclosed '
         '(consistent with polyalphaolefin-based or similar synthetic hydrocarbon PPD)')

_m(NEO, 'component_general', 'active_content',
   'not found; described as a neat liquid PPD; active content % not stated',
   review=REVIEW_NEO)
_m(NEO, 'component_general', 'carrier.identity',
   'not found; product appears to be a neat liquid PPD; no carrier stated',
   review=REVIEW_NEO)
_m(NEO, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated', review=REVIEW_NEO)

_r(NEO, 'component_general', 'treat_rate',
   'Engine Oils: 0.2~0.5%; Automotive Gear Oils: 0.2~0.5%; Industry Oils: 0.1~0.3%',
   unit='wt%', lo='0.1', hi='0.5', vk='range',
   sha='f4170e38995a', pg=1, vc=VC_TDS, review=REVIEW_NEO,
   entry='various applications',
   notes='application-specific ranges stated; engine oils / gear oils 0.2-0.5%; '
         'industry oils 0.1-0.3%; overall range 0.1-0.5 wt%')

_r(NEO, 'component_general', 'compatibility_restrictions',
   'Keeps excellent efficiency with Group III and Group III+ base stocks; '
   'performance data shown in Group III/III+, Group II, and Group I base oils.',
   vk='text', sha='f4170e38995a', pg=1, vc=VC_TDS, review=REVIEW_NEO,
   notes='from TDS; performance tables on p.2 show results in Group III/III+ (SK Yubase, '
         'Shell GTL, ADNOC, S-Oil), Group II (Formosa, SinoPec, CNOOC, GS-Caltex), and '
         'Group I (PetroChina) base oils; no restrictions stated')

_m(NEO, 'component_general', 'function_specific_markers.tbn',
   'not found; PPD — TBN not applicable and not stated', review=REVIEW_NEO)
_m(NEO, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_NEO)
_m(NEO, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_NEO)
_m(NEO, 'component_general', 'function_specific_markers.p',   'not found', review=REVIEW_NEO)
_m(NEO, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_NEO)
_m(NEO, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_NEO)

# not_in_template for NEOFLEX_680
_nit(NEO, 'kv100',
     'Kinematic Viscosity @100℃, mm2/s: 18',
     unit='mm2/s', value='18', vk='typical',
     meth='ASTM D445', cond='100°C',
     sha='f4170e38995a', pg=1, vc=VC_TDS, review=REVIEW_NEO,
     notes='kv100 of neat PPD concentrate; not a formulated oil property')
_nit(NEO, 'density',
     'Density @20℃, g/cm3: 0.845',
     unit='g/cm3', value='0.845', vk='typical',
     meth='ASTM D1298', cond='20°C',
     sha='f4170e38995a', pg=1, vc=VC_TDS, review=REVIEW_NEO,
     notes='temperature 20°C (non-standard; template density fields assume 15°C or 15.6°C)')
_nit(NEO, 'flash_point',
     'Flash Point (COC), ℃: 225',
     unit='°C', value='225', vk='typical',
     meth='ASTM D92',
     sha='f4170e38995a', pg=1, vc=VC_TDS, review=REVIEW_NEO)
_nit(NEO, 'pour_point',
     'Pour Point, ℃: -21',
     unit='°C', value='-21', vk='typical',
     meth='ASTM D97',
     sha='f4170e38995a', pg=1, vc=VC_TDS, review=REVIEW_NEO,
     notes='pour point of the neat PPD product itself, not of a formulated oil')


# ===========================================================================
write_rows('s28_sk_yubase.csv', ROWS)
if __name__ == '__main__':
    print(f's28_sk_yubase: {len(ROWS)} rows written to field_evidence/s28_sk_yubase.csv')
