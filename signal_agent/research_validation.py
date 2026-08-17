from __future__ import annotations

import re
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from forecasting.profile import REQUIRED_PROFILE_SECTIONS

from .tavily import canonical_manifest_sha256, verify_frozen_quote


SUPPORTED_SIGNAL_BEHAVIOUR = {
    ("anchor", "extract_management_guidance", "forecast_starting_range"),
    ("anchor", "establish_forecast_baseline", "forecast_starting_range"),
    ("driver", "extract_explicit_driver", "additive_adjustment"),
    ("modifier", "extract_qualitative_modifier", "qualitative_only"),
    ("scenario_trigger", "extract_scenario_trigger", "conditional_adjustment"),
    ("constraint", "evaluate_constraint", "constraint_check"),
}

SUPPORTED_LOOKAHEAD_ISSUES = {
    "UNSUPPORTED_CLAIM",
    "SOURCE_NOT_SUPPLIED",
    "QUOTE_NOT_IN_SOURCE",
    "POST_CUTOFF_FACT",
    "ACTUAL_PRESENTED_AS_FORECAST",
    "UNDECLARED_ASSUMPTION",
    "SUSPICIOUS_PRECISION",
    "PERIOD_LEAKAGE",
    "MODEL_CUTOFF_UNDISCLOSED",
}

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ResearchValidationError(ValueError):
    pass


def _require_text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ResearchValidationError(f"{context} must be non-empty text")
    return value.strip()


def validate_profile_candidate(
    profile: dict[str, Any],
    sources: list[dict[str, Any]],
    source_root: str | Path,
) -> dict[str, Any]:
    source_by_id = {item.get("id"): item for item in sources}
    if len(source_by_id) != len(sources) or None in source_by_id:
        raise ResearchValidationError("source IDs must be present and unique")
    accepted_claim_ids: list[str] = []
    for section in REQUIRED_PROFILE_SECTIONS:
        claims = profile.get(section)
        if not isinstance(claims, list) or not claims:
            raise ResearchValidationError(f"profile.{section} must contain a source-backed claim")
        for index, claim in enumerate(claims):
            context = f"profile.{section}[{index}]"
            if not isinstance(claim, dict):
                raise ResearchValidationError(f"{context} must be an object")
            claim_id = _require_text(claim.get("claimId"), f"{context}.claimId")
            _require_text(claim.get("claim"), f"{context}.claim")
            source_ids = claim.get("sourceIds")
            quotes = claim.get("exactQuotes")
            if not isinstance(source_ids, list) or not source_ids:
                raise ResearchValidationError(f"{context}.sourceIds must be non-empty")
            if not isinstance(quotes, list) or not quotes:
                raise ResearchValidationError(f"{context}.exactQuotes must be non-empty")
            records: list[dict[str, Any]] = []
            for source_id in source_ids:
                record = source_by_id.get(source_id)
                if record is None:
                    raise ResearchValidationError(f"{context} references unknown source {source_id}")
                if record.get("cutoffDecision") != "accepted":
                    raise ResearchValidationError(f"{context} references inadmissible source {source_id}")
                records.append(record)
            for quote in quotes:
                if not isinstance(quote, str) or not any(
                    verify_frozen_quote(record, quote, source_root) for record in records
                ):
                    raise ResearchValidationError(f"{context} exact quote is not present in a cited frozen source")
            accepted_claim_ids.append(claim_id)
    duplicates = [claim_id for claim_id, count in Counter(accepted_claim_ids).items() if count > 1]
    if duplicates:
        raise ResearchValidationError(f"duplicate profile claim id {duplicates[0]}")
    return {
        "schemaVersion": "profile_receipt.v1",
        "status": "accepted",
        "acceptedClaimCount": len(accepted_claim_ids),
        "acceptedClaimIds": accepted_claim_ids,
        "sourceManifestSha256": canonical_manifest_sha256(sources),
    }


def validate_signal_map(metrics: list[dict[str, Any]], signals: list[dict[str, Any]]) -> dict[str, Any]:
    metric_by_id: dict[str, dict[str, Any]] = {}
    for index, metric in enumerate(metrics):
        metric_id = _require_text(metric.get("id"), f"metrics[{index}].id")
        if metric_id in metric_by_id:
            raise ResearchValidationError(f"duplicate metric id {metric_id}")
        metric_by_id[metric_id] = metric
    signal_ids: set[str] = set()
    by_metric: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, signal in enumerate(signals):
        context = f"signals[{index}]"
        signal_id = _require_text(signal.get("id"), f"{context}.id")
        if signal_id in signal_ids:
            raise ResearchValidationError(f"duplicate signal id {signal_id}")
        signal_ids.add(signal_id)
        if "weight" in signal or "numericWeight" in signal:
            raise ResearchValidationError(f"{context}: qualitative or arbitrary weights are forbidden")
        metric_id = _require_text(signal.get("targetMetric"), f"{context}.targetMetric")
        metric = metric_by_id.get(metric_id)
        if metric is None:
            raise ResearchValidationError(f"{context} references unknown metric {metric_id}")
        if signal.get("targetPeriod") != metric.get("targetPeriod"):
            raise ResearchValidationError(f"{context} target period mismatch")
        if signal.get("accountingBasis", metric.get("accountingBasis")) != metric.get("accountingBasis"):
            raise ResearchValidationError(f"{context} accounting basis mismatch")
        behaviour = (signal.get("role"), signal.get("resolver"), signal.get("combinationMethod"))
        if behaviour not in SUPPORTED_SIGNAL_BEHAVIOUR:
            raise ResearchValidationError(f"{context} has unsupported resolver/combination for role")
        if signal.get("role") in {"anchor", "driver", "scenario_trigger"} and signal.get("units") != metric.get("units"):
            raise ResearchValidationError(f"{context} units do not match target metric")
        required_text = (
            "signal", "hypothesis", "expectedDirection", "importance",
            "freshnessRequirement", "correlationGroup", "status",
        )
        for field in required_text:
            _require_text(signal.get(field), f"{context}.{field}")
        evidence = signal.get("evidenceRequired")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
            raise ResearchValidationError(f"{context}.evidenceRequired must be non-empty text")
        if signal.get("status") == "approved":
            by_metric[metric_id].append(signal)

    metric_receipts: dict[str, dict[str, Any]] = {}
    for metric_id in metric_by_id:
        approved = by_metric.get(metric_id, [])
        if not 3 <= len(approved) <= 7:
            raise ResearchValidationError(f"metric {metric_id} must have between 3 and 7 approved signals")
        anchors = [item for item in approved if item["role"] == "anchor"]
        if len(anchors) != 1:
            raise ResearchValidationError(f"metric {metric_id} must have exactly one approved anchor")
        metric_receipts[metric_id] = {
            "signalCount": len(approved),
            "anchorSignalId": anchors[0]["id"],
            "approvedSignalIds": [item["id"] for item in approved],
        }
    return {
        "schemaVersion": "signal_map_receipt.v1",
        "status": "accepted",
        "metrics": metric_receipts,
    }


def _validate_audit(audit: dict[str, Any], manifest_hash: str, source_ids: set[str]) -> None:
    if audit.get("schemaVersion") != "research_audit.v1":
        raise ResearchValidationError("research audit schema is not research_audit.v1")
    for field in ("provider", "model", "modelKnowledgeCutoff", "requestId", "reasoningSummary", "createdAt"):
        _require_text(audit.get(field), f"researchAudit.{field}")
    for field in ("promptSha256", "inputManifestSha256"):
        value = audit.get(field)
        if not isinstance(value, str) or not _SHA256.fullmatch(value):
            raise ResearchValidationError(f"researchAudit.{field} must be a SHA-256 hash")
    if audit["inputManifestSha256"] != manifest_hash:
        raise ResearchValidationError("research audit input manifest does not match frozen sources")
    supplied = audit.get("suppliedSourceIds")
    if not isinstance(supplied, list) or not set(supplied).issubset(source_ids):
        raise ResearchValidationError("research audit references an unsupplied source")
    if not isinstance(audit.get("claims"), list) or not isinstance(audit.get("rejectedEvidence"), list):
        raise ResearchValidationError("research audit claims and rejectedEvidence must be arrays")


def _validate_review(review: dict[str, Any], source_ids: set[str]) -> None:
    if review.get("schemaVersion") != "lookahead_review.v1":
        raise ResearchValidationError("look-ahead review schema is not lookahead_review.v1")
    if review.get("status") not in {"passed", "blocked_for_lookahead", "incomplete"}:
        raise ResearchValidationError("look-ahead review status is unsupported")
    issues = review.get("issues")
    if not isinstance(issues, list):
        raise ResearchValidationError("look-ahead review issues must be an array")
    for index, issue in enumerate(issues):
        if issue.get("code") not in SUPPORTED_LOOKAHEAD_ISSUES:
            raise ResearchValidationError(f"look-ahead issue {index} has unsupported code")
        if issue.get("severity") not in {"warning", "error"}:
            raise ResearchValidationError(f"look-ahead issue {index} has unsupported severity")
        if not set(issue.get("sourceIds", [])).issubset(source_ids):
            raise ResearchValidationError(f"look-ahead issue {index} references unknown source")
        _require_text(issue.get("explanation"), f"lookaheadReview.issues[{index}].explanation")
    if review.get("status") != "passed" or any(issue.get("severity") == "error" for issue in issues):
        raise ResearchValidationError("look-ahead review has not passed")


def _validate_decimal_value(value: Any, context: str) -> None:
    values = value.values() if isinstance(value, dict) else (value,)
    for item in values:
        if not isinstance(item, str):
            raise ResearchValidationError(f"{context} must preserve every number as a decimal string")
        try:
            Decimal(item)
        except InvalidOperation as error:
            raise ResearchValidationError(f"{context} contains an invalid decimal string") from error


def _is_decimal_value(value: Any) -> bool:
    try:
        _validate_decimal_value(value, "value")
        return True
    except ResearchValidationError:
        return False


def build_forecast_input_v2(
    *,
    company_id: str,
    profile_receipt: dict[str, Any],
    signal_map_receipt: dict[str, Any],
    observations: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    source_root: str | Path,
    research_audit: dict[str, Any],
    lookahead_review: dict[str, Any],
) -> dict[str, Any]:
    if profile_receipt.get("status") != "accepted":
        raise ResearchValidationError("company profile has not been accepted")
    if signal_map_receipt.get("status") != "accepted":
        raise ResearchValidationError("signal map has not been accepted")
    source_by_id = {record.get("id"): record for record in sources}
    manifest_hash = canonical_manifest_sha256(sources)
    source_ids = set(source_by_id)
    _validate_audit(research_audit, manifest_hash, source_ids)
    _validate_review(lookahead_review, source_ids)
    accepted: list[dict[str, Any]] = []
    approved_signals = {
        signal_id
        for metric in signal_map_receipt.get("metrics", {}).values()
        for signal_id in metric.get("approvedSignalIds", [])
    }
    for index, observation in enumerate(observations):
        context = f"observations[{index}]"
        if observation.get("deterministicStatus") != "accepted":
            raise ResearchValidationError(f"{context} has not passed deterministic validation")
        if observation.get("signalId") not in approved_signals:
            raise ResearchValidationError(f"{context} references an unapproved signal")
        source = source_by_id.get(observation.get("sourceId"))
        if source is None or source.get("cutoffDecision") != "accepted":
            raise ResearchValidationError(f"{context} references inadmissible evidence")
        quote = observation.get("exactQuote")
        if not isinstance(quote, str) or not verify_frozen_quote(source, quote, source_root):
            raise ResearchValidationError(f"{context} quotation does not match frozen evidence")
        value = observation.get("value")
        if not isinstance(value, str) or _is_decimal_value(value):
            _validate_decimal_value(value, f"{context}.value")
        accepted.append(observation)
    return {
        "schemaVersion": "forecast_input.v2",
        "companyId": company_id,
        "profileReceipt": profile_receipt,
        "signalMapReceipt": signal_map_receipt,
        "observations": accepted,
        "researchAudit": research_audit,
        "lookaheadReview": lookahead_review,
        "provenanceManifestSha256": manifest_hash,
    }


def build_forecast_input_v2_1(
    *, company: dict[str, Any], information_cutoff: str,
    profile: dict[str, Any], metrics: list[dict[str, Any]],
    signals: list[dict[str, Any]], profile_receipt: dict[str, Any],
    signal_map_receipt: dict[str, Any], observations: list[dict[str, Any]],
    sources: list[dict[str, Any]], source_root: str | Path,
    research_audit: dict[str, Any], lookahead_review: dict[str, Any],
) -> dict[str, Any]:
    """Build the self-contained, compiler-ready extension of forecast_input.v2."""
    company_id = _require_text(company.get("id"), "company.id")
    for field in ("name", "ticker", "currency", "fiscalCalendar"):
        _require_text(company.get(field), f"company.{field}")
    if len(metrics) != 3:
        raise ResearchValidationError("forecast_input.v2.1 requires exactly three metrics")
    validated_profile = validate_profile_candidate(profile, sources, source_root)
    validated_map = validate_signal_map(metrics, signals)
    if validated_profile != profile_receipt:
        raise ResearchValidationError("profile receipt does not match supplied profile")
    if validated_map != signal_map_receipt:
        raise ResearchValidationError("signal-map receipt does not match supplied definitions")
    role_by_signal = {item["id"]: item["role"] for item in signals if item.get("status") == "approved"}
    for index, observation in enumerate(observations):
        context = f"observations[{index}]"
        _require_text(observation.get("locator"), f"{context}.locator")
        role = role_by_signal.get(observation.get("signalId"))
        if role == "modifier":
            _require_text(observation.get("value"), f"{context}.value")
        elif role in {"anchor", "driver", "scenario_trigger"}:
            _validate_decimal_value(observation.get("value"), f"{context}.value")
        if role in {"driver", "scenario_trigger"}:
            _require_text(observation.get("calculation"), f"{context}.calculation")
        if role == "scenario_trigger":
            _require_text(observation.get("condition"), f"{context}.condition")
    base = build_forecast_input_v2(
        company_id=company_id, profile_receipt=profile_receipt,
        signal_map_receipt=signal_map_receipt, observations=observations,
        sources=sources, source_root=source_root, research_audit=research_audit,
        lookahead_review=lookahead_review,
    )
    return {
        **base,
        "schemaVersion": "forecast_input.v2.1",
        "company": company,
        "informationCutoff": information_cutoff,
        "profile": profile,
        "metrics": metrics,
        "signalMap": signals,
        "sources": sources,
        "sourceRoot": str(Path(source_root).resolve()),
    }
