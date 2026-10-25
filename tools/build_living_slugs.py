#!/usr/bin/env python3
"""Write private/living-slugs.json: the slugs of every person people.json marks living.

The kit's lines gate (checklines.py --living) refuses a living person as a lane or pen member. It wants a list of
slugs; the archive's living list (private/living-links.json) holds names, so this writes the slugs from the
published person graph (the same `living` flag the person pages are built from, itself the kit's one rule).
The file is under private/, which is gitignored, and holds slugs only; it is rebuilt on every run.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
people = json.load(open(os.path.join(ROOT, "site", "src", "data", "people.json"), encoding="utf-8"))
slugs = sorted(p["slug"] for p in people if p.get("living"))
if not slugs:
    raise SystemExit("build_living_slugs: no living person in people.json; refusing to write an empty list the gate would pass on")
out = os.path.join(ROOT, "private", "living-slugs.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump({"slugs": slugs}, f, indent=1)
print("build_living_slugs: %d living slugs -> private/living-slugs.json" % len(slugs))
