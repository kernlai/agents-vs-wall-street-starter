from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .contracts import (
    Company,
    CompanyProfile,
    MetricDefinition,
    SignalDefinition,
    SignalRole,
    SourceDocument,
    SourcedClaim,
)


REQUIRED_PROFILE_SECTIONS = (
    "businessModel",
    "productsAndCustomers",
    "segmentsAndGeographies",
    "fiscalCalendar",
    "revenueAndCostDrivers",
    "accountingDefinitions",
    "guidanceStyle",
    "cyclicalityAndSeasonality",
    "externalExposures",
)

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ProfileValidationError(ValueError):
    pass


def _require_text(data: dict[str, Any], key: str, context: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ProfileValidationError(f"{context}.{key} must be non-empty text")
    return value.strip()


def _parse_datetime(value: str, context: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ProfileValidationError(f"{context} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ProfileValidationError(f"{context} must include a timezone")
    return parsed


def _parse_publication(value: str, context: str) -> date | datetime:
    if "T" not in value:
        try:
            return date.fromisoformat(value)
        except ValueError as error:
            raise ProfileValidationError(f"{context} must be an ISO-8601 date or timestamp") from error
    return _parse_datetime(value, context)


def _is_after_cutoff(published_at: date | datetime, cutoff: datetime) -> bool:
    if isinstance(published_at, datetime):
        return published_at > cutoff
    return published_at > cutoff.date()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProfileValidationError(f"cannot load profile JSON: {error}") from error
    if not isinstance(value, dict):
        raise ProfileValidationError("profile root must be an object")
    return value


def _resolve_local_path(root: Path, value: str, context: str) -> Path:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ProfileValidationError(f"{context} escapes repository root") from error
    if not candidate.is_file():
        raise ProfileValidationError(f"{context} does not exist: {value}")
    return candidate


def _build_sources(
    records: Any,
    root: Path,
    cutoff: datetime,
) -> dict[str, SourceDocument]:
    if not isinstance(records, list) or not records:
        raise ProfileValidationError("sources must be a non-empty array")

    sources: dict[str, SourceDocument] = {}
    for index, record in enumerate(records):
        context = f"sources[{index}]"
        if not isinstance(record, dict):
            raise ProfileValidationError(f"{context} must be an object")
        source_id = _require_text(record, "id", context)
        if source_id in sources:
            raise ProfileValidationError(f"duplicate source id {source_id}")
        url = _require_text(record, "url", context)
        if urlparse(url).scheme not in {"http", "https"}:
            raise ProfileValidationError(f"{context}.url must be http or https")
        expected_hash = _require_text(record, "sha256", context).lower()
        if not _SHA256.fullmatch(expected_hash):
            raise ProfileValidationError(f"{context}.sha256 must be 64 lowercase hex characters")
        local_path_value = _require_text(record, "localPath", context)
        local_path = _resolve_local_path(root, local_path_value, f"{context}.localPath")
        actual_hash = hashlib.sha256(local_path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            raise ProfileValidationError(f"source hash mismatch for {source_id}")
        published_at = _parse_publication(_require_text(record, "publishedAt", context), f"{context}.publishedAt")
        if _is_after_cutoff(published_at, cutoff):
            raise ProfileValidationError(f"source {source_id} is after information cutoff")
        sources[source_id] = SourceDocument(
            source_id=source_id,
            publisher=_require_text(record, "publisher", context),
            title=_require_text(record, "title", context),
            document_type=_require_text(record, "documentType", context),
            published_at=published_at,
            url=url,
            local_path=local_path,
            local_path_reference=local_path_value,
            sha256=expected_hash,
        )
    return sources


def _build_metrics(records: Any) -> dict[str, MetricDefinition]:
    if not isinstance(records, list) or not records:
        raise ProfileValidationError("metrics must be a non-empty array")
    metrics: dict[str, MetricDefinition] = {}
    for index, record in enumerate(records):
        context = f"metrics[{index}]"
        if not isinstance(record, dict):
            raise ProfileValidationError(f"{context} must be an object")
        metric_id = _require_text(record, "id", context)
        if metric_id in metrics:
            raise ProfileValidationError(f"duplicate metric id {metric_id}")
        metrics[metric_id] = MetricDefinition(
            metric_id=metric_id,
            name=_require_text(record, "name", context),
            units=_require_text(record, "units", context),
            target_period=_require_text(record, "targetPeriod", context),
            accounting_basis=_require_text(record, "accountingBasis", context),
        )
    return metrics


def _build_profile_sections(
    record: Any,
    sources: dict[str, SourceDocument],
) -> dict[str, tuple[SourcedClaim, ...]]:
    if not isinstance(record, dict):
        raise ProfileValidationError("profile must be an object")
    sections: dict[str, tuple[SourcedClaim, ...]] = {}
    for section_name in REQUIRED_PROFILE_SECTIONS:
        claims_data = record.get(section_name)
        if not isinstance(claims_data, list) or not claims_data:
            raise ProfileValidationError(f"profile.{section_name} must be a non-empty array")
        claims: list[SourcedClaim] = []
        for index, claim_data in enumerate(claims_data):
            context = f"profile.{section_name}[{index}]"
            if not isinstance(claim_data, dict):
                raise ProfileValidationError(f"{context} must be an object")
            source_ids = claim_data.get("sourceIds")
            if not isinstance(source_ids, list) or not source_ids or not all(isinstance(item, str) for item in source_ids):
                raise ProfileValidationError(f"{context}.sourceIds must be a non-empty text array")
            for source_id in source_ids:
                if source_id not in sources:
                    raise ProfileValidationError(f"{context} references unknown source {source_id}")
            claims.append(
                SourcedClaim(
                    claim=_require_text(claim_data, "claim", context),
                    source_ids=tuple(source_ids),
                )
            )
        sections[section_name] = tuple(claims)
    return sections


def _build_signals(records: Any, metrics: dict[str, MetricDefinition]) -> dict[str, SignalDefinition]:
    if not isinstance(records, list) or not records:
        raise ProfileValidationError("signalMap must be a non-empty array")
    signals: dict[str, SignalDefinition] = {}
    for index, record in enumerate(records):
        context = f"signalMap[{index}]"
        if not isinstance(record, dict):
            raise ProfileValidationError(f"{context} must be an object")
        signal_id = _require_text(record, "id", context)
        if signal_id in signals:
            raise ProfileValidationError(f"duplicate signal id {signal_id}")
        target_metric_id = _require_text(record, "targetMetric", context)
        metric = metrics.get(target_metric_id)
        if metric is None:
            raise ProfileValidationError(f"{context} references unknown metric {target_metric_id}")
        target_period = _require_text(record, "targetPeriod", context)
        if target_period != metric.target_period:
            raise ProfileValidationError(f"{context}.targetPeriod does not match target metric")
        try:
            role = SignalRole(_require_text(record, "role", context))
        except ValueError as error:
            raise ProfileValidationError(f"{context}.role is not supported") from error
        evidence_required = record.get("evidenceRequired")
        if not isinstance(evidence_required, list) or not evidence_required or not all(
            isinstance(item, str) and item.strip() for item in evidence_required
        ):
            raise ProfileValidationError(f"{context}.evidenceRequired must be a non-empty text array")
        signals[signal_id] = SignalDefinition(
            signal_id=signal_id,
            signal=_require_text(record, "signal", context),
            target_metric_id=target_metric_id,
            role=role,
            hypothesis=_require_text(record, "hypothesis", context),
            expected_direction=_require_text(record, "expectedDirection", context),
            target_period=target_period,
            units=_require_text(record, "units", context),
            importance=_require_text(record, "importance", context),
            resolver=_require_text(record, "resolver", context),
            evidence_required=tuple(item.strip() for item in evidence_required),
            combination_method=_require_text(record, "combinationMethod", context),
            freshness_requirement=_require_text(record, "freshnessRequirement", context),
            correlation_group=_require_text(record, "correlationGroup", context),
            status=_require_text(record, "status", context),
        )
    return signals


def load_company_profile(
    path: str | Path,
    *,
    repository_root: str | Path | None = None,
) -> CompanyProfile:
    profile_path = Path(path).resolve()
    root = Path(repository_root).resolve() if repository_root is not None else profile_path.parent
    data = _load_json(profile_path)
    if _require_text(data, "schemaVersion", "profile") != "1.0":
        raise ProfileValidationError("unsupported schemaVersion")

    company_data = data.get("company")
    if not isinstance(company_data, dict):
        raise ProfileValidationError("company must be an object")
    company = Company(
        company_id=_require_text(company_data, "id", "company"),
        name=_require_text(company_data, "name", "company"),
        ticker=_require_text(company_data, "ticker", "company"),
        currency=_require_text(company_data, "currency", "company"),
        fiscal_calendar=_require_text(company_data, "fiscalCalendar", "company"),
    )
    cutoff = _parse_datetime(_require_text(data, "informationCutoff", "profile"), "informationCutoff")
    sources = _build_sources(data.get("sources"), root, cutoff)
    metrics = _build_metrics(data.get("metrics"))
    sections = _build_profile_sections(data.get("profile"), sources)
    signals = _build_signals(data.get("signalMap"), metrics)

    return CompanyProfile(
        schema_version="1.0",
        company=company,
        information_cutoff=cutoff,
        sources=CompanyProfile.immutable_mapping(sources),
        profile_sections=CompanyProfile.immutable_mapping(sections),
        metrics=CompanyProfile.immutable_mapping(metrics),
        signals=CompanyProfile.immutable_mapping(signals),
    )
