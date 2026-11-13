"""Eighteenth pass, batch 26: the columns of the combined Chevron Phillips C10 / C12 PAO typical-properties sheet DL2-13200.pdf
(1 page, undated; read in full in batch 20) that had no ledger link, reviewed against the in-scope inventory. Nine records already
list DL2-13200.pdf in their source_documents (specific-gravity notes say the family sheet 'prints the same value'); each column is
compared with that record field by field. No equivalence with the single-grade sheets is assumed beyond the records' own association:
where the values differ, the difference is proposed as a conflict CONDITIONAL on the reviewer confirming the column's identity.
Writes decisions/zzzzzzzzzzzzzzzzzz_b26_dl2_13200_columns_eighteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'eighteenth pass, 2026-11-14'
f = 'DL2-13200.pdf'
ED = "combined 'C12 Based PAOs' / 'C10 Based PAOs' typical-properties sheet, undated (no trade name 'Synfluid' printed)"
O = f're-read manually: {f} ({ED}) p.1 whole text, column by column ({T})'
METH = "methods printed on this sheet: KV100 / KV40 'ASTM D 7042', KV -40 °C 'ASTM D 445', VI 'ASTM D 2270', pour 'ASTM D 5950', flash / fire 'ASTM D 92', Noack 'ASTM D 5800', specific gravity 'ASTM D 4052'"
links, F = [], []


def link(pid, col, cov, ident):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'p.1 (only page) read in full (text layer; batch 20) and column {col!r} compared with this record ({T})',
                      coverage=f'assessed by reading (2026-11-14, eighteenth pass) for column {col!r}: {cov}', identity=ident,
                      note='Reviewer-recorded link: the record already lists DL2-13200.pdf in source_documents; the ledger had no link for this column.'))


def row(pid, path, tier, old, text, reason, action, outcome, form, cond, cmp, unit='as printed', method='as printed'):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=1, new_text=text, unit=unit, form=form, qual='typical', method=method, cond=cond, basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=O, cmp_override=cmp))


IDENT = "column header {col!r} under the heading {head!r}; the record lists DL2-13200.pdf in source_documents and its specific-gravity note cites this column. The page prints no trade name, so the identity rests on that existing association (reviewer to confirm)."

# ---- columns whose every printed value equals the record ----
SAME = [
    ('CHEVRON_SYNFLUID_DIMER_C10', 'C10 Dimer', 'C10 Based PAOs', 'DL2-13201.pdf', "KV100 1.7, KV40 4.9, pour -73 (-100), flash 159 (318), SG 0.8026; VI and Noack '—'"),
    ('CHEVRON_SYNFLUID_DIMER_C12', 'C12 Dimer', 'C12 Based PAOs', 'DL2-13202.pdf', "KV100 2.3, KV40 7.7, pour '-53 (-63)' under the label '°C (°F)' (the record's audit note CF-136 already cites it), flash 183 (362), SG 0.8100; VI and Noack '—'"),
    ('CHEVRON_SYNFLUID_PAO_2', '2 cSt', 'C10 Based PAOs', 'DL2-13192.pdf / DL2-14990.pdf', "KV100 1.7, KV40 5.1, pour -73 (-99), flash 159 (317), SG 0.7981; VI and Noack '—'"),
    ('CHEVRON_SYNFLUID_PAO_4', '4 cSt', 'C10 Based PAOs', 'DL2-11914.pdf', "KV100 3.9, KV40 16.8, VI 124, pour -68 (-91), flash 226 (438), Noack 13.4, SG 0.8190"),
    ('CHEVRON_SYNFLUID_PAO_6', '6 cSt', 'C10 Based PAOs', 'DL2-11915.pdf', "KV100 5.9, KV40 30.5, VI 137, pour -61 (-78), flash 245 (473), Noack 6.6, SG 0.8278. The values exclude Synfluid PAO 6 cSt HVI (record: KV40 29.1, VI 150, pour -44, Noack 4.9, SG 0.8256)"),
    ('CHEVRON_SYNFLUID_PAO_8', '8 cSt', 'C10 Based PAOs', 'DL2-11916.pdf', "KV100 7.8, KV40 46.4, VI 138, pour -56 (-68), flash 262 (504), Noack 3.5, SG 0.8326. Synfluid PAO 8 cSt Blend shares KV100 7.8 and SG 0.8326 but differs in VI (145), pour (-45), flash (266) and Noack (2.5), so this column is not the Blend"),
]
for pid, col, head, cited, vals in SAME:
    link(pid, col, f"every value printed in the column equals the record ({vals}); the record cites {cited} for them. Not recorded: KV -40 °C, fire point, density lb/gal, the methods and the shared footnote -> source-addition row (methods) / note.",
         IDENT.format(col=col, head=head))
    row(pid, 'kv100', 1, f"Record kv100 cites {cited} (no method printed there).", f"Column '{col}' ({head}): the same KV100 / KV40 / VI / pour / flash / Noack / SG values as the record, with the {METH}.",
        "Same values in a second Chevron Phillips document that also prints the test methods. Propose adding it as a second source for the matching fields (methods as printed on this sheet; the single-grade sheet's own entry keeps no method). Values unchanged; nothing selected or merged. Conditional on the column identity (see identity).",
        'propose_source_addition', 'already_captured', 'typical value (family typical-properties table)', f"CONDITIONAL: apply only after the reviewer confirms that column '{col}' is this product", 'existing: same values, single-grade source without methods',
        unit='cSt', method='ASTM D 7042 (KV)')

# ---- C12 columns whose values differ from the single-grade sheets ----
DIFF = {
    'CHEVRON_SYNFLUID_PAO_5': ('5 cSt', 'DL2-13193.pdf (MSDS #5940, Revision Date December, 2008)',
        [('viscosity_index', 1, "Viscosity Index 145 (ASTM D 2270)", 'VI 144')],
        "pour -46 (-50) vs -45; Noack 5.6 vs 5.5; KV -40 °C 4,787 vs 4716; KV100 5.1, KV40 24.1, flash 245, SG 0.8240 equal"),
    'CHEVRON_SYNFLUID_PAO_7': ('7 cSt', 'DL2-13194.pdf (MSDS #5941, Revision Date December, 2008)',
        [('kv40', 1, "40°C (104°F) 37.7 (ASTM D 7042)", 'KV40 37.3'), ('viscosity_index', 1, "Viscosity Index 146 (ASTM D 2270)", 'VI 148')],
        "pour -43 (-45) vs -42; flash 264 (507) vs 262; Noack 3.7 vs 3.3; KV -40 °C 10,732 vs 10,561; KV100 7.0 and SG 0.8306 equal"),
    'CHEVRON_SYNFLUID_PAO_9': ('9 cSt', 'DL2-13196.pdf (MSDS #5653, Revision Date December, 2008)',
        [('kv100', 1, "100°C (212°F) 8.9 (ASTM D 7042)", 'KV100 9.0'), ('kv40', 1, "40°C (104°F) 53.4 (ASTM D 7042)", 'KV40 53.9')],
        "pour -34 (-29) vs -36; flash 280 (536) vs 276; Noack 2.4 vs 2.2; VI 146 and SG 0.8343 equal"),
}
for pid, (col, single, rows, others) in DIFF.items():
    link(pid, col, f"the column prints different typicals from the single-grade sheet {single} that the record cites: " + '; '.join(f"{r[2]} vs record {r[3]}" for r in rows) + f"; also {others}. -> conditional conflict rows. The sheet is undated, so no edition order is assumed.",
         IDENT.format(col=col, head='C12 Based PAOs'))
    for path, tier, txt, rec in rows:
        row(pid, path, tier, f"Record {path}: {rec} ({single}).", f"Column '{col}' ('C12 Based PAOs'): '{txt}'",
            f"Two Chevron Phillips documents print different typicals for what the record treats as the same grade. Propose a conflict entry with both values and sources; not averaged, no edition order (the family sheet is undated), the record keeps its value. Conditional on the column identity: if the reviewer finds that the '{col}' column under 'C12 Based PAOs' is not this product, the row lapses and the record's source_documents entry for DL2-13200.pdf should be reviewed instead.",
            'propose_record_conflict', 'changed_or_conflicting', 'typical value (family typical-properties table)', f"CONDITIONAL: only if column '{col}' is confirmed to be this product", f'existing: {rec}',
            unit='cSt' if 'kv' in path else 'dimensionless', method='ASTM D 7042' if 'kv' in path else 'ASTM D 2270')
    row(pid, 'open_questions', 1, f"Record values from {single}.", f"Column '{col}' ('C12 Based PAOs'): {others}.",
        "The tier-2 differences (pour, flash, Noack) and the KV -40 °C difference are listed for the reviewer in the same conditional way; they are not recorded as separate conflicts here, and no value is changed. The question also asks Chevron Phillips which document is current.",
        'propose_open_question_update', 'additional', 'typical values beside the single-grade sheet', f"CONDITIONAL: only if column '{col}' is confirmed to be this product", 'existing: single-grade values only')

d = dict(batch='DL2-13200.pdf unlinked columns, batch 26 (eighteenth pass)', reviewed_on='2026-11-14 (eighteenth pass)',
         note="Nine reviewer-recorded links (C10 Dimer, C12 Dimer, 2, 4, 6, 8 cSt equal their records; 5, 7, 9 cSt differ). Every column of the sheet now has a product: 2.5 cSt was linked in batch 20. No column is out of scope and none is left without a record.",
         documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzz_b26_dl2_13200_columns_eighteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
