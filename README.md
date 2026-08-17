# Agents vs Wall Street

Agents vs Wall Street is a one-day hackathon presented by Primer, OpenStocks, AI Tinkerers and OpenAI. Around 50 people will build 20–25 forecasting agents, working alone or in teams of up to four.

The challenge covers four companies: Home Depot, Analog Devices, Hays plc and Deere & Company. Your agent forecasts three reported figures for each.

The repository includes a frozen historical corpus of 1,139 filings, call-transcript sections and slide documents for the four known companies. Start at [challenge/offline-data/INDEX.md](challenge/offline-data/INDEX.md) or search the Markdown files directly.

Your agent should be able to do the research, make the financial judgements and produce completed OpenStocks workbooks with as little manual help as possible.

Install both dependency sets after cloning:

```bash
npm install
python3 -m pip install -r requirements.txt
```

## What the day is for

1. **Build something real.** Create a repeatable agent that researches companies, makes financial judgements and produces completed forecast workbooks.
2. **Show what is possible.** Help us learn what works and show how powerful this technology can be when it is assembled properly.

OpenStocks offers ongoing $100 prizes for individual earnings events after the hackathon, so build an agent you can use again.

## The challenge at a glance

- Doors open at 10:00 on Sunday 16 August 2026 at Ground Floor, 33 Johns Mews, London WC1N 2QL. The competition briefing begins at 10:30 and building starts at 11:15.
- Teams can have one to four people.
- Each individual or team enters one agent.
- Each team receives $50 of Codex credit, kindly provided by OpenAI.
- Competition-specific work must be built during the event; evidence of a pre-made entry means disqualification from all prizes.
- Your agent must forecast three figures for each of four companies.
- The final run starts at 17:15 and must finish before the 18:00 deadline.
- OpenStocks opens for challenge uploads at 17:30.
- Your final command must produce all four `.xlsx` workbooks.
- Upload each workbook manually to the matching company Forecast Model on [openstocks.com](https://openstocks.com).
- If you upload more than once, the last valid workbook uploaded for each company before 18:00 is your final forecast.

## What you need to submit

1. A completed private `entry.json` with the agent name, every team member and email address, technical setup and final-run details. Upload it through openstocks.com/hackathon; no account is needed for this private team-entry form.
2. Your code repository and the commit used for the final run.
3. The completed self-contained `architecture/index.html`, uploaded through the same private form. You do not need to host it anywhere.
4. A timestamped log from a clear run of the system.
5. Four completed company workbooks in `submission/`.

Complete [ENTRY.md](ENTRY.md), then read [SUBMISSION.md](SUBMISSION.md) before the final run. The full event rules are in [RULES.md](RULES.md), the day is set out in [SCHEDULE.md](SCHEDULE.md), and the judging process is explained in [JUDGING.md](JUDGING.md).

By submitting the private team entry, your team accepts the hackathon and prize rules in [RULES.md](RULES.md).

## Expected final output

Your final command can use any language or framework, and it can run the four companies one after another or at the same time. It must finish by creating these exact files:

```text
submission/
├── ADI-FY2026Q3.xlsx
├── DE-FY2026Q3.xlsx
├── HAS-FY2026.xlsx
└── HD-FY2026Q2.xlsx
```

Start from the supplied files in `challenge/templates/`. Do not rename the `Summary` sheet, metric labels, units or fiscal-period column.

Run `npm install` and `npm run setup:entry` once. Complete the private `entry.json` and `architecture/index.html`, then use `npm run check:submission` before uploading. It checks the entry record, architecture file and four workbooks. It does not judge whether the forecasts are good.

## Optional document-search helper

[`starter/search.py`](starter/search.py) is a small, dependency-free example of searching the supplied Markdown corpus and producing a cited research note. It does not make forecasts or edit a workbook.

```bash
python3 starter/search.py --company HD
less research/HD.md
```

Use `HD`, `ADI`, `HAS` or `DE` for the four challenge companies. The output contains search leads rather than verified financial history, so check each figure in its cited document. Read [starter/README.md](starter/README.md) for narrower searches and testing instructions.

## Evidence-to-forecast example

The first compiler slice turns a source-backed company profile and metric-specific signal map into a deterministic forecast receipt. It verifies the frozen document hash and exact quotation before any observation can affect a number, keeps qualitative modifiers out of arithmetic and rejects correlated quantitative drivers.

```bash
python3 example.py
```

The example uses ADI's 20 May 2026 SEC-filed earnings release and writes `build/example-adi-revenue-receipt.json`. The receipt preserves the SEC URL, local corpus path, SHA-256, exact quotation, signal decision and Decimal formula. Read [ARCHITECTURE.md](ARCHITECTURE.md) for the Red/Blue worker workflow and limits.

Run the compiler tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Tavily company and signal research

Copy `.env.example` to the ignored `.env` file and set both `TAVILY_API_KEY` and
`OPENAI_API_KEY`. Secrets are read from the process or `.env`; they are never
written to requests, artifacts or logs.

Run the complete four-company workflow, with a 45-minute live-research budget:

```bash
python3 -m pipeline.run --max-minutes 45
```

The four research lanes run concurrently. Each lane combines current official web
research with the supplied offline corpus, generates a source-bound proposal for
exactly the three challenge metrics, performs deterministic quote/hash/cutoff
checks, and sends it to an independent no-web review before forecasting. A failed
company or review stops the final submission rather than silently using a guess.

Research all four company profiles concurrently:

```bash
npm run research:profiles
```

This writes timestamped candidate bundles under ignored `research/`. Each selected page is frozen locally with its canonical URL, publication time, Tavily request IDs and SHA-256. Post-cutoff or undated evidence cannot drive a forecast.

After creating validated `signal_maps/<company>.json` files with three to seven approved signals and one anchor per metric, run:

```bash
npm run research:signals
```

The second planner searches only evidence declared by approved signals. `signal_agent.research_validation` validates profile coverage, exact quotations, signal formulas, units, accounting basis, decimal-string observations, audit metadata and the independent review before emitting `forecast_input.v2`. The repository skill at `.agents/skills/researching-company-signals/` documents the operator workflow.

## Forecast handoff and final stages

For manual debugging, an operator can still build a self-contained compiler handoff:

```bash
python3 -m signal_agent.handoff_cli \
  --proposal research/ADI-proposal.json \
  --candidates research/ADI/signal-candidates.json \
  --audit research/ADI-audit.json \
  --review research/ADI-review.json \
  --source-root research/ADI \
  --output forecast_inputs/ADI.json
```

To rerun only the deterministic stages from existing validated handoffs:

```bash
python3 -m pipeline.run --skip-research
```

This compiles exactly three metrics per company, retains receipts and rejected-signal
reasons, aggregates `evaluation/forecasts.json`, validates all twelve figures and
writes the four supplied workbook templates.

## Repository map

```text
challenge/                 Companies, metrics, workbooks and historical documents
architecture/index.html    Template for the required architecture explanation
entry.template.json        Template for private team and agent details
submission/                Put the four completed workbooks here
logs/                      Save the final clear-run log here
scripts/                   Local entry and workbook checks
starter/                   Optional historical-document search helper
```

## Licence

The original code and documentation in this repository are available under the [MIT License](LICENSE). The historical company documents under `challenge/offline-data/` are excluded; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
