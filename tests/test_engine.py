from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from forecasting import (
    compile_forecast,
    load_company_profile,
    resolve_explicit_driver,
    resolve_management_guidance,
    resolve_qualitative_modifier,
    resolve_scenario_trigger,
)


GUIDANCE_QUOTE = "Revenue guidance is $3.9 billion, plus or minus $100 million."
DEMAND_QUOTE = "Verified orders support a direct $25 million revenue adjustment."
BACKLOG_QUOTE = "Verified backlog supports a direct $15 million revenue adjustment."
MODIFIER_QUOTE = "Industrial demand remains constructive."
SCENARIO_QUOTE = "A proposed tariff would reduce target-quarter revenue if enacted."


class ForecastEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        source_path = self.root / "filing.md"
        source_path.write_text(
            (
                f"# Results\n\n{GUIDANCE_QUOTE}\n\n{DEMAND_QUOTE}\n\n{BACKLOG_QUOTE}"
                f"\n\n{MODIFIER_QUOTE}\n\n{SCENARIO_QUOTE}\n"
            ),
            encoding="utf-8",
        )
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
        demand_driver = {
            "id": "verified_orders",
            "signal": "Verified order adjustment",
            "targetMetric": "EX_REVENUE_Q3",
            "role": "driver",
            "hypothesis": "Incremental verified orders directly change target-quarter revenue.",
            "expectedDirection": "up",
            "targetPeriod": "FY2026Q3",
            "units": "USDm",
            "importance": "secondary",
            "resolver": "resolve_explicit_driver",
            "evidenceRequired": ["order evidence"],
            "combinationMethod": "additive_adjustment",
            "freshnessRequirement": "current target-period evidence",
            "correlationGroup": "demand_pipeline",
            "status": "pending",
        }
        backlog_driver = {**demand_driver, "id": "verified_backlog", "signal": "Verified backlog adjustment"}
        modifier = {
            "id": "industrial_demand_commentary",
            "signal": "Industrial demand commentary",
            "targetMetric": "EX_REVENUE_Q3",
            "role": "modifier",
            "hypothesis": "Current demand commentary helps interpret the guidance range without false precision.",
            "expectedDirection": "up",
            "targetPeriod": "FY2026Q3",
            "units": "qualitative",
            "importance": "secondary",
            "resolver": "resolve_qualitative_modifier",
            "evidenceRequired": ["current management commentary"],
            "combinationMethod": "range_selection_context",
            "freshnessRequirement": "current target-period evidence",
            "correlationGroup": "industrial_demand",
            "status": "pending",
        }
        scenario = {
            "id": "tariff_trigger",
            "signal": "Tariff enactment",
            "targetMetric": "EX_REVENUE_Q3",
            "role": "scenario_trigger",
            "hypothesis": "A tariff enacted in the target period creates a conditional downside.",
            "expectedDirection": "down",
            "targetPeriod": "FY2026Q3",
            "units": "USDm",
            "importance": "secondary",
            "resolver": "resolve_scenario_trigger",
            "evidenceRequired": ["tariff proposal and exposure estimate"],
            "combinationMethod": "conditional_additive_scenario",
            "freshnessRequirement": "effective in target period",
            "correlationGroup": "tariff_exposure",
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
            "signalMap": [anchor, demand_driver, backlog_driver, modifier, scenario],
        }
        profile_path = self.root / "profile.json"
        profile_path.write_text(json.dumps(data), encoding="utf-8")
        self.profile = load_company_profile(profile_path, repository_root=self.root)
        self.anchor = resolve_management_guidance(
            self.profile,
            signal_id="guidance",
            source_id="filing",
            exact_quote=GUIDANCE_QUOTE,
            locator="Outlook",
            low="3800",
            high="4000",
            units="USDm",
            period="FY2026Q3",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _driver(self, signal_id: str, quote: str, adjustment: str):
        return resolve_explicit_driver(
            self.profile,
            signal_id=signal_id,
            source_id="filing",
            exact_quote=quote,
            locator="Demand evidence",
            adjustment=adjustment,
            units="USDm",
            period="FY2026Q3",
            calculation=f"direct evidenced adjustment = {adjustment} USDm",
        )

    def test_combines_anchor_and_explicit_driver_with_decimal_arithmetic(self) -> None:
        driver = self._driver("verified_orders", DEMAND_QUOTE, "25")

        result = compile_forecast(self.profile, "EX_REVENUE_Q3", [self.anchor, driver])

        self.assertEqual(result.anchor_range.low, Decimal("3800"))
        self.assertEqual(result.anchor_range.high, Decimal("4000"))
        self.assertEqual(result.driver_adjustment, Decimal("25"))
        self.assertEqual(result.base_forecast, Decimal("3925"))
        self.assertEqual(result.base_range.low, Decimal("3825"))
        self.assertEqual(result.base_range.high, Decimal("4025"))
        self.assertEqual([item.observation.signal_id for item in result.accepted], ["guidance", "verified_orders"])
        self.assertEqual(result.formula, "midpoint(3800, 4000) + 25 = 3925 USDm")

    def test_rejects_correlated_drivers_instead_of_double_counting(self) -> None:
        orders = self._driver("verified_orders", DEMAND_QUOTE, "25")
        backlog = self._driver("verified_backlog", BACKLOG_QUOTE, "15")

        result = compile_forecast(self.profile, "EX_REVENUE_Q3", [self.anchor, orders, backlog])

        self.assertEqual(result.base_forecast, Decimal("3900"))
        self.assertEqual(result.driver_adjustment, Decimal("0"))
        self.assertEqual(len(result.rejected), 2)
        self.assertTrue(all(item.reason_code == "CORRELATED_SIGNAL_CONFLICT" for item in result.rejected))

    def test_keeps_qualitative_modifier_out_of_arithmetic_and_scenario_conditional(self) -> None:
        modifier = resolve_qualitative_modifier(
            self.profile,
            signal_id="industrial_demand_commentary",
            source_id="filing",
            exact_quote=MODIFIER_QUOTE,
            locator="Demand commentary",
            assessment="Supports the upper half of management's range, but has no calibrated weight.",
            period="FY2026Q3",
        )
        scenario = resolve_scenario_trigger(
            self.profile,
            signal_id="tariff_trigger",
            source_id="filing",
            exact_quote=SCENARIO_QUOTE,
            locator="Risk factors",
            condition="Tariff is enacted before the target quarter closes.",
            adjustment="-100",
            units="USDm",
            period="FY2026Q3",
            calculation="verified exposure estimate = -100 USDm",
        )

        result = compile_forecast(self.profile, "EX_REVENUE_Q3", [self.anchor, modifier, scenario])

        self.assertEqual(result.base_forecast, Decimal("3900"))
        self.assertEqual(result.driver_adjustment, Decimal("0"))
        self.assertEqual(result.modifiers, (modifier,))
        self.assertEqual(len(result.scenarios), 1)
        self.assertEqual(result.scenarios[0].forecast, Decimal("3800"))
        self.assertEqual(result.scenarios[0].condition, "Tariff is enacted before the target quarter closes.")
        self.assertIn("- 100", result.scenarios[0].formula)


if __name__ == "__main__":
    unittest.main()
