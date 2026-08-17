from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from urllib.parse import urlsplit

from .models import Company, Finding, ReconciledSignal


SCHEMA = """
CREATE TABLE IF NOT EXISTS companies (
  company_id TEXT PRIMARY KEY, payload TEXT NOT NULL, updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS runs (
  run_id TEXT PRIMARY KEY, company_id TEXT NOT NULL, signal_type TEXT NOT NULL,
  status TEXT NOT NULL, confidence REAL NOT NULL, payload TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS findings (
  run_id TEXT NOT NULL, agent_id TEXT NOT NULL, company_id TEXT NOT NULL,
  signal_type TEXT NOT NULL, identity_key TEXT NOT NULL, source_domain TEXT NOT NULL,
  payload TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS source_memory (
  company_id TEXT NOT NULL, signal_type TEXT NOT NULL, domain TEXT NOT NULL,
  useful_count INTEGER NOT NULL DEFAULT 0, rejected_count INTEGER NOT NULL DEFAULT 0,
  last_seen TEXT DEFAULT CURRENT_TIMESTAMP, score REAL NOT NULL DEFAULT 0.5,
  PRIMARY KEY (company_id, signal_type, domain)
);
"""


class SignalStore:
    def __init__(self, path: str | Path = "data/signals.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path, timeout=30)
        self.connection.execute("PRAGMA busy_timeout=30000")
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.executescript(SCHEMA)

    def save_company(self, company: Company) -> None:
        self.connection.execute(
            "INSERT INTO companies(company_id,payload) VALUES(?,?) "
            "ON CONFLICT(company_id) DO UPDATE SET payload=excluded.payload, updated_at=CURRENT_TIMESTAMP",
            (company.company_id, json.dumps(asdict(company))),
        )
        self.connection.commit()

    def source_hints(self, company_id: str, signal_type: str, limit: int = 8) -> list[str]:
        rows = self.connection.execute(
            "SELECT domain FROM source_memory WHERE company_id=? AND signal_type=? "
            "ORDER BY score DESC, useful_count DESC LIMIT ?",
            (company_id, signal_type, limit),
        ).fetchall()
        return [row[0] for row in rows]

    def save_run(
        self, signal: ReconciledSignal, findings: list[Finding], identity_fn,
    ) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO runs(run_id,company_id,signal_type,status,confidence,payload) "
            "VALUES(?,?,?,?,?,?)",
            (
                signal.run_id, signal.company_id, signal.signal_type,
                signal.status, signal.confidence, json.dumps(signal.to_dict()),
            ),
        )
        consensus_identities = {item.identity for item in signal.reports if item.confidence >= 0.65}
        for finding in findings:
            identity = identity_fn(finding)
            domain = urlsplit(finding.source_url).netloc.lower().removeprefix("www.")
            self.connection.execute(
                "INSERT INTO findings(run_id,agent_id,company_id,signal_type,identity_key,source_domain,payload) "
                "VALUES(?,?,?,?,?,?,?)",
                (
                    signal.run_id, finding.agent_id, finding.company_id,
                    finding.signal_type, identity, domain, json.dumps(finding.to_dict()),
                ),
            )
            useful = identity in consensus_identities
            self.connection.execute(
                "INSERT INTO source_memory(company_id,signal_type,domain,useful_count,rejected_count,score) "
                "VALUES(?,?,?,?,?,?) ON CONFLICT(company_id,signal_type,domain) DO UPDATE SET "
                "useful_count=useful_count+excluded.useful_count, "
                "rejected_count=rejected_count+excluded.rejected_count, last_seen=CURRENT_TIMESTAMP, "
                "score=MIN(0.95,MAX(0.10,(useful_count+excluded.useful_count+1.0)/"
                "(useful_count+rejected_count+excluded.useful_count+excluded.rejected_count+2.0)))",
                (finding.company_id, finding.signal_type, domain, int(useful), int(not useful), 0.667 if useful else 0.333),
            )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
