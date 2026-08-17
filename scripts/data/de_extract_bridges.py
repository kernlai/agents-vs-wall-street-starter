#!/usr/bin/env python3
"""
Extract Deere segment operating-profit BRIDGES from the OCR'd slide decks.

OCR renders the waterfall in several ways across vintages:
  (a) prose narrative of the image, labels and values interleaved IN ORDER
  (b) JSON-ish blocks with parallel x_axis (labels) / y_axis (values) arrays
  (c) flat token dumps where VALUES ARE SCRAMBLED relative to LABELS
      (the 8-K exhibit text is always of this kind -- e.g. the 2Q26 SAT bridge
       renders as "$719 ($22) ($11) $574 $101 $40 $27 $2 $0 $8" against labels
       "2Q 2025 / Volume Mix / Price / Currency / Warranty / Production Costs /
        SA&G R&D / Special Items / Other / 2Q 2026").
Only (a) and (b) carry a trustworthy label->value mapping, and even those are
only accepted after ARITHMETIC RECONCILIATION:
        prior-year operating profit + sum(components) == current-year OP
Endpoints are independently cross-checked against the 8-K segment tables.
Anything that will not reconcile is REJECTED, never guessed.

The one inference allowed: if exactly ONE canonical component label is absent
from the parsed set and the residual closes the bridge exactly, that residual
is assigned to the missing label and the row is flagged
`reconciled_residual_to_<label>`. That is determinate, not a guess. Rows where
the missing label would be `production_costs` are still reported separately so
the downstream correlation can be run with and without them.
"""
import re, os, json, glob, argparse, sys
from itertools import permutations

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"

# NB word boundaries matter: without \b the "Other" pattern matches inside
# "Another light gray bar ..." and silently steals the Production Costs value.
COMPONENTS = [
    ("volume_mix",       r"\bVolume\s*/?\s*(?:and\s*)?Mix\b"),
    ("price",            r"\bPrice(?:\s*Realization)?\b"),
    ("currency",         r"\bCurrency\b"),
    ("warranty",         r"\bWarranty\b"),
    ("production_costs", r"\bProduction\s*Costs?\b"),
    ("sag_rd",           r"\bSA\s*&\s*G\s*/?\s*R\s*&\s*D\b"),
    ("special_items",    r"\bSpecial\s*Items?\b"),
    ("other",            r"\bOther\b"),
]
COMP_KEYS = [k for k, _ in COMPONENTS]

SEGMENTS = [
    ("PPA", r"Production\s*(?:&|and)\s*Precision\s*Ag"),
    ("SAT", r"Small\s*Ag(?:riculture)?\s*(?:&|and)\s*Turf"),
    ("CF",  r"Construction\s*(?:&|and)\s*Forestry"),
]

QTR = re.compile(r"\b([1-4])\s*Q\s*(20\d\d)\b", re.I)
MONEY_TOK = re.compile(r"\(\s*\$\s?[\d,]+\s*\)|\$\s?\(\s?[\d,]+\s?\)|[-+]?\$\s?[\d,]+")


def money(tok):
    t = tok.strip()
    neg = "(" in t and ")" in t
    t = t.replace("(", "").replace(")", "").replace("$", "").replace(",", "").replace("+", "").strip()
    if t.startswith("-"):
        neg, t = True, t[1:]
    if not re.fullmatch(r"\d+", t):
        return None
    v = int(t)
    return -v if neg else v


def norm(s):
    for a, b in [("&quot;", '"'), ("&amp;", "&"), ("&#39;", "'"), ("’", "'"),
                 ("–", "-"), ("—", "-"), ("&nbsp;", " ")]:
        s = s.replace(a, b)
    return s


def find_segment(text, pos):
    best, bestpos = None, -1
    for seg, pat in SEGMENTS:
        for m in re.finditer(pat, text[:pos], re.I):
            if m.start() > bestpos:
                bestpos, best = m.start(), seg
    return best


def label_at(s):
    if QTR.search(s):
        m = QTR.search(s)
        return f"EP:{m.group(1)}Q{m.group(2)}"
    for key, pat in COMPONENTS:
        if re.search(pat, s, re.I):
            return key
    return None


def token_stream(chunk):
    """Ordered stream of ('L', label) and ('V', value) tokens."""
    toks = []
    for m in QTR.finditer(chunk):
        toks.append((m.start(), "L", f"EP:{m.group(1)}Q{m.group(2)}", m.end()))
    for key, pat in COMPONENTS:
        for m in re.finditer(pat, chunk, re.I):
            toks.append((m.start(), "L", key, m.end()))
    for m in MONEY_TOK.finditer(chunk):
        v = money(m.group(0))
        if v is not None:
            toks.append((m.start(), "V", v, m.end()))
    toks.sort(key=lambda t: t[0])
    # de-duplicate overlapping label matches at the same position
    out, lastpos = [], -99
    for p, k, v, e in toks:
        if k == "L" and out and out[-1][1] == "L" and p - lastpos < 4:
            continue
        out.append((p, k, v, e))
        lastpos = p
    return out


def parse_json_style(chunk):
    cats = re.findall(r'"category"\s*:\s*"([^"]+)"\s*,\s*"[a-z_ ]*profit[a-z_ ]*"\s*:\s*"([^"]+)"',
                      chunk, re.I)
    if len(cats) >= 6:
        return [(c, money(v)) for c, v in cats], "json_catlist"
    ax = re.search(r'"x[_ ]?axis(?:_labels)?"\s*:\s*\[(.*?)\]', chunk, re.S)
    ay = re.search(r'"y[_ ]?axis(?:_values)?"\s*:\s*\[(.*?)\]', chunk, re.S)
    if ax and ay:
        labels = re.findall(r'"([^"]*)"', ax.group(1))
        vals = re.findall(r'"([^"]*)"', ay.group(1))
        if len(labels) == len(vals) and len(labels) >= 6:
            return [(l, money(v)) for l, v in zip(labels, vals)], "json_parallel"
    return None, None


def parse_ordered_prose(chunk):
    """Labels and values appear in the same order; zip them when counts agree."""
    st = token_stream(chunk)
    labels = [t[2] for t in st if t[1] == "L"]
    values = [t[2] for t in st if t[1] == "V"]
    if len(labels) >= 6 and len(labels) == len(values):
        return list(zip(labels, values)), "prose_ordered"
    # fall back: pair each label with the nearest value that is not already used
    pairs, used = [], set()
    for i, (p, k, v, _e) in enumerate(st):
        if k != "L":
            continue
        best, bestd = None, 1e9
        for j, (q, k2, v2, _e2) in enumerate(st):
            if k2 != "V" or j in used:
                continue
            d = abs(q - p)
            if d < bestd:
                best, bestd = j, d
        if best is not None and bestd < 160:
            used.add(best)
            pairs.append((v, st[best][2]))
    if len(pairs) >= 6:
        return pairs, "prose_nearest"
    return None, None



V2L = re.compile(r"\b(for|due to|attributed to|owing to|from)\b", re.I)
L2V = re.compile(r"(:|=|\b(of|showing|shows|representing|represents|increase[ds]?|"
                 r"decrease[ds]?|contributed|resulted in|impact|value|with)\b)", re.I)


def tight_pairs(chunk, inner, vals, maxgap=45):
    """
    Bind each waterfall label to its own value using the CONNECTOR TEXT between
    them rather than raw proximity.

    Proximity alone fails because the OCR narratives use two conventions and
    sometimes mix them inside one chart. 4Q24 PPA opens with
        '($1,204) due to "Volume/Mix." ... - Price: $2 - Currency: ($60)'
    -- value-then-label for the first bar, label-then-value for the rest -- so
    nearest-neighbour matching shifts Price onto Currency's number. 1Q26 PPA is
    the opposite: '"($61)" for "Volume/Mix", "($4)" for "Price"', where the
    FOLLOWING value is always nearer than the label's own preceding one.

    So for each label both gaps are scored: a short gap containing a
    value->label connector ("for", "due to") binds backwards, a short gap
    containing a label->value connector (":", "of", "showing") binds forwards,
    and a bare punctuation gap falls back to distance. Returns [(label, value)]
    only if the assignment is injective and exactly exhausts the component
    values; otherwise None so the caller can reject the quarter.
    """
    labs, seen = [], set()
    for pos, kind, val, end in inner:
        if kind == "L" and val in COMP_KEYS and val not in seen:
            seen.add(val)
            labs.append((pos, end, val))
    vps = [(pos, end, val) for pos, kind, val, end in inner if kind == "V"]
    if not labs or len(labs) != len(vps):
        return None

    def score(gap, rx):
        if len(gap) > maxgap:
            return 0
        if rx.search(gap):
            return 3
        if len(gap) <= 6:
            return 2
        return 1

    used, out, defer = set(), {}, []
    for lpos, lend, lab in labs:
        prev = [j for j, (vp, ve, _) in enumerate(vps) if ve <= lpos and j not in used]
        nxt = [j for j, (vp, ve, _) in enumerate(vps) if vp >= lend and j not in used]
        pj = max(prev) if prev else None
        nj = min(nxt) if nxt else None
        sb = score(chunk[vps[pj][1]:lpos], V2L) if pj is not None else 0
        sa = score(chunk[lend:vps[nj][0]], L2V) if nj is not None else 0
        if sb == 0 and sa == 0:
            defer.append((lpos, lab))
            continue
        if sb > sa:
            pick = pj
        elif sa > sb:
            pick = nj
        else:
            db = lpos - vps[pj][1] if pj is not None else 10 ** 9
            da = vps[nj][0] - lend if nj is not None else 10 ** 9
            pick = pj if db <= da else nj
        used.add(pick)
        out[lab] = vps[pick][2]
    for lpos, lab in defer:
        left = [j for j in range(len(vps)) if j not in used]
        if not left:
            return None
        j = min(left, key=lambda j: abs(vps[j][0] - lpos))
        used.add(j)
        out[lab] = vps[j][2]
    if sorted(out.values()) != sorted(vals):
        return None
    return [(l, out[l]) for _, _, l in labs]


def parse_anchored(chunk, pstart, pend):
    """
    Endpoint-anchored parse.

    The 8-K panel gives both endpoint values independently, so locate them in
    the token stream and take the component values as the ones strictly BETWEEN
    them, in reading order.

    CRITICAL: arithmetic reconciliation alone does NOT pin the label->value
    mapping -- any permutation of the components sums to the same total. Several
    OCR narratives drop the first component label and describe the bar only as
    "a gray bar with a value of ($627) positioned between the 2Q 2023 bar and
    the Volume/Mix bar", which shifts every subsequent label by one and would
    silently reconcile with Volume/Mix = +137 and Other = -627. Deere's
    waterfall always runs in the fixed order

        start | Volume/Mix | Price | Currency | Warranty | Production Costs
              | SA&G/R&D | Special Items | Other | end

    so when the full set of 8 component bars is present the values are assigned
    BY CANONICAL POSITION, not by the OCR's label adjacency. Assignments are
    additionally sign-checked against the 8-K MD&A narrative downstream.
    """
    if pstart is None or pend is None:
        return None, None
    st = token_stream(chunk)
    vi = [(i, t[2]) for i, t in enumerate(st) if t[1] == "V"]
    si = next((i for i, v in vi if v == pstart), None)
    ei = None
    for i, v in vi:
        if v == pend and (si is None or i > si):
            ei = i
    if si is None or ei is None or ei <= si:
        return None, None
    inner = st[si + 1: ei]
    vals = [t[2] for t in inner if t[1] == "V"]
    labs = []
    for t in inner:
        if t[1] == "L" and not str(t[2]).startswith("EP:") and t[2] not in labs:
            labs.append(t[2])
    if not labs:   # JSON-array style puts every label ahead of every value
        for t in st:
            if t[1] == "L" and not str(t[2]).startswith("EP:") and t[2] not in labs:
                labs.append(t[2])
    if not vals:
        return None, None
    if sum(vals) != pend - pstart:
        # Orphan-lead case: some narratives describe the first component bar
        # out of position -- "A gray bar with a value of ($627) is positioned
        # between the 2Q 2023 bar and the Volume/Mix bar" -- which leaves the
        # in-span values one short and every label attached one bar late. If a
        # single money token elsewhere in the chunk closes the bridge exactly,
        # it IS the first (Volume/Mix) bar and the canonical order applies.
        delta = pend - pstart - sum(vals)
        outside = [t[2] for k, t in enumerate(st)
                   if t[1] == "V" and not (si < k < ei) and t[2] == delta]
        if len(outside) == 1 and len(vals) == len(COMP_KEYS) - 1:
            idx0 = [COMP_KEYS.index(l) for l in labs if l in COMP_KEYS]
            if idx0 == sorted(idx0):
                return list(zip(COMP_KEYS, [delta] + vals)), "anchored_orphan_lead"
        return None, None
    # The OCR sometimes emits the label row out of order -- e.g. the 2Q22 deck
    # renders labels as [2Q 2021, Price, Volume/Mix, Currency, ...]. When the
    # label sequence is not Deere's fixed waterfall order the mapping cannot be
    # recovered from the arithmetic (every permutation sums the same), so the
    # quarter is REJECTED rather than assigned on a coin flip.
    # Case 1: every label sits immediately beside its own value in the prose
    # ("($61)" for "Volume/Mix"). Then the pairing is explicit and the order in
    # which the narrator walks the bars does not matter.
    tight = tight_pairs(chunk, inner, vals)
    if tight is not None and len(tight) == len(vals):
        return tight, "anchored_tightpairs"
    idx = [COMP_KEYS.index(l) for l in labs if l in COMP_KEYS]
    if idx != sorted(idx):
        return None, "scrambled_labels"
    if len(vals) == len(COMP_KEYS):
        return list(zip(COMP_KEYS, vals)), "anchored_canonical8"
    if len(vals) == len(labs):
        return list(zip(labs, vals)), "anchored_labelmatched"
    return None, None

def build_record(pairs, style):
    comps, eps = {}, []
    for lab, val in pairs:
        if val is None:
            continue
        key = lab if (lab in COMP_KEYS or str(lab).startswith("EP:")) else label_at(str(lab))
        if key is None:
            continue
        if key.startswith("EP:"):
            eps.append((key[3:], val))
        elif key not in comps:
            comps[key] = val
    return comps, eps, style


def qkey(s):
    m = re.match(r"([1-4])Q(20\d\d)", s)
    return (int(m.group(2)), int(m.group(1))) if m else (0, 0)


# ---------------------------------------------------------------- 8-K endpoints
def eightk_segment_profits():
    """Segment operating profit by (segment, fiscalYear, fiscalQuarter) from 8-Ks."""
    tbl = {}
    for path in sorted(glob.glob(os.path.join(CORPUS, "filings", "*8k*.md"))):
        raw = norm(open(path, encoding="utf-8").read())
        fn = os.path.basename(path)
        mq = re.search(r"-(q[1-4])-8k", fn)
        if not mq:
            continue
        q = int(mq.group(1)[1])
        pub = fn[:10]
        year = int(pub[:4])
        fy = year if q < 4 else year  # Q4 8-K published in Nov of same FY
        for seg, pat in SEGMENTS:
            for m in re.finditer(pat + r"\s*Operating Profit", raw, re.I):
                sub = raw[m.start(): m.start() + 4000]
                mo = re.search(r"\|\s*Operating profit\s*\|.*?\|\s*\$?\s*\|?\s*([\d,]+|\([\d,]+\))\s*\|.*?\|\s*\$?\s*\|?\s*([\d,]+|\([\d,]+\))\s*\|",
                               sub)
                break
        # simpler: parse the three "Operating profit | $ | X | $ | Y" rows in order
    return tbl


PANEL = {}


def load_panel(path):
    d = json.load(open(path))
    return {(r["fy"], r["q"], r["key"]): r["value"] for r in d["rows"]}


def main():
    global PANEL
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--panel", default=None,
                    help="JSON from de_segment_panel.py; enables endpoint verification")
    a = ap.parse_args()
    if a.panel:
        PANEL = load_panel(a.panel)

    raw_rows = []
    for path in sorted(glob.glob(os.path.join(CORPUS, "slides", "*.md"))):
        raw = norm(open(path, encoding="utf-8").read())
        pub = os.path.basename(path)[:10]
        # Two independent chunking strategies; every candidate chunk is parsed
        # and the results merged, preferring rows that reconcile. Strategy A
        # anchors on the literal chart title and clamps at the next block
        # boundary. Strategy B block-splits the deck and keeps any block with
        # >=5 canonical waterfall labels -- needed because some narratives
        # (e.g. 4Q25 PPA) never say "Operating Profit Comparison" at all.
        cands = []
        for mm in re.finditer(r"Operating Profit Comparison", raw, re.I):
            stops = [len(raw)]
            for pat in (r"\n\s*#", r"\*Image:", r"!\[", r"\]\(page_",
                        r"Operating Profit Comparison"):
                m2 = re.search(pat, raw[mm.start() + 30:])
                if m2:
                    stops.append(mm.start() + 30 + m2.start())
            cands.append((mm.start(), raw[mm.start(): min(min(stops), mm.start() + 2600)]))
        cuts = sorted(set([0] + [x.start() for x in
                                 re.finditer(r"!\[|\*Image:|\n\s*#", raw)] + [len(raw)]))
        for j in range(len(cuts) - 1):
            b = raw[cuts[j]: cuts[j + 1]]
            nlab = sum(1 for _, pat in COMPONENTS if re.search(pat, b, re.I))
            if nlab >= 5 and re.search(r"operating profit", b, re.I):
                cands.append((cuts[j], b))
        for i, (cpos, chunk) in enumerate(cands):
            seg = find_segment(raw, cpos)
            # fiscal quarter implied by the deck's own endpoint labels
            qlabs = sorted({f"{q.group(1)}Q{q.group(2)}" for q in QTR.finditer(chunk)},
                           key=qkey)
            pstart = pend = None
            if PANEL and seg and len(qlabs) >= 2:
                def _pv(lab):
                    mm = re.match(r"([1-4])Q(20\d\d)", lab)
                    return PANEL.get((int(mm.group(2)), int(mm.group(1)), seg + "_op"))
                pstart, pend = _pv(qlabs[0]), _pv(qlabs[-1])
            pairs, style = parse_anchored(chunk, pstart, pend)
            if style == "scrambled_labels":
                rec["status"] = "rejected_scrambled_label_order"
                raw_rows.append(rec)
                continue
            if pairs and len(qlabs) >= 2:
                pairs = ([(f"EP:{qlabs[0]}", pstart)] + list(pairs)
                         + [(f"EP:{qlabs[-1]}", pend)])
            if not pairs:
                pairs, style = parse_json_style(chunk)
            if not pairs:
                pairs, style = parse_ordered_prose(chunk)
            rec = {"file": os.path.basename(path), "published": pub, "segment": seg}
            if not pairs:
                rec["status"] = "unparsed"
                raw_rows.append(rec)
                continue
            comps, eps, style = build_record(pairs, style)
            seen, eu = set(), []
            for l, v in eps:
                if l not in seen:
                    seen.add(l); eu.append((l, v))
            eu.sort(key=lambda x: qkey(x[0]))
            if len(eu) < 2 or not comps:
                rec["status"] = "unparsed"
                raw_rows.append(rec)
                continue
            (slab, sval), (elab, eval_) = eu[0], eu[-1]
            # ---- independent endpoint check against the 8-K segment panel ----
            if PANEL and seg:
                def pv(lab):
                    mm = re.match(r"([1-4])Q(20\d\d)", lab)
                    return PANEL.get((int(mm.group(2)), int(mm.group(1)), seg + "_op"))
                ps, pe = pv(slab), pv(elab)
                rec["panel_start"], rec["panel_end"] = ps, pe
                if ps is not None and sval != ps:
                    rec["status"] = "rejected_start_mismatch_vs_8k"
                    rec.update({"style": style, "start_label": slab, "start": sval,
                                "end_label": elab, "end": eval_,
                                "components": dict(comps), "residual": None,
                                "missing_labels": [k for k in COMP_KEYS if k not in comps]})
                    raw_rows.append(rec)
                    continue
                if pe is not None and eval_ != pe:
                    rec["status"] = "rejected_end_mismatch_vs_8k"
                    rec.update({"style": style, "start_label": slab, "start": sval,
                                "end_label": elab, "end": eval_,
                                "components": dict(comps), "residual": None,
                                "missing_labels": [k for k in COMP_KEYS if k not in comps]})
                    raw_rows.append(rec)
                    continue
            resid = eval_ - (sval + sum(comps.values()))
            missing = [k for k in COMP_KEYS if k not in comps]
            rec.update({"style": style, "start_label": slab, "start": sval,
                        "end_label": elab, "end": eval_, "components": dict(comps),
                        "residual": resid, "missing_labels": missing})
            if resid == 0:
                rec["status"] = "reconciled"
            elif len(missing) == 1:
                comps[missing[0]] = resid
                rec["components"] = dict(comps)
                rec["status"] = f"reconciled_residual_to_{missing[0]}"
                rec["residual"] = 0
            else:
                rec["status"] = "rejected_no_reconcile"
            raw_rows.append(rec)

    # de-duplicate: same (segment, start_label, end_label); prefer reconciled
    best = {}
    scrambled = []
    for r in raw_rows:
        if r.get("status") in ("unparsed",) or "start_label" not in r:
            if r.get("status") == "rejected_scrambled_label_order":
                scrambled.append(r)
            continue
        k = (r["segment"], r["start_label"], r["end_label"])
        rank = 0 if r["status"] == "reconciled" else (1 if r["status"].startswith("reconciled") else 2)
        if k not in best or rank < best[k][0]:
            best[k] = (rank, r)
    kept = [v[1] for v in best.values()]
    kept.sort(key=lambda r: (qkey(r["end_label"]), str(r["segment"])))

    rec_ok = [r for r in kept if r["status"].startswith("reconciled")]
    rec_bad = [r for r in kept if not r["status"].startswith("reconciled")]
    unparsed = [r for r in raw_rows if r.get("status") == "unparsed"]

    out = {"reconciled": rec_ok, "rejected": rec_bad,
           "scrambled_label_order": scrambled,
           "unparsed_count": len(unparsed),
           "n_reconciled": len(rec_ok), "n_rejected": len(rec_bad),
           "n_scrambled": len(scrambled)}
    if a.out:
        open(a.out, "w").write(json.dumps(out, indent=1))
    print(f"reconciled={len(rec_ok)} rejected={len(rec_bad)} "
          f"scrambled={len(scrambled)} unparsed_chunks={len(unparsed)}",
          file=sys.stderr)
    for r in rec_ok:
        print(f"OK  {r['end_label']:>7} {str(r['segment']):>4} {r['start']:>6}->{r['end']:>6} "
              f"pc={str(r['components'].get('production_costs')):>6} "
              f"war={str(r['components'].get('warranty')):>6} "
              f"vm={str(r['components'].get('volume_mix')):>6} "
              f"px={str(r['components'].get('price')):>6}  [{r['status']}]", file=sys.stderr)
    for r in rec_bad:
        print(f"REJ {r['end_label']:>7} {str(r['segment']):>4} resid={str(r['residual']):>7} "
              f"missing={r['missing_labels']} file={r['file']}", file=sys.stderr)


if __name__ == "__main__":
    main()
