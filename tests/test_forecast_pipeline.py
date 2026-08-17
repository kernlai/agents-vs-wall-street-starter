from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from forecasting.aggregate import aggregate
from forecasting.cli import forecast_payload
from signal_agent.research_validation import (
    build_forecast_input_v2_1, validate_profile_candidate, validate_signal_map,
)
from signal_agent.tavily import canonical_manifest_sha256, freeze_source


class ForecastPipelineTests(unittest.TestCase):
    def test_v2_1_compiles_three_metrics_and_aggregates_four_companies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            quote = "Management expects each target metric to be between 95 and 105."
            source = freeze_source(
                {"url": "https://example.com/results", "title": "Results", "publisher": "Example",
                 "published_date": "2026-05-20", "raw_content": quote},
                root, query_id="q", request_id="r", information_cutoff="2026-08-16T17:15:00+01:00",
            )
            sections = (
                "businessModel", "productsAndCustomers", "segmentsAndGeographies", "fiscalCalendar",
                "revenueAndCostDrivers", "accountingDefinitions", "guidanceStyle",
                "cyclicalityAndSeasonality", "externalExposures",
            )
            profile = {name: [{"claimId": f"c-{i}", "claim": "Source-backed claim",
                               "sourceIds": [source["id"]], "exactQuotes": [quote]}]
                       for i, name in enumerate(sections)}
            metrics, signals, observations = [], [], []
            for index in range(3):
                metric_id = f"EX_METRIC_{index}"
                metrics.append({"id": metric_id, "name": f"Metric {index}", "units": "USDm",
                                "targetPeriod": "FY2026Q3", "accountingBasis": "reported"})
                common = {"targetMetric": metric_id, "targetPeriod": "FY2026Q3", "importance": "secondary",
                          "freshnessRequirement": "latest", "status": "approved", "accountingBasis": "reported"}
                anchor_id = f"anchor-{index}"
                signals.extend([
                    {**common, "id": anchor_id, "signal": "Guidance", "role": "anchor",
                     "hypothesis": "Guidance anchors forecast", "expectedDirection": "range", "units": "USDm",
                     "resolver": "extract_management_guidance", "evidenceRequired": ["guidance"],
                     "combinationMethod": "forecast_starting_range", "correlationGroup": f"guide-{index}"},
                    {**common, "id": f"tone-{index}", "signal": "Tone", "role": "modifier",
                     "hypothesis": "Tone adds context", "expectedDirection": "qualitative", "units": "text",
                     "resolver": "extract_qualitative_modifier", "evidenceRequired": ["commentary"],
                     "combinationMethod": "qualitative_only", "correlationGroup": f"tone-{index}"},
                    {**common, "id": f"risk-{index}", "signal": "Risk", "role": "modifier",
                     "hypothesis": "Risk adds context", "expectedDirection": "qualitative", "units": "text",
                     "resolver": "extract_qualitative_modifier", "evidenceRequired": ["risk"],
                     "combinationMethod": "qualitative_only", "correlationGroup": f"risk-{index}"},
                ])
                observations.append({"observationId": f"o-{index}", "signalId": anchor_id,
                                     "targetMetricId": metric_id, "period": "FY2026Q3", "units": "USDm",
                                     "accountingBasis": "reported", "value": {"low": "95", "high": "105"},
                                     "sourceId": source["id"], "exactQuote": quote, "locator": "Results guidance",
                                     "deterministicStatus": "accepted"})
            profile_receipt = validate_profile_candidate(profile, [source], root)
            map_receipt = validate_signal_map(metrics, signals)
            manifest = canonical_manifest_sha256([source])
            audit = {"schemaVersion": "research_audit.v1", "provider": "test", "model": "test",
                     "modelKnowledgeCutoff": "none", "requestId": "r", "promptSha256": hashlib.sha256(b"p").hexdigest(),
                     "inputManifestSha256": manifest, "suppliedSourceIds": [source["id"]], "claims": [],
                     "rejectedEvidence": [], "reasoningSummary": "fixture", "createdAt": "2026-08-16T12:00:00Z"}
            review = {"schemaVersion": "lookahead_review.v1", "status": "passed", "issues": [],
                      "provider": "test", "model": "test", "requestId": "review"}
            handoff = build_forecast_input_v2_1(
                company={"id": "EX", "name": "Example", "ticker": "EX", "currency": "USD", "fiscalCalendar": "calendar"},
                information_cutoff="2026-08-16T17:15:00+01:00", profile=profile, metrics=metrics, signals=signals,
                profile_receipt=profile_receipt, signal_map_receipt=map_receipt, observations=observations,
                sources=[source], source_root=root, research_audit=audit, lookahead_review=review,
            )
            result = forecast_payload("EX", handoff)
            self.assertEqual([item["value"] for item in result["forecasts"]], [100.0, 100.0, 100.0])

            forecasts = root / "forecasts"
            forecasts.mkdir()
            companies = {"companies": []}
            for ticker in ("HAS", "HD", "ADI", "DE"):
                names = [f"{ticker} metric {i}" for i in range(3)]
                companies["companies"].append({"ticker": ticker, "metrics": [{"label": name} for name in names]})
                (forecasts / f"{ticker}.json").write_text(json.dumps({"forecasts": [
                    {"metric": name, "value": i + 1.0} for i, name in enumerate(names)
                ]}))
            registry = root / "companies.json"
            registry.write_text(json.dumps(companies))
            self.assertEqual(len(aggregate(forecasts, registry)), 4)


if __name__ == "__main__":
    unittest.main()
