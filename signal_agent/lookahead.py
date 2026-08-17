from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Protocol

from .research_validation import SUPPORTED_LOOKAHEAD_ISSUES
from .secrets import load_secret
from .http import verified_ssl_context


class ReviewTransport(Protocol):
    def post(self, url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]: ...


class UrlLibReviewTransport:
    def post(self, url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=timeout, context=verified_ssl_context()) as response:
            value = json.load(response)
        if not isinstance(value, dict):
            raise RuntimeError("OpenAI reviewer returned a non-object response")
        return value


def _output_text(response: dict[str, Any]) -> str:
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                return content["text"]
    raise RuntimeError("OpenAI reviewer response did not contain output text")


def incomplete_review(reason: str) -> dict[str, Any]:
    return {
        "schemaVersion": "lookahead_review.v1",
        "status": "incomplete",
        "issues": [],
        "reason": reason,
        "provider": "none",
        "model": "none",
        "requestId": "none",
    }


@dataclass
class OpenAIReviewProvider:
    api_key: str = ""
    model: str = "gpt-5.6-terra"
    reasoning_effort: str = "medium"
    timeout_seconds: int = 120
    transport: ReviewTransport | None = None

    def __post_init__(self) -> None:
        self.api_key = self.api_key or load_secret("OPENAI_API_KEY")
        self.transport = self.transport or UrlLibReviewTransport()

    def review(self, review_input: dict[str, Any]) -> dict[str, Any]:
        request_body = {
            "model": self.model,
            "reasoning": {"effort": self.reasoning_effort},
            "store": False,
            "instructions": (
                "Act as an independent evidence-bound look-ahead reviewer. Use only the supplied source "
                "manifest and excerpts. Do not use model memory as evidence. Flag claims that cannot be "
                "reconstructed from admissible excerpts, post-cutoff facts, or actuals presented as guidance. "
                "A latest same-metric actual may be used as a forecast persistence baseline only when methodology "
                "and calculation explicitly declare target equals that actual; do not label that as period leakage. Flag "
                "unsupported factual inputs, but distinguish them from explicitly declared forecast assumptions. A "
                "declared deterministic reconstruction (for example annualizing a sourced half-year actual) is an "
                "analyst forecast method, not a claim that management supplied the resulting target. It need not be "
                "stated by the source when its input, assumption, arithmetic, units, and target period are all explicit. "
                "undeclared assumptions, suspicious precision, or period leakage. Return the schema only."
            ),
            "input": json.dumps(review_input, sort_keys=True, separators=(",", ":")),
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "lookahead_review",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["passed", "blocked_for_lookahead"]},
                            "issues": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "string", "enum": sorted(SUPPORTED_LOOKAHEAD_ISSUES)},
                                        "severity": {"type": "string", "enum": ["warning", "error"]},
                                        "claimIds": {"type": "array", "items": {"type": "string"}},
                                        "sourceIds": {"type": "array", "items": {"type": "string"}},
                                        "explanation": {"type": "string"},
                                    },
                                    "required": ["code", "severity", "claimIds", "sourceIds", "explanation"],
                                    "additionalProperties": False,
                                },
                            },
                            "reasoningSummary": {"type": "string"},
                        },
                        "required": ["status", "issues", "reasoningSummary"],
                        "additionalProperties": False,
                    },
                }
            },
        }
        assert self.transport is not None
        response = self.transport.post(
            "https://api.openai.com/v1/responses",
            request_body,
            {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            self.timeout_seconds,
        )
        try:
            payload = json.loads(_output_text(response))
        except json.JSONDecodeError as error:
            raise RuntimeError("OpenAI reviewer returned invalid JSON") from error
        if not isinstance(payload, dict):
            raise RuntimeError("OpenAI reviewer output must be an object")
        issues = payload.get("issues", [])
        if any(issue.get("severity") == "error" for issue in issues):
            payload["status"] = "blocked_for_lookahead"
        return {
            "schemaVersion": "lookahead_review.v1",
            **payload,
            "provider": "openai",
            "model": self.model,
            "requestId": str(response.get("id", "unknown")),
            "reasoningEffort": self.reasoning_effort,
        }
