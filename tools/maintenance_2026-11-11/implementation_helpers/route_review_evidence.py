"""One-off helper (2026-11-12): writes the reviewed co-component route evidence for eight packages and the reviewed
assessment of the two supplier statements. The findings below were read on the cited pages (text layer and page
renders) on 2026-11-12. The fingerprints are those of the product records as they were at the review; the helper
computes them once. Do not rerun to "refresh" fingerprints: a changed record needs a new review, not a new hash."""
import json, os, sys
R = 'C:\\Users\\windo\\sf-wsA\\'
sys.path[:0] = [R + 'tools\\mandatory_properties', R + 'tools\\data_policy']
import requirements as RQ  # noqa: E402
import policy_lib as P  # noqa: E402

prods = P.load_products()
ON = '2026-11-12'


def fields(pid):
    return next(d for d in prods[pid]['files'].values() if d.get('tier') == 1)['fields']


def b(pid, path):
    rec = RQ.record_at(fields(pid), path)
    assert rec is not None, (pid, path)
    return dict(path=path, sha256=RQ.record_fingerprint(rec))


def co(pid, *idx):
    return [b(pid, f'required_co_components[{i}]') for i in idx]


def tr(pid, *idx):
    return [b(pid, f'treat_rate_matrix[{i}]') for i in idx]


def route(pid, rid, label, conditions, f, page, quote, read, basis, required, bound, confirmed, assess, limits, unrec=()):
    return dict(product=pid, route_id=rid, label=label, conditions=conditions, source_file=f, page=page, quote=quote, read_how=read,
                reviewed_on=ON, association_basis=basis, required=required, bound_records=bound, unrecorded_requirements=list(unrec),
                requirement_list_confirmed=confirmed, list_assessment=assess, limitations=limits)


def grp(name, combination, alts, evidence):
    return dict(group=name, combination=combination, alternatives=alts, evidence=evidence)


routes = []
NOT_EXHAUSTIVE = 'The source names these components and does not state that nothing else is required; exhaustiveness is not established.'

# ---------------------------------------------------------------- INFINEUM_D3354 (DL2-10203.pdf p.1, text layer + render)
p, f = 'INFINEUM_D3354', 'DL2-10203.pdf'
VM3354 = ("Whether Infineum SV261 belongs to this row is not printed: the Description ties SV261 to the 'API CG-4/CF-4/CF/SJ, MB "
          "p228.1/3 (package approved) performance level', and footnote 1 says 'For full claims, and claims with OCP, see the technical brochure'.")
routes.append(route(p, 'D3354-row1-CI-4', 'API CI-4/CF/SL, ACEA A3/B4/E7, MB p228.3 (PA), Volvo VDS-3; SAE 15W-40',
                    "Performance table row 1, Mass %: '11.8 + 3.0 Booster(3)'; 'Equivalent to Infineum D3420 technology family'", f, 1,
                    "(3) Three boosters are available which have been tuned for different base stock qualities: Infineum D2332 at 2.8 mass%, "
                    "Infineum D2333 at 4.5 mass% and Infineum D2334 at 3.0 to 3.3 mass%.", 'text layer and page render',
                    'footnote marker (3) on the Mass % cell of row 1',
                    [grp('booster (one of three, by base stock quality)', 'one_of', co(p, 0, 1, 2), 'footnote 3: alternatives tuned for different base stock qualities')],
                    tr(p, 0), False, NOT_EXHAUSTIVE,
                    [VM3354, "The table prints '3.0 Booster' while footnote 3 gives 2.8, 4.5 and 3.0 to 3.3 mass% for the three boosters.",
                     'Which base stock quality each booster is tuned for is not printed.']))
routes.append(route(p, 'D3354-row2-VDS-2', "'As below plus Volvo VDS-2'; SAE 15W-40", "Performance table row 2, Mass %: '11.8 + 0.8 Booster(4)'", f, 1,
                    '(4) Use Infineum D2332 at 0.75 mass%, Infineum D2333 at 0.75 mass% and Infineum D2334 at 0.80 mass%.', 'text layer and page render',
                    'footnote marker (4) on the Mass % cell of row 2',
                    [grp('booster (footnote 4)', 'unresolved', co(p, 3, 4, 5),
                         "footnote 4 joins the three boosters with 'and'; the table prints one '0.8 Booster'. Whether they are alternatives or are "
                         'used together is not stated.')],
                    tr(p, 1), False, NOT_EXHAUSTIVE, [VM3354, "'As below' refers to the claims of the row beneath; the row's own claim list is not printed."]))
routes.append(route(p, 'D3354-description-SV261', 'API CG-4/CF-4/CF/SJ, MB p228.1/3 (package approved) performance level',
                    'Description, first sentence', f, 1,
                    'Infineum D3354 is a performance package designed to meet API CG-4/CF-4/CF/SJ, MB p228.1/3 (package approved) performance level with Infineum SV261.',
                    'text layer and page render', 'Description sentence; not tied to individual table rows',
                    [grp('viscosity modifier Infineum SV261', 'all', co(p, 6), "Description: 'with Infineum SV261'; no dose is printed")],
                    [], False, 'Only the viscosity modifier is named in the sentence; exhaustiveness is not established.',
                    ['Which of the five table rows without a booster this sentence covers is not printed row by row; no treat-rate entry is bound.',
                     'No dose of Infineum SV261 is printed in this document.']))

# ---------------------------------------------------------------- INFINEUM_D3384 (DL2-10218.pdf p.1, image-only: render)
p, f = 'INFINEUM_D3384', 'DL2-10218.pdf'
DESC = ('When treated at the recommended treat rate in combination with approved base stocks and viscosity modifier, Infineum D3384 can be '
        'used to formulate diesel engine oils meeting the API performance category CH-4, among others.')
VMB = "Description (document level): 'in combination with approved base stocks and viscosity modifier'; not named, no dose printed"
rows = [(0, 'API CI-4/SL; SAE 15W-40', '9.97 + Infineum D2359 at 1.93 %', 0), (1, 'API CI-4/SL, (10 TBN); SAE 15W-40', '9.97 + Infineum D2353 at 2.23 %', 1),
        (2, 'API CH-4/SJ, MB-Approval 228.1, MTU Oil Category 1, MAN 270/271; SAE 15W-40', '9.2', None),
        (3, 'API CH-4/SJ; SAE 20W-50', '9.25 + Infineum C9274 at 0.5 %', 2),
        (4, 'API CG-4/SJ, MB-Approval 228.1, MTU Oil Category 1, MAN 270/271; SAE 15W-40', '8.05 + Infineum D2358 at 0.7 %', 3),
        (5, 'API CG-4/SG, MB-Approval 228.1, MAN 270/271; SAE 15W-40', '8.05', None),
        (6, 'API CF-4/SJ, MB-Approval 228.1, MTU Oil Category 1, MAN 270/271; SAE 15W-40', '6.9 + Infineum D2358 at 1.4 %', 4),
        (7, 'API CF-4/SG; SAE 15W-40', '6.9', None), (8, 'API CH-4; SAE 10W-30', '9.25 + Infineum C9274 at 0.5 %', 2)]
for t, label, mass, boost in rows:
    req = [grp('viscosity modifier (not named)', 'all', co(p, 5), VMB)]
    if boost is not None:
        req.insert(0, grp('booster named in the row', 'all', co(p, boost), f"Mass % cell of the row: '{mass}'"))
    routes.append(route(p, f'D3384-row{t + 1}', label, f"Performance table row {t + 1}, column 'Mass %:': '{mass}'", f, 1,
                        f"Row: '{mass}'. Description: {DESC}", 'page render (the file has no text layer)',
                        'table row for the booster; document-level Description for the viscosity modifier', req, tr(p, t), False,
                        "The Description adds 'Claims are base stock and viscosity grade specific - for more information; contact your local "
                        "Infineum Representative'; exhaustiveness is not established.",
                        ['The viscosity modifier is not named and no dose is printed.',
                         "The viscosity-modifier requirement comes from the Description, which names 'API performance category CH-4, among others'; it is not repeated per row."]))

# ---------------------------------------------------------------- INFINEUM_D3451 (DL2-12029.pdf p.1, text layer + render)
p, f = 'INFINEUM_D3451', 'DL2-12029.pdf'
DESC = ('Used at the recommended treat rate of 11.9 mass% in combination with approved base stocks and viscosity modifier, Infineum D3451 '
        'provides engine oils meeting the API performance category CI-4 and can be downtreated to meet API CG-4 and CF-4.')
for t, label, mass, boost in [(0, 'API CI-4/SL, ACEA E7-12; SAE 10W-30, 15W-40, 20W-50', '11.9', None),
                              (1, 'API CH-4/SL, ACEA E7-12; SAE 10W-40', '11.9 + Infineum D2367 at 1.2 %', 0), (2, 'API CH-4; SAE 15W-40', '11.0', None)]:
    req = [grp('viscosity modifier (not named)', 'all', co(p, 1), "Description: 'in combination with approved base stocks and viscosity modifier'; not named, no dose printed")]
    if boost is not None:
        req.insert(0, grp('booster named in the row', 'all', co(p, boost), f"Mass % cell of the row: '{mass}'"))
    routes.append(route(p, f'D3451-row{t + 1}', label, f"Performance table row {t + 1}, column 'Mass %:': '{mass}'", f, 1,
                        f"Row: '{mass}'. Description: {DESC}", 'text layer and page render',
                        'table row for the booster; Description for the viscosity modifier', req, tr(p, t), False,
                        "The Description adds 'Claims are base stock and viscosity grade specific'; exhaustiveness is not established.",
                        ['The viscosity modifier is not named and no dose is printed.']
                        + (["The Description states the viscosity modifier for the 11.9 mass% treat rate; this row is at 11.0."] if t == 2 else [])))

# ---------------------------------------------------------------- LUBRIZOL_3589C (DL2-10629.pdf p.1, text layer)
p, f = 'LUBRIZOL_3589C', 'DL2-10629.pdf'
routes.append(route(p, '3589C-6.15', 'ACEA E2-96 Issue 5 (2007), API CF, API CF-2, API SF, MB-Approval 228.0, MAN 270, MTU Type 1, ZF TE-ML 04B (monograde lubricants)',
                    "'Recommended for use at: 6.15 % by weight'", f, 1,
                    'When formulated with appropriate base oils, the lubricant meets the following performance specifications:', 'text layer',
                    'application block', [], tr(p, 0), False,
                    'The block names only base oils. It does not state that no co-component is required, so nothing is concluded about other components.',
                    ["No co-component is named for this block; that is not a 'none required' statement."]))
routes.append(route(p, '3589C-Kolomna', 'Kolomna M-14D2 approval', "Footnote 2: package at 6.2 % by weight plus a booster", f, 1,
                    '2) Product approved by Kolomna railroad at 6.2 % by weight plus a 0.8 % by weight booster.', 'text layer',
                    'footnote 2, which names the Kolomna approval',
                    [grp('booster (not named)', 'all', co(p, 0), 'footnote 2')], [], False, NOT_EXHAUSTIVE,
                    ['The booster is not named in the document.',
                     'The footnote gives the package at 6.2 % by weight for this approval; the record holds one treat-rate entry at 6.15 % that lists Kolomna M-14D2, so no treat-rate entry is bound.']))

# ---------------------------------------------------------------- LUBRIZOL_3700 and 3700D (p.1, text layer + render)
for p, f, hi, lo in (('LUBRIZOL_3700', 'DL2-10632.pdf', '8.5', '7.7'), ('LUBRIZOL_3700D', 'DL2-10633.pdf', '8', '7.25')):
    tag = p.split('_')[1]
    FOOT = '1) Addition of a 0.25 % by weight TBN booster required to claim MTU Type 1'
    VMQ = 'When formulated with appropriate base oils and viscosity modifier, the lubricant meets the following performance specifications:'
    unrec = [dict(component='viscosity modifier (not named)', quote=VMQ, dose='not printed',
                  proposed_correction='add a required_co_components entry for the viscosity modifier of this block, with its dose Missing')]
    MARK = ("The footnote is numbered '1)' but no claim carries a marker on the page; it is tied to this block only through the claim name "
            "'MTU Type 1', which both application blocks list.")
    routes.append(route(p, f'{tag}-{hi}pct', f'first application block ({hi} % by weight), claims other than MTU Type 1', f"'Recommended for use at: {hi} % by weight'", f, 1,
                        VMQ, 'text layer and page render', 'application block', [], tr(p, 0), False, NOT_EXHAUSTIVE,
                        ['The viscosity modifier is not named and no dose is printed.'], unrec))
    routes.append(route(p, f'{tag}-{hi}pct-MTU-Type-1', f'first application block ({hi} % by weight), MTU Type 1 claim', f"'Recommended for use at: {hi} % by weight'; footnote 1", f, 1,
                        f'{VMQ} / {FOOT}', 'text layer and page render', "application block; footnote 1 by the claim name 'MTU Type 1'",
                        [grp('TBN booster (not named)', 'all', co(p, 0), 'footnote 1')], tr(p, 0), False, NOT_EXHAUSTIVE,
                        ['The viscosity modifier is not named and no dose is printed.', 'The TBN booster is not named.', MARK], unrec))
    routes.append(route(p, f'{tag}-{lo}pct', f'second application block ({lo} % by weight), claims other than MTU Type 1', f"'Recommended for use at: {lo} % by weight'", f, 1,
                        'When formulated with appropriate base oils, the lubricant meets the following performance specifications:', 'text layer and page render',
                        'application block', [], tr(p, 1), False,
                        'The block names only base oils. It does not state that no co-component is required, so nothing is concluded about other components.',
                        ["No co-component is named for this block; that is not a 'none required' statement."]))
    routes.append(route(p, f'{tag}-{lo}pct-MTU-Type-1', f'second application block ({lo} % by weight), MTU Type 1 claim', f"'Recommended for use at: {lo} % by weight'; footnote 1", f, 1,
                        f'When formulated with appropriate base oils, the lubricant meets the following performance specifications: / {FOOT}',
                        'text layer and page render', "application block; footnote 1 by the claim name 'MTU Type 1'",
                        [grp('TBN booster (not named)', 'all', co(p, 0), 'footnote 1')], tr(p, 1), False, NOT_EXHAUSTIVE,
                        ['The TBN booster is not named.', MARK]))

# ---------------------------------------------------------------- LUBRIZOL_CV1100 (DL2-11503.pdf p.1, text layer)
p, f = 'LUBRIZOL_CV1100', 'DL2-11503.pdf'
routes.append(route(p, 'CV1100-CK-4', 'API CK-4 and the other claims of the first block; SAE 15W-40 and 10W-30', "'Recommended for use at: 14.2 % by weight' (first block)", f, 1,
                    'When blended with appropriate base oils and viscosity modifier, the formulated lubricant meets the following performance specifications as SAE 15W-40 and 10W-30 viscosity grade :',
                    'text layer', 'application block',
                    [grp('viscosity modifier (not named)', 'all', co(p, 1), "block sentence: 'appropriate base oils and viscosity modifier'; no dose printed")],
                    tr(p, 0), False, NOT_EXHAUSTIVE,
                    ['The viscosity modifier is not named and no dose is printed.', "'API CK-4 / SN claim limited to SAE 15W-40 viscosity grade in select Group II base oils.'"]))
routes.append(route(p, 'CV1100-FA-4', 'API FA-4, Cummins CES 20087, Detroit Diesel DFS93K223; SAE 10W-30', "'Recommended for use at: 14.2 % by weight' (second block)", f, 1,
                    'When 2.0wt% CV6320 is top treated in addition to 14.2wt% CV1100 and blended with appropriate base oils and viscosity modifier, the formulated lubricant meets the following performance specifications as SAE 10W-30 viscosity grade :',
                    'text layer', 'application block',
                    [grp('top-treat booster LUBRIZOL CV6320', 'all', co(p, 0), "block sentence: '2.0wt% CV6320'"),
                     grp('viscosity modifier (not named)', 'all', co(p, 1), "block sentence: 'appropriate base oils and viscosity modifier'; no dose printed")],
                    tr(p, 1), False, NOT_EXHAUSTIVE, ['The viscosity modifier is not named and no dose is printed.']))

# ---------------------------------------------------------------- LUBRIZOL_CV1103 (DL2-14978.pdf pp.1-2, text layer + render)
p, f = 'LUBRIZOL_CV1103', 'DL2-14978.pdf'
STAR = ('p.2: * All Lubrizol product performance claims are only applicable when the additive package is used with defined base oil(s), '
        'viscosity modifier(s) and other required components to produce the applicable viscosity grade in a properly blended finished fluid.')
COL = ("Both table columns are headed '14.30% by weight' and carry no other label. The second column marks only API FA-4, Cummins CES 20087 and "
       "Detroit Diesel DDC 93K223, which are the claims of the CV6320 sentence; the first column also marks API FA-4 'L'. Which column is the "
       'CV6320 route is not printed.')
LIST = "The footnote on p.2 refers to 'other required components' beyond base oils and viscosity modifiers, so the list is expressly not exhaustive."
routes.append(route(p, 'CV1103-column1', 'first table column (14.30% by weight): API CK-4 and the other marked claims', "Product Performance table, first column", f, 1,
                    f'Formulated and approved in combination with Lubrizol® 7077 performance polymer / {STAR}', 'text layer and page render',
                    "'Features and benefits' bullet and the table footnote; the column itself names no co-component",
                    [grp('performance polymer Lubrizol 7077 (viscosity modifier)', 'all', co(p, 1), "'Formulated and approved in combination with Lubrizol 7077 performance polymer'; no dose printed")],
                    tr(p, 0), False, LIST, ['No dose of the Lubrizol 7077 performance polymer is printed.', COL]))
routes.append(route(p, 'CV1103-FA-4', 'API FA-4; SAE 10W-30', 'opening sentence of p.1 (repeated on p.2)', f, 1,
                    'When 2.0wt% CV6320 is top treated in addition to 14.3wt% CV1103 and blended with appropriate base oils and performance polymer, '
                    f'Lubrizol 7077 series, the formulated lubricant meets API FA-4 specification as an SAE 10W-30 viscosity grade / {STAR}',
                    'text layer and page render', 'opening sentence',
                    [grp('top-treat booster LUBRIZOL CV6320', 'all', co(p, 0), "sentence: '2.0wt% CV6320'"),
                     grp('performance polymer Lubrizol 7077 series (viscosity modifier)', 'all', co(p, 1), "sentence: 'performance polymer, Lubrizol 7077 series'; no dose printed")],
                    tr(p, 1), False, LIST, ['No dose of the Lubrizol 7077 performance polymer is printed.', COL]))

doc = {
    "description": ("Reviewed evidence of co-component ROUTES (policy 2 of 2026-11-11; schema of 2026-11-12). A route is a supplier-evidenced way "
                    "of using the package (a claim, grade or application block) with the co-components that route requires. Each entry gives the "
                    "conditions and quote as printed, how the page was read, the basis of the association, the required groups (combination "
                    "'all', 'one_of' for supplier-stated alternatives, or 'unresolved' where the source does not say), the requirements the "
                    "source states that the record does not hold (unrecorded_requirements), whether the requirement list is confirmed complete, "
                    "and the limitations. Every record a route relies on is bound by the SHA-256 fingerprint of the complete record "
                    "(requirements.record_fingerprint): if a bound record changes, the route is stale until it is reviewed again. No route is "
                    "derived from the role text of a record, and no list is treated as exhaustive because it names some components."),
    "review_status": ("Reviewed 2026-11-12: INFINEUM_D3354, D3384, D3451; LUBRIZOL_3589C, 3700, 3700D, CV1100, CV1103 (cited datasheet pages; "
                      "text layer, and page renders where the association needed it; DL2-10218.pdf is image-only and was read on its render). "
                      "No other package has been reviewed. No requirement list could be confirmed complete."),
    "proposed_record_corrections": [
        {"product": "LUBRIZOL_3700", "proposal": "The first application block (8.5 % by weight) requires a viscosity modifier ('appropriate base oils and viscosity modifier'); the record holds no viscosity-modifier requirement. Add one with its dose Missing.", "source": "DL2-10632.pdf p.1"},
        {"product": "LUBRIZOL_3700D", "proposal": "The first application block (8 % by weight) requires a viscosity modifier; the record holds no viscosity-modifier requirement. Add one with its dose Missing.", "source": "DL2-10633.pdf p.1"},
        {"product": "LUBRIZOL_3589C", "proposal": "Footnote 2 gives the Kolomna approval at 6.2 % by weight plus a 0.8 % booster; the record lists Kolomna M-14D2 under the single 6.15 % treat-rate entry. Consider a separate treat-rate entry for the Kolomna approval at 6.2 % by weight.", "source": "DL2-10629.pdf p.1"},
        {"product": "INFINEUM_D3354", "proposal": "Record with the row-1 boosters that the table prints '3.0 Booster' while footnote 3 gives 2.8 / 4.5 / 3.0 to 3.3 mass%, and that footnote 4 does not say whether its three boosters are alternatives. No value change is proposed.", "source": "DL2-10203.pdf p.1"},
        {"product": "LUBRIZOL_CV1103", "proposal": "Record that the table footnote on p.2 refers to 'other required components', and that the two table columns are not labelled. No value change is proposed.", "source": "DL2-14978.pdf pp.1-2"}],
    "routes": routes}
open(R + 'tools\\mandatory_properties\\co_component_route_evidence.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')

sp = R + 'tools\\mandatory_properties\\co_component_statements.json'
d = json.load(open(sp, encoding='utf-8'))
d['description'] = ("Reviewed supplier statements about co-component requirements. quote: the supplier wording exactly as printed. review: the "
                    "explicit reviewed assessment that requirements.explicit_none_required needs: reviewed_on, meaning, unconditional (true/false), "
                    "qualification_verbatim (the supplier's qualification as printed; '' only if unconditional), scope (component_types and routes: "
                    "'all' or a list) and conditions_verbatim. A statement makes the product-level requirement met only if it is for this product, "
                    "its reviewed meaning is 'no_co_component_required', it is unconditional, and it covers all component types and all routes. "
                    "A missing field proves nothing. An empty record is never recorded here as supplier silence.")
for x in d['statements']:
    x.pop('qualification', None)
    x['review'] = dict(reviewed_on=ON, meaning='no_supplemental_ppd_expected', unconditional=False, qualification_verbatim='should be needed',
                       scope=dict(component_types=['pour point depressant (PPD)'], routes=['the API CK-4 and API FA-4 grades listed with the statement']),
                       conditions_verbatim='to meet low temperature properties',
                       note="The supplier says the package already contains a PPD 'so no supplemental PPD should be needed'. This is a qualified "
                            "expectation about one component type. It says nothing about a viscosity modifier, which the same page names.")
open(sp, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print(len(routes), 'routes written')
