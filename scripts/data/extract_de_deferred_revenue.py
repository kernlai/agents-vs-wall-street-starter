#!/usr/bin/env python3
"""
Pull the contract-liability / remaining-performance-obligation sentences out of
Deere's revenue-recognition note.  These are the only place the filings put a
number on precision-guidance / telematics / information-enabled-solutions
subscription revenue that has been invoiced but not yet recognised.
Standard library only.
"""
import re, glob, os, json

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"
MONTHS = ("January February March April May June July August September "
          "October November December").split()
MN = {m: i + 1 for i, m in enumerate(MONTHS)}

DEF_RE = re.compile(
    r"deferred revenue received,? but not recognized in revenue,?"
    r"(?: including extended warranty premiums[^,]*,)? was "
    r"((?:\$[\d,]+(?: million)?(?:,\s*|,?\s*and\s*)?)+)\s*at\s*([^.]+?)\.", re.I)
DATE_RE = re.compile(r"(%s)\s+(\d{1,2}),?\s*(\d{4})" % "|".join(MONTHS))
UPO_RE = re.compile(
    r"unsatisfied performance obligations for contracts with an original duration "
    r"greater than one year was \$([\d,]+)\s*(?:million\s*)?(?:at|as of)\s*(%s)\s+(\d{1,2}),?\s*(\d{4})"
    % "|".join(MONTHS), re.I)

def clean(s):
    for z in ["​", " ", " ", "﻿"]:
        s = s.replace(z, " ")
    return re.sub(r"\s+", " ", s)

def main():
    defr, upo = {}, {}
    for f in sorted(glob.glob(CORPUS + "/*.md")):
        t = clean(open(f, encoding="utf-8").read())
        base = os.path.basename(f)
        for m in DEF_RE.finditer(t):
            amts = [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", m.group(1))]
            dates = [f"{int(y):04d}-{MN[mo]:02d}-{int(d):02d}"
                     for mo, d, y in DATE_RE.findall(m.group(2))]
            if len(amts) == len(dates):
                for a, d in zip(amts, dates):
                    defr.setdefault(d, (a, base))
                    if defr[d][0] != a:
                        print("  ! deferred revenue conflict", d, defr[d], a, base)
        for m in UPO_RE.finditer(t):
            d = f"{int(m.group(4)):04d}-{MN[m.group(2)]:02d}-{int(m.group(3)):02d}"
            v = int(m.group(1).replace(",", ""))
            upo.setdefault(d, (v, base))
    print("deferred revenue (contract liability), USDm, at balance-sheet date")
    for d in sorted(defr):
        print(" ", d, defr[d][0])
    print("remaining performance obligations >1yr, USDm")
    for d in sorted(upo):
        print(" ", d, upo[d][0])
    json.dump({"deferred": defr, "upo": upo},
              open("/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/de_deferred.json", "w"), indent=1)

if __name__ == "__main__":
    main()
