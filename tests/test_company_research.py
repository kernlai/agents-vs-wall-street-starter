from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path

from signal_agent.company_research import collect_candidate_bundle, research_companies


class FakeClient:
    max_extract_urls = 2

    def __init__(self) -> None:
        self.search_calls = []
        self.extract_calls = []

    def search(self, query, *, include_domains=None, max_results=None, end_date=None):
        self.search_calls.append((query, include_domains, max_results))
        slug = query.rsplit(" ", 1)[-1]
        return {
            "request_id": f"search-{slug}",
            "results": [{
                "url": f"https://example.com/{slug}", "title": f"Result {slug}",
                "publisher": "Example Co", "published_date": "2026-05-20",
            }],
        }

    def extract(self, urls):
        self.extract_calls.append(urls)
        return {
            "request_id": "extract-1",
            "results": [{"url": url, "raw_content": f"Frozen content for {url}."} for url in urls],
            "failed_results": [],
        }


class CompanyResearchTests(unittest.TestCase):
    def test_collects_queries_freezes_sources_and_emits_manifest(self) -> None:
        queries = [
            {"query_id": "q-1", "profile_section": "businessModel", "query": "Example one", "include_domains": ["example.com"]},
            {"query_id": "q-2", "profile_section": "fiscalCalendar", "query": "Example two", "include_domains": ["example.com"]},
            {"query_id": "q-3", "profile_section": "guidanceStyle", "query": "Example three", "include_domains": ["example.com"]},
        ]
        with tempfile.TemporaryDirectory() as directory:
            client = FakeClient()
            bundle = collect_candidate_bundle(
                company_id="EX", kind="profile", queries=queries, client=client,
                output_directory=Path(directory), information_cutoff="2026-08-16T17:15:00+01:00",
                search_workers=2,
            )

            self.assertEqual(bundle["schemaVersion"], "research_candidate_bundle.v1")
            self.assertEqual(len(bundle["sources"]), 3)
            self.assertEqual(len(client.extract_calls), 2)
            self.assertEqual(bundle["unresolved"], [])
            self.assertEqual(len(bundle["provenanceManifestSha256"]), 64)
            self.assertTrue(all((Path(directory) / item["localPath"]).is_file() for item in bundle["sources"]))

    def test_company_lanes_preserve_success_when_one_lane_fails(self) -> None:
        def worker(company):
            if company["company_id"] == "BAD":
                raise RuntimeError("search unavailable")
            time.sleep(0.01)
            return {"companyId": company["company_id"], "status": "complete"}

        result = research_companies(
            [{"company_id": "GOOD"}, {"company_id": "BAD"}, {"company_id": "ALSO_GOOD"}],
            worker,
            max_workers=3,
        )
        self.assertEqual(set(result["completed"]), {"GOOD", "ALSO_GOOD"})
        self.assertEqual(set(result["failed"]), {"BAD"})
        self.assertIn("search unavailable", result["failed"]["BAD"])


if __name__ == "__main__":
    unittest.main()
