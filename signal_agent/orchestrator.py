from __future__ import annotations

import json
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .models import Company, Finding, ReconciledSignal
from .providers import ResearchProvider
from .reconcile import reconcile_findings, report_identity
from .store import SignalStore


STRATEGIES = (
    "Investor-relations first: locate the company's own results centre and report files.",
    "Regulator first: locate filings through the relevant securities regulator or national archive.",
    "Exchange first: locate official announcements through the listing exchange or RNS service.",
    "Document verification: find direct official PDF/HTML reports and verify dates and fiscal periods.",
    "Sceptical cross-check: independently challenge likely report identities and reject mirrors or aggregators.",
)


class SignalOrchestrator:
    def __init__(
        self, provider: ResearchProvider, store: SignalStore,
        *, prompt_path: str | Path = "signal_agent/prompts/financial_reports.md",
        worker_count: int = 5,
    ) -> None:
        self.provider = provider
        self.store = store
        self.prompt_path = Path(prompt_path)
        self.worker_count = worker_count

    def collect(self, company: Company, signal_type: str = "financial_reports") -> ReconciledSignal:
        if signal_type != "financial_reports":
            raise ValueError(f"Unsupported signal type: {signal_type}")
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:8]
        prompt = self.prompt_path.read_text()
        self.store.save_company(company)
        hints = self.store.source_hints(company.company_id, signal_type)
        findings: list[Finding] = []
        errors: list[str] = []
        with ThreadPoolExecutor(max_workers=self.worker_count) as executor:
            futures = {
                executor.submit(
                    self.provider.research,
                    company=company,
                    signal_type=signal_type,
                    agent_id=f"researcher-{index + 1}",
                    strategy=STRATEGIES[index % len(STRATEGIES)],
                    source_hints=hints if index < self.worker_count - 1 else [],
                    prompt=prompt,
                ): index
                for index in range(self.worker_count)
            }
            for future in as_completed(futures):
                try:
                    findings.extend(future.result())
                except Exception as error:  # one researcher must not abort the run
                    errors.append(f"researcher-{futures[future] + 1}: {error}")
        signal = reconcile_findings(
            run_id=run_id,
            company_id=company.company_id,
            signal_type=signal_type,
            findings=findings,
            agent_count=self.worker_count,
            expected_targets=company.financial_report_targets,
        )
        provider_metadata = {
            "model": getattr(self.provider, "model", "fixture"),
            "reasoning_effort": getattr(self.provider, "reasoning_effort", "n/a"),
            "worker_count": self.worker_count,
            "offline_corpus": "challenge/offline-data",
            "offline_corpus_frozen_at": "2026-08-14",
        }
        signal = ReconciledSignal(
            **{**signal.__dict__, "metadata": {**signal.metadata, **provider_metadata}}
        )
        if errors:
            signal = ReconciledSignal(
                **{**signal.__dict__, "warnings": signal.warnings + tuple(errors)}
            )
        self.store.save_run(signal, findings, report_identity)
        return signal

    @staticmethod
    def write_result(signal: ReconciledSignal, directory: str | Path = "signals") -> Path:
        output = Path(directory) / signal.company_id / signal.signal_type
        output.mkdir(parents=True, exist_ok=True)
        versioned = output / f"{signal.run_id}.json"
        versioned.write_text(json.dumps(signal.to_dict(), indent=2) + "\n")
        latest = output / "latest.json"
        latest.write_text(json.dumps(signal.to_dict(), indent=2) + "\n")
        return versioned
