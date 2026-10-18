#!/usr/bin/env python3
"""Holds every <Rec> on a page to the records table and to the words it wraps.

    python3 tools/check_records.py             # from site/ (npm run check:records)

The kit's <Rec> turns a citation the author already wrote into a link to the record (the linking standard's L3/L4). The build stops
on an id the table does not hold; this check goes one step further, because a link to the wrong volume is worse than none:

  * the generated files are current: tools/build_records.py --check and tools/build_plate_keys.py --check;
  * every <Rec id="..."> or act="..." on a page names a row of site/src/data/records.json (an id written as an expression,
    <Rec id={x}>, is not read here; the build still stops on a bad one);
  * the row is not held out (living / hold): <Rec> would draw nothing there, and the author's words would vanish;
  * a Rec with `thumb` names a row that has a plate and show true;
  * the WORDS it wraps agree with the volume: a year written in them is the volume's year (a range counts), and a register
    word in them (Nati / births, Morti / deaths, Matrimoni / marriage, processetti / bundle) is the volume's series where the
    archive's data names one.

It prints counts. It reads source files only, so it runs before the build.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "site", "src")
REC = re.compile(r"<Rec\b([^>]*)>(.*?)</Rec>", re.S)
ATTR = re.compile(r'\b(id|act)="([^"]*)"')
YEAR = re.compile(r"\b(1[6-9]\d\d)\b")
SER = [("Nati", re.compile(r"\b(births?|nati|nascite)\b", re.I)), ("Morti", re.compile(r"\b(deaths?|morti)\b", re.I)),
       ("Matrimoni", re.compile(r"\b(marriages?|matrimoni)\b", re.I)), ("Processetti", re.compile(r"\b(processett\w*|bundles?|dossier)\b", re.I))]


def years_of(y):
    m = re.fullmatch(r"(\d{4})(?:\s*[-–]\s*(\d{4}))?", str(y or "").strip())
    return (int(m.group(1)), int(m.group(2) or m.group(1))) if m else None


def main():
    bad = []
    for script in ("build_records.py", "build_plate_keys.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, script), "--check"], capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode:
            bad.append("%s --check failed" % script)
    rows = {r["id"]: r for r in json.load(open(os.path.join(SRC, "data", "records.json"), encoding="utf-8"))["records"]}
    bykey = {}
    for r in rows.values():
        for k in ([r["key"]] if isinstance(r.get("key"), str) else r.get("key", [])):
            bykey[re.sub(r"[^a-z0-9]+", " ", k.lower()).strip()] = r
    n = thumbs = words = 0
    for root, _d, files in os.walk(os.path.join(SRC, "pages")):
        for fn in files:
            if not fn.endswith(".astro"):
                continue
            path = os.path.join(root, fn)
            where = os.path.relpath(path, ROOT)
            for m in REC.finditer(open(path, encoding="utf-8").read()):
                attrs, text = m.group(1), m.group(2)
                a = dict(ATTR.findall(attrs))
                if "id=" in attrs and "id" not in a or "act=" in attrs and "act" not in a:
                    continue                                    # an expression: the build checks it
                row = rows.get(a.get("id")) if "id" in a else bykey.get(re.sub(r"[^a-z0-9]+", " ", a.get("act", "").lower()).strip())
                n += 1
                if row is None:
                    bad.append("%s: <Rec %s> is not in the records table" % (where, attrs.strip()))
                    continue
                if row.get("living") or row.get("hold"):
                    bad.append("%s: <Rec id=%s> names a row that is held out: it would draw nothing" % (where, row["id"]))
                    continue
                if re.search(r"\bthumb\b", attrs):
                    thumbs += 1
                    if not (row.get("plate") and row.get("show") is True):
                        bad.append("%s: <Rec id=%s thumb> but the row has no plate the archive shows" % (where, row["id"]))
                plain = re.sub(r"<[^>]+>|\{[^}]*\}", " ", text)
                if row["kind"] == "ark":
                    span = years_of(row.get("year"))
                    ys = [int(y) for y in YEAR.findall(plain)]
                    if ys and span and not all(span[0] <= y <= span[1] for y in ys):
                        bad.append("%s: <Rec id=%s> is the volume of %s but its words say %s: %r" % (where, row["id"], row.get("year"), ys, plain.strip()[:60]))
                    if row.get("series"):
                        said = [s for s, rx in SER if rx.search(plain)]
                        if said and row["series"] not in said:
                            bad.append("%s: <Rec id=%s> is %s but its words say %s: %r" % (where, row["id"], row["series"], "/".join(said), plain.strip()[:60]))
                    words += 1
    print("check_records: %d <Rec> read, %d with a volume's year and series held to their words, %d thumbs; %d problem(s)" % (n, words, thumbs, len(bad)))
    for b in bad:
        print("  FAIL", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
