from __future__ import annotations

import hashlib
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse, urlunparse

from .http import verified_ssl_context


PROFILE_QUERY_TOPICS = {
    "businessModel": "business model revenue model value chain",
    "productsAndCustomers": "products services customer types end markets",
    "segmentsAndGeographies": "reportable segments geographic revenue exposure",
    "fiscalCalendar": "fiscal year calendar quarter end dates 52 53 week",
    "revenueAndCostDrivers": "revenue drivers pricing volume mix cost drivers margins",
    "accountingDefinitions": "accounting definitions GAAP non-GAAP metric reconciliation",
    "guidanceStyle": "management guidance ranges cadence historical guidance",
    "cyclicalityAndSeasonality": "cyclicality seasonality quarterly sales pattern",
    "externalExposures": "macroeconomic political regulatory industry supply chain exposures",
}


class TavilyTransport(Protocol):
    def post(self, url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]: ...


class UrlLibJsonTransport:
    def post(self, url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=timeout, context=verified_ssl_context()) as response:
            value = json.load(response)
        if not isinstance(value, dict):
            raise RuntimeError("Tavily returned a non-object response")
        return value


def load_tavily_api_key(env_file: str | Path = ".env") -> str:
    """Return the process key, falling back to an ignored local .env file."""
    from .secrets import load_secret
    return load_secret("TAVILY_API_KEY", env_file)


@dataclass
class TavilyClient:
    api_key: str
    transport: TavilyTransport | None = None
    timeout_seconds: int = 45
    max_results: int = 5
    max_extract_urls: int = 10
    retries: int = 2

    def __post_init__(self) -> None:
        if not self.api_key.strip():
            raise RuntimeError("TAVILY_API_KEY is required")
        if self.max_results < 1 or self.max_extract_urls < 1:
            raise ValueError("Tavily request limits must be positive")
        self.transport = self.transport or UrlLibJsonTransport()

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                assert self.transport is not None
                return self.transport.post(
                    f"https://api.tavily.com/{endpoint}", payload, headers, self.timeout_seconds
                )
            except (TimeoutError, urllib.error.URLError, urllib.error.HTTPError) as error:
                last_error = error
                if attempt >= self.retries:
                    break
                time.sleep(0.25 * (2**attempt))
        raise RuntimeError(f"Tavily {endpoint} request failed after {self.retries + 1} attempts") from last_error

    def search(
        self,
        query: str,
        *,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        bounded_results = min(max_results or self.max_results, self.max_results)
        payload: dict[str, Any] = {
            "query": query,
            "search_depth": "advanced",
            "max_results": bounded_results,
            "include_raw_content": False,
        }
        if include_domains:
            payload["include_domains"] = list(dict.fromkeys(include_domains))
        if end_date:
            try:
                date.fromisoformat(end_date)
            except ValueError as error:
                raise ValueError("Tavily end_date must be YYYY-MM-DD") from error
            payload["end_date"] = end_date
        response = self._post("search", payload)
        if not isinstance(response.get("results", []), list):
            raise RuntimeError("Tavily search response has invalid results")
        return response

    def extract(self, urls: list[str]) -> dict[str, Any]:
        if not urls:
            raise ValueError("extract requires at least one URL")
        if len(urls) > self.max_extract_urls:
            raise ValueError(f"extract accepts at most {self.max_extract_urls} URLs")
        response = self._post("extract", {"urls": urls, "extract_depth": "advanced", "format": "markdown"})
        if not isinstance(response.get("results", []), list):
            raise RuntimeError("Tavily extract response has invalid results")
        return response


def _official_domains(company: dict[str, Any]) -> list[str]:
    urls = [company.get("investor_relations_url", ""), *company.get("regulator_urls", [])]
    domains: list[str] = []
    for value in urls:
        domain = urlparse(value).hostname
        if domain:
            domains.append(domain.lower().removeprefix("www."))
    return list(dict.fromkeys(domains))


def plan_profile_queries(company: dict[str, Any], information_cutoff: str) -> list[dict[str, Any]]:
    company_name = str(company["name"])
    ticker = str(company["ticker"])
    cutoff_date = information_cutoff[:10]
    domains = _official_domains(company)
    return [
        {
            "query_id": f"profile-{section}",
            "profile_section": section,
            "query": f"{company_name} {ticker} {topic} official information published by {cutoff_date}",
            "include_domains": domains,
            "end_date": cutoff_date,
        }
        for section, topic in PROFILE_QUERY_TOPICS.items()
    ]


def plan_signal_queries(
    company: dict[str, Any],
    metric: dict[str, Any],
    signals: list[dict[str, Any]],
    information_cutoff: str,
) -> list[dict[str, Any]]:
    domains = _official_domains(company)
    queries: list[dict[str, Any]] = []
    for signal in signals:
        if signal.get("status") != "approved" or signal.get("targetMetric") != metric.get("id"):
            continue
        requirements = "; ".join(str(item) for item in signal.get("evidenceRequired", []))
        query = " ".join(
            part
            for part in (
                str(company["name"]),
                str(signal.get("signal", "")),
                str(metric.get("name", "")),
                str(metric.get("targetPeriod", "")),
                str(signal.get("hypothesis", "")),
                requirements,
                str(signal.get("units", "")),
                str(signal.get("freshnessRequirement", "")),
                f"published by {information_cutoff[:10]}",
            )
            if part
        )
        queries.append(
            {
                "query_id": f"signal-{signal['id']}",
                "signal_id": signal["id"],
                "target_metric_id": metric["id"],
                "query": query,
                "include_domains": domains,
                "end_date": information_cutoff[:10],
            }
        )
    return queries


def _parse_temporal(value: str) -> date | datetime:
    if "T" not in value:
        return date.fromisoformat(value)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("publication timestamp must include a timezone")
    return parsed


def _after_cutoff(published: date | datetime, cutoff: datetime) -> bool:
    if isinstance(published, datetime):
        return published > cutoff
    return published > cutoff.date()


def _canonical_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("source URL must be HTTP(S)")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or "/", "", parsed.query, ""))


def freeze_source(
    result: dict[str, Any],
    destination: str | Path,
    *,
    query_id: str,
    request_id: str,
    information_cutoff: str,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    content = result.get("raw_content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("source extraction has no raw_content")
    published_value = result.get("published_date") or result.get("published_at")
    published = None
    if isinstance(published_value, str) and published_value.strip():
        published = _parse_temporal(published_value)
    else:
        published_value = None
    cutoff = datetime.fromisoformat(information_cutoff.replace("Z", "+00:00"))
    if cutoff.tzinfo is None:
        raise ValueError("information cutoff must include a timezone")
    canonical_url = _canonical_url(str(result.get("url", "")))
    frozen_bytes = content.replace("\r\n", "\n").encode("utf-8")
    digest = hashlib.sha256(frozen_bytes).hexdigest()
    source_id = "src-" + hashlib.sha256((canonical_url + "\n" + digest).encode("utf-8")).hexdigest()[:16]
    root = Path(destination)
    root.mkdir(parents=True, exist_ok=True)
    local_name = f"{source_id}.md"
    path = root / local_name
    if path.exists() and path.read_bytes() != frozen_bytes:
        raise RuntimeError(f"frozen source collision for {source_id}")
    path.write_bytes(frozen_bytes)
    return {
        "id": source_id,
        "url": canonical_url,
        "publisher": str(result.get("publisher") or urlparse(canonical_url).hostname or "unknown"),
        "title": str(result.get("title") or canonical_url),
        "documentType": str(result.get("document_type") or "web_page"),
        "publishedAt": published_value,
        "publicationTimeUncertain": published_value is None or len(published_value) == 10,
        "queryId": query_id,
        "tavilyRequestId": request_id,
        "localPath": local_name,
        "sha256": digest,
        "retrievedAt": retrieved_at or datetime.now(timezone.utc).isoformat(),
        "cutoffDecision": (
            "rejected_missing_publication_date"
            if published is None
            else "rejected_post_cutoff"
            if _after_cutoff(published, cutoff)
            else "accepted"
        ),
        "extractionStatus": "frozen",
        "failureReason": None,
    }


def canonical_manifest_sha256(records: list[dict[str, Any]]) -> str:
    canonical = json.dumps(sorted(records, key=lambda item: item["id"]), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_frozen_quote(record: dict[str, Any], quote: str, root: str | Path) -> bool:
    path = (Path(root) / str(record.get("localPath", ""))).resolve()
    try:
        path.relative_to(Path(root).resolve())
    except ValueError:
        return False
    if not path.is_file():
        return False
    content_bytes = path.read_bytes()
    if hashlib.sha256(content_bytes).hexdigest() != record.get("sha256"):
        return False
    normalize = lambda value: re.sub(r"\s+", " ", value).strip()
    return bool(normalize(quote)) and normalize(quote) in normalize(content_bytes.decode("utf-8"))
