import React from "react";
import { FileText, ExternalLink, Anchor, SlidersHorizontal, Zap } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DirArrow } from "../ui.jsx";
import { cn } from "@/lib/utils";

// Order + human labels for the profile facets emitted by forecasting/profile.py.
const FACETS = [
  ["businessModel", "Business model"],
  ["productsAndCustomers", "Products & customers"],
  ["segmentsAndGeographies", "Segments & geographies"],
  ["revenueAndCostDrivers", "Revenue & cost drivers"],
  ["guidanceStyle", "Guidance style"],
  ["accountingDefinitions", "Accounting definitions"],
  ["cyclicalityAndSeasonality", "Cyclicality & seasonality"],
  ["externalExposures", "External exposures"],
  ["fiscalCalendar", "Fiscal calendar"],
];

const ROLE = {
  anchor: { label: "anchor", icon: Anchor, cls: "bg-primary/10 text-foreground" },
  modifier: { label: "modifier", icon: SlidersHorizontal, cls: "bg-muted text-muted-foreground" },
  scenario_trigger: { label: "scenario", icon: Zap, cls: "bg-warn/15 text-warn" },
};

function Cite({ ids, index }) {
  if (!ids?.length) return null;
  return (
    <span className="ml-1 inline-flex gap-0.5 align-super">
      {ids.map((id) => {
        const s = index[id];
        if (!s) return null;
        return (
          <a key={id} href={s.url} target="_blank" rel="noreferrer" title={s.title}
            className="rounded bg-muted px-1 text-[9px] font-medium text-muted-foreground hover:bg-primary/10 hover:text-foreground">
            {s.n}
          </a>
        );
      })}
    </span>
  );
}

export default function CompanyProfile({ profile }) {
  if (!profile) return null;
  const sources = profile.sources || [];
  const index = Object.fromEntries(sources.map((s, i) => [s.id, { ...s, n: i + 1 }]));
  const facets = FACETS.filter(([k]) => profile.profile?.[k]?.length);
  const cutoff = profile.informationCutoff ? new Date(profile.informationCutoff) : null;

  return (
    <Card className="gap-0 p-0">
      <CardHeader className="flex-row items-center justify-between border-b p-5">
        <div>
          <CardTitle className="text-base">Company profile</CardTitle>
          <div className="mt-0.5 text-xs text-muted-foreground">
            Source-backed research · {sources.length} cited {sources.length === 1 ? "source" : "sources"}
            {cutoff && <> · cutoff {cutoff.toLocaleDateString()}</>}
          </div>
        </div>
        <FileText className="size-5 text-muted-foreground" />
      </CardHeader>

      <CardContent className="p-5">
        <dl className="grid grid-cols-1 gap-x-8 gap-y-4 md:grid-cols-2">
          {facets.map(([key, label]) => (
            <div key={key}>
              <dt className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">{label}</dt>
              <dd className="mt-1 space-y-1.5">
                {profile.profile[key].map((c, i) => (
                  <p key={i} className="text-[13px] leading-relaxed text-foreground/80">
                    {c.claim}
                    <Cite ids={c.sourceIds} index={index} />
                  </p>
                ))}
              </dd>
            </div>
          ))}
        </dl>

        {profile.signalMap?.length > 0 && (
          <div className="mt-6 border-t pt-5">
            <div className="mb-3 text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">
              Signal map · {profile.signalMap.length} signals
            </div>
            <div className="grid grid-cols-1 gap-2.5 md:grid-cols-2">
              {profile.signalMap.map((s) => {
                const role = ROLE[s.role] || ROLE.modifier;
                const Icon = role.icon;
                return (
                  <div key={s.id} className="rounded-lg border p-3">
                    <div className="flex items-center justify-between gap-2">
                      <span className="flex items-center gap-1.5 text-[13px] font-medium">
                        {s.signal}
                        {s.expectedDirection === "up" && <DirArrow direction="up" className="size-3.5" />}
                        {s.expectedDirection === "down" && <DirArrow direction="down" className="size-3.5" />}
                      </span>
                      <span className={cn("inline-flex h-5 items-center gap-1 rounded-full px-2 text-[10px] font-medium uppercase tracking-wide", role.cls)}>
                        <Icon className="size-3" /> {role.label}
                      </span>
                    </div>
                    <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">{s.hypothesis}</p>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {sources.length > 0 && (
          <div className="mt-6 border-t pt-5">
            <div className="mb-2 text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">Sources</div>
            <ol className="space-y-1.5">
              {sources.map((s, i) => (
                <li key={s.id} className="flex gap-2 text-xs text-muted-foreground">
                  <span className="font-mono text-foreground/50">{i + 1}</span>
                  <div>
                    <a href={s.url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 font-medium text-foreground/80 hover:text-foreground hover:underline">
                      {s.title}
                      <ExternalLink className="size-3" />
                    </a>
                    <span className="ml-1.5">— {s.publisher}{s.publishedAt && `, ${s.publishedAt}`}</span>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
