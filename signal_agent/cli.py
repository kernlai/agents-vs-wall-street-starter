from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import Company
from .orchestrator import SignalOrchestrator
from .providers import FixtureResearchProvider, OpenAIWebResearchProvider
from .store import SignalStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect and reconcile company signals")
    parser.add_argument("--company", required=True, help="Company ID from the config file")
    parser.add_argument("--companies", default="signal_agent/config/companies.json")
    parser.add_argument("--signal", default="financial_reports")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        default="medium",
    )
    parser.add_argument("--database", default="data/signals.db")
    parser.add_argument("--output", default="signals")
    parser.add_argument("--fixtures", help="Use offline researcher fixtures from this directory")
    args = parser.parse_args()

    companies = json.loads(Path(args.companies).read_text())["companies"]
    try:
        company = Company.from_dict(next(item for item in companies if item["company_id"] == args.company))
    except StopIteration as error:
        raise SystemExit(f"Unknown company ID: {args.company}") from error

    provider = (
        FixtureResearchProvider(args.fixtures)
        if args.fixtures else OpenAIWebResearchProvider(
            model=args.model, reasoning_effort=args.reasoning_effort
        )
    )
    store = SignalStore(args.database)
    try:
        orchestrator = SignalOrchestrator(provider, store, worker_count=args.workers)
        signal = orchestrator.collect(company, args.signal)
        path = orchestrator.write_result(signal, args.output)
    finally:
        store.close()
    print(
        json.dumps(
            {
                "status": signal.status,
                "confidence": signal.confidence,
                "reports": len(signal.reports),
                "successful_agents": signal.successful_agents,
                "model": signal.metadata.get("model"),
                "reasoning_effort": signal.metadata.get("reasoning_effort"),
                "confidence_explanation": signal.metadata.get("confidence_explanation", ""),
                "warnings": list(signal.warnings),
                "output": str(path),
            }
        )
    )


if __name__ == "__main__":
    main()
