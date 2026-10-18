#!/usr/bin/env python3
"""The two files the kit's build-time name linker (kit/tools/autolink.py, checklinks.py) reads, made from this archive's own data.

    python3 tools/build_names_index.py                 # writes private/names-index.json and private/living-links.json
    python3 tools/build_names_index.py --counts        # counts only, writes nothing
    python3 tools/build_names_index.py --index P --living P

`npm run autolink` (site/package.json) runs this, then autolink.py over the built site, right after `astro build` and before any
gate that reads the built HTML. `npm run check:links` is the ratchet (checklinks.py, floor in site/.linkfloor.json).

THE INDEX (names-index.json) is made from site/src/data/people.json, the committed file that drives every /people/<slug>/ page, and
from nothing else. The rule is lib/links.js's own (personLink): a name is read with its parentheses taken out and its case and
apostrophes folded, and

    people     the name is borne by exactly ONE record in people.json and that person is not living. The address is that person's
               page, /people/<slug>/. (links.js sends the direct line's generations to /direct-line/#gen-N instead; the kit holds
               one address per name and ignores a fragment, so the person page is used, and the sections where a <P> already links
               the same man to the direct line are counted in the report.)
    ambiguous  the name is borne by two or more records, none of them living. The address is /people/?q=<name>, which is what
               links.js's pl-several link already is: the reader sees all of them and chooses, the archive does not. The roster
               filters in the browser by the text of its rows, so the name is checked against the BUILT roster (<dist>/people/):
               a name that no row of it contains would send the reader to an empty table, and is left out.

Left out, always:
  - a name with a LIVING bearer, even when other bearers are dead (links.js would link it to the roster; the kit's rule is "a
    name whose bearers include a living person is linked to a disambiguation address or not at all", and the living list holds
    that name, so the index may not). The living people are named on the public site by policy, but a dead person's name is
    not allowed to lead to them silently.
  - a name that the living list holds under any spelling (the tree's own spellings of a living or held-out person), so a dead
    ancestor who shares a name with a living tree person is never linked either.
  - a one-word name, a name with a digit, a bracket, a slash, a question mark, a comma or a dash in it (the register's
    «Aniello Maione / Majone», «[daughter] Falco», «Carmela? Fuccio»), and «[unnamed]».
  - aliases: people.json holds none beyond the parenthesised married or maiden surname, and a married surname is exactly the
    kind of string that is another woman's maiden name. They are not indexed (aliases: 0).

THE LIVING LIST (living-links.json) is the set of names (every recorded spelling) and /people/<slug>/ addresses of every living
or held-out person, from the same decision as the pages and the prose gate: tools/build_checkprose_feed.py, which applies the kit's
living_rule.py to the private tree. It lives in private/ (gitignored) because it holds held-out people's names. It is never committed.

CI. The tree is gitignored, so on a runner this falls back, as tools/check_living_prose.py does, to the living records of the
committed people.json (the living people of this archive are named on the public site by policy). The INDEX is identical either
way, because it is made from people.json alone. What CI loses is only the extra net of the tree's own living spellings; the held-out
people (undated, with a living parent) are not in people.json, have no page and are not named anywhere, so no index entry can
reach them, and tools/living_feed.py (check:living-feed) guards their names by keyed hash over the linked pages.

Counts only are printed, never a name.
"""
import argparse
import importlib.util
import json
import os
import re
import sys
import html as _html
import unicodedata
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "site", "src", "data")
OUT_INDEX = os.path.join(ROOT, "private", "names-index.json")
OUT_LIVING = os.path.join(ROOT, "private", "living-links.json")


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def clean(name):
    """links.js norm(), without the lower-casing: parentheses out, quotes straightened, spaces collapsed."""
    s = re.sub(r"\s*\(.*?\)\s*", " ", str(name or ""))
    s = re.sub(r"[’‘]", "'", s)
    s = re.sub(r"[«»\"]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def key(name):
    """The comparison form: NFC, case-folded, accents kept (the kit matches accents as written), apostrophes straight."""
    return unicodedata.normalize("NFC", clean(name)).casefold()


def is_plain_name(name):
    """Two or more words, no digit, no bracket, slash, question mark, comma, ampersand or dash: a name and nothing else."""
    n = clean(name)
    if len(n.split()) < 2:
        return False
    return not re.search(r"[\d\[\]/?,&—–;:]", n)


def roster_text(dist):
    """The built roster (/people/) as the browser's filter reads it: each row's text and data-extra, accents and case folded.
    None when the roster is not built."""
    path = os.path.join(dist, "people", "index.html")
    if not os.path.exists(path):
        return None
    page = open(path, encoding="utf-8").read()
    rows = re.findall(r'<tr class="ft-row".*?</tr>', page, re.S)
    out = []
    for r in rows:
        extra = re.search(r'data-extra="([^"]*)"', r)
        out.append(fold(re.sub(r"<[^>]+>", " ", r) + " " + (extra.group(1) if extra else "")))
    return out or None


def fold(s):
    s = unicodedata.normalize("NFKD", _html.unescape(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).casefold().strip()


def living_feed():
    """(living names, how). The tree-based feed where the tree is here, the committed people.json otherwise."""
    fb = load_module(os.path.join(HERE, "build_checkprose_feed.py"), "build_checkprose_feed")
    feed, stats = fb.build(None)
    if feed is None:
        return fb.build_from_people(), "people.json only (the tree is not on this machine)"
    if stats["people.json living not living on the tree"]:
        raise SystemExit("build_names_index: FAIL, people.json calls somebody living whom the rule on the tree does not (check_living_v2 names the record)")
    return feed, "the tree and the kit's living rule (%d held out)" % stats["tree held out"]


def build(people, feed, roster=None):
    living_names = {key(n) for x in feed["living"] for n in x["names"]}
    by_key = {}
    for p in people:
        k = key(p["name"])
        by_key.setdefault(k, []).append(p)

    idx_people, idx_amb = [], []
    st = {"records": len(people), "living records": sum(1 for p in people if p.get("living")),
          "distinct names": len(by_key), "unique, dead": 0, "shared, all dead": 0, "left out: a living bearer": 0,
          "left out: a living spelling elsewhere": 0, "left out: not a plain name": 0,
          "left out: no row in the built roster": 0}
    for k, ps in sorted(by_key.items()):
        if not is_plain_name(ps[0]["name"]):
            st["left out: not a plain name"] += 1
            continue
        if any(p.get("living") for p in ps):
            st["left out: a living bearer"] += 1
            continue
        if k in living_names:
            st["left out: a living spelling elsewhere"] += 1
            continue
        display = clean(ps[0]["name"])
        if len(ps) == 1:
            st["unique, dead"] += 1
            idx_people.append({"name": display, "url": "/people/%s/" % ps[0]["slug"]})
        else:
            if roster is not None and not any(fold(display) in t for t in roster):
                st["left out: no row in the built roster"] += 1
                continue
            st["shared, all dead"] += 1
            idx_amb.append({"name": display, "url": "/people/?q=" + quote(display, safe="")})
    return {"people": idx_people, "ambiguous": idx_amb}, st


def living_list(people, feed):
    """Names and addresses. Every spelling of a living or held-out person; the page of every living record."""
    names = sorted({n for x in feed["living"] for n in x["names"]})
    urls = sorted("/people/%s/" % p["slug"] for p in people if p.get("living"))
    return names + urls


def write_private(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=0)
    os.chmod(path, 0o600)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--index", default=OUT_INDEX)
    ap.add_argument("--living", default=OUT_LIVING)
    ap.add_argument("--dist", default=os.path.join(ROOT, "site", "dist"),
                    help="the built site, for the roster check (ARCHIVE_OUT beats it, as for every kit tool)")
    ap.add_argument("--counts", action="store_true")
    a = ap.parse_args(argv)
    dist = os.environ.get("ARCHIVE_OUT") or a.dist
    if not os.path.isabs(dist):
        dist = os.path.join(ROOT, "site", dist)
    with open(os.path.join(DATA, "people.json"), encoding="utf-8") as f:
        people = json.load(f)
    feed, how = living_feed()
    roster = roster_text(dist)
    if roster is None:
        print("build_names_index: FAIL, no built roster at %s/people/index.html: run it after `astro build` (ARCHIVE_OUT names the build)" % dist)
        return 2
    index, st = build(people, feed, roster)
    living = living_list(people, feed)
    if not index["people"] or not living:
        print("build_names_index: FAIL, %d people in the index, %d living terms; refusing to write something that could pass on nothing"
              % (len(index["people"]), len(living)))
        return 1
    print("build_names_index: living list from %s" % how)
    for k, v in st.items():
        print("  %-42s %d" % (k, v))
    print("  %-42s %d people, %d ambiguous, 0 aliases" % ("index", len(index["people"]), len(index["ambiguous"])))
    print("  %-42s %d names and addresses" % ("living list", len(living)))
    if a.counts:
        return 0
    write_private(a.index, index)
    write_private(a.living, living)
    print("build_names_index: wrote %s and %s (gitignored; the living list holds names: never commit)"
          % (os.path.relpath(a.index, ROOT), os.path.relpath(a.living, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
