p = r'C:\Users\windo\sf-wsA\open_questions_and_conflicts.md'
s = open(p, encoding='utf-8').read()
a = "- All outstanding source leads were reviewed. That is 362 product × property cases: the 352 of revision 2 plus 10 found during the review."
b = "- All outstanding source leads were reviewed. That is 363 product × property cases: the 352 of revision 2 plus 11 found during the review (count corrected 2026-11-11)."
assert s.count(a) == 1
s = s.replace(a, b)
a = "  - 174 name-match document links were reviewed, and 9 were for other products (excluded): NYNAS Base Stock 20 ↔ S 3B / NS 3; S-OIL S-8 ↔ Ultra-S sheets."
b = "  - 174 name-match document links were reviewed (87 same product, 78 byte-identical copies, 9 other product). The 9 are excluded: NYNAS Base Stock 20 ↔ S 3B / NS 3; S-OIL S-8 ↔ Ultra-S sheets."
assert s.count(a) == 1
s = s.replace(a, b)
s = s.rstrip('\n') + '\n' + """
### 2026-11-11: external-source review (revision 3 completion)

- The 22 values selected from external (URL) sources and 7 pending fields with an external alternative were reviewed (`reports/data_policy/external_review.csv`; `docs/data_policy_mandatory_review/evidence_review.md` §8).
  - 21 were confirmed on copies whose identity is established.
  - 8 are inconclusive because the source could not be obtained: the Afton HiTEC 12204L PDS (KV100, density, flash point, TBN) and the HiTEC 8788B PDS (KV40, KV100, density, flash point; still pending). The Internet Archive refused automated download.
- New conflicts, not resolved:
  - ARAMCO_LUBEREF_PRIMA_230 Noack: the Aramco PRIMA 230 sheet prints a typical 7.5 wt%, above the DL2-12172.pdf maximum 7 (`EVR-2026-11-11-230-noack`). The selected value is unchanged.
  - ARAMCO_LUBEREF_PRIMA_230 density: the same sheet prints 0.8635 kg/L at 15 °C, a third value (`EVR-2026-11-11-230-density-external`). The field stays pending.
  - S_OIL_ARAMCO_ULTRA_8 KV40: the S-OIL typical 41.10 cSt lies below the SDS range 42.0–55.0 cSt (`EVR-2026-11-11-ULTRA8-kv40`). The field stays pending.
- Open question for the user: may an external (non-archive) technical document be selected over an archived SDS, or fill a Missing field? This affects aramcoULTRA 8 KV40/KV100/flash point and the BAPbase 4 specific gravity printed by the MOGO flyer.
"""
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
