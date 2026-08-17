import React from "react";
import { Link, useParams } from "react-router-dom";
import { useLive, matchSlug } from "../live.jsx";
import { Card } from "@/components/ui/card";
import CompanyProfile from "../components/CompanyProfile.jsx";
import {
  AreaChart,
  Gauge,
  DirArrow,
  StanceBadge,
  StatusDot,
  StatusChip,
  Sparkline,
  Weight,
  Logo,
  pct,
  fmtNum,
  timeAgo,
} from "../ui.jsx";

function SectionHead({ title, aside }) {
  return (
    <div className="mb-3.5 flex items-baseline justify-between">
      <h2 className="font-heading text-[17px] font-medium">{title}</h2>
      {aside && <span className="text-xs text-muted-foreground">{aside}</span>}
    </div>
  );
}

export default function Company() {
  const { slug } = useParams();
  const { data, loading } = useLive(`/api/companies/${slug}`, {
    match: matchSlug(slug),
    deps: [slug],
  });

  if (loading && !data) return <div className="text-sm text-muted-foreground">Loading {slug}…</div>;
  if (!data) return <div>Company not found.</div>;

  const { company, forecast, signals, agents, runs, profile } = data;
  const activeRuns = runs.filter((r) => r.status === "running");

  return (
    <div>
      <div className="mb-4 flex items-center gap-2 text-xs text-muted-foreground">
        <Link to="/workspaces" className="hover:text-foreground">Workspaces</Link>
        <span className="opacity-50">/</span>
        <b>{company.name}</b>
      </div>

      {/* hero */}
      <Card className="mb-6 flex-row items-stretch justify-between gap-8 p-6">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-4">
            <Logo slug={company.id} name={company.name} ticker={company.ticker} size="lg" />
            <div>
              <div className="flex items-baseline gap-2.5">
                <span className="font-heading text-[27px] font-medium">{company.name}</span>
                <span className="rounded-md border px-1.5 font-mono text-xs text-muted-foreground">{company.ticker}</span>
              </div>
              <div className="mt-0.5 text-xs text-muted-foreground">{company.sector} · forecasting {company.period}</div>
            </div>
          </div>

          <p className="my-3 text-[17px] font-medium leading-snug">{company.question}</p>
          <p className="max-w-165 text-sm leading-relaxed text-muted-foreground">{company.description}</p>

          {company.metrics?.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-3">
              {company.metrics.map((m) => (
                <div key={m.label} className="min-w-40 rounded-lg bg-muted/50 px-3.5 py-2.5">
                  <div className="text-xs text-muted-foreground">{m.label}</div>
                  <div className="font-mono text-lg font-bold tracking-tight">
                    {fmtNum(m.consensus)} <span className="text-xs font-medium text-muted-foreground">{m.units}</span>
                  </div>
                  <div className="text-[9px] font-semibold uppercase tracking-wide text-muted-foreground">consensus</div>
                </div>
              ))}
            </div>
          )}

          {forecast?.rationale && (
            <div className="mt-4 rounded-lg bg-primary/4 p-3.5 ring-1 ring-foreground/10">
              <div className="mb-1.5 text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">consensus rationale</div>
              <p className="text-[13px] leading-relaxed text-foreground/80">{forecast.rationale}</p>
            </div>
          )}
          {company.corpusDocs?.length > 0 && (
            <div className="mt-3 text-xs text-muted-foreground">
              corpus: {company.corpusDocs.length} recent docs · e.g.{" "}
              <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-foreground/70">{company.corpusDocs[0]}</code>
            </div>
          )}
        </div>

        <div className="flex flex-col items-center justify-center gap-1.5">
          <Gauge value={forecast?.consensus ?? 0.5} confidence={forecast?.confidence} size={200} />
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <DirArrow direction={forecast?.direction} /> updated {timeAgo(forecast?.updatedAt)}
          </div>
        </div>
      </Card>

      {/* consensus trend */}
      <section className="my-6">
        <SectionHead title="Consensus trend" aside={`${forecast?.history?.length || 0} points`} />
        <Card className="p-4">
          <AreaChart points={forecast?.history || []} field="p" w={900} h={200} />
        </Card>
      </section>

      {/* profile */}
      {profile && (
        <section className="my-6">
          <CompanyProfile profile={profile} />
        </section>
      )}

      {/* agents + signals */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <section>
          <SectionHead title="Agents" aside={`${agents.filter((a) => a.status === "running").length} running`} />
          <div className="flex flex-col gap-2.5">
            {agents.map((a) => {
              const run = a.currentRunId
                ? runs.find((r) => r.id === a.currentRunId)
                : runs.find((r) => r.agentId === a.id);
              const target = run ? `/c/${slug}/runs/${run.id}` : null;
              const inner = (
                <>
                  <StatusDot status={a.status} />
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 font-medium">
                      {a.name}
                      {a.isConsensus && <span className="rounded bg-primary/10 px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-foreground/70">consensus</span>}
                    </div>
                    <div className="text-xs text-muted-foreground">{a.role}</div>
                    {run && (
                      <div className="mt-1 truncate font-mono text-xs text-muted-foreground">
                        {run.status === "running" ? "▶ running: " : "last: "}
                        {run.summary || run.signalTitle || "working…"}
                      </div>
                    )}
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <StatusChip status={a.status} />
                    <span className="text-xs text-muted-foreground">{timeAgo(a.lastActiveAt)}</span>
                  </div>
                </>
              );
              const base = "flex items-center gap-3 rounded-xl bg-card p-3.5 ring-1 ring-foreground/10";
              return target ? (
                <Link to={target} key={a.id} className={`${base} transition-all hover:-translate-y-0.5 hover:ring-foreground/20 hover:shadow-md`}>
                  {inner}
                </Link>
              ) : (
                <div key={a.id} className={base}>{inner}</div>
              );
            })}
          </div>
        </section>

        <section>
          <SectionHead title="Signals" aside={`${signals.length} tracked`} />
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {signals.map((s) => (
              <Link to={`/c/${slug}/signals/${s.id}`} key={s.id}>
                <Card className="gap-0 p-3.5 transition-all hover:-translate-y-0.5 hover:ring-foreground/20 hover:shadow-md">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="text-sm font-medium">{s.title}</div>
                      <div className="text-[11px] uppercase tracking-wide text-muted-foreground">{s.category}</div>
                    </div>
                    <StanceBadge stance={s.stance} />
                  </div>
                  <div className="my-2 flex items-center justify-between">
                    <div className="font-mono text-2xl font-bold tracking-tight">
                      {s.value}<span className="text-xs font-medium text-muted-foreground"> {s.unit}</span>
                    </div>
                    <Sparkline
                      values={(s.valueHistory || []).slice(-24).map((h) => h.value)}
                      w={130} h={34}
                      stroke={s.stance === "bearish" ? "var(--down)" : "var(--up)"}
                    />
                  </div>
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs text-muted-foreground">implied {pct(s.p)}</span>
                    <Weight value={s.weight} />
                    <span className="text-xs text-muted-foreground">{timeAgo(s.updatedAt)}</span>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </section>
      </div>

      {/* runs */}
      <section className="my-6">
        <SectionHead title="Recent runs" aside={`${activeRuns.length} active`} />
        <Card className="gap-0 p-1.5">
          {runs.slice(0, 12).map((r, i) => (
            <Link to={`/c/${slug}/runs/${r.id}`} key={r.id}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 hover:bg-muted/60 ${i > 0 ? "border-t" : ""}`}>
              <StatusDot status={r.status} />
              <span className="min-w-38 font-medium">{r.agentName}</span>
              <span className="min-w-33 text-xs text-muted-foreground">{r.signalTitle || "—"}</span>
              <span className="flex-1 truncate text-xs text-muted-foreground">{r.summary || (r.status === "running" ? "in progress…" : "")}</span>
              <span className="whitespace-nowrap text-xs text-muted-foreground">{timeAgo(r.startedAt)}</span>
            </Link>
          ))}
        </Card>
      </section>
    </div>
  );
}
