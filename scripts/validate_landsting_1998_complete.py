#!/usr/bin/env python3
"""Full SCB 1998 landstingsval constituency/municipality reconciliation for Luleå."""
import csv
import sys
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
P=("m","c","fp","kd","mp","s","v","ovr")
EXPECTED_POST={"rostande":304,"giltiga":290,"m":51,"c":11,"fp":21,"kd":16,"mp":17,"s":90,"v":60,"ovr":24}
FIELDS=("rostberattigade","utlandska_medborgare","rostande","giltiga")+P

def validate(path):
    with open(path,encoding="utf-8-sig",newline="") as fh: rows=list(csv.DictReader(fh))
    ds=[r for r in rows if r["radtyp"]=="valdistrikt"]
    totals=[r for r in rows if r["radtyp"]=="kommun_summa"]
    errors=[]
    if len(ds)!=56: errors.append(f"expected 56 districts, got {len(ds)}")
    if len(totals)!=1: errors.append(f"expected 1 municipality total, got {len(totals)}")
    if len({r['valdistrikt'] for r in ds})!=len(ds): errors.append("duplicate district name")
    if any(r["kommunkod"]!="2580" or r["valtyp"]!="region" or r["valar"]!="1998" for r in rows):
        errors.append("wrong geography/election")
    try:
        for r in rows:
            if sum(int(r[p]) for p in P)!=int(r["giltiga"]):
                errors.append(f"{r['valdistrikt']}: party sum mismatch")
            pct=(Decimal(r["rostande"])*100/Decimal(r["rostberattigade"])).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP)
            if pct!=Decimal(r["valdeltagande_procent"].replace(",",".")):
                errors.append(f"{r['valdistrikt']}: turnout mismatch")
        if len(totals)==1:
            total=totals[0]
            for k in FIELDS:
                residual=int(total[k])-sum(int(r[k]) for r in ds)
                expected=EXPECTED_POST.get(k,0)
                if residual!=expected:
                    errors.append(f"{k}: municipality minus districts = {residual}, expected {expected}")
    except (ValueError, KeyError, ZeroDivisionError) as exc:
        errors.append(f"missing or invalid value: {exc}")
    return errors

if __name__=="__main__":
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/valresultat/1998/landsting_lulea_2580_utdrag_preliminart.csv")
    issues=validate(path)
    if issues:
        print("\n".join(issues))
        sys.exit(1)
    print("PASS: 56 districts, parties, turnout, and every SCB municipality/postal-vote reconciliation")
    print("Still subject to independent visual transcription review")
