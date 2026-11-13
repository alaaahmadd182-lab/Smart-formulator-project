# Local-only files of the new-dataset review (not committed)

Recorded 2026-11-13 (fifteenth pass), before the local checkpoint commit on branch `feat/new-dataset-review-ingestion`. These files are deliberately not tracked; they stay in the worktree `C:/Users/windo/sf-wsA` or the main checkout. Do not run `git clean` in either place: a branch does not protect untracked files.

Tree hash = SHA-256 of a manifest of `<sha256>  <relative path>` lines sorted by path.

| Folder | Size | Tree hash | What it is |
|---|---|---|---|
| `existing_product_comparison_2026-11-12/_cache/` | 147 files, 48.5 MB | `01971b35ae35dce2172bf57178acbf1f47426dd4fefc2f67d006669a5e7c9ed1` | page renders (render.py output); regenerable from the new archive |
| `incoming_dataset_review_2026-11-12/_cache/` | 4086 files, 15.3 MB | `136796915c98603175f0696d91ac5c065a8640e8009211f0ea4ba244fcb047db` | text extraction, members.jsonl, reference.json, ref_text, one sample render; regenerable with scripts/01_extract.py and 02_reference.py from the two archives |
| `review_snapshots/review_snapshot_2026-11-12/` | 947 files, 14.5 MB | `51fd76cf518bc667966935d69e93d985b262c1f5b4475b8c6f4baa78ec1dd49a` | frozen copy of the reviewed Part A state (2026-11-12); the published commits 1d0815b / 8d4626b hold the shared state |
| `existing_product_comparison_2026-11-12/current_json_excerpts/` | 343 files, 0.3 MB | `dd3411bb80c22935e7505cfb1b2962935b3fe92c8c964235e3ee3e5115e05791` | excerpts of the current product JSON written by scripts/02_build.py; regenerable from the tracked Products_json |

## Original sources and earlier review packages

| File | Size | SHA-256 | Note |
|---|---|---|---|
| `C:/Users/windo/OneDrive/Desktop/Smart formulator project/Downloaded lubricants sheets.zip` | 1447.9 MB | `62565d5c7a2afc2203536c241004cd4af7f62866a4bfe4f70801b378cf2c78b1` | new archive (untracked in the main checkout; never modified) |
| `C:/Users/windo/OneDrive/Desktop/Smart formulator project/Manual + Data to share.zip` | 91.0 MB | `6488b08f9729c4988c8e73bfe51dac355f64ee601e78554591a3450ba5f5497a` | old archive (tracked in the repository; never modified) |
| `Desktop/SmartFormulator_audit_review_v5_2026-11-02.zip` | 2.4 MB | `cee520e4faeb250ae6bd5a31d3cff2312fd6f2ddf62ff8903dc88832b5635232` | earlier review / evidence ZIP (not overwritten) |
| `Desktop/SmartFormulator_comparison_evidence_2026-11-12_12.zip` | 88.8 MB | `c9b450d063bc0954392659c1d461ff6e3ade7bbf40437fcb0646ea6c66aa121e` | earlier review / evidence ZIP (not overwritten) |
| `Desktop/SmartFormulator_comparison_evidence_2026-11-12_13.zip` | 107.4 MB | `932a5b32b22cfc0daf5b400bf6068fd43cf32602cd38fd544316ab765f0c926f` | earlier review / evidence ZIP (not overwritten) |
| `Desktop/SmartFormulator_comparison_review_2026-11-12_12.zip` | 2.0 MB | `42ace0d6c9c087601e63f223d04f9518202ea43d9495bd9deeac3710923d61bc` | earlier review / evidence ZIP (not overwritten) |
| `Desktop/SmartFormulator_comparison_review_2026-11-12_13.zip` | 2.2 MB | `262f9c40ae144fbb36a44d9a098e1db13d911c69e3c86881533c05ef37fde23e` | earlier review / evidence ZIP (not overwritten) |
| `Desktop/SmartFormulator_inventory_review_2026-11-12.zip` | 1.5 MB | `280d0685cc581ebbf8d1bf25e299deab5249b9b67d85c206b01b702487336124` | earlier review / evidence ZIP (not overwritten) |
| `Desktop/SmartFormulator_source_corrections_review_v2_2026-10-31.zip` | 1.2 MB | `976f199434d8fbe4bdd797c7c28f60a67f1d1b6ce9098754c98fb8b73e1385f0` | earlier review / evidence ZIP (not overwritten) |

The archive hashes are checked on every run (`scripts/03_checks.py`, preservation section).
