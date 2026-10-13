#!/usr/bin/env python3
"""Extract original, unaltered SCB PDF pages covering Luleå kommun (2580).

Usage:
 python scripts/extract_lulea_pdf.py full.pdf --year 1998 --election region --pages 277-278 --source-url https://...
--pages are PDF page numbers (1-based), NOT printed page numbers.
Page ranges must be checked manually so all Luleå rows, including any continuation pages, are included.
Requires pypdf. No OCR or reconstruction; output is a genuine subset of original PDF pages.
"""
import argparse
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def pages(spec):
    result=[]
    for item in spec.split(","):
        bounds=item.strip().split("-")
        a=int(bounds[0]); b=int(bounds[-1])
        if a<1 or b<a: raise ValueError("Invalid PDF page range")
        result.extend(range(a,b+1))
    if len(result)!=len(set(result)): raise ValueError("Duplicate PDF page")
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("source",type=Path)
    ap.add_argument("--year",type=int,required=True)
    ap.add_argument("--election",choices=["riksdag","region","kommun"],required=True)
    ap.add_argument("--pages",required=True,help="PDF page indices, 1-based; e.g. 284-285")
    ap.add_argument("--source-url",required=True)
    ap.add_argument("--printed-pages",default="",help="Printed page labels, e.g. 277-278")
    ap.add_argument("--out-dir",type=Path,default=Path("docs/pdf/lulea"))
    args=ap.parse_args()
    full=args.source.read_bytes()
    if not full.startswith(b"%PDF"): raise ValueError("Not a PDF")
    reader=PdfReader(args.source)
    requested=pages(args.pages)
    for page in requested:
        if page>len(reader.pages): raise ValueError(f"Page {page} beyond {len(reader.pages)}")
    writer=PdfWriter()
    for page in requested:
        writer.add_page(reader.pages[page-1])
    args.out_dir.mkdir(parents=True,exist_ok=True)
    stem=f"lulea_2580_{args.year}_{args.election}"
    target=args.out_dir/(stem+".pdf")
    with target.open("wb") as f: writer.write(f)
    manifest={"year":args.year,"election":args.election,"kommunkod":"2580",
       "source_url":args.source_url,"source_sha256":hashlib.sha256(full).hexdigest(),
       "source_pdf_page_numbers_1_based":requested,"source_printed_pages":args.printed_pages,
       "excerpt_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
       "scope_note":"Extracted original pages may also contain adjoining municipalities; only Luleå 2580 is in analysis scope.",
       "review_status":"pending_manual_page_and_boundary_check"}
    (args.out_dir/(stem+".json")).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(target)

if __name__=="__main__":main()
