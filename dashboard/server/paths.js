import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const ROOT = path.resolve(__dirname, "..");
export const DATA_DIR = path.join(ROOT, "data");
export const COMPANIES_DIR = path.join(DATA_DIR, "companies");
// Source-backed company profiles live here (committed, independent of data/).
export const PROFILES_DIR = path.join(ROOT, "server", "profiles");
export const profileFile = (slug) => path.join(PROFILES_DIR, `${slug}.json`);

export const companyDir = (slug) => path.join(COMPANIES_DIR, slug);
export const companyFile = (slug) => path.join(companyDir(slug), "company.json");
export const forecastFile = (slug) => path.join(companyDir(slug), "forecast.json");
export const signalsDir = (slug) => path.join(companyDir(slug), "signals");
export const agentsDir = (slug) => path.join(companyDir(slug), "agents");
export const runsDir = (slug) => path.join(companyDir(slug), "runs");
export const signalFile = (slug, id) => path.join(signalsDir(slug), `${id}.json`);
export const agentFile = (slug, id) => path.join(agentsDir(slug), `${id}.json`);
export const runFile = (slug, id) => path.join(runsDir(slug), `${id}.json`);
export const runLogFile = (slug, id) => path.join(runsDir(slug), `${id}.log.jsonl`);
