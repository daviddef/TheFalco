#!/usr/bin/env python3
"""The prose gate for living people: run the kit's checkprose.py over what this archive's authors type.

    python3 ../tools/check_living_prose.py                  # from site/ (what `npm run check:living-prose` and the build run)
    python3 ../tools/check_living_prose.py --require-tree   # a run without the tree is a FAILURE, even in CI

(The older tools/check_prose.py is a different gate: it refuses pages that repeat a retired COVERAGE claim.)

checkprose.py (kit/tools) fails when a hand-written page, a hand-edited data file or a note puts a year, a date
or a life-event word beside a living person's name, or when a JSON record naming a living person carries a field
beyond the standard (name, relationships, full town and country). tools/check_living_v2.py and check_release.py
guard the BUILT pages and the generated data; this guards what somebody typed.

THE FEED. Who is living is answered by tools/build_checkprose_feed.py with the kit's living_rule.py over the
private MyHeritage tree. The feed holds names, so it lives in private/ (gitignored) or at $CHECKPROSE_FEED, and is
rebuilt on every run so it is never stale. Held-out people (undated, with a living parent) are fed as living.

THE WORD "LIVING" IN THE REGISTERS. A register row that says a parent was "living" (Italian: vivente) at an act of
the 1800s describes a dead person. Nothing here reads that word: the feed comes from the tree and the rule only.

EXIT CODES. 0 passed. 1 failed. 2 NOT RUN: the tree is not on this machine, so nobody can say who is living, and
"cannot say" is not "nobody is". On David's machine that stops the build. In CI (the environment variable CI is
set: GitHub Actions sets it) the build goes on and the log says, in capitals, that this gate did not run;
--require-tree turns that into a failure there too.

WHICH FILES (see HAND_EDITED, GENERATED, TABLES below). The kit reads, by default, site/src/pages,
site/src/content, notes/, docs/ and the top-level markdown; this adds the hand-EDITED data files and the
components and layouts (a sentence can be typed there). A tracked data file that is in no list FAILS the gate,
so that a new file has to be classified by somebody who knows whether a person edits it or a script writes it.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KIT_TOOLS = os.path.join(ROOT, "site", "node_modules", "@daviddef", "archive-kit", "kit", "tools")
CHECKPROSE = os.path.join(KIT_TOOLS, "checkprose.py")
ALLOW = os.path.join(ROOT, "checkprose-allow.json")
SITE_DATA = "site/src/data"
TSV_DATA = "data"

# site/src/data files a person edits (or a research session appends to). Each is read by the gate.
HAND_EDITED = {
    "apart.json",           # the separated lines, written by hand
    "corrections.json",     # the archive's own corrections log, appended by hand
    "diaspora.json",        # towns and processetti notes
    "dna.json",             # the two DNA tests and what they read
    "errands.json",         # the doors still to be tried
    "families.json",        # the family pages' prose
    "households.json",      # the reconstructed households, built up by hand from the registers
    "line.json",            # the direct line, the spine of the archive
    "parent-verdicts.json",  # verdicts on parent edges, decided by a person
    "person-joins.json",    # reasoned overrides that join or split people
    "places.json",          # the towns' notes
    "plates.json",          # the captions of the plates
    "processetti.json",     # the marriage dossiers, read by hand
    "questions.json",       # the open questions
    "searched.json",        # the coverage page, one row per search
    "sources.json",         # the sources list
    "strands.json",         # the strands chart's captions
    "trees.json",           # the trees' notes
    "worklist.json",        # the work list
}

# site/src/data files a script writes. The generator's own scrub gate (check_living_v2.py, check_release.py,
# the kit's checkliving.py) is the guard; scanning them here would only meet homonyms, and a fix would be
# undone by the next run of the generator.
GENERATED = {
    "changes.json",         # build_changes.py, from git
    "married-in.json",      # build_marriedin.py
    "namefold.json",        # kit/tools/namefold.py ("run it again rather than editing it")
    "people-aliases.json",  # build_people.py, slug redirects
    "people.json",          # build_people.py; scrubbed to the standard and checked by check_living_v2.py
    "person-slugs.json",    # build_people.py, the slug ledger
    "register.json",        # build_register.py
    "researchlog.json",     # build_researchlog.py, from notes/
    "searchindex.json",     # build_searchindex.py
}

# data/ (the tab-separated tables and the ledger). Two kinds are NOT read:
#   GENERATED_TABLES  written by build_register.py / build_people.py / citation_check.py from the data above. The
#                     register carries the tree's own text about each dead person ("His daughter ..."), so a
#                     living relative's name sits beside a dead person's dates by construction; the generator's
#                     scrub (check_living_v2.py, check_release.py) is the guard, not a proximity test.
# Every other tracked table under data/ IS read: direct-line.tsv is typed by hand, and the rest are rows copied
# from a record office's index (Antenati, FamilySearch, Findmypast, NAA, Queensland BDM, cemetery lists) by a
# script or by hand. A living namesake of a man in a register shows up there, and is allowed once, with a reason.
# data/antenati-ids/ holds one JSON file of image ids per Antenati volume (no names) and is not read.
GENERATED_TABLES = {"people-register.tsv", "slug-ledger.txt", "citation-check.json", "living-feed.json", "living-by-inference.json"}  # living-feed.json: written by tools/living_feed.py, keyed hashes only; living-by-inference.json: written by tools/living_by_inference.py, tree ids and the rule text only (David edits only its "overridden" list)
TABLE_DIRS_NOT_READ = {"data/antenati-ids"}

# The JSON fields a living person's line.json entry may carry besides the kit's default (name, relationships,
# place): the generator keeps exactly these (tools/build_people.py _LINE_KEEP; check_living_v2.py LINE_KEYS).
# `gen` is the generation number (a relationship), `confidence` how sure the identification is.
ALLOW_KEYS = "gen,confidence"

# Prose that is typed outside src/pages and notes/*.md: components and layouts (a sentence can be typed there).
EXTRA_INCLUDE = ["site/src/components/**/*.astro", "site/src/layouts/**/*.astro"]


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def tracked(prefix):
    r = subprocess.run(["git", "-C", ROOT, "ls-files", "-z", prefix], capture_output=True, text=True)
    return sorted(f for f in r.stdout.split("\0") if f)


def classify():
    """Return (include list, problems)."""
    problems = []
    names = [os.path.basename(f) for f in tracked(SITE_DATA) if os.path.dirname(f) == SITE_DATA]
    for n in names:
        if n not in HAND_EDITED and n not in GENERATED:
            problems.append("%s/%s is in neither HAND_EDITED nor GENERATED in tools/check_living_prose.py: say "
                            "whether a person edits it or a script writes it" % (SITE_DATA, n))
    for n in sorted((HAND_EDITED | GENERATED) - set(names)):
        problems.append("tools/check_living_prose.py lists %s/%s, which is not a tracked file" % (SITE_DATA, n))
    for n in sorted(HAND_EDITED & GENERATED):
        problems.append("%s is listed as both hand-edited and generated" % n)
    # the tables under data/: read unless generated; anything that is not a .tsv has to be classified.
    tbl = [f for f in tracked(TSV_DATA)]
    tables = []
    for f in tbl:
        n = os.path.basename(f)
        d = os.path.dirname(f)
        if d in TABLE_DIRS_NOT_READ:
            continue
        if d != TSV_DATA:
            problems.append("%s is in a data/ subdirectory this gate does not know: say whether it is read" % f)
        elif n in GENERATED_TABLES:
            continue
        elif n.endswith(".tsv"):
            tables.append(f)
        else:
            problems.append("%s is not a .tsv table and is not in GENERATED_TABLES in tools/check_living_prose.py: "
                            "say whether a person edits it or a script writes it" % f)
    for n in sorted(GENERATED_TABLES - {os.path.basename(f) for f in tbl}):
        problems.append("tools/check_living_prose.py lists data/%s, which is not a tracked file" % n)
    return ["%s/%s" % (SITE_DATA, n) for n in sorted(HAND_EDITED)] + tables, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--require-tree", action="store_true",
                    help="a run without the tree (nobody can say who is living) fails even in CI")
    ap.add_argument("--feed", help="where to write the feed (default: $CHECKPROSE_FEED or private/checkprose-feed.json)")
    ap.add_argument("--tree")
    a = ap.parse_args(argv)

    if not os.path.exists(CHECKPROSE):
        print("check_living_prose: FAIL, the kit has no checkprose.py at %s (pin the kit at 26a4cba or later)" % CHECKPROSE)
        return 1
    include, problems = classify()
    if problems:
        print("check_living_prose: FAIL (%d)" % len(problems))
        for p in problems:
            print("  - " + p)
        return 1

    fb = load_module(os.path.join(HERE, "build_checkprose_feed.py"), "build_checkprose_feed")
    feed, stats = fb.build(a.tree)
    if feed is None:
        in_ci = bool(os.environ.get("CI")) and not a.require_tree
        print("check_living_prose: the tree is not here (%s)." % stats)
        if not in_ci:
            print("check_living_prose: NOT RUN. The prose gate could not say who is living, so it checked nothing; this "
                  "is NOT a pass.")
            return 2
        # IN CI THE GATE USED TO PRINT «NOT RUN» AND EXIT 0 (found by the sweep of 17 October 2026). It now reads who is
        # living from the committed people.json, whose living people are named on the public site by policy. That is the
        # generator's word, not the tree's; tools/living_feed.py seals the set so it cannot change unconfirmed, and guards
        # the people held out of people.json by keyed hash.
        feed = fb.build_from_people()
        stats = {"tree held out": 0, "people.json living not living on the tree": 0}
        print("check_living_prose: RUNNING IN CI FROM COMMITTED people.json (the generator's list of living people; the "
              "held-out are guarded by tools/living_feed.py)")
    if stats["people.json living not living on the tree"] or not feed["living"] or not feed["deadNames"]:
        print("check_living_prose: FAIL, the feed is not trustworthy (%d living, %d dead names, %d record(s) "
              "people.json calls living that the rule on the tree does not)" % (
                  len(feed["living"]), len(feed["deadNames"]), stats["people.json living not living on the tree"]))
        return 1

    out = fb.feed_path(a.feed)
    fb.write(feed, out)
    print("check_living_prose: feed has %d living people (%d names; %d held out) and %d dead names" % (
        len(feed["living"]), sum(len(x["names"]) for x in feed["living"]), stats["tree held out"],
        len(feed["deadNames"])))
    cmd = [sys.executable, CHECKPROSE, "--root", ROOT, "--feed", out, "--allow-keys", ALLOW_KEYS]
    for inc in include + EXTRA_INCLUDE:
        cmd += ["--include", inc]
    if os.path.exists(ALLOW):
        cmd += ["--allow", ALLOW]
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    sys.exit(main())
