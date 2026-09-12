#!/usr/bin/env python3
"""Refuse to ship a build that breaks the living-people rule.

David's rule is absolute: living people are named and NOTHING MORE — no date of
birth, no place, no record, no photograph. It has been broken three times with
the same date, twice by code that looked correct in the source:

  1. really_living() reused the ancestor filter for redaction
  2. the timeline positioned living generations at pos(1955) — leaked via geometry
  3. the Lines diagram printed it under "BORN HERE", on /lines AND the home page

Every one of those was found by reading the BUILT HTML, not the source. So this
runs against site/dist and exits non-zero if it finds anything. It is the last
gate before a release, and it is meant to be annoying.
"""
import json, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "site", "dist")
DATA = os.path.join(ROOT, "site", "src", "data")

def load(n): return json.load(open(os.path.join(DATA, n), encoding="utf-8"))

def flat(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))

def main():
    if not os.path.isdir(DIST):
        sys.exit("check_release: no site/dist — build first")

    people = load("people.json")
    living = [p for p in people if p.get("living")]
    liv_names = [p["name"] for p in living if p.get("name")]
    fails = []

    # 1. the graph itself must carry no date for anyone living
    for p in living:
        if p.get("events") or p.get("b") or p.get("d"):
            fails.append(f"people.json: {p['slug']} is living and carries a date/event")

    # 2. a living person's own dates, from the tree, must not sit beside their name
    tree_path = os.path.join(ROOT, "data", "myheritage-falco-tree.json")
    tree = json.load(open(tree_path, encoding="utf-8"))
    tree = tree if isinstance(tree, list) else (tree.get("people") or tree.get("individuals") or [])
    # WHY THIS IS AN EXACT-STRING TEST AND NOT A PROXIMITY ONE.
    #
    # Two earlier designs failed. Screening on BARE YEARS passed vacuously —
    # this is a genealogy site, every year appears somewhere. Screening on a
    # living person's NAME near a date fired on every homonym: a living Luigi
    # Falco shares his name with four dead ones, and HTML cannot tell them
    # apart. Identity lives in the data, not the markup.
    #
    # So: take the FULL DATE STRINGS the source data attaches to a LIVING
    # person and assert those literal strings appear nowhere in the build.
    # That is exactly the leak that reached the front page — line.json carried
    # generation nine's «3 Sep 1955» and a figure printed it verbatim.
    MONTHS = (r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|"
              r"January|February|March|April|June|July|August|September|October|November|December|"
              r"Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre")
    FULL = re.compile(r"\b\d{1,2}\s+(?:" + MONTHS + r")[a-z]*\.?\s+(?:1[89]\d\d|20\d\d)\b")

    lower = {n.strip().lower() for n in liv_names}
    forbidden = {}                      # exact string -> whose it is

    for g in load("line.json"):         # the spine: a living generation's own dates
        if str(g.get("name", "")).split(" (")[0].strip().lower() in lower:
            for k in ("born", "died", "married", "spouseBorn"):
                for d in FULL.findall(str(g.get(k) or "")):
                    forbidden[d] = f"{g.get('name')} (line.json {k})"
                m = FULL.search(str(g.get(k) or ""))
                if m:
                    forbidden[m.group(0)] = f"{g.get('name')} (line.json {k})"

    for x in tree:                      # the tree: living people's own dates
        nm = str(x.get("name", "")).split(" (")[0].strip()
        if nm.lower() not in lower:
            continue
        for k in ("b", "d"):
            m = FULL.search(str(x.get(k) or ""))
            if m:
                forbidden[m.group(0)] = f"{nm} (tree {k})"

    pages = glob.glob(os.path.join(DIST, "**", "index.html"), recursive=True)
    for f in pages:
        txt = flat(open(f, encoding="utf-8", errors="replace").read())
        for d, whose in forbidden.items():
            if d in txt:
                fails.append(f"{os.path.relpath(f, DIST)}: contains '{d}' — {whose} IS LIVING")

    print(f"check_release: guarding {len(forbidden)} date string(s) belonging to living people"
          + (": " + ", ".join(sorted(forbidden)) if forbidden else " — NONE FOUND, the guard is watching nothing"))

    # 3. every living person's own page must be noindexed
    person_pages = {p["slug"] for p in living}
    for f in pages:
        raw = open(f, encoding="utf-8", errors="replace").read()
        slug = os.path.basename(os.path.dirname(f))
        if slug in person_pages and 'content="noindex' not in raw:
            fails.append(f"{os.path.relpath(f, DIST)}: living person's own page is INDEXED")

    NOINDEX = 'content="noindex'
    n_noindex = sum(1 for f in pages
                    if NOINDEX in open(f, encoding="utf-8", errors="replace").read())
    print(f"check_release: {len(pages)} pages, {len(living)} living people, {n_noindex} noindexed")
    if fails:
        print("\nFAILED — the living-people rule is broken:\n")
        for x in sorted(set(fails))[:40]:
            print("   ", x)
        sys.exit(1)
    print("check_release: clean — no living person carries a date, no living person's page is indexed")

if __name__ == "__main__":
    main()
