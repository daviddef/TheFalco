#!/usr/bin/env python3
"""Refuse to ship when a person this archive has documented is told they are undocumented.

THE FAULT THIS GUARDS AGAINST, which the Mazza archive had and the estate
landing page caught. Mazza kept evidence in `documented-additions.tsv` (keyed to
a person by an `inTree` column) and `corrections.tsv` (keyed by `slug`), and the
script that built per-person data read NEITHER. Twelve people whose evidence was
sitting on disk had pages reading «No record has been read for this person …
what is known of them is what the tree asserts, and it is unverified».

**The data was fine. The build dropped it, and nothing refused.**

This archive's equivalent sentence is in `site/src/pages/people/[slug].astro`:

    No act has been read for this person. What is known of them comes from the
    family tree, and is unverified

and it is printed whenever `p.events` is empty. So the test is simple and it is
the one Mazza needed: **if households.json carries evidence for a name, some
person page for that name must carry an event.**

ONE CHECK, and it is the one Mazza needed:

  EVIDENCE MUST REACH A PAGE. Every person named in `households.json` with an
  `evidence` string or a real `event` must resolve to at least one person in
  `people.json` who has at least one event. A living person is exempt — this
  archive publishes their name and nothing else, on purpose, and the page says
  so in its own words rather than claiming nothing was read.

A SECOND CHECK WAS WRITTEN HERE AND THEN REMOVED, and the reason is worth
keeping. It compared `data/households.tsv` row by row against
`site/src/data/households.json`, on the belief that `check_release.py` compared
only HOUSEHOLD NAMES and would miss a row adding a person to a household that
already existed. **That belief was wrong.** `check_release.py` already keys on
`(household, person, event, date)` — tested by appending an orphan row to the
TSV, which it caught and refused. The duplicate was deleted rather than shipped.

Run:  python3 tools/check_person_evidence.py
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
J = lambda p: json.load(io.open(P(*p.split("/")), encoding="utf-8"))

TICKS = re.compile(r"[✔⭐]")
PAREN = re.compile(r"\s*\(.*?\)\s*")


def clean(s):
    """The archive's own name-cleaning: drop the bracketed gloss and the ticks."""
    return re.sub(r"\s+", " ", PAREN.sub(" ", TICKS.sub("", str(s or "")))).strip().lower()


fails = []

# ---------------------------------------------------------------- check one
H = J("site/src/data/households.json")
people = J("site/src/data/people.json")

documented = {}                       # cleaned name -> a sample of what documents it
for h in H:
    for m in h["members"]:
        has_event = (m.get("event") or "").strip() not in ("", "—")
        has_ev = bool((m.get("evidence") or "").strip())
        if has_event or has_ev:
            documented.setdefault(clean(m["person"]), (h["name"], m.get("event") or "named",
                                                       m.get("date") or "—"))

by_name = {}
for p in people:
    by_name.setdefault(clean(p["name"]), []).append(p)

for nm, (hh, ev, date) in sorted(documented.items()):
    pages = by_name.get(nm, [])
    if not pages:
        fails.append(f"documented but has NO person page: «{nm}» — {hh}, {ev} {date}")
        continue
    if any(p.get("living") for p in pages):
        continue                      # name-only by policy, and the page says so
    if not any(p.get("events") for p in pages):
        slugs = ", ".join(p["slug"] for p in pages[:4])
        fails.append(
            f"documented but EVERY page says nothing was read: «{nm}» — {hh}, "
            f"{ev} {date}  [pages: {slugs}]")

print(f"check_person_evidence: {len(documented)} names documented in households.json, "
      f"{len(people)} people built")

# ---------------------------------------------------------------- verdict
if fails:
    print(f"\nFAILED — {len(fails)} person(s) documented by this archive whose page "
          f"tells the reader nothing has been read:\n")
    for f in fails:
        print("  " + f)
    print("\nThe data is on disk. Something in the build is dropping it before it "
          "reaches the person.")
    sys.exit(1)

print("check_person_evidence: clean — every documented person's page carries their evidence")
