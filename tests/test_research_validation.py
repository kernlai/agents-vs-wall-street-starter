from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from signal_agent.research_validation import (
    ResearchValidationError,
    build_forecast_input_v2,
    validate_profile_candidate,
    validate_signal_map,
)
from signal_agent.tavily import canonical_manifest_sha256, freeze_source


class ResearchValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source = freeze_source(
            {
                "url": "https://example.com/results",
                "title": "Results",
                "publisher": "Example Co",
                "published_date": "2026-05-20",
                "raw_content": "Management expects revenue of $100 million. Demand is stable.\n",
            },
            self.root,
            query_id="profile-businessModel",
            request_id="request-1",
            information_cutoff="2026-08-16T17:15:00+01:00",
            retrieved_at="2026-08-16T12:00:00Z",
        )
        self.metric = {
            "id": "EX_REVENUE_Q3", "name": "Revenue", "units": "USDm",
            "targetPeriod": "FY2026Q3", "accountingBasis": "reported",
        }

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _signals(self) -> list[dict]:
        common = {
            "targetMetric": "EX_REVENUE_Q3", "targetPeriod": "FY2026Q3",
            "importance": "material", "freshnessRequirement": "latest before cutoff",
            "status": "approved", "accountingBasis": "reported",
        }
        return [
            {
                **common, "id": "guidance", "signal": "Guidance", "role": "anchor",
                "hypothesis": "Guidance is the starting range", "expectedDirection": "range",
                "units": "USDm", "resolver": "extract_management_guidance",
                "evidenceRequired": ["official guidance"], "combinationMethod": "forecast_starting_range",
                "correlationGroup": "guidance",
            },
            {
                **common, "id": "orders", "signal": "Orders", "role": "driver",
                "hypothesis": "Orders affect shipments", "expectedDirection": "positive",
                "units": "USDm", "resolver": "extract_explicit_driver",
                "evidenceRequired": ["quantified orders"], "combinationMethod": "additive_adjustment",
                "correlationGroup": "demand",
            },
            {
                **common, "id": "demand_tone", "signal": "Demand tone", "role": "modifier",
                "hypothesis": "Tone explains range selection", "expectedDirection": "qualitative",
                "units": "text", "resolver": "extract_qualitative_modifier",
                "evidenceRequired": ["management commentary"], "combinationMethod": "qualitative_only",
                "correlationGroup": "demand",
            },
        ]

    def test_validates_complete_source_backed_profile_and_three_to_seven_signal_map(self) -> None:
        sections = (
            "businessModel", "productsAndCustomers", "segmentsAndGeographies", "fiscalCalendar",
            "revenueAndCostDrivers", "accountingDefinitions", "guidanceStyle",
            "cyclicalityAndSeasonality", "externalExposures",
        )
        profile = {
            section: [{
                "claimId": f"claim-{index}", "claim": "Example Co has a guidance-led model.",
                "sourceIds": [self.source["id"]],
                "exactQuotes": ["Management expects revenue of $100 million."],
            }]
            for index, section in enumerate(sections, start=1)
        }
        receipt = validate_profile_candidate(profile, [self.source], self.root)
        signal_receipt = validate_signal_map([self.metric], self._signals())

        self.assertEqual(receipt["status"], "accepted")
        self.assertEqual(receipt["acceptedClaimCount"], 9)
        self.assertEqual(signal_receipt["status"], "accepted")
        self.assertEqual(signal_receipt["metrics"]["EX_REVENUE_Q3"]["signalCount"], 3)

    def test_rejects_incomplete_map_weights_and_bad_role_formula(self) -> None:
        with self.assertRaisesRegex(ResearchValidationError, "between 3 and 7"):
            validate_signal_map([self.metric], self._signals()[:2])
        weighted = self._signals()
        weighted[2]["weight"] = "0.4"
        with self.assertRaisesRegex(ResearchValidationError, "weights are forbidden"):
            validate_signal_map([self.metric], weighted)
        wrong = self._signals()
        wrong[1]["combinationMethod"] = "qualitative_only"
        with self.assertRaisesRegex(ResearchValidationError, "unsupported resolver/combination"):
            validate_signal_map([self.metric], wrong)

    def test_forecast_input_v2_requires_reconstructable_decimal_observation_and_passed_review(self) -> None:
        manifest_hash = canonical_manifest_sha256([self.source])
        audit = {
            "schemaVersion": "research_audit.v1", "provider": "openai", "model": "test-model",
            "modelKnowledgeCutoff": "unknown", "requestId": "model-request-1",
            "promptSha256": "a" * 64, "inputManifestSha256": manifest_hash,
            "suppliedSourceIds": [self.source["id"]], "claims": [], "rejectedEvidence": [],
            "reasoningSummary": "Selected direct management guidance.",
            "createdAt": "2026-08-16T12:01:00Z",
        }
        review = {
            "schemaVersion": "lookahead_review.v1", "status": "passed", "issues": [],
            "provider": "openai", "model": "review-model", "requestId": "review-request-1",
        }
        observation = {
            "observationId": "obs-1", "signalId": "guidance", "targetMetricId": "EX_REVENUE_Q3",
            "period": "FY2026Q3", "units": "USDm", "accountingBasis": "reported",
            "value": {"low": "95", "high": "105"}, "sourceId": self.source["id"],
            "exactQuote": "Management expects revenue of $100 million.",
            "deterministicStatus": "accepted",
        }
        result = build_forecast_input_v2(
            company_id="EX", profile_receipt={"status": "accepted"},
            signal_map_receipt=validate_signal_map([self.metric], self._signals()),
            observations=[observation], sources=[self.source], source_root=self.root,
            research_audit=audit, lookahead_review=review,
        )
        self.assertEqual(result["schemaVersion"], "forecast_input.v2")
        self.assertEqual(result["provenanceManifestSha256"], manifest_hash)
        self.assertEqual(result["observations"][0]["value"]["low"], "95")

        numeric = [{**observation, "value": {"low": 95.0, "high": "105"}}]
        with self.assertRaisesRegex(ResearchValidationError, "decimal string"):
            build_forecast_input_v2(
                company_id="EX", profile_receipt={"status": "accepted"},
                signal_map_receipt=validate_signal_map([self.metric], self._signals()),
                observations=numeric, sources=[self.source], source_root=self.root,
                research_audit=audit, lookahead_review=review,
            )

        blocked = {
            **review, "status": "blocked_for_lookahead",
            "issues": [{"code": "POST_CUTOFF_FACT", "severity": "error", "claimIds": ["obs-1"],
                        "sourceIds": [self.source["id"]], "explanation": "Period leakage."}],
        }
        with self.assertRaisesRegex(ResearchValidationError, "look-ahead review"):
            build_forecast_input_v2(
                company_id="EX", profile_receipt={"status": "accepted"},
                signal_map_receipt=validate_signal_map([self.metric], self._signals()),
                observations=[observation], sources=[self.source], source_root=self.root,
                research_audit=audit, lookahead_review=blocked,
            )


if __name__ == "__main__":
    unittest.main()
