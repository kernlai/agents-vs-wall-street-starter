from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def build_forecast_input(signal: dict[str, Any], minimum_confidence: float = 0.65) -> dict[str, Any]:
    facts = []
    observations = []
    source_reports = []
    for report in signal.get("reports", []):
        source_reports.append(
            {
                "identity": report["identity"],
                "title": report["report_title"],
                "period": report["fiscal_period"],
                "published_at": report["published_at"],
                "source_url": report["source_url"],
                "confidence": report["confidence"],
            }
        )
        for fact in report.get("facts", []):
            if fact["confidence"] >= minimum_confidence:
                facts.append(
                    {
                        **fact,
                        "report_identity": report["identity"],
                        "report_published_at": report["published_at"],
                        "source_url": report["source_url"],
                    }
                )
        for observation in report.get("observations", []):
            if observation["confidence"] >= minimum_confidence:
                observations.append(
                    {
                        **observation,
                        "report_identity": report["identity"],
                        "source_url": report["source_url"],
                    }
                )

    by_metric: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for fact in facts:
        key = " | ".join((fact["metric"], fact["scope"], fact["basis"], fact["unit"]))
        by_metric[key].append(fact)
    for series in by_metric.values():
        series.sort(key=lambda item: (item["report_published_at"], item["fiscal_period"]))

    return {
        "schema_version": "forecast_input.v1",
        "company_id": signal["company_id"],
        "signal_run_id": signal["run_id"],
        "signal_type": signal["signal_type"],
        "signal_confidence": signal["confidence"],
        "confidence_explanation": signal.get("metadata", {}).get("confidence_explanation", ""),
        "model": signal.get("metadata", {}).get("model"),
        "reasoning_effort": signal.get("metadata", {}).get("reasoning_effort"),
        "minimum_fact_confidence": minimum_confidence,
        "source_reports": source_reports,
        "facts": facts,
        "metric_series": dict(sorted(by_metric.items())),
        "observations": observations,
        "unresolved_conflicts": [
            fact for fact in facts if fact.get("conflicting_values")
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a forecast-ready input from a reconciled signal")
    parser.add_argument("--company", required=True)
    parser.add_argument("--signals", default="signals")
    parser.add_argument("--output", default="forecast_inputs")
    parser.add_argument("--minimum-confidence", type=float, default=0.65)
    args = parser.parse_args()

    source = Path(args.signals) / args.company / "financial_reports" / "latest.json"
    if not source.exists():
        raise SystemExit(f"Missing reconciled signal: {source}")
    result = build_forecast_input(json.loads(source.read_text()), args.minimum_confidence)
    output = Path(args.output) / f"{args.company}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"company": args.company, "facts": len(result["facts"]), "output": str(output)}))


if __name__ == "__main__":
    main()
