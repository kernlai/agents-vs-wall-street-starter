from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from forecasting import ProfileValidationError, load_company_profile


class CompanyProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source_path = self.root / "filing.md"
        self.source_path.write_text("Management guidance quotation.\n", encoding="utf-8")
        self.source_hash = hashlib.sha256(self.source_path.read_bytes()).hexdigest()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _profile(self) -> dict:
        claim = {"claim": "Example company sells semiconductors.", "sourceIds": ["filing"]}
        return {
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
                    "publishedAt": "2026-05-20T07:00:00-04:00",
                    "url": "https://example.com/filing",
                    "localPath": "filing.md",
                    "sha256": self.source_hash,
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
            "signalMap": [
                {
                    "id": "management_revenue_guidance",
                    "signal": "Management revenue guidance",
                    "targetMetric": "EX_REVENUE_Q3",
                    "role": "anchor",
                    "hypothesis": "Latest guidance is the direct starting range.",
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
            ],
        }

    def _write_profile(self, data: dict) -> Path:
        path = self.root / "profile.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_loads_source_backed_profile_and_signal_map(self) -> None:
        profile = load_company_profile(self._write_profile(self._profile()), repository_root=self.root)

        self.assertEqual(profile.company.company_id, "EX")
        self.assertEqual(profile.metrics["EX_REVENUE_Q3"].units, "USDm")
        self.assertEqual(profile.signals["management_revenue_guidance"].role.value, "anchor")
        self.assertEqual(profile.sources["filing"].sha256, self.source_hash)

    def test_rejects_profile_claim_with_unknown_source(self) -> None:
        data = self._profile()
        data["profile"]["businessModel"][0]["sourceIds"] = ["missing"]

        with self.assertRaisesRegex(ProfileValidationError, "unknown source missing"):
            load_company_profile(self._write_profile(data), repository_root=self.root)


if __name__ == "__main__":
    unittest.main()
