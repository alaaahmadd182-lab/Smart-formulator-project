"""Supplier batch S01: Chevron Oronite (125 documents whose provisional supplier is 'Chevron Oronite').
Read: the page-1 identity card of every document (text layer, first 230-900 characters; cards.py), plus page-1 header images
of DL2-11778, 11953, 14487, 14488, 11576, 11577, 11578, 11949 (product names printed as graphics, not in the text layer).
Identity only: no property values are taken here. Documents of Oronite products filed under other provisional suppliers are
handled in their own batches; the product register merges them by product key.
Writes decisions/s01_chevron_oronite.json."""
import json, os

PKG = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUP = 'Chevron Oronite'
R = 'page-1 identity card (text layer) read'
RI = 'page-1 identity card read; page-1 header viewed as an image (name printed as graphics)'

# product key -> (name, material_class, existing record, note)
PK = {
 'OLOA 59766': ('OLOA 59766', 'additive_package', 'CHEVRON_OLOA_59766', ''),
 'OLOA 61003': ('OLOA 61003', 'additive_package', 'CHEVRON_OLOA_61003', ''),
 'OLOA 59215': ('OLOA 59215', 'additive_package', 'CHEVRON_OLOA_59215', ''),
 'OLOA 59230': ('OLOA 59230', 'additive_package', 'CHEVRON_OLOA_59230', ''),
}
NEWPKG = ['OLOA 1255C', 'OLOA 1255F', 'OLOA 1255Z', 'OLOA 2000', 'OLOA 21020A', 'OLOA 21030A', 'OLOA 26008A', 'OLOA 340R', 'OLOA 40000', 'OLOA 44502',
          'OLOA 44506', 'OLOA 44507', 'OLOA 45400', 'OLOA 45400E', 'OLOA 45401', 'OLOA 46800', 'OLOA 48021', 'OLOA 49805', 'OLOA 49815', 'OLOA 49827',
          'OLOA 49835', 'OLOA 50704', 'OLOA 54050', 'OLOA 54499', 'OLOA 54500', 'OLOA 54510', 'OLOA 54530', 'OLOA 55501', 'OLOA 55516', 'OLOA 55517',
          'OLOA 55603', 'OLOA 59094', 'OLOA 59110', 'OLOA 59112', 'OLOA 59194', 'OLOA 59211', 'OLOA 59762', 'OLOA 59767', 'OLOA 59770', 'OLOA 61005',
          'OLOA 61011', 'OLOA 65770', 'OLOA 8888', 'OLOA 9362', 'OLOA 9725AXV', 'OLOA 9725XV', 'OLOA 9999', 'OLOA 54000', 'OLOA 54013', 'OLOA 54100',
          'OLOA 54120']
for k in NEWPKG:
    PK[k] = (k, 'additive_package', '', '')
PK['OLOA 65770'] = ('OLOA 65770', 'additive_package', '', "printed 'Booster for Engine Oils' used with OLOA 59766: a package booster (route co-component of OLOA 59766)")
for k, cls, note in (('OLOA 219', 'additive_component', 'overbased calcium alkylphenate (single-function detergent)'),
                     ('OLOA 249SX', 'additive_component', 'overbased calcium sulfonate (detergent)'),
                     ('OLOA 262', 'additive_component', 'zinc dialkyldithiophosphate'),
                     ('OLOA 15500', 'additive_component', 'PIBSA ashless-dispersant INTERMEDIATE: fits the component general block; whether intermediates belong in the database is a scope question'),
                     ('OLOA 67250', 'additive_component', "printed 'Viscosity Index Improver' (linear olefin copolymer): component general + VM subtype"),
                     ('PARATONE 8059', 'additive_component', 'viscosity modifier (Paratone): component general + VM subtype')):
    PK[k] = (k, cls, '', note)
PK['GA 2536'] = ('GA 2536', 'unresolved', '', "Oronite (Gonfreville) certificate name shipped to GULF OIL MIDDLE EAST: a customer product code; its nature (package / component) is not stated on the certificates read")
PK['GA 2537'] = ('GA 2537', 'unresolved', '', 'as GA 2536 (customer product code on certificates); nature not stated')

D = {}
def d(sha, typ, prods, date='', note='', rel='product', read=R, roles=None, nxt=''):
    D[sha] = dict(doc_type=typ, supplier=SUP, products=prods, relation=rel, read=read, date=date, note=note, roles=roles or {}, next_action=nxt)

SDS, BUL, PRES, COA, FORM = 'SDS', 'product bulletin (TDS/PDS)', 'presentation / brochure', 'certificate of analysis (batch)', 'formulation / performance data'
d('c261de0920', SDS, ['OLOA 65770'], 'Revision 2, September 27, 2012', 'EU SDS (Oronite S.A.S.); product identifier printed as graphics', read=RI)
d('5e79fd273a', SDS, ['OLOA 21030A'], 'Revision 1, April 25, 2016', 'EU SDS; product identifier printed as graphics', read=RI)
for sha, date in (('a646bf4c84', 'production 01.07.2019'), ('2aca317898', 'production 29.05.2019')):
    d(sha, COA, ['GA 2537'], date, "Gonfreville certificate to GULF OIL MIDDLE EAST, 'Product Name GA 2537'")
for sha, date in (('3564d2b128', 'production 01.07.2019'), ('156a4330d4', 'production 03.10.2019'), ('950636069f', 'production 28.05.2019'),
                  ('a531af11a2', 'production 15.07.2019'), ('32f6f92bad', 'production 10.07.2019'), ('26872bfa61', 'production 12.07.2019')):
    d(sha, COA, ['GA 2536'], date, "Gonfreville certificate to GULF OIL MIDDLE EAST, 'Product Name GA 2536'")
for sha, date in (('a2265eaa1b', 'production 06.03.2020'), ('09edba814e', 'production 06.09.2019')):
    d(sha, COA, [], date, "Gonfreville certificate of analysis; the 'Product Name' field is visibly redacted / blurred on the page image. The property values resemble the GA 2537 certificates, but similar values do not establish identity",
      rel='unresolved_identity', read=RI, nxt='BLOCKER: product name not legible on the source; ask for an unredacted copy or the shipment record')
for sha, date in (('b4ac56e853', 'COA 08.07.2020'), ('e73a77650a', 'COA 07.08.2020'), ('82fd3cd8ea', 'COA 02.09.2020'), ('733cb6f194', 'COA 10.08.2020'),
                  ('0ddd4adf74', 'COA 12.08.2020'), ('2e9b8294ca', 'COA 24.08.2020'), ('783511c2c2', 'COA 27.08.2020'), ('75f16c4887', 'COA 13.08.2020')):
    d(sha, COA, ['OLOA 8888'], date, "'CERTIFICATE OF ANALYSIS OLOA 8888' bulk batch (limits min / typical / max and results)")
d('7c658e4687', PRES, ['OLOA 1255C', 'OLOA 1255F'], '© 2019', "'OLOA 1255C Low ash NGEO additive package Replacement for OLOA 1255F'", roles={'OLOA 1255F': 'replaced product (mentioned)'})
d('4d80d91201', BUL, ['OLOA 1255C'], 'Version 2, 10 January 2013')
d('a83b2997df', BUL, ['OLOA 1255Z'], 'Version 1, 2 June 2006')
d('2dc4a90c92', BUL, ['OLOA 15500'], 'Version 1, 27 Mar 2003')
d('492d078e09', BUL, ['OLOA 2000'], 'Version 3, 13 June 2013')
d('fd36ed6977', SDS, ['OLOA 2000'], 'Revision 7, February 07, 2012 (MSDS 13916)')
d('673e23e32f', PRES, ['OLOA 2000'], '© 2013', 'railroad diesel engine oil leaflet')
d('4d5df4035f', PRES, ['OLOA 21020A'], '© 2015', 'value tier TO-4 product overview')
d('b4d2aade85', BUL, ['OLOA 219'], 'Version 1, 18 April 2006')
d('b75c0992bc', BUL, ['OLOA 249SX'], 'Version 1, 18 April 2006', 'older edition')
d('c90f04819c', BUL, ['OLOA 249SX'], 'Version 2, 2 July 2013', 'newer edition')
d('78116c8e9f', BUL, ['OLOA 26008A'], 'Version 1, 11 April 2014')
d('9d8a95b804', PRES, ['OLOA 26008A'], '© 2015', 'anti-wear hydraulic oil package presentation (25 pp)')
d('b5dd1f30d3', SDS, ['OLOA 26008A'], 'Revision 5, May 15, 2013 (MSDS 25975)')
d('f10dd91658', BUL, ['OLOA 262'], 'Version 4, 1 September 2015')
d('69a1189e7c', BUL, ['OLOA 340R'], 'Version 1, 18 April 2006', 'older edition')
d('3f7b1b9dbc', SDS, ['OLOA 340R'], 'Revision 10, August 14, 2015 (MSDS 12407)')
d('5291890b3b', BUL, ['OLOA 340R'], 'Version 3, 10 January 2013', 'newer edition')
d('01d1c6fe9f', PRES, ['OLOA 40000'], '© 2013', 'railroad engine oil leaflet page')
d('e27f3b4f36', BUL, ['OLOA 44502'], 'Version 3, 10 June 2014')
d('a39dc40b17', PRES, ['OLOA 44506'], '© 2014', 'gas engine oil technology presentation (13 pp)')
d('a1c142fa02', BUL, ['OLOA 44506'], 'Version 1, 22 May 2008')
d('710e67864a', BUL, ['OLOA 44507'], 'Version 1, 11 May 2015')
d('40b2b29e11', PRES, ['OLOA 44507'], '© 2017', '37-page presentation')
d('cc446af093', PRES, ['OLOA 45400'], 'not printed on the card', 'natural gas engine oil long-drain mobile presentation (28 pp)')
d('0a01d57516', PRES, ['OLOA 45400', 'OLOA 45401'], 'October 2009', 'presentation (31 pp, 2 copies)')
d('7fac09508d', BUL, ['OLOA 45400E'], 'Version 6, 30 June 2017')
d('761d296a69', PRES, ['OLOA 45400E'], 'Dec 2015 (© 2016)', '44-page presentation')
d('aa8a21bc20', BUL, ['OLOA 45401'], 'Version 5, 7 January 2008')
d('e7caed51d4', PRES, ['OLOA 46800'], '© 2020', 'steel-piston gas engine technology (19 pp)')
d('b38e5f4342', SDS, ['OLOA 48021'], 'Revision 5, January 29, 2019 (SDS 31970)')
d('a7c01d7c41', BUL, ['OLOA 48021'], 'Version 6, 13 June 2013')
d('fe14eb5940', BUL, ['OLOA 49805'], 'Version 3, 11 June 2013')
d('dc36d20121', SDS, ['OLOA 49805'], 'Revision 9, April 08, 2019 (SDS 28531)')
d('43ec40ef01', BUL, ['OLOA 49815'], 'Version 1, 22 April 2009')
d('1cc80ae801', BUL, ['OLOA 49827'], 'Version 1, 4 June 2014')
d('e18b284143', SDS, ['OLOA 49827'], 'Revision 3, May 07, 2019 (SDS 35250)')
d('429564cefe', BUL, ['OLOA 49835'], 'Version 2, 27 November 2018')
d('ed8a69358a', SDS, ['OLOA 49835'], 'Revision 6, January 29, 2020 (SDS 48372)')
d('30817de716', SDS, ['OLOA 50704'], 'Revision 7, November 15, 2018 (SDS 27731)')
d('9632e0fe4d', BUL, ['OLOA 54050'], 'Version 5, 9 May 2012')
d('e2945c8c15', BUL, ['OLOA 54499'], 'Version 5, 18 October 2013')
d('8664613ab7', BUL, ['OLOA 54510'], 'not printed on the card')
d('8005b455b9', PRES, ['OLOA 54510', 'OLOA 54499'], 'December 2019 (v5.3)', 'PCMO mid-SAPS presentation')
d('160a84d0bc', PRES, ['OLOA 54510', 'OLOA 54500', 'OLOA 54499'], '© 2016', 'PCMO mid-SAPS presentation')
d('0ae94a35c2', BUL, ['OLOA 54530'], 'Version 4.0, 26 January 2024')
d('c479ca37e6', SDS, ['OLOA 54530'], 'Revision 18, August 08, 2024 (SDS 50817)')
d('8995ef777d', PRES, ['OLOA 55501'], '© 2017', 'ILSAC GF-5 / API SN / dexos1 presentation')
d('d7c337ce1e', BUL, ['OLOA 55516'], 'Version 10, 13 July 2018')
d('6000107708', SDS, ['OLOA 55516'], 'Revision 2, May 24, 2018 (SDS 40840)', 'older SDS edition')
d('eebbb7c408', PRES, ['OLOA 55516', 'OLOA 55517'], 'updated Oct 2017 (© 2018)', 'dexos1 Gen 2 presentation (38 pp)')
d('74e0905064', PRES, ['OLOA 55516'], 'Jan 2018', 'customer presentation (CLP), 30 pp')
d('ac1410d6ea', PRES, ['OLOA 55516'], 'April 2020', '27-page presentation')
d('7569cf2fc3', BUL, ['OLOA 55516'], 'not printed on the card')
d('668742c74a', SDS, ['OLOA 55516'], 'Revision 9, September 13, 2021 (SDS 40840)', 'newer SDS edition')
d('66d48338ea', PRES, ['OLOA 55603'], 'July 2026', 'customer deck (pptx), slides 1-8; reviewed in the existing-product comparison (slide XML)')
d('7769cf3904', BUL, ['OLOA 55603'], 'Version 4.0, 28 January 2022', "file 'PDS OLOA 55603.pdf'")
d('805620e8af', PRES, ['OLOA 59094'], '© 2018', 'CJ-4 / CK-4 / E9 presentation (21 pp)')
d('5002ee18b6', BUL, ['OLOA 59094'], 'Version 7, 9 September 2013', 'older edition')
d('ca1122023c', SDS, ['OLOA 59094'], 'Revision 12, April 05, 2018 (SDS 22907)', 'same edition as DL2-15359 (different bytes)')
d('fdc019d415', BUL, ['OLOA 59094'], 'Version 11, 3 May 2019', 'same edition as DL2-15358 (different bytes)')
d('3a53a7b6a6', PRES, ['OLOA 59094'], 'November 2018', 'presentation (10 pp)')
d('17d5581850', PRES, ['OLOA 59094', 'OLOA 59112'], 'Jan 2010', 'presentation (12 pp)')
d('ffdc28048d', PRES, ['OLOA 59094', 'OLOA 59194'], 'July 2019', 'presentation (15 pp, 2 copies)')
d('65d555681a', BUL, ['OLOA 59094'], 'Version 11, 3 May 2019')
d('8d0d8d9f04', SDS, ['OLOA 59094'], 'Revision 12, April 05, 2018 (SDS 22907)')
d('bd71b14dfc', FORM, ['OLOA 59110'], 'Nov 2013', 'API CI-4 PLUS technology presentation; same title as DL2-13683')
d('3c1d0dc8eb', FORM, ['OLOA 59110'], 'Nov 2013', 'same title as DL2-13565 (different bytes)')
d('b4c3ea0392', BUL, ['OLOA 59112'], 'Version 4, 31 January 2013')
d('bc7297cdee', BUL, ['OLOA 59211'], 'Version 2, 20 January 2010', 'older edition')
d('7a24f9b470', BUL, ['OLOA 59211'], 'Version 1, 22 May 2013', "newer date but printed 'Version 1' (edition order to be checked)")
d('2c065309b7', FORM, ['OLOA 59211'], 'not printed on the card', 'formulation table OR-F57648DL / OR-F58282DG with Chevron 220R / 600R and BPCL base oils', roles={'OLOA 59211': 'subject (recipes)'})
d('8ce1e242ae', BUL, ['OLOA 59215'], 'Version 1, 29 May 2019', 'byte duplicate of an old-archive file (existing record source)')
d('4206ab0dbe', BUL, ['OLOA 59230'], 'Version 1, 25 June 2020', 'byte duplicate of an old-archive file (existing record source)')
d('c3638d6503', SDS, ['OLOA 59766'], 'Revision 14, January 24, 2017 (SDS 23738)', 'byte duplicate of an old-archive file; reviewed in the existing-product comparison')
d('344ab666b5', BUL, ['OLOA 59766'], 'July 10, 2018')
d('86ea3c83dd', BUL, ['OLOA 59770'], 'not printed on the card')
d('afc149bd5a', PRES, ['OLOA 59770', 'OLOA 59766', 'OLOA 59767', 'OLOA 59762'], 'January 2018', 'HDEO cascade presentation (40 pp); same title as DL2-12453')
d('45cfcd1565', PRES, ['OLOA 59770', 'OLOA 59766', 'OLOA 59767', 'OLOA 59762'], 'January 2018', 'same title as DL2-12452 (different bytes)')
d('096eb8264c', BUL, ['OLOA 59770'], 'Version 1, 25 April 2008')
d('856b5d2625', SDS, ['OLOA 59770'], 'Revision 1, March 12, 2009 (MSDS 24152)')
d('2bb59c8a14', BUL, ['OLOA 61003'], 'Version 1, 8 January 2009', 'byte duplicate of an old-archive file (existing record source)')
d('61f26d91d9', BUL, ['OLOA 61005'], 'Version 4, 16 July 2012', "'For GULF' customer bulletin; name printed as graphics", read=RI)
d('985d9c8563', PRES, ['OLOA 61005'], '© 2013 (copy 27/04/2014)', 'LEDL leaflet (3 pp, 2 copies)')
d('8f2da5649b', PRES, ['OLOA 61011'], '© 2017', '33-page presentation')
d('68c9c909d2', BUL, ['OLOA 61011'], 'Version 1, 17 December 2015')
d('7b9a8cad14', BUL, ['OLOA 65770'], 'Version 1, 26 May 2008')
d('f789cb601a', BUL, ['OLOA 67250'], 'Version 4, 16 July 2012', "'For GULF' bulletin; name printed as graphics", read=RI)
d('fba06b1d22', SDS, ['OLOA 8888'], 'Revision 13, June 06, 2016 (SDS 13795)')
d('70af131135', BUL, ['OLOA 9362'], 'Version 3, 25 March 2014')
d('f1af19c86e', BUL, ['OLOA 9725AXV'], 'Version 4, 4 September 2014')
d('bfd47fc03f', BUL, ['OLOA 9725XV'], 'Version 1, 19 April 2006')
d('e912569455', PRES, ['OLOA 9999'], '© 2018', 'entry-level API package presentation')
d('d5736b35d2', BUL, ['OLOA 9999'], 'Version 15, 27 November 2010')
d('a46bfd5a56', SDS, ['PARATONE 8059'], 'Revision 6, April 29, 2019 (MSDS 21339)')
d('a259c295d0', BUL, ['OLOA 61003'], 'Version 1, 13 May 2009', "'For GULF' customer bulletin of OLOA 61003 (dosage 18.4 mass %, VII GA 2140); name printed as graphics", read=RI)
d('6fa08cb95f', BUL, ['OLOA 21030A'], 'Version 1, 17 October 2016', "'For GULF OIL INTERNATIONAL' powershift transmission fluid package; name printed as graphics", read=RI)
d('b0c45e6743', PRES, [], 'April 2018', "'API SN Plus in EAME - Oronite Point of View' (18 pp): no single subject product; reviewed in the existing-product comparison as a formulation document", rel='product',
  nxt='list the packages named inside (multi-product presentation) in the package review')
d('3426ad9871', PRES, [], '© 2013', "'Marine And Powergen System (MAPS) version 1' (47 pp, 2 copies): portfolio presentation", nxt='list the marine / power packages named inside')
d('7f37f83b6b', PRES, ['OLOA 54000', 'OLOA 54050', 'OLOA 54013'], '© 2017', 'PCMO ACEA 2016 formulation deck (59 pp); reviewed for base-oil links in batch 35')
d('ec5785a99c', PRES, ['OLOA 2000'], 'not printed on the card', 'railroad engine oil brochure (20 pp)')
d('bdd671ed4c', FORM, [], '21 Dec 2005 / 23.08.07 / 18-Jun-12', "'Finished Oil Formulations & Treat Recommendations' (19 pp): subject packages not on page 1", rel='unresolved_identity',
  nxt='read pages 2-19 to identify the packages')
d('6cd83655f4', PRES, ['OLOA 61105', 'OLOA 61106', 'OLOA 61005', 'OLOA 61107', 'OLOA 59094', 'OLOA 59211', 'OLOA 59110', 'OLOA 59770', 'OLOA 54050', 'OLOA 55501', 'OLOA 59940'],
  'December 2019', 'APAC product summary; packages read on its pages in batch 35 (name-hit pages)')
d('b91025b948', PRES, [], 'January / 25 July 2019', "'Marine And Power' MAPS presentation (33 pp)", nxt='list the marine / power packages named inside')
d('e9af129606', PRES, ['OLOA 54100', 'OLOA 54120', 'OLOA 54050', 'OLOA 54000', 'OLOA 54013'], '© 2018', 'conventional SAPS PCMO deck (47 pp); read for base-oil links in batch 34')
for k in ('OLOA 61105', 'OLOA 61106', 'OLOA 61107', 'OLOA 59940'):
    PK[k] = (k, 'additive_package', '', '')

products = {k: dict(name=v[0], supplier=SUP, material_class=v[1], existing_record=v[2], status='existing' if v[2] else ('unresolved' if v[1] == 'unresolved' else 'new_candidate'),
                    identity_evidence='printed product name on the documents linked in this batch (see document_product_links.csv)',
                    template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ VM subtype where noted)'}.get(v[1], 'not determined'),
                    notes=v[3]) for k, v in PK.items()}
assert all(p in PK for v in D.values() for p in v['products']), [p for v in D.values() for p in v['products'] if p not in PK]
out = dict(batch='S01 Chevron Oronite (identity)', reviewed_on='2026-11-14', scope='125 documents with provisional supplier Chevron Oronite',
           products={'ORONITE:' + k: v for k, v in products.items()},
           documents={s: dict(v, products=['ORONITE:' + p for p in v['products']], roles={'ORONITE:' + k: r for k, r in v['roles'].items()}) for s, v in D.items()})
json.dump(out, open(os.path.join(PKG, 'decisions', 's01_chevron_oronite.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products')
