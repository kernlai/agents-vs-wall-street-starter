from __future__ import annotations

import json
import unittest
from pathlib import Path

from signal_agent.proposal import OpenAIProposalProvider, PROFILE_SECTIONS
from signal_agent.research_pipeline import ROOT, build_signal_map, load_challenge_metrics, offline_sources
from signal_agent.research_validation import validate_signal_map


class FakeTransport:
    def post(self, url, payload, headers, timeout):
        claim = {"claimId": "claim", "claim": "Supported claim", "quoteIds": ["quote-1"]}
        value = {
            "profile": {section: [{**claim, "claimId": f"claim-{index}"}]
                        for index, section in enumerate(PROFILE_SECTIONS)},
            "anchors": [
                {"metricId": f"metric-{index}", "quoteId": "quote-1",
                 "locator": "line 1", "low": "1", "high": "2", "reasoning": "Explicit range"}
                for index in range(3)
            ],
            "reasoningSummary": "Used explicit guidance.", "rejectedEvidence": [],
        }
        return {"id": "response-1", "output": [{"type": "message", "content": [
            {"type": "output_text", "text": json.dumps(value)}]}]}


class ResearchPipelineTests(unittest.TestCase):
    def test_challenge_config_builds_exactly_three_valid_signal_groups(self) -> None:
        metrics_by_company = load_challenge_metrics(ROOT / "challenge/companies.json")
        self.assertEqual(set(metrics_by_company), {"HAS", "HD", "ADI", "DE"})
        for metrics in metrics_by_company.values():
            self.assertEqual(len(metrics), 3)
            signals = build_signal_map(metrics)
            self.assertEqual(len(signals), 9)
            self.assertEqual(validate_signal_map(metrics, signals)["status"], "accepted")

    def test_offline_corpus_is_admissible_and_cutoff_bound(self) -> None:
        records = offline_sources("DE", "2026-08-16T17:15:00+01:00", limit=4)
        self.assertEqual(len(records), 4)
        self.assertTrue(all(item["publishedAt"] <= "2026-08-16" for item in records))
        self.assertTrue(all((ROOT / item["localPath"]).is_file() for item in records))

    def test_openai_proposal_uses_structured_responses_contract(self) -> None:
        provider = OpenAIProposalProvider(api_key="test", transport=FakeTransport())
        result, metadata = provider.propose({"metrics": []})
        self.assertEqual(len(result["anchors"]), 3)
        self.assertEqual(metadata["requestId"], "response-1")
        self.assertEqual(len(metadata["promptSha256"]), 64)


if __name__ == "__main__":
    unittest.main()
