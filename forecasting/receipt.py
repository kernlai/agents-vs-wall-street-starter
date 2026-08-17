from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

from .challenge import ChallengeReport
from .contracts import CompanyProfile, ForecastResult


COMPILER_VERSION = "0.1.0"
_CAMEL_BOUNDARY = re.compile(r"_([a-z])")


def _camel_case(value: str) -> str:
    return _CAMEL_BOUNDARY.sub(lambda match: match.group(1).upper(), value)


def _jsonable(value: Any) -> Any:
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return {_camel_case(field.name): _jsonable(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {_camel_case(str(key)): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def build_run_receipt(
    profile: CompanyProfile,
    result: ForecastResult,
    challenge: ChallengeReport,
) -> dict[str, Any]:
    metric = profile.metrics.get(result.metric_id)
    if metric is None:
        raise ValueError(f"unknown metric {result.metric_id}")
    sources = [
        {
            "id": source.source_id,
            "publisher": source.publisher,
            "title": source.title,
            "documentType": source.document_type,
            "publishedAt": _jsonable(source.published_at),
            "url": source.url,
            "localPath": source.local_path_reference,
            "sha256": source.sha256,
        }
        for source in profile.sources.values()
    ]
    profile_sections = {
        section: [
            {"claim": claim.claim, "sourceIds": list(claim.source_ids)}
            for claim in claims
        ]
        for section, claims in profile.profile_sections.items()
    }
    signal_map = [
        _jsonable(signal)
        for signal in profile.signals.values()
        if signal.target_metric_id == result.metric_id
    ]
    return {
        "schemaVersion": "1.0",
        "compilerVersion": COMPILER_VERSION,
        "company": {
            "id": profile.company.company_id,
            "name": profile.company.name,
            "ticker": profile.company.ticker,
            "currency": profile.company.currency,
            "fiscalCalendar": profile.company.fiscal_calendar,
        },
        "informationCutoff": profile.information_cutoff.isoformat(),
        "profile": profile_sections,
        "sources": sources,
        "metric": _jsonable(metric),
        "signalMap": signal_map,
        "forecast": {
            "period": result.period,
            "units": result.units,
            "anchorRange": _jsonable(result.anchor_range),
            "driverAdjustment": _jsonable(result.driver_adjustment),
            "baseRange": _jsonable(result.base_range),
            "baseForecast": _jsonable(result.base_forecast),
            "formula": result.formula,
            "modifiers": _jsonable(result.modifiers),
            "scenarios": _jsonable(result.scenarios),
        },
        "decisions": {
            "accepted": _jsonable(result.accepted),
            "rejected": _jsonable(result.rejected),
        },
        "challenge": _jsonable(challenge),
    }


def write_run_receipt(
    profile: CompanyProfile,
    result: ForecastResult,
    challenge: ChallengeReport,
    path: str | Path,
) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = build_run_receipt(profile, result, challenge)
    destination.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return destination
