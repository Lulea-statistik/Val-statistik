#!/usr/bin/env python3
"""Reconstruct provisional 1991 and copy the resulting district geometry to 1970-1988.

Base: the already-published 1994 reconstruction (NOT the 2002 source).
The Lulea 6 -> 7 cut is digitized approximately from a user-supplied screenshot.
"""
import copy
import json
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import Polygon, mapping, shape
from shapely.ops import transform, unary_union

ROOT = Path(__file__).resolve().parents[1]
YEARS = (1970, 1973, 1976, 1979, 1982, 1985, 1988, 1991)
BASE = ROOT / "docs/data/valdistrikt/1994/lulea_2580_valdistrikt_1994_preliminar_epsg4326.geojson"
SOURCE = json.loads(BASE.read_text(encoding="utf-8"))
assert len(SOURCE["features"]) == 56
assert all(str(f["properties"]["kommunkod"]) == "2580" for f in SOURCE["features"])

to_m = Transformer.from_crs("EPSG:4326", "EPSG:3006", always_xy=True).transform
to_ll = Transformer.from_crs("EPSG:3006", "EPSG:4326", always_xy=True).transform
rows = {f["properties"]["valdistriktskod"]: f for f in SOURCE["features"]}
assert len(rows) == 56
six_code, seven_code = "25800106", "25800107"
s1_code, s2_code = "25800350", "25800371"
assert [rows[c]["properties"]["valdistriktsnamn"] for c in (six_code, seven_code, s1_code, s2_code)] == [
    "Luleå 6", "Luleå 7", "Sunderbyns 1", "Sunderbyns 2"
]

six = transform(to_m, shape(rows[six_code]["geometry"]))
seven = transform(to_m, shape(rows[seven_code]["geometry"]))
s1 = transform(to_m, shape(rows[s1_code]["geometry"]))
s2 = transform(to_m, shape(rows[s2_code]["geometry"]))
for geo in (six, seven, s1, s2):
    assert geo.is_valid and not geo.is_empty

# Approximate user-drawn boundary, EPSG:3006.
# The northern part of Lulea 6 is transferred to Lulea 7.
cut = [(829060,7293910),(829150,7293825),(829350,7293815),
       (829560,7293825),(829760,7293840),(830020,7293878)]
north = Polygon([(828600,7296000),(830400,7296000),(830400,7293878)]
                + list(reversed(cut)) + [(828600,7293910)])
assert north.is_valid
transfer = six.intersection(north)
if not 100000 < transfer.area < 1000000:
    raise RuntimeError(f"Unexpected transfer area: {transfer.area} m2")
new_six = six.difference(transfer)
new_seven = unary_union([seven,transfer])
merged_sunderbyn = unary_union([s1,s2])
assert all(g.is_valid and not g.is_empty for g in (new_six,new_seven,merged_sunderbyn))
assert new_six.intersection(new_seven).area < .01
assert six.union(seven).symmetric_difference(new_six.union(new_seven)).area < .01
assert merged_sunderbyn.symmetric_difference(s1.union(s2)).area < .01

for year in YEARS:
    result = copy.deepcopy(SOURCE)
    result["features"] = [f for f in result["features"]
                          if f["properties"]["valdistriktskod"] != s2_code]
    for f in result["features"]:
        p = f["properties"]
        code = p["valdistriktskod"]
        p["valar"] = year
        p["historical_status"] = "preliminar_rekonstruktion"
        p["reference_year_geometry"] = 1994 if year == 1991 else 1991
        p["source_geometry_1994"] = True
        p["boundary_modified_against_1994"] = code in (six_code, seven_code, s1_code)
        if code == six_code:
            f["geometry"] = mapping(transform(to_ll,new_six))
        elif code == seven_code:
            f["geometry"] = mapping(transform(to_ll,new_seven))
        elif code == s1_code:
            f["geometry"] = mapping(transform(to_ll,merged_sunderbyn))
            p["valdistriktsnamn"] = "Sunderbyns 1 och 2"
            p["merged_from_codes"] = [s1_code,s2_code]
            p["historical_code_uncertain"] = True
            # Retain a valid 2580 district code for the map's municipality filter.
            p["valdistriktskod"] = s1_code
    if len(result["features"]) != 55:
        raise RuntimeError(f"Unexpected district count for {year}")
    codes = [f["properties"]["valdistriktskod"] for f in result["features"]]
    assert len(set(codes)) == 55
    assert all(f["properties"]["kommunkod"] == "2580" for f in result["features"])
    target = ROOT / "docs/data/valdistrikt" / str(year)
    target.mkdir(parents=True,exist_ok=True)
    name = f"lulea_2580_valdistrikt_{year}_preliminar_epsg4326.geojson"
    (target / name).write_text(json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    report = {
        "year":year,"status":"provisional_geometry_reconstruction",
        "reference":"published 1994 reconstructed district layer",
        "district_count":55,"unchanged_districts":52,
        "modified_codes":[six_code,seven_code,s1_code],
        "merged_codes":[s1_code,s2_code],
        "merged_historical_code":"unknown; retained 25800350 as map identifier",
        "approx_transfer_lulea6_to7_m2":round(transfer.area,1),
        "source_of_cut":"user-supplied screenshot, hand-estimated alignment; not surveyed",
        "1991_is_original":False,"pre1991_assumed_unchanged":year!=1991,
        "conserved_lulea6_plus7_m2":round(six.union(seven).symmetric_difference(new_six.union(new_seven)).area,8),
        "overlap_lulea6_and7_m2":round(new_six.intersection(new_seven).area,8),
    }
    (target/"quality.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"{year}: wrote 55 provisional districts; transferred {transfer.area:.1f} m2")
