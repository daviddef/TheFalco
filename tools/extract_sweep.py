#!/usr/bin/env python3
"""Pull the people read in the death-register sweeps out of the notes tables
and into structured rows, so they reach the register instead of sitting in prose."""
import re, csv, glob, os

ARK = {str(y): "an_ua%d" % (14311 + y - 1809) for y in range(1809, 1845)}
BIRTH_ARK = {"1816":"an_ua14413","1817":"an_ua14414","1818":"an_ua14415"}
rows=[]
for path in sorted(glob.glob("notes/18*-death-register-progress.md")):
    year = re.search(r"(18\d\d)", os.path.basename(path)).group(1)
    in_old = False
    for ln in open(path):
        if ln.startswith("|") and "side" in ln.lower() and "age" in ln.lower():
            in_old = True; continue          # | img | side | deceased | age | detail |
        if ln.startswith("|") and "parents" in ln.lower():
            in_old = False; continue         # the newer act-per-row shape
        if not ln.startswith("|"):
            in_old = False; continue
        if not in_old: continue
        c=[x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c)!=5: continue
        img,side,name,age,detail = c[0],c[1],c[2],c[3],c[4]
        if not re.fullmatch(r"\d+", img): continue
        if not name or name.startswith("*(") or name.startswith("(") : continue
        name = re.sub(r"\*\*|\*", "", name).strip()
        if len(name)<3: continue
        rows.append(dict(year=year, img=img, side=side, name=name,
                         age=re.sub(r"\*","",age).strip(),
                         detail=re.sub(r"\*\*|\*","",detail).strip(),
                         ark=ARK.get(year,"")))
# birth registers: | img | side | father | age | trade | street |
for path in sorted(glob.glob("notes/18*-birth-register-progress.md")):
    year = re.search(r"(18\d\d)", os.path.basename(path)).group(1)
    for ln in open(path):
        if not ln.startswith("|"): continue
        c=[x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c)<6: continue
        img,side,name,age,trade,street = c[0],c[1],c[2],c[3],c[4],c[5]
        if not re.fullmatch(r"\d+", img): continue
        name = re.sub(r"\*\*|\*", "", name).strip()
        if not name or name.startswith("(") or "duplicat" in name.lower(): continue
        if len(name)<3: continue
        det=[]
        if age and age not in ("—","-"): det.append("aged "+re.sub(r"\*","",age))
        if trade and trade not in ("—","-"): det.append(re.sub(r"\*","",trade))
        if street and street not in ("—","-"): det.append("strada "+re.sub(r"\*\*|\*","",street))
        det.append("declares a birth")
        rows.append(dict(year=year, img=img, side=side, name=name,
                         age=re.sub(r"\*","",age).strip(),
                         detail=" · ".join(det), ark=BIRTH_ARK.get(year,"")))

# --- the 1816/1817-style tables: one row per ACT, several people per row ---
# | act | img | date | deceased | parents | spouse | declarants |
# Every person named is emitted separately, so a neighbour or a declarant is
# as findable as the deceased. Nothing read is left sitting only in prose.
# Arienzo civil death registers: verified, not extrapolated — 1809 is an_ua14311, +1 a year.
DEATH_ARK_2 = {str(y): "an_ua%d" % (14311 + y - 1809) for y in range(1809, 1845)}
NOISE = re.compile(r"^(—|-|\?|blank.*|duplicate.*|widow|the volume ends.*)?$", re.I)

def clean_name(t):
    t = re.sub(r"\*\*|\*|«|»", "", t)
    t = re.sub(r"\(.*?\)", " ", t)          # drop parentheticals
    t = re.sub(r"^(fu|ved\.|m\.|seu)\s+", "", t.strip(), flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" ,.;:")
    return t

def looks_like_name(t):
    if len(t) < 4 or NOISE.match(t): return False
    if not re.match(r"^[A-ZÀ-Ü]", t): return False
    if re.search(r"\d", t): return False
    return len(t.split()) >= 2

for path in sorted(glob.glob("notes/18*-death-register-progress.md")):
    year = re.search(r"(18\d\d)", os.path.basename(path)).group(1)
    ark = DEATH_ARK_2.get(year, "")
    in_tbl = False
    for ln in open(path):
        if ln.startswith("|") and "parents" in ln.lower():
            in_tbl = True; continue
        if not ln.startswith("|"):
            in_tbl = False; continue
        if not in_tbl: continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if set(c[0]) <= set("-: "): continue
        # two shapes are in use: with a leading act-number column, and without
        if len(c) >= 7:
            _act, img, date, dead, parents, spouse, decl = c[:7]
        elif len(c) == 6:
            img, date, dead, parents, spouse, decl = c[:6]
        else:
            continue
        img_n = (re.search(r"(\d+)", img) or [""])[0] if img else ""
        y = year
        if year == "1817" and re.search(r"\b(Jan|Feb)\b", date) and img_n.isdigit() and int(img_n) >= 77:
            y = "1818"                      # the 1818 acts bound into the 1817 volume
        date = re.sub(r"\*\*|\*", "", date).strip()
        who = clean_name(dead)
        def emit(nm, det):
            nm = clean_name(nm)
            if looks_like_name(nm):
                rows.append(dict(year=y, img=img_n, side="", name=nm, age="",
                                 detail=det, ark=ark))
        if looks_like_name(who):
            rows.append(dict(year=y, img=img_n, side="", name=who, age="",
                             detail=f"died {date} — read in the death register", ark=ark))
        for pnt in re.split(r"\s*&\s*", parents):
            emit(pnt, f"named as a parent of {who or 'the deceased'}, {date}")
        emit(spouse, f"named as the spouse of {who or 'the deceased'}, {date}")
        for d in re.split(r"\s*;\s*", decl):
            d = re.sub(r"\s*—.*$", "", d)
            nm = re.split(r"\s+\d", d)[0]
            det = re.sub(r"\s+", " ", re.sub(r"\*\*|\*", "", d)).strip()
            emit(nm, f"declarant at the death of {who or 'a neighbour'}, {date} — {det}")

with open("data/sweep-people.tsv","w",newline="") as f:
    w=csv.DictWriter(f,delimiter="\t",fieldnames=["year","img","side","name","age","detail","ark"])
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} people extracted from the sweep tables")
from collections import Counter
print("by year:", dict(Counter(r["year"] for r in rows)))
