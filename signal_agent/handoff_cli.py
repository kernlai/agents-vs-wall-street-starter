from __future__ import annotations

import argparse
import json
from pathlib import Path

from .research_validation import build_forecast_input_v2_1


def load(path: str) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate research artifacts and build forecast_input.v2.1")
    parser.add_argument("--proposal", required=True, help="JSON with company, cutoff, profile, metrics, signals and observations")
    parser.add_argument("--candidates", required=True, help="Tavily candidate bundle containing frozen sources")
    parser.add_argument("--audit", required=True)
    parser.add_argument("--review", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    proposal, candidates = load(args.proposal), load(args.candidates)
    from .research_validation import validate_profile_candidate, validate_signal_map
    profile_receipt = validate_profile_candidate(proposal["profile"], candidates["sources"], args.source_root)
    map_receipt = validate_signal_map(proposal["metrics"], proposal["signals"])
    result = build_forecast_input_v2_1(
        company=proposal["company"], information_cutoff=proposal["informationCutoff"],
        profile=proposal["profile"], metrics=proposal["metrics"], signals=proposal["signals"],
        profile_receipt=profile_receipt, signal_map_receipt=map_receipt,
        observations=proposal["observations"], sources=candidates["sources"],
        source_root=args.source_root, research_audit=load(args.audit),
        lookahead_review=load(args.review),
    )
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"company": result["companyId"], "schema": result["schemaVersion"], "output": str(destination)}))


if __name__ == "__main__":
    main()
