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

# WHICH BUILD THIS GATE READS, and why the ENVIRONMENT beats the flag.
#
# `--dist` lets this gate run against an isolated build, because another
# session builds into site/dist continuously and reading that directory
# mid-write is how this check once came back with a missing page that was
# never missing. That much was already here. What was missing is the other
# half: the estate standardised on ARCHIVE_OUT, and this tool never read it.
#
# On 27 September 2026 that produced the failure this gate exists to prevent,
# in reverse. Run without a flag it graded site/dist — 9,492 pages, built the
# previous day — and reported TWO LIVING PEOPLE'S PAGES AS INDEXED. Both
# carry `<meta name="robots" content="noindex, nofollow">` in the build that
# had just been made. Nothing had leaked; the gate was grading a build nobody
# made.
#
# THE SYMMETRIC FAILURE IS THE ONE THAT MATTERS. A gate reading a stale dist
# can equally report GREEN on a build where the leak is real, and nobody
# looks twice at a green living-people check. This is the one rule in this
# archive that must never be wrong.
#
# The environment wins over the flag deliberately, which is the kit's rule and
# the opposite of the usual order: `--dist dist` in package.json is the
# repository's default — what to read when nobody has said otherwise —
# while ARCHIVE_OUT is an operator saying «read THIS build, the one I just
# made». The kit's outdir.resolve is used when it can be imported so this
# tool cannot drift from the estate; the fallback does the same thing, so a
# moved kit leaves this gate correct rather than silently back where it was.
_flag = sys.argv[sys.argv.index("--dist") + 1] if "--dist" in sys.argv else "dist"
try:
    sys.path.insert(0, os.path.join(ROOT, "site", "node_modules", "@daviddef",
                                    "archive-kit", "kit", "tools"))
    from outdir import resolve as _resolve          # type: ignore
except Exception:
    def _resolve(d):
        _o = os.environ.get("ARCHIVE_OUT")
        if not _o:
            return d
        _p = os.path.dirname((d or "").rstrip("/\\"))
        return os.path.join(_p, _o) if _p else _o
DIST = os.path.join(ROOT, "site", _resolve(_flag))
DATA = os.path.join(ROOT, "site", "src", "data")

def load(n): return json.load(open(os.path.join(DATA, n), encoding="utf-8"))

def flat(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))

def main():
    if not os.path.isdir(DIST):
        sys.exit(f"check_release: no {os.path.relpath(DIST, ROOT)} — build first "
                 f"(ARCHIVE_OUT={os.environ.get('ARCHIVE_OUT') or 'unset'})")

    people = load("people.json")
    def _alive(rows):
        """Who this gate treats as living. A function so the self-test below
        runs THE REAL detection rather than a copy of it."""
        return [p for p in rows if p.get("living")]

    living = _alive(people)
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

    def _harvest(rows, label):
        """Pull every full date a LIVING person carries out of `rows`.

        Extracted so the self-test below can run the REAL path rather than a
        copy of it. A test that exercises a duplicate of the code proves only
        that the duplicate works.
        """
        got = {}
        for x in rows:
            nm = str(x.get("name", "")).split(" (")[0].strip()
            if nm.lower() not in lower:
                continue
            for k in ("b", "d"):
                m = FULL.search(str(x.get(k) or ""))
                if m:
                    got[m.group(0)] = f"{nm} ({label} {k})"
        return got

    forbidden.update(_harvest(tree, "tree"))

    # A GUARD WATCHING NOTHING IS INDISTINGUISHABLE FROM A GUARD THAT HAS
    # STOPPED WORKING, and this one watches nothing: all 106 living people
    # carry no date in any source, so `forbidden` is empty and the scan below
    # has no work. That is the living-people rule being upheld UPSTREAM, which
    # is the right place — but it means a break anywhere in the gathering path
    # above (the living-name set, the date pattern, a source that stopped
    # loading) would produce exactly the same silence, and the gate would go on
    # printing a reassuring line for ever.
    #
    # So when it finds nothing, it proves it still CAN find something: a
    # synthetic record for a real living person, run through the real harvest.
    # AND THE INVERSE FAILURE, WHICH IS THE ONE THAT MATTERS MOST.
    #
    # The self-test below was first written as `if not forbidden and lower`,
    # which cannot fire when `lower` is EMPTY — that is, in exactly the case
    # where this gate has stopped seeing living people at all. Proved on
    # 27 September 2026 by renaming the `living` key the way an upstream
    # change would: the gate printed «0 living people» and «clean — no living
    # person carries a date, no living person's page is indexed» and EXITED
    # ZERO. A guard built so it cannot fire in the worst case is not a guard.
    #
    # Zero living people is a FINDING for an archive that has none and a
    # FAILURE TO LOOK for this one, and the gate cannot tell which from the
    # outside — so it asks the detection to prove itself.
    if not living:
        if not _alive([{"name": "Self Test", "living": True}]):
            fails.append("THE LIVING-PEOPLE DETECTION CANNOT FIRE. This gate finds nobody "
                         "living, and a synthetic person flagged living was not detected "
                         "either — so «nobody is flagged living» is not evidence of anything. "
                         "The flag has most likely been renamed upstream.")
            # NOT «no living person reaches the build» — that claim is stronger
            # than this archive enforces. Under the named-bare policy a living
            # person's NAME does reach the build, by design: David's rule is a
            # name and a relationship and nothing else. What is enforced, and
            # all this gate may claim, is that no living person carries a DATE
            # and no living person's page is INDEXED.
        else:
            print("check_release: NOBODY IS FLAGGED LIVING — the detection was self-tested "
                  "and works, so this is a finding and not a broken gate")

    if not forbidden and lower:
        _probe = _harvest([{"name": sorted(lower)[0], "b": "1 January 1801"}], "self-test")
        if not _probe:
            fails.append("THE DATE GUARD CANNOT FIRE. It reports no dates to watch, and a "
                         "synthetic date on a known living person did not register either — "
                         "so the empty result is not evidence that the rule is being kept.")

    pages = glob.glob(os.path.join(DIST, "**", "index.html"), recursive=True)
    for f in pages:
        txt = flat(open(f, encoding="utf-8", errors="replace").read())
        for d, whose in forbidden.items():
            if d in txt:
                fails.append(f"{os.path.relpath(f, DIST)}: contains '{d}' — {whose} IS LIVING")

    # NAME WHAT WAS EXAMINED, NOT WHAT WAS HANDED.
    #
    # «guarding 0 date strings» is true and says nothing about coverage. The
    # number that carries the meaning is how many living people this guard
    # could look at — those the sources give a date for — against how many
    # there are. «0 of 106 living people carry a date anywhere» is the rule
    # being kept; «0 of 0» would be the guard having lost the corpus.
    #
    # The estate learned this from the kit's kin gate, which reported «866
    # people · 1 impossible relationship» while examining 119 of them, because
    # every test it makes needs both a birth and a death. A ratio nobody
    # prints is a ratio nobody checks.
    print(f"check_release: guarding {len(forbidden)} date string(s) belonging to living people"
          # ALWAYS STATE THE RELATION BETWEEN NAMES AND PEOPLE, even when it is
          # one-to-one. This guard works on NAMES, so a per-person count can
          # never be recovered from a per-name count — the difference can only
          # be explained, never reconciled. Printing the explanation only when
          # the gap exists means that once it closes, A MISSING EXPLANATION AND
          # AN ABSENT GAP LOOK THE SAME, which is the ambiguity this line was
          # added to remove.
          + f" — examined {len(lower)} distinct living name(s) for {len(living)} living people"
          + (f", {len(living) - len(lower)} of whom share a name with another"
             if len(living) > len(lower) else ", none of whom share a name")
          + f"; {len(forbidden)} of those names carry a date"
          + (": " + ", ".join(sorted(forbidden)) if forbidden
             else "; NONE DO, so this guard has nothing to watch and said so"))

    # 3. every living person's own page must be noindexed
    person_pages = {p["slug"] for p in living}
    _matched = set()
    for f in pages:
        raw = open(f, encoding="utf-8", errors="replace").read()
        slug = os.path.basename(os.path.dirname(f))
        if slug in person_pages:
            _matched.add(slug)
            if 'content="noindex' not in raw:
                fails.append(f"{os.path.relpath(f, DIST)}: living person's own page is INDEXED")

    # AND SAY HOW MANY OF THEM IT ACTUALLY FOUND — work-list row 98.
    #
    # This test fires only where a built page's directory name equals a living
    # person's slug. A living person whose page is not built, or is built under
    # a different slug, is not examined and NOTHING SAYS SO: the loop simply
    # never matches them and the verdict still reads «no living person's page is
    # indexed». That is the same shape as the empty-corpus failure this file was
    # already caught by — a guard passing because it looked at nothing.
    _unmatched = sorted(person_pages - _matched)
    print(f"check_release: the noindex test matched {len(_matched)} of "
          f"{len(person_pages)} living person slug(s) to a built page"
          + ("" if not _unmatched else
             f" — {len(_unmatched)} "
             + ("HAS" if len(_unmatched) == 1 else "HAVE")
             + " NO PAGE UNDER THEIR SLUG and " 
             + ("was" if len(_unmatched) == 1 else "were")
             + " not examined: " + ", ".join(_unmatched[:6])
             + (" …" if len(_unmatched) > 6 else "")))

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
        # SINCE 23 SEPTEMBER 2026 THE TWO FILES ARE MATCHED ON THE HOUSEHOLD'S
        # id, NOT ON ITS NAME. The map below is what matching on a display
        # string cost: «Francesco Cossi & Maria Falco» was corrected to
        # «Francesco Cioffi & Maria Falco» in one file and not the other, and a
        # hand-written rename table had to be carried here so the gate would
        # not fail on the archive's own correction. With an id, a rename is one
        # field and this table is dead weight — kept only for TSV rows written
        # before the id existed.
        _RENAME = {"Francesco Cossi & Maria Falco": "Francesco Cioffi & Maria Falco"}
        _BY_ID = {h.get("id"): h["name"] for h in _H if h.get("id")}
        _have = {(h["name"], m.get("person", ""), m.get("event") or "", m.get("date") or "")
                 for h in _H for m in h["members"]}
        _names = {h["name"] for h in _H}
        _idbad = []
        _missing = []
        for _r in _csv.DictReader(open(_tsv, encoding="utf-8"), delimiter="\t"):
            _hid = (_r.get("hid") or "").strip()
            if _hid:
                if _hid not in _BY_ID:
                    _idbad.append(f"hid not in households.json: {_hid} ({_r['household']})")
                    continue
                if _BY_ID[_hid] != _r["household"]:
                    _idbad.append(f"{_hid}: TSV calls it {_r['household']!r}, "
                                  f"JSON calls it {_BY_ID[_hid]!r}")
                _n = _BY_ID[_hid]
            else:
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
        if _idbad:
            print(f"\nFAILED — {len(_idbad)} row(s) whose household id does not resolve:")
            for _x in _idbad[:12]:
                print("    " + _x)
            # AND IT MUST ACTUALLY FAIL. The first version of this check set a
            # flag no other line read, so it printed FAILED in red and exited
            # zero — a gate that reports and does not refuse is the same thing
            # as no gate, which is the fault this whole night has been about.
            sys.exit(1)
        print(f"check_release: households.tsv {'in step with' if not _missing else 'AHEAD OF'} households.json")
        print(f"check_release: and the two agree on the evidence, row for row")
        if _missing:
            print(f"\nFAILED — {len(_missing)} row(s) in data/households.tsv are not in the file the")
            print("site builds from. Findings written there will not appear on the archive:\n")
            for _x in _missing[:20]:
                print("   ", _x)
            sys.exit(1)

    # SAY WHICH BUILD WAS GRADED, AND HOW OLD IT IS.
    #
    # On 27 September 2026 this gate reported two living people's pages as
    # INDEXED. They were not: it had graded a day-old site/dist while the
    # build just made was correct. The reading was accurate about the
    # directory and said nothing about WHICH directory, so the only way to
    # discover that was to go and count the pages by hand. One line here
    # would have settled it in a second, and the same line settles the
    # dangerous case — a stale build reporting GREEN — just as fast.
    import datetime as _dt
    _age = _dt.datetime.fromtimestamp(os.path.getmtime(DIST)).strftime("%Y-%m-%d %H:%M")
    print(f"check_release: graded {os.path.relpath(DIST, ROOT)} — {len(pages)} pages, "
          f"last written {_age}"
          + (f" · ARCHIVE_OUT={os.environ['ARCHIVE_OUT']}" if os.environ.get("ARCHIVE_OUT") else ""))
    print(f"check_release: {len(pages)} pages, {len(living)} living people, {n_noindex} noindexed")
    if fails:
        print("\nFAILED — the living-people rule is broken:\n")
        for x in sorted(set(fails))[:40]:
            print("   ", x)
        sys.exit(1)
    print("check_release: clean — no living person carries a date, no living person's page is indexed")

if __name__ == "__main__":
    main()
