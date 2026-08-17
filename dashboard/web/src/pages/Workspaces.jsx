import React from "react";
import { Link } from "react-router-dom";
import { useLive } from "../live.jsx";
import { Card } from "@/components/ui/card";
import { Sparkline, DirArrow, Logo, pct, fmtNum, timeAgo } from "../ui.jsx";

export default function Workspaces() {
  const { data: companies, loading } = useLive("/api/companies");

  return (
    <div>
      <div className="mb-7 mt-2">
        <h1 className="font-heading text-[32px] font-medium leading-tight">Workspaces</h1>
        <p className="mt-2 max-w-160 text-[15px] leading-relaxed text-muted-foreground">
          Each workspace runs a fleet of forecasting agents that collect signals and vote on a consensus outcome.
        </p>
      </div>

      {loading && <div className="text-sm text-muted-foreground">Loading workspaces…</div>}

      <div className="grid grid-cols-[repeat(auto-fill,minmax(360px,1fr))] gap-4">
        {(companies || []).map((c) => {
          const hist = c.forecast?.history?.slice(-30).map((h) => h.p) || [];
          const p = c.forecast?.consensus ?? 0;
          const trendColor = c.forecast?.direction === "down" ? "var(--down)" : "var(--up)";
          return (
            <Link to={`/c/${c.id}`} key={c.id} className="group">
              <Card className="h-full gap-0 p-5.5 transition-all duration-200 group-hover:-translate-y-0.5 group-hover:ring-foreground/15 group-hover:shadow-[0_8px_30px_-8px] group-hover:shadow-primary/15">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex min-w-0 items-center gap-3">
                    <Logo slug={c.id} name={c.name} ticker={c.ticker} size="sm" />
                    <div className="min-w-0">
                      <div className="flex items-baseline gap-2">
                        <span className="truncate font-heading text-[19px] font-medium">{c.name}</span>
                        <span className="rounded-md border px-1.5 font-mono text-[11px] text-muted-foreground">{c.ticker}</span>
                      </div>
                      <div className="mt-0.5 text-xs text-muted-foreground">{c.sector} · {c.period}</div>
                    </div>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="flex items-center gap-1 font-mono text-[27px] font-bold leading-none tracking-tight">
                      {pct(p)} <DirArrow direction={c.forecast?.direction} className="size-5" />
                    </span>
                    <span className="text-[10px] uppercase tracking-wide text-muted-foreground">consensus</span>
                  </div>
                </div>

                <p className="mt-4 text-sm leading-snug text-foreground/80">{c.question}</p>

                {c.metrics?.length > 0 && (
                  <div className="mt-3 flex gap-2">
                    {c.metrics.slice(0, 3).map((m) => (
                      <div key={m.label} className="min-w-0 flex-1 rounded-lg bg-muted/50 px-2.5 py-2">
                        <div className="truncate text-[10px] text-muted-foreground">{m.label}</div>
                        <div className="mt-0.5 font-mono text-sm font-semibold tracking-tight">
                          {fmtNum(m.consensus)} <span className="text-[10px] font-medium text-muted-foreground">{m.units}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                <div className="-mx-1.5 mt-3 mb-1">
                  <Sparkline values={hist} w={320} h={44} stroke={trendColor} />
                </div>

                <div className="mt-auto flex flex-wrap gap-4 border-t pt-3 text-xs text-muted-foreground">
                  <span><b className="font-mono text-foreground/80">{c.runningAgents}</b>/{c.agentCount} agents live</span>
                  <span><b className="font-mono text-foreground/80">{c.signalCount}</b> signals</span>
                  <span>conf <b className="font-mono text-foreground/80">{pct(c.forecast?.confidence ?? 0)}</b></span>
                  <span className="ml-auto">{timeAgo(c.forecast?.updatedAt)}</span>
                </div>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
