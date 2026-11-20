"""Supplier batches S36 Elco (11), S37 Chemtura/SI Group (11), S38 Dorf Ketal (11), S39 Bettchem (11).

S36 Elco Corporation (Cleveland, Ohio; now brand of Italmatch Chemicals Group). All products are
grease additives (packages and components): Elco 301 (AW/rust inhibitor for oils and greases),
Elco 313A (slideway additive), Elco 7401/7403/8403/8715 (additive packages for lithium complex
grease), Elco 87/88 (EP/AW components for grease). DL2-12516 (41pp) is a company overview → non_product.

S37 Chemtura / SI Group. Three separate manufacturers are present:
  SI Group, Inc. (The Woodlands TX): ETHAFLOW 6705 (ashless phosphate-based AW/EP additive for
    lubricants; 2 docs: 13pp SDS + 3pp TDS) and ETHANOX 4703 (hindered phenol-amine hybrid
    antioxidant; 2pp TDS).
  Chemtura Corp. / Naugalube brand: Naugalube 16 (sulfur-containing phenolic antioxidant; 2pp TDS).
  Great Lakes Chemical / Chemtura: REOLUBE HYD 46B (fully formulated triarylphosphate fire-resistant
    hydraulic fluid, ISO HFDR; out of template).
  Hatco Corporation (mislabeled under Chemtura/SI Group): HATCOL 2938/2954 (PE/TMP polyol ester
    base stocks for high-temperature lubricants), HATCOL 3110 (synthetic diester), HATCOL 3165/3169
    (PE/DPE ester for high-temp chain lubrication), HATCOL 200 (biomedical plasticizer; out of scope).

S38 Dorf Ketal Chemicals India Pvt. Ltd. (Mumbai). Mostly fuel/gasoline additives (out of scope):
  PX 3219 (octane improver), PX 3402 (octane improver), PX 3462 (octane improver),
  SR 8208 (gasoline performance additive). Lubricant-applicable:
  PX-3841 (oligomeric non-silicone defoamant for gear oils), PX-3871 (mixed alkyl borate ester;
  dispersancy, AW/FM, dropping-point modifier for greases). DL2-14535 (product code IC:303144; product
  name not in extracted text — unresolved). DL2-15373 (contact page → non_product).

S39 Bettchem (South Africa / Middle East). All engine oil and hydraulic/transmission additive
packages: BT3088/3089/3093 existing; BT3090/3091/3095/3096/3097/3098 (engine oil packages),
BT 55006 (hydraulic AW package), BT 55050 (ATF/transmission package) — all new_candidate.

Writes decisions/s36_elco.json, s37_chemtura.json, s38_dorfketal.json, s39_bettchem.json."""
from dec_common import rows, page_text, top, doc, prod, write

# ===========================================================================
# S36 Elco
# ===========================================================================
SUP36 = 'Elco Corporation / Italmatch Chemicals Group'
MFG36 = 'Elco Corporation'
AC = 'additive_component'
OTG = 'out_of_template (grease additive package)'

ELCO = {
    # sha10: (key, name, class, doc_note)
    '511a261309': ('ELCO:ELCO_301',  'Elco 301',  AC,
                   "printed: 'Elco 301 is a multifunctional additive which imparts antiwear and rust inhibiting "
                   "properties to oil and grease formulations'; additive_component (AW/rust inhibitor); 2pp TDS"),
    'fc26ec81dc': ('ELCO:ELCO_313A', 'Elco 313A', AC,
                   "printed: 'Elco 313A is a slideway additive; benefits include Excellent stick slip, Exceptional "
                   "antiwear and EP performance, Good filterability and demulsibility'; 2pp TDS; additive_component (slideway/EP/AW)"),
    '1299ec4119': ('ELCO:ELCO_7401', 'Elco 7401', OTG,
                   "printed: 'Elco 7401 Additive Package for Grease... cost-effective package for making Lithium complex grease; "
                   "complete package containing a novel dropping point enhancer as well as EP and antiwear'; 2pp TDS; grease package → out_of_template"),
    'bc608c44c8': ('ELCO:ELCO_7403', 'Elco 7403', OTG,
                   "printed: 'Elco 7403 Additive Package for Grease... complete package containing a novel dropping point enhancer, "
                   "oxidation, rust and corrosion inhibitor'; 2pp TDS; grease package → out_of_template"),
    'e6aa2952d8': ('ELCO:ELCO_8403', 'Elco 8403', OTG,
                   "printed: 'Elco 8403 Additive Package for Grease... complete package containing EP and anti-wear agents as well as "
                   "protection from corrosion for both steel and yellow metals'; 1pp TDS; grease package → out_of_template"),
    '88450484ca': ('ELCO:ELCO_87',   'Elco 87',   AC,
                   "printed: 'Elco 87 is a partial additive package for use in blending extreme pressure industrial grease... "
                   "impart extreme pressure and antiwear to the grease'; 1pp TDS; additive_component (partial EP/AW)"),
    'f2af054872': ('ELCO:ELCO_8715', 'Elco 8715', OTG,
                   "printed: 'Elco 8715 Additive Package for Grease... complete package containing EP and anti-wear agents... "
                   "lithium soap base grease... 0.5 to 4.5 wt% treat rate'; 1pp TDS; grease package → out_of_template"),
    '6380d36231': ('ELCO:ELCO_88',   'Elco 88',   AC,
                   "printed: 'Elco 88 is a multipurpose additive... for non-soap thickened greases to improve extreme pressure, "
                   "antiwear performance, and oxidation stability'; 1pp TDS; additive_component (EP/AW/antioxidant)"),
}
D36, PK36 = {}, {}
for p10, (key, name, mc, notes) in ELCO.items():
    prod(PK36, key, name, SUP36, mc, notes)

for r in rows(lambda s: s == 'Elco', 's36_elco.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 in ELCO:
        key, name, _, note = ELCO[p10]
        doc(D36, sha, 'product data sheet (TDS/PDS)', SUP36, [key],
            'page-1 and page-2 text (product name, description, features, typical properties)',
            manufacturer=MFG36, issuer=MFG36, note=note)
    elif p10 == '254f169615':  # DL2-14899 Elco 7403 SDS (20pp)
        doc(D36, sha, 'SDS', SUP36, ['ELCO:ELCO_7403'],
            'page-1 text: GHS SDS header with product name', manufacturer=MFG36, issuer=MFG36,
            note="'GHS product identifier: Elco 7403'; Version 0.0, Date of issue 02/18/2021; 20pp GHS SDS")
    elif p10 == '46822bd09b':  # DL2-14901 Elco 8715 SDS (19pp)
        doc(D36, sha, 'SDS', SUP36, ['ELCO:ELCO_8715'],
            'page-1 text: GHS SDS header with product name', manufacturer=MFG36, issuer=MFG36,
            note="'GHS product identifier: Elco® 8715'; Version 1.1, Date of issue 07/27/2021; 19pp GHS SDS")
    elif p10 == '3ca182eab6':  # DL2-12516 company overview (41pp)
        doc(D36, sha, 'company profile (overview)', SUP36, [],
            'page-1 and page-2 text (company overview, capabilities, ISO certifications)',
            relation='non_product', issuer=MFG36,
            note="'The Elco Corporation • Continuous operations since 1927 • Headquarters Cleveland, Ohio • Certified to ISO 9001-2008, ISO 14001-2004'; "
                 "41pp company overview; no specific product TDS/SDS; not a product document")

write('s36_elco.json', 'S36 Elco (identity)', '11 documents with provisional supplier Elco', PK36, D36)

# ===========================================================================
# S37 Chemtura / SI Group
# ===========================================================================
SUP37 = 'SI Group, Inc. / Chemtura Corp.'
D37, PK37 = {}, {}

prod(PK37, 'SIGROUP:ETHAFLOW_6705', 'ETHAFLOW 6705', 'SI Group, Inc.', AC,
     "printed: 'ETHAFLOW™ 6705'; SI Group product code 001840; ashless phosphate-based antiwear/EP additive for lubricants; "
     "additive_component (AW/EP, ashless)")
prod(PK37, 'SIGROUP:ETHANOX_4703', 'ETHANOX 4703', 'SI Group, Inc.', AC,
     "printed: 'ETHANOX® 4703 Lubricant Antioxidant... unique polar molecule containing a hindered phenol structure and an aliphatic amine group; "
     "effective at high temperatures'; additive_component (antioxidant, phenol-amine hybrid)")
prod(PK37, 'CHEMTURA:NAUGALUBE_16', 'Naugalube 16', 'Chemtura Corporation / Naugalube brand', AC,
     "printed: 'Naugalube® 16 Sulfur-Containing Phenolic Antioxidant Issued: 7/2006'; "
     "additive_component (antioxidant, sulfurized phenol); Chemtura Naugalube brand (antioxidant range)")
prod(PK37, 'CHEMTURA:REOLUBE_HYD_46B', 'REOLUBE HYD 46B', 'Great Lakes Chemical / Chemtura Corp.',
     'out_of_template (fully formulated fire-resistant hydraulic fluid)',
     "printed: 'REOLUBE® HYD 46B is a fully formulated triarylphosphate fire resistant hydraulic fluid based on synthetic butylated phenol; "
     "ISO Standard 12922, ASTM D4293 for HFDR-type fire-resistant hydraulic fluids'; "
     "fully formulated finished product; not a base oil or additive raw material")

HATCO_SUP = 'Hatco Corporation'
for key, name, notes in [
    ('HATCO:HATCOL_200',  'HATCOL 200',
     "printed: 'HATCOL® 200 is a high molecular weight primary plasticizer recommended for use in blood bags, dialysis tubing, catheters, and similar bio-medical devices'; "
     "PVC biomedical plasticizer; completely outside lubricant scope; mislabeled under Chemtura/SI Group"),
    ('HATCO:HATCOL_2938', 'HATCOL 2938',
     "printed: 'HATCOL® 2938 is a pure polyol ester basestock based on trimethylolpropane; "
     "Applications: Automotive Engine Oils, Gear and Transmission Fluids, Gas Turbine Engine Oils; kV100 4.2-4.5 cSt'; "
     "TMP ester base stock; material class: unresolved (polyol ester — base fluid vs additive; template TBD); mislabeled under Chemtura/SI Group"),
    ('HATCO:HATCOL_2954', 'HATCOL 2954',
     "printed: 'HATCOL® 2954 is a pure polyol ester basestock based on pentaerythritol; "
     "Applications: Gas Turbine Engine Oils, Wide Temperature Lubricants'; "
     "PE ester base stock; material class: unresolved; mislabeled under Chemtura/SI Group"),
    ('HATCO:HATCOL_3110', 'HATCOL 3110',
     "printed: 'HATCOL® 3110 is a pure synthetic diester basestock offering both excellent lubricity and low temperature fluidity; "
     "Applications: Military Fluids & Greases, Low Temperature Lubricant Formulations'; "
     "diester base stock; material class: unresolved; mislabeled under Chemtura/SI Group"),
    ('HATCO:HATCOL_3165', 'HATCOL 3165',
     "printed: 'HATCOL® 3165 is an advanced pure polyol ester basestock based on dipentaerythritol; "
     "Applications: Conveyor Oven Chain Lubricants, High Temperature Greases'; "
     "DPE ester, high-temp chain/grease use; material class: unresolved; mislabeled under Chemtura/SI Group"),
    ('HATCO:HATCOL_3169', 'HATCOL 3169',
     "printed: 'HATCOL® 3169 is a pure polyol ester basestock based on pentaerythritol; "
     "Applications: High Temperature Greases, Chain Applications'; "
     "PE ester; material class: unresolved; mislabeled under Chemtura/SI Group"),
]:
    mc = ('out_of_scope (biomedical plasticizer)' if '200' in key
          else 'unresolved')
    prod(PK37, key, name, HATCO_SUP, mc, notes)

for r in rows(lambda s: s == 'Chemtura / SI Group', 's37_chemtura.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == '056ae14117':  # DL2-15396 ETHAFLOW 6705 SDS 13pp
        doc(D37, sha, 'SDS', 'SI Group, Inc.', ['SIGROUP:ETHAFLOW_6705'],
            'page-1 text: SDS header with product name and product code 001840',
            manufacturer='SI Group, Inc.', issuer='SI Group, Inc.',
            note="'ETHAFLOW™ 6705 Version 1.4 Issued 03/19/2021 Product code: 001840'; 13pp; EU REACH format")
    elif p10 == '358fecf67a':  # DL2-15397 ETHAFLOW 6705 TDS 3pp
        doc(D37, sha, 'product data sheet (TDS/PDS)', 'SI Group, Inc.', ['SIGROUP:ETHAFLOW_6705'],
            'page-1 text: product name, company info, typical properties table',
            manufacturer='SI Group, Inc.', issuer='SI Group, Inc.',
            note="'ETHAFLOW™ 6705 · R2 (7/22) SI Group Inc., 1790 Hughes Landing Blvd., Suite 600, The Woodlands, TX 77380'; "
                 "3pp TDS; auto-classifier misidentified as ETHANOX 4701 (page-1 text clearly shows ETHAFLOW 6705)")
    elif p10 == '1919f64448':  # DL2-15381 ETHANOX 4703 TDS 2pp
        doc(D37, sha, 'product data sheet (TDS/PDS)', 'SI Group, Inc.', ['SIGROUP:ETHANOX_4703'],
            'page-1 text: product name, description, properties',
            manufacturer='SI Group, Inc.', issuer='SI Group, Inc.',
            note="'ETHANOX® 4703 Lubricant Antioxidant DESCRIPTION: unique polar molecule containing a hindered phenol structure and an aliphatic amine group; "
                 "effective at high temperatures'; 'UT05582 (08/14) Page 1 of 2'; 2pp TDS")
    elif p10 == 'b6b41d837b':  # DL2-13771 Naugalube 16 TDS 2pp
        doc(D37, sha, 'product data sheet (TDS/PDS)', 'Chemtura Corporation / Naugalube brand',
            ['CHEMTURA:NAUGALUBE_16'],
            'page-1 text: product name and type description',
            manufacturer='Chemtura Corporation', issuer='Chemtura Corporation',
            note="'Naugalube® 16 Sulfur-Containing Phenolic Antioxidant Issued: 7/2006'; 2pp TDS")
    elif p10 == '73722d24b7':  # DL2-13681 REOLUBE HYD 46B 3pp
        doc(D37, sha, 'product data sheet (TDS/PDS)', 'Great Lakes Chemical / Chemtura Corp.',
            ['CHEMTURA:REOLUBE_HYD_46B'],
            'page-1 text: product name, type, and description',
            manufacturer='Great Lakes Chemical / Chemtura Corp.', issuer='Great Lakes Chemical / Chemtura Corp.',
            note="'REOLUBE® HYD 46B is a fully formulated triarylphosphate fire resistant hydraulic fluid'; "
                 "'Technical Information Effective: 12 January 2017'; 3pp; ISO 12922 / FM 6930 compliant; "
                 "fully formulated product, not a raw material; out_of_template")
    elif p10 == '88caf87a1f':  # DL2-12236 HATCOL 200 2pp
        doc(D37, sha, 'product data sheet (TDS/PDS)', HATCO_SUP, ['HATCO:HATCOL_200'],
            'page-1 text: product name and biomedical application description',
            manufacturer=HATCO_SUP, issuer=HATCO_SUP,
            note="'HATCOL® 200 is a high molecular weight primary plasticizer... blood bags, dialysis tubing, catheters'; "
                 "2pp; mislabeled under Chemtura/SI Group; biomedical plasticizer, out of lubricant scope")
    elif p10 in ('4098371144', 'b9e9ae9e56', '788a769d8c', 'ff76f65616', '74ba88d5d8'):
        # HATCOL ester TDS docs
        HATMAP = {
            '4098371144': ('HATCO:HATCOL_2938', 'HATCOL 2938 (TMP ester)', 'S2938C1 Rev 8: 22/2/2017'),
            'b9e9ae9e56': ('HATCO:HATCOL_2954', 'HATCOL 2954 (PE ester)', 'S1754C2 Rev 9: 27/2/2017'),
            '788a769d8c': ('HATCO:HATCOL_3169', 'HATCOL 3169 (PE ester, high-temp)', 'S3169C1 Rev 9: 6/3/2017'),
            'ff76f65616': ('HATCO:HATCOL_3110', 'HATCOL 3110 (diester)', 'S3110C1 Rev 6: 6/3/2017'),
            '74ba88d5d8': ('HATCO:HATCOL_3165', 'HATCOL 3165 (DPE ester)', 'S3165C1 Rev 1: 6/3/2017'),
        }
        key, name, rev = HATMAP[p10]
        doc(D37, sha, 'product data sheet (TDS/PDS)', HATCO_SUP, [key],
            'page-1 text: product name, ester type, applications, typical specification properties',
            manufacturer=HATCO_SUP, issuer=HATCO_SUP,
            note=f"2pp; ref {rev}; mislabeled under Chemtura/SI Group; Hatco Corporation polyol ester basestock")

write('s37_chemtura.json', 'S37 Chemtura / SI Group (identity)',
      '11 documents with provisional supplier Chemtura / SI Group', PK37, D37)

# ===========================================================================
# S38 Dorf Ketal
# ===========================================================================
SUP38 = 'Dorf Ketal Chemicals India Pvt. Ltd.'
MFG38 = SUP38
D38, PK38 = {}, {}

prod(PK38, 'DORFKETAL:PX_3841', 'PX-3841', SUP38, AC,
     "printed: 'PX 3841 is an oligomeric, non-silicone defoamant; excellent defoamant, even in low temperature applications; "
     "more soluble in oil than silicones; CAS NUMBER: 9003-49-0 95-63-6; "
     "APPLICATION: Gear Oil 0.05-0.30 %weight'; additive_component (defoamer for lubricating oils)")
prod(PK38, 'DORFKETAL:PX_3871', 'PX-3871', SUP38, AC,
     "printed: 'PX-3871 is a mixed alkyl borate ester additive; used in lubricating oils and greases to provide: "
     "Dispersancy - Friction and wear reduction - Dropping point increase in lithium based greases'; "
     "additive_component (borate ester AW/FM/dispersant)")
prod(PK38, 'DORFKETAL:PX_3219', 'PX 3219', SUP38, 'out_of_template (fuel additive)',
     "printed: 'PX 3219; Relevant identified uses: Octane Improver. Not for consumer use'; "
     "fuel octane improver — out of scope for lubricant base oil / additive database")
prod(PK38, 'DORFKETAL:PX_3402', 'PX 3402', SUP38, 'out_of_template (fuel additive)',
     "printed: 'PX 3402 OCTANE IMPROVER PRODUCT BULLETIN'; fuel octane improver — out of scope")
prod(PK38, 'DORFKETAL:PX_3462', 'PX 3462', SUP38, 'out_of_template (fuel additive)',
     "printed: 'PX 3462 OCTANE IMPROVER PRODUCT BULLETIN'; fuel octane improver — out of scope")
prod(PK38, 'DORFKETAL:SR_8208', 'SR 8208', SUP38, 'out_of_template (fuel additive)',
     "printed: 'SR 8208 Gasoline Performance Additive'; gasoline/fuel performance additive — out of scope")
prod(PK38, 'DORFKETAL:UNKNOWN_IC303144', 'Unknown product (IC:303144)', SUP38, 'unresolved',
     'product code IC:303144 printed on Product Sales Specification form (DKT/QCL/FM/001-PSS); '
     'product name not in extractable text layer; identity unresolved',
     evidence='Dorf Ketal product sales specification form; product name not visible in text layer')

for r in rows(lambda s: s == 'Dorf Ketal', 's38_dorfketal.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == 'c627e08f6c':  # DL2-12257 PX-3841 1pp TDS
        doc(D38, sha, 'product data sheet (TDS/PDS)', SUP38, ['DORFKETAL:PX_3841'],
            'page-1 text: product name, description, treat levels, CAS numbers',
            manufacturer=MFG38, issuer=MFG38,
            note="'PX-3841 LUBRICANT ADDITIVE... oligomeric, non-silicone defoamant'; 1pp TDS; CAS 9003-49-0 (polyisobutylene) + 95-63-6 (1,2,4-trimethylbenzene)")
    elif p10 == '0c6cfd4d5f':  # DL2-14626 PX-3871 1pp
        doc(D38, sha, 'product data sheet (TDS/PDS)', SUP38, ['DORFKETAL:PX_3871'],
            'page-1 text: product name, description, applications',
            manufacturer=MFG38, issuer=MFG38,
            note="'PX-3871 LUBRICANT ADDITIVE... mixed alkyl borate ester additive; Dispersancy - Friction and wear reduction - Dropping point increase in lithium greases'; 1pp TDS")
    elif p10 == '8db17b8f74':  # DL2-14538 PX 3219 SDS 9pp
        doc(D38, sha, 'SDS', SUP38, ['DORFKETAL:PX_3219'],
            'page-1 text: product name, identified use (Octane Improver)',
            manufacturer=MFG38, issuer=MFG38,
            note="'Product name: PX 3219; Relevant identified uses: Octane Improver. Not for consumer use'; "
                 "Version 1, Printing Date 21.02.2019; 9pp GHS SDS")
    elif p10 == 'ac2e34c8fa':  # DL2-14540 PX 3462 SDS 10pp (x2 copies)
        doc(D38, sha, 'SDS', SUP38, ['DORFKETAL:PX_3462'],
            'page-1 text: product name and identified use (Octane Improver)',
            manufacturer=MFG38, issuer=MFG38,
            note="'Product name: PX 3462; Relevant identified uses: Octane Improver. Not for consumer use'; "
                 "x2 copies in archive; Version 3, Printing Date 23.03.2015; 10pp GHS SDS")
    elif p10 == 'b320f949e4':  # DL2-13605 SR 8208 SDS 8pp
        doc(D38, sha, 'SDS', SUP38, ['DORFKETAL:SR_8208'],
            'page-1 text: product name and type (Gasoline Performance Additive)',
            manufacturer=MFG38, issuer=MFG38,
            note="'Product name: SR 8208; Relevant identified uses: Gasoline performance additive'; "
                 "Version 2, Printing Date 19.03.2019; 8pp GHS SDS; gasoline additive")
    elif p10 == '304d049487':  # DL2-13604 SR 8208 1pp TDS
        doc(D38, sha, 'product data sheet (TDS/PDS)', SUP38, ['DORFKETAL:SR_8208'],
            'page-1 text: product name, brief description',
            manufacturer=MFG38, issuer=MFG38,
            note="'SR 8208 Gasoline Performance Additive'; 1pp; Dorf Ketal global offices listed")
    elif p10 == '89850d970d':  # DL2-14536 PX 3402 bulletin 6pp
        doc(D38, sha, 'product bulletin', SUP38, ['DORFKETAL:PX_3402'],
            'page-1 text: product name, type (octane improver), description',
            manufacturer=MFG38, issuer=MFG38,
            note="'PX 3402 OCTANE IMPROVER PRODUCT BULLETIN'; 6pp; organometallic fuel octane improver; out_of_template")
    elif p10 == '47d45041fc':  # DL2-14537 PX 3462 bulletin 6pp
        doc(D38, sha, 'product bulletin', SUP38, ['DORFKETAL:PX_3462'],
            'page-1 text: product name, type (octane improver), description',
            manufacturer=MFG38, issuer=MFG38,
            note="'PX 3462 OCTANE IMPROVER PRODUCT BULLETIN'; 6pp; organometallic fuel octane improver; out_of_template")
    elif p10 == '24ad5c004c':  # DL2-14539 PX 3402 SDS 10pp
        doc(D38, sha, 'SDS', SUP38, ['DORFKETAL:PX_3402'],
            'page-1 text: product name, identified use (Octane Improver)',
            manufacturer=MFG38, issuer=MFG38,
            note="'Product name PX 3402; Relevant identified uses: Octane Improver'; "
                 "Revision date 21/06/2021; 10pp GHS SDS; fuel additive")
    elif p10 == '82ee230875':  # DL2-14535 IC:303144 product spec 1pp
        doc(D38, sha, 'product specification (form)', SUP38, ['DORFKETAL:UNKNOWN_IC303144'],
            'page-1 text: Dorf Ketal product sales spec form header; product code IC:303144; product name not in text',
            relation='unresolved_identity',
            manufacturer=MFG38, issuer=MFG38,
            note="'DKT/QCL/FM/001-PSS Product Sales Specification Rev # 00 20/02/2019 IC : 303144'; "
                 "product name not in extractable text layer (product data likely in a table or graphic area); 1pp",
            next_action='read full page content to identify product by IC:303144 code')
    elif p10 == 'df26ec51aa':  # DL2-15373 Dorf Ketal contact/footer page 1pp
        doc(D38, sha, 'contact page (footer/disclaimer)', SUP38, [],
            'page-1 text: Dorf Ketal global offices and contact information only',
            relation='non_product', issuer=MFG38,
            note="'Global Headquarters: Dorf Ketal Chemicals India Private Limited... Orlem, Malad (W), Mumbai-400064'; "
                 "1pp; only company contact information and standard disclaimer; no product data")

write('s38_dorfketal.json', 'S38 Dorf Ketal (identity)',
      '11 documents with provisional supplier Dorf Ketal', PK38, D38)

# ===========================================================================
# S39 Bettchem
# ===========================================================================
SUP39 = 'Bettchem'
MFG39 = SUP39
AP = 'additive_package'

EXISTING39 = {
    'EXISTING:BETTCHEM_BT_3088': ('BETTCHEM_BT_3088', 'BT3088'),
    'EXISTING:BETTCHEM_BT_3089': ('BETTCHEM_BT_3089', 'BT3089'),
    'EXISTING:BETTCHEM_BT_3093': ('BETTCHEM_BT_3093', 'BT 3093'),
}
NEW39 = {
    # sha10: (key, name, description)
    '56cce0d005': ('BETTCHEM:BT3090',  'BT3090',
                   "printed: 'BT3090 is an optimized additive package for PCMO; can meet requirements of "
                   "API SL/CF, SJ/CF and SG, JASO MA2/MB in Group II base oils at different treat rates in "
                   "appropriate viscosity modifier'; PCMO engine oil package"),
    '803ed35405': ('BETTCHEM:BT_3091', 'BT 3091',
                   "printed: 'BT 3091 MID TIER GASOLINE AND DIESEL ENGINE OIL ADDITIVE; developed to meet "
                   "customer specific needs; excellent rationalization for a wide range of mid-tier gasoline "
                   "and diesel engines oils at different treat rates'; mid-tier engine oil additive package"),
    'ed0f2209eb': ('BETTCHEM:BT_3095', 'BT 3095',
                   "printed: 'BT 3095 GASOLINE ENGINE OIL ADDITIVE PACKAGE; designed for gasoline engine oils "
                   "meeting API SP/SN performance levels when formulated in suitable base stocks'; PCMO package"),
    'cf8f2b77e4': ('BETTCHEM:BT3096',  'BT3096',
                   "printed: 'BT3096 PREMIUM DIESEL ENGINE OIL ADDITIVE PACKAGE; designed for premium heavy duty "
                   "modern diesel engine oils; protection against piston deposits, engine wear, oil oxidation'; "
                   "HDEO CI-4+ additive package"),
    'cce8367f0b': ('BETTCHEM:BT3097',  'BT3097',
                   "printed: 'BT3097 PASSENGER CAR ENGINE OIL ADDITIVE PACKAGE; can meet requirements of "
                   "API SL/CF, SJ/CF and SG, JASO MA2/MB in Group II base oils at different treat rates'; PCMO package"),
    'be9efdc919': ('BETTCHEM:BT3098',  'BT3098',
                   "printed: 'BT3098 GASOLINE AND DIESEL ENGINE OIL ADDITIVE PACKAGE; designed for specific "
                   "customer needs; outstanding rationalization for a range of gasoline and diesel engine oils'; "
                   "engine oil additive package"),
    '73145f665d': ('BETTCHEM:BT_55006', 'BT 55006',
                   "printed: 'BT 55006 HIGH ZINC ANTI-WEAR HYDRAULIC OIL ADDITIVE PACKAGE; formulated with "
                   "zinc-based antioxidant, anti-rust and anti-wear components; designed for blending anti-wear "
                   "hydraulic oils'; hydraulic AW additive package (zinc-based)"),
    '214ac88f7b': ('BETTCHEM:BT_55050', 'BT 55050',
                   "printed: 'BT 55050 MULTIFUNCTION TRANSMISSION OIL ADDITIVE PACKAGE; high quality hydraulic, "
                   "transmission & brake fluid additive package; superior protection against wear and oxidation; "
                   "blend universal ATFs, automatic transmission fluids, hydraulic transmission oils'; "
                   "ATF/transmission additive package"),
}

DUPOLD39 = {
    'b029e6a70b': 'EXISTING:BETTCHEM_BT_3088',
    'ca2e740185': 'EXISTING:BETTCHEM_BT_3089',
    '0d75064e3d': 'EXISTING:BETTCHEM_BT_3093',
}

D39, PK39 = {}, {}
for key, (rec, name) in EXISTING39.items():
    prod(PK39, key, name, SUP39, AP,
         'printed product name on the documents linked in this batch', existing=rec)
for p10, (key, name, notes) in NEW39.items():
    prod(PK39, key, name, SUP39, AP, notes)

for r in rows(lambda s: s == 'Bettchem', 's39_bettchem.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 in DUPOLD39:
        key = DUPOLD39[p10]
        dupmap = {'EXISTING:BETTCHEM_BT_3088': 'BT3088', 'EXISTING:BETTCHEM_BT_3089': 'BT3089', 'EXISTING:BETTCHEM_BT_3093': 'BT 3093'}
        name = dupmap[key]
        pages = '2' if p10 == 'be9efdc919' else '1'
        doc(D39, sha, 'product data sheet (TDS/PDS)', SUP39, [key],
            f'page-1 text (product name, type, treat rate summary)',
            manufacturer=MFG39, issuer=MFG39,
            note=f"dupOLD; '{name} additive package'; 1pp TDS")
    elif p10 in NEW39:
        key, name, _ = NEW39[p10]
        pages = '2' if p10 == 'be9efdc919' else '1'
        doc(D39, sha, 'product data sheet (TDS/PDS)', SUP39, [key],
            'page-1 text (product name, type, application, treat rate)',
            manufacturer=MFG39, issuer=MFG39,
            note=f"'{name}'; {pages}pp TDS")

write('s39_bettchem.json', 'S39 Bettchem (identity)',
      '11 documents with provisional supplier Bettchem', PK39, D39)
