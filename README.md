# Smart Formulator – raw-material data preparation

Structured, source-traceable extraction of supplier datasheets (base oils, additive packages,
additive components) following `Smart_Formulator_Minimum_Property_Set.pdf`, which is inside
`Manual + Data to share.zip`.

| Path | Contents |
|---|---|
| `Property_Glossary.docx` | Task 1 – property glossary |
| `json_templates/` | Task 2 – one JSON template per material class and tier |
| `Products_json/` | Task 3 – one folder per product, one JSON file per tier |
| `build_coverage_matrix.py`, `Coverage_Matrix.xlsx` | Task 4 – coverage script and its output |
| `open_questions_and_conflicts.md` | Task 5 – conflicts and open questions |

## Building the coverage matrix (Task 4)

Requires Python 3.12 (Windows, macOS or Linux). From the project folder:

```
python -m pip install -r requirements.txt
python build_coverage_matrix.py --output Coverage_Matrix_new.xlsx
```

Options: `--input` (default `Products_json`), `--output` (default `Coverage_Matrix.xlsx`) and
`--overwrite`. Without `--overwrite`, the script refuses to replace an existing workbook.

The script only reads the JSON files; it never changes them. The workbook contains:

- **Overview** – product, file and status counts, plus the run status.
- **Base Oils / Additive Packages / Additive Components** – one row per product, one column per
  property. Each cell is `reported`, `calculated`, `missing` or `not_applicable`.
- **Validation Issues** – structural problems and mixed nested statuses.
- **Status Detail** – every nested status in the JSON, with its original spelling, the source file and the page.
- **Traceability Audit** (informational) – reported values with no source file, with an
  external URL instead of an archive file, with no page number, or based on general knowledge.

When a property has subfields with different statuses, the cell shows the highest-priority
status (reported > calculated > missing > not_applicable) and is shaded amber. **A cell marked
`reported` may still contain missing subfields**; Status Detail lists every subfield.

### Exit codes and failed validation

| Code | Meaning |
|---|---|
| 0 | Passed; workbook written |
| 1 | Usage error (input folder not found, or output exists without `--overwrite`) |
| 2 | Validation failed; `<output>_DIAGNOSTIC.xlsx` is written instead and the requested output is **not** touched |

Validation fails on any of the following: an unrecognized status value (shown in red as
`unrecognized: <value>`, never converted to `missing`), an unreadable file or invalid JSON, a
missing material class or record ID, a duplicate tier or property, a missing expected tier, or
data without any status.
