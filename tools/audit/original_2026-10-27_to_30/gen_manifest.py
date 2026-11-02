"""Write reconciliation/audit_evidence/evidence_manifest.md (hashes computed from the saved files)."""
import base64, hashlib, json, os, sys, zipfile
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

EV = os.path.join(A.REPO, 'reconciliation', 'audit_evidence')
F = json.load(open(os.path.join(A.SCR, 'audit', 'findings_v3.json'), encoding='utf-8'))
ids = lambda pred: ', '.join(f['id'] for f in F if pred(f)) or '–'
pc = ids(lambda f: 'LUB3213E/IM-1809E' in f['verification'] or 'IM-1809E' in json.dumps(f['values'], ensure_ascii=False))
soil = ids(lambda f: 'S-OIL web table' in f['verification'] or (f['record_id'] == 'S_OIL_ULTRA_S_8' and f['property'] == 'product identity'))
ITEMS = [
    ('PetroCanada_PURITY_LUB3213E_2023-03__wayback_20251215051152.pdf',
     'https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx',
     'Internet Archive capture 2025-12-15 05:11:52 (id_ original bytes): https://web.archive.org/web/20251215051152id_/https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx',
     'Petro-Canada PURITY™ Base Oils, LUB3213E / IM-1809E (2023.03); PDF created 2024-03-08', 'p.2 (typical-properties tables, grades L35–L65 and 1003–2305)',
     'Direct download refused (HTTP 429). Same Internet Archive digest for the official URL (captures 2025-12-15, 2026-01-15) and for the mascherpa.it mirror cited in the records (capture 2025-12-20; direct download HTTP 403), so the file is byte-identical to the copy the records were based on.', pc),
    ('SOIL_LubeBaseOil_live_2026-10-30.html', 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx', 'live page', 'S-OIL "Lube Base Oil" web page (undated)',
     'aramcoULTRA and Ultra-S typical-property tables (grades 2, 3, 4, 6, 8)', 'The two tables print identical values.', soil),
    ('SOIL_LubeBaseOil__wayback_20260610070302.html', 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx',
     'Internet Archive capture 2026-06-10 07:03:02: https://web.archive.org/web/20260610070302id_/https://www.s-oil.com/en/energy/LubeBaseOil.aspx',
     'S-OIL "Lube Base Oil" web page', 'Ultra-S typical-property table', 'Table values identical to the live page, covering the registry check of 2026-10-22.', soil),
    ('API_1509_21st_Edition_Annex_E.pdf', 'https://www.api.org/-/media/Files/Certification/Engine-Oil-Diesel/Publications/API%201509-%2021st%20Edition%20Annex%20E.pdf',
     'live download', 'API 1509, 21st edition, Annex E (API Base Oil Interchangeability Guidelines)', 'E.1.3 Base stock categories (pp.1–2 of the PDF)',
     'Group I/II/III definitions (saturates, sulfur, VI) used for the API group findings.', ids(lambda f: f['category'] == 'C06' and 'api_group' in f['property'])),
    ('CPChem_Synfluid_Dimer_C12_TDS__cpchem_2020-12.pdf', 'https://www.cpchem.com/sites/default/files/2020-12/Dimer%20C12.pdf', 'live download',
     'Chevron Phillips Chemical, Synfluid® Dimer C12 typical properties, revision date June 2012', 'p.1 (Pour Point, °C (°F), ASTM D5950: -53 (-63))',
     'Manufacturer sheet with the header in °C (°F) order.', ids(lambda f: f['record_id'] == 'CHEVRON_SYNFLUID_DIMER_C12')),
    ('ADNOC_BaseOil_Spec_GroupII_GroupIII__wayback_20220815185412.pdf',
     'https://www.adnoc.ae/-/media/adnoc-v2/files/our-products/adnoc-base-oil-spec-group-ii--group-iii.ashx?hash=E8C7E60F6ED980EDDDB910B5EB2375E21F42336C&la=en',
     'Internet Archive capture 2022-08-15 18:54:12 (live URL refused, HTTP 403)', 'ADNOC Base Oil Specifications (Group II and Group III), last update August 2020',
     'PDF p.3: ADBASE 3CST (GROUP II), spec no. 8230, VI min 100', 'Registered in source_registry.json (verified 2026-10-22).', ids(lambda f: f['record_id'] == 'ADNOC_ADBASE_3CST' and 'api_group' in f['property'])),
    ('PubChem_substance_synonyms_64742-54-7.json', 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/64742-54-7/synonyms/JSON', 'live (NIH PubChem PUG-REST)',
     'PubChem substance synonyms for CAS 64742-54-7', '7 substance records', 'All "hydrotreated heavy paraffinic"; none "light". CAS Common Chemistry needs an API key (HTTP 401).', ids(lambda f: f['record_id'] == 'S_OIL_ULTRA_S_4' and 'CAS' in f['property'])),
    ('PubChem_substance_synonyms_64742-55-8.json', 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/64742-55-8/synonyms/JSON', 'live (NIH PubChem PUG-REST)',
     'PubChem substance synonyms for CAS 64742-55-8', '5 substance records', '"hydrotreated light paraffinic" belongs to this number.', ids(lambda f: f['record_id'] == 'S_OIL_ULTRA_S_4' and 'CAS' in f['property'])),
    ('Afton_HiTEC-5748_PDS_05-23__wayback_20241005085229.pdf', 'https://www.aftonchemical.com/getmedia/c378c7f9-8667-452e-be0f-d6882b2bff45/HiTEC-5748_PDS_3.pdf?ext=.pdf',
     'Internet Archive capture 2024-10-05 08:52:29 (registered in source_registry.json)', 'Afton HiTEC® 5748 PDS, edition 05/23', 'p.2 (Shear Stability Index %: 22)', '', ids(lambda f: f['record_id'] == 'AFTON_HITEC_5748' and 'SSI' in f['property'])),
    ('Afton_HiTEC-5748_PDS_07-11__wayback_20120503020512.pdf', 'http://www.aftonchemical.com/ProductDataSheets/Engine%20Oil/HiTEC-5748_PDS.pdf',
     'Internet Archive capture 2012-05-03 02:05:12', 'Afton HiTEC® 5748 PDS, edition 07/11', 'text "It is based on 23 SSI polymer"', 'Editions 03/18 and 04/21 not retrieved (Internet Archive search temporarily offline on 2026-10-30).', ids(lambda f: f['record_id'] == 'AFTON_HITEC_5748' and 'SSI' in f['property'])),
    ('Richful_productId105__api_2026-10-30.json', 'https://www.richful.com/rfapi/api/product/getproductbyid?productId=105', 'live (Richful product data feed)',
     'Richful product 105, RF6602 polymethacrylate VII (no revision date)', 'storage text: short term ≤ 60 ℃, long term ≤ 45 ℃', 'Product page https://www.richful.com/catalogueDetail.html?id=105.', ids(lambda f: f['record_id'] == 'RF6602' and 'storage' in f['property'])),
]
ARCHIVE_VISUAL = [('DL2-13731.pdf', 'p.7', 'Shell Risella X 430 SDS (encoded font), revision 13.01.2020'), ('DL2-15831.pdf', 'p.5', 'Richful RF6066 SDS, revision 9/2/2021'),
                  ('DL2-15619.pdf', 'p.5', 'Richful RF6069 SDS, revision 1/4/2022'), ('DL2-15833.pdf', 'p.5', 'Richful RF6078 SDS, revision 9/2/2021'),
                  ('DL2-11503.pdf', 'p.1–2', 'Lubrizol CV1100 product data sheet'), ('DL2-11773.pdf', 'p.1', 'aramcoPRIMA brochure, Group II table (image-only)'),
                  ('DL2-10217.pdf', 'p.1', 'Infineum D3375, version 10 March 2015 (image-only)'), ('DL2-12108.jpeg', '–', 'FPCC API GII base-oil specification table (image)'),
                  ('DL2-15568.pdf', 'p.2', 'Afton HiTEC 12210M bulletin 04/22 (claims table)')]


def h(path):
    b = open(path, 'rb').read(); return len(b), hashlib.sha256(b).hexdigest(), base64.b32encode(hashlib.sha1(b).digest()).decode()


L = ['# Audit evidence manifest', '',
     'Copies of external sources consulted in the conflicts-audit review of 2026-10-30 (`../comprehensive_conflicts_audit.md`). '
     'All files were retrieved on 2026-10-30. They are evidence copies only: no product JSON, template, coverage workbook or the curated log cites '
     'them, and nothing in the database was changed. SHA-1 is given in base 32 (the form the Internet Archive uses for its digests).', '',
     '## External documents saved in this folder', '',
     '| File | Source URL | Retrieval | Document and edition | Pages / part used | Size (bytes) | SHA-256 | SHA-1 (base 32) | Notes | Findings supported |',
     '|---|---|---|---|---|---|---|---|---|---|']
for fn, url, how, ed, pages, note, fids in ITEMS:
    n, s256, s1 = h(os.path.join(EV, fn))
    L.append(f'| `{fn}` | {url} | {how} | {ed} | {pages} | {n} | `{s256}` | `{s1}` | {note} | {fids} |')
L += ['', '## Archive documents checked visually (not copied; inside `Manual + Data to share.zip`)', '',
      '| Archive member | Pages viewed | Document | SHA-256 of the member |', '|---|---|---|---|']
z = zipfile.ZipFile(os.path.join(A.REPO, 'Manual + Data to share.zip')); names = {n.rsplit('/', 1)[-1]: n for n in z.namelist()}
for fn, pg, ed in ARCHIVE_VISUAL:
    L.append(f'| `{names[fn]}` | {pg} | {ed} | `{hashlib.sha256(z.read(names[fn])).hexdigest()}` |')
L += ['', '## Sources that could not be accessed', '',
      '- ASTM D874-23 (sulfated-ash factors): sold by ASTM; not accessed. Finding CF-144 stays pending.',
      '- CAS Common Chemistry record for 64742-54-7: API key required (HTTP 401); PubChem used instead.',
      '- Afton HiTEC 5748 PDS editions 03/18 and 04/21: Internet Archive search temporarily offline on 2026-10-30.',
      '- aramcoPRIMA 70 SDS flash-point method: not printed in the archived SDS; no other edition found.', '']
open(os.path.join(EV, 'evidence_manifest.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('manifest rows', len(ITEMS), '+', len(ARCHIVE_VISUAL), '| files in folder', sorted(os.listdir(EV)))
