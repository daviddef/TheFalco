#!/usr/bin/env python3
"""Build the feed the kit's prose gate (kit/tools/checkprose.py) reads: who is living, and who is dead.

    python3 tools/build_checkprose_feed.py                # writes private/checkprose-feed.json
    python3 tools/build_checkprose_feed.py --out PATH     # or $CHECKPROSE_FEED
    python3 tools/build_checkprose_feed.py --counts       # counts only, writes nothing

The feed holds living people's NAMES, so it is never committed: it is written under private/ (gitignored),
or wherever $CHECKPROSE_FEED / --out says, and the file is created readable by its owner only. This script
prints COUNTS only, never a name.

    {"living":    [{"id": "<tree id>", "names": ["Given Family", ...]}, ...],
     "deadNames": ["Given Family", ...]}

WHO IS LIVING is not decided here. It is the kit's one rule (kit/tools/living_rule.py), reached through
tools/living_v2.py, applied to the private MyHeritage tree (data/myheritage-falco-tree.json, the only place a
living person's birth year exists) by tools/check_living_v2.recompute(), which is the independent recomputation
the living gate already makes, so this feed and that gate cannot disagree:

  * every tree person the rule calls living (80 or younger, no death or burial recorded, no public source);
  * every HELD-OUT person (undated, with a living parent). They are not published at all, so any date or
    detail beside such a name in a hand-written page is as wrong as for a living one;
  * every people.json record flagged living whose tree person the recomputation did not call living (there
    should be none; the count is printed, and the run fails if there is one, because the generator and the
    gate disagree and somebody must look).

The register's own text says "living" in the sense of "alive at the time of the act" (Italian: vivente) about
people baptised in the 1800s. Those rows are dead people. Nothing here reads the word "living" in a row;
the only inputs are the tree, the kit's rule and people.json.

Every recorded spelling of a living person goes in: the tree's name, its given names with the surname, the
parenthesised maiden or birth name with the given names, and people.json's own name for the record.

WHO IS DEAD is decided by IDENTITY, never by "every name that is not a living name" (a living person and an
ancestor who share a name would then cancel each other out of the corpus; the kit skips and counts a name both
have, it does not guess). Dead names come from the archive's dead rows:

  * every tree person the recomputation calls dead (all of their spellings);
  * every people.json record not flagged living (register households and tree people), by name.

Without the tree this script writes nothing and exits 2: "cannot say who is living" is not "nobody is".
"""
import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import living_v2 as lv                      # the archive's adapter to the kit's living_rule.py
import check_living_v2 as cl                # the gate's independent recomputation of who is living

ROOT = lv.ROOT
DATA = os.path.join(ROOT, "site", "src", "data")
TREE = os.path.join(ROOT, "data", "myheritage-falco-tree.json")
DEFAULT_FEED = os.path.join(ROOT, "private", "checkprose-feed.json")


def feed_path(explicit=None):
    return explicit or os.environ.get("CHECKPROSE_FEED") or DEFAULT_FEED


def _json(name):
    with io.open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def _clean(n):
    """A name as written, without the tree's tick and star marks or a trailing comma."""
    n = re.sub(r"[✔⭐★⚠]", "", str(n or ""))
    return re.sub(r"\s+", " ", n).strip(" ,;")


def spellings(name, first=None, last=None):
    """Every recorded spelling of one person as plain 'Given Family' strings.

    The tree writes 'Given Family (Maiden)'. The kit reads the words outside a parenthesis, so the maiden
    name is added as its own spelling: 'Given Maiden'."""
    out = set()
    name = _clean(name)
    first, last = _clean(first), _clean(last)
    paren = re.findall(r"\(([^)]*)\)", name)
    bare = re.sub(r"\s*\([^)]*\)", " ", name)
    bare = re.sub(r"\s+", " ", bare).strip()
    if bare:
        out.add(bare)
    if first and last:
        out.add(first + " " + last)
    for p in paren:
        p = _clean(p)
        if not p:
            continue
        p = re.sub(r"^(?:n[ée]e|born)\s+", "", p, flags=re.I)
        if first:
            out.add(first + " " + p)
        elif bare:
            out.add(bare.split()[0] + " " + p)
    return {n for n in out if " " in n}


def build(tree_path=None):
    """Return (feed, stats), or (None, reason) when the tree is not on this machine."""
    path = tree_path or TREE
    if not os.path.exists(path):
        return None, "the private MyHeritage tree (data/myheritage-falco-tree.json) is not on this machine"
    tree = json.load(io.open(path, encoding="utf-8"))
    tree = tree if isinstance(tree, list) else (tree.get("people") or tree.get("individuals") or [])
    if len(tree) < 100:
        return None, "the tree has %d people; refusing to decide who is living from that" % len(tree)
    people = _json("people.json")
    line = _json("line.json")
    info, by_rec = cl.recompute(tree, people, line)

    living, dead = {}, set()
    stats = {"tree people": len(tree), "tree living": 0, "tree held out": 0, "tree dead": 0,
             "tree placeholders": 0, "people.json living not living on the tree": 0}
    tby = {t["id"]: t for t in tree}
    for t in tree:
        i = info.get(t["id"])
        if i is None:
            stats["tree placeholders"] += 1
            continue
        names = spellings(t.get("name"), t.get("first"), t.get("last"))
        rec = by_rec.get(t["id"])
        if rec:
            names |= spellings(rec.get("name"))
        if i["held"]:
            stats["tree held out"] += 1
            living.setdefault(str(t["id"]), set()).update(names)
        elif i["living"]:
            stats["tree living"] += 1
            living.setdefault(str(t["id"]), set()).update(names)
        else:
            stats["tree dead"] += 1
            dead |= names
    # a people.json record the generator calls living that the recomputation does not: the two disagree
    for p in people:
        if p.get("living"):
            tid = p.get("treeId")
            if tid is None or str(tid) not in living:
                stats["people.json living not living on the tree"] += 1
                living.setdefault("record:" + p["slug"], set()).update(spellings(p.get("name")))
    # dead rows of people.json (register households and tree people), by identity
    n_dead_rows = 0
    for p in people:
        if p.get("living"):
            continue
        tid = p.get("treeId")
        if tid is not None and str(tid) in living:
            continue                                    # held out of people.json but alive on the tree: not dead
        n_dead_rows += 1
        dead |= spellings(p.get("name"))
    stats["people.json dead rows"] = n_dead_rows
    feed = {"living": [{"id": k, "names": sorted(v)} for k, v in sorted(living.items()) if v],
            "deadNames": sorted(dead)}
    stats.update({"living people in the feed": len(feed["living"]),
                  "living names": sum(len(x["names"]) for x in feed["living"]),
                  "dead names": len(feed["deadNames"])})
    sys.path.insert(0, os.path.join(ROOT, "site", "node_modules", "@daviddef", "archive-kit", "kit", "tools"))
    try:
        import checkprose as cp
        lp, dp = set(), set()
        for x in feed["living"]:
            lp |= cp.phrases(x["names"])
        for n in feed["deadNames"]:
            dp |= cp.phrases([n])
        stats["living phrases"] = len(lp)
        stats["living phrases shared with a dead person (skipped by the gate)"] = len(lp & dp)
        stats["living people with every phrase shared with a dead person"] = sum(
            1 for x in feed["living"] if cp.phrases(x["names"]) and cp.phrases(x["names"]) <= dp)
    except ImportError:
        pass
    return feed, stats


def write(feed, out):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(feed, f, ensure_ascii=False)
    os.chmod(out, 0o600)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write the living / dead name feed for checkprose.py (counts only are printed).")
    ap.add_argument("--out")
    ap.add_argument("--tree")
    ap.add_argument("--counts", action="store_true", help="print counts, write nothing")
    a = ap.parse_args(argv)
    feed, stats = build(a.tree)
    if feed is None:
        print("build_checkprose_feed: not run: %s" % stats)
        return 2
    for k, v in stats.items():
        print("  %-62s %d" % (k, v))
    if not feed["living"] or not feed["deadNames"]:
        print("build_checkprose_feed: FAIL, %d living, %d dead names; refusing to write a feed that could pass on nothing" % (
            len(feed["living"]), len(feed["deadNames"])))
        return 1
    if stats["people.json living not living on the tree"]:
        print("build_checkprose_feed: FAIL, people.json calls somebody living whom the kit's rule on the tree does not; "
              "the generator and the gate disagree (check_living_v2 names the record)")
        return 1
    if a.counts:
        return 0
    out = feed_path(a.out)
    write(feed, out)
    print("build_checkprose_feed: wrote the feed (names inside, not for commit) outside the tracked files"
          if not os.path.abspath(out).startswith(ROOT + os.sep) else
          "build_checkprose_feed: wrote %s (names inside, gitignored, not for commit)" % os.path.relpath(out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
