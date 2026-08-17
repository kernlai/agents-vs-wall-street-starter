from __future__ import annotations

from dataclasses import dataclass

from .contracts import CompanyProfile, ForecastResult, SignalRole


@dataclass(frozen=True)
class ChallengeIssue:
    code: str
    severity: str
    signal_id: str
    message: str


@dataclass(frozen=True)
class ChallengeReport:
    passed: bool
    issues: tuple[ChallengeIssue, ...]


def challenge_forecast(profile: CompanyProfile, result: ForecastResult) -> ChallengeReport:
    if result.metric_id not in profile.metrics:
        raise ValueError(f"unknown metric {result.metric_id}")
    observed = {
        decision.observation.signal_id
        for decision in (*result.accepted, *result.rejected)
    }
    issues: list[ChallengeIssue] = []
    for signal in profile.signals.values():
        if signal.target_metric_id != result.metric_id or signal.signal_id in observed:
            continue
        if signal.importance == "primary":
            issues.append(
                ChallengeIssue(
                    code="MISSING_PRIMARY_SIGNAL",
                    severity="error",
                    signal_id=signal.signal_id,
                    message=f"Primary signal '{signal.signal}' was not resolved or explicitly rejected.",
                )
            )
        else:
            issues.append(
                ChallengeIssue(
                    code="MISSING_SIGNAL",
                    severity="warning",
                    signal_id=signal.signal_id,
                    message=f"Signal '{signal.signal}' has no current observation.",
                )
            )

    for decision in result.rejected:
        signal = profile.signals.get(decision.observation.signal_id)
        severity = "error" if signal is None or signal.importance == "primary" or signal.role is SignalRole.ANCHOR else "warning"
        issues.append(
            ChallengeIssue(
                code=decision.reason_code,
                severity=severity,
                signal_id=decision.observation.signal_id,
                message=decision.explanation,
            )
        )
    return ChallengeReport(
        passed=not any(issue.severity == "error" for issue in issues),
        issues=tuple(issues),
    )
