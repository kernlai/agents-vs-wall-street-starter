import React from "react";
import { Routes, Route, Link, Outlet, useLocation } from "react-router-dom";
import Landing from "./pages/Landing.jsx";
import Workspaces from "./pages/Workspaces.jsx";
import Company from "./pages/Company.jsx";
import Signal from "./pages/Signal.jsx";
import Run from "./pages/Run.jsx";
import { LiveIndicator } from "./ui.jsx";

function AppShell() {
  return (
    <main className="mx-auto max-w-310 px-6 pb-24 pt-7">
      <Outlet />
    </main>
  );
}

export default function App() {
  const loc = useLocation();
  const isLanding = loc.pathname === "/";
  return (
    <div className="min-h-full">
      <header className="sticky top-0 z-30 flex items-center justify-between border-b bg-background/70 px-7 py-3.5 backdrop-blur-xl">
        <Link to="/" className="group flex items-center gap-2.5">
          <span className="size-2 rounded-full bg-primary transition-transform group-hover:scale-125" />
          <span className="font-heading text-[19px] font-medium tracking-tight">Centurion</span>
          <span className="ml-1 hidden text-[12px] text-muted-foreground sm:inline">forecasting agents</span>
        </Link>
        <div className="flex items-center gap-4">
          {isLanding ? (
            <Link to="/workspaces" className="inline-flex items-center gap-1.5 rounded-full bg-primary px-4 py-2 text-[13px] font-medium text-primary-foreground transition hover:opacity-90">
              Open dashboard
            </Link>
          ) : (
            <>
              <Link to="/" className="text-sm text-muted-foreground transition hover:text-foreground">Architecture</Link>
              <LiveIndicator />
            </>
          )}
        </div>
      </header>

      <div key={loc.pathname}>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route element={<AppShell />}>
            <Route path="/workspaces" element={<Workspaces />} />
            <Route path="/c/:slug" element={<Company />} />
            <Route path="/c/:slug/signals/:signalId" element={<Signal />} />
            <Route path="/c/:slug/runs/:runId" element={<Run />} />
          </Route>
        </Routes>
      </div>
    </div>
  );
}
