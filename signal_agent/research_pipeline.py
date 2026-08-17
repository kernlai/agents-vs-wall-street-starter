from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from forecasting.profile import REQUIRED_PROFILE_SECTIONS

from .company_research import DEFAULT_CUTOFF, collect_candidate_bundle, _load_companies
from .lookahead import OpenAIReviewProvider
from .proposal import OpenAIProposalProvider
from .research_validation import (
    build_forecast_input_v2_1, validate_profile_candidate, validate_signal_map,
)
from .tavily import (
    TavilyClient, canonical_manifest_sha256, load_tavily_api_key,
    plan_profile_queries, plan_signal_queries,
)


ROOT = Path(__file__).resolve().parents[1]
OFFLINE_SLUGS = {"HAS": "hays", "HD": "home-depot", "ADI": "analog-devices", "DE": "deere"}
CURRENCIES = {"HAS": "GBP", "HD": "USD", "ADI": "USD", "DE": "USD"}


def _slug(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")


def load_challenge_metrics(path: Path) -> dict[str, list[dict[str, str]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, list[dict[str, str]]] = {}
    for company in payload["companies"]:
        ticker = company["ticker"].split(":")[-1]
        result[ticker] = [
            {"id": f"{ticker}_{_slug(metric['label'])}_{company['period']}", "name": metric["label"],
             "units": metric["units"], "targetPeriod": company["period"],
             "accountingBasis": "adjusted" if "Adjusted" in metric["label"] or "Pre-exceptional" in metric["label"] else "reported"}
            for metric in company["metrics"]
        ]
    return result


def build_signal_map(metrics: list[dict[str, str]]) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []
    for metric in metrics:
        common = {
            "targetMetric": metric["id"], "targetPeriod": metric["targetPeriod"],
            "accountingBasis": metric["accountingBasis"], "freshnessRequirement": "latest evidence before cutoff",
            "status": "approved",
        }
        signals.extend([
            {**common, "id": f"{metric['id']}_GUIDANCE", "signal": f"Management guidance for {metric['name']}",
             "role": "anchor", "hypothesis": "Explicit guidance or a declared latest-actual persistence baseline defines the starting range",
             "expectedDirection": "range", "importance": "primary", "units": metric["units"],
             "resolver": "establish_forecast_baseline", "evidenceRequired": ["official quantified guidance or latest same-metric actual"],
             "combinationMethod": "forecast_starting_range", "correlationGroup": "management_guidance"},
            {**common, "id": f"{metric['id']}_DEMAND", "signal": f"Demand and trading context for {metric['name']}",
             "role": "modifier", "hypothesis": "Current demand explains placement within the guidance range",
             "expectedDirection": "qualitative", "importance": "secondary", "units": "text",
             "resolver": "extract_qualitative_modifier", "evidenceRequired": ["management demand commentary"],
             "combinationMethod": "qualitative_only", "correlationGroup": "demand"},
            {**common, "id": f"{metric['id']}_RISKS", "signal": f"Execution and external risks for {metric['name']}",
             "role": "modifier", "hypothesis": "Disclosed risks contextualize confidence in guidance",
             "expectedDirection": "qualitative", "importance": "secondary", "units": "text",
             "resolver": "extract_qualitative_modifier", "evidenceRequired": ["official risk or outlook commentary"],
             "combinationMethod": "qualitative_only", "correlationGroup": "risk"},
        ])
    return signals


def offline_sources(company_id: str, cutoff: str, limit: int = 18) -> list[dict[str, Any]]:
    cutoff_date = cutoff[:10]
    base = ROOT / "challenge" / "offline-data" / OFFLINE_SLUGS[company_id]
    candidates: list[tuple[str, Path]] = []
    for path in base.rglob("*.md"):
        match = re.match(r"(\d{4}-\d{2}-\d{2})__", path.name)
        relevant_name = re.search(r"(?:q[1-4]|h[12]|fy|10[qk]|8k|call-pres|slide)", path.name, re.IGNORECASE)
        if match and match.group(1) <= cutoff_date and relevant_name:
            candidates.append((match.group(1), path))
    selected: list[tuple[str, Path]] = []
    categories = sorted({path.parent.name for _, path in candidates})
    per_category = max(1, limit // max(1, len(categories)))
    for category in categories:
        selected.extend(sorted((item for item in candidates if item[1].parent.name == category), reverse=True)[:per_category])
    selected_paths = {path for _, path in selected}
    selected.extend(item for item in sorted(candidates, reverse=True) if item[1] not in selected_paths)
    records = []
    for published, path in selected[:limit]:
        relative = path.relative_to(ROOT).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        records.append({
            "id": "offline-" + digest[:16], "url": f"https://offline.local/{relative}",
            "publisher": company_id, "title": path.stem, "documentType": path.parent.name.rstrip("s"),
            "publishedAt": published, "publicationTimeUncertain": True, "queryId": "offline-corpus",
            "tavilyRequestId": "offline", "localPath": relative, "sha256": digest,
            "retrievedAt": datetime.now(timezone.utc).isoformat(), "cutoffDecision": "accepted",
            "extractionStatus": "frozen", "failureReason": None,
        })
    return records


def _evidence_snippets(sources: list[dict[str, Any]], metrics: list[dict[str, str]], per_source: int = 20) -> list[dict[str, str]]:
    snippets = []
    terms = {word.lower() for metric in metrics for word in re.findall(r"[A-Za-z]{3,}", metric["name"])}
    terms.update({"guidance", "expect", "outlook", "forecast", "range", "business", "segment", "customer"})
    for source in sources:
        if source.get("cutoffDecision") != "accepted":
            continue
        text = (ROOT / source["localPath"]).read_text(encoding="utf-8", errors="replace")
        chunks: list[str] = []
        for line in (line.strip() for line in text.splitlines() if len(line.strip()) >= 20):
            if len(line) <= 700:
                chunks.append(line)
                continue
            sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", line) if len(part.strip()) >= 20]
            chunks.extend(part if len(part) <= 700 else part[:700] for part in sentences)
        ranked = sorted(enumerate(chunks), key=lambda item: (
            -sum(term in item[1].lower() for term in terms), item[0]
        ))[:per_source]
        for line_number, exact_text in sorted(ranked):
            quote_id = f"{source['id']}-q{line_number + 1}"
            snippets.append({"quoteId": quote_id, "sourceId": source["id"], "title": source["title"],
                             "publishedAt": source["publishedAt"], "exactText": exact_text})
    return snippets


def _decimal_text(value: Any) -> str:
    text = str(value).strip().replace(",", "")
    text = re.sub(r"^[£$€]", "", text)
    text = re.sub(r"(?:%|p|m|bn|million)$", "", text, flags=re.IGNORECASE).strip()
    if not re.fullmatch(r"[-+]?\d+(?:\.\d+)?", text):
        raise RuntimeError(f"model returned a non-decimal anchor value: {value}")
    return text


def _company_contract(config: dict[str, Any], period: str) -> dict[str, str]:
    return {"id": config["company_id"], "name": config["name"], "ticker": config["ticker"],
            "currency": CURRENCIES[config["company_id"]], "fiscalCalendar": period}


def run_company(*, config: dict[str, Any], metrics: list[dict[str, str]], client: TavilyClient,
                run_root: Path, output: Path, cutoff: str, model: str, effort: str,
                search_workers: int, deadline: float) -> dict[str, Any]:
    if time.monotonic() >= deadline:
        raise TimeoutError("45-minute research budget exhausted before company started")
    company_id = config["company_id"]
    signals = build_signal_map(metrics)
    queries = plan_profile_queries(config, cutoff)
    for metric in metrics:
        queries.extend(plan_signal_queries(config, metric, signals, cutoff))
    company_root = run_root / company_id
    bundle = collect_candidate_bundle(
        company_id=company_id, kind="signals", queries=queries, client=client,
        output_directory=company_root, information_cutoff=cutoff, search_workers=search_workers,
    )
    for source in bundle["sources"]:
        source["localPath"] = (company_root.relative_to(ROOT) / source["localPath"]).as_posix()
    sources_by_id = {source["id"]: source for source in [*bundle["sources"], *offline_sources(company_id, cutoff)]}
    sources = sorted(sources_by_id.values(), key=lambda item: item["id"])
    accepted = [source for source in sources if source["cutoffDecision"] == "accepted"]
    if not accepted:
        raise RuntimeError("research found no admissible sources")
    company = _company_contract(config, metrics[0]["targetPeriod"])
    snippets = _evidence_snippets(accepted, metrics)
    quote_by_id = {item["quoteId"]: item for item in snippets}
    proposal_input = {"company": company, "informationCutoff": cutoff, "metrics": metrics,
                      "approvedSignals": signals, "frozenEvidence": snippets}
    proposal, metadata = OpenAIProposalProvider(model=model, reasoning_effort=effort).propose(proposal_input)
    company_root.mkdir(parents=True, exist_ok=True)
    (company_root / "model-proposal.json").write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
    for section in REQUIRED_PROFILE_SECTIONS:
        for claim in proposal["profile"][section]:
            selected = [quote_by_id.get(quote_id) for quote_id in claim.pop("quoteIds")]
            if not selected or any(item is None for item in selected):
                raise RuntimeError(f"profile claim selected an unknown quoteId in {section}")
            claim["sourceIds"] = list(dict.fromkeys(item["sourceId"] for item in selected))
            claim["exactQuotes"] = [item["exactText"] for item in selected]
    anchors_by_metric = {item["metricId"]: item for item in proposal["anchors"]}
    if set(anchors_by_metric) != {metric["id"] for metric in metrics}:
        raise RuntimeError("proposal did not return exactly one anchor for every challenge metric")
    observations = []
    for index, metric in enumerate(metrics, start=1):
        anchor = anchors_by_metric[metric["id"]]
        evidence = quote_by_id.get(anchor["quoteId"])
        if evidence is None:
            raise RuntimeError(f"anchor for {metric['id']} selected an unknown quoteId")
        observations.append({
            "observationId": f"{company_id}-anchor-{index}", "signalId": f"{metric['id']}_GUIDANCE",
            "targetMetricId": metric["id"], "period": metric["targetPeriod"], "units": metric["units"],
            "accountingBasis": metric["accountingBasis"],
            "value": {"low": _decimal_text(anchor["low"]), "high": _decimal_text(anchor["high"])},
            "sourceId": evidence["sourceId"], "exactQuote": evidence["exactText"], "locator": anchor["locator"],
            "deterministicStatus": "accepted", "evidenceQuality": "high", "freshness": "current",
            "methodology": anchor["methodology"],
            "calculation": (
                f"Persistence baseline assumption: {metric['targetPeriod']} {metric['name']} forecast "
                f"equals the cited latest same-metric actual ({_decimal_text(anchor['low'])} to {_decimal_text(anchor['high'])} {metric['units']})."
                if anchor["methodology"] == "persistence_from_latest_actual" else
                f"Annualization assumption: H2 equals the cited H1 actual. {metric['targetPeriod']} {metric['name']} "
                f"forecast = H1 actual + assumed equal H2 = 2 × H1; result {_decimal_text(anchor['low'])} to {_decimal_text(anchor['high'])} {metric['units']}."
                if anchor["methodology"] == "deterministic_reconstruction" and metric["targetPeriod"].startswith("FY")
                else anchor["calculation"]
            ),
        })
    profile_receipt = validate_profile_candidate(proposal["profile"], sources, ROOT)
    map_receipt = validate_signal_map(metrics, signals)
    manifest = canonical_manifest_sha256(sources)
    audit = {
        "schemaVersion": "research_audit.v1", "provider": "openai", "model": model,
        "modelKnowledgeCutoff": "not_used_as_evidence", "requestId": metadata["requestId"],
        "promptSha256": metadata["promptSha256"], "inputManifestSha256": manifest,
        "suppliedSourceIds": [source["id"] for source in accepted],
        "claims": [{"claimId": item["observationId"], "sourceId": item["sourceId"]} for item in observations],
        "rejectedEvidence": proposal["rejectedEvidence"], "reasoningSummary": proposal["reasoningSummary"],
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    review_input = {"company": company, "informationCutoff": cutoff, "metrics": metrics,
                    "observations": observations, "researchAudit": audit,
                    "frozenEvidence": snippets}
    review = OpenAIReviewProvider(model=model, reasoning_effort=effort).review(review_input)
    (company_root / "research-audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    (company_root / "lookahead-review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
    handoff = build_forecast_input_v2_1(
        company=company, information_cutoff=cutoff, profile=proposal["profile"], metrics=metrics,
        signals=signals, profile_receipt=profile_receipt, signal_map_receipt=map_receipt,
        observations=observations, sources=sources, source_root=ROOT,
        research_audit=audit, lookahead_review=review,
    )
    destination = output / f"{company_id}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
    return {"company": company_id, "sources": len(sources), "output": str(destination)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build audited forecast_input.v2.1 artifacts from web and offline evidence")
    parser.add_argument("--company", action="append", dest="companies")
    parser.add_argument("--companies-config", default="signal_agent/config/companies.json")
    parser.add_argument("--challenge-config", default="challenge/companies.json")
    parser.add_argument("--output", default="forecast_inputs")
    parser.add_argument("--research-output", default="research")
    parser.add_argument("--cutoff", default=DEFAULT_CUTOFF)
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--reasoning-effort", choices=("none", "low", "medium", "high", "xhigh", "max"), default="medium")
    parser.add_argument("--company-workers", type=int, default=4)
    parser.add_argument("--search-workers", type=int, default=3)
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--max-minutes", type=float, default=45)
    args = parser.parse_args()
    started = time.monotonic()
    deadline = started + args.max_minutes * 60
    configs = _load_companies(ROOT / args.companies_config, args.companies)
    metrics_by_company = load_challenge_metrics(ROOT / args.challenge_config)
    client = TavilyClient(load_tavily_api_key(), max_results=args.max_results)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_root = ROOT / args.research_output / run_id
    completed, failed = {}, {}
    with ThreadPoolExecutor(max_workers=min(args.company_workers, len(configs))) as executor:
        futures = {executor.submit(
            run_company, config=config, metrics=metrics_by_company[config["company_id"]], client=client,
            run_root=run_root, output=ROOT / args.output, cutoff=args.cutoff, model=args.model,
            effort=args.reasoning_effort, search_workers=args.search_workers, deadline=deadline,
        ): config["company_id"] for config in configs}
        for future in as_completed(futures):
            company_id = futures[future]
            try:
                completed[company_id] = future.result()
            except Exception as error:
                failed[company_id] = str(error)
    summary = {"runId": run_id, "completed": completed, "failed": failed,
               "elapsedSeconds": round(time.monotonic() - started, 2), "withinBudget": time.monotonic() <= deadline}
    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))
    if failed or not summary["withinBudget"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
