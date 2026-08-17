import tempfile
import unittest
import ssl
import json
from pathlib import Path

from signal_agent.models import Company, Finding
from signal_agent.forecast_input import build_forecast_input
from signal_agent.orchestrator import SignalOrchestrator
from signal_agent.providers import _verified_ssl_context
from signal_agent.reconcile import (
    _domain, _normalise_basis, _normalise_metric, _reconcile_facts,
    reconcile_findings, report_identity,
)
from signal_agent.store import SignalStore


def finding(agent_id: str, domain: str = "haysplc.com", period: str = "2026-06-30") -> Finding:
    return Finding(
        agent_id=agent_id,
        strategy="test",
        company_id="HAS",
        signal_type="financial_reports",
        report_title="Hays FY2026 results",
        report_type="full_year_results",
        fiscal_period="FY2026",
        period_end=period,
        published_at="2026-08-20",
        source_url=f"https://{domain}/results/fy2026",
        source_domain=domain,
        source_kind="company_ir" if domain == "haysplc.com" else "regulator",
        official=True,
        evidence="Official FY2026 results page names Hays and the reporting period.",
        document_url=f"https://{domain}/results/fy2026.pdf",
        extracted_facts=(
            {
                "metric": "Net fees", "value": 904.0, "unit": "GBPm",
                "fiscal_period": "FY2026", "basis": "reported",
                "page_or_section": "Financial results",
                "evidence": "Net fees were £904.0 million.",
            },
        ),
    )


class FakeProvider:
    def research(self, *, company, signal_type, agent_id, strategy, source_hints, prompt):
        number = int(agent_id.rsplit("-", 1)[1])
        domain = "fca.org.uk" if number == 5 else "haysplc.com"
        return [finding(agent_id, domain)]


class ReconciliationTests(unittest.TestCase):
    def test_forecast_handoff_filters_and_groups_confirmed_facts(self):
        findings = [finding(f"researcher-{index}") for index in range(1, 6)]
        signal = reconcile_findings(
            run_id="run-handoff", company_id="HAS", signal_type="financial_reports",
            findings=findings, agent_count=5,
        )
        handoff = build_forecast_input(signal.to_dict())
        self.assertEqual(handoff["schema_version"], "forecast_input.v1")
        self.assertEqual(len(handoff["facts"]), 1)
        self.assertEqual(len(handoff["metric_series"]), 1)
        self.assertEqual(handoff["facts"][0]["value"], 904.0)

    def test_all_challenge_companies_have_report_and_fact_targets(self):
        config = json.loads(Path("signal_agent/config/companies.json").read_text())
        companies = {item["company_id"]: item for item in config["companies"]}
        self.assertEqual(set(companies), {"HAS", "HD", "ADI", "DE"})
        for company in companies.values():
            self.assertGreaterEqual(len(company["financial_report_targets"]), 3)
            self.assertGreaterEqual(len(company["financial_fact_targets"]), 3)
        for company_id in ("HD", "ADI", "DE"):
            self.assertGreaterEqual(len(companies[company_id]["financial_observation_targets"]), 5)

    def test_driver_dimensions_are_not_collapsed(self):
        self.assertEqual(_normalise_metric("Group net fees growth"), "Net fees growth")
        self.assertEqual(
            _normalise_metric("Temp & Contracting net fee growth"),
            "Temporary and Contracting net fees growth",
        )
        self.assertEqual(_normalise_metric("Perm net fees growth"), "Permanent net fees growth")
        self.assertNotEqual(
            _normalise_basis("company-compiled analyst consensus"),
            _normalise_basis("management guidance"),
        )
        self.assertEqual(_normalise_basis("GAAP, consolidated, unaudited"), "reported")
        self.assertEqual(_normalise_basis("Unaudited consolidated segment results"), "reported")

    def test_equivalent_fact_wording_units_and_signs_reconcile(self):
        first = finding("researcher-1")
        raw = finding("researcher-2").to_dict()
        raw["extracted_facts"] = [{
            "metric": "Group net fees", "value": 904, "unit": "GBP m",
            "fiscal_period": "FY2026", "basis": "unaudited",
            "page_or_section": "Results", "evidence": "Net fees were £904m."
        }]
        second = Finding.from_dict(raw)
        facts = _reconcile_facts([first, second], 2)
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0].metric, "Net fees")
        self.assertEqual(facts[0].unit, "GBPm")
        self.assertEqual(facts[0].confidence, 1.0)

    def test_quarterly_and_trading_labels_share_an_event_identity(self):
        trading_raw = finding("researcher-1").to_dict()
        trading_raw["report_title"] = "Fourth Quarter Trading Statement"
        trading_raw["report_type"] = "trading_update"
        trading = Finding.from_dict(trading_raw)
        raw = trading.to_dict()
        raw["report_title"] = "Quarterly update for the three months ended 30 June 2026"
        raw["report_type"] = "quarterly_results"
        quarterly = Finding.from_dict(raw)
        self.assertEqual(report_identity(trading), report_identity(quarterly))

    def test_subdomains_share_one_source_family(self):
        self.assertEqual(
            _domain("https://rns-pdf.londonstockexchange.com/report.pdf"),
            "londonstockexchange.com",
        )

    def test_research_vocabulary_is_normalised_before_reconciliation(self):
        raw = finding("researcher-1").to_dict()
        raw["report_title"] = "Fourth Quarter Trading Statement"
        raw["report_type"] = "quarterly_results"
        raw["source_kind"] = "listing_exchange_rns"
        normalised = Finding.from_dict(raw)
        self.assertEqual(normalised.report_type, "trading_update")
        self.assertEqual(normalised.source_kind, "stock_exchange")

    def test_https_context_keeps_certificate_verification_enabled(self):
        context = _verified_ssl_context()
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_five_agent_consensus_is_high_confidence(self):
        findings = [finding(f"researcher-{index}") for index in range(1, 5)]
        findings.append(finding("researcher-5", "fca.org.uk"))
        signal = reconcile_findings(
            run_id="run-1", company_id="HAS", signal_type="financial_reports",
            findings=findings, agent_count=5,
        )
        self.assertEqual(signal.status, "confirmed")
        self.assertGreaterEqual(signal.confidence, 0.8)
        self.assertEqual(len(signal.reports[0].supporting_agents), 5)
        self.assertEqual(len(signal.reports[0].supporting_domains), 2)
        self.assertEqual(signal.reports[0].facts[0].value, 904.0)
        self.assertGreaterEqual(signal.metadata["extraction_confidence"], 0.9)

    def test_disagreement_creates_separate_report_identity(self):
        findings = [finding("researcher-1"), finding("researcher-2", period="2025-06-30")]
        signal = reconcile_findings(
            run_id="run-2", company_id="HAS", signal_type="financial_reports",
            findings=findings, agent_count=5,
        )
        self.assertEqual(len(signal.reports), 2)
        self.assertEqual(signal.status, "needs_review")

    def test_missing_required_report_reduces_signal_confidence(self):
        findings = [finding(f"researcher-{index}") for index in range(1, 6)]
        targets = (
            {"report_type": "full_year_results", "period_end": "2026-06-30"},
            {"report_type": "annual_report", "period_end": "2025-06-30"},
        )
        signal = reconcile_findings(
            run_id="run-coverage", company_id="HAS", signal_type="financial_reports",
            findings=findings, agent_count=5, expected_targets=targets,
        )
        self.assertEqual(signal.metadata["target_coverage"], 0.5)
        self.assertLess(signal.confidence, 0.9)
        self.assertIn("1/2 required report events found", signal.metadata["confidence_explanation"])
        self.assertIn("extraction confidence", signal.metadata["confidence_explanation"])

    def test_confirmed_value_conflicts_are_visible_as_warnings(self):
        findings = [finding(f"researcher-{index}") for index in range(1, 6)]
        changed = findings[-1].to_dict()
        changed["extracted_facts"] = [{**changed["extracted_facts"][0], "value": 905.0}]
        findings[-1] = Finding.from_dict(changed)
        signal = reconcile_findings(
            run_id="run-conflict", company_id="HAS", signal_type="financial_reports",
            findings=findings, agent_count=5,
        )
        self.assertEqual(signal.metadata["conflicting_confirmed_fact_count"], 1)
        self.assertTrue(any("alternative extracted values" in warning for warning in signal.warnings))

    def test_orchestrator_persists_company_scoped_source_memory(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SignalStore(Path(directory) / "signals.db")
            prompt = Path(directory) / "prompt.md"
            prompt.write_text("test prompt")
            orchestrator = SignalOrchestrator(FakeProvider(), store, prompt_path=prompt)
            company = Company(company_id="HAS", name="Hays plc", ticker="HAS", exchange="LSE")
            signal = orchestrator.collect(company)
            hints = store.source_hints("HAS", "financial_reports")
            store.close()
            self.assertEqual(signal.status, "confirmed")
            self.assertIn("haysplc.com", hints)
            self.assertIn("fca.org.uk", hints)


if __name__ == "__main__":
    unittest.main()
