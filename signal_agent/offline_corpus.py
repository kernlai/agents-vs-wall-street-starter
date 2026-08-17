from __future__ import annotations

import json
import re
from pathlib import Path

from .models import Company


ROOT = Path(__file__).resolve().parents[1]
CORPUS_ROOT = ROOT / "challenge" / "offline-data"
COMPANY_DIRECTORIES = {
    "HAS": "hays",
    "HD": "home-depot",
    "ADI": "analog-devices",
    "DE": "deere",
}
WORD_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
STOP_WORDS = {"a", "adjusted", "and", "company", "for", "of", "the", "total", "worldwide"}


def _frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    metadata: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        try:
            metadata[key.strip()] = json.loads(value.strip())
        except json.JSONDecodeError:
            metadata[key.strip()] = value.strip()
    return metadata


def _terms(company: Company) -> set[str]:
    labels = [str(item.get("metric", "")) for item in company.financial_fact_targets]
    words = {word.casefold() for label in labels for word in WORD_RE.findall(label)}
    return words - STOP_WORDS


def build_offline_context(
    company: Company, *, corpus_root: str | Path = CORPUS_ROOT,
    document_limit: int = 10, character_limit: int = 18_000,
) -> str:
    """Return a bounded, recent, metric-relevant slice of the frozen corpus."""
    directory_name = COMPANY_DIRECTORIES.get(company.company_id)
    directory = Path(corpus_root) / directory_name if directory_name else None
    if directory is None or not directory.exists():
        return "No supplied offline corpus was found for this company."

    terms = _terms(company)
    candidates: list[tuple[int, str, Path, str, dict[str, object]]] = []
    for path in directory.rglob("*.md"):
        if path.name in {"INDEX.md", "README.md"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        metadata = _frontmatter(text)
        lowered = text.casefold()
        relevance = sum(min(lowered.count(term), 8) for term in terms)
        published = str(metadata.get("published_at", ""))
        candidates.append((relevance, published, path, text, metadata))

    # Favor recent documents while retaining metric relevance within the recent set.
    recent = sorted(candidates, key=lambda item: (item[1], item[0]), reverse=True)[:40]
    selected = sorted(recent, key=lambda item: (item[0], item[1]), reverse=True)[:document_limit]
    sections = [
        "SUPPLIED FROZEN CORPUS (frozen 2026-08-14):",
        "Use these local excerpts as reproducible evidence and search leads. Verify current facts "
        "against official web sources. Cite the corpus path in retrieval_notes when it informed a finding.",
    ]
    per_document = max(900, character_limit // max(len(selected), 1))
    for _, _, path, text, metadata in selected:
        body_start = text.find("\n---\n", 4)
        body = text[body_start + 5:] if body_start >= 0 else text
        paragraphs = [re.sub(r"\s+", " ", block).strip() for block in re.split(r"\n\s*\n", body)]
        ranked = sorted(
            (block for block in paragraphs if len(block) >= 40),
            key=lambda block: sum(min(block.casefold().count(term), 3) for term in terms),
            reverse=True,
        )
        excerpt = "\n".join(ranked[:3])[:per_document]
        relative = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()
        sections.append(
            f"\nSOURCE: {relative}\n"
            f"PUBLISHED: {metadata.get('published_at', '')}; PERIOD: {metadata.get('period', '')}; "
            f"TYPE: {metadata.get('document_type', '')}\n{excerpt}"
        )
    return "\n".join(sections)[:character_limit]
