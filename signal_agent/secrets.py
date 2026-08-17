from __future__ import annotations

import os
from pathlib import Path


def load_secret(name: str, env_file: str | Path = ".env") -> str:
    value = os.environ.get(name, "").strip()
    if value:
        return value
    path = Path(env_file)
    if path.is_file():
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, candidate = line.split("=", 1)
            if key.strip() == name:
                value = candidate.strip().strip("'\"")
                if value:
                    return value
    raise RuntimeError(f"{name} is not set; add it to the process environment or ignored .env file")
