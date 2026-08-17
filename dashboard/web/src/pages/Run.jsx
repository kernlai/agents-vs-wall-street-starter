import React, { useEffect, useRef } from "react";
import { Link, useParams } from "react-router-dom";
import { useLive } from "../live.jsx";
import { Card } from "@/components/ui/card";
import { StatusDot, StatusChip, timeAgo } from "../ui.jsx";

const LEVEL_MSG = {
  info: "text-slate-300",
  tool: "text-sky-400",
  result: "text-emerald-400",
  warn: "text-amber-400",
  error: "text-rose-400",
};

export default function Run() {
  const { slug, runId } = useParams();
  const { data: run } = useLive(`/api/companies/${slug}/runs/${runId}`, {
    match: (e) => e.slug === slug && e.path.includes(runId),
    deps: [slug, runId],
    throttle: 120,
  });
  const consoleRef = useRef(null);
  const log = run?.log || [];

  useEffect(() => {
    const el = consoleRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [log.length]);

  if (!run) return <div className="text-sm text-muted-foreground">Loading run…</div>;

  const dur = run.endedAt
    ? Math.round((new Date(run.endedAt) - new Date(run.startedAt)) / 1000)
    : Math.round((Date.now() - new Date(run.startedAt)) / 1000);

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
        <Link to="/workspaces" className="hover:text-foreground">Workspaces</Link>
        <span className="opacity-50">/</span>
        <Link to={`/c/${slug}`} className="hover:text-foreground">{slug}</Link>
        <span className="opacity-50">/</span>
        <b>{run.agentName}</b>
      </div>

      <Card className="mb-6 flex-row items-start justify-between gap-5 p-6">
        <div className="min-w-0">
          <div className="flex items-center gap-2.5 font-heading text-xl font-medium">
            <StatusDot status={run.status} />
            {run.agentName}
            <StatusChip status={run.status} />
          </div>
          <div className="mt-1 text-sm text-muted-foreground">
            signal: <b>{run.signalTitle || "all signals"}</b> · trigger {run.trigger} · started {timeAgo(run.startedAt)} · {dur}s
          </div>
          {run.summary && <div className="mt-2.5 font-mono text-[13px] text-foreground/70">{run.summary}</div>}
        </div>
        {run.result && (
          <div className="min-w-55 rounded-lg bg-muted/50 p-3.5">
            <div className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">result</div>
            <pre className="mt-1.5 whitespace-pre-wrap font-mono text-xs text-foreground/80">{JSON.stringify(run.result, null, 2)}</pre>
          </div>
        )}
      </Card>

      <section>
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="font-heading text-[17px] font-medium">Live trace</h2>
          <span className="text-xs text-muted-foreground">
            {log.length} lines{" "}
            {run.status === "running" && <span className="ml-1 animate-pulse text-up">● streaming</span>}
          </span>
        </div>
        <div ref={consoleRef}
          className="max-h-115 overflow-y-auto rounded-xl bg-[#0d1117] p-4 font-mono text-[12.5px] leading-relaxed ring-1 ring-black/40 shadow-md">
          {log.map((l, i) => (
            <div key={i} className="flex gap-3 py-px">
              <span className="w-21 shrink-0 text-slate-500">{new Date(l.t).toLocaleTimeString()}</span>
              <span className="w-15 shrink-0 self-center text-[10px] uppercase tracking-wide text-slate-500">{l.phase}</span>
              <span className={`flex-1 ${LEVEL_MSG[l.level] || LEVEL_MSG.info}`}>
                {l.message}
                {l.data && <span className="text-teal-400/80"> {JSON.stringify(l.data)}</span>}
              </span>
            </div>
          ))}
          {run.status === "running" && (
            <div className="flex gap-3 py-px">
              <span className="w-21 shrink-0" />
              <span className="w-15 shrink-0" />
              <span className="flex-1 animate-pulse text-emerald-400">▋</span>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
