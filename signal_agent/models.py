from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Company:
    company_id: str
    name: str
    ticker: str
    exchange: str = ""
    isin: str = ""
    investor_relations_url: str = ""
    regulator_urls: tuple[str, ...] = ()
    financial_report_targets: tuple[dict[str, str], ...] = ()
    financial_fact_targets: tuple[dict[str, str], ...] = ()
    financial_observation_targets: tuple[dict[str, str], ...] = ()

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Company":
        data = dict(value)
        data["regulator_urls"] = tuple(data.get("regulator_urls", ()))
        data["financial_report_targets"] = tuple(data.get("financial_report_targets", ()))
        data["financial_fact_targets"] = tuple(data.get("financial_fact_targets", ()))
        data["financial_observation_targets"] = tuple(data.get("financial_observation_targets", ()))
        return cls(**data)


@dataclass(frozen=True)
class Finding:
    agent_id: str
    strategy: str
    company_id: str
    signal_type: str
    report_title: str
    report_type: str
    fiscal_period: str
    period_end: str
    published_at: str
    source_url: str
    source_domain: str
    source_kind: str
    official: bool
    evidence: str
    document_url: str = ""
    retrieval_notes: str = ""
    extracted_facts: tuple[dict[str, Any], ...] = ()
    observations: tuple[dict[str, Any], ...] = ()

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Finding":
        value = dict(value)
        source_aliases = {
            "investor_relations": "company_ir",
            "company_investor_relations": "company_ir",
            "listing_exchange": "stock_exchange",
            "listing_exchange_rns": "stock_exchange",
            "exchange": "stock_exchange",
        }
        value["source_kind"] = source_aliases.get(value.get("source_kind", ""), value.get("source_kind", ""))
        title = str(value.get("report_title", "")).lower()
        if value.get("report_type") == "quarterly_results" and any(
            phrase in title for phrase in ("trading statement", "trading update")
        ):
            value["report_type"] = "trading_update"
        value["extracted_facts"] = tuple(value.get("extracted_facts", ()))
        value["observations"] = tuple(value.get("observations", ()))
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: value.get(key, "") for key in allowed})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConsensusItem:
    identity: str
    report_title: str
    report_type: str
    fiscal_period: str
    period_end: str
    published_at: str
    source_url: str
    document_url: str
    supporting_agents: tuple[str, ...]
    supporting_domains: tuple[str, ...]
    confidence: float
    confidence_factors: dict[str, float]
    evidence: tuple[str, ...] = ()
    facts: tuple["ConsensusFact", ...] = ()
    observations: tuple["ConsensusObservation", ...] = ()

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["facts"] = [fact.to_dict() for fact in self.facts]
        result["observations"] = [observation.to_dict() for observation in self.observations]
        return result


@dataclass(frozen=True)
class ConsensusFact:
    metric: str
    value: float
    unit: str
    fiscal_period: str
    basis: str
    category: str
    scope: str
    fact_type: str
    page_or_section: str
    evidence: str
    supporting_agents: tuple[str, ...]
    confidence: float
    conflicting_values: tuple[float, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConsensusObservation:
    indicator: str
    direction: str
    scope: str
    horizon: str
    evidence: str
    supporting_agents: tuple[str, ...]
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReconciledSignal:
    run_id: str
    company_id: str
    signal_type: str
    status: str
    confidence: float
    reports: tuple[ConsensusItem, ...]
    agent_count: int
    successful_agents: int
    disagreements: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["reports"] = [item.to_dict() for item in self.reports]
        return result
