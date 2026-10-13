#!/usr/bin/env python3
"""QA for the 1998 Luleå landsting source-specific layout (SCB SOS table 3)."""
import csv
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PARTIES = ["m", "c", "fp", "kd", "mp", "s", "v", "ovr"]

def check(path):
    errors=[]
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader=csv.DictReader(fh)
        rows=list(reader)
    if not rows:
        return ["Tom datafil"]
    for i,row in enumerate(rows,2):
        label=f"rad {i} {row.get('valdistrikt', '')}"
        if row["kommunkod"]!="2580" or row["valar"]!="1998" or row["valtyp"]!="region":
            errors.append(label+": fel geografisk/valmässig avgränsning")
            continue
        try:
            rostberattigade=int(row["rostberattigade"])
            rostande=int(row["rostande"])
            giltiga=int(row["giltiga"])
            party_sum=sum(int(row[k]) for k in PARTIES)
            turnout=Decimal(row["valdeltagande_procent"].replace(",","."))
        except (ValueError, KeyError) as exc:
            errors.append(label+": saknat eller ogiltigt numeriskt fält "+str(exc))
            continue
        if party_sum != giltiga:
            errors.append(f"{label}: partisumma {party_sum} != giltiga {giltiga}")
        if giltiga > rostande:
            errors.append(f"{label}: giltiga överstiger röstande")
        calc=(Decimal(rostande)*100/Decimal(rostberattigade)).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP)
        if calc!=turnout:
            errors.append(f"{label}: deltagande {turnout} != {calc}")
    return errors

if __name__=="__main__":
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/valresultat/1998/landsting_lulea_2580_utdrag_preliminart.csv")
    issues=check(path)
    if issues:
        print("\n".join(issues))
        sys.exit(1)
    print("Godkända aritmetiska kontroller (ej liktydigt med kontrollerad originaltranskription)")
