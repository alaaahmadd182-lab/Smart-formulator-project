# Dataset preparation, checkpoint P03 (2026-11-14)

This checkpoint continues from P02 (`58419c0`) after an interrupted run.
- No production JSON or template changed (check C08).
- No proposal was applied; nothing was pushed or merged; no ZIP was created.

## 1. Recovery

- The working tree was clean at `bba99f2`. The interrupted Functional Products / Oleon work had not been written to disk; it was redone from the documents (S26, S27).
- **OCR run finished** (`logs/01_ocr.log`, now committed):
  - 501 of 501 documents without a usable text layer are cached;
  - 911 pages were OCR'd, 26 of them with no legible text;
  - 1 file failed: `747b0e9f661a`, a truncated JPEG, which is unreadable in the archive itself.
- `02_identify.py` was re-run with the OCR text: 202 documents gained identity text and no supplier label changed. The table the S01–S24 generators selected from is frozen as `tables/document_identity_auto_v1_preOCR.csv`.

## 2. Stages (kept apart; `scripts/05_stages.py`, `tables/product_stages.csv`)

| Stage | Meaning | Count (non-existing products: 1,394) |
|---|---|---|
| 1 Candidate detected | a product key exists | 1,394 |
| 2 Identity verified | a subject document was read in an identity decision | 1,356 verified; 13 verified with an open question; 25 candidate only (mentioned, no document of their own) |
| 3 Class and template established | one of the three templates, no open scope / fit question | 887 established; 195 open question; 159 unresolved; 153 out of template |
| 4 Technical evidence reviewed | per-field evidence read | **0** |
| 5 Field-level mapping complete | every template field traceable or explicitly Missing | **0** |

**Conversion-ready products: 0.**
- 868 products have both a verified identity and an established template. That makes them eligible for technical review, not ready for conversion.
- "Identity verified" means the printed name was read on page 1 of a subject document. It says nothing about values.

Existing production records: 264. Their evidence backlog is unchanged since checkpoint 20 of the existing-product comparison:
- 665 proposals, none approved;
- 508 open non-duplicate links;
- D3503 × DL2-11768;
- six visual checks;
- HiTEC 12210M claim dots;
- OLOA 55603 slides.

## 3. Identity progress

- **Documents with a reviewed identity: 2,497 of 4,186.**
- Batches since P02: S13–S27. Documents per batch:

| Batch | Supplier label | Documents |
|---|---|---|
| S13 | Jinzhou label, split into Donggong / Xinxing / Bettchem / KangTai | 50 |
| S14 | ExxonMobil | 48 |
| S15 | Lubimax / Coraplus | 47 |
| S16 | Kusa | 46 |
| S17 | KangTai | 40 |
| S18 | Eni / Versalis | 37 |
| S19 | Dow label, split into Dowpol and Dow Chemical | 35 |
| S20 | Chevron Phillips | 33 |
| S21 | Mingyue | 30 |
| S22 | Vanderbilt | 29 |
| S23 | Goncord | 29 |
| S24 | Yasho | 27 |
| S25 | Wuxi South | 26 |
| S26 | Functional Products | 23 |
| S27 | Oleon | 20 |

- **Not yet reviewed: 1,689 documents** = 278 with a supplier label (smaller suppliers) + 1,411 without one.

**Rules added in S25–S27:**
- The document's **subject** is separated from products that are only **mentioned**. Example: on the Paratac XT sheet, FUNCTIONAL V-188 is "recommended instead" for higher temperatures. Mentioned-only products stay at stage 1.
- Manufacturer, distributor and issuer are recorded in separate columns. Examples: Tri-iso Inc. sheet for PARATAC 178; Multisol France sheet for NOVAD B700; Oleon nv vs OLEON N.V. Oelegem vs Oleon Port Klang certificates.
- RADIALUBE 7361 / 7364 / 7563 print the same chemical name and stay three products.

## 4. Reconciliation across batches (`decisions_reconciliation.json`, `tables/reconciliation_candidates.csv`)

29 entries, 8 of them open. No merge was made on a name or value similarity.

- **Kept separate (different manufacturers):** generic codes T106 / T106A / T115B / T154A / T161 / T202–T205 (Xinxing, Mingyue, Donggong, Wuxi); PAO 4 / 6 / 10 / 100 (Dowpol, Goncord, Sama).
- **Kept separate (printed variants):** RC 9321 / 9321 D; RC 9200 / 9200 N; FUNCTIONAL V-178 / PARATAC 178; NT561 / P46.
- **Merged on a documented spelling variant:** KangTai "KT D1354" = "KTD1354" (same company; code printed both ways).
- **Open:**
  - Sama EHC-50 / EHC-120 vs the ExxonMobil records;
  - KangTai J-0010 vs PetroChina Jilin J0010;
  - Mingyue T106A / T154A vs MY-T106A / MY-T154A;
  - Wuxi T109A vs WX109A;
  - **YALUB ZDD chemical identity:** the TDS prints "Zinc Diamyldithiocarbamate in 50% oil", the SDS "2,5-Dimercapto-1,3,4-thiadiazol…". Unresolved; the SDS is blocked;
  - Sama A1011 SDS naming A1010.

`tables/blocker_log.csv`: 23 entries (identity conflicts, redacted names, documents whose identity is not established).

## 5. Checks

`python scripts/04_checks.py --hash-archive`: **10 / 10 passed.**
- baseline counts and archive hash;
- one row per document;
- one owner per decision;
- all linked keys defined;
- vocabularies;
- multi-product dispositions;
- stage consistency;
- production data untouched;
- OCR coverage;
- field-evidence rows.

## 6. Next

1. Field-level mapping pilot on a batch whose identity and template are established (starting with one-page product sheets), writing `tables/field_evidence.csv` and `tables/field_mapping_status.csv`.
2. Identity batches for the remaining 278 labelled documents, then the 1,411 unlabelled ones using the OCR text.
3. The existing-product backlog listed in §2.
