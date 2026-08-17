from __future__ import annotations

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

import example


class ExampleRunTests(unittest.TestCase):
    def test_runs_real_adi_example_and_writes_provenance_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "adi-receipt.json"

            result, report = example.run(output)

            self.assertEqual(result.base_range.low, Decimal("3800"))
            self.assertEqual(result.base_forecast, Decimal("3900"))
            self.assertEqual(result.base_range.high, Decimal("4000"))
            self.assertTrue(report.passed)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(receipt["company"]["ticker"], "ADI")
            self.assertEqual(receipt["forecast"]["baseForecast"], "3900")
            self.assertEqual(
                receipt["sources"][0]["url"],
                "https://www.sec.gov/Archives/edgar/data/6281/000000628126000050/adi2q26exhibit991earnings.htm",
            )
            self.assertIn(
                "we are forecasting revenue of $3.9 billion",
                receipt["decisions"]["accepted"][0]["observation"]["provenance"]["exactQuote"],
            )


if __name__ == "__main__":
    unittest.main()
