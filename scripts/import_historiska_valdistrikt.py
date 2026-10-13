#!/usr/bin/env python3
"""Fetch Valmyndigheten's election-district archives; extract only Luleå (2580).

Usage: python scripts/import_historiska_valdistrikt.py --year 2018
Install: pip install requests beautifulsoup4 pyshp shapely pyproj
Do NOT change or infer an unknown source CRS. Outputs to docs/data/valdistrikt/.
"""
import argparse
import hashlib
import json
import re
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import shapefile
from pyproj import CRS, Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform

SOURCES={
 2006:("https://historik.val.se/val/val2006/slutlig_ovrigt/statistik/kartor/index.html",["riksdagsvalet 2006 i valdistrikt"]),
 2010:("https://historik.val.se/val/val2010/statistik/index.html",["alla valdistrikt"]),
 2014:("https://historik.val.se/val/val2014/statistik/",["alla valdistrikt"]),
 2018:("https://historik.val.se/val/val2018/statistik/",["2018_valgeografi_valdistrikt.zip"]),
 2022:("https://www.val.se/valresultat-och-statistik/statistik-och-data/radata-fran-val-2002-2022",["norrbottens län zip"]),
 2026:("https://www.val.se/valresultat-och-statistik/statistik-och-data/radata-val-2026",["norrbottens län zip"])
}
def fetch_archive(year,session):
    page,labels=SOURCES[year]
    if year in (2006,2014,2018):
        url={2006:"https://historik.val.se/val/val2006/slutlig_ovrigt/statistik/kartor/riksdagen_i_valdistrikt.zip",2014:"https://historik.val.se/val/val2014/statistik/gis/valgeografi_valdistrikt.zip",2018:"https://historik.val.se/val/val2018/statistik/2018_valgeografi_valdistrikt.zip"}[year]
        r=session.get(url,timeout=180);r.raise_for_status()
        if not zipfile.is_zipfile(__import__("io").BytesIO(r.content)):
            raise RuntimeError(f"Official {year} archive is not a ZIP")
        return url,r.content
    r=session.get(page,timeout=45);r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    matches=[]
    for a in soup.select("a[href]"):
        label=a.get_text(" ",strip=True).casefold()
        href=a["href"]
        if any(term in (label+" "+href.casefold()) for term in labels):
            matches.append(urljoin(r.url,href))
    matches=list(dict.fromkeys(matches))
    if len(matches)!=1:
        raise RuntimeError(f"Expected exactly one matching download for {year}, got {matches}. Inspect source HTML and use a verified source URL.")
    url=matches[0]
    r=session.get(url,timeout=180);r.raise_for_status()
    if not zipfile.is_zipfile(__import__("io").BytesIO(r.content)):
        raise RuntimeError(f"Downloaded source is not a ZIP: {url}")
    return url,r.content

def code_column(properties):
    for k,v in properties.items():
        key=re.sub(r"[^a-z0-9]","",k.casefold())
        if key in ("vd","vdkod","valdistriktskod","valdistriktkod","valdistriktid","vdid","vdnr","valdistrikt","kod","vdk","lkfv"):
            sv=str(v).strip().split(".")[0]
            if re.fullmatch(r"2580\d{4}",sv):return True
    return False

def municipality(properties):
    for k,v in properties.items():
        key=re.sub(r"[^a-z0-9]","",k.casefold())
        if key in ("kommunkod","kommunid","komkod","knkod","kommunnr","komnr","kommunk","kn","knkod4","kom"):
            if str(v).strip() in ("2580","2580.0"):return True
    return code_column(properties)

def inspect_geojson(data, year):
    collection=json.loads(data.decode("utf-8-sig"))
    if collection.get("type")!="FeatureCollection":raise RuntimeError("Expected GeoJSON FeatureCollection")
    crs=collection.get("crs",{})
    name=(crs.get("properties") or {}).get("name","")
    if not name:raise RuntimeError("Missing source CRS; specify and independently verify CRS from official file metadata before conversion")
    epsg=CRS.from_user_input(name)
    return collection.get("features",[]),epsg

def read_shapefile(z):
    names=z.namelist()
    shp=[x for x in names if x.lower().endswith(".shp")]
    if len(shp)!=1:raise RuntimeError(f"Expected a single shapefile, got {shp}")
    stem=shp[0][:-4]
    prj=next((x for x in names if x.casefold()==(stem+".prj").casefold()),None)
    if prj is None:raise RuntimeError("Missing .prj: CRS must be verified")
    crs=CRS.from_wkt(z.read(prj).decode("utf-8-sig",errors="replace"))
    with tempfile.TemporaryDirectory() as tmp:
        z.extractall(tmp)
        reader=shapefile.Reader(str(Path(tmp)/shp[0]),encoding="cp1252",encodingErrors="strict")
        fields=[f[0] for f in reader.fields[1:]]
        features=[]
        for record in reader.iterShapeRecords():
            geom=record.shape.__geo_interface__
            features.append({"type":"Feature","properties":dict(zip(fields,record.record)),"geometry":geom})
        return features,crs

def run(year,root):
    session=requests.Session()
    session.headers["User-Agent"]="Lulea-statistik-historiska-valdistrikt/1.0 (research)"
    source,raw=fetch_archive(year,session)
    digest=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(__import__("io").BytesIO(raw)) as z:
        geojsons=[x for x in z.namelist() if x.lower().endswith((".json",".geojson"))]
        if year>=2022:
            if len(geojsons)!=1:raise RuntimeError(f"Expected one JSON in archive, got {geojsons}")
            feats,crs=inspect_geojson(z.read(geojsons[0]),year)
        else:
            feats,crs=read_shapefile(z)
    matched=[]
    for f in feats:
        props=f.get("properties") or {}
        if not municipality(props):continue
        g=shape(f["geometry"])
        if g.geom_type not in ("Polygon","MultiPolygon"):raise RuntimeError("Non-polygon feature for Lulea")
        if not g.is_valid:raise RuntimeError("Invalid source geometry; do not silently repair")
        matched.append(f)
    if not matched:raise RuntimeError("No provable Lulea 2580 features; inspect original property schema.")
    transformer=Transformer.from_crs(crs,CRS.from_epsg(4326),always_xy=True)
    # Multiple source records can represent pieces of the same 2006 district.\n    # Merge by verified eight-digit district code to avoid duplicated district options.\n    if year==2006:\n        from collections import defaultdict\n        from shapely.ops import unary_union\n        groups=defaultdict(list)\n        for feature in matched:\n            code=str(feature["properties"]["Lkfv"])\n            groups[code].append(feature)\n        merged=[]\n        for code, parts in sorted(groups.items()):\n            props=dict(parts[0]["properties"])\n            if any(str(f["properties"].get("KOM"))!="2580" or str(f["properties"].get("NAMN"))!=str(props["NAMN"]) for f in parts):\n                raise RuntimeError(f"Inconsistent source attributes for {code}")\n            props["source_part_count"]=len(parts)\n            merged.append({"type":"Feature","properties":props,"geometry":mapping(unary_union([shape(f["geometry"]) for f in parts]))})\n        matched=merged\n    output=[]\n    for f in matched:
        g=transform(transformer.transform,shape(f["geometry"]))
        if not g.is_valid:raise RuntimeError("Reprojection resulted in invalid geometry")
        if not (18.0<=g.bounds[0]<=25.0 and 64.0<=g.bounds[1]<=68.0 and 18.0<=g.bounds[2]<=25.0 and 64.0<=g.bounds[3]<=68.0):
            raise RuntimeError("Reprojected coordinates outside WGS84 range")
        props=dict(f["properties"])
        props.update({"valar":year,"kommunkod":"2580","kallstatus":"original_valmyndigheten","original_epsg":crs.to_epsg()})
        output.append({"type":"Feature","properties":props,"geometry":mapping(g)})
    outdir=root/"docs"/"data"/"valdistrikt"/str(year)
    outdir.mkdir(parents=True,exist_ok=True)
    outputfile=outdir/f"lulea_2580_valdistrikt_{year}_epsg4326.geojson"
    outputfile.write_text(json.dumps({"type":"FeatureCollection","features":output},ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    quality={"valar":year,"kommunkod":"2580","source_page":SOURCES[year][0],"archive_url":source,
             "source_sha256":digest,"source_crs":crs.to_string(),"target_crs":"EPSG:4326",
             "feature_count":len(output),"geometry_types":sorted(set(f["geometry"]["type"] for f in output)),
             "checked_utc":datetime.now(timezone.utc).isoformat(),"status":"imported_requires_crossyear_boundary_review"}
    (outdir/"quality.json").write_text(json.dumps(quality,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"{year}: {len(output)} Lulea districts -> {outputfile}")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--year",required=True,type=int,choices=sorted(SOURCES))
    p.add_argument("--repo-root",type=Path,default=Path("."))
    a=p.parse_args()
    run(a.year,a.repo_root)
