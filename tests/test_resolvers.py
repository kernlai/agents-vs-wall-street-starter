from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from forecasting import (
    ObservationValidationError,
    load_company_profile,
    resolve_management_guidance,
)


QUOTE = "For the third quarter, we are forecasting revenue of $3.9 billion, +/- $100 million."


class GuidanceResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source_path = self.root / "filing.md"
        self.source_path.write_text(f"# Results\n\n{QUOTE}\n", encoding="utf-8")
        source_hash = hashlib.sha256(self.source_path.read_bytes()).hexdigest()
        claim = {"claim": "Example profile fact.", "sourceIds": ["filing"]}
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
        profile_path = self.root / "profile.json"
        profile_path.write_text(json.dumps(data), encoding="utf-8")
        self.profile = load_company_profile(profile_path, repository_root=self.root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_resolves_guidance_only_with_verified_quote_and_source_hash(self) -> None:
        observation = resolve_management_guidance(
            self.profile,
            signal_id="management_revenue_guidance",
            source_id="filing",
            exact_quote=QUOTE,
            locator="Outlook, paragraph 1",
            low="3800",
            high="4000",
            units="USDm",
            period="FY2026Q3",
        )

        self.assertEqual(observation.value.low, Decimal("3800"))
        self.assertEqual(observation.value.high, Decimal("4000"))
        self.assertEqual(observation.provenance.source_url, "https://example.com/filing")
        self.assertEqual(observation.provenance.exact_quote, QUOTE)
        self.assertEqual(observation.provenance.source_sha256, self.profile.sources["filing"].sha256)

    def test_rejects_quote_that_is_not_in_frozen_source(self) -> None:
        with self.assertRaisesRegex(ObservationValidationError, "exact quotation not found"):
            resolve_management_guidance(
                self.profile,
                signal_id="management_revenue_guidance",
                source_id="filing",
                exact_quote="Invented guidance.",
                locator="Outlook",
                low="3800",
                high="4000",
                units="USDm",
                period="FY2026Q3",
            )

    def test_rejects_source_changed_after_profile_validation(self) -> None:
        self.source_path.write_text(f"# Changed\n\n{QUOTE}\n", encoding="utf-8")

        with self.assertRaisesRegex(ObservationValidationError, "source hash mismatch"):
            resolve_management_guidance(
                self.profile,
                signal_id="management_revenue_guidance",
                source_id="filing",
                exact_quote=QUOTE,
                locator="Outlook",
                low="3800",
                high="4000",
                units="USDm",
                period="FY2026Q3",
            )


if __name__ == "__main__":
    unittest.main()
