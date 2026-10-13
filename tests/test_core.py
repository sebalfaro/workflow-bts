"""Invented identifiers and facts only; no private pilot fixtures."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "bts_core", ROOT / "skills/bts-orquestador/scripts/bts_core.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


class CoreTests(unittest.TestCase):
    def test_identity_contradiction_is_review(self):
        self.assertEqual(core.central_dni("20-00000001-0"), "00000001")
        with self.assertRaises(core.InputReview):
            core.central_dni("20-00000001-0", "00000002")

    def test_no_digit_repair(self):
        with self.assertRaises(core.InputReview):
            core.identifier("00O00001", "DNI")

    def test_partial_name_is_not_silently_matched(self):
        self.assertFalse(core.name_candidate("PERSONA ALFA", "PERSONA ALPHA", True))
        # DEC-018 remains a documented semantic rule; helper isn't a validator.
        self.assertIn("DEC-018", (ROOT / "skills/bts-orquestador/references/reglas.md").read_text())

    def test_expiry_boundary_and_payment_period(self):
        self.assertTrue(core.expiry_at_least("2026-10-29", "2026-10-29"))
        self.assertFalse(core.expiry_at_least("2026-10-28", "2026-10-29"))
        self.assertTrue(core.period_in_range("2026-01", "2026-01", "2026-10"))
        self.assertFalse(core.period_in_range("2026-11", "2026-01", "2026-10"))

    def test_blank_end_is_only_allowed_for_high_registration(self):
        self.assertTrue(core.interval_covers("2026-10-01", None,
                        "2026-10-07", "2026-10-30", "L", True))
        with self.assertRaises(core.InputReview):
            core.interval_covers("2026-10-01", None,
                                 "2026-10-07", "2026-10-30", "M", True)

    def test_overlapping_limits_are_not_summed(self):
        with self.assertRaises(core.InputReview):
            core.compatible_expense_total([
                {"id": "a", "category": "joint", "amount": "10"},
                {"id": "b", "category": "medical", "amount": "5"}])

    def test_readback_detects_type_and_identity_change(self):
        before = {"spreadsheet_id": "synthetic-sheet", "tab_id": "synthetic-tab",
                  "row_context_id": "synthetic-context", "schema_hash": "synthetic-schema",
                  "cells": [{"a1": "C2", "type": "string", "value": "00000001"}]}
        after = copy.deepcopy(before)
        self.assertTrue(core.compare_readback(before, after))
        after["cells"][0]["type"] = "number"
        self.assertFalse(core.compare_readback(before, after))
        after = copy.deepcopy(before)
        after["row_context_id"] = "other-context"
        self.assertFalse(core.compare_readback(before, after))

    def test_dependency_closure_with_cycle(self):
        self.assertEqual(core.affected_results(["fact"],
                         {"result": ["fact", "central"], "central": ["result"]}),
                         ["central", "result"])


if __name__ == "__main__":
    unittest.main()
