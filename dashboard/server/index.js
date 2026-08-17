import express from "express";
import cors from "cors";
import fs from "node:fs";
import { spawnSync } from "node:child_process";
import chokidar from "chokidar";
import path from "node:path";
import { DATA_DIR, COMPANIES_DIR } from "./paths.js";
import {
  listCompanies,
  getCompanyBundle,
  getForecast,
  getSignals,
  getSignal,
  getAgents,
  getAgent,
  getRuns,
  getRun,
  getRunLog,
  getProfile,
} from "./store.js";

const PORT = process.env.PORT || 8787;

// Auto-seed on first boot so `npm run server` alone produces a working demo.
if (!fs.existsSync(DATA_DIR)) {
  console.log("No data/ found — seeding…");
  spawnSync("node", [path.join(import.meta.dirname, "seed.js")], { stdio: "inherit" });
}

const app = express();
app.use(cors());
app.use(express.json());

const wrap = (fn) => (req, res) =>
  Promise.resolve(fn(req, res)).catch((err) => {
    console.error(err);
    res.status(500).json({ error: String(err.message || err) });
  });

// ---------- REST ----------

app.get("/api/health", (_req, res) => res.json({ ok: true }));

app.get("/api/companies", wrap(async (_req, res) => res.json(await listCompanies())));

app.get(
  "/api/companies/:slug",
  wrap(async (req, res) => {
    const bundle = await getCompanyBundle(req.params.slug);
    if (!bundle) return res.status(404).json({ error: "company not found" });
    res.json(bundle);
  })
);

app.get("/api/companies/:slug/forecast", wrap(async (req, res) => res.json(await getForecast(req.params.slug))));
app.get("/api/companies/:slug/profile", wrap(async (req, res) => res.json(await getProfile(req.params.slug))));
app.get("/api/companies/:slug/signals", wrap(async (req, res) => res.json(await getSignals(req.params.slug))));
app.get(
  "/api/companies/:slug/signals/:id",
  wrap(async (req, res) => {
    const s = await getSignal(req.params.slug, req.params.id);
    if (!s) return res.status(404).json({ error: "signal not found" });
    res.json(s);
  })
);
app.get("/api/companies/:slug/agents", wrap(async (req, res) => res.json(await getAgents(req.params.slug))));
app.get(
  "/api/companies/:slug/agents/:id",
  wrap(async (req, res) => {
    const a = await getAgent(req.params.slug, req.params.id);
    if (!a) return res.status(404).json({ error: "agent not found" });
    res.json(a);
  })
);
app.get("/api/companies/:slug/runs", wrap(async (req, res) => res.json(await getRuns(req.params.slug))));
app.get(
  "/api/companies/:slug/runs/:id",
  wrap(async (req, res) => {
    const run = await getRun(req.params.slug, req.params.id);
    if (!run) return res.status(404).json({ error: "run not found" });
    const log = await getRunLog(req.params.slug, req.params.id);
    res.json({ ...run, log });
  })
);

// ---------- SSE: "something changed, refetch" ----------
// One global stream. Each event carries the changed path (relative to data/) so
// clients can decide whether it affects their current view.

const clients = new Set();

app.get("/api/events", (req, res) => {
  res.set({
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache, no-transform",
    Connection: "keep-alive",
    "X-Accel-Buffering": "no",
  });
  res.flushHeaders?.();
  res.write(`event: hello\ndata: {"ok":true}\n\n`);
  clients.add(res);
  const ping = setInterval(() => res.write(`event: ping\ndata: {}\n\n`), 20000);
  req.on("close", () => {
    clearInterval(ping);
    clients.delete(res);
  });
});

function broadcast(relPath) {
  const parts = relPath.split(path.sep);
  // parts: companies/<slug>/...  -> extract slug + kind for client filtering
  const slug = parts[1] || null;
  const payload = JSON.stringify({ path: relPath.split(path.sep).join("/"), slug, at: Date.now() });
  for (const res of clients) res.write(`event: change\ndata: ${payload}\n\n`);
}

// Debounce a storm of writes into single change pings per path.
const pending = new Map();
function schedule(relPath) {
  if (pending.has(relPath)) return;
  pending.set(
    relPath,
    setTimeout(() => {
      pending.delete(relPath);
      broadcast(relPath);
    }, 120)
  );
}

const watcher = chokidar.watch(COMPANIES_DIR, {
  ignoreInitial: true,
  ignored: /\.tmp$/,
  awaitWriteFinish: { stabilityThreshold: 60, pollInterval: 20 },
});
watcher.on("all", (_event, file) => schedule(path.relative(DATA_DIR, file)));

app.listen(PORT, () => {
  console.log(`Centurion API on http://localhost:${PORT}`);
});
