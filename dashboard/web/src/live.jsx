import React, { createContext, useContext, useEffect, useRef, useState, useCallback } from "react";

// One EventSource for the whole app. Components subscribe with a predicate over
// the changed path (e.g. "companies/rivian/...") and a callback.

const LiveCtx = createContext(null);

export function LiveProvider({ children }) {
  const subs = useRef(new Set());
  const [connected, setConnected] = useState(false);
  const [lastEventAt, setLastEventAt] = useState(0);

  useEffect(() => {
    const es = new EventSource("/api/events");
    es.addEventListener("hello", () => setConnected(true));
    es.addEventListener("change", (e) => {
      let data;
      try {
        data = JSON.parse(e.data);
      } catch {
        return;
      }
      setLastEventAt(Date.now());
      for (const sub of subs.current) {
        try {
          if (sub.match(data)) sub.cb(data);
        } catch {
          /* ignore subscriber errors */
        }
      }
    });
    es.onerror = () => setConnected(false);
    es.onopen = () => setConnected(true);
    return () => es.close();
  }, []);

  const subscribe = useCallback((match, cb) => {
    const sub = { match, cb };
    subs.current.add(sub);
    return () => subs.current.delete(sub);
  }, []);

  return (
    <LiveCtx.Provider value={{ subscribe, connected, lastEventAt }}>
      {children}
    </LiveCtx.Provider>
  );
}

export function useLiveStatus() {
  const ctx = useContext(LiveCtx);
  return { connected: ctx?.connected ?? false, lastEventAt: ctx?.lastEventAt ?? 0 };
}

// Fetch `url`, then refetch (debounced) whenever a change event matches `match`.
// `match` receives the event {path, slug} and returns boolean. Defaults to always.
export function useLive(url, { match, deps = [], throttle = 250 } = {}) {
  const { subscribe } = useContext(LiveCtx);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const timer = useRef(null);

  const fetchNow = useCallback(async () => {
    if (!url) return;
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      setData(await res.json());
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    setLoading(true);
    fetchNow();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url, ...deps]);

  useEffect(() => {
    if (!subscribe) return;
    const m = match || (() => true);
    return subscribe(m, () => {
      if (timer.current) return;
      timer.current = setTimeout(() => {
        timer.current = null;
        fetchNow();
      }, throttle);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [subscribe, url, ...deps]);

  return { data, error, loading, refetch: fetchNow };
}

// Convenience matchers.
export const matchSlug = (slug) => (evt) => evt.slug === slug;
export const matchPath = (substr) => (evt) => evt.path?.includes(substr);
