from __future__ import annotations

import argparse
from pathlib import Path

from forecasting import (
    ChallengeReport,
    ForecastResult,
    challenge_forecast,
    compile_forecast,
    load_company_profile,
    resolve_management_guidance,
    resolve_qualitative_modifier,
    write_run_receipt,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "build" / "example-adi-revenue-receipt.json"
SOURCE_ID = "adi-fy2026q2-earnings-release"
GUIDANCE_QUOTE = (
    "For the third quarter of fiscal 2026, we are forecasting revenue of $3.9 billion, +/- $100 million."
)
BOOKINGS_QUOTE = (
    "We continued to see growing demand in the second quarter with record bookings across our B2B markets "
    "of Industrial, Automotive, and Communications"
)
DEMAND_OUTLOOK_QUOTE = (
    "These positive demand signals are reflected in our outlook for continued strong growth in the third quarter."
)


def run(output_path: str | Path = DEFAULT_OUTPUT) -> tuple[ForecastResult, ChallengeReport]:
    profile = load_company_profile(
        ROOT / "examples" / "adi_profile.json",
        repository_root=ROOT,
    )
    anchor = resolve_management_guidance(
        profile,
        signal_id="adi_revenue_guidance",
        source_id=SOURCE_ID,
        exact_quote=GUIDANCE_QUOTE,
        locator="Outlook for the Third Quarter of Fiscal Year 2026, first paragraph",
        low="3800",
        high="4000",
        units="USDm",
        period="FY2026Q3",
    )
    bookings = resolve_qualitative_modifier(
        profile,
        signal_id="adi_b2b_bookings",
        source_id=SOURCE_ID,
        exact_quote=BOOKINGS_QUOTE,
        locator="Management quotations, CFO statement",
        assessment="Bookings are constructive, but the release does not provide a calibrated revenue increment.",
        period="FY2026Q3",
    )
    demand_outlook = resolve_qualitative_modifier(
        profile,
        signal_id="adi_q3_demand_outlook",
        source_id=SOURCE_ID,
        exact_quote=DEMAND_OUTLOOK_QUOTE,
        locator="Management quotations, CFO statement",
        assessment="Management expects continued strong Q3 growth; retain as range context only.",
        period="FY2026Q3",
    )
    result = compile_forecast(
        profile,
        "ADI_REVENUE_FY2026Q3",
        [anchor, bookings, demand_outlook],
    )
    report = challenge_forecast(profile, result)
    write_run_receipt(profile, result, report, output_path)
    return result, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the source-backed ADI revenue example.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path for the deterministic provenance receipt.",
    )
    args = parser.parse_args()
    result, report = run(args.output)
    warning_count = sum(issue.severity == "warning" for issue in report.issues)
    print("ADI FY2026Q3 revenue")
    print(f"downside: {result.base_range.low} {result.units}")
    print(f"base:     {result.base_forecast} {result.units}")
    print(f"upside:   {result.base_range.high} {result.units}")
    print(f"formula:  {result.formula}")
    print(f"challenge: {'PASS' if report.passed else 'FAIL'} ({warning_count} warning(s))")
    print(f"receipt:  {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
