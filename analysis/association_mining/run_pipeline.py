"""
Step 11 — End-to-end pipeline runner for Pipeline B (association mining).

Runs Steps 4 -> 6 -> 7 -> 8 -> 9 -> 10 in sequence, verifies expected
output files after each step, and prints a timed summary table.

Usage:
    python analysis/association_mining/run_pipeline.py
    python analysis/association_mining/run_pipeline.py \\
        --json-input Products_json \\
        --output     analysis/association_mining/outputs \\
        --from-step  4

Options:
    --json-input PATH   Source JSON folder for Step 4 (default: Products_json)
    --output PATH       All step outputs land here (default: analysis/association_mining/outputs)
    --from-step N       Skip steps before N (4..10); useful when earlier outputs exist
    --min-sup FLOAT     Passed to Step 10 (default 0.05)
    --min-conf FLOAT    Passed to Step 10 (default 0.50)
    --check             Verify expected outputs exist without running any steps

Exit codes: 0 = success, 1 = one or more steps failed.
"""

from __future__ import annotations

import argparse
import importlib
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

# ---------------------------------------------------------------------------
# Step registry
# ---------------------------------------------------------------------------

# Each entry: (step_number, label, module_name, expected_outputs)
# args_fn(json_dir, out_dir, extra) -> list[str] passed to step's main()
_STEPS: list[dict] = [
    {
        "number": 4,
        "label":  "Data extraction",
        "module": "analysis.association_mining.run_extraction",
        "outputs": ["bo_features.csv", "ap_features.csv", "treat_rate.csv"],
        "args_fn": lambda j, o, _: ["--input", j, "--output", o],
    },
    {
        "number": 6,
        "label":  "Feature engineering",
        "module": "analysis.association_mining.run_feature_engineering",
        "outputs": ["bo_ml.csv", "ap_ml.csv"],
        "args_fn": lambda j, o, _: ["--input", o, "--output", o],
    },
    {
        "number": 7,
        "label":  "Similarity & clustering",
        "module": "analysis.association_mining.run_similarity",
        "outputs": ["bo_clusters.csv", "ap_clusters.csv", "bo_top_pairs.csv", "ap_top_pairs.csv"],
        "args_fn": lambda j, o, _: ["--input", o, "--output", o],
    },
    {
        "number": 8,
        "label":  "SAE compatibility mapping",
        "module": "analysis.association_mining.run_compatibility",
        "outputs": ["formulation_candidates.csv", "compatibility_matrix.csv"],
        "args_fn": lambda j, o, _: ["--input", o, "--output", o],
    },
    {
        "number": 9,
        "label":  "Candidate scoring & ranking",
        "module": "analysis.association_mining.run_ranking",
        "outputs": ["formulation_ranked.csv"],
        "args_fn": lambda j, o, _: ["--input", o, "--output", o],
    },
    {
        "number": 10,
        "label":  "Association rule mining",
        "module": "analysis.association_mining.run_association",
        "outputs": ["association_rules.csv"],
        "args_fn": lambda j, o, x: [
            "--input",    o,
            "--output",   o,
            "--min-sup",  str(x.get("min_sup",  0.05)),
            "--min-conf", str(x.get("min_conf", 0.50)),
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def check_outputs(out_dir: pathlib.Path, expected: list[str]) -> list[str]:
    """Return list of missing or empty expected output files."""
    missing = []
    for name in expected:
        p = out_dir / name
        if not p.exists() or p.stat().st_size == 0:
            missing.append(name)
    return missing


def _row(number, label, status, elapsed, missing):
    elapsed_s = f"{elapsed:.1f}s" if elapsed is not None else "-"
    flag = ""
    if missing:
        flag = f"  MISSING: {', '.join(missing)}"
    return f"  Step {number:<3} {label:<30} {status:<8} {elapsed_s:>7}{flag}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pipeline B end-to-end runner"
    )
    parser.add_argument("--json-input", default="Products_json",
                        help="Source JSON folder for Step 4")
    parser.add_argument("--output", default="analysis/association_mining/outputs",
                        help="Output directory for all steps")
    parser.add_argument("--from-step", type=int, default=4, metavar="N",
                        help="Skip steps before N (4..10)")
    parser.add_argument("--min-sup",  type=float, default=0.05)
    parser.add_argument("--min-conf", type=float, default=0.50)
    parser.add_argument("--check", action="store_true",
                        help="Only verify outputs exist; do not run steps")
    args = parser.parse_args(argv)

    json_dir = str(pathlib.Path(args.json_input).resolve())
    out_dir  = pathlib.Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    extra = {"min_sup": args.min_sup, "min_conf": args.min_conf}

    # --- Check mode ---
    if args.check:
        print("Checking pipeline outputs …")
        all_ok = True
        for step in _STEPS:
            missing = check_outputs(out_dir, step["outputs"])
            status = "OK" if not missing else "MISSING"
            if missing:
                all_ok = False
            print(_row(step["number"], step["label"], status, None, missing))
        return 0 if all_ok else 1

    # --- Run mode ---
    t_pipeline = time.monotonic()
    print(f"Pipeline B — running steps {args.from_step}..10")
    print(f"  JSON input : {json_dir}")
    print(f"  Output dir : {out_dir}")
    print()

    summary: list[tuple] = []   # (number, label, status, elapsed, missing)
    failed = False

    for step in _STEPS:
        n = step["number"]
        if n < args.from_step:
            summary.append((n, step["label"], "SKIPPED", None, []))
            continue

        label  = step["label"]
        module = step["module"]
        step_args = step["args_fn"](json_dir, str(out_dir), extra)

        print(f"--- Step {n}: {label} ---")
        t0 = time.monotonic()
        try:
            mod = importlib.import_module(module)
            mod.main(step_args)
            elapsed = time.monotonic() - t0
            missing = check_outputs(out_dir, step["outputs"])
            if missing:
                status = "WARN"
                print(f"  WARNING: missing outputs: {', '.join(missing)}")
            else:
                status = "OK"
            summary.append((n, label, status, elapsed, missing))
            if missing:
                failed = True
                break
        except SystemExit as e:
            elapsed = time.monotonic() - t0
            print(f"  FAILED (SystemExit: {e})")
            summary.append((n, label, "FAILED", elapsed, []))
            failed = True
            break
        except Exception as e:
            elapsed = time.monotonic() - t0
            print(f"  FAILED: {e}")
            summary.append((n, label, "FAILED", elapsed, []))
            failed = True
            break
        print()

    total = time.monotonic() - t_pipeline

    # Print summary table
    print("=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    for row in summary:
        print(_row(*row))
    print(f"\n  Total time: {total:.1f}s")
    print("=" * 60)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
