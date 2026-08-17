from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from signal_agent.tavily import (
    TavilyClient,
    canonical_manifest_sha256,
    freeze_source,
    load_tavily_api_key,
    plan_profile_queries,
    plan_signal_queries,
    verify_frozen_quote,
)


class RecordingTransport:
    def __init__(self, responses: list[dict]) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[str, dict, dict]] = []

    def post(self, url: str, payload: dict, headers: dict, timeout: int) -> dict:
        self.calls.append((url, payload, headers))
        return self.responses.pop(0)


class TavilyResearchTests(unittest.TestCase):
    def test_loads_key_without_overriding_environment_or_exposing_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text("TAVILY_API_KEY=file-secret\nOTHER=value\n")
            previous = os.environ.get("TAVILY_API_KEY")
            os.environ["TAVILY_API_KEY"] = "process-secret"
            try:
                self.assertEqual(load_tavily_api_key(env_file), "process-secret")
            finally:
                if previous is None:
                    os.environ.pop("TAVILY_API_KEY", None)
                else:
                    os.environ["TAVILY_API_KEY"] = previous

    def test_tavily_search_and_batch_extract_use_bounded_requests(self) -> None:
        transport = RecordingTransport(
            [
                {"request_id": "search-1", "results": [{"url": "https://example.com/a"}]},
                {"request_id": "extract-1", "results": [{"url": "https://example.com/a", "raw_content": "A"}]},
            ]
        )
        client = TavilyClient("secret", transport=transport, max_results=4, max_extract_urls=2)

        search = client.search(
            "Example filing", include_domains=["example.com"], max_results=99,
            end_date="2026-08-16",
        )
        extracted = client.extract(["https://example.com/a"])

        self.assertEqual(search["request_id"], "search-1")
        self.assertEqual(extracted["request_id"], "extract-1")
        self.assertEqual(transport.calls[0][1]["max_results"], 4)
        self.assertEqual(transport.calls[0][1]["end_date"], "2026-08-16")
        self.assertNotIn("api_key", transport.calls[0][1])
        self.assertEqual(transport.calls[0][2]["Authorization"], "Bearer secret")
        with self.assertRaisesRegex(ValueError, "at most 2"):
            client.extract(["https://example.com/1", "https://example.com/2", "https://example.com/3"])

    def test_profile_plan_covers_all_nine_sections_and_signal_plan_is_approved_only(self) -> None:
        company = {
            "company_id": "ADI",
            "name": "Analog Devices, Inc.",
            "ticker": "ADI",
            "investor_relations_url": "https://investor.analog.com/",
            "regulator_urls": ["https://www.sec.gov/edgar/browse/?CIK=6281"],
        }
        profile_queries = plan_profile_queries(company, "2026-08-16T17:15:00+01:00")
        self.assertEqual(len(profile_queries), 9)
        self.assertEqual(len({item["profile_section"] for item in profile_queries}), 9)
        self.assertTrue(all("2026-08-16" in item["query"] for item in profile_queries))
        self.assertTrue(all(item["end_date"] == "2026-08-16" for item in profile_queries))
        self.assertTrue(all("sec.gov" in item["include_domains"] for item in profile_queries))

        metric = {"id": "ADI_REVENUE_Q3", "name": "Revenue", "units": "USDm", "targetPeriod": "FY2026Q3"}
        signals = [
            {
                "id": "guidance", "signal": "Management guidance", "targetMetric": "ADI_REVENUE_Q3",
                "status": "approved", "hypothesis": "Guidance anchors revenue", "units": "USDm",
                "freshnessRequirement": "latest", "evidenceRequired": ["official earnings release"],
            },
            {
                "id": "sentiment", "signal": "Generic sentiment", "targetMetric": "ADI_REVENUE_Q3",
                "status": "pending", "hypothesis": "Sentiment may correlate", "units": "text",
                "freshnessRequirement": "latest", "evidenceRequired": ["news"],
            },
        ]
        signal_queries = plan_signal_queries(company, metric, signals, "2026-08-16T17:15:00+01:00")
        self.assertEqual([item["signal_id"] for item in signal_queries], ["guidance"])
        self.assertIn("official earnings release", signal_queries[0]["query"])

    def test_freeze_hash_manifest_cutoff_and_exact_quote_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = {
                "url": "https://example.com/results#section",
                "title": "Quarterly results",
                "publisher": "Example Co",
                "published_date": "2026-05-20T07:00:00-04:00",
                "raw_content": "Revenue guidance is $3.9 billion.\nSecond line.\n",
            }
            record = freeze_source(
                result,
                root,
                query_id="profile-guidance",
                request_id="request-1",
                information_cutoff="2026-08-16T17:15:00+01:00",
                retrieved_at="2026-08-16T12:00:00Z",
            )
            frozen_path = root / record["localPath"]
            self.assertTrue(frozen_path.is_file())
            self.assertEqual(record["sha256"], hashlib.sha256(frozen_path.read_bytes()).hexdigest())
            self.assertEqual(record["url"], "https://example.com/results")
            self.assertEqual(record["cutoffDecision"], "accepted")
            self.assertTrue(verify_frozen_quote(record, "Revenue guidance is $3.9 billion.", root))
            self.assertFalse(verify_frozen_quote(record, "Invented quotation", root))

            manifest_hash = canonical_manifest_sha256([record])
            self.assertEqual(manifest_hash, canonical_manifest_sha256([json.loads(json.dumps(record))]))

            post_cutoff = freeze_source(
                {**result, "url": "https://example.com/late", "published_date": "2026-08-17"},
                root,
                query_id="late",
                request_id="request-2",
                information_cutoff="2026-08-16T17:15:00+01:00",
                retrieved_at=datetime.now(timezone.utc).isoformat(),
            )
            self.assertEqual(post_cutoff["cutoffDecision"], "rejected_post_cutoff")

            undated = freeze_source(
                {key: value for key, value in result.items() if key != "published_date"},
                root,
                query_id="undated",
                request_id="request-3",
                information_cutoff="2026-08-16T17:15:00+01:00",
                retrieved_at="2026-08-16T12:00:00Z",
            )
            self.assertEqual(undated["cutoffDecision"], "rejected_missing_publication_date")
            self.assertIsNone(undated["publishedAt"])
            self.assertTrue((root / undated["localPath"]).is_file())


if __name__ == "__main__":
    unittest.main()
