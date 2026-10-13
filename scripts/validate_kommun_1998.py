#!/usr/bin/env python3
"""SCB 1998 Luleå municipal election: strict arithmetic and source-total checks."""
import csv
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import sys

PARTIES=("m","c","fp","kd","mp","s","v","ovr")
FIELDS=("rostberattigade","utlandska_medborgare","rostande","giltiga")+PARTIES
EXPECTED={
"Norra":(29,[27311,1070,21642,21122,3136,1433,1160,952,1084,9041,3900,416],
          [0,0,151,146,29,6,7,4,13,48,34,5]),
"Södra":(27,[28413,747,22917,22387,4396,1322,1468,1275,1156,8935,3583,252],
          [0,0,159,150,29,9,13,11,13,45,29,1])
}
COMMUNE=(55724,1817,44869,43805,7590,2770,2648,2242,2266,18069,7546,674)
def audit(path):
    with open(path,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    errors=[]
    if len(rows)!=56 or len(set((r["valkrets"],r["valdistrikt"]) for r in rows))!=56:
        errors.append("56 unique districts required")
    if any(r["valar"]!="1998" or r["valtyp"]!="kommun" or r["kommunkod"]!="2580" or r["radtyp"]!="valdistrikt" for r in rows):
        errors.append("geography/election mismatch")
    if dict(Counter(r["tryckt_sida"] for r in rows))!={"279":18,"280":34,"281":4}:
        errors.append("source page distribution differs")
    for r in rows:
        try:
            if sum(int(r[k]) for k in PARTIES)!=int(r["giltiga"]):
                errors.append("parties: "+r["valdistrikt"])
            x=(Decimal(r["rostande"])*100/Decimal(r["rostberattigade"])).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP)
            if x!=Decimal(r["valdeltagande_procent"].replace(",",".")):
                errors.append("turnout: "+r["valdistrikt"])
        except (ValueError, KeyError, ZeroDivisionError) as err:
            errors.append(str(err))
    combined=[0]*len(FIELDS)
    for constituency,(count,district_sums,postal_residuals) in EXPECTED.items():
        group=[r for r in rows if r["valkrets"]==constituency]
        if len(group)!=count: errors.append("district count "+constituency)
        for i,k in enumerate(FIELDS):
            s=sum(int(r[k]) for r in group)
            if s!=district_sums[i]: errors.append(f"{constituency} {k}: {s} != {district_sums[i]}")
            combined[i]+=s+postal_residuals[i]
    for i,k in enumerate(FIELDS):
        if combined[i]!=COMMUNE[i]: errors.append(f"municipality {k}: {combined[i]} != {COMMUNE[i]}")
    return errors

if __name__=="__main__":
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/valresultat/1998/kommun_lulea_2580_distrikt.csv")
    errs=audit(path)
    if errs:
        for e in errs: print("FAIL",e)
        raise SystemExit(1)
    print("PASS 1998 kommun: 56 districts, parties, turnout, Norra/Sodra and municipal postal reconciliations")
    print("Independent second reading of original remains pending")
