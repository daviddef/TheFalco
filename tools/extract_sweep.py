#!/usr/bin/env python3
"""Pull the people read in the death-register sweeps out of the notes tables
and into structured rows, so they reach the register instead of sitting in prose."""
import re, csv, glob, os

ARK = {"1829":"an_ua14331","1830":"an_ua14332","1831":"an_ua14333","1832":"an_ua14334",
       "1833":"an_ua14335","1834":"an_ua14336","1835":"an_ua14337","1836":"an_ua14338"}
rows=[]
for path in sorted(glob.glob("notes/18*-death-register-progress.md")):
    year = re.search(r"(18\d\d)", os.path.basename(path)).group(1)
    for ln in open(path):
        if not ln.startswith("|"): continue
        c=[x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c)<5: continue
        img,side,name,age,detail = c[0],c[1],c[2],c[3],c[4]
        if not re.fullmatch(r"\d+", img): continue
        if not name or name.startswith("*(") or name.startswith("(") : continue
        name = re.sub(r"\*\*|\*", "", name).strip()
        if len(name)<3: continue
        rows.append(dict(year=year, img=img, side=side, name=name,
                         age=re.sub(r"\*","",age).strip(),
                         detail=re.sub(r"\*\*|\*","",detail).strip(),
                         ark=ARK.get(year,"")))
with open("data/sweep-people.tsv","w",newline="") as f:
    w=csv.DictWriter(f,delimiter="\t",fieldnames=["year","img","side","name","age","detail","ark"])
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} people extracted from the sweep tables")
from collections import Counter
print("by year:", dict(Counter(r["year"] for r in rows)))
