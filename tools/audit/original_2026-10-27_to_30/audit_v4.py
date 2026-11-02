"""Version-4 reporting corrections (2026-10-30, second pass): classification split, follow-up categories, CF-144 wording.
Reads audit/findings_v3.json, writes audit/findings_v4.json and audit/corrections_v4.json. Nothing is resolved here."""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

F = json.load(open(os.path.join(A.SCR, 'audit', 'findings_v3.json'), encoding='utf-8'))
BY = {f['id']: f for f in F}
LOG = []


def change(f, field, new, why):
    if f.get(field) != new:
        LOG.append(dict(id=f['id'], record_id=f['record_id'], field=field, old=f.get(field), new=new, reason=why)); f[field] = new


CONF, POT = 'Confirmed contradiction', 'Potential contradiction (comparability uncertain)'
unc = lambda f: f['comparability'].startswith(('Uncertain', 'Partly uncertain'))
for f in F:
    if f['group'] == 'Genuine contradiction':
        change(f, 'group', POT if unc(f) else CONF, 'Contradiction records split into confirmed and potential (comparability uncertain); evidence and uncertainty notes unchanged.')

for f in F:
    if f['nature'].startswith('Genuine contradiction'):
        lead = 'Confirmed contradiction' if f['group'] == CONF else 'Potential contradiction (comparability uncertain)' if f['group'] == POT else None
        if lead:
            change(f, 'nature', lead + f['nature'][len('Genuine contradiction'):], 'Description aligned with the confirmed/potential split.')

# ---- follow-up categories (finding-specific reasons)
SUP, POL, FIX, STD, DEC, NONE = ('Supplier clarification', 'Edition-selection policy', 'Correctable from existing evidence (data owner)',
                                 'Standard or further source needed', 'Data-owner decision (field-selection rule)', 'No follow-up needed beyond documentation')


def docs(f):
    out = []
    for v in f['values']:
        x = str(v.get('file') or '')
        x = 'S-OIL web table' if 's-oil.com' in x else 'LUB3213E 2023.03' if ('IM-1809E' in str(v.get('doc_type')) or 'LUB3213E_2023' in x) else x.split(' (')[0]
        if x and x not in out: out.append(x)
    return ' and '.join(out[:3]) or 'the documents cited'


SPECIFIC = {
    'CF-025': (SUP, 'One supplier data sheet (DL2-10414) prints a density (0.854 g/cm³) and a specific gravity (0.9183) at the same temperature that cannot both be right; the documents cannot show which entry is in error.'),
    'CF-165': (SUP, 'The same bulletin footnote (DL2-14639 p.2) states 14.2 % = 10.3 % + 4.2 %; only the supplier can say which number is intended.'),
    'CF-171': (SUP, 'The SDS line pairs the name of one substance with the CAS number of another; only the supplier can state which identifier is correct.'),
    'CF-146': (SUP, 'The specification heading (Group II) and its VI minimum (76) are inconsistent with the API 1509 Group II definition; the grade-level group can only come from the supplier.'),
    'CF-162': (SUP, 'TDS (75 ℃) and product page (60 ℃) state different short-term storage limits for the same condition; neither is dated relative to the other.'),
    'CF-163': (SUP, 'The two undated TDS state different blending limits (60 vs 65 ℃); the documents give no basis to choose.'),
    'CF-014': (SUP, 'TDS 998 kg/m³ at 20 °C vs SDS 0.991 g/cm³ at 15 °C cannot both hold (direction opposite to thermal expansion); the 2026-10-18 user decision selects a working value but does not explain the disagreement.'),
    'CF-009': (SUP, 'The two undated TDS print 227 and 185 mm²/s at 100 °C (both D445); the 2021 SDS value is printed on its "Viscosity, dynamic" line, so its comparability is uncertain; dating of the TDS and the SDS label need the supplier.'),
    'CF-019': (SUP, 'The SDS prints "Relative density : 0.958 g/cm3@20℃"; whether this is a density or a relative density is needed before comparing it with the TDS 963 kg/m³.'),
    'CF-036': (SUP, 'The TDS prints no measurement temperature for 0.8429 kg/L; the temperature is needed before comparing it with the SDS value at 15 °C.'),
    'CF-102': (SUP, 'The SDS prints "42.0 - 55.0 cSt" without stating whether it is a specification or a typical band; that basis is needed before comparing it with the web typical 41.10.'),
    'CF-126': (SUP, 'Neither SDS prints a flash-point method; the method is needed before comparing 255 °C with the TDS open-cup 265 °C.'),
    'CF-140': (SUP, 'The SDS prints no flash-point method anywhere; the method is needed before comparing 168 °C with the specification minimum of 175 °C (COC).'),
    'CF-161': (SUP, 'The SDS prints no flash-point method; the method is needed before comparing 160 °C with the TDS open-cup values.'),
    'CF-147': (SUP, 'The Group III label is a family/refinery statement; a grade-level classification for VHVI 2 (VI 100) is needed.'),
    'CF-133': (STD, 'A dated edition of the family table DL2-13200, or the test methods behind the December 2008 TDS values, is needed to establish comparability (the family table uses ASTM D7042 for viscosity).'),
    'CF-134': (STD, 'A dated edition of the family table DL2-13200, or the test methods behind the December 2008 TDS values, is needed to establish comparability (the family table uses ASTM D7042 for viscosity).'),
    'CF-135': (STD, 'A dated edition of the family table DL2-13200, or the test methods behind the December 2008 TDS values, is needed to establish comparability (the family table uses ASTM D7042 for viscosity).'),
    'CF-168': (STD, 'The brochure marks these typicals "subject to confirmation upon startup of the new Group II plant", and DL2-12172 prints no unit; a later brochure edition would show whether the difference persists.'),
    'CF-169': (STD, 'The brochure marks these typicals "subject to confirmation upon startup of the new Group II plant", and DL2-12172 prints no unit; a later brochure edition would show whether the difference persists.'),
    'CF-170': (SUP, 'Both documents print a typical density at 15 °C by D4052 (0.867 vs 0.8720) and neither is dated relative to the other.'),
    'CF-172': (STD, 'The catalog (0.843) and the Cosan sheet (0.840) are undated; dating them would show whether this is an edition change. The SDS relative-density basis is not stated.'),
    'CF-024': (SUP, 'The same number 1.3 is printed in ppm (typical, DL2-13944) and in WT% (maximum, DL2-12173); neither document shows which unit is intended.'),
    'CF-136': (FIX, 'The manufacturer\'s own sheet (Chevron Phillips, June 2012) prints "Pour Point, °C (°F) -53 (-63)"; the stored -63 °C can be reviewed against this evidence by the data owner.'),
    'CF-142': (FIX, 'The cited product data sheet prints a typical sulfated ash of 7 (% weight); the data owner can decide whether to record this printed value beside the estimate.'),
    'CF-143': (FIX, 'The cited product data sheet prints a typical sulfated ash of 10 (% weight); the data owner can decide whether to record this printed value beside the estimate.'),
    'CF-144': (STD, 'The applicable ASTM D874 provisions (factor table and its conditions) must be consulted before the calculation method is harmonised; the data owner then applies one documented rule.'),
    'CF-157': (FIX, 'The source wording ("110 min." in a table marked "Not a specification") is fully visible; the data owner can choose how to label it (value_kind, qualifier) and note the ambiguity.'),
    'CF-158': (FIX, 'The source wording ("110 Minimum" in a table marked "Not a specification") is fully visible; the data owner can choose how to label it (value_kind, qualifier) and note the ambiguity.'),
    'CF-159': (FIX, 'Annotate the RF6066 KV100 conflict with the SDS label/unit mismatch; no new value is needed.'),
    'CF-160': (SUP, 'The data sheet prints "kg/m3" with 1.0130; the archive holds no second density for this product to show which part is misprinted.'),
    'CF-173': (FIX, 'The label "Specific gravity" and the magnitude 0,8299 are printed; the data owner can record the printed unit "g/m3" as printed with a note. Supplier clarification only if the unit itself is needed.'),
    'CF-174': (FIX, 'The label "Specific gravity" and the magnitude 0,8338 are printed; the data owner can record the printed unit "g/m3" as printed with a note. Supplier clarification only if the unit itself is needed.'),
    'CF-175': (FIX, 'The label "Specific gravity" and the magnitude 0,8363 are printed; the data owner can record the printed unit "g/m3" as printed with a note. Supplier clarification only if the unit itself is needed.'),
    'CF-176': (FIX, 'The label "Specific gravity" and the magnitude 0,8423 are printed; the data owner can record the printed unit "g/m3" as printed with a note. Supplier clarification only if the unit itself is needed.'),
    'CF-177': (SUP, 'No document states whether Ultra-S 8 and aramcoULTRA 8 designate one product (the web tables and SDS ranges are identical, which is suggestive only).'),
    'CF-178': (SUP, 'No document states whether the FPCC GII 150N/500N columns are the FORMOSA_150N_GII_PLUS and FORMOSA_500N_GII products.'),
    'CF-179': (FIX, 'The printed name "Xinxiang Richful Lube Additive Co." is available; the spelling can be aligned, and the three null suppliers stay null because their documents print no name.'),
    'CF-180': (FIX, 'Both PDFs show the note is correct; the kept PR #2 proposal text can be annotated as checked and incorrect.'),
    'CF-164': (SUP, 'No edition prints the SSI test method, cycle count or base oil; only the supplier can establish comparability (two further editions also remain to be retrieved).'),
    'CF-145': (NONE, 'Explained by the manufacturer specification (VI minimum 100, Group II); an optional low-priority check of the current typical VI.'),
}
for f in F:
    fid = f['id']
    if fid in SPECIFIC:
        cat, why = SPECIFIC[fid]
    elif f['resolution'] == 'Not a value conflict':
        cat, why = NONE, 'Not a disagreement (claims added or removed between bulletin editions, or a measurement-temperature note).'
    elif f['group'] == 'Edition difference':
        cat = POL
        why = (f'Values differ between editions of the same supplier document series ({docs(f)}); a documented rule for which edition supplies the working value is needed. '
               'Supplier contact is not required unless the older value must be confirmed as obsolete.')
        if f['recorded_decision'].startswith('Working value: newer dated edition'):
            why = 'A working value from the newer dated edition is already recorded; the edition-selection rule behind it should be documented. ' + why.split('; ', 1)[1]
    elif f['group'] == CONF:
        undated = 'undated' in (f['explanation'] + f['comparability'] + json.dumps(f['values'], ensure_ascii=False)).lower()
        cat = SUP
        why = (f'{docs(f)} print incompatible values under comparable conditions'
               + ('; at least one document is undated, so the documents give no basis to choose' if undated else '; the documents give no documented basis (method, edition or date) to choose')
               + '.')
        if f['recorded_decision'].startswith('User decision'):
            why += ' The 2026-10-18 user decision selects a working value but does not explain the disagreement.'
    elif f['group'] == 'Explainable difference':
        if f['category'] == 'C05' and f['record_id'].startswith('RICHFUL_') and 'flash' in f['property']:
            cat, why = DEC, 'Values are compatible (SDS lower bound vs TDS typical); the data owner should choose one rule for which value the field holds across the Richful records.'
        else:
            cat, why = NONE, 'The documents themselves state the difference in method, condition, unit or bound type; both values stay documented.'
    else:
        raise SystemExit(f'no follow-up rule for {fid} {f["record_id"]} {f["group"]}')
    change(f, 'follow_up_category', cat, 'Task 3: replaces the blanket "settled only by suppliers" statement with finding-specific follow-up.')
    change(f, 'follow_up_reason', why, 'Task 3.')
    old_out = f.get('outstanding_action', '')
    if old_out == 'Supplier confirmation (not contacted in this audit)' or (old_out.startswith('Supplier') and cat != SUP):
        change(f, 'outstanding_action', '' if cat != SUP else 'Supplier clarification (not contacted in this audit)', 'Task 3: aligned with the follow-up category.')

# ---- CF-144 and the related estimated-ash findings
f = BY['CF-144']
change(f, 'nature', 'Inconsistent calculation method across records: two zinc factors are used to estimate sulfated ash', 'Task 4.')
change(f, 'explanation', ('The 26 Calculated sulfated-ash values are estimates derived from element contents, not measured sulfated ash (ASTM D874 measures the residue after '
                          'ignition and sulfation). Their calculation notes cite "ASTM D874" factors but use two different zinc factors: 1.24 for Zn with Ca/Mg/Zn only '
                          'in 25 records, and 1.5 for Zn plus Mo (1.5) and B (3.22) terms in MINGLAN_T3161A. This shows that the calculation method is inconsistent '
                          'across records. It does not by itself establish which factor, or which estimate, is wrong. Where a product document prints its own sulfated '
                          'ash (CF-142, CF-143), the estimate and the printed value differ.'), 'Task 4.')
change(f, 'verification', ('Pending: the inconsistency in the JSON calculation notes is confirmed (JSON-only). Validation of either factor set against the applicable '
                           'ASTM D874-23 provisions has not been done: the standard is sold by ASTM and was not accessed.'), 'Task 4.')
change(f, 'verification_priority', 'High: consult the applicable ASTM D874-23 provisions before harmonising the calculation; affects all 26 estimated values.', 'Task 4.')
change(f, 'next_step', 'Obtain ASTM D874-23; then the data owner documents one calculation rule and labels all values as estimates. No value is changed by this audit.', 'Task 4.')
for fid, est, prt in (('CF-142', '5.8', '7'), ('CF-143', '9.2', '10')):
    f = BY[fid]
    change(f, 'nature', 'Estimated value used although the cited product document prints a typical value; the two differ', 'Task 4: estimated vs printed ash distinguished.')
    change(f, 'explanation', (f'The JSON field is an estimate ({est} wt.%, status Calculated) from element contents with ASTM D874-type factors (see CF-144). The product data sheet '
                              f'cited by this record prints a typical sulfated ash of {prt} (column heading "% Weight"; no test method printed for that row). An estimate and a '
                              'printed typical value are different kinds of value; the difference does not show which is correct.'), 'Task 4.')

json.dump(F, open(os.path.join(A.SCR, 'audit', 'findings_v4.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
json.dump(LOG, open(os.path.join(A.SCR, 'audit', 'corrections_v4.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
C = collections.Counter
print('types', C(f['group'] for f in F))
print('follow-up', C(f['follow_up_category'] for f in F))
print('follow-up x type', sorted(C((f['group'], f['follow_up_category']) for f in F).items()))
print('changes', len(LOG), C(x['field'] for x in LOG))
