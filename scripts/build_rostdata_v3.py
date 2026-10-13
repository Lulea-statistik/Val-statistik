#!/usr/bin/env python3
"""Convert the uploaded 'Röstdata v3' Excel table (exported to semicolon CSV) into public vote data.
No fabricated geographical joins; area names are matched in the browser against historical polygons.
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/"data/import/rostdata_v3.csv"
target=ROOT/"docs/data/roster"
target.mkdir(parents=True,exist_ok=True)
REQUIRED=["Område","Röstberättigade","VDT","med giltiga valsedlar",
          "med ogiltiga valsedlar","OG varav blanka","OG varav ÖVR ogiltiga",
          "OG varav EGEJ, ej anmälda part.","Val","År"]
with source.open(encoding="utf-8-sig",newline="") as f:
    reader=csv.DictReader(f,delimiter=";")
    if not reader.fieldnames or any(x not in reader.fieldnames for x in REQUIRED):
        raise ValueError("Missing vote table columns: "+str(reader.fieldnames))
    rows=list(reader)
for row in rows:
    if row["Val"] not in ("KF","RS"):
        raise ValueError("Unexpected vote type "+str(row["Val"]))
    if not row["År"].isdigit():
        raise ValueError("Unexpected election year "+str(row["År"]))
    for key in REQUIRED[1:8]:
        x=row[key]
        if x:
            try:
                num=float(x.replace(",","."))
                if num<0:raise ValueError
            except ValueError:
                raise ValueError("Bad value "+str((row["År"],row["Område"],key,x)))
        row[key]=float(x.replace(",",".")) if x and ("," in x or "." in x) else int(x) if x else None
    row["År"]=int(row["År"])
    # Preserve other columns in their original names; remove spreadsheet error cells.
    for key,value in row.items():
        if value=="#VALUE!":row[key]=None
if len(rows)!=1190:
    raise ValueError(f"Expected 1190 Excel rows, found {len(rows)}")
with (target/"rostdata_v3.json").open("w",encoding="utf-8") as f:
    json.dump({"source_sheet":"Röstdata v3","source_table":"röstdata",
               "field_labels":{"OG varav EGEJ, ej anmälda part.":"OG varav EGEJ, ej anmälda partier"},
               "rows":rows},f,ensure_ascii=False,separators=(",",":"))
types=Counter(r["Val"] for r in rows)
years=Counter(r["År"] for r in rows)
(target/"importstatus.json").write_text(json.dumps({"rows":len(rows),"vote_types":types,
  "years":years,"source":"User provided Excel table Röstdata v3/röstdata",
  "missing": "Empty fields remain null; rows for the whole municipality and vote collection districts are not mapped to polygons."},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Exported {len(rows)} rows to docs/data/roster/rostdata_v3.json")
