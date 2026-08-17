from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPANIES = ("HAS", "HD", "ADI", "DE")
OUTPUT_FILES = {
    "HAS": "HAS-FY2026.xlsx",
    "HD": "HD-FY2026Q2.xlsx",
    "ADI": "ADI-FY2026Q3.xlsx",
    "DE": "DE-FY2026Q3.xlsx",
}
STAGE_ORDER = ("signals", "inputs", "forecasts", "workbooks")


class PipelineError(RuntimeError):
    pass


class RunLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.Lock()
        path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, message: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        line = f"[{timestamp}] {message}"
        with self.lock:
            print(line, flush=True)
            with self.path.open("a") as stream:
                stream.write(line + "\n")


def run_command(command: list[str], log: RunLog, *, allowed_exit_codes: tuple[int, ...] = (0,)) -> None:
    log.write("RUN " + " ".join(command))
    process = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
    )
    if process.stdout:
        for line in process.stdout.rstrip().splitlines():
            log.write("  " + line)
    if process.returncode not in allowed_exit_codes:
        raise PipelineError(f"Command failed with exit code {process.returncode}: {' '.join(command)}")


def ensure_module(module: str, owner: str) -> None:
    if importlib.util.find_spec(module) is None:
        raise PipelineError(
            f"Missing {owner} implementation: Python module `{module}`. "
            f"Implement the interface documented in TEAM-HANDOFF.md."
        )


def validate_forecast(company: str, path: Path) -> None:
    if not path.exists():
        raise PipelineError(f"Forecast stage did not create {path}")
    payload = json.loads(path.read_text())
    if payload.get("schema_version") != "company_forecast.v1":
        raise PipelineError(f"{path} must use schema_version company_forecast.v1")
    if payload.get("company_id") != company:
        raise PipelineError(f"{path} has the wrong company_id")
    if len(payload.get("forecasts", [])) != 3:
        raise PipelineError(f"{path} must contain exactly three forecasts")
    for forecast in payload["forecasts"]:
        if not isinstance(forecast.get("value"), (int, float)):
            raise PipelineError(f"Non-numeric forecast in {path}: {forecast.get('metric')}")


def validate_handoff(company: str, path: Path) -> None:
    if not path.exists():
        raise PipelineError(f"Missing prepared v2.1 handoff for {company}: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schemaVersion") != "forecast_input.v2.1" or payload.get("companyId") != company:
        raise PipelineError(f"{path} must be a forecast_input.v2.1 artifact for {company}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run research, forecasting and workbook generation")
    parser.add_argument("--companies", nargs="+", choices=COMPANIES, default=list(COMPANIES))
    parser.add_argument("--reasoning-effort", choices=("none", "low", "medium", "high", "xhigh", "max"), default="medium")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--parallel-companies", type=int, default=4, choices=range(1, 5))
    parser.add_argument("--through", choices=STAGE_ORDER, default="workbooks")
    parser.add_argument("--skip-research", action="store_true", help="Reuse existing forecast_inputs/*.json")
    parser.add_argument("--max-minutes", type=float, default=45, help="Maximum live-research runtime")
    args = parser.parse_args()

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log = RunLog(ROOT / "logs" / f"pipeline-{run_id}.log")
    log.write(f"START run_id={run_id} companies={','.join(args.companies)} model={args.model} effort={args.reasoning_effort}")
    try:
        if STAGE_ORDER.index(args.through) >= STAGE_ORDER.index("forecasts"):
            ensure_module("forecasting.cli", "forecasting stage")
        if args.through == "workbooks":
            ensure_module("workbook_generator.cli", "workbook generation stage")
        if not args.skip_research:
            research_command = [
                sys.executable, "-m", "signal_agent.research_pipeline",
                "--model", args.model, "--reasoning-effort", args.reasoning_effort,
                "--company-workers", str(args.parallel_companies), "--max-minutes", str(args.max_minutes),
            ]
            for company in args.companies:
                research_command.extend(["--company", company])
            run_command(research_command, log)

        def run_company(company: str) -> None:
            log.write(f"COMPANY {company} START")
            if args.through == "signals":
                log.write(f"COMPANY {company} COMPLETE through=signals")
                return
            handoff_path = ROOT / "forecast_inputs" / f"{company}.json"
            validate_handoff(company, handoff_path)
            log.write(f"COMPANY {company} {'REUSE' if args.skip_research else 'USE'} {handoff_path.relative_to(ROOT)}")
            if args.through == "inputs":
                log.write(f"COMPANY {company} COMPLETE through=inputs")
                return
            forecast_path = ROOT / "forecasts" / f"{company}.json"
            run_command(
                [
                    sys.executable, "-m", "forecasting.cli",
                    "--company", company,
                    "--input", str(ROOT / "forecast_inputs" / f"{company}.json"),
                    "--output", str(forecast_path),
                ],
                log,
            )
            validate_forecast(company, forecast_path)
            if args.through == "forecasts":
                log.write(f"COMPANY {company} COMPLETE through=forecasts")
                return
            run_command(
                [
                    sys.executable, "-m", "workbook_generator.cli",
                    "--company", company,
                    "--forecast", str(ROOT / "forecasts" / f"{company}.json"),
                    "--template", str(ROOT / "challenge" / "templates" / OUTPUT_FILES[company]),
                    "--output", str(ROOT / "submission" / OUTPUT_FILES[company]),
                ],
                log,
            )
            log.write(f"COMPANY {company} COMPLETE through=workbooks")

        with ThreadPoolExecutor(max_workers=min(args.parallel_companies, len(args.companies))) as executor:
            futures = {executor.submit(run_company, company): company for company in args.companies}
            failures = []
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as error:
                    failures.append(f"{futures[future]}: {error}")
            if failures:
                raise PipelineError("; ".join(failures))

        if args.through in {"forecasts", "workbooks"} and set(args.companies) == set(COMPANIES):
            run_command([sys.executable, "-m", "forecasting.aggregate"], log)
        if args.through == "workbooks":
            # validate_forecasts uses 0=clean, 1=warnings only, 2=errors.
            run_command(
                [sys.executable, "scripts/validate_forecasts.py", "evaluation/forecasts.json"],
                log, allowed_exit_codes=(0, 1),
            )
            run_command(["npm", "run", "check:forecasts"], log)
        log.write("COMPLETE all requested pipeline stages succeeded")
    except Exception as error:
        log.write(f"FAILED {error}")
        raise SystemExit(str(error)) from error
    finally:
        log.write(f"END log={log.path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
