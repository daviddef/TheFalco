#!/usr/bin/env python3
"""Every family that married into this line, built from the family tree.

The public build never names the living, so this only carries the dead. Each
surname keeps its places, its date span, the marriages that joined it to the
line, and an honest count of how many of its people are withheld."""
import json, re, collections, os

TREE = json.load(open("data/myheritage-falco-tree.json"))
byid = {p["id"]: p for p in TREE}

def surname(p):
    return (p.get("last") or "").strip()

def year(s):
    m = re.search(r"(1[6-9]\d\d|20\d\d)", s or "")
    return int(m.group(1)) if m else None

def place(s):
    """Town only — the trailing province/region/country is noise on a list."""
    s = (s or "").split(",")[0].strip()
    return s if s and not s.startswith("[") else ""

# spouse links, both directions
SPOUSE = {"His wife", "Her husband", "His ex-wife", "Her ex-husband",
          "His partner", "Her partner", "Her spouse", "Spouse"}

groups = collections.defaultdict(lambda: {
    "people": [], "withheld": 0, "places": collections.Counter(),
    "marriages": [], "first": None, "last": None})

for p in TREE:
    sn = surname(p)
    if not sn or sn == "?" or sn.startswith("["):
        continue
    g = groups[sn]
    if p.get("alive"):
        g["withheld"] += 1
        continue
    b, dd = year(p.get("b")), year(p.get("d"))
    for y in (b, dd):
        if y:
            g["first"] = y if g["first"] is None else min(g["first"], y)
            g["last"] = y if g["last"] is None else max(g["last"], y)
    for pl in (place(p.get("bp")), place(p.get("dp"))):
        if pl:
            g["places"][pl] += 1
    g["people"].append({
        "name": re.sub(r",? ?[✔⭐]+", "", p["name"]).strip(),
        "b": p.get("b", ""), "bp": place(p.get("bp")),
        "d": p.get("d", ""), "dp": place(p.get("dp")),
    })
    # who they married
    for r in p.get("relatives", []):
        if r["rel"] in SPOUSE:
            o = byid.get(r["id"])
            if not o or o.get("alive"):
                continue
            osn = surname(o)
            if osn and osn != sn:
                g["marriages"].append({
                    "who": re.sub(r",? ?[✔⭐]+", "", p["name"]).strip(),
                    "to": re.sub(r",? ?[✔⭐]+", "", o["name"]).strip(),
                    "into": osn})

# --- the Nudgee Cemetery burials: documented dead the tree marks as living ---
import csv
with open("data/nudgee-burials.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        sn = (r.get("surname") or "").strip()
        if not sn:
            continue
        g = groups[sn]
        nm = f"{(r.get('given') or '').strip()} {sn}".strip()
        if any(x["name"] == nm for x in g["people"]):
            continue
        for y in (year(r.get("born")), year(r.get("died"))):
            if y:
                g["first"] = y if g["first"] is None else min(g["first"], y)
                g["last"] = y if g["last"] is None else max(g["last"], y)
        g["places"]["Brisbane"] += 1
        g["people"].append({
            "name": nm, "b": (r.get("born") or "").strip(), "bp": "",
            "d": (r.get("died") or "").strip(), "dp": "Nudgee Cemetery, Brisbane",
            "src": "Nudgee Cemetery"})
        if g["withheld"]:
            g["withheld"] -= 1   # the tree's "living" flag is wrong where a grave says otherwise

out = []
for sn, g in groups.items():
    if not g["people"] and not g["withheld"]:
        continue
    g["people"].sort(key=lambda x: (year(x["b"]) or 9999, x["name"]))
    seen, marriages = set(), []
    for m in g["marriages"]:
        k = tuple(sorted((m["who"], m["to"])))
        if k in seen:
            continue
        seen.add(k)
        marriages.append(m)
    out.append({
        "surname": sn,
        "n": len(g["people"]),
        "withheld": g["withheld"],
        "first": g["first"], "last": g["last"],
        "places": [p for p, _ in g["places"].most_common(4)],
        "marriages": marriages,
        "people": g["people"],
    })

out.sort(key=lambda x: (-x["n"], x["surname"]))
os.makedirs("site/src/data", exist_ok=True)
json.dump(out, open("site/src/data/married-in.json", "w"), indent=1, ensure_ascii=False)
print(f"{len(out)} surnames · {sum(x['n'] for x in out)} named · "
      f"{sum(x['withheld'] for x in out)} withheld as living")
