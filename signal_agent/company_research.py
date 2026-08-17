from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urldefrag

from .research_validation import validate_signal_map
from .tavily import (
    TavilyClient,
    canonical_manifest_sha256,
    freeze_source,
    load_tavily_api_key,
    plan_profile_queries,
    plan_signal_queries,
)


DEFAULT_CUTOFF = "2026-08-16T17:15:00+01:00"


def _url_key(value: str) -> str:
    return urldefrag(value)[0].rstrip("/")


def collect_candidate_bundle(
    *,
    company_id: str,
    kind: str,
    queries: list[dict[str, Any]],
    client: TavilyClient,
    output_directory: str | Path,
    information_cutoff: str,
    search_workers: int = 3,
) -> dict[str, Any]:
    if kind not in {"profile", "signals"}:
        raise ValueError("candidate bundle kind must be profile or signals")
    if not queries:
        raise ValueError("candidate research requires at least one query")
    output = Path(output_directory)
    sources_directory = output / "sources"
    output.mkdir(parents=True, exist_ok=True)
    unresolved: list[dict[str, str]] = []
    leads_by_url: dict[str, dict[str, Any]] = {}

    def search_one(query: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        response = client.search(
            query["query"],
            include_domains=query.get("include_domains"),
            end_date=query.get("end_date"),
        )
        return query, response

    with ThreadPoolExecutor(max_workers=min(max(1, search_workers), len(queries))) as executor:
        futures = {executor.submit(search_one, query): query for query in queries}
        for future in as_completed(futures):
            query = futures[future]
            try:
                planned, response = future.result()
            except Exception as error:
                unresolved.append({"queryId": query["query_id"], "reason": f"search_failed: {error}"})
                continue
            request_id = str(response.get("request_id", "unknown"))
            for result in response.get("results", []):
                url = result.get("url")
                if not isinstance(url, str) or not url:
                    unresolved.append({"queryId": planned["query_id"], "reason": "search_result_missing_url"})
                    continue
                key = _url_key(url)
                lead = leads_by_url.setdefault(key, {**result, "queryIds": [], "searchRequestIds": []})
                lead["queryIds"].append(planned["query_id"])
                lead["searchRequestIds"].append(request_id)

    records: list[dict[str, Any]] = []
    urls = [lead["url"] for lead in leads_by_url.values()]
    batch_size = getattr(client, "max_extract_urls", 10)
    for start in range(0, len(urls), batch_size):
        batch = urls[start : start + batch_size]
        try:
            response = client.extract(batch)
        except Exception as error:
            unresolved.extend({"url": url, "reason": f"extract_failed: {error}"} for url in batch)
            continue
        extract_request_id = str(response.get("request_id", "unknown"))
        for failure in response.get("failed_results", []):
            if isinstance(failure, dict):
                unresolved.append({
                    "url": str(failure.get("url", "unknown")),
                    "reason": f"extract_failed: {failure.get('error', 'unknown error')}",
                })
        for extracted in response.get("results", []):
            url = extracted.get("url")
            lead = leads_by_url.get(_url_key(str(url)))
            if lead is None:
                unresolved.append({"url": str(url), "reason": "extract_result_not_in_search_leads"})
                continue
            merged = {**lead, **extracted}
            try:
                record = freeze_source(
                    merged,
                    sources_directory,
                    query_id=lead["queryIds"][0],
                    request_id=extract_request_id,
                    information_cutoff=information_cutoff,
                )
            except Exception as error:
                unresolved.append({"url": str(url), "reason": f"freeze_failed: {error}"})
                continue
            record["localPath"] = f"sources/{record['localPath']}"
            record["queryIds"] = list(dict.fromkeys(lead["queryIds"]))
            record["searchRequestIds"] = list(dict.fromkeys(lead["searchRequestIds"]))
            records.append(record)

    records.sort(key=lambda item: item["id"])
    bundle = {
        "schemaVersion": "research_candidate_bundle.v1",
        "kind": kind,
        "companyId": company_id,
        "informationCutoff": information_cutoff,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "queryPlan": queries,
        "sources": records,
        "unresolved": sorted(unresolved, key=lambda item: (item.get("queryId", ""), item.get("url", ""))),
        "provenanceManifestSha256": canonical_manifest_sha256(records),
    }
    (output / f"{kind}-candidates.json").write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    return bundle


def research_companies(
    companies: list[dict[str, Any]],
    worker: Callable[[dict[str, Any]], dict[str, Any]],
    *,
    max_workers: int = 4,
) -> dict[str, dict[str, Any]]:
    completed: dict[str, Any] = {}
    failed: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=min(max(1, max_workers), len(companies))) as executor:
        futures = {executor.submit(worker, company): company["company_id"] for company in companies}
        for future in as_completed(futures):
            company_id = futures[future]
            try:
                completed[company_id] = future.result()
            except Exception as error:
                failed[company_id] = str(error)
    return {"completed": completed, "failed": failed}


def _load_companies(path: Path, requested: list[str] | None) -> list[dict[str, Any]]:
    companies = json.loads(path.read_text(encoding="utf-8"))["companies"]
    if requested:
        wanted = set(requested)
        companies = [company for company in companies if company["company_id"] in wanted]
        missing = wanted - {company["company_id"] for company in companies}
        if missing:
            raise ValueError(f"unknown company IDs: {', '.join(sorted(missing))}")
    return companies


def main() -> None:
    parser = argparse.ArgumentParser(description="Research company profiles or approved forecast signals with Tavily")
    parser.add_argument("--stage", choices=("profile", "signals"), default="profile")
    parser.add_argument("--company", action="append", dest="companies")
    parser.add_argument("--companies-config", default="signal_agent/config/companies.json")
    parser.add_argument("--signal-map-directory", default="signal_maps")
    parser.add_argument("--output", default="research")
    parser.add_argument("--cutoff", default=DEFAULT_CUTOFF)
    parser.add_argument("--company-workers", type=int, default=4)
    parser.add_argument("--search-workers", type=int, default=3)
    parser.add_argument("--max-results", type=int, default=5)
    args = parser.parse_args()

    companies = _load_companies(Path(args.companies_config), args.companies)
    client = TavilyClient(load_tavily_api_key(), max_results=args.max_results)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_root = Path(args.output) / run_id

    def research_one(company: dict[str, Any]) -> dict[str, Any]:
        if args.stage == "profile":
            queries = plan_profile_queries(company, args.cutoff)
        else:
            map_path = Path(args.signal_map_directory) / f"{company['company_id']}.json"
            payload = json.loads(map_path.read_text(encoding="utf-8"))
            metrics = payload["metrics"]
            signals = payload["signalMap"]
            validate_signal_map(metrics, signals)
            queries = [
                query
                for metric in metrics
                for query in plan_signal_queries(company, metric, signals, args.cutoff)
            ]
        return collect_candidate_bundle(
            company_id=company["company_id"],
            kind=args.stage,
            queries=queries,
            client=client,
            output_directory=run_root / company["company_id"],
            information_cutoff=args.cutoff,
            search_workers=args.search_workers,
        )

    result = research_companies(companies, research_one, max_workers=args.company_workers)
    summary = {
        "runId": run_id,
        "stage": args.stage,
        "completed": sorted(result["completed"]),
        "failed": result["failed"],
        "output": str(run_root),
    }
    (run_root / "summary.json").parent.mkdir(parents=True, exist_ok=True)
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))
    if result["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
