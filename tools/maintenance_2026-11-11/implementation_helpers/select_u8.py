import json, re
R = 'C:\\Users\\windo\\sf-wsA\\'


def load(rel):
    return open(R + rel, encoding='utf-8').read()


def save(rel, s):
    open(R + rel, 'w', encoding='utf-8', newline='\n').write(s)


def sub(s, a, b):
    assert s.count(a) == 1, (a[:70], s.count(a))
    return s.replace(a, b)


# ------------------------------------------------------------------ source_selection.py
p = 'tools\\data_policy\\source_selection.py'
s = load(p)
NEW = '''
# aramcoULTRA 8 (decision of 2026-11-11): the applicable technical-source value is selected; the archived SDS range is
# kept as an alternate, and the disagreement with the SDS is recorded and assessed separately (it is not a veto).
# Values confirmed on both saved copies of the manufacturer table by verify_soil_table.py.
SOIL_URL = 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx'
SOIL_NOTE = ("Selected 2026-11-11 under the source-selection policy (technical source first). S-OIL 'Lube Base Oil' web page, table "
             "'Typical Properties of aramcoULTRA Base Oil', column 'aramcoULTRA 8', row '{row}', ASTM cell '{astm}'. Read on the two "
             "saved copies in reconciliation/audit_evidence/: SOIL_LubeBaseOil__wayback_20260610070302.html (Internet Archive capture "
             "2026-06-10, SHA-256 cff0d3bbb7964c7450a1b9fa813617bf76e4b09de39187d026f674c7604fda60) and SOIL_LubeBaseOil_live_2026-10-30.html (live page retrieved 2026-10-30, SHA-256 "
             "94b263ad23cfd8b9631b5b637635c0cbdb341aad25cb7553a2a44513f10f011c); both print the same cell. The page prints no publication or revision date: its edition date is unknown, "
             "and a capture or retrieval date is not an edition date. The archived SDS DL2-14611.pdf (2018-09-07) prints {sds}; it is "
             "kept as an alternate entry. {rel}")
for _path, _file, _row, _astm, _printed, _val, _unit, _temp, _method, _sds, _rel, _extra in [
        ('kv40', 'S_OIL_ARAMCO_ULTRA_8_tier1.json', 'Kinematic Viscosity @ 40℃, cSt', 'D445', '41.10', 41.1, 'cSt', 40, 'ASTM D445',
         'the range 42.0 - 55.0 cSt @ 40 °C (ASTM D 445)',
         'The typical value lies below that range: the disagreement is the unresolved conflict already in conflicts[] (2026-10 audit); '
         'selecting the technical value does not resolve it and does not judge the SDS wrong.', {}),
        ('kv100', 'S_OIL_ARAMCO_ULTRA_8_tier1.json', 'Kinematic Viscosity @ 100℃, cSt', 'D445', '7.1', 7.1, 'cSt', 100, 'ASTM D445',
         'the range 7.0 - 7.5 cSt @ 100 °C (ASTM D 445)',
         'The typical value lies inside that range: logically compatible, which is not evidence of agreement (the kind of the SDS range '
         'is not stated).', {}),
        ('flash_point', 'S_OIL_ARAMCO_ULTRA_8_tier2.json', 'Flash Point,COC ,℃', 'D92', '250', 250, '°C', None, 'ASTM D92',
         'the range 240 ~ 260 °C (ASTM D 92)',
         'The typical value lies inside that range: logically compatible, which is not evidence of agreement (the kind of the SDS range '
         'is not stated; the SDS prints the method number only, the page also prints COC).', dict(flash_method='COC'))]:
    CHANGES.append(dict(
        product='S_OIL_ARAMCO_ULTRA_8', file=_file, path=_path, expect=dict(value=None, source='DL2-14611.pdf'),
        change_label='external technical source selected (manufacturer table, typical; edition date unknown); SDS range kept as alternate',
        new=dict(value=_val, qualifier=None, min=None, max=None, value_kind='typical', printed_text=f'{_row}: {_printed}', unit=_unit,
                 test_temperature_c=_temp, method=_method, source=dict(file=SOIL_URL, page=None, revision_date=None),
                 calculation_note=SOIL_NOTE.format(row=_row, astm=_astm, sds=_sds, rel=_rel), **_extra),
        old_kind=None,
        evidence=f"S-OIL page (saved copies, hashes verified): 'Typical Properties of aramcoULTRA Base Oil' | {_row} | {_astm} | aramcoULTRA 8: {_printed}"))

for _pid, _file, _src_file, _pg, _rev, _printed, _val, _rng in ['''
s = sub(s, "\nfor _pid, _file, _src_file, _pg, _rev, _printed, _val, _rng in [", NEW)
# pending entry removed
ls = s.split('\n')
hit = [i for i, x in enumerate(ls) if x.startswith("    ('S_OIL_ARAMCO_ULTRA_8', 'kv40, kv100, flash_point',")]
assert len(hit) == 1
del ls[hit[0]]
s = '\n'.join(ls)
# conflict note: the selection is recorded, the conflict stays unresolved
s = sub(s, "NOTE_APPENDS = [  # (product, file, conflict field, text appended to the conflict note)\n",
        "NOTE_APPENDS = [  # (product, file, conflict field, text appended to the conflict note)\n"
        "    ('S_OIL_ARAMCO_ULTRA_8', 'S_OIL_ARAMCO_ULTRA_8_tier1.json', 'tier1.kv40',\n"
        "     ' [2026-11-11 source-selection policy: the field now holds the S-OIL table typical 41.10 cSt (technical source first; edition date '\n"
        "     'of the page unknown); the SDS range 42.0 - 55.0 cSt is kept as an alternate entry. The typical lies below the SDS range, so the '\n"
        "     'documents still disagree. Not resolved.]'),\n")
save(p, s)

# ------------------------------------------------------------------ external review decisions: the three cases are now selected values
p = 'tools\\data_policy\\external_review_decisions.json'
d = json.loads(load(p))
EXP = {'kv40': {'value': 41.1, 'unit': 'cSt', 'test_temperature_c': 40, 'method': 'ASTM D445', 'value_kind': 'typical'},
       'kv100': {'value': 7.1, 'unit': 'cSt', 'test_temperature_c': 100, 'method': 'ASTM D445', 'value_kind': 'typical'},
       'flash_point': {'value': 250, 'unit': '°C', 'method': 'ASTM D92', 'value_kind': 'typical'}}
n = 0
for c in d['cases']:
    if c['product'] == 'S_OIL_ARAMCO_ULTRA_8' and c['kind'] == 'pending_external_alternative':
        n += 1
        c['kind'] = 'external_selected'
        c['expect'] = EXP[c['property']]
        c['change'] = 'selected 2026-11-11 (technical source first); SDS range kept as alternate'
        c['sds'] = c['sds'].replace('selected SDS DL2-14611.pdf', 'alternate (previously selected) SDS DL2-14611.pdf')
        c['applicability'] = c['applicability'].replace('typical value on an undated manufacturer page', 'typical value on a manufacturer page whose edition date is unknown (none printed)')
        c['reason'] = {
            'kv40': 'Confirmed as printed on both saved copies and selected as the applicable technical-source value. The disagreement with the SDS range is recorded separately (existing unresolved conflict) and is not a selection veto.',
            'kv100': 'Confirmed as printed on both saved copies and selected as the applicable technical-source value. Same unit, temperature and method as the SDS; the typical lies inside the SDS range (logically compatible, not agreement).',
            'flash_point': 'Confirmed as printed on both saved copies and selected as the applicable technical-source value. Same unit and method number as the SDS; the typical lies inside the SDS range (logically compatible, not agreement).'}[c['property']]
assert n == 3
for c in d['cases']:
    if c['product'] == 'S_OIL_ARAMCO_ULTRA_8':
        c['applicability'] = c['applicability'].replace('typical value on an undated manufacturer page', 'typical value on a manufacturer page whose edition date is unknown (none printed)')
d['description'] = d['description'].replace(
    "and for every pending field whose open question is an external technical source (review of 2026-11-11)",
    "and for every pending field whose open question is an external technical source (review of 2026-11-11; the three aramcoULTRA 8 "
    "fields reviewed as pending alternatives were selected on 2026-11-11 and are external_selected cases now)")
save(p, json.dumps(d, ensure_ascii=False, indent=1) + '\n')

# ------------------------------------------------------------------ run_checks: new step, stale result files removed
p = 'tools\\data_policy\\run_checks.py'
s = load(p)
s = sub(s, "    ('source_review_status', ['tools/data_policy/source_review_status.py'], 'zero', None),\n",
        "    ('source_review_status', ['tools/data_policy/source_review_status.py'], 'zero', None),\n"
        "    ('verify_soil_table', ['tools/data_policy/verify_soil_table.py'], 'zero', None),\n")
s = sub(s, "    os.makedirs(a.out_dir, exist_ok=True)\n",
        "    os.makedirs(a.out_dir, exist_ok=True)\n"
        "    for old in os.listdir(a.out_dir):  # step files of an earlier run (the numbering changes when a step is added)\n"
        "        if re.fullmatch(r'\\d\\d_[a-z0-9_]+\\.txt', old):\n"
        "            os.remove(os.path.join(a.out_dir, old))\n")
save(p, s)
print('ok')
