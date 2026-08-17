from __future__ import annotations

from collections import Counter
from decimal import Decimal
from typing import Iterable

from .contracts import (
    CompanyProfile,
    EffectKind,
    ForecastResult,
    ForecastScenario,
    NumericRange,
    ObservationDecision,
    SignalObservation,
    SignalRole,
)


class ForecastValidationError(ValueError):
    pass


def _rejection(
    observation: SignalObservation,
    reason_code: str,
    explanation: str,
) -> ObservationDecision:
    return ObservationDecision(
        observation=observation,
        accepted=False,
        reason_code=reason_code,
        explanation=explanation,
    )


def _validate_observation(
    profile: CompanyProfile,
    metric_id: str,
    observation: SignalObservation,
) -> ObservationDecision | None:
    signal = profile.signals.get(observation.signal_id)
    if signal is None:
        return _rejection(observation, "UNKNOWN_SIGNAL", "Signal is not present in the approved signal map.")
    metric = profile.metrics[metric_id]
    if signal.target_metric_id != metric_id or observation.target_metric_id != metric_id:
        return _rejection(observation, "TARGET_METRIC_MISMATCH", "Signal does not belong to this target metric.")
    if observation.role is not signal.role:
        return _rejection(observation, "SIGNAL_ROLE_MISMATCH", "Observation role differs from the signal map.")
    if observation.period != metric.target_period or observation.period != signal.target_period:
        return _rejection(observation, "PERIOD_MISMATCH", "Observation is not for the target period.")
    if observation.units != signal.units:
        return _rejection(observation, "UNIT_MISMATCH", "Observation units differ from the signal map.")
    source = profile.sources.get(observation.provenance.source_id)
    if source is None:
        return _rejection(observation, "UNKNOWN_SOURCE", "Observation source is not declared in the profile.")
    if (
        observation.provenance.source_sha256 != source.sha256
        or observation.provenance.source_url != source.url
    ):
        return _rejection(observation, "PROVENANCE_MISMATCH", "Observation provenance differs from the source record.")
    expected_effect = {
        SignalRole.ANCHOR: EffectKind.SET_RANGE,
        SignalRole.DRIVER: EffectKind.ADDITIVE,
        SignalRole.MODIFIER: EffectKind.QUALITATIVE,
        SignalRole.SCENARIO_TRIGGER: EffectKind.SCENARIO_ADJUSTMENT,
    }.get(signal.role)
    if expected_effect is not None and observation.effect_kind is not expected_effect:
        return _rejection(observation, "EFFECT_KIND_MISMATCH", "Observation effect is not allowed for this role.")
    return None


def _format_decimal(value: Decimal) -> str:
    return format(value, "f")


def compile_forecast(
    profile: CompanyProfile,
    metric_id: str,
    observations: Iterable[SignalObservation],
) -> ForecastResult:
    metric = profile.metrics.get(metric_id)
    if metric is None:
        raise ForecastValidationError(f"unknown metric {metric_id}")

    candidates = list(observations)
    accepted_candidates: list[SignalObservation] = []
    rejected: list[ObservationDecision] = []
    for observation in candidates:
        failure = _validate_observation(profile, metric_id, observation)
        if failure is None:
            accepted_candidates.append(observation)
        else:
            rejected.append(failure)

    drivers = [item for item in accepted_candidates if item.role is SignalRole.DRIVER]
    group_counts = Counter(profile.signals[item.signal_id].correlation_group for item in drivers)
    conflicting_groups = {group for group, count in group_counts.items() if count > 1}
    if conflicting_groups:
        non_conflicting: list[SignalObservation] = []
        for observation in accepted_candidates:
            signal = profile.signals[observation.signal_id]
            if observation.role is SignalRole.DRIVER and signal.correlation_group in conflicting_groups:
                rejected.append(
                    _rejection(
                        observation,
                        "CORRELATED_SIGNAL_CONFLICT",
                        f"Multiple quantitative drivers use correlation group {signal.correlation_group}.",
                    )
                )
            else:
                non_conflicting.append(observation)
        accepted_candidates = non_conflicting

    anchors = [item for item in accepted_candidates if item.role is SignalRole.ANCHOR]
    if len(anchors) != 1:
        raise ForecastValidationError(
            f"metric {metric_id} requires exactly one accepted anchor; found {len(anchors)}"
        )
    anchor = anchors[0]
    if not isinstance(anchor.value, NumericRange):
        raise ForecastValidationError("accepted anchor must contain a numeric range")

    driver_adjustment = Decimal("0")
    for observation in accepted_candidates:
        if observation.role is SignalRole.DRIVER:
            if not isinstance(observation.value, Decimal):
                raise ForecastValidationError("accepted driver must contain a Decimal adjustment")
            driver_adjustment += observation.value

    base_range = NumericRange(
        low=anchor.value.low + driver_adjustment,
        high=anchor.value.high + driver_adjustment,
    )
    base_forecast = anchor.value.midpoint + driver_adjustment
    operator = "+" if driver_adjustment >= 0 else "-"
    amount = abs(driver_adjustment)
    formula = (
        f"midpoint({_format_decimal(anchor.value.low)}, {_format_decimal(anchor.value.high)}) "
        f"{operator} {_format_decimal(amount)} = {_format_decimal(base_forecast)} {metric.units}"
    )
    accepted = tuple(
        ObservationDecision(
            observation=item,
            accepted=True,
            reason_code="ACCEPTED",
            explanation="Observation passed the declared signal and provenance checks.",
        )
        for item in accepted_candidates
    )
    modifiers = tuple(item for item in accepted_candidates if item.role is SignalRole.MODIFIER)
    scenarios: list[ForecastScenario] = []
    for observation in accepted_candidates:
        if observation.role is not SignalRole.SCENARIO_TRIGGER:
            continue
        if not isinstance(observation.value, Decimal) or not observation.condition:
            raise ForecastValidationError("accepted scenario must contain a Decimal adjustment and condition")
        scenario_forecast = base_forecast + observation.value
        scenario_range = NumericRange(
            low=base_range.low + observation.value,
            high=base_range.high + observation.value,
        )
        scenario_operator = "+" if observation.value >= 0 else "-"
        scenario_amount = abs(observation.value)
        scenarios.append(
            ForecastScenario(
                signal_id=observation.signal_id,
                condition=observation.condition,
                adjustment=observation.value,
                range=scenario_range,
                forecast=scenario_forecast,
                formula=(
                    f"{_format_decimal(base_forecast)} {scenario_operator} "
                    f"{_format_decimal(scenario_amount)} = {_format_decimal(scenario_forecast)} {metric.units}"
                ),
                provenance=observation.provenance,
            )
        )
    return ForecastResult(
        metric_id=metric.metric_id,
        period=metric.target_period,
        units=metric.units,
        anchor_range=anchor.value,
        driver_adjustment=driver_adjustment,
        base_range=base_range,
        base_forecast=base_forecast,
        formula=formula,
        accepted=accepted,
        rejected=tuple(rejected),
        modifiers=modifiers,
        scenarios=tuple(scenarios),
    )