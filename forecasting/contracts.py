from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


class SignalRole(str, Enum):
    CONSTRAINT = "constraint"
    ANCHOR = "anchor"
    DRIVER = "driver"
    MODIFIER = "modifier"
    SCENARIO_TRIGGER = "scenario_trigger"


class EffectKind(str, Enum):
    SET_RANGE = "set_range"
    ADDITIVE = "additive"
    QUALITATIVE = "qualitative"
    SCENARIO_ADJUSTMENT = "scenario_adjustment"
    CONSTRAINT = "constraint"


@dataclass(frozen=True)
class Company:
    company_id: str
    name: str
    ticker: str
    currency: str
    fiscal_calendar: str


@dataclass(frozen=True)
class SourceDocument:
    source_id: str
    publisher: str
    title: str
    document_type: str
    published_at: date | datetime
    url: str
    local_path: Path
    local_path_reference: str
    sha256: str


@dataclass(frozen=True)
class SourcedClaim:
    claim: str
    source_ids: tuple[str, ...]


@dataclass(frozen=True)
class MetricDefinition:
    metric_id: str
    name: str
    units: str
    target_period: str
    accounting_basis: str


@dataclass(frozen=True)
class SignalDefinition:
    signal_id: str
    signal: str
    target_metric_id: str
    role: SignalRole
    hypothesis: str
    expected_direction: str
    target_period: str
    units: str
    importance: str
    resolver: str
    evidence_required: tuple[str, ...]
    combination_method: str
    freshness_requirement: str
    correlation_group: str
    status: str


@dataclass(frozen=True)
class NumericRange:
    low: Decimal
    high: Decimal

    @property
    def midpoint(self) -> Decimal:
        return (self.low + self.high) / Decimal("2")


@dataclass(frozen=True)
class EvidenceProvenance:
    source_id: str
    publisher: str
    source_title: str
    source_document_type: str
    published_at: date | datetime
    source_url: str
    local_path: str
    source_sha256: str
    exact_quote: str
    locator: str


@dataclass(frozen=True)
class SignalObservation:
    signal_id: str
    target_metric_id: str
    role: SignalRole
    period: str
    units: str
    effect_kind: EffectKind
    value: NumericRange | Decimal | str
    provenance: EvidenceProvenance
    evidence_quality: str
    freshness: str
    calculation: str
    condition: str | None


@dataclass(frozen=True)
class ObservationDecision:
    observation: SignalObservation
    accepted: bool
    reason_code: str
    explanation: str


@dataclass(frozen=True)
class ForecastScenario:
    signal_id: str
    condition: str
    adjustment: Decimal
    range: NumericRange
    forecast: Decimal
    formula: str
    provenance: EvidenceProvenance


@dataclass(frozen=True)
class ForecastResult:
    metric_id: str
    period: str
    units: str
    anchor_range: NumericRange
    driver_adjustment: Decimal
    base_range: NumericRange
    base_forecast: Decimal
    formula: str
    accepted: tuple[ObservationDecision, ...]
    rejected: tuple[ObservationDecision, ...]
    modifiers: tuple[SignalObservation, ...]
    scenarios: tuple[ForecastScenario, ...]


@dataclass(frozen=True)
class CompanyProfile:
    schema_version: str
    company: Company
    information_cutoff: datetime
    sources: Mapping[str, SourceDocument]
    profile_sections: Mapping[str, tuple[SourcedClaim, ...]]
    metrics: Mapping[str, MetricDefinition]
    signals: Mapping[str, SignalDefinition]

    @staticmethod
    def immutable_mapping(values: dict) -> Mapping:
        return MappingProxyType(values)
