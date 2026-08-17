import React, { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { Logo } from "../ui.jsx";
import { cn } from "@/lib/utils";

/* Reveal-on-scroll wrapper */
function Reveal({ as: Tag = "div", className = "", delay = 0, children }) {
  const ref = useRef(null);
  const [shown, setShown] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([e]) => { if (e.isIntersecting) { setShown(true); io.disconnect(); } },
      { threshold: 0.16 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return (
    <Tag ref={ref} style={{ transitionDelay: `${delay}ms` }}
      className={cn("transition-all duration-700 ease-[cubic-bezier(.2,.7,.2,1)]",
        shown ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4", className)}>
      {children}
    </Tag>
  );
}

const WORKERS = [
  { x: 52, slug: "home-depot", name: "Home Depot", tk: "HD · comparable sales" },
  { x: 292, slug: "analog-devices", name: "Analog Devices", tk: "ADI · revenue" },
  { x: 532, slug: "hays", name: "Hays plc", tk: "HAS · net fees" },
  { x: 772, slug: "deere", name: "Deere & Co.", tk: "DE · op. profit" },
];
const LOGO_SRC = {
  "home-depot": "/logos/home-depot.png",
  "analog-devices": "/logos/analog-devices.svg",
  hays: "/logos/hays.png",
  deere: "/logos/deere.webp",
};

const STAGES = [
  ["1", "Profile", "Source-backed profile: business model, fiscal calendar, segments, metric definitions."],
  ["2", "Signal map", "Name the 3–7 material signals that could move each metric, each with a role and direction."],
  ["3", "Resolve", "Reusable resolvers collect evidence for approved signals and return typed, cited observations."],
  ["4", "Combine", "Anchor + approved driver adjustments = base forecast in Decimal. Correlated drivers are dropped, so nothing is double-counted."],
  ["5", "Scenarios", "Low / base / high. Triggers stay out of the base unless their condition actually occurs."],
  ["6", "Challenge", "A challenger reads the reasoning behind each estimate for bias, then code checks numbers, units and format."],
];

// TODO: replace with the real multi-run backtest figures.
const RESULT = { runs: "N", single: "—%", consensus: "X%" };

const ROLES = [
  ["constraint", "Enforced", "#6b7280", "Accounting identities the forecast must satisfy — never weighted.", "EPS must reconcile with profit, tax and diluted shares."],
  ["anchor", "Starting range", "var(--primary)", "A direct, defensible estimate that forms the forecast's starting point.", "Management's stated Q3 revenue guidance range."],
  ["driver", "Moves the number", "#4f7a8a", "A quantified effect applied through an explicit formula.", "revenue × volume change × price/mix change."],
  ["modifier", "Guides judgement", "#9a7bb0", "Qualitative evidence that selects the upper or lower half — never given false precision.", "“automotive demand stronger than expected.”"],
  ["scenario trigger", "Conditional risk", "#c99a3a", "A risk that only matters if an event occurs — lives in a scenario, not the base.", "a proposed tariff taking effect before period close."],
];

const CHAIN = [
  ["Source", "URL + frozen file + SHA-256 hash"],
  ["Exact quotation", "verbatim text + locator, verified against the frozen source"],
  ["Typed observation", "value, units, period, factType, confidence"],
  ["Approved signal", "role, direction, combination method, correlation group"],
  ["Validation decision", "accepted or rejected, with a reason"],
  ["Explicit Decimal formula", "the arithmetic the code actually ran"],
  ["Forecast component & final value", "written only to the required workbook cells"],
];

const IMPLEMENTED = [
  "Strict JSON company profiles and signal maps",
  "Source hashes, URLs, exact quotations and cutoff checks",
  "Reusable management-guidance and explicit-driver resolvers",
  "Deterministic anchor-plus-driver combination in Decimal",
  "Qualitative modifiers and conditional scenarios, no arbitrary weights",
  "Challenge checks for unsupported evidence, mismatches, double-counting",
  "Replayable JSON run receipts + an end-to-end ADI example",
];
const EXCLUDED = [
  "Generic news sentiment",
  "Automatic supplier-network inference",
  "Arbitrary model-generated weights",
  "Unrestricted LLM arithmetic",
  "A universal financial ontology",
  "A multi-agent swarm",
];

function SecHead({ eyebrow, title, children }) {
  return (
    <Reveal className="mx-auto mb-11 max-w-2xl text-center">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted-foreground">{eyebrow}</p>
      <h2 className="mt-3 font-heading text-[clamp(28px,4vw,40px)] font-medium leading-tight">{title}</h2>
      <p className="mt-3 text-muted-foreground">{children}</p>
    </Reveal>
  );
}

export default function Landing() {
  return (
    <div className="[--bg-glow:radial-gradient(1100px_520px_at_78%_-8%,color-mix(in_oklab,var(--primary)_10%,transparent),transparent_60%)]">
      {/* HERO */}
      <header className="relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0 bg-[var(--bg-glow)]" />
        <div className="relative mx-auto max-w-4xl px-6 pt-24 pb-12 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">Agents vs Wall Street</p>
          <h1 className="mx-auto mt-5 max-w-[16ch] font-heading text-[clamp(42px,7vw,76px)] font-medium leading-[1.02]">
            An evidence-to-forecast <em className="italic text-primary">compiler</em>
          </h1>
          <p className="mx-auto mt-6 max-w-[60ch] text-[clamp(17px,2.4vw,21px)] leading-relaxed text-foreground/75">
            One reusable forecasting worker, run four times in parallel — one per company. Each builds a source-backed
            profile, maps the signals that move each metric, resolves them into cited evidence, and combines them with
            deterministic code into an auditable forecast.
          </p>

          <div className="mx-auto mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link to="/workspaces" className="inline-flex items-center gap-2 rounded-full bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow-sm transition hover:opacity-90">
              Open the dashboard <ArrowRight className="size-4" />
            </Link>
            <a href="#worker" className="inline-flex items-center gap-2 rounded-full border bg-card px-5 py-2.5 text-sm font-medium transition hover:bg-muted">
              How it works
            </a>
          </div>

          <div className="mx-auto mt-9 max-w-[760px] rounded-xl border border-l-[3px] border-l-primary bg-card p-5 text-left shadow-[0_8px_30px_-18px_rgba(60,40,20,.35)]">
            <p className="text-[15px] leading-relaxed text-foreground/80">
              <b className="font-heading font-semibold">The rule that keeps it honest.</b> The model may propose
              structured observations. It may <b className="font-heading font-semibold">not</b> invent sources, choose
              arbitrary weights, perform forecast arithmetic, or write submission values. A signal moves a number only
              when its evidence and declared transformation pass deterministic validation.
            </p>
          </div>

          <div className="mt-9 flex flex-wrap items-center justify-center gap-2.5">
            {WORKERS.map((w) => (
              <div key={w.slug} className="flex items-center gap-2.5 rounded-full border bg-card py-1.5 pl-1.5 pr-4 text-sm font-medium">
                <Logo slug={w.slug} name={w.name} size="sm" className="!size-7 !rounded-full !p-1" />
                {w.name}
              </div>
            ))}
          </div>
        </div>
      </header>

      {/* ORCHESTRATION */}
      <section id="orchestration" className="border-t py-16">
        <div className="mx-auto max-w-[1080px] px-6">
          <SecHead eyebrow="How the work fans out" title="One worker, four companies, in parallel">
            An orchestrator spins up an identical worker per company. Each returns three validated forecasts;
            deterministic code validates them and writes the submission workbooks.
          </SecHead>
          <Reveal>
            <svg viewBox="0 0 960 560" className="block h-auto w-full" role="img" aria-label="Orchestration diagram">
              {/* connectors */}
              {WORKERS.map((w, i) => {
                const cx = w.x + 88;
                return <path key={"c" + i} id={"lc" + i} className="fill-none stroke-border" strokeWidth="1.6"
                  d={`M480,74 C480,150 ${cx},120 ${cx},196`} />;
              })}
              {WORKERS.map((w, i) => {
                const cx = w.x + 88;
                return <path key={"v" + i} id={"lv" + i} className="fill-none stroke-border" strokeWidth="1.6"
                  d={`M${cx},338 C${cx},424 480,404 480,470`} />;
              })}
              {/* flow tokens */}
              {WORKERS.map((_, i) => (
                <circle key={"tc" + i} className="fill-primary" r="3.4">
                  <animateMotion dur="2.2s" repeatCount="indefinite" begin={`${i * 0.5}s`}><mpath href={`#lc${i}`} /></animateMotion>
                </circle>
              ))}
              {WORKERS.map((_, i) => (
                <circle key={"tv" + i} className="fill-primary" r="3.4">
                  <animateMotion dur="2.4s" repeatCount="indefinite" begin={`${1.1 + i * 0.5}s`}><mpath href={`#lv${i}`} /></animateMotion>
                </circle>
              ))}

              {/* orchestrator */}
              <rect x="360" y="18" width="240" height="56" rx="14" className="fill-card stroke-primary" strokeWidth="1.4" />
              <text x="480" y="42" textAnchor="middle" className="font-heading fill-foreground text-[17px] font-semibold">Orchestrator</text>
              <text x="480" y="60" textAnchor="middle" className="fill-muted-foreground text-[11px]">agent plugin · one worker per company</text>

              {/* workers */}
              {WORKERS.map((w) => (
                <g key={w.slug}>
                  <rect x={w.x} y="196" width="176" height="92" rx="14" className="fill-card stroke-border" strokeWidth="1.2" />
                  <rect x={w.x + 12} y="212" width="34" height="34" rx="8" className="fill-white stroke-border" strokeWidth="1" />
                  <image href={LOGO_SRC[w.slug]} x={w.x + 15} y="215" width="28" height="28" preserveAspectRatio="xMidYMid meet" />
                  <text x={w.x + 56} y="230" className="font-heading fill-foreground text-[14px] font-medium">{w.name}</text>
                  <text x={w.x + 56} y="248" className="fill-muted-foreground text-[10px] font-mono">{w.tk}</text>
                  {/* forecasts pill */}
                  <rect x={w.x} y="312" width="176" height="26" rx="13" className="fill-primary/10" />
                  <text x={w.x + 88} y="329" textAnchor="middle" className="fill-primary text-[11px] font-semibold">3 forecasts · by consensus</text>
                </g>
              ))}

              {/* convergence */}
              <rect x="340" y="470" width="280" height="58" rx="14" className="fill-card stroke-border" strokeWidth="1.2" />
              <text x="480" y="494" textAnchor="middle" className="font-heading fill-foreground text-[15px] font-semibold">Validate &amp; write workbooks</text>
              <text x="480" y="513" textAnchor="middle" className="fill-muted-foreground text-[11px]">deterministic checks → Excel submissions</text>
            </svg>
          </Reveal>
        </div>
      </section>

      {/* CONSENSUS MODEL */}
      <section id="consensus" className="border-t py-16">
        <div className="mx-auto max-w-[1080px] px-6">
          <SecHead eyebrow="The consensus model" title="Every number is a consensus — and we read the reasoning">
            No figure is a single guess. Several independent estimates are produced for each number. Before they are
            blended, a challenger reads the <em className="not-italic font-medium text-foreground/80">reasoning</em> behind
            each one — not just the evidence it surfaced — and drops the estimates whose logic is biased or double-counts
            a correlated signal. The survivors form the consensus, with a trust score.
          </SecHead>

          <Reveal>
            <svg viewBox="0 0 960 300" className="block h-auto w-full" role="img" aria-label="Consensus model diagram">
              {(() => {
                const est = [
                  { m: "Guidance anchor", ok: true },
                  { m: "Historical seasonality", ok: true },
                  { m: "Driver bridge", ok: true },
                  { m: "Peer read-across", ok: false, why: "biased reasoning" },
                  { m: "Segment model", ok: true },
                ];
                const top = (i) => 8 + i * 58;
                const cy = (i) => top(i) + 22;
                return (
                  <>
                    {/* gate line */}
                    <line x1="452" y1="16" x2="452" y2="284" className="stroke-border" strokeWidth="1.4" strokeDasharray="4 5" />
                    <text x="452" y="298" textAnchor="middle" className="fill-muted-foreground text-[10px]">reasoning &amp; bias check</text>

                    {/* connectors + tokens */}
                    {est.map((e, i) =>
                      e.ok ? (
                        <g key={"k" + i}>
                          <path id={"kc" + i} className="fill-none stroke-border" strokeWidth="1.6"
                            d={`M278,${cy(i)} C430,${cy(i)} 470,150 612,150`} />
                          <circle className="fill-primary" r="3.2">
                            <animateMotion dur="2.3s" repeatCount="indefinite" begin={`${i * 0.45}s`}><mpath href={`#kc${i}`} /></animateMotion>
                          </circle>
                        </g>
                      ) : (
                        <g key={"k" + i}>
                          <path className="fill-none stroke-down/50" strokeWidth="1.4" strokeDasharray="4 4"
                            d={`M278,${cy(i)} L436,${cy(i)}`} />
                          <circle cx="452" cy={cy(i)} r="9" className="fill-down/12 stroke-down/50" strokeWidth="1" />
                          <text x="452" y={cy(i) + 3.5} textAnchor="middle" className="fill-down text-[11px] font-bold">✕</text>
                        </g>
                      )
                    )}

                    {/* estimate cards */}
                    {est.map((e, i) => (
                      <g key={"e" + i} opacity={e.ok ? 1 : 0.5}>
                        <rect x="28" y={top(i)} width="250" height="44" rx="11"
                          className={cn("fill-card", e.ok ? "stroke-border" : "stroke-down/40")} strokeWidth="1.2"
                          strokeDasharray={e.ok ? undefined : "5 4"} />
                        <circle cx="48" cy={cy(i)} r="4" className={e.ok ? "fill-primary" : "fill-down/60"} />
                        <text x="66" y={cy(i) - 2} className="font-heading fill-foreground text-[13px] font-medium">{e.m}</text>
                        <text x="66" y={cy(i) + 12} className={cn("text-[10px]", e.ok ? "fill-muted-foreground" : "fill-down")}>
                          {e.ok ? "independent estimate" : e.why + " — dropped"}
                        </text>
                      </g>
                    ))}

                    {/* consensus node */}
                    <rect x="612" y="92" width="320" height="116" rx="16" className="fill-card stroke-primary" strokeWidth="1.4" />
                    <text x="632" y="122" className="font-heading fill-foreground text-[16px] font-semibold">Consensus value</text>
                    <text x="632" y="142" className="fill-muted-foreground text-[11px] font-mono">median of surviving estimates</text>
                    <text x="632" y="166" className="fill-primary text-[18px] font-mono font-semibold">2,760</text>
                    <text x="686" y="166" className="fill-muted-foreground text-[11px] font-mono">USDm</text>
                    {/* trust bar */}
                    <text x="632" y="190" className="fill-muted-foreground text-[10px] uppercase tracking-wide">trust</text>
                    <rect x="668" y="182" width="220" height="7" rx="3.5" className="fill-muted" />
                    <rect x="668" y="182" width="180" height="7" rx="3.5" className="fill-primary" />
                    <text x="896" y="190" textAnchor="end" className="fill-foreground text-[10px] font-mono">0.82</text>
                  </>
                );
              })()}
            </svg>
          </Reveal>

          <Reveal className="mt-10 rounded-2xl border bg-card p-6">
            <div className="flex flex-col items-center gap-6 sm:flex-row sm:justify-between">
              <div className="max-w-md">
                <h3 className="font-heading text-lg font-medium">Averaging cancels the bias</h3>
                <p className="mt-1.5 text-[13.5px] leading-relaxed text-muted-foreground">
                  We ran the forecast <b className="text-foreground/80">{RESULT.runs}×</b> per company and took the
                  consensus. It lands closer than any single run — the errors that pull individual runs off-target
                  average out.
                </p>
              </div>
              <div className="flex items-center gap-5">
                <div className="text-center">
                  <div className="font-mono text-2xl font-semibold text-muted-foreground/70">{RESULT.single}</div>
                  <div className="text-[11px] uppercase tracking-wide text-muted-foreground">single run</div>
                </div>
                <ArrowRight className="size-5 text-primary" />
                <div className="text-center">
                  <div className="font-mono text-3xl font-bold text-primary">{RESULT.consensus}</div>
                  <div className="text-[11px] uppercase tracking-wide text-muted-foreground">consensus</div>
                </div>
              </div>
            </div>
            <p className="mt-4 border-t pt-3 text-[11px] text-muted-foreground">
              Error = mean absolute % difference vs the analyst consensus figure.
            </p>
          </Reveal>

          <Reveal className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-3">
            {[
              ["Independent estimates", "Each number is produced several ways — guidance, seasonality, drivers, segments — instead of one path."],
              ["Reasoning inspected", "The challenger judges why each estimate landed where it did, catching bias and correlated evidence dressed up as independent."],
              ["Blended with a trust score", "Only survivors are combined, and the consensus carries a trust score set at the consensus level."],
            ].map(([t, d]) => (
              <div key={t} className="rounded-2xl border bg-card p-5">
                <h3 className="font-heading text-base font-medium">{t}</h3>
                <p className="mt-1.5 text-[13.5px] leading-relaxed text-muted-foreground">{d}</p>
              </div>
            ))}
          </Reveal>
        </div>
      </section>

      {/* WORKER PIPELINE */}
      <section id="worker" className="border-t py-16">
        <div className="mx-auto max-w-[1080px] px-6">
          <SecHead eyebrow="The worker" title="Every worker follows six stages">
            Profile the company, decide which signals matter, resolve them into cited evidence, combine them into an
            auditable number, stress the scenarios, then challenge and validate before returning.
          </SecHead>
          <Reveal className="relative">
            <div className="absolute inset-x-[5%] top-[34px] hidden h-0.5 overflow-hidden rounded bg-border md:block">
              <div className="h-full w-[34%] bg-[linear-gradient(90deg,transparent,var(--primary),transparent)]"
                style={{ animation: "lp-sweep 5.4s linear infinite" }} />
            </div>
            <div className="grid grid-cols-2 gap-x-3.5 gap-y-8 md:grid-cols-6">
              {STAGES.map(([n, title, desc], i) => (
                <div key={n} className="text-center">
                  <div className="relative mx-auto grid size-[52px] place-items-center rounded-full border-[1.5px] bg-card font-heading text-xl font-semibold text-primary">
                    {n}
                    <span className="pointer-events-none absolute -inset-1 rounded-full border-[1.5px] border-primary opacity-0"
                      style={{ animation: "lp-ring 5.4s ease-in-out infinite", animationDelay: `${i * 0.9}s` }} />
                  </div>
                  <h3 className="mt-3.5 font-heading text-base font-medium">{title}</h3>
                  <p className="mx-1 mt-2 text-[13px] leading-relaxed text-muted-foreground">{desc}</p>
                </div>
              ))}
            </div>
          </Reveal>
        </div>
      </section>

      {/* SIGNALS */}
      <section id="signals" className="border-t py-16">
        <div className="mx-auto max-w-[1080px] px-6">
          <SecHead eyebrow="Signals & roles" title="Not every signal gets a number">
            Instead of inventing arbitrary weights, each signal is assigned a role. A weight appears only when a
            backtest or historical analysis defensibly justifies it.
          </SecHead>
          <Reveal className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {ROLES.map(([tag, title, color, desc, ex]) => (
              <div key={tag} className="rounded-2xl border border-t-[3px] bg-card p-5" style={{ borderTopColor: color }}>
                <span className="inline-block rounded-md px-2 py-1 font-mono text-[11px] font-semibold"
                  style={{ color, background: `color-mix(in oklab, ${color} 12%, transparent)` }}>{tag}</span>
                <h3 className="mt-3 font-heading text-lg font-medium">{title}</h3>
                <p className="mt-2 text-[13.5px] leading-relaxed text-muted-foreground">{desc}</p>
                <p className="mt-3 border-t border-dashed pt-2.5 text-[12.5px] text-foreground/70">
                  <b className="font-heading">e.g.</b> {ex}
                </p>
              </div>
            ))}
          </Reveal>
        </div>
      </section>

      {/* PROVENANCE */}
      <section id="provenance" className="border-t py-16">
        <div className="mx-auto max-w-[1080px] px-6">
          <SecHead eyebrow="Traceability" title="Every number keeps its receipt">
            No value reaches a forecast without an unbroken chain from a hashed source to an explicit formula.
            Accepted inputs replay to the same output.
          </SecHead>
          <div className="mx-auto flex max-w-xl flex-col gap-3">
            {CHAIN.map(([t, s], i) => (
              <Reveal key={t} delay={i * 90}>
                <div className="relative flex items-center gap-4 rounded-xl border bg-card px-4.5 py-3.5">
                  <div className="grid size-9 flex-none place-items-center rounded-[10px] bg-primary/10 font-mono text-[13px] font-semibold text-primary">
                    {String(i + 1).padStart(2, "0")}
                  </div>
                  <div>
                    <b className="font-heading text-[15px] font-semibold">{t}</b>
                    <span className="block text-[13px] text-muted-foreground">{s}</span>
                  </div>
                  {i < CHAIN.length - 1 && <span className="absolute -bottom-3 left-[34px] h-3 w-0.5 bg-border" />}
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* SCOPE */}
      <section id="scope" className="border-t py-16">
        <div className="mx-auto max-w-[1080px] px-6">
          <SecHead eyebrow="Disciplined scope" title="What's in, and what's deliberately out">
            The architecture stays generic even though only the signals needed for today's four companies are built.
          </SecHead>
          <Reveal className="grid grid-cols-1 gap-5 md:grid-cols-2">
            <div className="rounded-2xl border bg-card p-6">
              <h3 className="flex items-center gap-2.5 font-heading text-lg font-medium">
                <span className="grid size-5 place-items-center rounded-md bg-[#e6f0e3] text-xs font-bold text-[#5f8a5c]">✓</span>
                Implemented now
              </h3>
              <ul className="mt-4 flex flex-col gap-2.5">
                {IMPLEMENTED.map((t) => (
                  <li key={t} className="flex gap-3 text-[14.5px] leading-snug text-foreground/80">
                    <span className="mt-0.5 grid size-5 flex-none place-items-center rounded-md bg-[#e6f0e3] text-xs font-bold text-[#5f8a5c]">✓</span>
                    {t}
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-2xl border bg-card p-6">
              <h3 className="flex items-center gap-2.5 font-heading text-lg font-medium">
                <span className="grid size-5 place-items-center rounded-md bg-[#f2e6e2] text-xs font-bold text-[#b4553a]">✕</span>
                Kept off the critical path
              </h3>
              <ul className="mt-4 flex flex-col gap-2.5">
                {EXCLUDED.map((t) => (
                  <li key={t} className="flex gap-3 text-[14.5px] leading-snug text-foreground/80">
                    <span className="mt-0.5 grid size-5 flex-none place-items-center rounded-md bg-[#f2e6e2] text-xs font-bold text-[#b4553a]">✕</span>
                    {t}
                  </li>
                ))}
              </ul>
            </div>
          </Reveal>
        </div>
      </section>

      <footer className="border-t py-14 text-center text-sm text-muted-foreground">
        <div className="mb-2.5 font-heading text-[22px] text-foreground">Centurion</div>
        <p>
          A source-to-formula receipt for every forecast.<br />
          <Link to="/workspaces" className="font-medium text-primary hover:underline">Open the dashboard</Link>
          {"  ·  "}
          <a href="https://github.com/KiishiAD/agents-vs-wall-street-starter" className="font-medium text-primary hover:underline">Repository</a>
        </p>
      </footer>
    </div>
  );
}
