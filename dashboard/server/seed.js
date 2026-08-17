import fs from "node:fs";
import fsp from "node:fs/promises";
import { DATA_DIR } from "./paths.js";
import {
  writeJsonSync,
  companyFile,
  forecastFile,
  signalFile,
  agentFile,
  runFile,
  runLogFile,
} from "./store.js";

// Seed data for the "Agents vs Wall Street" challenge: four real companies,
// each forecasting three reported figures for an upcoming period. We keep a
// single 0..1 "consensus" gauge per company that expresses how confident the
// agent fleet is that the company will meet/beat consensus on its headline
// figure. `p` on each signal is that signal's implied probability; the weighted
// blend drives the gauge. Signals cite real documents from the frozen corpus in
// challenge/offline-data/.

const NOW = Date.now();
const iso = (msAgo = 0) => new Date(NOW - msAgo).toISOString();
const MIN = 60_000;
const HOUR = 60 * MIN;

function history(end, points, stepMs, jitter = 0.03) {
  const out = [];
  let v = end - (Math.random() - 0.3) * 0.15;
  for (let i = points - 1; i >= 0; i--) {
    v = Math.min(0.95, Math.max(0.05, v + (Math.random() - 0.5) * jitter));
    out.push({ t: iso(i * stepMs), p: Number(v.toFixed(3)) });
  }
  out[out.length - 1] = { t: iso(0), p: end };
  return out;
}

function valueHistory(end, points, stepMs, spread) {
  const out = [];
  let v = end - spread * 0.6;
  for (let i = points - 1; i >= 0; i--) {
    v = v + (Math.random() - 0.4) * spread * 0.25;
    out.push({ t: iso(i * stepMs), value: Number(v.toFixed(1)) });
  }
  out[out.length - 1] = { t: iso(0), value: end };
  return out;
}

// Real, recent documents from the corpus, per company. Runs cite these so the
// live trace looks like an agent actually reading the offline data.
const CORPUS = {
  HD: [
    "home-depot/slides/2025-12-09__hd-us-20251209-slide__384215.md",
    "home-depot/call-transcripts/2025-08-19__hd-us-20250819-call-qna.md",
    "home-depot/filings/2025-08-19__hd-10q.md",
  ],
  ADI: [
    "analog-devices/slides/2025-11-12__adi-us-20251112-slide__968955.md",
    "analog-devices/call-transcripts/2025-08-20__adi-us-20250820-call-qna.md",
    "analog-devices/filings/2025-08-20__adi-10q.md",
  ],
  HAS: [
    "hays/slides/2026-02-27__has-ln-20260227-slide__643289.md",
    "hays/call-transcripts/2025-08-21__has-ln-20250821-call-pres.md",
    "hays/filings/2025-08-21__has-trading-update.md",
  ],
  DE: [
    "deere/slides/2026-05-26__de-us-20260526-slide__1053239.md",
    "deere/call-transcripts/2026-05-15__de-us-20260515-call-qna.md",
    "deere/filings/2026-05-15__de-10q.md",
  ],
};

const COMPANIES = [
  {
    id: "home-depot",
    name: "Home Depot",
    ticker: "HD",
    sector: "Home Improvement Retail",
    period: "FY2026 Q2",
    horizon: "FY2026Q2",
    description:
      "Big-box home-improvement retailer. Demand tracks housing turnover, renovation activity and the Pro customer.",
    question: "Will Home Depot meet or beat consensus on FY2026 Q2 net sales?",
    headlineMetric: "Net sales",
    metrics: [
      { label: "Net sales", units: "USDm", consensus: 45200 },
      { label: "Adjusted diluted EPS", units: "USD / share", consensus: 4.55 },
      { label: "Comparable sales, total company", units: "%", consensus: 1.2 },
    ],
    signals: [
      { id: "housing-turnover", title: "Housing Turnover", category: "Demand", unit: "idx", value: 96, stance: "bearish", weight: 0.22, p: 0.45, spread: 6, desc: "Existing-home-sales momentum index; big-ticket remodel demand tracks housing turnover.", src: "Filings, call transcripts" },
      { id: "pro-segment", title: "Pro Segment Strength", category: "Demand", unit: "%yoy", value: 4.1, stance: "bullish", weight: 0.24, p: 0.63, spread: 2, desc: "Commentary-derived Pro (contractor) revenue momentum — HD's structural growth lever.", src: "Call transcripts, slides" },
      { id: "ticket-traffic", title: "Ticket & Traffic", category: "Demand", unit: "%yoy", value: 0.6, stance: "neutral", weight: 0.18, p: 0.52, spread: 2, desc: "Average-ticket and transaction-count trend blended from prior-quarter disclosures.", src: "10-Q filing" },
      { id: "gross-margin", title: "Gross Margin Signal", category: "Margin", unit: "bps", value: 15, stance: "bullish", weight: 0.18, p: 0.58, spread: 20, desc: "Directional read on gross-margin from management commentary; supports the EPS figure.", src: "Call transcripts" },
      { id: "weather-storm", title: "Weather / Storm Demand", category: "External", unit: "idx", value: 58, stance: "bullish", weight: 0.18, p: 0.56, spread: 12, desc: "Seasonal + storm-recovery demand proxy affecting outdoor and repair categories.", src: "Slides, external" },
    ],
  },
  {
    id: "analog-devices",
    name: "Analog Devices",
    ticker: "ADI",
    sector: "Analog Semiconductors",
    period: "FY2026 Q3",
    horizon: "FY2026Q3",
    description:
      "High-performance analog & mixed-signal chipmaker. Cycle-sensitive across industrial, automotive and comms.",
    question: "Will ADI's FY2026 Q3 revenue land above the guidance midpoint?",
    headlineMetric: "Revenue",
    metrics: [
      { label: "Revenue", units: "USDm", consensus: 2760 },
      { label: "Adjusted diluted EPS", units: "USD / share", consensus: 1.98 },
      { label: "Adjusted gross margin", units: "%", consensus: 69.5 },
    ],
    signals: [
      { id: "book-to-bill", title: "Book-to-Bill", category: "Demand", unit: "ratio", value: 1.03, stance: "bullish", weight: 0.26, p: 0.66, spread: 0.08, desc: "Bookings vs billings; >1.0 signals a recovering order book — the cleanest revenue tell.", src: "Call transcripts" },
      { id: "industrial-recovery", title: "Industrial Recovery", category: "Demand", unit: "idx", value: 61, stance: "bullish", weight: 0.22, p: 0.62, spread: 8, desc: "Industrial end-market recovery proxy — ADI's largest and most cyclical segment.", src: "Slides, transcripts" },
      { id: "inventory-normal", title: "Channel Inventory", category: "Supply", unit: "wks", value: 7.4, stance: "bullish", weight: 0.2, p: 0.6, spread: 1, desc: "Distributor weeks-of-inventory; normalization unlocks shippable demand.", src: "10-Q filing" },
      { id: "auto-content", title: "Auto Content Growth", category: "Demand", unit: "%yoy", value: 6.8, stance: "bullish", weight: 0.16, p: 0.58, spread: 3, desc: "Automotive design-win content growth (BMS, connectivity) supporting the top line.", src: "Call transcripts" },
      { id: "gm-trajectory", title: "Gross-Margin Trajectory", category: "Margin", unit: "bps", value: -20, stance: "bearish", weight: 0.16, p: 0.47, spread: 25, desc: "Utilization-driven gross-margin direction; underloaded fabs pressure the margin figure.", src: "Filings, slides" },
    ],
  },
  {
    id: "hays",
    name: "Hays plc",
    ticker: "LSE:HAS",
    sector: "Recruitment / Staffing",
    period: "FY2026",
    horizon: "FY2026",
    description:
      "UK-listed specialist recruiter. Net fees track white-collar hiring across Germany, UK&I and Australia.",
    question: "Will Hays FY2026 net fees stabilise versus the prior year?",
    headlineMetric: "Net fees",
    metrics: [
      { label: "Net fees", units: "GBPm", consensus: 1015 },
      { label: "Pre-exceptional basic EPS", units: "GBp", consensus: 1.4 },
      { label: "Pre-exceptional operating profit", units: "GBPm", consensus: 60 },
    ],
    signals: [
      { id: "germany-market", title: "Germany Hiring", category: "Demand", unit: "idx", value: 88, stance: "bearish", weight: 0.26, p: 0.44, spread: 6, desc: "German white-collar hiring index — Hays' single largest net-fee market.", src: "Call transcripts, slides" },
      { id: "perm-temp-mix", title: "Perm / Temp Mix", category: "Demand", unit: "%perm", value: 41, stance: "bearish", weight: 0.2, p: 0.46, spread: 4, desc: "Permanent-placement share; perm fees are higher-margin but more cyclical.", src: "Trading update" },
      { id: "consultant-count", title: "Consultant Headcount", category: "Capacity", unit: "%yoy", value: -6, stance: "bearish", weight: 0.18, p: 0.45, spread: 3, desc: "Fee-earner headcount trend; capacity cuts cap near-term net-fee upside.", src: "Filings" },
      { id: "fee-per-head", title: "Fee per Consultant", category: "Productivity", unit: "idx", value: 103, stance: "bullish", weight: 0.18, p: 0.55, spread: 5, desc: "Productivity per fee-earner; a self-help lever supporting operating profit.", src: "Slides" },
      { id: "uk-market", title: "UK&I Market", category: "Demand", unit: "idx", value: 84, stance: "bearish", weight: 0.18, p: 0.43, spread: 6, desc: "UK & Ireland hiring conditions proxy; soft public + private demand.", src: "Call transcripts" },
    ],
  },
  {
    id: "deere",
    name: "Deere & Company",
    ticker: "DE",
    sector: "Agricultural Machinery",
    period: "FY2026 Q3",
    horizon: "FY2026Q3",
    description:
      "Farm & construction equipment maker. Ag cycle driven by farmer income, crop prices and dealer inventory.",
    question: "Will Deere's FY2026 Q3 Production & Precision Ag operating profit beat consensus?",
    headlineMetric: "Prod. & Precision Ag operating profit",
    metrics: [
      { label: "Worldwide net sales and revenues", units: "USDm", consensus: 11200 },
      { label: "Diluted EPS (GAAP)", units: "USD / share", consensus: 4.75 },
      { label: "Production & Precision Ag operating profit", units: "USDm", consensus: 1150 },
    ],
    signals: [
      { id: "farm-income", title: "Net Farm Income", category: "External", unit: "idx", value: 92, stance: "bearish", weight: 0.24, p: 0.45, spread: 5, desc: "USDA-style net-farm-income proxy; the primary driver of large-ag equipment demand.", src: "Slides, external" },
      { id: "dealer-inventory", title: "Dealer Inventory", category: "Supply", unit: "mo", value: 4.8, stance: "bullish", weight: 0.22, p: 0.6, spread: 1, desc: "Months of dealer inventory; lean channel supports production discipline and margin.", src: "Call transcripts" },
      { id: "order-backlog", title: "Order Backlog", category: "Demand", unit: "%full", value: 63, stance: "bullish", weight: 0.2, p: 0.58, spread: 8, desc: "Early-order-program fill rate for the coming season — a forward demand read.", src: "10-Q filing" },
      { id: "used-prices", title: "Used Equipment Prices", category: "Demand", unit: "%yoy", value: -8, stance: "bearish", weight: 0.16, p: 0.46, spread: 4, desc: "Used-combine/tractor price trend; weakness signals soft new-equipment appetite.", src: "External, slides" },
      { id: "precision-mix", title: "Precision Ag Mix", category: "Margin", unit: "%", value: 34, stance: "bullish", weight: 0.18, p: 0.62, spread: 3, desc: "High-margin precision-ag attach rate lifting the Production & Precision Ag profit line.", src: "Call transcripts, slides" },
    ],
  },
];

function agentsForCompany(c) {
  const AGENT_NAMES = {
    Demand: "Demand Signal Agent",
    Margin: "Margin Signal Agent",
    Supply: "Supply-Chain Agent",
    External: "Macro Signal Agent",
    Capacity: "Capacity Signal Agent",
    Productivity: "Productivity Agent",
  };
  const perSignal = c.signals.map((s, i) => ({
    id: `agent-${s.id}`,
    name: AGENT_NAMES[s.category] || `${s.category} Agent`,
    role: `Reads the corpus to score the "${s.title}" signal`,
    model: "claude-opus-4",
    status: i % 3 === 0 ? "running" : "idle",
    signalIds: [s.id],
    order: i,
    lastActiveAt: iso(Math.floor(Math.random() * 20 * MIN)),
  }));
  perSignal.push({
    id: "agent-consensus",
    name: "Consensus Agent",
    role: "Blends every signal into the forecast for the three reported figures",
    model: "claude-opus-4",
    status: "running",
    signalIds: c.signals.map((s) => s.id),
    order: perSignal.length,
    isConsensus: true,
    lastActiveAt: iso(2 * MIN),
  });
  return perSignal;
}

function consensusFrom(signals) {
  const totalW = signals.reduce((a, s) => a + s.weight, 0);
  const p = signals.reduce((a, s) => a + s.weight * s.p, 0) / totalW;
  const variance = signals.reduce((a, s) => a + s.weight * (s.p - p) ** 2, 0) / totalW;
  const dispersion = Math.sqrt(variance);
  const confidence = Math.max(0.35, Math.min(0.95, 1 - dispersion * 2.2));
  return { p: Number(p.toFixed(3)), confidence: Number(confidence.toFixed(3)) };
}

function seedCompany(c) {
  const slug = c.id;

  writeJsonSync(companyFile(slug), {
    id: c.id,
    name: c.name,
    ticker: c.ticker,
    sector: c.sector,
    description: c.description,
    question: c.question,
    period: c.period,
    horizon: c.horizon,
    headlineMetric: c.headlineMetric,
    metrics: c.metrics,
    corpusDocs: CORPUS[c.ticker.replace("LSE:", "")] || [],
    createdAt: iso(30 * 24 * HOUR),
  });

  for (const s of c.signals) {
    writeJsonSync(signalFile(slug, s.id), {
      id: s.id,
      title: s.title,
      category: s.category,
      description: s.desc,
      unit: s.unit,
      value: s.value,
      prevValue: s.value,
      p: s.p,
      stance: s.stance,
      confidence: Number((0.55 + Math.random() * 0.3).toFixed(3)),
      weight: s.weight,
      source: s.src,
      agentIds: [`agent-${s.id}`],
      updatedAt: iso(Math.floor(Math.random() * 15 * MIN)),
      history: history(s.p, 40, 15 * MIN),
      valueHistory: valueHistory(s.value, 40, 15 * MIN, s.spread),
    });
  }

  const { p, confidence } = consensusFrom(c.signals);
  writeJsonSync(forecastFile(slug), {
    consensus: p,
    confidence,
    direction: "flat",
    updatedAt: iso(2 * MIN),
    headlineMetric: c.headlineMetric,
    rationale:
      `Probability that ${c.name} meets or beats consensus on ${c.headlineMetric} (${c.period}). ` +
      "Weighted blend of all active signals; demand signals carry the most weight, margin and macro apply cross-pressure.",
    history: history(p, 60, 12 * MIN, 0.02),
    contributions: c.signals.map((s) => ({
      signalId: s.id,
      title: s.title,
      weight: s.weight,
      p: s.p,
    })),
  });

  const agents = agentsForCompany(c);
  for (const a of agents) writeJsonSync(agentFile(slug, a.id), a);

  const docs = CORPUS[c.ticker.replace("LSE:", "")] || [];
  let runIdx = 0;
  for (const a of agents.filter((x) => !x.isConsensus).slice(0, 3)) {
    const sig = c.signals.find((s) => s.id === a.signalIds[0]);
    const rid = `run-${slug}-${String(++runIdx).padStart(3, "0")}`;
    const startedAgo = (10 + runIdx * 4) * MIN;
    writeJsonSync(runFile(slug, rid), {
      id: rid,
      agentId: a.id,
      agentName: a.name,
      signalId: sig.id,
      signalTitle: sig.title,
      status: "completed",
      trigger: "scheduled",
      startedAt: iso(startedAgo),
      endedAt: iso(startedAgo - 45 * 1000),
      summary: `Scored ${sig.title}: ${sig.value}${sig.unit ? " " + sig.unit : ""} (implied ${(sig.p * 100).toFixed(0)}%).`,
      result: { value: sig.value, p: sig.p, stance: sig.stance, confidence: 0.66 },
    });
    const log = seedLog(a, sig, startedAgo, docs);
    fs.writeFileSync(runLogFile(slug, rid), log.map((l) => JSON.stringify(l)).join("\n") + "\n");
  }

  return slug;
}

function seedLog(agent, sig, startedAgo, docs) {
  const base = NOW - startedAgo;
  const t = (i) => new Date(base + i * 1500).toISOString();
  const doc = docs[0] || "challenge/offline-data/…";
  return [
    { t: t(0), level: "info", phase: "start", message: `Run started for signal "${sig.title}".` },
    { t: t(1), level: "info", phase: "plan", message: `Sources to read: ${sig.src}.` },
    { t: t(2), level: "tool", phase: "read", message: `tool_call read_corpus`, data: { doc } },
    { t: t(3), level: "info", phase: "read", message: `Read ${doc.split("/").pop()} + 2 related documents.` },
    { t: t(4), level: "info", phase: "reason", message: `Extracting the relevant figures and comparing against the prior period.` },
    { t: t(5), level: "info", phase: "reason", message: `Read looks ${sig.stance} for the forecast question.` },
    { t: t(6), level: "result", phase: "emit", message: `Emitting ${sig.title} = ${sig.value}${sig.unit ? " " + sig.unit : ""}, implied p=${sig.p}.`, data: { value: sig.value, p: sig.p } },
    { t: t(7), level: "info", phase: "done", message: `Signal file updated. Run complete.` },
  ];
}

async function main() {
  const force = process.argv.includes("--force");
  if (fs.existsSync(DATA_DIR)) {
    if (!force) {
      console.log("data/ already exists — skipping seed (use `npm run reset` to overwrite).");
      return;
    }
    await fsp.rm(DATA_DIR, { recursive: true, force: true });
  }
  fs.mkdirSync(DATA_DIR, { recursive: true });
  const slugs = COMPANIES.map(seedCompany);
  console.log(`Seeded ${slugs.length} companies: ${slugs.join(", ")}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
