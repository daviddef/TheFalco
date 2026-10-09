#!/usr/bin/env python3
"""Does every FamilySearch citation point at an image that volume actually has?

WHY THIS EXISTS.

On 8 October 2026 this archive wrote `3:1:3QSQ-G976-QHD5` into a citation for
image 144 of waypoint `MC55-FNT`. **There is no such ark.** It was invented —
assembled out of the shape of its neighbours — and it was caught by eye, before
any commit, by one person who happened to look twice. Nothing in the build
could have caught it: `checkarchive` verifies that links reach pages, and no
gate has ever opened a FamilySearch image.

It does not need to. **The ark index is on disk**: `tools/fswaypoint.py` walked
the open waypoint API and wrote every image number and its ark into
`data/*-tribunale-images.tsv`, 6,405 of them across three volumes. So a citation
that names a waypoint, an image number and an ark can be checked against the
volume's own manifest without fetching anything:

- does that waypoint have an image of that number?
- is the ark the one the manifest gives for it?

**Both failures are silent and both are fatal to a reader**: a citation one
image out sends the next person to a stranger's act, and an invented ark sends
them to a 404 they will read as "the archive is wrong" rather than "the citation
is". Antenati citations have `tools/citation_check.py`, which ranks them for a
human to open; this is the FamilySearch half, and it needs no human and no
network.

    python3 tools/check_fscite.py

Exit 1 on any citation whose ark and image disagree with the manifest.
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = {"MC55-FNT": "data/arienzo-fs-tribunale-images.tsv",
       "MC5R-M2Q": "data/smav-fs-tribunale-images.tsv",
       "MC5R-Q23": "data/smav-q23-tribunale-images.tsv"}

ark_of, img_of = {}, {}
for wp, path in TSV.items():
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        continue
    for line in open(full, encoding="utf-8").read().splitlines()[1:]:
        f = line.split("\t")
        if len(f) > 3 and f[1] == wp:
            ark_of[(wp, int(f[2]))] = f[3]
            img_of[f[3]] = (wp, int(f[2]))

# «FamilySearch 3:1:3QS7-8976-Q4F8 — image 144 of waypoint MC55-FNT»
CITE = re.compile(r"(3:1:[0-9A-Z-]+)\s*—\s*image\s+(\d+)\s+of\s+waypoint\s+(MC\S+?)[,\s]", re.I)
# a waypoint and an image with no ark at all
BARE = re.compile(r"\bimage\s+(\d+)\s+of\s+waypoint\s+(MC\S+?)[,\s]", re.I)

H = json.load(open(os.path.join(ROOT, "site/src/data/households.json"), encoding="utf-8"))
checked = fails = bare = 0
problems = []
for h in H:
    for m in h["members"]:
        a = m.get("ark") or ""
        hit = CITE.search(a)
        if not hit:
            if BARE.search(a):
                bare += 1
                problems.append(("NO ARK", h["id"], m["person"], a[:90]))
            continue
        ark, img, wp = hit.group(1), int(hit.group(2)), hit.group(3)
        checked += 1
        if wp not in TSV:
            problems.append(("UNKNOWN WAYPOINT", h["id"], m["person"], f"{wp}"))
            fails += 1
        elif (wp, img) not in ark_of:
            problems.append(("NO SUCH IMAGE", h["id"], m["person"], f"{wp} has no image {img}"))
            fails += 1
        elif ark_of[(wp, img)] != ark:
            where = img_of.get(ark)
            says = f" — that ark is image {where[1]} of {where[0]}" if where else " — that ark is in no manifest here"
            problems.append(("ARK MISMATCH", h["id"], m["person"],
                             f"{wp} image {img} is {ark_of[(wp,img)]}, the citation says {ark}{says}"))
            fails += 1

print(f"  check_fscite: {checked} FamilySearch citation(s) checked against "
      f"{len(ark_of)} image arks in {len(TSV)} volume manifest(s)")
if bare:
    print(f"    note  {bare} citation(s) name a waypoint and an image but NO ARK — "
          f"nothing here can verify those, and they are counted so the number is visible")
for kind, hid, who, what in problems:
    print(f"    {'FAIL ' if kind != 'NO ARK' else 'note '} {kind}: {who} ({hid}) — {what}")
if fails:
    print(f"  check_fscite: {fails} citation(s) point where the volume does not")
    sys.exit(1)
print("  check_fscite: clean — every cited ark is the one its volume gives for that image")
