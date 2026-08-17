#!/usr/bin/env python3
"""
Build a Deere quarterly panel (revenue, diluted EPS, segment net sales, segment
operating profit, FY guidance) from the offline 8-K earnings releases, cross-checked
against SEC EDGAR XBRL companyfacts.

Stdlib only.  Writes <SCRATCH>/de_panel.json

Design notes
------------
* Each 8-K segment table carries BOTH the current-year and prior-year quarter, so
  every quarter is observed twice (once as "current", once as "prior" a year later).
  We record both and reconcile; disagreements are reported, never silently averaged.
* Segment definitions change in FY2021 (Ag & Turf splits into Production & Precision
  Ag + Small Ag & Turf).  We therefore also build a spliced "AG" series
  (= A&T before the split, PPA+SAT after) so margin history is continuous.
* Missing data is an absent key.  Never zero, never a guess.
"""
import json
import os
import re
import sys
import datetime as dt

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
FILINGS = os.path.join(CORPUS, "filings")
SCRATCH = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"

NUM = re.compile(r"\(?[-+]?\$?\s?\d[\d,]*(?:\.\d+)?\)?$")
MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"])}


# ---------------------------------------------------------------- table utils
def cells(line):
    return [c.strip().replace("​", "").strip()
            for c in line.strip().strip("|").split("|")]


def toks(line):
    out = []
    for c in cells(line):
        c = c.replace("$", "").strip()
        if not c or not NUM.match(c.replace(" ", "")):
            continue
        s = c.replace(",", "").replace(" ", "").replace("+", "")
        neg = s.startswith("(") and s.endswith(")")
        s = s.strip("()")
        try:
            v = float(s)
        except ValueError:
            continue
        out.append(-v if neg else v)
    return out


def norm0(s):
    """Normalise a row label WITHOUT stripping the trailing noun."""
    s = s.lower().replace("\u200b", "")
    s = s.replace("&amp;", "&")
    s = re.sub(r"\s*&\s*", " and ", s)
    s = re.sub(r"[*\u2020:]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    """Normalise a SEGMENT row label, dropping a trailing 'net sales'/'revenues'."""
    return re.sub(r"\s+(net sales|revenues|sales)$", "", norm0(s)).strip()


SEG_RAW = {
    "agriculture and turf": "AT",
    "construction and forestry": "CF",
    "production and precision ag": "PPA",
    "production and precision agriculture": "PPA",
    "small ag and turf": "SAT",
    "small agriculture and turf": "SAT",
    "financial services": "FS",
}
# OCR of the releases sometimes drops spaces ("Production &PrecisionAg"), so match
# on a space-free key as well.
SEG = dict(SEG_RAW)
SEG.update({k.replace(" ", ""): v for k, v in SEG_RAW.items()})


def seg_key(lab):
    if lab in SEG:
        return SEG[lab]
    return SEG.get(lab.replace(" ", ""))


# ---------------------------------------------------------------- 8-K parsing
def parse_dates_from_header(lines, i):
    """Look back a few lines for a column header carrying explicit period-end dates."""
    for l in lines[max(0, i - 8):i]:
        cs = cells(l)
        found = []
        for c in cs:
            m = re.match(r"^([A-Za-z]+)\s+(\d{1,2}),?\s*(\d{4})$", c.strip())
            if m and m.group(1).lower() in MONTHS:
                found.append(dt.date(int(m.group(3)), MONTHS[m.group(1).lower()],
                                     int(m.group(2))).isoformat())
        if len(found) >= 2:
            return found[:2]
    return None


FQ_FROM_NAME = re.compile(r"-(q[1-4]|fy)-8k")


def fiscal_from_filename(fname, published):
    """Deere reports Q1 in Feb, Q2 in May, Q3 in Aug and Q4/FY in Nov of the SAME
    fiscal year, so filename quarter + publication year fixes (fy, fq) unambiguously."""
    m = FQ_FROM_NAME.search(fname)
    if not m:
        return None
    tag = m.group(1)
    fq = 4 if tag == "fy" else int(tag[1])
    y, mo = int(published[:4]), int(published[5:7])
    expect = {1: (1, 2, 3), 2: (4, 5, 6), 3: (7, 8, 9), 4: (10, 11, 12)}[fq]
    if mo not in expect:
        return None                      # not a regular earnings release
    return y, fq


def parse_8k(path):
    txt = open(path, encoding="utf-8").read()
    lines = txt.split("\n")
    pub = re.search(r'published_at:\s*"(\d{4}-\d{2}-\d{2})"', txt)
    per = re.search(r'period:\s*"(Q\d|FY)\s+(\d{4})"', txt)
    rec = {"file": os.path.basename(path),
           "published": pub.group(1) if pub else None,
           "period_label": (per.group(1) + " " + per.group(2)) if per else None,
           "sales": {}, "op": {}, "raw": {}}

    # ---- locate segment table
    starts = [i for i, l in enumerate(lines)
              if norm0(cells(l)[0] if cells(l) else "").startswith("net sales and revenues")
              and not toks(l)]
    best = None
    for i in starts:
        if any(norm0(cells(l)[0] if cells(l) else "").startswith("operating profit")
               and not toks(l) for l in lines[i:i + 40]):
            best = i
            break
    if best is None:
        return None
    d = parse_dates_from_header(lines, best)
    if d:
        rec["period_end"], rec["prior_period_end"] = d[0], d[1]

    mode = "sales"
    for l in lines[best:best + 45]:
        cs = cells(l)
        lab0 = norm0(cs[0]) if cs else ""
        lab = norm(cs[0]) if cs else ""
        if lab0.startswith("operating profit") and not toks(l):
            mode = "op"
            continue
        if lab0.startswith("net sales and revenues") and not toks(l):
            mode = "sales"
            continue
        t = toks(l)
        if not t:
            continue
        if mode == "sales":
            sk = seg_key(lab)
            if sk:
                rec["sales"][sk] = t
            elif lab0.startswith("total net sales and revenues"):
                rec["raw"]["total_rev"] = t
            elif lab0 == "total net sales":
                rec["raw"]["equip_net_sales"] = t
        else:
            sk = seg_key(lab)
            if sk:
                rec["op"][sk] = t
            elif lab0.startswith("total operating profit"):
                rec["raw"]["total_op"] = t
            elif lab0.startswith("net income attributable"):
                rec["raw"]["ni"] = t
                break

    # ---- EPS + period end from the headline paragraph
    head = "\n".join(lines[:120]).replace("&amp;", "&")
    m = re.search(r"quarter ended ([A-Z][a-z]+ \d{1,2},? \d{4}),? or \$?([\d.]+) per share",
                  head)
    m2 = re.search(r"or \$?([\d.]+) per share,? compared with net\s*income of \$?[\d.,]+ ?"
                   r"(?:billion|million)?,? or \$?([\d.]+) per share, for the (?:quarter|same period) ended "
                   r"([A-Z][a-z]+ \d{1,2},? \d{4})", head.replace("\n", " "))
    flat = head.replace("\n", " ")
    eps = re.findall(r"\$?([\d]+\.\d{2}) per share", flat)
    if eps:
        vals = [float(x) for x in eps]
        # "reported a net loss of $X ... or $Y per share" -> current quarter EPS is negative
        if re.search(r"net loss of \$[\d.,]+ ?(?:billion|million)? for the "
                     r"(?:first|second|third|fourth) quarter", flat, re.I):
            vals[0] = -vals[0]
        rec["raw"]["eps_text"] = vals
    ends = re.findall(r"(?:quarter|period) ended ([A-Z][a-z]+ \d{1,2},? \d{4})",
                      head.replace("\n", " "))
    parsed_ends = []
    for e in ends:
        mm = re.match(r"([A-Za-z]+) (\d{1,2}),? (\d{4})", e)
        if mm and mm.group(1).lower() in MONTHS:
            parsed_ends.append(dt.date(int(mm.group(3)), MONTHS[mm.group(1).lower()],
                                       int(mm.group(2))).isoformat())
    if parsed_ends and "period_end" not in rec:
        rec["period_end"] = parsed_ends[0]
        if len(parsed_ends) > 1:
            rec["prior_period_end"] = parsed_ends[1]

    # ---- FY net income guidance issued with this release
    body = txt.replace("&amp;", "&").replace("\n", " ")
    g = None
    pat_rng = re.search(r"net income attributable to Deere ?& ?Company for fiscal (\d{4}) is "
                        r"(?:forecasted|expected|anticipated|projected) to be in a range of "
                        r"\$?([\d.]+) billion to \$?([\d.]+) billion", body, re.I)
    pat_rng2 = re.search(r"net income attributable to Deere ?& ?Company .{0,60}?"
                         r"(?:forecast|expect|anticipat|project)\w*\s+to be\s+"
                         r"(?:in a range of\s+)?\$?([\d.]+)\s*(?:billion|million)?\s*to\s*"
                         r"\$?([\d.]+)\s*(billion|million)", body, re.I)
    pat_abt = re.search(r"net income attributable to Deere ?& ?Company is "
                        r"(?:anticipated|forecast|forecasted|expected|projected) to be "
                        r"(?:approximately |about |)\$?([\d.]+) (billion|million)", body, re.I)
    if pat_rng:
        g = {"lo": float(pat_rng.group(2)) * 1000, "hi": float(pat_rng.group(3)) * 1000}
    elif pat_rng2:
        mult = 1000 if pat_rng2.group(3).lower() == "billion" else 1
        g = {"lo": float(pat_rng2.group(1)) * mult, "hi": float(pat_rng2.group(2)) * mult}
    elif pat_abt:
        mult = 1000 if pat_abt.group(2).lower() == "billion" else 1
        g = {"lo": float(pat_abt.group(1)) * mult, "hi": float(pat_abt.group(1)) * mult}
    if g:
        rec["guidance_fy_ni_usdm"] = g
    return rec


# ---------------------------------------------------------------- fiscal calendar
def fq_from_end(iso):
    """Map a period-end date to (fiscal_year, fiscal_quarter) on Deere's Oct/Nov FY end."""
    d = dt.date.fromisoformat(iso)
    m, y = d.month, d.year
    if m in (1, 2):
        return y, 1
    if m in (4, 5):
        return y, 2
    if m in (7, 8):
        return y, 3
    if m in (10, 11):
        # FY ends late Oct / early Nov; early-Nov end still belongs to that FY
        return y, 4
    if m == 3:
        return y, 1
    if m in (6,):
        return y, 2
    if m in (9,):
        return y, 3
    if m == 12:
        return y + 1, 1
    return y, None


def main():
    files = sorted(f for f in os.listdir(FILINGS) if re.search(r"-(q\d|fy)-8k", f))
    recs = []
    for f in files:
        r = parse_8k(os.path.join(FILINGS, f))
        if r is None:
            print("SKIP (no segment table):", f, file=sys.stderr)
            continue
        recs.append(r)

    # de-duplicate: two 8-Ks on 2026-05-21 carry the same table
    seen, uniq = set(), []
    for r in sorted(recs, key=lambda x: x["published"]):
        key = (r["published"], tuple(sorted(r["sales"])), tuple(r["raw"].get("total_rev", [])[:2]))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)
    recs = uniq

    panel = {}          # (fy,fq) -> dict
    conflicts = []

    def put(fy, fq, field, val, src, pend):
        k = f"{fy}Q{fq}"
        e = panel.setdefault(k, {"fiscal_year": fy, "fiscal_quarter": fq,
                                 "period_end": pend, "sources": []})
        if pend and not e.get("period_end"):
            e["period_end"] = pend
        if field in e and abs(e[field] - val) > 1.0:
            conflicts.append((k, field, e[field], val, src))
            return
        e[field] = val
        if src not in e["sources"]:
            e["sources"].append(src)

    for r in recs:
        fk = fiscal_from_filename(r["file"], r["published"])
        if fk is None:
            print("SKIP (not a regular earnings release):", r["file"], file=sys.stderr)
            continue
        fy, fq = fk
        pfy, pfq = fy - 1, fq
        pe, ppe = r.get("period_end"), r.get("prior_period_end")
        # only trust a scraped date if it is consistent with the deterministic mapping
        if pe and fq_from_end(pe) != (fy, fq):
            pe = None
        if ppe and fq_from_end(ppe) != (pfy, pfq):
            ppe = None
        r["fy"], r["fq"] = fy, fq
        src = r["file"]
        for seg, t in r["sales"].items():
            if len(t) >= 2:
                put(fy, fq, f"sales_{seg}", t[0], src, pe)
                put(pfy, pfq, f"sales_{seg}", t[1], src, ppe)
        for seg, t in r["op"].items():
            if len(t) >= 2:
                put(fy, fq, f"op_{seg}", t[0], src, pe)
                put(pfy, pfq, f"op_{seg}", t[1], src, ppe)
        for nm, key in (("total_rev", "total_rev"), ("total_op", "total_op"),
                        ("equip_net_sales", "equip_net_sales"), ("ni", "net_income")):
            t = r["raw"].get(nm)
            if t and len(t) >= 2:
                put(fy, fq, key, t[0], src, pe)
                put(pfy, pfq, key, t[1], src, ppe)
        eps = r["raw"].get("eps_text")
        if eps and len(eps) >= 2:
            put(fy, fq, "eps_diluted", eps[0], src, pe)
            put(pfy, pfq, "eps_diluted", eps[1], src, ppe)
        if "guidance_fy_ni_usdm" in r:
            k = f"{fy}Q{fq}"
            panel.setdefault(k, {"fiscal_year": fy, "fiscal_quarter": fq,
                                 "period_end": pe, "sources": []})
            panel[k]["guidance_fy_ni_lo"] = r["guidance_fy_ni_usdm"]["lo"]
            panel[k]["guidance_fy_ni_hi"] = r["guidance_fy_ni_usdm"]["hi"]

    # ---- spliced AG series and equipment aggregate
    for k, e in panel.items():
        ag_s = ag_o = None
        if "sales_AT" in e and "op_AT" in e:
            ag_s, ag_o = e["sales_AT"], e["op_AT"]
        elif all(x in e for x in ("sales_PPA", "sales_SAT", "op_PPA", "op_SAT")):
            ag_s = e["sales_PPA"] + e["sales_SAT"]
            ag_o = e["op_PPA"] + e["op_SAT"]
        if ag_s is not None:
            e["sales_AG"] = ag_s
            e["op_AG"] = ag_o
        eq_s = eq_o = 0.0
        ok = False
        for seg in ("AG", "CF"):
            if f"sales_{seg}" in e and f"op_{seg}" in e:
                eq_s += e[f"sales_{seg}"]
                eq_o += e[f"op_{seg}"]
                ok = True
            else:
                ok = False
                break
        if ok:
            e["sales_EQUIP"] = eq_s
            e["op_EQUIP"] = eq_o
        for seg in ("AG", "CF", "PPA", "SAT", "EQUIP"):
            if f"sales_{seg}" in e and f"op_{seg}" in e and e[f"sales_{seg}"]:
                e[f"margin_{seg}"] = 100.0 * e[f"op_{seg}"] / e[f"sales_{seg}"]

    # ---- sign repair: the press-release text prints EPS unsigned in loss quarters
    for k, e in panel.items():
        if e.get("net_income") is not None and e.get("eps_diluted") is not None:
            if e["net_income"] < 0 and e["eps_diluted"] > 0:
                e["eps_diluted"] = -e["eps_diluted"]
                e.setdefault("notes", []).append("EPS sign corrected (loss quarter)")

    # ---- EDGAR cross-check of total revenue and EPS
    cf = json.load(open(os.path.join(SCRATCH, "cf.json")))
    g = cf["facts"]["us-gaap"]
    edgar = {}
    for tag, unit, field in (("Revenues", "USD", "total_rev"),
                             ("EarningsPerShareDiluted", "USD/shares", "eps_diluted")):
        for x in g[tag]["units"][unit]:
            if "start" not in x:
                continue
            days = (dt.date.fromisoformat(x["end"]) - dt.date.fromisoformat(x["start"])).days
            if not (80 <= days <= 100):
                continue
            fy, fq = fq_from_end(x["end"])
            v = x["val"] / 1e6 if field == "total_rev" else x["val"]
            edgar.setdefault(f"{fy}Q{fq}", {})[field] = round(v, 3)

    for k, ev in edgar.items():
        if k in panel and "eps_diluted" in ev and "eps_diluted" in panel[k]:
            if abs(ev["eps_diluted"] - panel[k]["eps_diluted"]) > 0.02:
                panel[k].setdefault("notes", []).append(
                    "EPS overridden by EDGAR XBRL (press-release text %.2f)"
                    % panel[k]["eps_diluted"])
                panel[k]["eps_diluted"] = ev["eps_diluted"]

    checks = {"rev_match": 0, "rev_mismatch": [], "eps_match": 0, "eps_mismatch": []}
    for k, ev in edgar.items():
        if k not in panel:
            continue
        if "total_rev" in ev and "total_rev" in panel[k]:
            if abs(ev["total_rev"] - panel[k]["total_rev"]) <= 1.5:
                checks["rev_match"] += 1
            else:
                checks["rev_mismatch"].append((k, ev["total_rev"], panel[k]["total_rev"]))
        if "eps_diluted" in ev and "eps_diluted" in panel[k]:
            if abs(ev["eps_diluted"] - panel[k]["eps_diluted"]) <= 0.02:
                checks["eps_match"] += 1
            else:
                checks["eps_mismatch"].append((k, ev["eps_diluted"], panel[k]["eps_diluted"]))

    # backfill total_rev / eps from EDGAR where the corpus has no 8-K (pre-FY2014)
    for k, ev in edgar.items():
        e = panel.setdefault(k, {"fiscal_year": int(k[:4]), "fiscal_quarter": int(k[-1]),
                                 "period_end": None, "sources": ["EDGAR XBRL"]})
        for f2, v in ev.items():
            if f2 not in e:
                e[f2] = v
                if "EDGAR XBRL" not in e["sources"]:
                    e["sources"].append("EDGAR XBRL")

    out = {"panel": panel, "conflicts": conflicts, "edgar_checks": checks,
           "n_8k_parsed": len(recs)}
    with open(os.path.join(SCRATCH, "de_panel.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    ks = sorted(panel, key=lambda k: (int(k[:4]), int(k[-1])))
    print(f"8-Ks parsed: {len(recs)}   quarters in panel: {len(panel)}   "
          f"{ks[0]} .. {ks[-1]}")
    print("EDGAR cross-check: revenue matches", checks["rev_match"],
          "mismatches", len(checks["rev_mismatch"]),
          "| EPS matches", checks["eps_match"], "mismatches", len(checks["eps_mismatch"]))
    for m in checks["rev_mismatch"][:10]:
        print("  REV MISMATCH", m)
    for m in checks["eps_mismatch"][:10]:
        print("  EPS MISMATCH", m)
    print("internal conflicts (same quarter, two filings disagree):", len(conflicts))
    for c in conflicts[:15]:
        print("  ", c)
    nseg = sum(1 for k in panel if "margin_AG" in panel[k])
    nppa = sum(1 for k in panel if "margin_PPA" in panel[k])
    neps = sum(1 for k in panel if "eps_diluted" in panel[k])
    nrev = sum(1 for k in panel if "total_rev" in panel[k])
    print(f"coverage: total_rev {nrev}, eps {neps}, AG margin {nseg}, PPA margin {nppa}")


if __name__ == "__main__":
    main()
