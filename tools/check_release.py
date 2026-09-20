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
# --dist lets this gate run against an isolated build. Another session builds into
# site/dist continuously, and reading that directory mid-write is how this check
# once came back with a missing page that was never missing.
DIST = os.path.join(ROOT, "site",
                    sys.argv[sys.argv.index("--dist") + 1] if "--dist" in sys.argv else "dist")
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
    # The tree export is the private source: it carries every living person in
    # full, so it is gitignored and CI never sees it. Absent, this guard runs on
    # the committed data alone — which is the material that actually ships — and
    # says so rather than quietly checking less than it claims.
    tree_path = os.path.join(ROOT, "data", "myheritage-falco-tree.json")
    if os.path.exists(tree_path):
        tree = json.load(open(tree_path, encoding="utf-8"))
        tree = tree if isinstance(tree, list) else (tree.get("people") or tree.get("individuals") or [])
    else:
        tree = []
        print("check_release: no myheritage-falco-tree.json — the private export is not "
              "in this checkout, so the tree's own dates cannot be screened. line.json "
              "and people.json still are, and so is every page.")
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
    # --- the two household files must not drift apart again -----------------
    #
    # data/households.tsv is where this archive's reconstructed families are
    # written; site/src/data/households.json is what the site is BUILT from.
    # They silently diverged once, and two days of findings sat in the TSV
    # while the site showed none of them — and the TSV kept a household name
    # the JSON had already corrected, so a retracted reading was republished
    # from it. Every TSV row must be present in the JSON.
    import csv as _csv
    _tsv = os.path.join(ROOT, "data", "households.tsv")
    _js  = os.path.join(ROOT, "site", "src", "data", "households.json")
    if os.path.exists(_tsv) and os.path.exists(_js):
        _H = json.load(open(_js, encoding="utf-8"))
        _RENAME = {"Francesco Cossi & Maria Falco": "Francesco Cioffi & Maria Falco"}
        _have = {(h["name"], m.get("person", ""), m.get("event") or "", m.get("date") or "")
                 for h in _H for m in h["members"]}
        _names = {h["name"] for h in _H}
        _missing = []
        for _r in _csv.DictReader(open(_tsv, encoding="utf-8"), delimiter="\t"):
            _n = _RENAME.get(_r["household"], _r["household"])
            if _n not in _names:
                _missing.append(f"household absent from households.json: {_n}")
            elif (_n, _r["person"], _r["event"], _r["date"]) not in _have:
                _missing.append(f"{_n}: {_r['person']} / {_r['event']} / {_r['date']}")
        # AND THE EVIDENCE, NOT ONLY THE NAMES.
        #
        # For months this compared only (household, person, event, date), so two
        # files could agree on WHO was in a household and disagree on WHAT THE
        # DOCUMENT SAID about them — and they did, on sixty rows. The worst of
        # them: «Magdalenae RIVETTA» was read from the image on 14 September,
        # written into the TSV, and never into the JSON, so the site published
        # the OCR guess «Pivera» for six days. Two rows asserted a man «alive»
        # from a signal this archive had itself disproved, because the downgrade
        # reached the TSV alone.
        #
        # Compared on WHITESPACE-FLATTENED text, because the TSV cannot hold a
        # newline and the JSON is written in paragraphs. A row may carry several
        # entries under one key — a person legitimately appears twice under one
        # date — so the TSV matches if it equals ANY of them.
        _ev = {}
        for _h in _H:
            for _m in _h["members"]:
                _k = (_h["name"], _m.get("person", ""), _m.get("date") or "")
                _e = " ".join((_m.get("evidence") or "").split())
                _ev.setdefault(_k, set()).add(_e)
        _drift = []
        for _r in _csv.DictReader(open(_tsv, encoding="utf-8"), delimiter="\t"):
            _n = _RENAME.get(_r["household"], _r["household"])
            _k = (_n, _r["person"], _r["date"])
            if _k not in _ev:
                continue
            if " ".join((_r.get("evidence") or "").split()) not in _ev[_k]:
                _drift.append(f"{_n}: {_r['person']} / {_r['date']}")
        if _drift:
            print(f"\nFAILED — {len(_drift)} row(s) where the two household files disagree about")
            print("WHAT THE DOCUMENT SAYS. One of them is on the site and one of them is not:\n")
            for _x in _drift[:20]:
                print("   ", _x)
            print("\nMirror the one that is right into the other. Do NOT bulk-copy: the newer text")
            print("is not always the longer one, and a row may hold a reading the other has lost.")
            sys.exit(1)
        print(f"check_release: households.tsv {'in step with' if not _missing else 'AHEAD OF'} households.json")
        print(f"check_release: and the two agree on the evidence, row for row")
        if _missing:
            print(f"\nFAILED — {len(_missing)} row(s) in data/households.tsv are not in the file the")
            print("site builds from. Findings written there will not appear on the archive:\n")
            for _x in _missing[:20]:
                print("   ", _x)
            sys.exit(1)

    print(f"check_release: {len(pages)} pages, {len(living)} living people, {n_noindex} noindexed")
    if fails:
        print("\nFAILED — the living-people rule is broken:\n")
        for x in sorted(set(fails))[:40]:
            print("   ", x)
        sys.exit(1)
    print("check_release: clean — no living person carries a date, no living person's page is indexed")

if __name__ == "__main__":
    main()
