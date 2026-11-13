import os
os.chdir(r'C:\Users\windo\sf-wsA')


def app(path, text):
    s = open(path, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in s else '\n'
    if text.strip().splitlines()[0] in s:
        return
    if not s.endswith(nl):
        s += nl
    s += text.replace('\n', nl); open(path, 'w', encoding='utf-8', newline='').write(s)


def rep(path, old, new):
    s = open(path, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in s else '\n'
    o = old.replace('\n', nl); assert s.count(o) == 1, (path, old[:60]); s = s.replace(o, new.replace('\n', nl))
    open(path, 'w', encoding='utf-8', newline='').write(s)


# CLAUDE.md
rep('CLAUDE.md', "- A product missing any mandatory Tier 1 requirement is not formulation-eligible but stays in the database.",
    "- `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied under the requirements version (version `.3`); documented-but-unusable information is reported only in `documentation_coverage.csv`. A product missing any mandatory Tier 1 requirement is not formulation-eligible but stays in the database.")
rep('CLAUDE.md', "- Every requirement outcome has a category",
    "- A keyword mention in a document is only a lead. Evidence review: `tools/data_policy/lead_review.py` (decisions in `lead_review_decisions.json`, one rule per document group with what was read); name-match document links must be reviewed (`association_review.py`) before their evidence is used. Fill a Missing field only from exact product-specific printed evidence, declared in `source_selection.py` with its expected current state.\n- Every requirement outcome has a category")

# tools/README.md
rep('tools/README.md', "| `mandatory_properties/tests/test_requirements.py` |",
    """| `data_policy/lead_review.py` | Review of the outstanding source leads: the case set frozen at revision 2 (plus cases found during the review), extracts per page, reviewed outcomes from `lead_review_decisions.json` (rules with what was read, and the reviewed SDS comparisons) | `reports/data_policy/lead_review.csv` |
| `data_policy/association_review.py` | Identity review of the name-match document associations (verdicts in `association_review_decisions.json`; byte-identical copies detected) | `reports/data_policy/name_match_review.csv` |
| `mandatory_properties/co_component_evidence_scan.py` | Supplier statements about required (or not required) co-components in each package's cited pages | `reports/mandatory_properties/co_component_evidence.csv` |
| `mandatory_properties/tests/test_requirements.py` |""")
rep('tools/README.md', "| `data_policy/tests/test_data_policy.py` | Regression tests (26): Rule 1, comparison rules, the outputs, counts and the safety checks | nothing |",
    "| `data_policy/tests/test_data_policy.py` | Regression tests (36): Rule 1, comparison rules, the outputs and counts, the evidence review (every case reviewed, wrong associations excluded, comparisons reach the inventory, fills and corrections), protected bytes, safety | nothing |")
rep('tools/README.md', "| `mandatory_properties/tests/test_requirements.py` | Regression tests (30):",
    "| `mandatory_properties/tests/test_requirements.py` | Regression tests (31):")

# PROJECT_FILE_GUIDE.md
rep('PROJECT_FILE_GUIDE.md', "`threshold_sensitivity.csv`, `source_coverage_ledger.csv` (+ `.meta.json`) |",
    "`threshold_sensitivity.csv`, `source_coverage_ledger.csv` (+ `.meta.json`), `lead_review.csv` (every reviewed lead), `name_match_review.csv` (identity of name-matched documents) |")
rep('PROJECT_FILE_GUIDE.md', "`missing_mandatory_properties.csv` / `.md`, `treat_rate_basis_scan.csv` |",
    "`missing_mandatory_properties.csv` / `.md`, `documentation_coverage.csv` (companion, never completeness), `treat_rate_basis_scan.csv`, `co_component_evidence.csv` |")
rep('PROJECT_FILE_GUIDE.md', "| `docs/data_policy_mandatory_review/requirements_review.md`, `source_review_coverage.md` |",
    "| `docs/data_policy_mandatory_review/requirements_review.md`, `source_review_coverage.md`, `evidence_review.md` |")

# curated log
app('open_questions_and_conflicts.md', """
### Revision 3 of the 2026-11-10 review (evidence review)

- All outstanding source leads were reviewed. That is 362 product × property cases: the 352 of revision 2 plus 10 found during the review. Each case has a recorded outcome (`reports/data_policy/lead_review.csv`; summary in `docs/data_policy_mandatory_review/evidence_review.md`). A keyword mention was treated as a lead only.
- Filled from exact product-specific printed evidence:
  - CHEVRON_GROUP_II_600R KV40 (spec ≥ 100 cSt);
  - PETRONAS_ETRO_6 CCS (2,088 / 3,977 / 7,422 cP at −25 / −30 / −35 °C, from its own TDS);
  - ARAMCO_LUBEREF_PRIMA_500 KV40 96.4 cSt and CCS 14,550 / 26,000 mPa·s at −20 / −25 °C (brochure);
  - CHEVRON_SYNFLUID_MPAO_65 flash point > 266 °C (COC), with the SDS 270 °C kept as an alternate;
  - ERGON_HYGOLD_P150BS Noack 1.1 wt%;
  - EXXONMOBIL_SPECTRASYN_ULTRA_1000 specific gravity 0.855;
  - NEXBASE 3020/3043/3060/3080 specific gravity (SDS fallback).
- Corrected against the source pages: ERGON_HYGOLD_5000BS and P70N VI qualifier (the "minimum" belonged to the specification column; the typical value is 81).
- New conflicts, not resolved; the fields are pending:
  - PETRONAS_ETRO_4 KV100 / VI / CCS: PDS vs the ETRO 4 & 6 TDS;
  - LUBRIZOL_CV2301 flash point: 158 vs 165 °C in the same technical document;
  - aramcoPRIMA 110 / 230 / 500 density: spec without a unit vs brochure in Kg/L.
- Identity:
  - 174 name-match document links were reviewed, and 9 were for other products (excluded): NYNAS Base Stock 20 ↔ S 3B / NS 3; S-OIL S-8 ↔ Ultra-S sheets.
  - The FORMOSA KV100 specifications name the exact products. The FORMOSA SDSs do not name the grade, so their KV40 and specific-gravity fallbacks are now pending.
- Eligibility (version `.3`, `tier1_complete` = all mandatory requirements satisfied): 10 of 181 base oils; 0 packages; 0 components.
""")

# implementation plan
app('docs/data_policy_mandatory_review/implementation_plan.md', """
## 6. Revision 3 (2026-11-10, evidence review): additional affected files

- **Product JSON:** the fills, qualifier corrections and conflict additions in `evidence_review.md` §2:
  - CHEVRON_GROUP_II_600R, PETRONAS_ETRO_6, ARAMCO_LUBEREF_PRIMA_500, CHEVRON_SYNFLUID_MPAO_65, ERGON_HYGOLD_P150BS;
  - EXXONMOBIL_SPECTRASYN_ULTRA_1000, NESTE_NEXBASE_3020/3043/3060/3080;
  - ERGON_HYGOLD_5000BS/P70N;
  - PETRONAS_ETRO_4, LUBRIZOL_CV2301, ARAMCO_LUBEREF_PRIMA_110/230/500.
- **New tools:**
  - `tools/data_policy/lead_review.py` (+ `lead_review_decisions.json`);
  - `tools/data_policy/association_review.py` (+ `association_review_decisions.json`);
  - `tools/mandatory_properties/co_component_evidence_scan.py`.
- **New reports:**
  - `reports/data_policy/lead_review.csv`, `name_match_review.csv`;
  - `reports/mandatory_properties/documentation_coverage.csv`, `co_component_evidence.csv`.
- **Changed tools:**
  - `document_classes.py`: Lubrizol handling pages are technical; only a strong technical heading overrides inside an SDS file;
  - `source_coverage_ledger.py`: reviewed associations only;
  - `tds_sds_inventory.py`: reviewed comparisons; flash cup type required on both sides;
  - `source_selection.py`: evidence fills, list fills, qualifier fixes, conflict additions, new pending fields;
  - `requirements.py` / `build_eligibility.py`: version `.3`, restored `tier1_complete`, documentation coverage;
  - `verify_preserved.py`: reports worktree, blob and reconstructed matches separately.
- **New document:** `evidence_review.md`.
""")
print('ok')
