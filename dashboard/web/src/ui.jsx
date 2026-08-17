import React from "react";
import { ArrowUp, ArrowDown, Minus } from "lucide-react";
import { useLiveStatus } from "./live.jsx";
import { cn } from "@/lib/utils";

export const pct = (p) => `${(p * 100).toFixed(0)}%`;
export const pct1 = (p) => `${(p * 100).toFixed(1)}%`;
export const fmtNum = (v) =>
  typeof v === "number" ? (v >= 1000 ? v.toLocaleString() : String(v)) : v;

export function timeAgo(iso) {
  if (!iso) return "—";
  const s = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (s < 5) return "just now";
  if (s < 60) return `${s}s ago`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  return `${Math.floor(h / 24)}d ago`;
}

/* ---------- company logos ----------
   Files live in web/public/logos/<slug>.<ext>. Add a file, map it here;
   missing/broken files fall back to ticker initials automatically. */
const LOGOS = {
  "home-depot": "/logos/home-depot.png",
  "analog-devices": "/logos/analog-devices.svg",
  deere: "/logos/deere.webp",
  hays: "/logos/hays.png",
};

function initials(name = "", ticker = "") {
  const t = (ticker.split(":").pop() || "").replace(/[^A-Za-z]/g, "");
  if (t) return t.slice(0, 3).toUpperCase();
  return name.split(/\s+/).map((w) => w[0]).join("").slice(0, 2).toUpperCase();
}

const LOGO_SIZE = {
  sm: "size-10 rounded-lg p-1.5",
  lg: "size-14 rounded-xl p-2",
};

export function Logo({ slug, name, ticker, size = "sm", className }) {
  const src = LOGOS[slug];
  const [failed, setFailed] = React.useState(false);
  const box = cn(
    "inline-flex items-center justify-center shrink-0 bg-white ring-1 ring-foreground/10 overflow-hidden",
    LOGO_SIZE[size],
    className
  );
  if (!src || failed) {
    return (
      <span className={box} aria-hidden="true">
        <span className={cn("font-mono font-bold tracking-tight text-foreground/70", size === "lg" ? "text-lg" : "text-sm")}>
          {initials(name, ticker)}
        </span>
      </span>
    );
  }
  return (
    <span className={box}>
      <img src={src} alt={`${name} logo`} loading="lazy" className="h-full w-full object-contain" onError={() => setFailed(true)} />
    </span>
  );
}

/* ---------- status + direction ---------- */
export function StanceBadge({ stance }) {
  const map = {
    bullish: "bg-up/12 text-up",
    bearish: "bg-down/12 text-down",
  };
  return (
    <span className={cn("inline-flex h-5 items-center rounded-full px-2 text-xs font-medium capitalize", map[stance] || "bg-muted text-muted-foreground")}>
      {stance || "neutral"}
    </span>
  );
}

const DOT = {
  running: "bg-up shadow-[0_0_0_3px_var(--color-up)]/15 animate-pulse",
  completed: "bg-foreground/40",
  idle: "bg-muted-foreground/40",
  error: "bg-down",
};
export function StatusDot({ status }) {
  return <span className={cn("size-2.5 rounded-full shrink-0", DOT[status] || DOT.idle)} title={status} />;
}

const CHIP = {
  running: "bg-up/12 text-up",
  completed: "bg-primary/10 text-foreground",
  idle: "bg-muted text-muted-foreground",
  error: "bg-down/12 text-down",
};
export function StatusChip({ status }) {
  return (
    <span className={cn("inline-flex h-5 items-center rounded-full px-2 text-[11px] font-medium uppercase tracking-wide", CHIP[status] || CHIP.idle)}>
      {status}
    </span>
  );
}

export function DirArrow({ direction, className }) {
  if (direction === "up") return <ArrowUp className={cn("inline size-4 text-up", className)} />;
  if (direction === "down") return <ArrowDown className={cn("inline size-4 text-down", className)} />;
  return <Minus className={cn("inline size-4 text-muted-foreground", className)} />;
}

/* ---------- charts (SVG, themed via CSS vars) ---------- */
export function Sparkline({ values, w = 120, h = 30, stroke = "var(--primary)", fill = true }) {
  if (!values || values.length < 2) return <svg width={w} height={h} />;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const step = w / (values.length - 1);
  const pts = values.map((v, i) => [i * step, h - ((v - min) / span) * (h - 4) - 2]);
  const line = pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ");
  const area = `${line} L${w},${h} L0,${h} Z`;
  return (
    <svg width={w} height={h} className="block">
      {fill && <path d={area} fill={stroke} opacity="0.1" />}
      <path d={line} fill="none" stroke={stroke} strokeWidth="1.6" />
    </svg>
  );
}

export function AreaChart({ points, field = "p", w = 640, h = 180 }) {
  if (!points || points.length < 2)
    return <div className="py-10 text-center text-sm text-muted-foreground">gathering data…</div>;
  const vals = points.map((d) => d[field]);
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const span = max - min || 1;
  const padY = 16;
  const step = w / (points.length - 1);
  const y = (v) => h - padY - ((v - min) / span) * (h - padY * 2);
  const pts = vals.map((v, i) => [i * step, y(v)]);
  const line = pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ");
  const area = `${line} L${w},${h} L0,${h} Z`;
  const rising = vals[vals.length - 1] >= vals[0];
  const color = rising ? "var(--up)" : "var(--down)";
  const gid = `ag-${field}-${rising ? "up" : "dn"}`;
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="block w-full h-auto" preserveAspectRatio="none">
      <defs>
        <linearGradient id={gid} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.28" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      {[0.25, 0.5, 0.75].map((g) => (
        <line key={g} x1="0" x2={w} y1={padY + g * (h - padY * 2)} y2={padY + g * (h - padY * 2)}
          stroke="var(--border)" strokeWidth="1" strokeDasharray="3 4" opacity="0.8" />
      ))}
      <path d={area} fill={`url(#${gid})`} />
      <path d={line} fill="none" stroke={color} strokeWidth="2" />
      <circle cx={pts[pts.length - 1][0]} cy={pts[pts.length - 1][1]} r="3.5" fill={color} />
    </svg>
  );
}

export function Gauge({ value = 0.5, confidence, size = 160 }) {
  const r = size / 2 - 12;
  const c = size / 2;
  const circ = Math.PI * r;
  const dash = circ * value;
  const color = value >= 0.6 ? "var(--up)" : value <= 0.4 ? "var(--down)" : "var(--warn)";
  return (
    <div className="flex flex-col items-center" style={{ width: size }}>
      <svg width={size} height={size / 2 + 24}>
        <path d={arc(c, c, r, 180, 360)} fill="none" stroke="var(--muted)" strokeWidth="10" strokeLinecap="round" />
        <path d={arc(c, c, r, 180, 360)} fill="none" stroke={color} strokeWidth="10" strokeLinecap="round"
          strokeDasharray={`${dash} ${circ}`} />
        <text x={c} y={c - 6} textAnchor="middle" fill={color}
          className="font-mono font-bold" style={{ fontSize: 30, letterSpacing: -1 }}>
          {pct(value)}
        </text>
      </svg>
      {confidence != null && (
        <div className="text-xs text-muted-foreground -mt-1">
          confidence <b>{pct(confidence)}</b>
        </div>
      )}
    </div>
  );
}

function arc(cx, cy, r, startDeg, endDeg) {
  const s = polar(cx, cy, r, startDeg);
  const e = polar(cx, cy, r, endDeg);
  const large = endDeg - startDeg <= 180 ? 0 : 1;
  return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 1 ${e.x} ${e.y}`;
}
function polar(cx, cy, r, deg) {
  const rad = (deg * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

export function LiveIndicator() {
  const { connected } = useLiveStatus();
  return (
    <span className={cn(
      "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 font-mono text-[11px] tracking-wide",
      connected ? "text-up" : "text-muted-foreground"
    )}>
      <span className={cn("size-1.5 rounded-full bg-current animate-pulse", connected && "shadow-[0_0_0_3px_currentColor]/20")} />
      {connected ? "LIVE" : "offline"}
    </span>
  );
}

export function Weight({ value }) {
  return (
    <span className="inline-flex items-center gap-1.5 font-mono text-[11px]" title="Weight in consensus">
      <span className="inline-block h-1.5 rounded-full bg-linear-to-r from-foreground/70 to-foreground/40"
        style={{ width: `${Math.max(8, Math.min(100, value * 200))}%`, minWidth: 8 }} />
      <span className="text-muted-foreground">{pct(value)}</span>
    </span>
  );
}
