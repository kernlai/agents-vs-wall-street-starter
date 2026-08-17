from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from .lookahead import ReviewTransport, UrlLibReviewTransport, _output_text
from .secrets import load_secret


PROFILE_SECTIONS = (
    "businessModel", "productsAndCustomers", "segmentsAndGeographies", "fiscalCalendar",
    "revenueAndCostDrivers", "accountingDefinitions", "guidanceStyle",
    "cyclicalityAndSeasonality", "externalExposures",
)


def _claim_schema(quote_ids: list[str] | None = None) -> dict[str, Any]:
    quote_id_schema: dict[str, Any] = {"type": "string"}
    if quote_ids:
        quote_id_schema["enum"] = quote_ids
    return {
        "type": "array", "minItems": 1, "maxItems": 2,
        "items": {
            "type": "object",
            "properties": {
                "claimId": {"type": "string"}, "claim": {"type": "string"},
                "quoteIds": {"type": "array", "minItems": 1, "items": quote_id_schema},
            },
            "required": ["claimId", "claim", "quoteIds"],
            "additionalProperties": False,
        },
    }


def proposal_schema(quote_ids: list[str] | None = None) -> dict[str, Any]:
    profile = {section: _claim_schema(quote_ids) for section in PROFILE_SECTIONS}
    quote_id_schema: dict[str, Any] = {"type": "string"}
    if quote_ids:
        quote_id_schema["enum"] = quote_ids
    return {
        "type": "object",
        "properties": {
            "profile": {"type": "object", "properties": profile, "required": list(PROFILE_SECTIONS),
                        "additionalProperties": False},
            "anchors": {
                "type": "array", "minItems": 3, "maxItems": 3,
                "items": {
                    "type": "object",
                    "properties": {
                        "metricId": {"type": "string"}, "quoteId": quote_id_schema,
                        "locator": {"type": "string"},
                        "low": {"type": "string"}, "high": {"type": "string"},
                        "methodology": {"type": "string", "enum": ["explicit_target_guidance", "persistence_from_latest_actual", "deterministic_reconstruction"]},
                        "reasoning": {"type": "string"}, "calculation": {"type": "string"},
                    },
                    "required": ["metricId", "quoteId", "locator", "low", "high", "methodology", "reasoning", "calculation"],
                    "additionalProperties": False,
                },
            },
            "reasoningSummary": {"type": "string"},
            "rejectedEvidence": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["profile", "anchors", "reasoningSummary", "rejectedEvidence"],
        "additionalProperties": False,
    }


@dataclass
class OpenAIProposalProvider:
    api_key: str = ""
    model: str = "gpt-5.6-terra"
    reasoning_effort: str = "medium"
    timeout_seconds: int = 300
    transport: ReviewTransport | None = None

    def __post_init__(self) -> None:
        self.api_key = self.api_key or load_secret("OPENAI_API_KEY")
        self.transport = self.transport or UrlLibReviewTransport()

    def propose(self, proposal_input: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        instructions = (
            "You are an evidence-bound financial research analyst. Use only the supplied frozen excerpts; "
            "never use memory as evidence. Produce all nine company-profile sections and exactly one forecast "
            "starting range for each of the three configured metrics. Cite only supplied quoteIds; never transcribe "
            "or manufacture a quotation. Decimal values must be plain decimal strings in the metric's stated "
            "units. Prefer explicit target-period management guidance. If none exists, use the latest same-metric "
            "actual as a clearly declared persistence baseline; this is a forecast method, not a claim that the "
            "actual is target-period guidance. Persistence is only valid for a same-length immediately prior period, "
            "and a same-length prior-period actual must be preferred over partial-period annualization. For a full-year "
            "target only when no prior full-year actual is supplied, use deterministic_reconstruction and explicitly "
            "annualize the half-year value (multiply by 2) unless the evidence supplies a better formula. Never "
            "return an empty or placeholder zero. If guidance is a point, set low and high equal. If an "
            "explicit range must be reconstructed from a stated midpoint and tolerance, calculate it exactly and "
            "explain that calculation. Do not turn qualitative commentary into a number. Return only the schema."
        )
        body = {
            "model": self.model, "reasoning": {"effort": self.reasoning_effort}, "store": False,
            "instructions": instructions,
            "input": json.dumps(proposal_input, sort_keys=True, separators=(",", ":")),
            "text": {"format": {"type": "json_schema", "name": "forecast_research_proposal",
                                "strict": True, "schema": proposal_schema([
                                    item["quoteId"] for item in proposal_input.get("frozenEvidence", [])
                                ])}},
        }
        assert self.transport is not None
        response = self.transport.post(
            "https://api.openai.com/v1/responses", body,
            {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            self.timeout_seconds,
        )
        try:
            result = json.loads(_output_text(response))
        except json.JSONDecodeError as error:
            raise RuntimeError("OpenAI proposal returned invalid JSON") from error
        if not isinstance(result, dict):
            raise RuntimeError("OpenAI proposal output must be an object")
        metadata = {
            "requestId": str(response.get("id", "unknown")),
            "promptSha256": hashlib.sha256((instructions + body["input"]).encode()).hexdigest(),
        }
        return result, metadata
