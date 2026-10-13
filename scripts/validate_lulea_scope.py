#!/usr/bin/env python3
"""Check structure and commune isolation of a transcribed SCB SOS raw table.

Input is UTF-8 CSV. Preserve ALL original table columns. Required metadata:
valar,valtyp,kommunkod,kalla_id,tryckt_sida,tabell,radtyp,original_radnummer
Additional columns are allowed and never discarded.
"""
import argparse
import csv
import sys

REQUIRED=("valar","valtyp","kommunkod","kalla_id","tryckt_sida","tabell","radtyp","original_radnummer")
TYPES={"valdistrikt","kommun_summa","valkrets_summa_kontroll","vallokal","postroster","annan_kallrad"}
ELECTIONS={"riksdag","region","kommun"}

def validate(path):
    errors=[]
    with open(path,encoding="utf-8-sig",newline="") as source:
        reader=csv.DictReader(source)
        missing=set(REQUIRED)-set(reader.fieldnames or [])
        if missing:
            return [f"Saknade metadatafält: {sorted(missing)}"]
        for i,row in enumerate(reader,2):
            if row.get("kommunkod","").strip()!="2580":
                errors.append(f"Rad {i}: kommunkod måste vara 2580")
            if row.get("valtyp") not in ELECTIONS:
                errors.append(f"Rad {i}: ogiltig valtyp")
            if row.get("radtyp") not in TYPES:
                errors.append(f"Rad {i}: okänd radtyp")
            if any(not str(row.get(k) or "").strip() for k in REQUIRED):
                errors.append(f"Rad {i}: ofullständig proveniens")
    return errors

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("csv_file")
    args=p.parse_args()
    errors=validate(args.csv_file)
    if errors:
        print("\n".join(errors),file=sys.stderr)
        sys.exit(1)
    print("Godkänd geografisk avgränsning och obligatoriska metadata (ej röstsummeringskontroll)")
