# Decision generators

Each `gen_*.py` writes one file in `../../decisions/`. Run with `PYTHONDONTWRITEBYTECODE=1`; each script changes to the
workspace root first.

- **Thirteenth pass:** `gen_b1_synfluid.py` … `gen_b7_d3503.py` reproduce the decision files of this pass. b1 and b2 were
  verified byte-identical after saving.
- **Older generators (eleventh and twelfth passes):** saved for the record but NOT re-run. A later decision file may override
  their rows. Compare bytes before regenerating.
