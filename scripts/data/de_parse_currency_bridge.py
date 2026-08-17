#!/usr/bin/env python3
"""
Parse Deere & Company disclosed currency-translation effects out of the frozen
offline corpus (10-Q / 10-K / 8-K / slide-deck markdown).

Two disclosure families are captured, and they are NEVER mixed:

  A) MD&A "Currency translation" / "Currency translation impact on Net sales"
     rows.  Stated in PERCENTAGE POINTS of the year-over-year NET SALES change.
     Scope = segment (PPA / SAT / CF, or legacy A&T) or geography split
     (worldwide equipment ops / U.S. & Canada / outside U.S. & Canada).

  B) Slide-deck earnings-call waterfall "Currency" bars.  USDm, and they apply
     to OPERATING PROFIT, not to net sales.

Blank cells in the MD&A tables mean Deere disclosed no material effect (the
figure rounds to zero at 1pp granularity).  They are emitted as period entries
with value None so downstream code can decide -- they are never coerced to 0
silently, and never dropped without a trace.

Standard library only.
"""
import json
import os
import re
import sys

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"

ZW = dict.fromkeys(map(ord, "​‌‍﻿­"), None)


def clean(s):
    s = s.translate(ZW)
    s = s.replace(" ", " ").replace("–", "-").replace("—", "-")
    s = s.replace("&amp;", "&")
    return re.sub(r"\s+", " ", s).strip()


def split_row(line):
    line = line.strip()
    if not line.startswith("|"):
        return None
    cells = line.split("|")
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [clean(c) for c in cells]


def is_sep(cells):
    return bool(cells) and all(
        re.fullmatch(r":?-{2,}:?", c or "") for c in cells if c != "")


def iter_tables(lines):
    i, n = 0, len(lines)
    while i < n:
        if split_row(lines[i]) is None:
            i += 1
            continue
        start = i
        rows = []
        while i < n:
            cells = split_row(lines[i])
            if cells is None:
                break
            if not is_sep(cells):
                rows.append((i, cells))
            i += 1
        if rows:
            yield start, rows


NUM = re.compile(r"^[+-]?\$?\s*\(?\s*\$?\s*\d[\d,]*(?:\.\d+)?\s*%?\s*\)?$")


def parse_num(c):
    if c is None:
        return None
    t = c.strip()
    if t in ("", "-", "--", "N/A", "*", "$"):
        return None
    if not NUM.match(t):
        return None
    neg = t.lstrip().startswith("-") or (t.startswith("(") and t.endswith(")"))
    t = re.sub(r"[()$,%+\-\s]", "", t)
    if t == "":
        return None
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


# ---------------------------------------------------------------- scope map
# ORDER MATTERS: geography qualifiers before the generic catch-alls, and the
# "small" ag test before the plain ag test.
SCOPE_PATTERNS = [
    (r"outside\s+u\.?s\.?\s*(and|&)\s*canada", "OUTSIDE_US_CANADA"),
    (r"^u\.?s\.?\s*(and|&)\s*canada", "US_CANADA"),
    (r"production\s*(and|&)\s*precision\s*ag", "PPA"),
    (r"small\s*ag(riculture)?\s*(and|&)\s*turf", "SAT"),
    (r"construction\s*(and|&)\s*forestry", "CF"),
    (r"^agriculture\s*(and|&)\s*turf", "AT_LEGACY"),
    (r"worldwide net sales", "WW_EQUIP"),
    (r"^worldwide\b", "WW_EQUIP"),
    (r"equipment operations", "WW_EQUIP"),
]


def scope_of(label):
    low = label.lower().strip(": ")
    for pat, code in SCOPE_PATTERNS:
        if re.search(pat, low):
            return code
    return None


CURRENCY_ROW = re.compile(r"^currency translation\b", re.I)
PERIOD_HDR = re.compile(r"(three|six|nine|twelve)\s+months\s+ended", re.I)


def table_period_count(rows):
    """How many distinct reporting periods do this table's columns cover?"""
    seen = []
    for _ln, cells in rows[:3]:
        for c in cells:
            m = PERIOD_HDR.search(c)
            if m:
                key = m.group(1).lower()
                if key not in seen:
                    seen.append(key)
    return seen


def split_periods(cells, nperiods):
    """Map a currency row's numeric cells onto its reporting periods.

    The corpus tables are ragged (zero-width padding cells vary row to row), so
    column indices are unreliable.  What IS reliable is that the periods run
    left to right in equal-width blocks, so the row body is cut into nperiods
    contiguous blocks and each block contributes at most one number.
    """
    body = cells[1:]
    if nperiods <= 1:
        vals = [parse_num(c) for c in body]
        vals = [v for v in vals if v is not None]
        return [vals[-1] if vals else None]
    out = []
    width = len(body) / float(nperiods)
    for k in range(nperiods):
        lo, hi = int(round(k * width)), int(round((k + 1) * width))
        vals = [parse_num(c) for c in body[lo:hi]]
        vals = [v for v in vals if v is not None]
        out.append(vals[-1] if vals else None)
    return out


SKIP_TABLE = re.compile(
    r"comprehensive income|retained earnings|total equity|unrealized|hedg|"
    r"noncontrolling|accumulated other", re.I)

HEADING = re.compile(r"^[#*\s]*([A-Za-z][^|]*?)[*\s:]*$")


def context_scope(lines, start):
    """Fall back to the nearest preceding heading/sentence naming a segment."""
    for j in range(start - 1, max(-1, start - 12), -1):
        raw = clean(lines[j])
        if not raw or raw.startswith("|"):
            continue
        m = HEADING.match(raw)
        if not m:
            continue
        s = scope_of(m.group(1))
        if s:
            return s, m.group(1)[:70]
    return None, None


def file_meta(fn):
    m = re.match(r"^(\d{4}-\d{2}-\d{2})__de-us-\d{8}-(q[1-4]|fy)-([a-z0-9-]+?)__", fn)
    if not m:
        return None
    return {"published": m.group(1), "qtag": m.group(2), "kind": m.group(3)}


def parse_filing(path):
    fn = os.path.basename(path)
    meta = file_meta(fn)
    if meta is None:
        return []
    lines = open(path, encoding="utf-8").read().split("\n")
    out = []
    for start, rows in iter_tables(lines):
        labels = [r[1][0] if r[1] else "" for r in rows]
        joined = " || ".join(labels)
        if "urrency translation" not in joined:
            continue
        if SKIP_TABLE.search(joined):
            continue

        periods = table_period_count(rows)
        nper = max(1, len(periods))

        scope = None
        ctx_scope, ctx_label = context_scope(lines, start)
        net_sales = None

        for ln, cells in rows:
            first = cells[0] if cells else ""
            s = scope_of(first)
            if s:
                scope = s
            if re.match(r"^net sales", first, re.I):
                # per period block: [current, prior, % change]
                body = cells[1:]
                blocks = []
                width = len(body) / float(nper)
                for k in range(nper):
                    lo, hi = int(round(k * width)), int(round((k + 1) * width))
                    vv = [parse_num(c) for c in body[lo:hi]]
                    blocks.append([v for v in vv if v is not None])
                net_sales = blocks

            if CURRENCY_ROW.match(first):
                vals = split_periods(cells, nper)
                if all(v is None for v in vals) and "" == "":
                    pass  # keep: a wholly blank row is still a disclosure
                out.append({
                    "file": fn,
                    "line": ln + 1,
                    "published": meta["published"],
                    "qtag": meta["qtag"],
                    "kind": meta["kind"],
                    "scope": scope or ctx_scope,
                    "scope_from": "row" if scope else ("context" if ctx_scope else None),
                    "context_label": ctx_label,
                    "label": first,
                    "periods": periods or ["fy"],
                    "values": vals,
                    "net_sales_blocks": net_sales,
                    "raw": cells,
                })
    return out


# --------------------------------------------------- slide operating-profit

SEG_SLIDE = [
    (r"production\s*(?:&|and)?\s*precision\s*ag", "PPA"),
    (r"small\s*ag(?:riculture)?\s*(?:&|and)\s*turf", "SAT"),
    (r"construction\s*(?:&|and)\s*forestry", "CF"),
    (r"^ag(?:riculture)?\s*(?:&|and)\s*turf", "AT_LEGACY"),
]
SEG_HDR = re.compile(r"^[#*\s>]*\**\s*(?:" + "|".join(p for p, _ in SEG_SLIDE) + r")",
                     re.I)

# a money token: $1,148 / ($402) / -$46 / +$27 / ($9)
MONEY = re.compile(r"\(\s*-?\$?\s*(\d[\d,]*)\s*\)|([+-])?\s*\$\s*(\d[\d,]*)")

BRIDGE_LABELS = ["Volume/Mix", "Volume/ Mix", "Price", "Currency", "Warranty",
                 "Production Costs", "SA&G/R&D", "SA&G/ R&D", "Special Items",
                 "Other"]


def money_at(text, pos, radius=150):
    """Nearest money token to `pos`, preferring one that follows the label."""
    best = None
    for m in MONEY.finditer(text):
        if m.start() < pos - radius or m.start() > pos + radius:
            continue
        if m.group(1) is not None:                      # parenthesised = negative
            v = -float(m.group(1).replace(",", ""))
        else:
            v = float(m.group(3).replace(",", ""))
            if m.group(2) == "-":
                v = -v
        after = m.start() >= pos
        dist = abs(m.start() - pos) + (0 if after else 40)  # bias toward "after"
        if best is None or dist < best[0]:
            best = (dist, v, m.start(), m.end())
    return best


DECREASE = re.compile(r"decreas|down|reduc|negative|lower", re.I)
INCREASE = re.compile(r"increas|contribut|up |positive|higher|gain", re.I)


def parse_slide(path):
    """Pull the 'Currency' bar out of each segment operating-profit waterfall.

    These are OPERATING PROFIT effects in USDm.  They are not the net-sales
    currency effect and must never be merged with the MD&A percentage series.
    """
    fn = os.path.basename(path)
    text = clean_multiline(open(path, encoding="utf-8").read())
    out = []

    # segment headings, with their character offsets
    heads = []
    off = 0
    for line in text.split("\n"):
        m = SEG_HDR.match(line)
        if m:
            low = line.lower()
            for pat, code in SEG_SLIDE:
                if re.search(pat, low):
                    heads.append((off, code))
                    break
        off += len(line) + 1

    for wm in re.finditer(r"Operating Profit Comparison", text):
        start = wm.start()
        seg = None
        for hoff, code in heads:
            if hoff <= start:
                seg = code
        if seg is None:
            continue
        nxt = text.find("Operating Profit Comparison", start + 1)
        # Also stop at the next segment heading, otherwise the following
        # slide's net-sales bars leak in and break the waterfall arithmetic.
        nxt_head = min([h for h, _ in heads if h > start] or [len(text)])
        end = min(len(text), nxt if nxt > 0 else len(text), nxt_head, start + 2600)
        win = text[start:end]

        got = solve_waterfall(win)
        if got is None:
            continue
        assign, convention = got
        if "Currency" not in assign:
            continue
        out.append({"file": fn, "segment": seg, "value": assign["Currency"],
                    "line": text[:start].count("\n") + 1,
                    "convention": convention,
                    "bridge": assign,
                    "snippet": re.sub(r"\s+", " ", win[:200])})
    return out


LABEL_RE = re.compile(
    r"\b(Volume\s*/\s*ance|Volume\s*/\s*Mix|Price|Currency|Warranty(?: Costs)?|"
    r"Production Costs|SA&G\s*/\s*R&D|Special Items|Other)\b")
QTR_RE = re.compile(r"\b([1-4]Q\s*20\d\d)\b")


def solve_waterfall(win):
    """Read a full operating-profit waterfall and accept it only if it balances.

    The slide text is an LLM transcription of a chart image, so the value can
    sit before the label, after the label, or in a separate parallel list.  All
    three conventions are tried and one is accepted only when
    start + sum(components) == end exactly.  Anything that fails is discarded
    rather than guessed at, which is why the resulting series is short.
    """
    labels = [(m.start(), m.group(1)) for m in LABEL_RE.finditer(win)]
    quarters = [(m.start(), m.group(1)) for m in QTR_RE.finditer(win)]
    monies = []
    for m in MONEY.finditer(win):
        if m.group(1) is not None:
            v = -float(m.group(1).replace(",", ""))
        else:
            v = float(m.group(3).replace(",", ""))
            if m.group(2) == "-":
                v = -v
        monies.append((m.start(), v))
    if len(quarters) < 2 or not labels or not monies:
        return None

    # de-duplicate repeated label mentions, keeping first occurrence order
    seen_lab, ordered = set(), []
    for pos, lab in labels:
        key = re.sub(r"\s+", "", lab)
        if key in seen_lab:
            continue
        seen_lab.add(key)
        ordered.append((pos, key, lab))

    def check(assign, start_v, end_v):
        if start_v is None or end_v is None:
            return False
        return abs(start_v + sum(assign.values()) - end_v) < 0.5

    # Conventions A/B: a label's value sits immediately after it, or
    # immediately before it.  Real decks mix the two inside one chart, so every
    # per-label combination is enumerated and the waterfall identity picks the
    # winner.  If more than one distinct assignment balances, the chart is
    # ambiguous and is thrown away.
    n = len(ordered)

    def try_mask(mask):
        assign, used = {}, set()
        for bit, (pos, key, _lab) in enumerate(ordered):
            after = bool(mask & (1 << bit))
            cands = [(p, v) for p, v in monies
                     if (p > pos if after else p < pos) and p not in used
                     and abs(p - pos) <= 120]
            if not cands:
                return None
            p, v = (min(cands, key=lambda x: x[0]) if after
                    else max(cands, key=lambda x: x[0]))
            used.add(p)
            assign[key] = v
        free = [(p, v) for p, v in monies if p not in used]
        # Structural guard: a waterfall opens with the prior-period bar and
        # closes with the current-period bar, so exactly two tokens must be
        # left over and they must bracket every component token.  Without this
        # the label/value lists in the older decks throw up combinations that
        # balance by coincidence.
        if len(free) != 2:
            return None
        if not (free[0][0] < min(used) and free[1][0] > max(used)):
            return None
        if not check(assign, free[0][1], free[1][1]):
            return None
        return assign

    # The two pure conventions are tried first and trusted on their own, since
    # a whole chart transcribed one way and balancing exactly is convincing.
    for conv, mask in (("value-after-label", (1 << n) - 1),
                       ("value-before-label", 0)):
        a = try_mask(mask)
        if a is not None:
            return {norm(k): v for k, v in a.items()}, conv

    if n <= 10:
        solutions = {}
        for mask in range(1 << n):
            assign, used = {}, set()
            ok = True
            for bit, (pos, key, _lab) in enumerate(ordered):
                after = bool(mask & (1 << bit))
                cands = [(p, v) for p, v in monies
                         if (p > pos if after else p < pos) and p not in used]
                if not cands:
                    ok = False
                    break
                p, v = (min(cands, key=lambda x: x[0]) if after
                        else max(cands, key=lambda x: x[0]))
                used.add(p)
                assign[key] = v
            if not ok:
                continue
            free = [(p, v) for p, v in monies if p not in used]
            if len(free) != 2:
                continue
            if not (free[0][0] < min(used) and free[1][0] > max(used)):
                continue
            if check(assign, free[0][1], free[1][1]):
                sig = tuple(sorted(assign.items()))
                solutions[sig] = assign
        if len(solutions) == 1:
            assign = next(iter(solutions.values()))
            return {norm(k): v for k, v in assign.items()}, "label-adjacent"
        if len(solutions) > 1:
            return None   # ambiguous transcription: discarded, not guessed

    # convention C: a values list followed by a labels list (or vice versa)
    if len(monies) == len(ordered) + 2:
        vals = [v for _p, v in monies]
        for start_v, comp, end_v in ((vals[0], vals[1:-1], vals[-1]),
                                     (vals[-2], vals[:-2], vals[-1])):
            if len(comp) != len(ordered):
                continue
            assign = {norm(k): v for (_p, k, _l), v in zip(ordered, comp)}
            if check(assign, start_v, end_v):
                return assign, "parallel-list"
    return None


def norm(key):
    k = re.sub(r"\s+", "", key)
    return {"Volume/Mix": "Volume/Mix", "SA&G/R&D": "SA&G/R&D",
            "WarrantyCosts": "Warranty", "ProductionCosts": "Production Costs",
            "SpecialItems": "Special Items"}.get(k, k)


def clean_multiline(s):
    s = s.translate(ZW).replace(" ", " ")
    s = s.replace("&quot;", '"').replace("&amp;", "&").replace("&#39;", "'")
    s = s.replace("&gt;", ">").replace("&lt;", "<").replace("–", "-").replace("—", "-")
    return s


def main():
    res = {"mdna": [], "slides": []}
    fdir = os.path.join(CORPUS, "filings")
    for fn in sorted(os.listdir(fdir)):
        if fn.endswith(".md"):
            res["mdna"].extend(parse_filing(os.path.join(fdir, fn)))
    sdir = os.path.join(CORPUS, "slides")
    for fn in sorted(os.listdir(sdir)):
        if fn.endswith(".md"):
            res["slides"].extend(parse_slide(os.path.join(sdir, fn)))
    json.dump(res, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
