R = 'C:\\Users\\windo\\sf-wsA\\'
D = 'docs\\data_policy_mandatory_review\\'


def load(rel):
    return open(R + rel, encoding='utf-8').read()


def save(rel, s):
    open(R + rel, 'w', encoding='utf-8', newline='\n').write(s)


def sub(s, a, b):
    assert s.count(a) == 1, (a[:80], s.count(a))
    return s.replace(a, b)


def line(s, prefix, new):
    ls = s.split('\n')
    hit = [i for i, x in enumerate(ls) if x.startswith(prefix)]
    assert len(hit) == 1, (prefix, len(hit))
    if new is None:
        del ls[hit[0]]
    else:
        ls[hit[0]] = new
    return '\n'.join(ls)


ACCOUNT = """| Comparison status | All 114 values | The 25 ledger `external_selected` values |
|---|---:|---:|
| paired with an SDS value in the inventory | 8 | 4 |
| inapplicable: text, classification, claim or block (no numeric comparison) | 41 | 0 |
| inapplicable: the external source is itself an SDS | 11 | 0 |
| inapplicable: the SDS prints a different quantity (reviewed) | 2 | 2 |
| unavailable: no SDS document is associated with the product | 1 | 1 |
| unavailable: no SDS page mentions the property | 14 | 14 |
| unresolved: the external source could not be obtained (value not verified) | 31 | 4 |
| unresolved: numeric property outside the coverage ledger, not assessed | 6 | 0 |
| **Total** | **114** | **25** |"""

# ------------------------------------------------------------------ threshold_proposal.md
rel = D + 'threshold_proposal.md'
s = load(rel)
s = sub(s, '(141 comparison rows; 71 of them pair', '(151 comparison rows; 10 have a registered external technical source on the technical side; 71 pair')
s = sub(s, 'The pairs come from four places, duplicates merged:', 'The pairs come from five places, duplicates merged:')
s = sub(s, "each paired with the record's selected technical value.\n",
        "each paired with the record's selected technical value;\n"
        "- **(2026-11-11)** registered external technical sources. A URL in `source_registry.json` is treated like an archive document: technical, or SDS when its registry title names a safety data sheet. An unregistered URL is never paired. Each selected external technical value is also paired with every SDS value the inventory already holds for the same product and property.\n\n"
        "One URL is one source, however many saved copies of it exist, and a pair found both in `conflicts[]` and through an alternate entry is one row. If no copy of an external source could be obtained, its pairs are \"comparability unknown\" whatever the numbers. A count below is a count of document pairs: when several technical documents print the same value, each gives its own pair with the SDS.\n")
a = s.index('| Property group | Comparisons | Comparable |')
b = s.index('There are no TDS–SDS comparisons for CCS')
s = s[:a] + """| Property group | Comparisons | Comparable | Bound / range check | Comparability unknown | Not comparable |
|---|---:|---:|---:|---:|---:|
| viscosity (KV40, KV100) | 24 | 17 | 4 | 3 | 0 |
| density, specific gravity | 49 | 15 | 1 | 32 | 1 |
| flash point | 60 | 10 | 43 | 5 | 2 |
| pour point | 12 | 6 | 6 | 0 | 0 |
| viscosity index | 2 | 0 | 2 | 0 | 0 |
| Noack volatility | 1 | 1 | 0 | 0 | 0 |
| TBN | 3 | 3 | 0 | 0 | 0 |
| **Total** | **151** | **52** | **56** | **40** | **3** |

The 10 pairs with an external technical side (added 2026-11-11; the other 141 rows are unchanged):

| Product · property | External technical value | SDS value | Result |
|---|---|---|---|
| S_OIL_ARAMCO_ULTRA_8 · KV40 | 41.10 cSt at 40 °C, D445, typical (S-OIL table) | range 42.0–55.0 cSt at 40 °C, D445 (2018) | bound check: **outside the range**; retained for review. This is the existing unresolved conflict, one row |
| S_OIL_ARAMCO_ULTRA_8 · KV100 | 7.1 cSt at 100 °C, D445, typical | range 7.0–7.5 cSt at 100 °C, D445 | bound check: numerically inside the range; logically compatible, not evidence of agreement |
| S_OIL_ARAMCO_ULTRA_8 · flash point | 250 °C, COC, D92, typical | range 240–260 °C, D92 | bound check: numerically inside the range; logically compatible, not evidence of agreement |
| RICHFUL_RF6078 · density | 972 kg/m³ at 20 °C (Richful page) | 975 kg/m³ at 20 °C | comparable: 0.003 g/cm³ |
| RICHFUL_RF6066 · density (2 pairs) | 988 kg/m³ at 20 °C (Richful page) | 0.988 g/cm³ at 20 °C; 990 kg/m³, no temperature | within print rounding; comparability unknown (temperature missing) |
| RICHFUL_RF6066 · KV100 (2 pairs) | 185 mm²/s at 100 °C | 200 mm²/s; "Viscosity, dynamic: 185 mm²/s" | comparable: 8.11 %; comparability unknown (label and unit inconsistent) |
| RICHFUL_RF6066 · TBN | 108 mg KOH/g | 106 mg KOH/g | comparable: 2 mg KOH/g; no threshold proposed |
| RICHFUL_RF6069 · KV100 | 142 mm²/s at 100 °C | 142 mm²/s at 100 °C, D445 | within print rounding |

The Richful web pages for RF6066 and RF6069 are registry-verified (checked 2026-10-22) but were not re-read in the external review; the column `external_evidence` says so for each row.

""" + s[b:]
s = line(s, '| KV100 | 0.68, 1.52, 6.25, 8.11, 11.89, 20.34 % (Richful) |',
         '| KV100 | 0.68, 1.52, 6.25, 8.11, 8.11, 11.89, 20.34 % (Richful; the second 8.11 % is the RF6066 web-page value against the same SDS) | 1 %: 1 / 6 · 2–5 %◆: 2 / 5 · 7 %: 3 / 4 · 10 %: 5 / 2 |')
s = line(s, '| Density | 0.002, 0.003, 0.003 g/cm³ (Richful) |',
         '| Density | 0.002, 0.003, 0.003, 0.003 g/cm³ (Richful; the third 0.003 is the RF6078 web-page value against the same SDS) | 0.001, 0.002: 0 / 4 · 0.003: 1 / 3 · 0.005◆, 0.010: 4 / 0 |')
a = s.index('**Re-checked 2026-11-11 against the current inventory**')
b = s.index('What the sensitivity shows:')
s = s[:a] + """**Re-checked 2026-11-11 against the extended inventory** (151 rows; 52 comparable; 28 of them within print rounding). The 24 comparable pairs outside rounding are the ones in the table above (KV40 2, KV100 7, density 4, flash point 8), plus one Noack pair (ETRO 6+, 7.0 %) and two TBN pairs (RF6066, 1.85 % each), which have no proposed threshold. The external pairs added one KV100 pair above every candidate threshold up to 7 % and one density pair of 0.003 g/cm³; both repeat a difference already in the table, through a second technical source. The three aramcoULTRA 8 pairs are bound checks and enter no threshold. The conclusions below are unchanged.

""" + s[b:]
s = sub(s, '- **Density.** Any threshold above 0.003 g/cm³ puts all three pairs below it,', '- **Density.** Any threshold above 0.003 g/cm³ puts all four pairs below it,')
save(rel, s)

# ------------------------------------------------------------------ source_review_coverage.md
rel = D + 'source_review_coverage.md'
s = load(rel)
s = sub(s, '| a TDS–SDS pair exists in the inventory (comparable, unknown, bound check, not comparable) | 129 |', '| a TDS–SDS pair exists in the inventory (comparable, unknown, bound check, not comparable) | 132 |')
s = sub(s, '| not possible: only one document class, or no searchable document, mentions the property | 2,008 |', '| not possible: only one document class, or no searchable document, mentions the property | 2,005 |')
s = line(s, 'The TDS–SDS inventory (`tds_sds_comparisons.csv`) has 141 rows.',
         'The TDS–SDS inventory (`tds_sds_comparisons.csv`) has 151 rows. 71 of them come from SDS values recorded in this review (70 product × property cases; S_OIL_ULTRA_S_3 flash point has two SDSs), and 10 have a registered external technical source on the technical side (added 2026-11-11).\n\n'
         '## External selected values and their SDS comparison (`external_comparison_accounting.csv`)\n\n'
         'Counting unit: a value object whose selected source is a URL (product × field). There are 114; 29 are properties of the coverage ledger (25 `external_selected`, 4 pending). Every one has exactly one status, from `tools/data_policy/external_comparison_accounting.py`:\n\n'
         + ACCOUNT + '\n\n'
         '- **Evidence state, reported separately and never upgraded:** copy read in the external review 26; registry-verified but not re-read in the external review 57; external source not obtained 31 (the Afton HiTEC 12204L / 12250 and 8788B data sheets).\n'
         '- The 8 paired values give 10 inventory rows: aramcoULTRA 8 KV40, KV100 and flash point; RF6078 density; RF6066 density (2), KV100 (2) and TBN; RF6069 KV100.\n'
         '- "No SDS page mentions the property" is a text-layer finding over the documents associated with the product.\n'
         '- The 6 numeric values outside the ledger (RF6066 Ca and Zn, an RF6406 treat rate, HiTEC 5748 shear stability, aramcoULTRA 8 sulfur and saturates) were not assessed against an SDS; they are listed as unresolved, not as compared.')
save(rel, s)

# ------------------------------------------------------------------ evidence_review.md (new section)
rel = D + 'evidence_review.md'
s = load(rel).rstrip('\n') + """

## 11. External technical values compared with the SDS (2026-11-11)

The comparison inventory now pairs registered external technical sources with SDS values, as it does archive technical documents (`tds_sds_inventory.py`). `external_comparison_accounting.py` then accounts for every value whose selected source is a URL.

**Counting units.** Inventory: one row is one pair of a technical value and an SDS value for a product and property. Accounting: one row is one value object (product × field).

""" + ACCOUNT + """

- **Rules.** Only URLs in `source_registry.json` are paired; an external safety data sheet counts as SDS, not as technical. A value is compared only with SDS values recorded for the same product and property; nothing is inferred and no other grade is used. Unit, temperature, method, value kind, revision date and source are carried into each row; a blank revision date means none is recorded (the S-OIL page prints none).
- **No duplicates.** One URL is one source however many saved copies exist. A pair found in `conflicts[]` and through an alternate entry is one row with both origins. The aramcoULTRA 8 KV40 disagreement is one inventory row and one conflict record.
- **Unavailable evidence.** A source that could not be obtained is never verified: its values are "unresolved", and any pair with such a source would be "comparability unknown" (none exists now, because no SDS value is recorded against the Afton external values).
- **Selection and disagreement stay separate.** The inventory records relations only. It selected nothing and resolved nothing.

The three aramcoULTRA 8 comparisons:

| Property | S-OIL table (typical, edition date unknown) | SDS DL2-14611.pdf p.2 (2018-09-07) | Unit, temperature, method | Result |
|---|---|---|---|---|
| KV40 | 41.10 cSt | range 42.0–55.0 cSt | cSt, 40 °C, ASTM D445 on both sides | below the SDS range; retained for review; the existing disagreement stays unresolved |
| KV100 | 7.1 cSt | range 7.0–7.5 cSt | cSt, 100 °C, ASTM D445 on both sides | numerically inside the range; logically compatible; no measured agreement is claimed |
| Flash point | 250 °C, COC | range 240–260 °C | °C, ASTM D92 on both sides (the SDS prints the method number only) | numerically inside the range; logically compatible; no measured agreement is claimed |
"""
save(rel, s)

# ------------------------------------------------------------------ recommendation: the gap is closed
rel = D + 'recommendation_aramcoULTRA8_source_selection.md'
s = load(rel)
s = line(s, '- **Not done.**',
         '- **Comparison inventory.** The three pairs are rows of the TDS–SDS inventory since the extension of 2026-11-11 (`evidence_review.md` §11): KV40 outside the SDS range (retained for review), KV100 and flash point numerically inside the range (logically compatible, no agreement claimed).')
save(rel, s)

# ------------------------------------------------------------------ HANDOFF
rel = D + 'HANDOFF.md'
s = load(rel)
s = sub(s, 'Sensitivity re-checked on the 141-row inventory: the conclusions hold.', 'Sensitivity re-checked on the 151-row inventory (10 rows with an external technical side): the conclusions hold.')
s = sub(s, '7. **Reliable check runner**',
        '7. **External technical values compared with the SDS** ([evidence_review.md](evidence_review.md) §11). The inventory now includes registered external technical sources: 151 rows, 10 of them external. All 114 values with an external selected source are accounted for (`external_comparison_accounting.csv`): 8 paired; 54 inapplicable; 15 unavailable (no SDS document, or no SDS page prints the property); 37 unresolved (31 because the source could not be obtained, 6 numeric values outside the coverage ledger). Of the 25 ledger `external_selected` values: 4 paired, 2 inapplicable, 15 unavailable, 4 unresolved.\n8. **Reliable check runner**')
s = sub(s, '8. **Corrections found by the review.**', '9. **Corrections found by the review.**')
a = s.index('| 1–8, 10–12 | pipeline (document classes → eligibility) | 0 each | pass |')
b = s.index('- **Expected incomplete verification is not an execution failure.**')
s = s[:a] + """| 1–7, 9, 11–13 | pipeline (document classes → eligibility) | 0 each | pass |
| 8 | `external_comparison_accounting.py` | 0 | pass: 114 external-sourced values, each with one status; none unaccounted |
| 10 | `verify_soil_table.py` | 0 | pass: the three aramcoULTRA 8 cells read in both saved copies; hashes match the manifest; the record holds them |
| 14 | `build_eligibility.py --check` | 0 | pass (up to date) |
| 15 | coverage matrix | 0 | pass (validation issues 30) |
| 16 | `integrate_products.py` dry run | 0 | pass (annotations 10/10, conflict rules 16/16; **do not `--write`**) |
| 17 | `integration_diff.py --changed --against f4d97e7` | 0 | pass: 13 differences in the 2 product files changed since `43e7f8b`, all pre-existing at the baseline, 0 new |
| 18 | `verify_preserved.py` | 0 | pass (section 6) |
| 19 | protected paths vs baseline | 0 | pass (no differences) |
| 20 | product JSON valid, status vocabulary | 0 | pass (706 files) |
| 21 | `tools/mandatory_properties/tests` | 0 | 31 OK |
| 22 | `tools/data_policy/tests` | 0 | 61 OK |
| 23 | `tools/audit/review_2026-11-02/tests` (v5) | 0 | 12 OK |
| 24 | `verify_revision.py` (v5) | 1 | **expected failure (by design):** it compares with `545fd3d`, and product JSON and the workbook changed since |

""" + s[b:]
s = sub(s, 'are outcomes inside steps 6–8, which return 0.', 'are outcomes inside steps 6–9, which return 0.')
s = sub(s, 'python tools/data_policy/source_review_status.py             # source_review_status.csv\n',
        'python tools/data_policy/external_comparison_accounting.py   # every external-sourced value: paired, or why not\n'
        'python tools/data_policy/source_review_status.py             # source_review_status.csv\n')
s = sub(s, '**Not individually reviewed:** 1,783 ledger rows', '**External values not compared with an SDS** (`external_comparison_accounting.csv`): 31 values of sources that could not be obtained; 6 numeric values outside the coverage ledger, not assessed; the Richful pages for RF6066 and RF6069 are registry-verified but were not re-read in the external review.\n\n**Not individually reviewed:** 1,783 ledger rows')
save(rel, s)

# ------------------------------------------------------------------ tools/README, file guide, CLAUDE.md
rel = 'tools\\README.md'
s = load(rel)
s = sub(s, '| Regression tests (52): technical-source selection', '| Regression tests (61): external technical sources in the comparison inventory (inclusion, unavailable evidence, duplicate prevention, point versus range) and the accounting of every external-sourced value; technical-source selection')
s = sub(s, "| `data_policy/verify_soil_table.py` |", "| `data_policy/external_comparison_accounting.py` | One row per value whose selected source is a URL: paired with an SDS value in the inventory, or the reason a comparison is inapplicable, unavailable or unresolved; the evidence state is reported separately; exits 1 on an unaccounted value | `reports/data_policy/external_comparison_accounting.csv` |\n| `data_policy/verify_soil_table.py` |")
s = sub(s, "| `data_policy/tds_sds_inventory.py` | Rule 2 A-B: every TDS-SDS comparison, comparability first, differences, proposed screen |",
        "| `data_policy/tds_sds_inventory.py` | Rule 2 A-B: every TDS-SDS comparison, comparability first, differences, proposed screen; registered external (URL) technical sources are paired like archive documents, and a pair with a source that could not be obtained is never screened |")
save(rel, s)

rel = 'PROJECT_FILE_GUIDE.md'
s = load(rel)
s = sub(s, '`external_review.csv` (every external-source value),', '`external_review.csv` (every external-source value), `external_comparison_accounting.csv` (each external-sourced value: paired with an SDS value, or why not),')
save(rel, s)

rel = 'CLAUDE.md'
s = load(rel)
s = sub(s, '- Run every check with `python tools/data_policy/run_checks.py`',
        '- Whenever a technical value and an SDS value exist for the same product and property, the pair belongs in the comparison inventory, also when the technical source is a registered external URL (`tds_sds_inventory.py`). Account for every external-sourced value with `external_comparison_accounting.py` (paired, or why not). A source that could not be obtained is unresolved, never verified. The inventory never selects a source or resolves a disagreement.\n- Run every check with `python tools/data_policy/run_checks.py`')
save(rel, s)

# ------------------------------------------------------------------ changelog
rel = D + 'CHANGELOG_2026-11-10.md'
s = load(rel)
s = sub(s, '| TDS–SDS inventory rows | 141 | 141 | pair (the inventory does not pair external technical values with SDS values) |',
        '| TDS–SDS inventory rows | 141 | 141 at this step; 151 after the extension below | pair |')
s = sub(s, '`run_checks.py` has 23 steps (new: `verify_soil_table`)', '`run_checks.py` had 23 steps at this step (new: `verify_soil_table`)')
s = s.rstrip('\n') + """

## Comparison inventory extended to external technical sources (2026-11-11, uncommitted)

Instruction: check SDS values whenever applicable technical evidence also exists, including external technical evidence.

- **`tds_sds_inventory.py`.**
  - A URL registered in `source_registry.json` is paired like an archive document: technical, or SDS when its registry title names a safety data sheet. An unregistered URL is never paired.
  - Each selected external technical value is also paired with every SDS value the inventory already holds for the same product and property.
  - New columns: `tds_value_kind`, `sds_value_kind`, `tds_source`, `sds_source`, `tds_revision_date`, `sds_revision_date`, `external_evidence`.
  - A pair whose external source could not be obtained becomes "comparability unknown" and is not screened.
  - One URL is one source however many saved copies exist; a pair found in `conflicts[]` and through an alternate entry is one row.
- **New tool `external_comparison_accounting.py`** → `reports/data_policy/external_comparison_accounting.csv`: every value whose selected source is a URL, with one comparison status and a reason. Two reviewed reasons are recorded in `external_review_decisions.json` (`comparison_reviews`): Ultra-S 3 density (the SDS prints only a vapour density) and aramcoULTRA 8 density (the SDS prints a relative density).
- **No product value, requirement or threshold changed.** The data fingerprint and the eligibility result are the same as after the aramcoULTRA 8 selections (11 of 181 base oils).

Calculated counts:

| Number | Before the extension | Now | Counting unit |
|---|---:|---:|---|
| Inventory rows | 141 | 151 | pair of a technical value and an SDS value |
| Rows with an external technical side | 0 | 10 | pair |
| Comparable / bound check / comparability unknown / not comparable | 47 / 53 / 38 / 3 | 52 / 56 / 40 / 3 | pair |
| Comparable pairs within print rounding | 26 | 28 | pair |
| Bound checks: compatible / outside / not parsed | 44 / 3 / 6 | 46 / 4 / 6 | pair |
| Ledger rows with a pair | 129 | 132 | product × property |
| Values with an external selected source, accounted for | — | 114 | value object |

The 10 external pairs: aramcoULTRA 8 KV40 (outside the SDS range; the existing unresolved conflict, one row), KV100 and flash point (numerically inside the SDS range; logically compatible, no agreement claimed); RF6078 density; RF6066 density (2), KV100 (2) and TBN; RF6069 KV100. The 141 earlier rows are unchanged in every earlier column.

Accounting of the 114 values:

""" + ACCOUNT + """

- **Sensitivity** (`threshold_proposal.md` §4, re-checked): KV100 at the proposed 3 %: 2 below / 5 at or above (was 2 / 4); density at the proposed 0.005 g/cm³: 4 below / 0 (was 3 / 0). Both additions repeat a difference already present, through a second technical source. The conclusions are unchanged, and no threshold was applied.
- **Tests.** `tools/data_policy/tests` 61 (nine added in `ExternalComparisons`). `run_checks.py` has 24 steps (new: `external_comparison_accounting`).
"""
save(rel, s)
print('ok')
