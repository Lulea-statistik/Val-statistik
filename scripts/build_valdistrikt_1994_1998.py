#!/usr/bin/env python3
"""Provisional 1994/1998 district layers from 2002 plus KF 2001-10-29 section 140.
The digitized 2001 dashed boundary is approximate, not survey-grade.
"""
import copy
import json
from pathlib import Path
from shapely.geometry import shape, Polygon, mapping
from shapely.ops import transform, unary_union
from pyproj import Transformer

root=Path(__file__).resolve().parents[1]
original=json.loads((root/"docs/data/lulea_valdistrikt_2002.geojson").read_text(encoding="utf-8"))
assert len(original["features"])==56
by_code={f["properties"]["valdistriktskod"]:f for f in original["features"]}
assert len(by_code)==56
to3006=Transformer.from_crs(4326,3006,always_xy=True).transform
to4326=Transformer.from_crs(3006,4326,always_xy=True).transform
one=transform(to3006,shape(by_code["25800267"]["geometry"]))
two=transform(to3006,shape(by_code["25800268"]["geometry"]))
assert one.is_valid and two.is_valid and one.intersection(two).area<0.01
# Approximate EPSG:3006 georeferencing of the dashed PRE-2002 line in
# the municipal map, KF 2001-10-29 section 140, page 4, supplemented
# by SWEREF99 TM reference E829939 N7296378 within the local area.
# It is not an exact tracing of historical parcel boundaries.
old_boundary_window=Polygon([
 (829990,7295780),(830560,7295780),
 (830560,7296513),(830485,7296480),(830365,7296438),
 (830280,7296412),(830180,7296360),(830100,7296315),
 (830030,7296285),(829990,7296285)
])
shared=one.boundary.intersection(two.boundary)
transfer=one.intersection(old_boundary_window).intersection(shared.buffer(360))
if transfer.is_empty or not 10000<transfer.area<220000:
    raise ValueError(f"Unreasonable Bjorkskatan transfer: {transfer.area}")
new_one=one.difference(transfer)
new_two=unary_union([two,transfer])
assert new_one.is_valid and new_two.is_valid
assert new_one.intersection(new_two).area<0.01
assert one.union(two).symmetric_difference(new_one.union(new_two)).area<0.01
for year in (1994,1998):
    output=copy.deepcopy(original)
    for feature in output["features"]:
        props=feature["properties"]
        code=props["valdistriktskod"]
        props["valar"]=year
        props["historical_status"]="preliminar_rekonstruktion"
        props["reference_year_geometry"]=2002
        props["geometry_origin"]="2002 GIS reconstruction, adjusted Bjorkskatan from 2001 municipal map"
        props["boundary_modified"]=code in ("25800267","25800268")
        if code=="25800267":
            feature["geometry"]=mapping(transform(to4326,new_one))
        elif code=="25800268":
            feature["geometry"]=mapping(transform(to4326,new_two))
    folder=root/"docs/data/valdistrikt"/str(year)
    folder.mkdir(parents=True,exist_ok=True)
    (folder/f"lulea_2580_valdistrikt_{year}_preliminar_epsg4326.geojson").write_text(
        json.dumps(output,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    report={
        "year":year,"kommunkod":"2580","feature_count":56,
        "source_layer":"2002 reconstructed, not 2002 original",
        "source_document":"Lulea KF 2001-10-29 section 140, page 4, dashed previous boundary",
        "modified_districts":["25800267","25800268"],
        "approximate_transfer_area_m2":round(transfer.area,2),
        "changed_area_is_estimate":True,
        "unchanged_geometry_features":54,
        "reference_point_epsg3006":[829939,7296378],
        "geometry_precision":"preliminary manual map alignment, NOT verified parcel-level georeferencing",
        "boundaries_1994_equal_1998":"working assumption; not independently verified",
        "source_status":"provisional_reconstruction",
        "no_overlap_m2":round(new_one.intersection(new_two).area,8),
        "no_gap_change_m2":round(one.union(two).symmetric_difference(new_one.union(new_two)).area,8)
    }
    (folder/"quality.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Created 1994 and 1998 provisional GIS layers; Bjorkskatan transfer {transfer.area:.1f} m2")
