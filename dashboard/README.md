# Centurion — Forecasting-Agent Dashboard

The live control room for the **Agents vs Wall Street** challenge. It sits alongside
the starter repo and visualises a fleet of forecasting agents working the four
challenge companies — **Home Depot (HD), Analog Devices (ADI), Hays (HAS), Deere (DE)**.

Each agent reads the frozen corpus in [`../challenge/offline-data/`](../challenge/offline-data),
scores a signal, and a consensus agent blends the signals into a single 0–100%
confidence that the company will meet/beat consensus on its headline reported figure.
Each company card also shows the three target figures it forecasts for the period.

Everything is **file-based**. No database. The `data/` directory _is_ the state:

Everything is **file-based**. No database. The `data/` directory _is_ the state:

```
data/companies/<slug>/
  company.json          # name, ticker, period, the 3 target metrics, cited corpus docs
  forecast.json         # consensus probability, confidence, direction, history[]
  signals/<id>.json     # one signal: value, implied p, stance, weight, history[]
  agents/<id>.json      # one agent: status, role, which signal(s) it owns
  runs/<id>.json        # run metadata: status, result, summary
  runs/<id>.log.jsonl   # append-only live trace (tool calls + reasoning + emit)
```

When the real LLM agents land, they just **write these same files** and the UI keeps
working unchanged. The included simulator stands in for them for the demo.

## Run it

```bash
npm run setup     # installs deps (root + web) and seeds data/
npm run dev       # starts API + simulator + web, all together
```

Then open **http://localhost:5173**.

- `npm run reset` — wipe and re-seed `data/`
- `npm run server` / `npm run sim` / `npm run web` — run any piece on its own

## Architecture

- **`server/index.js`** — Express API on `:8787`. Serves the files as JSON and exposes
  `GET /api/events`, a Server-Sent-Events stream. It watches `data/` with chokidar and
  emits a "something changed" ping (with the changed path) on every write.
- **`server/simulator.js`** — stands in for the real agents. On a timer it starts runs,
  streams log lines, moves signal probabilities, and recomputes the consensus forecast.
  Delete it the day real agents write the files.
- **`web/`** — Vite + React. A single `EventSource` drives `useLive()`, which refetches
  the relevant endpoint whenever a matching change event arrives, so the whole UI stays
  live without polling.

## The UI

1. **Workspaces** — one card per company: consensus %, trend, live agent count.
2. **Company** — consensus gauge + trend, the agent fleet (with live status), every
   signal, and recent runs.
3. **Signal** — what it measures, metric + implied-probability history, agents on it.
4. **Run** — a live-streaming console of the agent's trace, plus its structured result.

## Wiring in real agents

Point your agents' output at `data/companies/<slug>/…` using the same shapes (see
`server/store.js` for the reads and `server/seed.js` for the shapes). Append trace lines
to `runs/<id>.log.jsonl` as `{t, level, phase, message, data?}`. The file watcher turns
every write into a live UI update automatically.
