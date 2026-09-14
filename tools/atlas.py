#!/usr/bin/env python3
"""Falco's places, for the map.

Six entries, each with a province, a span of years and a paragraph that is
better written than anything a generator would produce. Nothing is derived
here; the list is simply given a coordinate so it can be seen as geography.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "site", "node_modules",
                                "@daviddef", "archive-kit", "kit", "tools"))
import atlasdata
D = os.path.join(HERE, "..", "site", "src", "data")
J = lambda n: json.load(open(os.path.join(D, n), encoding="utf-8"))
OUT = os.path.join(HERE, "..", "site", "public", "atlas-data.json")

def cat(p):
    s = p.lower()
    if re.search(r"arienzo|caserta|valle caudina|forchia|benevento|campania", s): return "valle"
    if re.search(r"napoli|naples", s):                                            return "naples"
    if re.search(r"australia|brisbane|queensland", s):                            return "au"
    return "other"

def main():
    rows = []
    for p in J("places.json"):
        name = p["name"]
        span = " to ".join(x for x in (p.get("from"), p.get("to")) if x)
        rows.append({
            "name": name, "_lookup": f"{name}, {p.get('prov','')}, Italy".replace(", ,", ","),
            "cat": cat(f"{name} {p.get('prov','')}"), "n": 0,
            "when": span, "what": p.get("what") or "",
        })
    atlasdata.build(rows, OUT, countries=["Italia","Italy","Australia"])

if __name__ == "__main__":
    sys.exit(main())
