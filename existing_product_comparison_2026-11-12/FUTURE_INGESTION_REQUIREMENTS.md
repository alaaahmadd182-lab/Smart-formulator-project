# Future ingestion: requirements (recorded 2026-11-13; NOT implemented)

This review compares the new archive ("Downloaded lubricants sheets.zip") with the existing data and proposes JSON changes.
**No proposal has been applied, and no ingestion pipeline exists yet.** This file records what the eventual ingestion must do,
so that the review output can feed it later. Pipeline implementation is a separate, future task and is not started.

## Required design

The ingestion must be a reusable lubricant-data pipeline, not a one-off script.

1. **Configurable material templates.**
   - Base oil, additive package and additive component, with their tiers, are defined by the templates in `json_templates/`.
   - Templates are configuration, not hard-coded fields.
   - A new material class or field is added in the template, and the pipeline follows it without code changes.
2. **Source provenance on every value.**
   - Record the file, the page, the document SHA-256 and the revision date, as printed.
   - Keep `printed_text`, unit, method, conditions, qualifier and percentage basis, and the value class:
     typical / specification / batch / SDS reported value with unspecified statistical basis / third-party.
   - Keep route or formulation scope where it applies.
3. **Duplicate detection.**
   - **Documents:** by SHA-256, then by normalised text, then by edition.
   - **Products:** by stable product id plus reviewed identity (grade suffixes such as 5748 vs 5748A are never merged).
   - **Values:** by (product, field, source document, page).
   - **Rerunning must not create duplicate records, alternate entries, conflicts or open questions.** Ingestion is idempotent.
4. **Validation.**
   - JSON validity and the allowed status vocabulary.
   - Units and conditions.
   - Value-class rules: SDS values are never promoted to typicals or specifications, and component shares are never treated as
     element contents.
   - Range and bound handling: never a midpoint.
   - No averaging, and no automatic TDS-vs-SDS preference.
   - Conflicts are recorded with both sources and stay unresolved unless authoritative evidence supports a resolution.
5. **A review queue.** Every change goes through a reviewer queue with these states, in this order: proposed → ready for reviewer
   decision → approved / rejected. "Ready" is never "approved". Only approved items are written. Unknown layouts, unreadable
   pages, uncertain identity and uncertain evidence are flagged into the queue and are never written automatically.

## Required tests

- **Verified examples.** The pipeline must be tested against verified examples from this review, for example:
  - the Synfluid SDS / data-sheet pairs (SDS class, conflicts kept);
  - Esterex A34 PMCC (capture from an old source);
  - RF6400 SDS composition and classification wording (kept verbatim; nothing inferred);
  - the D3503 formulation tables (printed anomalies kept as printed);
  - CV2301 OS415889 / OS269689 (separate oil codes, mass % vs volume %);
  - the Nyfrost 32 citation correction (p.6 → p.7).
- **Rerun.** Running twice on the same input must produce the same files and no duplicate records.
- **Negative tests.**
  - a file with an unknown layout is flagged, not ingested;
  - a value without a page or document hash is rejected;
  - a 5748A value offered for HiTEC 5748 is refused.

## Inputs this review will provide

- `tables/proposed_json_changes_NOT_APPLIED.csv`: each proposal with its source, page, document hash, value form, qualifier,
  method, conditions, percentage basis, reason and readiness.
- `tables/progress_ledger.csv`: every product × document link, with relationship, verification status and coverage.
- `decisions/*.json`: the reviewed decisions, reproducible with `scripts/decision_generators/`.
- `tables/new_product_candidate_queue.csv`: candidate new products. These are not ingested without a reviewed identity.
