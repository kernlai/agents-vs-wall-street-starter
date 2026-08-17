import {
  listCompanySlugs,
  getCompany,
  getAgents,
  getSignals,
  getSignal,
  getForecast,
  getRuns,
  getRun,
  readJson,
  writeJson,
  appendLog,
  signalFile,
  agentFile,
  forecastFile,
  runFile,
  runLogFile,
} from "./store.js";

// The simulator stands in for real LLM agents. It mutates the same files those
// agents will write, so the UI needs no changes when the real thing ships.

const TICK_MS = 1800;
const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
const now = () => new Date().toISOString();
let runCounter = Date.now() % 100000;

// A scripted trace per agent run — mimics an LLM agent's tool calls + reasoning.
function buildScript(agent, signal, docs = []) {
  if (agent.isConsensus) {
    return [
      { phase: "start", level: "info", msg: () => `Consensus run started. Reading all signal files.` },
      { phase: "read", level: "tool", msg: (ctx) => `tool_call read_signals`, data: (ctx) => ({ count: ctx.signals.length }) },
      { phase: "read", level: "info", msg: (ctx) => `Loaded ${ctx.signals.length} signals (${ctx.signals.filter((s) => s.stance === "bullish").length} bullish / ${ctx.signals.filter((s) => s.stance === "bearish").length} bearish).` },
      { phase: "reason", level: "info", msg: (ctx) => `Top driver: ${ctx.top.title} (weight ${(ctx.top.weight * 100).toFixed(0)}%, implied ${(ctx.top.p * 100).toFixed(0)}%).` },
      { phase: "reason", level: "info", msg: (ctx) => `Signal dispersion ${(ctx.dispersion * 100).toFixed(1)}% → confidence ${(ctx.confidence * 100).toFixed(0)}%.` },
      { phase: "emit", level: "result", msg: (ctx) => `Consensus updated: ${(ctx.p * 100).toFixed(1)}% (${ctx.deltaStr}).`, data: (ctx) => ({ consensus: ctx.p, confidence: ctx.confidence }) },
      { phase: "done", level: "info", msg: () => `Forecast file written. Run complete.` },
    ];
  }
  const src = (signal.source || "corpus").split(",").map((s) => s.trim());
  const doc = docs.length ? pick(docs) : null;
  return [
    { phase: "start", level: "info", msg: () => `Run started for signal "${signal.title}".` },
    { phase: "plan", level: "info", msg: () => `Sources to read: ${src.join(", ")}.` },
    { phase: "read", level: "tool", msg: () => `tool_call read_corpus`, data: () => (doc ? { doc } : { source: pick(src) }) },
    { phase: "read", level: "info", msg: () => doc ? `Read ${doc.split("/").pop()} + ${1 + Math.floor(Math.random() * 3)} related documents.` : `Read ${1 + Math.floor(Math.random() * 4)} documents.` },
    { phase: "reason", level: "info", msg: () => pick([
      `Extracting reported figures and comparing against the prior period.`,
      `Cross-checking management commentary against the filed numbers.`,
      `Reconciling segment detail with the headline figure.`,
    ]) },
    { phase: "reason", level: "info", msg: (ctx) => `Read looks ${ctx.stance} on the forecast question (Δp ${ctx.dpStr}).` },
    { phase: "emit", level: "result", msg: (ctx) => `Emitting ${signal.title} = ${ctx.value}${signal.unit ? " " + signal.unit : ""}, implied p=${ctx.p}.`, data: (ctx) => ({ value: ctx.value, p: ctx.p }) },
    { phase: "done", level: "info", msg: () => `Signal file updated. Run complete.` },
  ];
}

function consensusFrom(signals) {
  const totalW = signals.reduce((a, s) => a + (s.weight || 0), 0) || 1;
  const p = signals.reduce((a, s) => a + (s.weight || 0) * (s.p ?? 0.5), 0) / totalW;
  const variance = signals.reduce((a, s) => a + (s.weight || 0) * ((s.p ?? 0.5) - p) ** 2, 0) / totalW;
  const dispersion = Math.sqrt(variance);
  const confidence = clamp(1 - dispersion * 2.2, 0.35, 0.95);
  return { p, confidence, dispersion };
}

async function startRun(slug, agent) {
  const signal = agent.signalIds?.[0] ? await getSignal(slug, agent.signalIds[0]) : null;
  const id = `run-${slug}-live-${++runCounter}`;
  const run = {
    id,
    agentId: agent.id,
    agentName: agent.name,
    signalId: agent.isConsensus ? null : signal?.id ?? null,
    signalTitle: agent.isConsensus ? "All signals" : signal?.title ?? null,
    status: "running",
    trigger: "scheduled",
    startedAt: now(),
    endedAt: null,
    summary: null,
    result: null,
    _step: 0,
    _script: null, // filled lazily; script fns need live ctx
  };
  await writeJson(runFile(slug, id), stripInternal(run));
  await appendLog(runLogFile(slug, id), { t: now(), level: "info", phase: "queue", message: `${agent.name} picked up by scheduler.` });

  agent.status = "running";
  agent.currentRunId = id;
  agent.lastActiveAt = now();
  await writeJson(agentFile(slug, agent.id), agent);
  return id;
}

function stripInternal(run) {
  const { _step, _script, ...rest } = run;
  return rest;
}

// Advance one in-flight run by a single script step.
async function advanceRun(slug, agent, runId) {
  const run = await getRun(slug, runId);
  if (!run || run.status !== "running") return true; // treat as finished

  const signal = run.signalId ? await getSignal(slug, run.signalId) : null;
  const signals = await getSignals(slug);
  const company = await getCompany(slug);
  const script = buildScript(agent, signal || {}, company?.corpusDocs || []);

  // Step index is tracked directly on the run file.
  const curStep = run.step ?? 0;
  const item = script[curStep];
  if (!item) {
    return finishRun(slug, agent, run, signal, signals);
  }

  // Build ctx for this step.
  const ctx = buildCtx(agent, signal, signals);
  await appendLog(runLogFile(slug, runId), {
    t: now(),
    level: item.level,
    phase: item.phase,
    message: item.msg(ctx),
    ...(item.data ? { data: item.data(ctx) } : {}),
  });

  run.step = curStep + 1;
  await writeJson(runFile(slug, runId), run);

  if (run.step >= script.length) {
    return finishRun(slug, agent, run, ctx.signal || signal, signals, ctx);
  }
  return false;
}

function buildCtx(agent, signal, signals) {
  if (agent.isConsensus) {
    const { p, confidence, dispersion } = consensusFrom(signals);
    const top = [...signals].sort((a, b) => (b.weight || 0) - (a.weight || 0))[0] || {};
    return { signals, p, confidence, dispersion, top, deltaStr: "recomputed", value: null };
  }
  // Random-walk the signal's implied probability, biased by its stance.
  const bias = signal.stance === "bullish" ? 0.012 : signal.stance === "bearish" ? -0.012 : 0;
  const dp = (Math.random() - 0.5) * 0.05 + bias;
  const newP = clamp((signal.p ?? 0.5) + dp, 0.05, 0.95);
  const stepVal = (Math.abs(dp) * 40 + Math.random() * 3);
  const dir = dp >= 0 ? 1 : -1;
  const newVal = Number(((signal.value ?? 0) + dir * stepVal).toFixed(1));
  return {
    signal: { ...signal, _newP: Number(newP.toFixed(3)), _newVal: newVal },
    value: newVal,
    p: Number(newP.toFixed(3)),
    stance: dp > 0.005 ? "bullish" : dp < -0.005 ? "bearish" : "neutral",
    dpStr: (dp >= 0 ? "+" : "") + dp.toFixed(3),
  };
}

async function finishRun(slug, agent, run, signal, signals, ctx) {
  ctx = ctx || buildCtx(agent, signal, signals);
  run.status = "completed";
  run.endedAt = now();

  if (agent.isConsensus) {
    await recomputeForecast(slug, signals);
    const { p, confidence } = consensusFrom(signals);
    run.summary = `Consensus at ${(p * 100).toFixed(1)}%, confidence ${(confidence * 100).toFixed(0)}%.`;
    run.result = { consensus: Number(p.toFixed(3)), confidence: Number(confidence.toFixed(3)) };
  } else if (signal) {
    const newP = ctx.p;
    const newVal = ctx.value;
    signal.prevValue = signal.value;
    signal.value = newVal;
    signal.p = newP;
    signal.stance = newP > 0.55 ? "bullish" : newP < 0.45 ? "bearish" : "neutral";
    signal.confidence = Number(clamp((signal.confidence ?? 0.6) + (Math.random() - 0.5) * 0.05, 0.4, 0.95).toFixed(3));
    signal.updatedAt = now();
    signal.history = [...(signal.history || []), { t: now(), p: newP }].slice(-80);
    signal.valueHistory = [...(signal.valueHistory || []), { t: now(), value: newVal }].slice(-80);
    await writeJson(signalFile(slug, signal.id), signal);
    run.summary = `Refreshed ${signal.title}: ${newVal}${signal.unit ? " " + signal.unit : ""} (implied ${(newP * 100).toFixed(0)}%).`;
    run.result = { value: newVal, p: newP, stance: signal.stance, confidence: signal.confidence };
    // Recompute forecast after a signal moves so the headline number reacts.
    await recomputeForecast(slug, await getSignals(slug));
  }

  await writeJson(runFile(slug, run.id), stripInternal(run));

  agent.status = "idle";
  agent.currentRunId = null;
  agent.lastActiveAt = now();
  // Stagger the next kick-off so agents don't all fire in lockstep.
  agent._nextAt = Date.now() + 4000 + Math.floor(Math.random() * 12000);
  await writeJson(agentFile(slug, agent.id), agent);
  return true;
}

async function recomputeForecast(slug, signals) {
  const forecast = (await getForecast(slug)) || {};
  const { p, confidence } = consensusFrom(signals);
  const prev = forecast.consensus ?? p;
  const dp = p - prev;
  forecast.consensus = Number(p.toFixed(3));
  forecast.confidence = Number(confidence.toFixed(3));
  forecast.direction = dp > 0.002 ? "up" : dp < -0.002 ? "down" : "flat";
  forecast.updatedAt = now();
  forecast.history = [...(forecast.history || []), { t: now(), p: Number(p.toFixed(3)) }].slice(-120);
  forecast.contributions = signals.map((s) => ({
    signalId: s.id,
    title: s.title,
    weight: s.weight,
    p: s.p,
  }));
  await writeJson(forecastFile(slug), forecast);
}

async function tickCompany(slug) {
  const agents = await getAgents(slug);
  for (const agent of agents) {
    if (agent.status === "running" && agent.currentRunId) {
      await advanceRun(slug, agent, agent.currentRunId);
    } else if (agent.status !== "running") {
      const nextAt = agent._nextAt ?? 0;
      // Kick off a new run when it's time, or ~15% chance if never scheduled.
      if (Date.now() >= nextAt && (agent._nextAt !== undefined || Math.random() < 0.15)) {
        await startRun(slug, agent);
      }
    }
  }
}

async function loop() {
  try {
    const slugs = await listCompanySlugs();
    for (const slug of slugs) await tickCompany(slug);
  } catch (err) {
    console.error("[sim] tick error:", err.message);
  }
  setTimeout(loop, TICK_MS);
}

console.log("Centurion simulator running — agents will start producing live activity.");
loop();
