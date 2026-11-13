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


app('open_questions_and_conflicts.md', """
### Revision 2 of the 2026-11-10 review (provisional checkpoint)

- FORMOSA_150N_GII_PLUS and FORMOSA_500N_GII (tier 1) `kv100`: the technical specification range is now selected as printed (DL2-10001.pdf / DL2-10003.pdf p.1, issued 2009-10-21: 5.0–5.4 and 10–12 mm²/s). The SDS typical values (5.2 and 11 cSt) are kept as alternates with their own SDS lines. The earlier record had mixed the specification range into the SDS entry; it is corrected. No single value is derived from the range.
- NEXBASE 3043–3080: the family TDS DL2-10962.pdf (Edition 8) and the individual sheets disagree on 15 fields (densities, and some KV40, KV100, VI, pour point, flash point and Noack values). These fields stay pending: conflicting undated technical editions.
- ERGON_HYGOLD_5000BS and ERGON_HYGOLD_P70N `viscosity_index`: the record puts `qualifier: "minimum"` on the value 81, which its own notes call the typical value. A correction (qualifier to null) is proposed, not applied.
- Eligibility (provisional rules, version `mandatory-tier1-2026-11-10.2`): 10 of 181 base oils are formulation-eligible and 11 are Tier 1 complete; no package or component is eligible. S_OIL_ARAMCO_ULTRA_8 is no longer eligible: its KV40/KV100 are SDS ranges and its source selection is pending. Details: `docs/data_policy_mandatory_review/requirements_review.md`.
- Coverage of the TDS–SDS checking is not exhaustive. Remaining gaps: `docs/data_policy_mandatory_review/source_review_coverage.md`.
""")

rep('CLAUDE.md', "- TDS–SDS screening thresholds (Rule 2) are **proposed, not approved** (`tools/data_policy/thresholds.py`, `APPROVAL = 'proposed'`); do not reclassify findings with them until approved.",
    """- TDS–SDS screening thresholds (Rule 2) are **proposed, not approved** (`tools/data_policy/thresholds.py`, `APPROVAL = 'proposed'`); do not reclassify findings with them until approved. They are empirical project screening choices, not technical tolerances: say "below the proposed review threshold", never "ordinary"; a point inside a bound is only "logically compatible", not agreement.
- A technical specification range or bound can be the selected value: select it as printed, never convert it to a single value, and keep the SDS typical as an alternate. A pending source selection needs an explicit reason (identity, applicability, conflicting editions, reliability); a different value kind alone is not one.""")
rep('CLAUDE.md', "- A product missing any mandatory Tier 1 requirement is not formulation-eligible but stays in the database. Tier 2/3 gaps never block. `Not Required` / `Not Applicable` satisfy a requirement only under an approved applicability rule; a calculated value only through a registered reproducibility check. \"Eligible\" is not a statement of chemical suitability.",
    """- A product missing any mandatory Tier 1 requirement is not formulation-eligible but stays in the database. Tier 2/3 gaps never block (the VM/PPD subtype blocks are tier 2/3 files: reported, not blocking). `Not Required` / `Not Applicable` satisfy a requirement only under an approved applicability rule; a calculated value only through a registered check that reproduces it from inputs printed on the cited page. "Eligible" is not a statement of chemical suitability.
- Every requirement outcome has a category (absent, bound/range needing assessment, missing unit/condition/provenance, invalid value, unreproducible calculation, unresolved applicability, unresolved source selection). Do not call every unmet requirement "missing". Authority and open decisions: `docs/data_policy_mandatory_review/requirements_review.md`. Build order: `tds_sds_inventory.py` → `source_coverage_ledger.py` → `build_eligibility.py` (the build stops on a stale ledger).
- Line endings: this machine checks files out with CRLF (`core.autocrlf=true`, system config), while product JSON is committed with LF. The eligibility fingerprint is over exact checkout bytes: regenerate in each checkout and never bypass a mismatch. Verify preserved files and evidence with `python tools/data_policy/verify_preserved.py` (form-aware), not a bare `sha256sum -c` in a CRLF checkout.""")

rep('tools/README.md', "| `data_policy/thresholds.py` | Rule 2 C: the proposed property-specific screening rules (`APPROVAL = 'proposed'`) | nothing |",
    """| `data_policy/thresholds.py` | Rule 2 C: the proposed property-specific screening rules (`APPROVAL = 'proposed'`; empirical choices) and the sensitivity function | nothing |
| `data_policy/source_coverage_ledger.py` | Rule 1 coverage, per product × property: the technical and SDS documents examined, selection status and reason, comparison status, unsearchable documents | `reports/data_policy/source_coverage_ledger.csv` + `.meta.json` |
| `data_policy/verify_preserved.py` | Checks the 49 preserved files and 11 evidence copies against their manifests, form-aware (worktree / committed blob / blob with CRLF); checks the archive against HEAD and the baseline | only `--out`, if given |
| `mandatory_properties/treat_rate_basis_scan.py` | Reading aid: the basis wording on the cited page of every bare-"%" treat rate | `reports/mandatory_properties/treat_rate_basis_scan.csv` |
| `mandatory_properties/treat_rate_basis_evidence.json` | Reviewed page evidence of a mass basis (3 cases) | (data) |
| `mandatory_properties/tests/test_requirements.py` | Regression tests (30): the five reported validation bugs with their valid counterparts, categories, calculations, nested rules | nothing |""")
rep('tools/README.md', "| `data_policy/tests/test_data_policy.py` | Regression tests (36) for Rules 1-3, the outputs and the safety checks | nothing |",
    "| `data_policy/tests/test_data_policy.py` | Regression tests (26): Rule 1, comparison rules, the outputs, counts and the safety checks | nothing |")
rep('tools/README.md', "| `mandatory_properties/build_eligibility.py` | Eligibility outputs; `--check` compares without writing | `reports/mandatory_properties/*` |",
    "| `mandatory_properties/build_eligibility.py` | Eligibility outputs (needs a current coverage ledger); `--check` compares without writing | `reports/mandatory_properties/*` |")
rep('tools/README.md', """**Line endings.** With `core.autocrlf=true`, a fresh checkout rewrites line endings, so `sha256sum -c PRESERVED_SHA256.txt`
can report text files as FAILED although their committed content is unchanged. Check them in a checkout without
conversion, or compare the committed blobs (`git diff <commit> -- tools/`).""",
    """**Line endings.** The manifest records the original bytes, which differ in their line endings:

| Files | Original line ends | How committed |
|---:|---|---|
| 31 | LF | byte-exact |
| 17 | CRLF | normalised to LF |
| 1 | none | byte-exact |

No single `core.autocrlf` setting therefore reproduces all 49 on disk. A bare `sha256sum -c PRESERVED_SHA256.txt` fails for 31 files in a CRLF checkout, and for 17 in an LF checkout.

Use `python tools/data_policy/verify_preserved.py` instead. It checks each file against the worktree bytes, the committed blob, and the blob written with CRLF, and names the form that reproduces the original. On 2026-11-10: 49/49 preserved files and 11/11 evidence copies verified.""")

rep('PROJECT_FILE_GUIDE.md', "| `reports/data_policy/` | Generated output | `document_classes.csv`, `source_selection_changes.csv`, `tds_sds_comparisons.csv` |",
    "| `reports/data_policy/` | Generated output | `document_classes.csv`, `source_selection_changes.csv`, `tds_sds_comparisons.csv`, `threshold_sensitivity.csv`, `source_coverage_ledger.csv` (+ `.meta.json`) |")
rep('PROJECT_FILE_GUIDE.md', "| `reports/mandatory_properties/` | Generated output | `product_eligibility.csv` (one row per product), `missing_mandatory_properties.csv` / `.md` |",
    """| `reports/mandatory_properties/` | Generated output | `product_eligibility.csv` (one row per product), `requirement_outcomes.csv` (every requirement, with its category), `missing_mandatory_properties.csv` / `.md`, `treat_rate_basis_scan.csv` |
| `docs/data_policy_mandatory_review/requirements_review.md`, `source_review_coverage.md` | Review records | The authority for every mandatory requirement and the open decisions; what the source-selection check covered, and the remaining gaps |
| `docs/data_policy_mandatory_review/test_results/` | Historical record | Saved outputs of the pipeline, the tests and the protected-file checks |""")
print('ok')
