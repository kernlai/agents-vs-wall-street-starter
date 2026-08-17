from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .models import Company, Finding
from .offline_corpus import build_offline_context


def _verified_ssl_context() -> ssl.SSLContext:
    """Build a verified context that also works with python.org macOS builds.

    Those builds can have an empty OpenSSL certificate directory even when the
    operating system has valid roots. Prefer an explicit operator setting, then
    certifi when available, and finally Python's normal verified defaults.
    """
    configured_bundle = os.environ.get("SSL_CERT_FILE")
    if configured_bundle:
        return ssl.create_default_context(cafile=configured_bundle)
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


class ResearchProvider(Protocol):
    def research(
        self, *, company: Company, signal_type: str, agent_id: str,
        strategy: str, source_hints: list[str], prompt: str,
    ) -> list[Finding]: ...


def _output_text(response: dict) -> str:
    for item in response.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    return content.get("text", "")
    raise ValueError("The model response did not contain output text")


@dataclass
class OpenAIWebResearchProvider:
    model: str = "gpt-5.6-terra"
    reasoning_effort: str = "medium"
    api_key: str = ""
    timeout_seconds: int = 180

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for live web research")

    def research(
        self, *, company: Company, signal_type: str, agent_id: str,
        strategy: str, source_hints: list[str], prompt: str,
    ) -> list[Finding]:
        offline_context = build_offline_context(company)
        company_context = json.dumps(
            {
                "company_id": company.company_id,
                "name": company.name,
                "ticker": company.ticker,
                "exchange": company.exchange,
                "isin": company.isin,
                "investor_relations_url": company.investor_relations_url,
                "regulator_urls": company.regulator_urls,
                "required_report_targets": company.financial_report_targets,
                "priority_fact_targets": company.financial_fact_targets,
                "priority_observation_targets": company.financial_observation_targets,
                "previously_useful_domains": source_hints,
            },
            indent=2,
        )
        request_body = {
            "model": self.model,
            "reasoning": {"effort": self.reasoning_effort},
            "tools": [{"type": "web_search"}],
            "instructions": prompt,
            "input": (
                f"You are research instance {agent_id}. Strategy: {strategy}.\n"
                f"Signal type: {signal_type}.\nCompany:\n{company_context}\n\n"
                f"{offline_context}\n"
                "Search independently. Return only the requested JSON object."
            ),
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "financial_report_findings",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "findings": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "report_title": {"type": "string"},
                                        "report_type": {"type": "string"},
                                        "fiscal_period": {"type": "string"},
                                        "period_end": {"type": "string"},
                                        "published_at": {"type": "string"},
                                        "source_url": {"type": "string"},
                                        "source_domain": {"type": "string"},
                                        "source_kind": {
                                            "type": "string",
                                            "enum": [
                                                "company_ir", "regulator", "stock_exchange",
                                                "official_archive", "other_official"
                                            ]
                                        },
                                        "official": {"type": "boolean"},
                                        "evidence": {"type": "string"},
                                        "document_url": {"type": "string"},
                                        "retrieval_notes": {"type": "string"},
                                        "extracted_facts": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "metric": {"type": "string"},
                                                    "value": {"type": "number"},
                                                    "unit": {"type": "string"},
                                                    "fiscal_period": {"type": "string"},
                                                    "basis": {"type": "string"},
                                                    "category": {
                                                        "type": "string",
                                                        "enum": [
                                                            "financial_performance", "operating_drivers",
                                                            "guidance", "capital_and_cash", "accounting_adjustments"
                                                        ]
                                                    },
                                                    "scope": {"type": "string"},
                                                    "fact_type": {
                                                        "type": "string",
                                                        "enum": ["reported", "guidance", "derived"]
                                                    },
                                                    "page_or_section": {"type": "string"},
                                                    "evidence": {"type": "string"}
                                                },
                                                "required": [
                                                    "metric", "value", "unit", "fiscal_period",
                                                    "basis", "category", "scope", "fact_type",
                                                    "page_or_section", "evidence"
                                                ],
                                                "additionalProperties": False
                                            }
                                        },
                                        "observations": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "indicator": {"type": "string"},
                                                    "direction": {
                                                        "type": "string",
                                                        "enum": ["improving", "stable", "deteriorating", "mixed"]
                                                    },
                                                    "scope": {"type": "string"},
                                                    "horizon": {"type": "string"},
                                                    "evidence": {"type": "string"}
                                                },
                                                "required": ["indicator", "direction", "scope", "horizon", "evidence"],
                                                "additionalProperties": False
                                            }
                                        },
                                    },
                                    "required": [
                                        "report_title", "report_type", "fiscal_period",
                                        "period_end", "published_at", "source_url",
                                        "source_domain", "source_kind", "official",
                                        "evidence", "document_url", "retrieval_notes",
                                        "extracted_facts",
                                        "observations",
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["findings"],
                        "additionalProperties": False,
                    },
                }
            },
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(request_body).encode(),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout_seconds,
                context=_verified_ssl_context(),
            ) as result:
                response = json.load(result)
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            raise RuntimeError(f"OpenAI request failed ({error.code}): {detail}") from error
        payload = json.loads(_output_text(response))
        findings: list[Finding] = []
        for raw in payload.get("findings", []):
            raw.update(
                agent_id=agent_id,
                strategy=strategy,
                company_id=company.company_id,
                signal_type=signal_type,
            )
            findings.append(Finding.from_dict(raw))
        return findings


class FixtureResearchProvider:
    """Offline provider used by tests and repeatable demonstrations."""

    def __init__(self, fixture_directory: str | Path) -> None:
        self.fixture_directory = Path(fixture_directory)

    def research(
        self, *, company: Company, signal_type: str, agent_id: str,
        strategy: str, source_hints: list[str], prompt: str,
    ) -> list[Finding]:
        path = self.fixture_directory / f"{company.company_id}-{agent_id}.json"
        payload = json.loads(path.read_text())
        findings = []
        for raw in payload["findings"]:
            raw.update(
                agent_id=agent_id, strategy=strategy,
                company_id=company.company_id, signal_type=signal_type,
            )
            findings.append(Finding.from_dict(raw))
        return findings
