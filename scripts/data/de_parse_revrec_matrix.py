#!/usr/bin/env python3
"""
Parse Deere & Company ASC 606 revenue-recognition footnote tables
(segment x primary geographic market, and major product lines)
out of the offline filing corpus.

Corpus: challenge/offline-data/deere/filings/*.md
Output: data/deere/de_geo_segment_matrix.csv  (tidy long)

Standard library only. Emits a reconciliation report to stdout.

The corpus renders each footnote table in up to TWO ways in the same file:
  (a) a loose plain-text dump (no pipes), and
  (b) a markdown pipe table.
Both are parsed; blocks are keyed by (period, basis-segments, geography) and
cross-checked. Blocks whose rows/columns do not reconcile are reported, not
silently repaired.
"""

import csv
import os
import re
import sys
from collections import defaultdict, OrderedDict

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
FILINGS = os.path.join(CORPUS, "filings")
OUT_CSV = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_geo_segment_matrix.csv"

# ----------------------------------------------------------------------------
# normalisation
# ----------------------------------------------------------------------------
ZW = dict.fromkeys(map(ord, "​‌‍﻿­"), None)


def norm(s):
    s = s.translate(ZW)
    s = s.replace(" ", " ").replace("–", "-").replace("—", "-")
    s = s.replace("’", "'")
    return re.sub(r"[ \t]+", " ", s).strip()


NUM_RE = re.compile(r"\(?\$?\s?(\d[\d,]*)\)?")


def numbers(s):
    """All integer tokens on a line, left to right, as ints (parens = negative)."""
    out = []
    for m in re.finditer(r"(\()?\s*\$?\s*(\d[\d,]*)\s*(\))?", s):
        v = int(m.group(2).replace(",", ""))
        if m.group(1) and m.group(3):
            v = -v
        out.append(v)
    return out


def strip_row(line):
    """Row label + payload for either a pipe row or a plain-text row."""
    l = norm(line)
    if l.startswith("|"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        return cells
    return [l]


# ----------------------------------------------------------------------------
# dimension vocabularies
# ----------------------------------------------------------------------------
GEO_CANON = OrderedDict([
    ("United States", [r"^united\s*states$"]),
    ("Canada", [r"^canada$"]),
    ("Western Europe", [r"^western\s*europe$"]),
    ("Central Europe and CIS", [r"^central\s*europe\s*and\s*cis$"]),
    ("Latin America", [r"^latin\s*america$"]),
    ("Asia, Africa, Oceania, and Middle East",
     [r"^asia,?\s*africa,?\s*(australia,?\s*new\s*zealand|oceania),?\s*and\s*middle\s*east$",
      r"^asia,?\s*africa,?\s*australia,?\s*newzealand,?\s*and\s*middle\s*east$"]),
])
GEO_ORDER = list(GEO_CANON)


def geo_of(label):
    key = re.sub(r"[\s]+", " ", label.strip().rstrip(":").strip()).lower()
    key = key.replace("  ", " ")
    for canon, pats in GEO_CANON.items():
        for p in pats:
            if re.match(p, key):
                return canon
    # tolerate glued variants from the pdf->md conversion
    glued = re.sub(r"[^a-z]", "", key)
    table = {
        "unitedstates": "United States",
        "canada": "Canada",
        "westerneurope": "Western Europe",
        "centraleuropeandcis": "Central Europe and CIS",
        "latinamerica": "Latin America",
    }
    if glued in table:
        return table[glued]
    if glued.startswith("asiaafrica") and glued.endswith("middleeast"):
        return "Asia, Africa, Oceania, and Middle East"
    return None


# product line -> which segment columns carry a figure, per segment scheme
PL_OLD = OrderedDict([  # Agriculture & Turf / Construction & Forestry / Financial Services
    ("Large Agriculture", ["A&T"]),
    ("Small Agriculture", ["A&T"]),
    ("Turf", ["A&T"]),
    ("Construction", ["C&F"]),
    ("Compact Construction", ["C&F"]),
    ("Road Building", ["C&F"]),
    ("Forestry", ["C&F"]),
    ("Financial Products", ["A&T", "C&F", "FS"]),
    ("Other", ["A&T", "C&F"]),
])
PL_NEW = OrderedDict([  # PPA / SAT / CF / FS
    ("Production agriculture", ["PPA"]),
    ("Small agriculture", ["SAT"]),
    ("Turf", ["SAT"]),
    ("Construction", ["CF"]),
    ("Compact construction", ["CF"]),
    ("Roadbuilding", ["CF"]),
    ("Forestry", ["CF"]),
    ("Financial products", ["PPA", "SAT", "CF", "FS"]),
    ("Other", ["PPA", "SAT", "CF"]),
])


def pl_of(label, scheme):
    key = re.sub(r"[^a-z]", "", label.lower())
    src = PL_OLD if scheme == "old" else PL_NEW
    for name, spans in src.items():
        if re.sub(r"[^a-z]", "", name.lower()) == key:
            return name, spans
    return None, None


SEG_OLD = ["A&T", "C&F", "FS"]
SEG_NEW = ["PPA", "SAT", "CF", "FS"]

SEG_LABEL = {
    "A&T": "Agriculture and Turf",
    "C&F": "Construction and Forestry",
    "FS": "Financial Services",
    "PPA": "Production and Precision Ag",
    "SAT": "Small Ag and Turf",
    "CF": "Construction and Forestry",
}


def seg_header(line):
    """Return the segment scheme if this line is a column header row."""
    l = norm(line)
    flat = re.sub(r"[^A-Za-z&]", "", l)
    if "Total" not in l:
        return None
    if re.search(r"\bPPA\b", l) and re.search(r"\bSAT\b", l) and re.search(r"\bCF\b", l):
        return "new"
    if "Precision" in l and ("SmallAg" in flat or "Small" in l):
        return "new"
    if "AgricultureandTurf" in flat and "Construction" in l:
        return "old"
    if "AgricultureandTurf" in flat:
        return "old"
    if re.search(r"^Agriculture$", l) or l == "Agriculture":
        return None
    return None


# ----------------------------------------------------------------------------
# period markers
# ----------------------------------------------------------------------------
MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}

PERIOD_RE = re.compile(
    r"\b(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})")
# the pdf->md conversion sometimes wraps the header, dropping the year onto the
# next line, or drops the span word entirely ("Months Ended July 31, 2022")
PERIOD_NOYEAR_RE = re.compile(
    r"\b(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),[\s|]*$")
PERIOD_NOSPAN_RE = re.compile(
    r"(?:^|\|)\s*Months\s+Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})")
YEAR_HEAD_RE = re.compile(r"^\|?\s*(\d{4})\b")
QTR_WORD_RE = re.compile(
    r"In the (first|second|third|fourth) quarter of (\d{4}),?\s+the Company's revenue",
    re.I)

FY_END = {
    2019: "2019-11-03", 2020: "2020-11-01", 2021: "2021-10-31",
    2022: "2022-10-30", 2023: "2023-10-29", 2024: "2024-10-27",
    2025: "2025-11-02",
}
# quarter-end date -> (fiscal_year, fiscal_quarter). Built from period headers seen
# in the corpus; fiscal year is the year whose FY-end follows the date.
FY_BOUNDS = [(2019, "2018-10-29", "2019-11-03"), (2020, "2019-11-04", "2020-11-01"),
             (2021, "2020-11-02", "2021-10-31"), (2022, "2021-11-01", "2022-10-30"),
             (2023, "2022-10-31", "2023-10-29"), (2024, "2023-10-30", "2024-10-27"),
             (2025, "2024-10-28", "2025-11-02"), (2026, "2025-11-03", "2026-11-01")]


def fy_of(date_iso):
    for fy, a, b in FY_BOUNDS:
        if a <= date_iso <= b:
            return fy
    return None  # pre-ASC606 period header elsewhere in the filing; ignored


def iso(monthname, day, year):
    return "%04d-%02d-%02d" % (int(year), MONTHS[monthname], int(day))


MONTHS_TO_Q = {"Three": 1, "Six": 2, "Nine": 3, "Twelve": 4}


def period_from_header_parts(span, mon, day, year):
    d = iso(mon, day, year)
    fy = fy_of(d)
    if fy is None:
        return None
    return {"span": span, "period_end": d, "fy": fy, "cum_q": MONTHS_TO_Q[span]}


def period_from_header(m):
    span = m.group(1)
    d = iso(m.group(2), m.group(3), m.group(4))
    fy = fy_of(d)
    if fy is None:
        return None
    return {"span": span, "period_end": d, "fy": fy,
            "cum_q": MONTHS_TO_Q[span]}


QW = {"first": 1, "second": 2, "third": 3, "fourth": 4}

# ----------------------------------------------------------------------------
# block extraction
# ----------------------------------------------------------------------------


def parse_file(path):
    """Yield blocks: dicts with period, scheme, kind ('geo'|'pl'), rows, totals."""
    raw = open(path, encoding="utf-8").read()
    lines = raw.split("\n")
    is_10k = "10k" in os.path.basename(path)

    blocks = []
    period = None          # dict or None
    scheme = None
    pending_label = ""     # for wrapped row labels in plain-text dumps
    pending_period = None  # header wrapped across two lines
    cur = None             # current block being accumulated

    def close():
        nonlocal cur
        if cur and cur["rows"]:
            blocks.append(cur)
        cur = None

    window = []

    def window_scheme():
        joined = " ".join(window)
        flat = re.sub(r"[^A-Za-z&]", "", joined)
        if re.search(r"\bPPA\b", joined) and re.search(r"\bSAT\b", joined):
            return "new"
        if "Precision" in joined and "Total" in joined:
            return "new"
        if "AgricultureandTurf" in flat and "Total" in joined:
            return "old"
        return None

    for ln, line in enumerate(lines, 1):
        l = norm(line)
        window.append(l)
        if len(window) > 10:
            window.pop(0)
        if not l:
            pending_label = ""
            continue

        # --- period markers -------------------------------------------------
        # a header wrapped across two lines: finish it with the year that
        # opens this line
        if pending_period is not None:
            ym = YEAR_HEAD_RE.match(l)
            if ym:
                span, mon, day = pending_period
                pending_period = None
                close()
                period = period_from_header_parts(span, mon, day, ym.group(1))
                s = seg_header(l)
                if s:
                    scheme = s
                pending_label = ""
                continue
            pending_period = None

        m = PERIOD_NOYEAR_RE.search(l)
        if m:
            pending_period = (m.group(1), m.group(2), m.group(3))
            continue

        if is_10k and re.fullmatch(r"\d{4}", l):
            fy = int(l)
            if fy in FY_END:
                close()
                period = {"span": "Twelve", "period_end": FY_END[fy],
                          "fy": fy, "cum_q": 4}
                pending_label = ""
                continue

        m = PERIOD_RE.search(l)
        if m:
            close()
            period = period_from_header(m)
            pending_label = ""
            # a header line can also carry the segment scheme
            s = seg_header(l)
            if s:
                scheme = s
            continue
        m = PERIOD_NOSPAN_RE.search(l)
        if m:
            close()
            d = iso(m.group(1), m.group(2), m.group(3))
            fy = fy_of(d)
            period = ({"span": "Unknown", "period_end": d, "fy": fy, "cum_q": None}
                      if fy else None)
            s = seg_header(l)
            if s:
                scheme = s
            pending_label = ""
            continue

        m = QTR_WORD_RE.search(l)
        if m:
            close()
            q = QW[m.group(1).lower()]
            fy = int(m.group(2))
            period = {"span": "Three", "period_end": None, "fy": fy, "cum_q": 1,
                      "explicit_q": q}
            pending_label = ""
            continue

        # --- segment header -------------------------------------------------
        s = seg_header(l)
        if s:
            close()
            scheme = s
            pending_label = ""
            continue

        is_pipe = l.startswith("|")
        if is_pipe:
            cells = strip_row(line)
            label = norm(cells[0]).rstrip(":").strip()
            payload = " ".join(cells[1:])
        else:
            # plain-text dump: label is everything before the first numeral
            m2 = re.search(r"\d", l)
            if m2:
                # back up over a leading "$" attached to the first number
                cut = m2.start()
                while cut > 0 and l[cut - 1] in "$ ":
                    cut -= 1
                label = l[:cut].rstrip(":").strip()
                payload = l[cut:]
            else:
                label = l.rstrip(":").strip()
                payload = ""
            cells = [label, payload]

        # --- bare fiscal-year marker inside a 10-K table ---------------------
        if is_10k:
            m = re.match(r"^(20\d\d)$", label)
            if m:
                close()
                fy = int(m.group(1))
                if fy in FY_END:
                    period = {"span": "Twelve", "period_end": FY_END[fy],
                              "fy": fy, "cum_q": 4}
                    pending_label = ""
                    continue
            # "2019 Primary geographic" style merged cell
            m = re.match(r"^(20\d\d)\s+Primary geograp", label)
            if m and scheme:
                close()
                fy = int(m.group(1))
                if fy in FY_END:
                    period = {"span": "Twelve", "period_end": FY_END[fy],
                              "fy": fy, "cum_q": 4}
                    pending_label = ""
                    continue

        if re.match(r"^Primary geograp", label, re.I):
            close()
            scheme = window_scheme() or scheme
            if period and scheme:
                cur = {"kind": "geo", "period": period, "scheme": scheme,
                       "rows": OrderedDict(), "totals": None, "file": path,
                       "line": ln, "pipe": is_pipe}
            pending_label = ""
            continue
        if re.match(r"^Major product line", label, re.I):
            close()
            if period and scheme:
                cur = {"kind": "pl", "period": period, "scheme": scheme,
                       "rows": OrderedDict(), "totals": None, "file": path,
                       "line": ln, "pipe": is_pipe}
            pending_label = ""
            continue
        if re.match(r"^(Timing of revenue|Revenue recognized)", label, re.I):
            close()
            pending_label = ""
            continue

        if cur is None:
            pending_label = ""
            continue

        # the pdf->md conversion frequently wraps "Primary geographic markets:"
        # across rows, leaving "markets: United" / "States" fragments
        mk = re.match(r"^markets?:\s*(.*)$", label, re.I)
        if mk:
            label = mk.group(1).strip()
            if not label and not vals:
                continue

        vals = numbers(payload)

        # total row terminates the block
        if re.match(r"^total$", label, re.I):
            cur["totals"] = vals
            close()
            pending_label = ""
            continue

        if cur["kind"] == "geo":
            full = (pending_label + " " + label).strip() if pending_label else label
            g = geo_of(full)
            if g is None:
                # maybe a wrapped label line with no numbers -> buffer it
                if not vals:
                    pending_label = full
                else:
                    cur.setdefault("unparsed", []).append((full, vals))
                continue
            pending_label = ""
            cur["rows"][g] = vals
        else:
            name, spans = pl_of(label, cur["scheme"])
            if name is None:
                if not vals:
                    pending_label = label
                else:
                    cur.setdefault("unparsed", []).append((label, vals))
                continue
            pending_label = ""
            cur["rows"][name] = (spans, vals)

    close()
    return blocks


# ----------------------------------------------------------------------------
# validation
# ----------------------------------------------------------------------------

def validate_geo(b):
    segs = SEG_OLD if b["scheme"] == "old" else SEG_NEW
    n = len(segs)
    problems = []
    if set(b["rows"]) != set(GEO_ORDER):
        problems.append("missing geographies: %s" %
                        sorted(set(GEO_ORDER) - set(b["rows"])))
    for g, v in b["rows"].items():
        if len(v) != n + 1:
            problems.append("%s: got %d values, expected %d" % (g, len(v), n + 1))
        elif sum(v[:n]) != v[n]:
            problems.append("%s: row sum %d != stated %d" % (g, sum(v[:n]), v[n]))
    if b["totals"] is None or len(b["totals"]) != n + 1:
        problems.append("total row missing/malformed: %r" % (b["totals"],))
    elif not problems:
        for i, s in enumerate(segs):
            col = sum(v[i] for v in b["rows"].values())
            if col != b["totals"][i]:
                problems.append("%s column sum %d != stated %d" %
                                (s, col, b["totals"][i]))
        col = sum(v[n] for v in b["rows"].values())
        if col != b["totals"][n]:
            problems.append("Total column sum %d != stated %d" % (col, b["totals"][n]))
    return problems


def validate_pl(b):
    segs = SEG_OLD if b["scheme"] == "old" else SEG_NEW
    n = len(segs)
    problems = []
    for name, (spans, v) in b["rows"].items():
        if len(v) != len(spans) + 1:
            problems.append("%s: got %d values, expected %d" %
                            (name, len(v), len(spans) + 1))
        elif sum(v[:-1]) != v[-1]:
            problems.append("%s: row sum %d != stated %d" %
                            (name, sum(v[:-1]), v[-1]))
    if b["totals"] is None or len(b["totals"]) != n + 1:
        problems.append("total row missing/malformed")
    elif not problems:
        for i, s in enumerate(segs):
            col = sum(v[spans.index(s)] for spans, v in b["rows"].values() if s in spans)
            if col != b["totals"][i]:
                problems.append("%s column sum %d != stated %d" %
                                (s, col, b["totals"][i]))
    return problems


def repair_pl(b):
    """Recover product-line rows whose cells the pdf->md conversion merged.

    Only applied when the block still carries a well-formed stated total row.
    Unknown cells are solved against the column residuals; the solution must be
    unique as a multiset and every multi-segment row total must itself appear
    among the stray numbers. Order within a merged cell is taken to follow the
    order the product lines are printed in. Returns True if repaired.
    """
    import itertools
    segs = SEG_OLD if b["scheme"] == "old" else SEG_NEW
    n = len(segs)
    if not b["totals"] or len(b["totals"]) != n + 1:
        return False
    vocab = PL_OLD if b["scheme"] == "old" else PL_NEW

    good, bad_rows = OrderedDict(), []
    for name, (spans, v) in b["rows"].items():
        if len(v) == len(spans) + 1 and sum(v[:-1]) == v[-1]:
            good[name] = (spans, v)
        else:
            bad_rows.append((name, v))

    # stray numbers: from over-long rows and from rows whose label was merged
    pool = []
    missing_names = []
    for name, v in bad_rows:
        missing_names.append(name)
        pool.extend(v)
    def squash(s):
        return re.sub(r"[^a-z]", "", s.lower())

    for lab, v in b.get("unparsed", []):
        pool.extend(v)
        for cand in vocab:
            if squash(cand) in squash(lab) \
                    and cand not in good and cand not in missing_names:
                missing_names.append(cand)
    if not missing_names or not pool:
        return False
    # keep printing order
    missing_names = [c for c in vocab if c in missing_names]
    cands = []
    for v in pool:
        if v not in cands:
            cands.append(v)

    residual = {}
    for i, s in enumerate(segs):
        residual[s] = b["totals"][i] - sum(
            v[spans.index(s)] for spans, v in good.values() if s in spans)

    per_seg = {}
    for s in segs:
        unknowns = [nm for nm in missing_names if s in vocab[nm]]
        if not unknowns:
            if residual[s] != 0:
                return False
            continue
        sols = [c for c in itertools.product(cands, repeat=len(unknowns))
                if sum(c) == residual[s]]
        # collapse permutations: keep the one ordered as the values first appear
        uniq = {tuple(sorted(c)) for c in sols}
        if len(uniq) != 1:
            return False
        multiset = sorted(uniq.pop())
        ordered = sorted(multiset, key=lambda v: cands.index(v))
        per_seg[s] = dict(zip(unknowns, ordered))

    out = OrderedDict()
    for nm in missing_names:
        spans = vocab[nm]
        vals = [per_seg[s][nm] for s in spans]
        tot = sum(vals)
        if len(spans) > 1 and tot not in pool:
            return False
        out[nm] = (spans, vals + [tot])

    merged = OrderedDict()
    for nm in vocab:
        if nm in good:
            merged[nm] = good[nm]
        elif nm in out:
            merged[nm] = out[nm]
    b["rows"] = merged
    b.pop("unparsed", None)
    b["repaired"] = sorted(out)
    return True


def main():
    files = sorted(f for f in os.listdir(FILINGS) if f.endswith(".md"))
    all_blocks = []
    for f in files:
        p = os.path.join(FILINGS, f)
        txt = open(p, encoding="utf-8").read()
        if "Central Europe" not in txt:
            continue
        for b in parse_file(p):
            b["src"] = f
            problems = validate_geo(b) if b["kind"] == "geo" else validate_pl(b)
            b["problems"] = problems
            all_blocks.append(b)

    for b in all_blocks:
        per = b["period"]
        tag = "%s/%s FY%s %s %s" % (b["kind"], b["scheme"], per["fy"],
                                    per["span"], per["period_end"])
        status = "OK " if not b["problems"] else "BAD"
        print("%s %-52s %-58s line %d %s" %
              (status, tag, b["src"], b["line"], "pipe" if b["pipe"] else "text"))
        for p in b["problems"][:4]:
            print("      -", p)
    print("\nblocks: %d, clean: %d" %
          (len(all_blocks), sum(1 for b in all_blocks if not b["problems"])))
    return all_blocks


if __name__ == "__main__":
    main()
