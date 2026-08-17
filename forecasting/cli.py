from __future__ import annotations

import argparse
import json
from pathlib import Path

from .challenge import challenge_forecast
from .engine import compile_forecast
from .handoff import load_v2_1
from .receipt import build_run_receipt


def forecast_payload(company_id: str, handoff: dict) -> dict:
    profile, observations = load_v2_1(handoff)
    if profile.company.company_id != company_id:
        raise ValueError("company ID does not match forecast input")
    forecasts, receipts, warnings = [], [], []
    for metric in profile.metrics.values():
        metric_observations = [item for item in observations if item.target_metric_id == metric.metric_id]
        result = compile_forecast(profile, metric.metric_id, metric_observations)
        challenge = challenge_forecast(profile, result)
        if not challenge.passed:
            errors = [issue.message for issue in challenge.issues if issue.severity == "error"]
            raise ValueError(f"{metric.name} challenge failed: {'; '.join(errors)}")
        forecasts.append({
            "metric": metric.name, "value": float(result.base_forecast), "unit": metric.units,
            "scenario": "base", "rationale": result.formula,
            "input_fact_ids": [item.observation.signal_id for item in result.accepted],
        })
        warnings.extend(issue.message for issue in challenge.issues if issue.severity == "warning")
        receipts.append(build_run_receipt(profile, result, challenge))
    if len(forecasts) != 3:
        raise ValueError("forecast input must compile exactly three metrics")
    return {
        "schema_version": "company_forecast.v1", "company_id": company_id,
        "signal_run_id": handoff["provenanceManifestSha256"],
        "forecasts": forecasts, "receipts": receipts, "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile three evidence-gated company forecasts")
    parser.add_argument("--company", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = forecast_payload(args.company, json.loads(Path(args.input).read_text(encoding="utf-8")))
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"company": args.company, "forecasts": 3, "output": str(destination)}))


if __name__ == "__main__":
    main()
