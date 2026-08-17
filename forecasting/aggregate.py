from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def aggregate(input_directory: Path, companies_path: Path) -> dict:
    companies = json.loads(companies_path.read_text(encoding="utf-8"))["companies"]
    result = {}
    for company in companies:
        ticker = company["ticker"].split(":")[-1]
        payload = json.loads((input_directory / f"{ticker}.json").read_text(encoding="utf-8"))
        values = {item["metric"]: item["value"] for item in payload.get("forecasts", [])}
        expected = [metric["label"] for metric in company["metrics"]]
        if set(values) != set(expected) or any(isinstance(values[name], bool) or not isinstance(values[name], (int, float)) for name in expected):
            raise ValueError(f"{ticker} must contain exactly the three configured numeric metrics")
        result[ticker] = {name: values[name] for name in expected}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate four company forecasts")
    parser.add_argument("--inputs", default="forecasts")
    parser.add_argument("--companies", default="challenge/companies.json")
    parser.add_argument("--output", default="evaluation/forecasts.json")
    args = parser.parse_args()
    result = aggregate(Path(args.inputs), Path(args.companies))
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"companies": len(result), "forecasts": 12, "output": str(destination)}))


if __name__ == "__main__":
    main()
