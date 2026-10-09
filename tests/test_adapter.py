import copy
import json
from pathlib import Path
import unittest

from app import adapt
from review_core import InputError, review
from jev import normalize


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(Path("examples/case.json").read_text())
        self.policy = json.loads(Path("examples/policy.json").read_text())

    def test_removed_field_requires_review(self):
        parsed = adapt(self.case)
        self.assertEqual(parsed["subject"], "warehouse/sales.orders")
        self.assertIn("field_removed", parsed["flags"])
        self.assertTrue(any("schema.fields" in item for item in parsed["evidence"]))
        result = review(
            self.case, self.policy, lambda _: normalize("low", 0.99, self.policy), adapt
        )
        self.assertEqual(result["outcome"], "review")

    def test_rejects_mismatched_dataset_and_duplicate_fields(self):
        bad = copy.deepcopy(self.case)
        bad["after"]["outputs"][0]["name"] = "other"
        with self.assertRaises(InputError):
            adapt(bad)
        bad = copy.deepcopy(self.case)
        bad["before"]["outputs"][0]["facets"]["schema"]["fields"].append(
            {"name": "order_id", "type": "BIGINT"}
        )
        with self.assertRaises(InputError):
            adapt(bad)


if __name__ == "__main__":
    unittest.main()
