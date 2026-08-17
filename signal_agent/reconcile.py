from __future__ import annotations

import re
from collections import defaultdict
from datetime import date
from statistics import mean
from urllib.parse import urlsplit

from .models import ConsensusFact, ConsensusItem, ConsensusObservation, Finding, ReconciledSignal


SOURCE_AUTHORITY = {
    "company_ir": 1.0,
    "regulator": 0.98,
    "stock_exchange": 0.95,
    "official_archive": 0.9,
    "other_official": 0.85,
}


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def report_identity(finding: Finding) -> str:
    period = finding.period_end or finding.fiscal_period
    # Discovery agents often describe the same unaudited period-end event as a
    # quarterly result, trading statement, or trading update. Reconcile at the
    # event-family level while retaining the representative's original type.
    report_family = (
        "periodic_update"
        if finding.report_type in {"quarterly_results", "trading_update"}
        else finding.report_type
    )
    return "|".join(
        (_normalise(finding.company_id), _normalise(report_family), _normalise(period))
    )


def _domain(url: str) -> str:
    hostname = urlsplit(url).netloc.lower().removeprefix("www.")
    # Independence is organizational, not host-level. A document CDN and the
    # parent website do not count as two corroborating sources.
    source_families = (
        "londonstockexchange.com",
        "haysplc.com",
        "sec.gov",
        "homedepot.com",
        "analog.com",
        "deere.com",
    )
    return next((family for family in source_families if hostname == family or hostname.endswith(f".{family}")), hostname)


def _completeness(finding: Finding) -> float:
    required = (
        finding.report_title,
        finding.report_type,
        finding.fiscal_period,
        finding.period_end,
        finding.published_at,
        finding.source_url,
        finding.evidence,
    )
    return sum(bool(item) for item in required) / len(required)


def _normalise_unit(unit: str) -> str:
    aliases = {
        "£m": "GBPm", "gbp m": "GBPm", "gbpm": "GBPm",
        "p": "GBp", "pence": "GBp", "gbp": "GBP",
        "$m": "USDm", "usd m": "USDm", "usdm": "USDm",
        "%": "%", "percent": "%", "percentage points": "%",
    }
    key = unit.strip().lower()
    return aliases.get(key, unit.strip())


def _normalise_metric(metric: str) -> str:
    key = _normalise(metric)
    if "net fee" in key and "growth" in key:
        if "temp" in key or "contract" in key:
            return "Temporary and Contracting net fees growth"
        if "perm" in key:
            return "Permanent net fees growth"
        return "Net fees growth"
    if "net fee" in key and "growth" not in key:
        return "Net fees"
    if "effective tax rate" in key:
        return "Pre-exceptional effective tax rate" if "exception" in key else "Effective tax rate"
    if "basic eps" in key or "basic earnings per share" in key:
        return "Pre-exceptional basic EPS" if "exception" in key else "Basic EPS"
    if "operating profit" in key and ("expect" in key or "consensus" in key):
        return "Expected pre-exceptional operating profit"
    if "operating profit" in key:
        return "Pre-exceptional operating profit" if "exception" in key else "Operating profit"
    if "finance charge" in key:
        return "Net finance charge"
    return metric.strip()


def _normalise_basis(basis: str) -> str:
    key = _normalise(basis)
    if "like for like" in key or "constant currency" in key:
        return "like_for_like"
    if "actual" in key and "year on year" in key:
        return "actual_yoy"
    if "before exceptional" in key or "pre exceptional" in key:
        return "pre_exceptional"
    if "consensus" in key:
        return "analyst_consensus"
    if "expectation" in key or "guidance" in key:
        return "management_guidance"
    if "period end" in key:
        return "period_end"
    if "non gaap" in key or "adjusted" in key:
        return "adjusted"
    if any(token in key for token in ("gaap", "reported", "unaudited", "audited", "segment result", "consolidated")):
        return "reported"
    if key in {"unaudited", "audited", "reported", ""}:
        return "reported"
    return key.replace(" ", "_")


def _normalise_scope(scope: str) -> str:
    key = _normalise(scope)
    # Preserve economically distinct segments before collapsing consolidated aliases.
    segment_names = (
        "production precision agriculture", "small agriculture turf",
        "construction forestry", "financial services", "industrial end market",
        "automotive end market", "communications end market", "consumer end market",
    )
    for segment in segment_names:
        if segment in key:
            return segment
    if any(token in key for token in ("consolidated", "deere company", "company total")):
        return "company"
    key = re.sub(r"\b(year over year|at period end|balance sheet at .*)\b", "", key).strip()
    key = re.sub(r"\b(diluted eps|diluted weighted average|midpoint)\b", "", key).strip()
    return key or "company"


def _reconcile_facts(group: list[Finding], agent_count: int) -> tuple[ConsensusFact, ...]:
    candidates: dict[tuple[str, ...], list[tuple[str, dict]]] = defaultdict(list)
    for finding in group:
        for fact in finding.extracted_facts:
            try:
                value = float(fact["value"])
            except (KeyError, TypeError, ValueError):
                continue
            metric = _normalise_metric(str(fact.get("metric", "")))
            basis = _normalise_basis(str(fact.get("basis", "reported")))
            evidence_text = _normalise(str(fact.get("evidence", "")))
            if "consensus" in evidence_text:
                basis = "analyst_consensus"
            elif str(fact.get("fact_type", "")).lower() == "guidance":
                basis = "management_guidance"
            unit = _normalise_unit(str(fact.get("unit", "")))
            if "EPS" in metric and unit == "GBP":
                unit = "GBp"
            if metric == "Net finance charge":
                value = abs(value)
            if metric in {"Operating profit", "Pre-exceptional operating profit"} and "loss" in evidence_text:
                value = -abs(value)
            key = (
                _normalise(metric),
                _normalise(str(fact.get("fiscal_period", finding.fiscal_period))),
                basis,
                unit,
                _normalise_scope(str(fact.get("scope", "Group"))),
                _normalise(str(fact.get("fact_type", "reported"))),
            )
            if key[0] and key[3]:
                normalised = dict(fact)
                normalised["value"] = value
                normalised["metric"] = metric
                normalised["unit"] = unit
                normalised["basis"] = basis
                normalised["scope"] = _normalise_scope(str(fact.get("scope", "Group")))
                normalised["fact_type"] = str(fact.get("fact_type", "reported"))
                normalised["category"] = str(fact.get("category", "financial_performance"))
                candidates[key].append((finding.agent_id, normalised))

    reconciled: list[ConsensusFact] = []
    for (metric_key, period_key, basis_key, unit, scope_key, fact_type_key), facts in candidates.items():
        by_value: dict[float, list[tuple[str, dict]]] = defaultdict(list)
        for agent_id, fact in facts:
            by_value[round(fact["value"], 6)].append((agent_id, fact))
        winning_value, supporters = max(
            by_value.items(), key=lambda item: len({agent_id for agent_id, _ in item[1]})
        )
        supporting_agents = sorted({agent_id for agent_id, _ in supporters})
        representative = max(
            (fact for _, fact in supporters),
            key=lambda fact: sum(bool(fact.get(field)) for field in ("evidence", "page_or_section", "fiscal_period", "basis")),
        )
        # Extraction agreement is measured against the full research panel.
        # A fact asserted by the only agent that found a report is not consensus.
        agreement = len(supporting_agents) / max(agent_count, 1)
        evidence_quality = sum(
            bool(representative.get(field))
            for field in ("evidence", "page_or_section", "fiscal_period", "basis")
        ) / 4
        confidence = round(0.75 * agreement + 0.25 * evidence_quality, 3)
        reconciled.append(
            ConsensusFact(
                metric=str(representative.get("metric", metric_key)),
                value=winning_value,
                unit=unit,
                fiscal_period=str(representative.get("fiscal_period", period_key)),
                basis=str(representative.get("basis", basis_key)),
                category=str(representative.get("category", "financial_performance")),
                scope=str(representative.get("scope", scope_key)),
                fact_type=str(representative.get("fact_type", fact_type_key)),
                page_or_section=str(representative.get("page_or_section", "")),
                evidence=str(representative.get("evidence", "")),
                supporting_agents=tuple(supporting_agents),
                confidence=confidence,
                conflicting_values=tuple(sorted(value for value in by_value if value != winning_value)),
            )
        )
    reconciled.sort(key=lambda fact: (fact.fiscal_period, fact.metric, fact.confidence), reverse=True)
    return tuple(reconciled)


def _reconcile_observations(group: list[Finding], agent_count: int) -> tuple[ConsensusObservation, ...]:
    candidates: dict[tuple[str, str, str, str], list[tuple[str, dict]]] = defaultdict(list)
    for finding in group:
        for observation in finding.observations:
            key = (
                _normalise(str(observation.get("indicator", ""))),
                _normalise(str(observation.get("direction", ""))),
                _normalise(str(observation.get("scope", "Group"))),
                _normalise(str(observation.get("horizon", finding.fiscal_period))),
            )
            if key[0] and key[1]:
                candidates[key].append((finding.agent_id, observation))
    results = []
    for _, values in candidates.items():
        agents = sorted({agent_id for agent_id, _ in values})
        representative = max(
            (value for _, value in values), key=lambda value: len(str(value.get("evidence", "")))
        )
        evidence_quality = 1.0 if representative.get("evidence") else 0.0
        confidence = round(0.8 * len(agents) / max(agent_count, 1) + 0.2 * evidence_quality, 3)
        results.append(
            ConsensusObservation(
                indicator=str(representative.get("indicator", "")),
                direction=str(representative.get("direction", "")),
                scope=str(representative.get("scope", "Group")),
                horizon=str(representative.get("horizon", "")),
                evidence=str(representative.get("evidence", "")),
                supporting_agents=tuple(agents),
                confidence=confidence,
            )
        )
    results.sort(key=lambda item: (item.confidence, item.indicator), reverse=True)
    return tuple(results)


def reconcile_findings(
    *, run_id: str, company_id: str, signal_type: str,
    findings: list[Finding], agent_count: int,
    expected_targets: tuple[dict[str, str], ...] = (),
) -> ReconciledSignal:
    clusters: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        if finding.official and finding.source_url:
            clusters[report_identity(finding)].append(finding)

    items: list[ConsensusItem] = []
    disagreements: list[str] = []
    for identity, group in clusters.items():
        agents = sorted({item.agent_id for item in group})
        domains = sorted({_domain(item.source_url) or item.source_domain for item in group})
        authority = mean(SOURCE_AUTHORITY.get(item.source_kind, 0.7) for item in group)
        agreement = len(agents) / max(agent_count, 1)
        # A single domain is not independent corroboration, even when several
        # agents rediscover it. Two domains earn partial credit; three earn full.
        independence = min(1.0, max(0, len(domains) - 1) / 2)
        completeness = mean(_completeness(item) for item in group)
        officiality = sum(item.official for item in group) / len(group)
        confidence = round(
            0.40 * agreement
            + 0.25 * authority
            + 0.15 * independence
            + 0.15 * completeness
            + 0.05 * officiality,
            3,
        )
        representative = max(
            group,
            key=lambda item: (SOURCE_AUTHORITY.get(item.source_kind, 0.7), _completeness(item)),
        )
        facts = _reconcile_facts(group, agent_count)
        observations = _reconcile_observations(group, agent_count)
        if len({item.published_at for item in group if item.published_at}) > 1:
            disagreements.append(f"Conflicting publication dates for {identity}")
        items.append(
            ConsensusItem(
                identity=identity,
                report_title=representative.report_title,
                report_type=representative.report_type,
                fiscal_period=representative.fiscal_period,
                period_end=representative.period_end,
                published_at=representative.published_at,
                source_url=representative.source_url,
                document_url=representative.document_url or representative.source_url,
                supporting_agents=tuple(agents),
                supporting_domains=tuple(domains),
                confidence=confidence,
                confidence_factors={
                    "agreement": round(agreement, 3),
                    "source_authority": round(authority, 3),
                    "source_independence": round(independence, 3),
                    "record_completeness": round(completeness, 3),
                    "officiality": round(officiality, 3),
                },
                evidence=tuple(dict.fromkeys(item.evidence for item in group if item.evidence)),
                facts=facts,
                observations=observations,
            )
        )

    items.sort(key=lambda item: (item.period_end, item.published_at, item.confidence), reverse=True)
    leading_quality = mean(item.confidence for item in items[:3]) if items else 0.0
    coverage = 1.0
    if expected_targets:
        found_identities = {item.identity for item in items}
        expected_identities = set()
        for target in expected_targets:
            report_type = target["report_type"]
            family = "periodic_update" if report_type in {"quarterly_results", "trading_update"} else report_type
            expected_identities.add(
                "|".join((_normalise(company_id), _normalise(family), _normalise(target["period_end"])))
            )
        coverage = len(found_identities & expected_identities) / len(expected_identities)
    confirmed_facts = [fact for item in items for fact in item.facts if fact.confidence >= 0.65]
    conflicting_confirmed_facts = [fact for fact in confirmed_facts if fact.conflicting_values]
    extraction_confidence = mean(fact.confidence for fact in confirmed_facts) if confirmed_facts else 0.0
    reports_with_facts = sum(any(fact.confidence >= 0.65 for fact in item.facts) for item in items)
    extraction_coverage = reports_with_facts / len(items) if items else 0.0
    document_confidence = 0.75 * leading_quality + 0.25 * coverage if items else 0.0
    signal_confidence = round(
        0.50 * document_confidence + 0.35 * extraction_confidence + 0.15 * extraction_coverage,
        3,
    ) if items else 0.0
    leading_items = items[:3]
    average_agreement = mean(
        item.confidence_factors["agreement"] for item in leading_items
    ) if leading_items else 0.0
    corroborated_count = sum(len(item.supporting_domains) >= 2 for item in items)
    if not items:
        confidence_explanation = "No usable official report findings were returned, so confidence is 0."
    else:
        coverage_text = (
            f"{round(coverage * len(expected_targets))}/{len(expected_targets)} required report events found"
            if expected_targets else f"{len(items)} report events found (no explicit target checklist)"
        )
        confidence_explanation = (
            f"Confidence {signal_confidence:.3f}: document confidence {document_confidence:.3f} "
            f"({coverage_text}); extraction confidence {extraction_confidence:.3f} from "
            f"{len(confirmed_facts)} reconciled facts across {reports_with_facts}/{len(items)} reports; "
            f"the three most recent events had {average_agreement:.0%} researcher agreement and "
            f"{corroborated_count}/{len(items)} events had multi-organization corroboration."
        )
    successful_agents = len({item.agent_id for item in findings})
    warnings: list[str] = []
    if successful_agents < max(3, agent_count // 2 + 1):
        warnings.append("Fewer than a majority of research agents returned usable findings")
    if items and items[0].confidence < 0.65:
        warnings.append("The leading report did not reach the high-confidence threshold")
    if conflicting_confirmed_facts:
        warnings.append(
            f"{len(conflicting_confirmed_facts)} confirmed facts retain alternative extracted values"
        )
    status = "confirmed" if items and confirmed_facts and signal_confidence >= 0.65 else "needs_review"
    return ReconciledSignal(
        run_id=run_id,
        company_id=company_id,
        signal_type=signal_type,
        status=status,
        confidence=signal_confidence,
        reports=tuple(items),
        agent_count=agent_count,
        successful_agents=successful_agents,
        disagreements=tuple(disagreements),
        warnings=tuple(warnings),
        metadata={
            "reconciled_at": date.today().isoformat(),
            "confidence_version": "v2",
            "target_coverage": round(coverage, 3),
            "expected_target_count": len(expected_targets),
            "leading_evidence_quality": round(leading_quality, 3),
            "leading_researcher_agreement": round(average_agreement, 3),
            "organizationally_corroborated_reports": corroborated_count,
            "document_confidence": round(document_confidence, 3),
            "extraction_confidence": round(extraction_confidence, 3),
            "extraction_coverage": round(extraction_coverage, 3),
            "confirmed_fact_count": len(confirmed_facts),
            "conflicting_confirmed_fact_count": len(conflicting_confirmed_facts),
            "confidence_explanation": confidence_explanation,
        },
    )
