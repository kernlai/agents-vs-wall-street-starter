"""Q3 FY2026 revenue bridge from Deere's own unchanged FY2026 segment guidance.

Corrects an error carried by two dealer agents, who both stated H1 FY2026 PPA was
running "-16% (Q1) and -14% (Q2)". Q1 FY2026 PPA was +3% (3,163 vs 3,067, Q1 10-Q
filings/2026-02-26__de-us-20260226-q1-10q__636995.md). H1 PPA is -8%, not -15%.
That error made the implied H2 look far easier than the guide actually requires.
"""
FY25 = {"PPA":17311.0, "SAT":10224.0, "CF":11382.0}          # FY2025 10-K
H1_26= {"PPA": 7666.0, "SAT": 5653.0, "CF": 6460.0}          # Q2 FY2026 10-Q, six months
H1_25= {"PPA": 8297.0, "SAT": 4742.0, "CF": 4941.0}
Q3_25= {"PPA": 4273.0, "SAT": 3025.0, "CF": 3059.0}
TOT_Q3_25 = 12018.0
OTHER_Q3_25 = TOT_Q3_25 - sum(Q3_25.values())                # FS + other revenues
GUIDE = {"PPA":(-0.10,-0.05), "SAT":(0.15,0.15), "CF":(0.20,0.20)}

print(f"Q3 FY2025 base: PPA {Q3_25['PPA']:.0f}  SAT {Q3_25['SAT']:.0f}  CF {Q3_25['CF']:.0f}  "
      f"FS/other {OTHER_Q3_25:.0f}  total {TOT_Q3_25:.0f}\n")

print("H1 FY2026 actual y/y:")
for s in FY25: print(f"  {s}: {H1_26[s]:,.0f} vs {H1_25[s]:,.0f} = {100*(H1_26[s]/H1_25[s]-1):+.1f}%")

print("\nWhat the unchanged FY2026 guide implies for H2, then for Q3:")
rows={}
for s,(lo,hi) in GUIDE.items():
    H2_25 = FY25[s]-H1_25[s]
    Q4_25 = H2_25 - Q3_25[s]
    out=[]
    for g in (lo,hi):
        FY26 = FY25[s]*(1+g)
        H2_26 = FY26 - H1_26[s]
        h2g = H2_26/H2_25 - 1
        out.append((g,FY26,H2_26,h2g,Q3_25[s]*(1+h2g)))
    rows[s]=out
    print(f"\n  {s}: FY25 {FY25[s]:,.0f}; H2 FY25 {H2_25:,.0f} (Q3 {Q3_25[s]:,.0f} + Q4 {Q4_25:,.0f})")
    for g,FY26,H2_26,h2g,q3 in out:
        print(f"    guide {g:+.0%} -> FY26 {FY26:,.0f}; H2 needs {H2_26:,.0f} = {h2g:+.1%} y/y; "
              f"Q3 at that rate = {q3:,.0f}")

print("\n" + "="*72)
print("TOTAL Q3 FY2026 REVENUE, segments at their guide-implied H2 rate")
for i,lab in [(0,"low end of PPA guide (-10%)"),(1,"high end of PPA guide (-5%)")]:
    ppa=rows["PPA"][i][4]; sat=rows["SAT"][0][4]; cf=rows["CF"][0][4]
    for oth_g,ol in [(-0.03,"FS/other -3%"),(0.0,"FS/other flat")]:
        oth=OTHER_Q3_25*(1+oth_g)
        tot=ppa+sat+cf+oth
        print(f"  {lab:30s} {ol:14s} -> PPA {ppa:,.0f} SAT {sat:,.0f} CF {cf:,.0f} oth {oth:,.0f} "
              f"= {tot:,.0f}  ({100*(tot/TOT_Q3_25-1):+.1f}% y/y)")

print("\nSensitivity: Q3 total if PPA lands X% y/y, SAT/CF at guide-implied H2 rates, FS/other flat")
sat=rows["SAT"][0][4]; cf=rows["CF"][0][4]; oth=OTHER_Q3_25
for p in (-0.20,-0.15,-0.12,-0.10,-0.075,-0.05,-0.025,0.0):
    ppa=Q3_25["PPA"]*(1+p); tot=ppa+sat+cf+oth
    print(f"  PPA {p:+6.1%} -> PPA {ppa:,.0f}  TOTAL {tot:,.0f}  ({100*(tot/TOT_Q3_25-1):+.1f}% y/y)")

print("\nCross-check vs the stated central case $12,350m and range $11,900-12,800m")
for name,tot in [("central",12350),("low",11900),("high",12800)]:
    implied = (tot - sat - cf - oth)/Q3_25["PPA"] - 1
    print(f"  {name:8s} {tot:,} -> implied PPA y/y = {implied:+.1%} (PPA ${Q3_25['PPA']*(1+implied):,.0f}m)")
