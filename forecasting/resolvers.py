from __future__ import annotations

import hashlib
from decimal import Decimal, InvalidOperation
from typing import Any

from .contracts import (
    CompanyProfile,
    EffectKind,
    EvidenceProvenance,
    NumericRange,
    SignalObservation,
    SignalRole,
    SourceDocument,
)


class ObservationValidationError(ValueError):
    pass


def _decimal(value: Any, field: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise ObservationValidationError(f"{field} must be an exact decimal string, integer or Decimal")
    try:
        parsed = value if isinstance(value, Decimal) else Decimal(value)
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ObservationValidationError(f"{field} is not a valid decimal") from error
    if not parsed.is_finite():
        raise ObservationValidationError(f"{field} must be finite")
    return parsed


def _verified_provenance(
    source: SourceDocument,
    *,
    exact_quote: str,
    locator: str,
) -> EvidenceProvenance:
    actual_hash = hashlib.sha256(source.local_path.read_bytes()).hexdigest()
    if actual_hash != source.sha256:
        raise ObservationValidationError(f"source hash mismatch for {source.source_id}")
    if not exact_quote.strip():
        raise ObservationValidationError("exact quotation is required")
    source_text = source.local_path.read_text(encoding="utf-8")
    if exact_quote not in source_text:
        raise ObservationValidationError("exact quotation not found in frozen source")
    if not locator.strip():
        raise ObservationValidationError("source locator is required")
    return EvidenceProvenance(
        source_id=source.source_id,
        publisher=source.publisher,
        source_title=source.title,
        source_document_type=source.document_type,
        published_at=source.published_at,
        source_url=source.url,
        local_path=source.local_path_reference,
        source_sha256=source.sha256,
        exact_quote=exact_quote,
        locator=locator,
    )


def resolve_management_guidance(
    profile: CompanyProfile,
    *,
    signal_id: str,
    source_id: str,
    exact_quote: str,
    locator: str,
    low: str | int | Decimal,
    high: str | int | Decimal,
    units: str,
    period: str,
    evidence_quality: str = "high",
    freshness: str = "current",
) -> SignalObservation:
    signal = profile.signals.get(signal_id)
    if signal is None:
        raise ObservationValidationError(f"unknown signal {signal_id}")
    if signal.role is not SignalRole.ANCHOR:
        raise ObservationValidationError(f"signal {signal_id} is not an anchor")
    if signal.resolver not in {"extract_management_guidance", "establish_forecast_baseline"}:
        raise ObservationValidationError(f"signal {signal_id} does not use management-guidance resolver")
    if signal.combination_method != "forecast_starting_range":
        raise ObservationValidationError(f"signal {signal_id} does not define a starting range")
    if period != signal.target_period:
        raise ObservationValidationError("observation period does not match signal target period")
    if units != signal.units:
        raise ObservationValidationError("observation units do not match signal units")
    source = profile.sources.get(source_id)
    if source is None:
        raise ObservationValidationError(f"unknown source {source_id}")

    low_value = _decimal(low, "low")
    high_value = _decimal(high, "high")
    if low_value > high_value:
        raise ObservationValidationError("guidance low must not exceed high")
    provenance = _verified_provenance(source, exact_quote=exact_quote, locator=locator)

    return SignalObservation(
        signal_id=signal.signal_id,
        target_metric_id=signal.target_metric_id,
        role=signal.role,
        period=period,
        units=units,
        effect_kind=EffectKind.SET_RANGE,
        value=NumericRange(low=low_value, high=high_value),
        provenance=provenance,
        evidence_quality=evidence_quality,
        freshness=freshness,
        calculation=f"range({low_value}, {high_value})",
        condition=None,
    )


def resolve_explicit_driver(
    profile: CompanyProfile,
    *,
    signal_id: str,
    source_id: str,
    exact_quote: str,
    locator: str,
    adjustment: str | int | Decimal,
    units: str,
    period: str,
    calculation: str,
    evidence_quality: str = "high",
    freshness: str = "current",
) -> SignalObservation:
    signal = profile.signals.get(signal_id)
    if signal is None:
        raise ObservationValidationError(f"unknown signal {signal_id}")
    if signal.role is not SignalRole.DRIVER:
        raise ObservationValidationError(f"signal {signal_id} is not a quantitative driver")
    if signal.resolver not in {"extract_explicit_driver", "resolve_explicit_driver"}:
        raise ObservationValidationError(f"signal {signal_id} does not use explicit-driver resolver")
    if signal.combination_method != "additive_adjustment":
        raise ObservationValidationError(f"signal {signal_id} does not define an additive adjustment")
    if period != signal.target_period:
        raise ObservationValidationError("observation period does not match signal target period")
    if units != signal.units:
        raise ObservationValidationError("observation units do not match signal units")
    if not calculation.strip():
        raise ObservationValidationError("driver calculation is required")
    source = profile.sources.get(source_id)
    if source is None:
        raise ObservationValidationError(f"unknown source {source_id}")
    value = _decimal(adjustment, "adjustment")
    provenance = _verified_provenance(source, exact_quote=exact_quote, locator=locator)
    return SignalObservation(
        signal_id=signal.signal_id,
        target_metric_id=signal.target_metric_id,
        role=signal.role,
        period=period,
        units=units,
        effect_kind=EffectKind.ADDITIVE,
        value=value,
        provenance=provenance,
        evidence_quality=evidence_quality,
        freshness=freshness,
        calculation=calculation.strip(),
        condition=None,
    )


def resolve_qualitative_modifier(
    profile: CompanyProfile,
    *,
    signal_id: str,
    source_id: str,
    exact_quote: str,
    locator: str,
    assessment: str,
    period: str,
    evidence_quality: str = "medium",
    freshness: str = "current",
) -> SignalObservation:
    signal = profile.signals.get(signal_id)
    if signal is None:
        raise ObservationValidationError(f"unknown signal {signal_id}")
    if signal.role is not SignalRole.MODIFIER:
        raise ObservationValidationError(f"signal {signal_id} is not a qualitative modifier")
    if signal.resolver not in {"extract_qualitative_modifier", "resolve_qualitative_modifier"}:
        raise ObservationValidationError(f"signal {signal_id} does not use qualitative-modifier resolver")
    if signal.combination_method not in {"qualitative_only", "range_selection_context"}:
        raise ObservationValidationError(f"signal {signal_id} does not define non-numeric range context")
    if period != signal.target_period:
        raise ObservationValidationError("observation period does not match signal target period")
    if not assessment.strip():
        raise ObservationValidationError("qualitative assessment is required")
    source = profile.sources.get(source_id)
    if source is None:
        raise ObservationValidationError(f"unknown source {source_id}")
    provenance = _verified_provenance(source, exact_quote=exact_quote, locator=locator)
    return SignalObservation(
        signal_id=signal.signal_id,
        target_metric_id=signal.target_metric_id,
        role=signal.role,
        period=period,
        units=signal.units,
        effect_kind=EffectKind.QUALITATIVE,
        value=assessment.strip(),
        provenance=provenance,
        evidence_quality=evidence_quality,
        freshness=freshness,
        calculation="not quantified; context only",
        condition=None,
    )


def resolve_scenario_trigger(
    profile: CompanyProfile,
    *,
    signal_id: str,
    source_id: str,
    exact_quote: str,
    locator: str,
    condition: str,
    adjustment: str | int | Decimal,
    units: str,
    period: str,
    calculation: str,
    evidence_quality: str = "medium",
    freshness: str = "current",
) -> SignalObservation:
    signal = profile.signals.get(signal_id)
    if signal is None:
        raise ObservationValidationError(f"unknown signal {signal_id}")
    if signal.role is not SignalRole.SCENARIO_TRIGGER:
        raise ObservationValidationError(f"signal {signal_id} is not a scenario trigger")
    if signal.resolver not in {"extract_scenario_trigger", "resolve_scenario_trigger"}:
        raise ObservationValidationError(f"signal {signal_id} does not use scenario-trigger resolver")
    if signal.combination_method not in {"conditional_adjustment", "conditional_additive_scenario"}:
        raise ObservationValidationError(f"signal {signal_id} does not define a conditional scenario")
    if period != signal.target_period:
        raise ObservationValidationError("observation period does not match signal target period")
    if units != signal.units:
        raise ObservationValidationError("observation units do not match signal units")
    if not condition.strip():
        raise ObservationValidationError("scenario condition is required")
    if not calculation.strip():
        raise ObservationValidationError("scenario calculation is required")
    source = profile.sources.get(source_id)
    if source is None:
        raise ObservationValidationError(f"unknown source {source_id}")
    value = _decimal(adjustment, "adjustment")
    provenance = _verified_provenance(source, exact_quote=exact_quote, locator=locator)
    return SignalObservation(
        signal_id=signal.signal_id,
        target_metric_id=signal.target_metric_id,
        role=signal.role,
        period=period,
        units=units,
        effect_kind=EffectKind.SCENARIO_ADJUSTMENT,
        value=value,
        provenance=provenance,
        evidence_quality=evidence_quality,
        freshness=freshness,
        calculation=calculation.strip(),
        condition=condition.strip(),
    )
