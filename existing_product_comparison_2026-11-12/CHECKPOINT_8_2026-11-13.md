# Checkpoint 8 — old-versus-new comparison (eighth pass, 2026-11-13)

Supersedes the status sections of checkpoints 1-7 (kept unchanged). Comparison and proposal preparation only: nothing
ingested, no JSON or production file changed, nothing staged or committed. `logs/03_checks.log`: 55 of 55 (structural).
**Not complete:** 383 of 1,068 non-duplicate links not yet assessed. "Ready for reviewer decision" means the three-way
comparison as recorded is done for that proposal; it does not mean approved, and it does not mean the comparison is complete.

## 1. HiTEC 12204L premix arithmetic ("14.2 % = 10.3 % + 4.2 %", which adds to 14.5 %)

- **Already recorded, not duplicated:** AFTON_HITEC_12204L tier-1 notes ("10.3% + 4.2% = 14.5%, not the printed 14.2% …
  recorded as printed, not reconciled. Confirm with Afton.") and AFTON_HITEC_12250 open questions (same finding).
- **Original page verified as an image:** `DL2-14639.pdf` (08/18) p.2 footnote 1, wording verbatim. Sibling footnotes on the
  same page are arithmetically consistent (12204Y: 10.3 + 5.0 = 15.3; 12252: 10.8 + 0.35 = 11.15); only footnote 1 is not.
- The same printing recurs in `DL2-14863.pdf` p.2 (04/19), `DL2-13364.pdf` p.7 (2019) and, as "%wt" sentences beside
  "14.2 %wt", in `DL2-14862.pdf` p.2 (May-19, Aramco Prima Group II programme).
- **Proposal (HiTEC 12200 only):** an open-question entry that links to the existing finding and lists these printings.
  No value corrected; the premix and the 10.3 + 4.2 route are not treated as numerically interchangeable.
- **Narrowed basis proposal:** row [0] of the HiTEC 12200 treat-rate matrix and the HiTEC 12250 4.2 booster dose are now
  left unresolved. Their only "%wt" evidence is restricted to the Aramco Prima Group II programme; that restriction stays
  attached to the citation. The mass-basis proposal now covers 9 rows and 2 booster doses.

## 2. Neste NEXBASE

- Old sources read: TDS `DL2-10037.pdf` (3043, ed. 5.2), `DL2-10039.pdf` (3060, ed. 6.2), `DL2-10040.pdf` (3080, ed. 2.2).
- `DL2-12853.pdf`, Neste (Suisse) certificate, NEXBASE 3060 drums (read as an image): limits equal the TDS limits
  already in the JSON. New: "Additional typical properties" sulphur < 10 mg/kg (D5453) and saturates > 99 % (D2007);
  tier-3 fields are Missing → proposed as bounded typicals. The printed 300 / 90 are API/ATIEL Group III thresholds, not
  product limits.
- Third-party certificates: 3060 (`DL2-14400`), 3043 (`DL2-14397` = `DL2-14398`, same measurement re-issued), 3080
  (`DL2-14401` = `DL2-14402`). Batch evidence only; notes for the Missing 3043 / 3080 sulphur and saturates fields.
- 127 mention links: every captured first-hit passage read; all are recipe shares; content review limited to that passage.

## 3. Status (separate measures)

| Measure | Value |
|---|---|
| Relationship settled (non-duplicate) | 664 (+2 excluded, 20 unresolved) |
| … content review limited (name-hit passage, unread pages) | 529 |
| … source-to-JSON coverage "not assessed" | 575 |
| Not yet assessed | 383 |
| Proposals | 137 (all with recorded three-way comparison; 0 provisional) |
| Duplicate-source coverage (223 documents) | not started |

## 4. Exact resume point

1. `CHEVRON_GROUP_II_220R` (46 links), then `CHEVRON_GROUP_II_600R` (30), `S_OIL_ULTRA_S_4` (28), `CHEVRON_GROUP_II_100R` (26),
   `S_OIL_ULTRA_S_8` (20), `S_OIL_ULTRA_S_6` (11), `CHEVRON_GROUP_II_150R` (9), `EXXONMOBIL_APE_CORE_600` (9),
   `EXXONMOBIL_APE_CORE_150` (8), `PETRONAS_ETRO_4` (7), … Method: `scripts/hits.py <id>` → identify product-specific
   documents and read them against the cited old source and the JSON → `scripts/helpers/write_base_oil_mentions.py` for the
   rest → print and READ every captured passage before saving.
2. Unread content (checkpoint 4 §3 and the 529 limited reviews).
3. Duplicate-source coverage (223 documents).
