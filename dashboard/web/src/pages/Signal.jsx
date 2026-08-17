import React from "react";
import { Link, useParams } from "react-router-dom";
import { useLive, matchSlug } from "../live.jsx";
import { Card } from "@/components/ui/card";
import { AreaChart, StanceBadge, StatusDot, StatusChip, Weight, pct, timeAgo } from "../ui.jsx";

function KV({ label, children }) {
  return (
    <div>
      <span className="block text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">{label}</span>
      <b className="font-mono text-lg">{children}</b>
    </div>
  );
}

function SectionHead({ title }) {
  return <h2 className="mb-3.5 font-heading text-[17px] font-medium">{title}</h2>;
}

export default function Signal() {
  const { slug, signalId } = useParams();
  const { data: signal } = useLive(`/api/companies/${slug}/signals/${signalId}`, {
    match: (e) => e.slug === slug && e.path.includes(signalId),
    deps: [slug, signalId],
  });
  const { data: bundle } = useLive(`/api/companies/${slug}`, {
    match: matchSlug(slug),
    deps: [slug],
  });

  if (!signal) return <div className="text-sm text-muted-foreground">Loading signal…</div>;

  const agents = (bundle?.agents || []).filter((a) => (a.signalIds || []).includes(signalId));
  const runs = (bundle?.runs || []).filter((r) => r.signalId === signalId);

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
        <Link to="/workspaces" className="hover:text-foreground">Workspaces</Link>
        <span className="opacity-50">/</span>
        <Link to={`/c/${slug}`} className="hover:text-foreground">{bundle?.company?.name || slug}</Link>
        <span className="opacity-50">/</span>
        <b>{signal.title}</b>
      </div>

      <Card className="mb-2 p-6">
        <div className="text-[11px] uppercase tracking-wide text-muted-foreground">{signal.category}</div>
        <h1 className="mt-1 font-heading text-[27px] font-medium">{signal.title}</h1>
        <p className="mt-2 max-w-200 text-sm leading-relaxed text-muted-foreground">{signal.description}</p>

        <div className="my-4 flex flex-wrap gap-8">
          <KV label="current">{signal.value} <span className="text-xs text-muted-foreground">{signal.unit}</span></KV>
          <KV label="implied prob.">{pct(signal.p)}</KV>
          <KV label="confidence">{pct(signal.confidence)}</KV>
          <div>
            <span className="block text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">stance</span>
            <div className="mt-1"><StanceBadge stance={signal.stance} /></div>
          </div>
          <div>
            <span className="block text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">weight</span>
            <div className="mt-1"><Weight value={signal.weight} /></div>
          </div>
        </div>

        {signal.source && (
          <div className="rounded-lg bg-primary/4 p-3.5 ring-1 ring-foreground/10">
            <div className="mb-1.5 text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">sources</div>
            <p className="text-[13px] leading-relaxed text-foreground/80">{signal.source}</p>
          </div>
        )}
      </Card>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <section>
          <SectionHead title="Metric history" />
          <Card className="p-4"><AreaChart points={signal.valueHistory || []} field="value" w={560} h={180} /></Card>
        </section>
        <section>
          <SectionHead title="Implied probability" />
          <Card className="p-4"><AreaChart points={signal.history || []} field="p" w={560} h={180} /></Card>
        </section>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <section>
          <SectionHead title="Agents on this signal" />
          <div className="flex flex-col gap-2.5">
            {agents.map((a) => (
              <div key={a.id} className="flex items-center gap-3 rounded-xl bg-card p-3.5 ring-1 ring-foreground/10">
                <StatusDot status={a.status} />
                <div className="min-w-0 flex-1">
                  <div className="font-medium">{a.name}</div>
                  <div className="text-xs text-muted-foreground">{a.role}</div>
                </div>
                <StatusChip status={a.status} />
              </div>
            ))}
            {agents.length === 0 && <div className="text-sm text-muted-foreground">No agents assigned.</div>}
          </div>
        </section>

        <section>
          <SectionHead title="Runs for this signal" />
          <Card className="gap-0 p-1.5">
            {runs.slice(0, 10).map((r, i) => (
              <Link to={`/c/${slug}/runs/${r.id}`} key={r.id}
                className={`flex items-center gap-3 rounded-lg px-3 py-2.5 hover:bg-muted/60 ${i > 0 ? "border-t" : ""}`}>
                <StatusDot status={r.status} />
                <span className="min-w-38 font-medium">{r.agentName}</span>
                <span className="flex-1 truncate text-xs text-muted-foreground">{r.summary || (r.status === "running" ? "in progress…" : "")}</span>
                <span className="whitespace-nowrap text-xs text-muted-foreground">{timeAgo(r.startedAt)}</span>
              </Link>
            ))}
            {runs.length === 0 && <div className="p-3.5 text-sm text-muted-foreground">No runs yet.</div>}
          </Card>
        </section>
      </div>
    </div>
  );
}
