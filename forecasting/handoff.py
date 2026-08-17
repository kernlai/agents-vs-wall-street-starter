from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from .contracts import CompanyProfile, SignalObservation, SignalRole
from .profile import load_company_profile
from .resolvers import (
    resolve_explicit_driver, resolve_management_guidance,
    resolve_qualitative_modifier, resolve_scenario_trigger,
)


class HandoffValidationError(ValueError):
    pass


def load_v2_1(payload: dict[str, Any]) -> tuple[CompanyProfile, list[SignalObservation]]:
    if payload.get("schemaVersion") != "forecast_input.v2.1":
        raise HandoffValidationError("forecast input must use forecast_input.v2.1")
    source_root = Path(payload["sourceRoot"]).resolve()
    sources = [item for item in payload["sources"] if item.get("cutoffDecision") == "accepted"]
    profile_payload = {
        "schemaVersion": "1.0", "company": payload["company"],
        "informationCutoff": payload["informationCutoff"], "sources": sources,
        "profile": payload["profile"], "metrics": payload["metrics"],
        "signalMap": payload["signalMap"],
    }
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "profile.json"
        path.write_text(json.dumps(profile_payload), encoding="utf-8")
        profile = load_company_profile(path, repository_root=source_root)

    observations: list[SignalObservation] = []
    for raw in payload["observations"]:
        signal = profile.signals.get(raw["signalId"])
        if signal is None:
            raise HandoffValidationError(f"unknown signal {raw['signalId']}")
        common = {
            "profile": profile, "signal_id": signal.signal_id,
            "source_id": raw["sourceId"], "exact_quote": raw["exactQuote"],
            "locator": raw["locator"], "period": raw["period"],
            "evidence_quality": raw.get("evidenceQuality", "high"),
            "freshness": raw.get("freshness", "current"),
        }
        if signal.role is SignalRole.ANCHOR:
            observations.append(resolve_management_guidance(
                **common, low=raw["value"]["low"], high=raw["value"]["high"], units=raw["units"]
            ))
        elif signal.role is SignalRole.DRIVER:
            observations.append(resolve_explicit_driver(
                **common, adjustment=raw["value"], units=raw["units"], calculation=raw["calculation"]
            ))
        elif signal.role is SignalRole.MODIFIER:
            observations.append(resolve_qualitative_modifier(**common, assessment=raw["value"]))
        elif signal.role is SignalRole.SCENARIO_TRIGGER:
            observations.append(resolve_scenario_trigger(
                **common, condition=raw["condition"], adjustment=raw["value"],
                units=raw["units"], calculation=raw["calculation"],
            ))
    return profile, observations
