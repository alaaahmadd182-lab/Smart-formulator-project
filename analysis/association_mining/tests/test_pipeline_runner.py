"""Tests for run_pipeline.py — Step 11 end-to-end pipeline runner."""

import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from analysis.association_mining.run_pipeline import (
    check_outputs,
    _row,
    _STEPS,
    main,
)


# ---------------------------------------------------------------------------
# TestCheckOutputs
# ---------------------------------------------------------------------------

class TestCheckOutputs(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_all_present_returns_empty(self):
        (self.out / "a.csv").write_text("data", encoding="utf-8")
        (self.out / "b.csv").write_text("data", encoding="utf-8")
        self.assertEqual(check_outputs(self.out, ["a.csv", "b.csv"]), [])

    def test_missing_file_returned(self):
        missing = check_outputs(self.out, ["not_there.csv"])
        self.assertIn("not_there.csv", missing)

    def test_empty_file_reported_missing(self):
        (self.out / "empty.csv").write_text("", encoding="utf-8")
        missing = check_outputs(self.out, ["empty.csv"])
        self.assertIn("empty.csv", missing)

    def test_non_empty_file_not_reported(self):
        (self.out / "good.csv").write_text("col\nval\n", encoding="utf-8")
        self.assertEqual(check_outputs(self.out, ["good.csv"]), [])

    def test_empty_expected_list(self):
        self.assertEqual(check_outputs(self.out, []), [])

    def test_partial_missing(self):
        (self.out / "present.csv").write_text("x", encoding="utf-8")
        missing = check_outputs(self.out, ["present.csv", "absent.csv"])
        self.assertEqual(missing, ["absent.csv"])


# ---------------------------------------------------------------------------
# TestRowFormatter
# ---------------------------------------------------------------------------

class TestRowFormatter(unittest.TestCase):

    def test_ok_row_contains_label(self):
        line = _row(4, "Data extraction", "OK", 1.5, [])
        self.assertIn("Data extraction", line)
        self.assertIn("OK", line)
        self.assertIn("1.5s", line)

    def test_missing_row_contains_flag(self):
        line = _row(6, "Feature eng", "WARN", 2.0, ["bo_ml.csv"])
        self.assertIn("bo_ml.csv", line)
        self.assertIn("MISSING", line)

    def test_skipped_row_shows_dash(self):
        line = _row(4, "Data extraction", "SKIPPED", None, [])
        self.assertIn("-", line)
        self.assertNotIn("None", line)

    def test_step_number_included(self):
        line = _row(10, "Association", "OK", 0.1, [])
        self.assertIn("10", line)


# ---------------------------------------------------------------------------
# TestStepRegistry
# ---------------------------------------------------------------------------

class TestStepRegistry(unittest.TestCase):

    def test_all_required_steps_present(self):
        numbers = [s["number"] for s in _STEPS]
        for n in (4, 6, 7, 8, 9, 10):
            self.assertIn(n, numbers)

    def test_step5_not_a_runner(self):
        # EDA (step 5) is a library module, not a runner — must not be in registry
        numbers = [s["number"] for s in _STEPS]
        self.assertNotIn(5, numbers)

    def test_each_step_has_required_keys(self):
        for step in _STEPS:
            for key in ("number", "label", "module", "outputs", "args_fn"):
                self.assertIn(key, step, f"Step {step.get('number')} missing key {key!r}")

    def test_outputs_are_nonempty_lists(self):
        for step in _STEPS:
            self.assertIsInstance(step["outputs"], list)
            self.assertGreater(len(step["outputs"]), 0)

    def test_steps_ordered_by_number(self):
        numbers = [s["number"] for s in _STEPS]
        self.assertEqual(numbers, sorted(numbers))

    def test_args_fn_callable(self):
        for step in _STEPS:
            self.assertTrue(callable(step["args_fn"]))

    def test_args_fn_returns_list(self):
        for step in _STEPS:
            result = step["args_fn"]("/json", "/out", {})
            self.assertIsInstance(result, list)
            self.assertTrue(all(isinstance(a, str) for a in result))


# ---------------------------------------------------------------------------
# TestMainArgParsing
# ---------------------------------------------------------------------------

class TestMainArgParsing(unittest.TestCase):

    def test_check_mode_missing_outputs_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            ret = main(["--output", tmp, "--check"])
        # No outputs exist → non-zero
        self.assertNotEqual(ret, 0)

    def test_check_mode_all_outputs_present_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp)
            # Write all expected output files
            for step in _STEPS:
                for fname in step["outputs"]:
                    (out / fname).write_text("col\nval\n", encoding="utf-8")
            ret = main(["--output", tmp, "--check"])
        self.assertEqual(ret, 0)

    def test_from_step_beyond_last_skips_all(self):
        # --from-step 99 means no step runs; with --check outputs missing → nonzero
        with tempfile.TemporaryDirectory() as tmp:
            ret = main(["--output", tmp, "--check", "--from-step", "99"])
        # check mode still checks all — nonzero since nothing is there
        self.assertNotEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
