#!/usr/bin/env python3
"""Strict audit of SCB SOS 1998 tabell 3, Luleå 2580.
No district is marked independently verified by arithmetic checks alone.
"""
import csv
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

FIELDS = ("rostberattigade","utlandska_medborgare","rostande","giltiga","m","c","fp","kd","mp","s","v","ovr")
PARTIES = ("m","c","fp","kd","mp","s","v","ovr")
EXPECTED_POST = dict(zip(FIELDS, (0,0,304,290,51,11,21,16,17,90,60,24)))
EXPECTED_PAGES = {"276":6,"277":38,"278":12}

def audit(main_path, postal_path):
    with open(main_path,encoding="utf-8-sig",newline="") as f: all_rows=list(csv.DictReader(f))
    with open(postal_path,encoding="utf-8-sig",newline="") as f: postal=list(csv.DictReader(f))
    errors=[]
    ds=[r for r in all_rows if r["radtyp"]=="valdistrikt"]
    totals=[r for r in all_rows if r["radtyp"]=="kommun_summa"]
    if len(ds)!=56 or len(totals)!=1: errors.append("expected 56 district rows and one municipality total")
    if len(postal)!=1: errors.append("expected one separate postal remainder row")
    if len(set(r["valdistrikt"] for r in ds))!=len(ds): errors.append("duplicate district names")
    if dict(Counter(r["tryckt_sida"] for r in ds)) != EXPECTED_PAGES: errors.append("incorrect distribution of source page references")
    if any(r["valar"]!="1998" or r["valtyp"]!="region" or r["kommunkod"]!="2580" for r in all_rows+postal):
        errors.append("wrong election/year/municipality")
    if any(r["granskningsstatus"]=="verifierad" for r in ds):
        errors.append("independent review has not been recorded")
    try:
        for r in all_rows:
            if sum(int(r[k]) for k in PARTIES)!=int(r["giltiga"]):
                errors.append("party mismatch: "+r["valdistrikt"])
            pct=(Decimal(r["rostande"])*100/Decimal(r["rostberattigade"])).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP)
            if pct != Decimal(r["valdeltagande_procent"].replace(",",".")):
                errors.append("turnout mismatch: "+r["valdistrikt"])
        if len(totals)==1 and len(postal)==1:
            total=totals[0]; p=postal[0]
            for col in FIELDS:
                remainder=int(total[col])-sum(int(r[col]) for r in ds)
                if remainder != EXPECTED_POST[col]: errors.append(f"{col}: remainder {remainder}, expected {EXPECTED_POST[col]}")
                if col in p and p[col] and remainder != int(p[col]): errors.append(f"{col}: mismatch with explicit postal remainder")
            if sum(int(p[k]) for k in PARTIES)!=int(p["giltiga"]):
                errors.append("post remainder party mismatch")
    except (KeyError,ValueError,ArithmeticError) as err: errors.append(str(err))
    return errors

if __name__=="__main__":
    args=sys.argv[1:]
    if len(args)!=2: raise SystemExit("usage: audit_1998.py DISTRICTS.csv POSTAL.csv")
    issues=audit(*args)
    if issues:
        for i in issues: print("FAIL:",i)
        raise SystemExit(1)
    print("PASS: complete arithmetic, Luleå scope, page distribution, and postal reconciliation")
    print("Independent visual transcription review remains pending.")
