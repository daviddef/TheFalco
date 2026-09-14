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

ARK = re.compile(r"ark:/61903/([0-9]:[0-9]:[A-Z0-9\-]+)")
CC  = re.compile(r"[?&]cc=([0-9]+)")
WC  = re.compile(r"[?&]wc=([^\s\"&)]+)")


def films_by_place(place_names):
    """The register images this archive has actually opened, by parish.

    register.json carries 11,760 rows and each one that came off a film keeps
    the link. The parish is named in the row's own detail line, so the join is
    the archive's own words rather than anything inferred. Films repeat across
    hundreds of rows — one book holds a great many baptisms — so they are
    deduplicated by ark and counted honestly.
    """
    out = {n: {} for n in place_names}
    for r in J("register.json"):
        link = r.get("link") or ""
        m = ARK.search(link)
        if not m:
            continue
        detail = (r.get("detail") or "")
        for n in place_names:
            if n.lower() in detail.lower():
                ark = m.group(1)
                if ark not in out[n]:
                    cc, wc = CC.search(link), WC.search(link)
                    # The row's own source line names the register far better
                    # than a generated label would.
                    src = (r.get("source") or "").strip()
                    # Some rows cite a film as evidence for a reconstruction the
                    # archive made; the source line then describes the archive's
                    # own work rather than the book. Call those what they are.
                    title = ("Parish register image"
                             if not src or src.lower().startswith("reconstructed") else src)
                    when = (r.get("sort") or "").strip()
                    out[n][ark] = {"t": f"{title} · {when}" if when else title,
                                   "ark": ark,
                                   "cc": cc.group(1) if cc else "",
                                   "wc": wc.group(1) if wc else ""}
                break
    return out


def main():
    rows = []
    names = [p["name"] for p in J("places.json")]
    films = films_by_place(names)
    for p in J("places.json"):
        name = p["name"]
        span = " to ".join(x for x in (p.get("from"), p.get("to")) if x)
        rows.append({
            "name": name, "_lookup": f"{name}, {p.get('prov','')}, Italy".replace(", ,", ","),
            "cat": cat(f"{name} {p.get('prov','')}"), "n": 0,
            "when": span, "what": p.get("what") or "",
            "films": list(films.get(name, {}).values())[:40],
            "nfilms": len(films.get(name, {})),
        })
    atlasdata.build(rows, OUT, countries=["Italia","Italy","Australia"])

if __name__ == "__main__":
    sys.exit(main())
