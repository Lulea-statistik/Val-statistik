#!/usr/bin/env python3
"""Audit Luleå 1998 riksdag, SCB SOS del 1 table 10 pp. 266-268."""
import csv,sys
from decimal import Decimal,ROUND_HALF_UP
from collections import Counter
F=("rostberattigade","rostande","giltiga","ogiltiga","m","c","fp","kd","mp","s","v","ovr")
P=("m","c","fp","kd","mp","s","v","ovr")
TOTAL=(54157,44998,44385,613,6924,1815,1919,3165,1939,19631,8470,522)
POST=(0,376,367,9,86,9,17,24,33,118,77,3)
def run(path):
 with open(path,encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
 errors=[]
 if len(rows)!=56 or len({r["valdistrikt"] for r in rows})!=56: errors.append("expected 56 unique districts")
 if Counter(r["tryckt_sida"] for r in rows)!=Counter({"266":20,"267":36}): errors.append("wrong printed page counts")
 for r in rows:
  name=r["valdistrikt"]
  if (r["valar"],r["valtyp"],r["kommunkod"])!=("1998","riksdag","2580"):errors.append("wrong scope "+name)
  try:
   if sum(int(r[p]) for p in P)!=int(r["giltiga"]):errors.append("parties "+name)
   if int(r["rostande"])!=int(r["giltiga"])+int(r["ogiltiga"]):errors.append("ballots "+name)
   val=(Decimal(r["rostande"])*100/Decimal(r["rostberattigade"])).quantize(Decimal(".1"),rounding=ROUND_HALF_UP)
   if val!=Decimal(r["valdeltagande_procent"].replace(",",".")):errors.append("turnout "+name)
  except (KeyError,ValueError,ArithmeticError) as ex:errors.append(name+" "+str(ex))
 for k,tot,post in zip(F,TOTAL,POST):
  v=sum(int(r[k]) for r in rows)
  if v+post!=tot: errors.append(f"total {k}: {v}+{post}!={tot}")
 if sum(POST[4:])!=POST[2]: errors.append("postal party breakdown")
 return errors
if __name__=="__main__":
 path=sys.argv[1] if len(sys.argv)>1 else "data/valresultat/1998/riksdag_lulea_2580_distrikt.csv"
 e=run(path)
 if e:
  print("\n".join("FAIL "+v for v in e));sys.exit(1)
 print("PASS: 56 Luleå districts, vote and turnout calculations, complete SCB municipal and postal reconciliation")
 print("Independent second source reading pending.")
