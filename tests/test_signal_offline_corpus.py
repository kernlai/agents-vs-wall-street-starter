from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from signal_agent.models import Company
from signal_agent.offline_corpus import build_offline_context


class OfflineCorpusTests(unittest.TestCase):
    def test_returns_bounded_metric_relevant_context(self) -> None:
        company = Company(
            company_id="HAS", name="Hays plc", ticker="LSE:HAS",
            financial_fact_targets=({"metric": "Net fees", "unit": "GBPm"},),
        )
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "hays" / "filings"
            directory.mkdir(parents=True)
            (directory / "2026-report.md").write_text(
                "---\npublished_at: \"2026-08-03\"\nperiod: \"FY2026\"\n"
                "document_type: \"filing\"\n---\n# Results\n\n"
                "Net fees for the year were £1,000 million after a mixed regional performance.\n"
            )
            context = build_offline_context(company, corpus_root=temporary, character_limit=2_000)

        self.assertIn("Net fees", context)
        self.assertIn("2026-08-03", context)
        self.assertLessEqual(len(context), 2_000)

    def test_missing_company_corpus_is_explicit(self) -> None:
        company = Company(company_id="UNKNOWN", name="Unknown", ticker="UNKNOWN")
        self.assertIn("No supplied offline corpus", build_offline_context(company))


if __name__ == "__main__":
    unittest.main()
