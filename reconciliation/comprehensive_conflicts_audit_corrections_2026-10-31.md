# Comprehensive conflicts audit: correction log (2026-10-31)

This log records the product-data corrections made after the comprehensive conflicts audit
(`comprehensive_conflicts_audit.md` / `.csv`, PR #4, commit `e6617ca`). The audit report, its CSV and
`audit_evidence/` (including `evidence_manifest.md`) are kept unchanged as the 2026-10-30 snapshot. Where a finding
below differs from the snapshot's wording (for example "not changed by this audit"), this log describes the later
state.

The audit placed 12 records in the follow-up category "Correctable from existing evidence (data owner)". Each was
checked again against its source. Five led to a change: three value corrections and two documentation notes. The
other seven were deliberately left unchanged.

## Changes

| Audit ID | Product, file, field | Before | After | Evidence | Type |
|---|---|---|---|---|---|
| CF-136 | CHEVRON_SYNFLUID_DIMER_C12, `…__base_oil_tier2_verification.json`, `fields.pour_point` | −63 °C; printed_text "-63" | −53 °C; printed_text "Pour Point, °F, °C -53 (-63)"; earlier reading kept in `notes` | DL2-13202.pdf p.1 (Revision Date April 2011); DL2-13200.pdf p.1 (C12 Dimer column); Chevron Phillips data sheet, revision June 2012 (`audit_evidence/CPChem_Synfluid_Dimer_C12_TDS__cpchem_2020-12.pdf`) | Transcription correction |
| CF-142 | LUBRIZOL_CV1100, `tier2_numeric_contribution.json`, `fields.sulfated_ash` | 5.8 wt.%, Calculated (Ca × 3.40, Zn taken as 0), no source | 7 wt.%, typical, Reported; the 5.8 estimate kept in `alternate_entries` as a historical calculation | DL2-11503.pdf p.2, "SULFATED ASH 7" (Typical column; Effective 11/8/2017) | Value and metadata correction |
| CF-143 | LUBRIZOL_CV3515, same file and field | 9.2 wt.%, Calculated, no source | 10 wt.%, typical, Reported; the 9.2 estimate kept as a historical alternate | DL2-15722.pdf p.2, "SULFATED ASH 10" (Effective 10/9/2017) | Value and metadata correction |
| (linked to CF-142/143) | CV1100 `fields.elements.Zn` / `.S` | Missing / Missing | 0.778 (0.700–0.856) / 2.35 wt.%, Reported | DL2-11503.pdf p.2, "ZINC 0.700 0.778 0.856", "SULFUR 2.35" | Transcription omission |
| (linked to CF-142/143) | CV3515 `fields.elements.Zn` / `.S` | Missing / Missing | 0.772 (0.695–0.850) / 2.4 wt.%, Reported | DL2-15722.pdf p.2, "ZINC 0.695 0.772 0.850", "SULFUR 2.4" | Transcription omission |
| CF-159 | RICHFUL_RF6066, `tier2_numeric_contribution.json`, `conflicts[1].note` (tier2.kv100) | "… field left null. Not resolved." | Same text, plus a dated review note (see below) | DL2-15831.pdf p.5 (SDS 2021-09-02, read visually) | Documentation |
| CF-180 | RICHFUL_RF6078, `tier1_route_defining.json`, `conflicts[0].final_resolution` | Kept origin/main proposal, including "the note text has the two files swapped" | Same text, plus a dated review note: the statement is incorrect | DL2-15832.pdf p.1; RF6078 - TDS.pdf p.1 | Documentation |

### Details of the changes

**CF-136.** Read in the row-label order (°F, °C), −53 °F would be about −47 °C, not −63 °C. The pair is consistent
only as −53 °C = −63 °F. The sheet's other °F, °C rows do follow the label order: flash 362 (183) and fire 396 (202).
No method is printed in DL2-13202.pdf, so the method stays null; ASTM D5950 appears only in the 2012 sheet.

**CF-142 and CF-143.** The values were checked by word position in both PDFs:
- The "Typical" column sits at x=347, under the p.1 header "Minimum % Weight | Typical | Maximum % Weight".
- The table continues on p.2 with no new header.
- No method is printed for these rows.

The unit follows the existing Ca/P/N convention in these files (wt.%).

**CF-159.** The review note says two things:
1. "Field left null" refers to the archive documents only. Since 2026-10-17, `fields.kv100` has held 185 mm²/s from
   the Richful product page (open question 6).
2. The SDS prints 185 on its "Viscosity, dynamic" line with a kinematic unit, while its "Viscosity, kinematic" line
   reads "Not available".

**CF-159 and CF-180: conflict state.** Both conflicts remain unresolved (`resolved: false`). Their values and their
original note or proposal text are unchanged; the review notes are appended after the original text.

### Derived keys

The changed value objects carry `value_final`, `unit_final`, `min_final` and `max_final` identical to those
`integrate_products.py` derives. The historical alternates carry none, following the repository convention.
`integrate_products.py` was not run with `--write`.

## Audit records not changed

| Audit ID | Reason |
|---|---|
| CF-157, CF-158 (Infineum D3354, D3375 flash point) | Already recorded faithfully: the "110 min." value is printed in the Typical column under the footnote "(a) Not a specification". Relabelling it as a specification would contradict the footnote. |
| CF-173 to CF-176 (YUBASE 3/4/5/6 specific gravity in g/m3) | Density stays Missing. The existing open questions already record the issuer (NARMAK TRADE S.R.O.), the missing date and the inconsistent unit, so no further note was added. |
| CF-179 (Richful supplier names) | The three null suppliers (RF6071L, RF6406, RF6408) have no company name printed in their documents. Standardising the printed suffix variants is a separate data-owner naming decision. |

## Effect on CF-144 (sulfated-ash estimates)

CF-144 counts the sulfated-ash fields whose selected value is a calculated estimate.

| Count | e6617ca (audit snapshot) | After these corrections |
|---|---|---|
| Selected `fields.sulfated_ash` with status Calculated | 26 | **24** |
| … with Zn factor 1.24 (Ca/Mg/Zn only) | 25 | 23 |
| … with Zn factor 1.5 plus Mo and B terms (MINGLAN_T3161A) | 1 | 1 |
| Historical Calculated estimates kept in `alternate_entries` | 0 | 2 (LUBRIZOL_CV1100, LUBRIZOL_CV3515) |
| Selected `fields.sulfated_ash` with status Reported | 34 | 36 |

The two Lubrizol estimates are no longer selected values: each has been replaced by its product's printed typical
value. They are kept, labelled as historical, and not counted among the 24. CF-144's finding stands for the 24
records: two different zinc factor sets are in use, and which is correct depends on ASTM D874, which has not been
accessed.

## Supporting updates

- `open_questions_and_conflicts.md` (curated by hand):
  - Added dated correction lines to the CV1100, CV3515 and Dimer C12 sections.
  - The RF6066 KV100 conflict line now mirrors the JSON note.
  - Added a review line after the RF6078 conflict.
  - Added a summary bullet under "Documentation uncertainties and corrections".
  - Extended the RF6078/RF6066 item under "Human review".
  - Existing text is kept.
- `Coverage_Matrix.xlsx`, regenerated with `build_coverage_matrix.py`. Coverage uses the recorded `status`; no product
  file carries `status_final`. A rebuild from the `e6617ca` data was identical to the committed workbook, so every
  difference below comes from these corrections:
  - Additive Packages: CV1100 and CV3515 `sulfated_ash` changed from calculated to reported, and `elements.Zn` and
    `elements.S` from missing to reported. That is 6 cells; nothing else changed.
  - Overview, Additive Packages row: Reported cells 1004 → 1010, Calculated cells 26 → 24, Missing / N.A. cells
    764 → 760.
  - Overview, Status Detail rows: 6318 → 6320. The two historical alternates are listed as nested rows, "not
    counted in cell".
  - Status Detail: the Dimer C12 pour_point row shows −53 instead of −63. Its status is Reported both before and
    after, so no matrix cell changes.
  - Unchanged: products 264, JSON files 706, class counts (181 / 78 / 5), the Base Oils and Additive Components
    sheets, Validation Issues (30) and the Traceability Audit.

## Not done

- No commit, push or merge, and PR #4 is unchanged.
- Dimer C12 `source.revision_date` is still null, although the sheet prints "Revision Date April 2011". This is a
  product-wide change, not made here.
- The Chevron Phillips 2012 sheet is cited in a field note, not as a field source, and is not added to
  `source_registry.json`.
- `reconciliation/README.md` does not list this log.
