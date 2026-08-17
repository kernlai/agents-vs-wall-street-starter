from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from forecasting import (
    challenge_forecast,
    compile_forecast,
    load_company_profile,
    resolve_management_guidance,
    write_run_receipt,
)


QUOTE = "Revenue guidance is $3.9 billion, plus or minus $100 million."


class RunReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        source_path = self.root / "filing.md"
        source_path.write_text(f"# Results\n\n{QUOTE}\n", encoding="utf-8")
        source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        claim = {"claim": "Example profile fact.", "sourceIds": ["filing"]}
        anchor = {
            "id": "guidance",
            "signal": "Management revenue guidance",
            "targetMetric": "EX_REVENUE_Q3",
            "role": "anchor",
            "hypothesis": "Latest guidance is the starting range.",
            "expectedDirection": "range",
            "targetPeriod": "FY2026Q3",
            "units": "USDm",
            "importance": "primary",
            "resolver": "extract_management_guidance",
            "evidenceRequired": ["latest earnings release"],
            "combinationMethod": "forecast_starting_range",
            "freshnessRequirement": "latest available guidance",
            "correlationGroup": "management_guidance",
            "status": "pending",
        }
        missing_driver = {
            "id": "orders",
            "signal": "Verified target-quarter orders",
            "targetMetric": "EX_REVENUE_Q3",
            "role": "driver",
            "hypothesis": "Verified incremental orders change revenue.",
            "expectedDirection": "up",
            "targetPeriod": "FY2026Q3",
            "units": "USDm",
            "importance": "primary",
            "resolver": "resolve_explicit_driver",
            "evidenceRequired": ["order evidence and conversion bridge"],
            "combinationMethod": "additive_adjustment",
            "freshnessRequirement": "current target-period evidence",
            "correlationGroup": "demand_pipeline",
            "status": "pending",
        }
        data = {
            "schemaVersion": "1.0",
            "company": {
                "id": "EX",
                "name": "Example Company",
                "ticker": "EX",
                "currency": "USD",
                "fiscalCalendar": "52/53-week year",
            },
            "informationCutoff": "2026-08-16T17:15:00+01:00",
            "sources": [
                {
                    "id": "filing",
                    "publisher": "Example Company",
                    "title": "Quarterly results",
                    "documentType": "earnings_release",
                    "publishedAt": "2026-05-20",
                    "url": "https://example.com/filing",
                    "localPath": "filing.md",
                    "sha256": source_hash,
                }
            ],
            "profile": {
                "businessModel": [claim],
                "productsAndCustomers": [claim],
                "segmentsAndGeographies": [claim],
                "fiscalCalendar": [claim],
                "revenueAndCostDrivers": [claim],
                "accountingDefinitions": [claim],
                "guidanceStyle": [claim],
                "cyclicalityAndSeasonality": [claim],
                "externalExposures": [claim],
            },
            "metrics": [
                {
                    "id": "EX_REVENUE_Q3",
                    "name": "Revenue",
                    "units": "USDm",
                    "targetPeriod": "FY2026Q3",
                    "accountingBasis": "reported",
                }
            ],
            "signalMap": [anchor, missing_driver],
        }
        profile_path = self.root / "profile.json"
        profile_path.write_text(json.dumps(data), encoding="utf-8")
        self.profile = load_company_profile(profile_path, repository_root=self.root)
        anchor_observation = resolve_management_guidance(
            self.profile,
            signal_id="guidance",
            source_id="filing",
            exact_quote=QUOTE,
            locator="Outlook",
            low="3800",
            high="4000",
            units="USDm",
            period="FY2026Q3",
        )
        self.result = compile_forecast(self.profile, "EX_REVENUE_Q3", [anchor_observation])

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_receipt_preserves_source_to_formula_chain_and_is_replay_stable(self) -> None:
        report = challenge_forecast(self.profile, self.result)
        first = self.root / "first.json"
        second = self.root / "second.json"

        write_run_receipt(self.profile, self.result, report, first)
        write_run_receipt(self.profile, self.result, report, second)

        self.assertEqual(first.read_bytes(), second.read_bytes())
        receipt = json.loads(first.read_text(encoding="utf-8"))
        accepted = receipt["decisions"]["accepted"][0]
        self.assertEqual(receipt["forecast"]["baseForecast"], "3900")
        self.assertEqual(receipt["forecast"]["formula"], "midpoint(3800, 4000) + 0 = 3900 USDm")
        self.assertEqual(accepted["observation"]["provenance"]["sourceUrl"], "https://example.com/filing")
        self.assertEqual(accepted["observation"]["provenance"]["exactQuote"], QUOTE)
        self.assertEqual(
            accepted["observation"]["provenance"]["sourceSha256"],
            self.profile.sources["filing"].sha256,
        )
        self.assertFalse(receipt["challenge"]["passed"])
        self.assertEqual(receipt["challenge"]["issues"][0]["code"], "MISSING_PRIMARY_SIGNAL")
        self.assertEqual(receipt["challenge"]["issues"][0]["signalId"], "orders")


if __name__ == "__main__":
    unittest.main()
