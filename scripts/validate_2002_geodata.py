#!/usr/bin/env python3
"""Validate 2002 reconstructed municipality geometry metadata without GIS dependencies."""
import json
import sys
from collections import Counter
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/valdistrikt/2002/lulea_valdistrikt_2002_reconstructed_epsg4326.geojson")
dataset = json.loads(path.read_text(encoding="utf-8"))
features = dataset.get("features", [])
assert len(features) == 56, f"Expected 56 districts, got {len(features)}"
codes = []
groups = Counter()
for feature in features:
    p = feature.get("properties", {})
    assert str(p.get("kommunkod")) == "2580", f"Wrong municipality: {p}"
    assert str(p.get("valar")) == "2002", f"Wrong year: {p}"
    code = str(p.get("valdistriktskod",""))
    assert code.startswith("2580") and len(code) == 8, f"Bad code: {code}"
    codes.append(code)
    groups[str(p.get("kommunvalkrets_kod"))] += 1
    assert feature.get("geometry",{}).get("type") in ("Polygon","MultiPolygon"), f"Wrong geometry: {code}"
assert len(set(codes))==56, "Duplicate district code"
assert sorted(groups.values()) == [27,29], f"Unexpected constituency counts: {groups}"
print("2002 GIS metadata validated: 56 unique Lulea districts and constituency counts 27/29")
print("Note: not a spatial topology test or independent verification of 2002 boundaries.")
