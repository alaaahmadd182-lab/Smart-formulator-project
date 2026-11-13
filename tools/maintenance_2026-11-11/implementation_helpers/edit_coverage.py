p = r'C:\Users\windo\sf-wsA\docs\data_policy_mandatory_review\source_review_coverage.md'
s = open(p, encoding='utf-8').read()
reps = [
("Revision 3, 2026-11-10. The case-by-case review of the leads is in [evidence_review.md](evidence_review.md).",
 "Revision 3, 2026-11-10; completed 2026-11-11. The case-by-case review of the archive leads and of the external sources is in [evidence_review.md](evidence_review.md) (sections 1 and 8)."),
("The ledger labels rows mechanically. Its lead labels (\"Missing, label found\", \"not searchable\", \"gap\") are **leads**. The reviewed outcome of every such case is in `reports/data_policy/lead_review.csv`.",
 "The ledger labels rows mechanically. Its lead labels (\"Missing, label found\", \"not searchable\", \"gap\") are **leads**. The reviewed outcome of every such case is in `reports/data_policy/lead_review.csv`; the outcome of every external-source value is in `reports/data_policy/external_review.csv`; and the review state of every ledger row is in `reports/data_policy/source_review_status.csv` (section \"Review state\" below)."),
("| external (URL) source selected | 22 | 14 |",
 "| external (URL) source selected (all reviewed: see `external_review.csv`) | 22 | 14 |"),
("The TDS–SDS inventory (`tds_sds_comparisons.csv`) has 141 pairs. 70 of them come from SDS values recorded in this review.",
 """The TDS–SDS inventory (`tds_sds_comparisons.csv`) has 141 rows. 71 of them come from SDS values recorded in this review (70 product × property cases; S_OIL_ULTRA_S_3 flash point has two SDSs).

## Review state (`source_review_status.csv`; counting unit: ledger row)

| Review state | Rows | Mandatory |
|---|---:|---:|
| completed archive lead review (usable 81, already recorded 31, unrelated mention 71) | 183 | 61 |
| completed external-source review (confirmed on an identified copy) | 21 | 16 |
| evidence unavailable: the archive documents do not print the value (173), or no copy of the external source could be obtained (8) | 181 | 81 |
| evidence inconclusive: document identity not established | 7 | 2 |
| not individually reviewed: the state rests on the mechanical classification only | 1,783 | 745 |
| **Total** | **2,175** | **905** |

A recorded outcome for every one of the 363 frozen lead cases and the 29 external cases does **not** mean that all source verification is complete. 188 reviewed rows end without usable evidence, and 1,783 rows were never individually re-read."""),
("| ARAMCO_LUBEREF_PRIMA_110 / 230 / 500 | density | spec DL2-12172 (no unit) vs brochure DL2-11773 (Kg/L); the brochure marks 110/230 typicals as provisional |",
 "| ARAMCO_LUBEREF_PRIMA_110 / 230 / 500 | density | spec DL2-12172 (no unit) vs brochure DL2-11773 (Kg/L); the brochure marks 110/230 typicals as provisional; for 230 the external Aramco sheet prints a third value, 0.8635 kg/L (conflict EVR-2026-11-11-230-density-external) |"),
("| S_OIL_ARAMCO_ULTRA_8 | KV40, KV100, flash point | external S-OIL web table vs archived SDS; identity question ID-01 |",
 "| S_OIL_ARAMCO_ULTRA_8 | KV40, KV100, flash point | external S-OIL web table (values confirmed on the saved copies, 2026-11-11) vs archived SDS ranges: a policy decision on external technical sources; KV40 typical 41.10 lies below the SDS range (conflict EVR-2026-11-11-ULTRA8-kv40); identity question ID-01 |"),
("| AFTON_HITEC_8788B | KV40, KV100, density, flash point | external PDS not re-read |",
 "| AFTON_HITEC_8788B | KV40, KV100, density, flash point | external PDS (Internet Archive) could not be obtained on 2026-11-11; whether it prints these values is unknown |"),
("- **22 external-source values not re-read** (technical work still possible).",
 "- **8 external-source cases without a copy** (Afton HiTEC 12204L and 8788B PDSs): the Internet Archive refused automated download; a manual download matching the registry SHA-256 would allow the review;\n- external technical pages vs archived SDSs (a policy decision)."),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
