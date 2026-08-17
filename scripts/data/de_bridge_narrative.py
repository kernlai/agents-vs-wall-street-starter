#!/usr/bin/env python3
"""
Independent cross-check on the parsed bridge SIGNS.

The slide waterfall is one source; the 8-K MD&A sentence for the same segment
and quarter is a second, textual one:

  "Operating profit decreased due to lower shipment volumes and higher
   production costs, partially offset by price realization."

That sentence pins the SIGN of several bridge components without using any of
the numbers.  Drivers named in the main clause carry the sign of the verb
(decreased -> negative contribution); drivers after "partially offset by" carry
the opposite sign.  Comparing those expected signs with the parsed component
signs catches label swaps -- the one failure mode the arithmetic sum test is
blind to.

Exposes: expected_signs(filings_dir) -> {"2026Q2": {"PPA": {"volume_mix": -1,...}}}
stdlib only.
"""
import os
import re

SEGMAP = [
    (re.compile(r"^production\s+and\s+precision\s+ag", re.I), "PPA"),
    (re.compile(r"^small\s+ag(riculture)?\s+and\s+turf", re.I), "SAT"),
    (re.compile(r"^construction\s+and\s+forestry", re.I), "CF"),
    (re.compile(r"^agriculture\s+and\s+turf", re.I), "AT"),
]

DRIVERS = [
    ("volume_mix", r"shipment volumes|sales volumes|shipment volume"),
    ("price", r"price realization"),
    ("warranty", r"warranty"),
    ("production_costs", r"production costs"),
    ("sag_rd", r"selling, administrative|sa&g|research and development|r&d"),
    ("special_items", r"special item|employee-separation|impairment"),
    ("currency", r"currency|foreign[- ]currency|foreign exchange"),
]

SPLIT = re.compile(r"partially offset by|these (?:items|factors) were partially offset by",
                   re.I)


def expected_signs(filings_dir):
    out = {}
    for fn in sorted(os.listdir(filings_dir)):
        m = re.search(r"-(q[1-4])-", fn)
        if not m:
            continue
        fy, q = int(fn[:4]), int(m.group(1)[1])
        key = f"{fy}Q{q}"
        txt = open(os.path.join(filings_dir, fn), encoding="utf-8").read()
        txt = txt.replace("&amp;", "&").replace("​", "")
        for para in re.split(r"\n\s*\n", txt):
            para = " ".join(para.split())
            seg = None
            for pat, k in SEGMAP:
                if pat.match(para):
                    seg = k
                    break
            if not seg:
                continue
            mm = re.search(r"Operating profit\s+(decreased|increased|declined|rose|"
                           r"was down|was up|improved)(.*?)(?:\.\s|$)", para, re.I)
            if not mm:
                continue
            base = -1 if re.match(r"decreas|declin|was down", mm.group(1), re.I) else 1
            body = mm.group(2)
            parts = SPLIT.split(body)
            signs = {}
            for i, clause in enumerate(parts):
                s = base if i == 0 else -base
                for name, pat in DRIVERS:
                    if re.search(pat, clause, re.I):
                        signs.setdefault(name, s)
            if signs:
                out.setdefault(key, {}).setdefault(seg, signs)
    return out


if __name__ == "__main__":
    import json
    d = expected_signs("/Users/cor/Documents/projects/agents-vs-wall-street-starter/"
                       "challenge/offline-data/deere/filings")
    print(json.dumps({k: d[k] for k in sorted(d)[-6:]}, indent=1))
    print("quarters covered:", len(d))
