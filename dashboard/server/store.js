import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import {
  COMPANIES_DIR,
  companyDir,
  companyFile,
  forecastFile,
  signalsDir,
  agentsDir,
  runsDir,
  signalFile,
  agentFile,
  runFile,
  runLogFile,
  profileFile,
} from "./paths.js";

// ---------- low-level helpers ----------

export async function readJson(file, fallback = null) {
  try {
    const raw = await fsp.readFile(file, "utf8");
    return JSON.parse(raw);
  } catch (err) {
    if (err.code === "ENOENT") return fallback;
    // A concurrent write can momentarily produce an unparseable file; treat as fallback.
    if (err instanceof SyntaxError) return fallback;
    throw err;
  }
}

// Atomic-ish write: write to a temp file then rename so readers never see a
// half-written JSON document.
export async function writeJson(file, data) {
  await fsp.mkdir(path.dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.tmp`;
  await fsp.writeFile(tmp, JSON.stringify(data, null, 2));
  await fsp.rename(tmp, file);
}

export function writeJsonSync(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2));
  fs.renameSync(tmp, file);
}

export async function appendLog(file, entry) {
  await fsp.mkdir(path.dirname(file), { recursive: true });
  await fsp.appendFile(file, JSON.stringify(entry) + "\n");
}

export async function readLog(file) {
  try {
    const raw = await fsp.readFile(file, "utf8");
    return raw
      .split("\n")
      .filter(Boolean)
      .map((line) => {
        try {
          return JSON.parse(line);
        } catch {
          return null;
        }
      })
      .filter(Boolean);
  } catch (err) {
    if (err.code === "ENOENT") return [];
    throw err;
  }
}

async function listJson(dir) {
  try {
    const names = await fsp.readdir(dir);
    return names.filter((n) => n.endsWith(".json")).map((n) => n.replace(/\.json$/, ""));
  } catch (err) {
    if (err.code === "ENOENT") return [];
    throw err;
  }
}

// ---------- domain reads ----------

export async function listCompanySlugs() {
  try {
    const entries = await fsp.readdir(COMPANIES_DIR, { withFileTypes: true });
    return entries.filter((e) => e.isDirectory()).map((e) => e.name);
  } catch (err) {
    if (err.code === "ENOENT") return [];
    throw err;
  }
}

export const getCompany = (slug) => readJson(companyFile(slug));
export const getForecast = (slug) => readJson(forecastFile(slug));
// Source-backed research profile (cited claims, metrics, signal map). Optional.
export const getProfile = (slug) => readJson(profileFile(slug));

export async function getSignals(slug) {
  const ids = await listJson(signalsDir(slug));
  const signals = await Promise.all(ids.map((id) => readJson(signalFile(slug, id))));
  return signals.filter(Boolean).sort((a, b) => (b.weight ?? 0) - (a.weight ?? 0));
}

export const getSignal = (slug, id) => readJson(signalFile(slug, id));

export async function getAgents(slug) {
  const ids = await listJson(agentsDir(slug));
  const agents = await Promise.all(ids.map((id) => readJson(agentFile(slug, id))));
  return agents.filter(Boolean).sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
}

export const getAgent = (slug, id) => readJson(agentFile(slug, id));

export async function getRuns(slug) {
  const ids = await listJson(runsDir(slug));
  const runs = await Promise.all(ids.map((id) => readJson(runFile(slug, id))));
  return runs
    .filter(Boolean)
    .sort((a, b) => new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime());
}

export const getRun = (slug, id) => readJson(runFile(slug, id));
export const getRunLog = (slug, id) => readLog(runLogFile(slug, id));

// A single rolled-up view of a company, convenient for the dashboard.
export async function getCompanyBundle(slug) {
  const company = await getCompany(slug);
  if (!company) return null;
  const [forecast, signals, agents, runs, profile] = await Promise.all([
    getForecast(slug),
    getSignals(slug),
    getAgents(slug),
    getRuns(slug),
    getProfile(slug),
  ]);
  return { company, forecast, signals, agents, runs, profile };
}

export async function listCompanies() {
  const slugs = await listCompanySlugs();
  const bundles = await Promise.all(
    slugs.map(async (slug) => {
      const [company, forecast, signals, agents, runs] = await Promise.all([
        getCompany(slug),
        getForecast(slug),
        getSignals(slug),
        getAgents(slug),
        getRuns(slug),
      ]);
      if (!company) return null;
      return {
        ...company,
        forecast,
        signalCount: signals.length,
        agentCount: agents.length,
        runningAgents: agents.filter((a) => a.status === "running").length,
        activeRuns: runs.filter((r) => r.status === "running").length,
      };
    })
  );
  return bundles.filter(Boolean);
}

export {
  companyDir,
  companyFile,
  forecastFile,
  signalsDir,
  agentsDir,
  runsDir,
  signalFile,
  agentFile,
  runFile,
  runLogFile,
  profileFile,
};
