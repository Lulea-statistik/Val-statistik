#!/usr/bin/env python3
"""Validate transcribed Swedish historical election rows. Standard library only.

CSV columns: valar,valtyp,geografi,rostberattigade,rostande,giltiga,ogiltiga,
valdeltagande_procent,m,c,f,kds,s,vpk,kfml,ovr
Optional: vallokal_rostande,postroster_rostande,vallokal_giltiga,postroster_giltiga.
Empty numeric fields are NOT zero. A dash in a party column means zero only
when a transcription reviewer has confirmed this is the source convention.
"""
import argparse
import csv
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

PARTIES = ("m", "c", "f", "kds", "s", "vpk", "kfml", "ovr")
BASE = ("rostberattigade", "rostande", "giltiga", "ogiltiga", "valdeltagande_procent")

def number(value, integer=True):
    s = str(value or "").strip().replace(" ", "").replace("\u00a0", "")
    if not s:
        raise ValueError("saknat värde")
    if s == "-":
        raise ValueError("streck måste granskas och ersättas med explicit 0 vid behov")
    try:
        n = Decimal(s.replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("inte numeriskt: " + s) from exc
    if n < 0 or (integer and n != n.to_integral_value()):
        raise ValueError("negativt eller ej heltal: " + s)
    return n

def validate(row):
    errors = []
    values = {}
    for key in BASE + PARTIES:
        try:
            values[key] = number(row.get(key), integer=(key != "valdeltagande_procent"))
        except ValueError as exc:
            errors.append(f"{key}: {exc}")
    if errors:
        return errors
    v = values
    if v["rostande"] != v["giltiga"] + v["ogiltiga"]:
        errors.append("rostande != giltiga + ogiltiga")
    if v["giltiga"] != sum((v[k] for k in PARTIES), Decimal(0)):
        errors.append("giltiga != summa partiröster")
    if v["rostberattigade"] <= 0:
        errors.append("rostberattigade måste vara > 0")
    else:
        calc = (100 * v["rostande"] / v["rostberattigade"]).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        if calc != v["valdeltagande_procent"]:
            errors.append(f"valdeltagande {v['valdeltagande_procent']} != beräknat {calc}")
    if v["rostande"] > v["rostberattigade"]:
        errors.append("rostande > rostberattigade")
    for target, a, b in (
        ("rostande", "vallokal_rostande", "postroster_rostande"),
        ("giltiga", "vallokal_giltiga", "postroster_giltiga"),
    ):
        if row.get(a, "").strip() or row.get(b, "").strip():
            try:
                if v[target] != number(row.get(a)) + number(row.get(b)):
                    errors.append(f"{target} != {a} + {b}")
            except ValueError as exc:
                errors.append(f"deluppdelning {target}: {exc}")
    return errors

def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv_path")
    args = p.parse_args()
    failures = 0
    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for n, row in enumerate(reader, 2):
            problems = validate(row)
            label = f"rad {n} ({row.get('valar','?')}, {row.get('valtyp','?')}, {row.get('geografi','?')})"
            if problems:
                failures += 1
                print("FEL", label, "; ".join(problems))
            else:
                print("OK ", label)
    if failures:
        raise SystemExit(f"{failures} rader underkända: kontrollera mot SCB:s originaltabell")
if __name__ == "__main__":
    main()
