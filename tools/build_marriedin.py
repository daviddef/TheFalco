#!/usr/bin/env python3
"""Every family that married into this line, built from the family tree.

The public build never names the living, so this only carries the dead. Each
surname keeps its places, its date span, the marriages that joined it to the
line, and an honest count of how many of its people are withheld."""
import json, re, collections, os

TREE = json.load(open("data/myheritage-falco-tree.json"))
byid = {p["id"]: p for p in TREE}

# The slug of each person, taken from the file build_people.py already wrote and
# keyed on the tree id both builds share. It is joined on the ID, never on the
# name: 103 of the 294 people on this page share a name with somebody else here
# — there are three separate Marta Zampiello — so a name would point a third of
# these links at a guess, in an archive whose whole method is refusing to merge
# on a name.
SLUG = {}
ARCH = {}
try:
    _pj = json.load(open("site/src/data/people.json"))
    for _r in (_pj if isinstance(_pj, list) else _pj.get("people", [])):
        if _r.get("treeId") is not None:
            SLUG[_r["treeId"]] = _r["slug"]
            ARCH[_r["treeId"]] = _r
except FileNotFoundError:
    pass          # people.json is built first; a missing one just means no links

# WHERE THE TREE IS SILENT, THE ARCHIVE SPEAKS — 22 September 2026.
#
# This page was built from the tree alone, so a person the ARCHIVE had dated from
# an act but the tree had not dated at all came out blank. MARIANTONIA CARFORA
# was `first: null, last: null` here while her birth act of 30 December 1830 and
# her marriage act of 21 January 1860 were both published and both cited on her
# own person page. The tree is not the archive and had never been asked to be.
#
# The join is the TREE ID, the same one SLUG uses, never the name — 103 of the
# 294 people here share a name with somebody else on the page. The tree still
# wins when it has a value; this only fills a blank. And it cannot leak a living
# person's date: build_people.py strips b/d from the living before it writes
# people.json, and the living branch below returns before any of this is reached.
_FILLED = collections.Counter()

def fld(p, key):
    """The tree's value if it has one, else the archive's own."""
    v = (p.get(key) or "").strip()
    if v:
        return v
    a = ARCH.get(p.get("id")) or {}
    v = (a.get(key) or "").strip()
    if v:
        _FILLED[key] += 1
    return v

def surname(p):
    return (p.get("last") or "").strip()

def is_placeholder(n):
    """The same rule build_people.py applies, and for the same reason: the tree
    carries rows that are not people. Without it this page counted «UNKNOWN
    Falco», «Unknown Zampiello», and one whose whole name is an address —
    «Arienzo, Caserta, Campania, Italia [Unconfirmed Family] Falco» — as named
    people, which is why 18 of its 294 could never have a person page."""
    n = re.sub(r",? ?[✔⭐]+", "", n or "").strip()
    return (not n) or n.lower().startswith("unknown") or "[" in n

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

# --------------------------------------------------------------------------
# HOW THIS LINE IS REACHED, computed on PEOPLE and never on a surname.
#
# This page used to be built from "any surname in the tree that is not Falco".
# That is a name match, in the archive whose founding rule is that it never
# merges people on a name — and it showed. Three separate women here are called
# Filomena Annecchino; three separate people are called D'Arcy. Grouping by the
# word made them one family each, and produced routes into this line that do
# not exist.
#
# Descent instead:
#   BLOOD    born Falco, or descended from someone who was. A Falco daughter's
#            children are Falco by blood whatever surname they carry — which is
#            how Mia and Rocco Mazza qualify, through their great-grandmother
#            Giuseppina Falco.
#   MARRIED  married somebody in BLOOD.
#   KIN      the blood family a MARRIED person came from — their parents,
#            siblings and descendants. This is what "the Annecchino" means.
#   SECOND   married into one of those families.
CHILD = {"His son", "His daughter", "Her son", "Her daughter"}
SIB   = {"His brother", "His sister", "Her brother", "Her sister",
         "Half sister", "Half brother"}
PAR   = {"His father", "His mother", "Her father", "Her mother"}

def _rel(p, kinds):
    return [r["id"] for r in p.get("relatives", []) if r["rel"] in kinds and r["id"] in byid]

BLOOD = {p["id"] for p in TREE if surname(p) == "Falco"}
_grew = True
while _grew:
    _grew = False
    for _p in TREE:
        if _p["id"] in BLOOD:
            for _k in _rel(_p, CHILD):
                if _k not in BLOOD:
                    BLOOD.add(_k); _grew = True

MARRIED = {}                      # spouse id -> the blood Falco they married
for _i in BLOOD:
    for _s in _rel(byid[_i], SPOUSE):
        if _s not in BLOOD:
            MARRIED.setdefault(_s, _i)

KIN, _q = set(), list(MARRIED)    # the families those spouses came from
while _q:
    _x = _q.pop()
    for _y in _rel(byid[_x], SIB | PAR | CHILD):
        if _y not in BLOOD and _y not in KIN and _y not in MARRIED:
            KIN.add(_y); _q.append(_y)

SECOND = {}
for _i in KIN:
    for _s in _rel(byid[_i], SPOUSE):
        if _s not in BLOOD and _s not in KIN and _s not in MARRIED:
            SECOND.setdefault(_s, _i)

def reach(pid):
    if pid in BLOOD:   return "blood"
    if pid in MARRIED: return "married"
    if pid in KIN:     return "kin"
    if pid in SECOND:  return "second"
    return "unconnected"

groups = collections.defaultdict(lambda: {
    "people": [], "withheld": 0, "places": collections.Counter(),
    "marriages": [], "first": None, "last": None,
    "reach": collections.Counter(), "withheldNames": set()})

for p in TREE:
    sn = surname(p)
    if not sn or sn == "?" or sn.startswith("["):
        continue
    g = groups[sn]
    g["reach"][reach(p["id"])] += 1
    if p.get("alive"):
        g["withheld"] += 1
        g["withheldNames"].add(re.sub(r",? ?[✔⭐]+", "", p["name"]).strip())
        # A LIVING PERSON IS NAMED AND NOTHING MORE — which includes being named
        # as somebody's wife. Skipping these entirely is how Bucolo came to show
        # seven people and no marriage at all: its three Bucolo women married
        # Anthony Falco, Angelo Falco and Angelo Servodio, all six are living, so
        # every one of those marriages was dropped and the family that genuinely
        # married in looked like a family that had married nobody. A name and a
        # relationship is exactly what the rule permits; no date, no place.
        for r in p.get("relatives", []):
            if r["rel"] not in SPOUSE:
                continue
            o = byid.get(r["id"])
            if not o or is_placeholder(o.get("name")):
                continue
            osn = surname(o)
            if osn and osn != sn:
                g["marriages"].append({
                    "who": re.sub(r",? ?[✔⭐]+", "", p["name"]).strip(),
                    "whoSlug": SLUG.get(p["id"], ""),
                    "to": re.sub(r",? ?[✔⭐]+", "", o["name"]).strip(),
                    "toSlug": SLUG.get(o["id"], ""),
                    "into": osn,
                    "living": True})
        continue
    b, dd = year(fld(p, "b")), year(fld(p, "d"))
    for y in (b, dd):
        if y:
            g["first"] = y if g["first"] is None else min(g["first"], y)
            g["last"] = y if g["last"] is None else max(g["last"], y)
    for pl in (place(fld(p, "bp")), place(fld(p, "dp"))):
        if pl:
            g["places"][pl] += 1
    if is_placeholder(p.get("name")):
        continue
    g["people"].append({
        "name": re.sub(r",? ?[✔⭐]+", "", p["name"]).strip(),
        "slug": SLUG.get(p["id"], ""),
        "b": fld(p, "b"), "bp": place(fld(p, "bp")),
        "d": fld(p, "d"), "dp": place(fld(p, "dp")),
    })
    # who they married
    for r in p.get("relatives", []):
        if r["rel"] in SPOUSE:
            o = byid.get(r["id"])
            if not o:
                continue
            osn = surname(o)
            if osn and osn != sn and not is_placeholder(o.get("name")):
                g["marriages"].append({
                    "who": re.sub(r",? ?[✔⭐]+", "", p["name"]).strip(),
                    "whoSlug": SLUG.get(p["id"], ""),
                    "to": re.sub(r",? ?[✔⭐]+", "", o["name"]).strip(),
                    "toSlug": SLUG.get(o["id"], ""),
                    "into": osn,
                    "living": bool(o.get("alive"))})

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
        # A burial does NOT reduce the withheld count. This used to decrement
        # once per grave of the surname, so Bucolo's seven graves — Carmelo,
        # Sebastiano, Palma, Angelo, Filippo, Rosaria, Muriel — took its three
        # living women to zero, and an entry with three people withheld read as
        # none. The narrower repair, decrementing only on an exact name match,
        # is no better: a Carmine Falco at Nudgee and a Carmine Falco alive
        # today are two people, and this archive does not merge records on a
        # name. The tree says who is living; the cemetery index is keyed on a
        # name and cannot outrank it. Where the two overlap, both are shown and
        # neither is collapsed into the other.

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
        # how this surname reaches the line, by the people in it rather than the
        # word: "married" if somebody married a blood Falco, "kin" if they are
        # the family such a person came from, "second" if they married into one
        # of those, "blood" if they descend from a Falco whatever name they carry.
        # burials of this surname that are NOT any withheld person in the tree:
        # same name, same city, very likely the same family — and not proved, so
        # not merged.
        "unjoinedBurials": sum(1 for x in g["people"] if x.get("src") == "Nudgee Cemetery"),
        "reach": sorted(g["reach"], key=lambda k: -g["reach"][k]),
        "reachCount": dict(g["reach"]),
    })

out.sort(key=lambda x: (-x["n"], x["surname"]))
os.makedirs("site/src/data", exist_ok=True)
json.dump(out, open("site/src/data/married-in.json", "w"), indent=1, ensure_ascii=False)
if _FILLED:
    print("  filled from the archive where the tree was blank: "
          + " · ".join(f"{k} {n}" for k, n in sorted(_FILLED.items())))
def _has(x, k): return k in x["reach"]
print(f"{len(out)} surnames · {sum(x['n'] for x in out)} named · "
      f"{sum(x['withheld'] for x in out)} withheld as living · "
      f"{sum(len(x['marriages']) for x in out)} marriages")
print(f"  reaching this line: {sum(1 for x in out if _has(x,'blood'))} carry Falco blood · "
      f"{sum(1 for x in out if _has(x,'married'))} married one · "
      f"{sum(1 for x in out if _has(x,'kin'))} are such a family · "
      f"{sum(1 for x in out if _has(x,'second'))} married into one of those · "
      f"{sum(1 for x in out if x['reach']==['unconnected'])} reach it not at all")
