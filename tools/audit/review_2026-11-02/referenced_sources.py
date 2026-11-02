"""Sources that findings name in their explanation, verification or follow-up text without a value citation, with the
reviewer's explicit verdict for each (read on 2026-11-02 unless stated). Used by verification_ledger.py.

Each entry: (finding id, reference key, source, page, verdict, basis, note). The reference keys match the patterns in
REF_PATTERNS, which verification_ledger.py uses to find every reference in the findings' texts: a reference that is
neither covered by a value citation nor listed here becomes a ledger row without a verdict (unresolved).

Verdicts: "verified" (with a basis), "unavailable" (the source could not be obtained; unresolved), "not used as
evidence" (the finding names the source only to say it was not consulted).
"""

REF_PATTERNS = {
    'api1509': r'API 1509',
    'pubchem': r'PubChem',
    'cas_common_chemistry': r'CAS Common Chemistry',
    'astm_d874': r'ASTM D874',
    'identity_review': r'identity_review',
    'readme': r'\bREADME\b',
    'internet_archive': r'Internet Archive|wayback|capture 20\d\d',
    'soil_web': r's-oil\.com|S-OIL web|S-OIL Lube Base Oil web',
    'cpchem_2012': r'cpchem\.com|Chevron Phillips data sheet|\b2012 sheet',
    'afton_0318': r'\b03/18\b',
    'afton_0421': r'\b04/21\b',
    'integration_flags': r'integrate_products',
    'adnoc_spec': r'ADNOC (?:Base Oil )?Spec',
    'richful_feed': r'richful\.com|Richful product (?:page|data feed)',
}

# value-citation files that cover a reference key (the cited source is the referenced one)
COVERED_BY_CITATION = [
    (r'petrocanadalubricants\.com', {'internet_archive'}),          # checked on the saved Internet Archive copy of the 2023.03 brochure
    (r'PetroCanada_PURITY_LUB3213E_2023-03__wayback', {'internet_archive'}),
    (r's-oil\.com', {'soil_web'}),
    (r'adnoc\.ae', {'adnoc_spec', 'internet_archive'}),            # read on the saved Internet Archive copy
    (r'Afton_HiTEC-5748_PDS_.*wayback', {'internet_archive'}),
    (r'richful\.com', {'richful_feed'}),
]

AUTO = 'automated comparison (check_columns.py)'
CTX = 'context review (text layer)'
SOIL_CAPTURE = ('SOIL_LubeBaseOil__wayback_20260610070302.html (audit_evidence)', '-', 'verified', AUTO,
                'the Internet Archive capture of 2026-06-10 holds the same Ultra-S and aramcoULTRA tables as the live page of 2026-10-30 '
                '(both parsed; the grids are equal), so the web values cited from the live page are the captured values too')

# findings whose explanation quotes a JSON final_resolution that names integrate_products.py (the PR #2 proposal kept as
# text): check_report.py compares every quoted final_resolution with the JSON conflict entry at e6617ca
FINAL_RESOLUTION_QUOTES = ['CF-003', 'CF-008', 'CF-009', 'CF-010', 'CF-011', 'CF-012', 'CF-013', 'CF-016', 'CF-017', 'CF-018', 'CF-021',
                           'CF-022', 'CF-026', 'CF-031', 'CF-032', 'CF-033', 'CF-034', 'CF-035', 'CF-036', 'CF-099', 'CF-100', 'CF-101']
FINAL_RESOLUTION = ('JSON conflicts[].final_resolution at e6617ca (the integrate_products.py proposal, kept as text)', '-', 'verified',
                    'automated comparison (check_report.py: the quoted final_resolution equals the JSON conflict entry)',
                    'the explanation quotes the final_resolution of the entry word for word; the proposal itself was not adopted')

ENTRIES = [(f'CF-{n:03d}', 'internet_archive') + SOIL_CAPTURE for n in list(range(102, 126))] +           [(i, 'integration_flags') + FINAL_RESOLUTION for i in FINAL_RESOLUTION_QUOTES] + [
    ('CF-136', 'cpchem_2012', 'CPChem_Synfluid_Dimer_C12_TDS__cpchem_2020-12.pdf (audit_evidence)', '1', 'verified', CTX,
     'Revision Date June 2012: "Pour Point, °C (°F) ASTM D5950 -53 (-63)"; KV40 8.11 cSt; Flash Point (COC) 181 (357), as the finding states'),
    ('CF-142', 'astm_d874', 'ASTM D874 (sulfated ash), sold by ASTM', '-', 'unavailable', 'not accessed',
     'named only to describe the factors in the JSON calculation note ("ASTM D874-type"); the standard was not accessed, so the label cannot be checked against it'),
    ('CF-143', 'astm_d874', 'ASTM D874 (sulfated ash), sold by ASTM', '-', 'unavailable', 'not accessed',
     'as CF-142'),
    ('CF-144', 'astm_d874', 'ASTM D874-23 (sulfated ash), sold by ASTM', '-', 'unavailable', 'not accessed',
     'the factor table and its conditions are needed to validate either factor set; not accessed (the finding is "Pending")'),
    ('CF-145', 'api1509', 'API_1509_21st_Edition_Annex_E.pdf (audit_evidence)', '1-2', 'verified', CTX,
     'E.1.3: "b. Group II ... viscosity index greater than or equal to 80 and less than 120"; "c. Group III ... viscosity index greater than or equal to 120"'),
    ('CF-146', 'api1509', 'API_1509_21st_Edition_Annex_E.pdf (audit_evidence)', '1-2', 'verified', CTX, 'E.1.3 as for CF-145'),
    ('CF-147', 'api1509', 'API_1509_21st_Edition_Annex_E.pdf (audit_evidence)', '1-2', 'verified', CTX, 'E.1.3 as for CF-145'),
    ('CF-160', 'integration_flags', 'Products_json TIANHE_P_TEC_3232 tier2 at e6617ca, fields.density', '-', 'verified', CTX,
     'value_final null; integration flag "converted density 0.001013 g/cm³ is outside 0.6-1.3, so the printed number and unit disagree; value_final left null until checked"'),
    ('CF-164', 'afton_0318', 'Afton HiTEC 5748 PDS, edition 03/18', '-', 'unavailable', 'not retrieved',
     'quoted in the open question ("a typical Shear Stability Index (SSI) of 22"); not retrieved (Internet Archive search offline on 2026-10-30); not re-tried'),
    ('CF-164', 'afton_0421', 'Afton HiTEC 5748 PDS, edition 04/21', '-', 'unavailable', 'not retrieved',
     'quoted in the open question ("Shear Stability Index %: 22"); not retrieved; not re-tried'),
    ('CF-171', 'pubchem', 'PubChem_substance_synonyms_64742-54-7.json (audit_evidence)', '-', 'verified', CTX,
     '7 substance records, all with CAS 64742-54-7; names "Distillates (petroleum), hydrotreated heavy paraffinic" (and mild/severe variants); no "light"'),
    ('CF-171', 'pubchem', 'PubChem_substance_synonyms_64742-55-8.json (audit_evidence)', '-', 'verified', CTX,
     '5 substance records, all with CAS 64742-55-8; names "Distillates (petroleum), hydrotreated light paraffinic" (and mild/severe variants)'),
    ('CF-171', 'cas_common_chemistry', 'CAS Common Chemistry', '-', 'not used as evidence', 'not consulted (API key required)',
     'named only to say it was not consulted'),
    ('CF-177', 'doc:dl2-15238.pdf', 'DL2-15238.pdf', '1-2', 'verified', CTX,
     '"Base Oil Ultra-S 8 (250 Neutral)", REVISION DATE June.10. 2015; RELATIVE DENSITY 0.847; 7.0 - 7.5 cSt @ 100℃; 42.0 - 55.0 cSt @ 40℃'),
    ('CF-177', 'doc:dl2-14611.pdf', 'DL2-14611.pdf', '1-2', 'verified', CTX,
     '"Base Oil aramcoULTRA 8 (250 Neutral)", REVISION DATE September.7. 2018; RELATIVE DENSITY 0.847; same KV ranges'),
    ('CF-177', 'soil_web', 'SOIL_LubeBaseOil_live_2026-10-30.html (audit_evidence)', '-', 'verified', AUTO,
     'the "Ultra-S" and "aramcoULTRA" typical-property tables for grades 2-8 are identical (parsed grids equal)'),
    ('CF-177', 'identity_review', 'reconciliation/identity_review.md', 'ID-01', 'verified', CTX,
     '"ID-01: Possible duplicate S-OIL JSON products (manual review)": S_OIL_ULTRA_S_8 vs S_OIL_ARAMCO_ULTRA_8'),
    ('CF-177', 'readme', 'README.md', 'Scope', 'verified', CTX, 'ID-01 listed: "whether they are one product is unresolved"'),
    ('CF-178', 'identity_review', 'reconciliation/identity_review.md', 'ID-15', 'verified', CTX,
     '"ID-15: FPCC GII 150N / 500N vs Formosa Base Oil 150N GII+ / 500N GII (unresolved)"'),
    ('CF-178', 'readme', 'README.md', 'Scope', 'verified', CTX, 'ID-15 listed with DL2-12108.jpeg p.1 and copies DL2-12109, DL2-12111'),
    ('CF-179', 'identity_review', 'reconciliation/identity_review.md', 'ID-14', 'verified', CTX,
     '"ID-14: JSON products with no supplier recorded": product.supplier null in RICHFUL_RF6071L, RICHFUL_RF6406, RICHFUL_RF6408 (and three '
     'non-Richful records); update 2026-10-24: their documents print no supplier or company name'),
    ('CF-179', 'json_suppliers', 'Products_json Richful records at e6617ca, product.supplier', '-', 'verified', CTX,
     '"Xinxiang Richful Lube Additive Co., Ltd." in 11 records, without the final period in 1 (RF6602), null in RF6071L, RF6406, RF6408'),
    ('CF-179', 'archive_names', 'Richful archive PDFs (text search)', '-', 'verified', CTX,
     'printed as "Xinxiang Richful Lube Additive Co., Ltd." (6 occurrences) and "...Co., Ltd" (3)'),
]
