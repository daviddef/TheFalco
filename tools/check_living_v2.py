#!/usr/bin/env python3
"""The living-people standard, version 2 (16 October 2026): the gate.

    python3 tools/check_living_v2.py [--dist dist] [--selftest]

WHAT IT ENFORCES, against the BUILT SITE and the committed data:

  a  who is living is recomputed HERE, from the private family tree and the kit's
     one rule (kit/tools/living_rule.py), by code that shares nothing with
     tools/build_people.py, and compared with what people.json says;
  b  a living person shows a name, relationships and a town and country, and
     nothing else, in the data AND on the page;
  c  a living person's page is noindex, is not in the sitemap, is not in either
     search index, has no structured data, no table, no image and no year of
     their own, and a living person drawn on another page carries no year there;
  d  a held-out person (undated, with a living parent) appears nowhere: no page, no data file,
     no tsv, no built file, no served file;
  e  every person the archive names has a person page: every edge, every chart
     node, every roster and family row that names a tree person links to a page
     that was built;
  f  it refuses an empty build, and says so when it cannot do a part of its job;
  g  no page, data file or attribute states a living person's AGE («aged 14», «eight years old»), a BIRTH YEAR derived
     for them («born 1955», «born the same year»), or a PASSENGER record naming them (tools/living_ages.py; 25 October
     2026): a living person is a name, relationships and a town and country, and no record.

TWO PARTS NEED THE PRIVATE TREE, which is gitignored and so is not on CI: (a) and
(d). Without it they are reported as NOT RUN, loudly, and the rest still runs. On
a machine that has the tree nothing is skipped.

`--selftest` plants a fault of each kind in a copy of the build and proves the gate
refuses it. The planted values are ones no living person can have (the year 1799,
a street address, a name that is nobody's), never a real person's.
"""
import argparse
import collections
import glob
import html as htmllib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT_TOOLS = os.path.join(ROOT, "site", "node_modules", "@daviddef", "archive-kit", "kit", "tools")
sys.path.insert(0, KIT_TOOLS)
import living_rule as lr          # the one definition; nothing of this archive's own
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import living_ages as la          # a living person's AGE, derived BIRTH YEAR and PASSENGER record (25 October 2026)
try:
    from outdir import resolve as _resolve
except Exception:                 # pragma: no cover
    def _resolve(d):
        o = os.environ.get("ARCHIVE_OUT")
        return os.path.join(os.path.dirname(d.rstrip("/")), o) if o else d

DATA = os.path.join(ROOT, "site", "src", "data")
TREE = os.path.join(ROOT, "data", "myheritage-falco-tree.json")
YEAR = re.compile(r"\b(1[5-9]\d\d|20\d\d)\b")
THIS_YEAR = lr.this_year()

# what a living person's record may hold in people.json
LIVING_KEYS = {"slug", "name", "surname", "household", "role", "events", "sources", "living",
               "parents", "spouses", "children", "siblings", "treeId", "place", "rel",
               "gen", "line", "noKin"}
LINE_KEYS = {"gen", "name", "spouse", "confidence", "living"}
EDGE_KEYS = {"slug", "name", "via", "vias", "superseded", "sameAs", "kept"}


def tag(p):
    """How a person is named in a message. THIS GATE'S OUTPUT IS A PUBLIC CI LOG, so
    a living person is never named in it: their tree id (a number) stands in."""
    return f"living person (tree id {p.get('treeId')})" if p.get("living") else p["slug"]


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def strip_marks(n):
    return re.sub(r"[✔⭐★⚠]", "", str(n or "")).strip(" ,;")


def bare_name(n):
    return re.sub(r"\s+", " ", re.sub(r"\s*\(.*?\)\s*", " ", strip_marks(n))).strip()


def is_placeholder(n):
    n = strip_marks(n)
    return (not n) or n.lower().startswith("unknown") or "[" in n


def text_of(raw):
    """The visible words of a built page, entities decoded, whitespace collapsed."""
    s = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    s = htmllib.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s)


def head_of(raw):
    """Everything up to </head>: where a robots tag lives, wherever in the head it sits."""
    i = raw.find("</head>")
    return raw[:i] if i >= 0 else raw[:20000]


def main_of(raw):
    m = re.search(r"(?is)<main\b.*?</main>", raw)
    return m.group(0) if m else raw


# ---------------------------------------------------------------------------
# the independent recomputation of who is living (a) and who is held out (d)
# ---------------------------------------------------------------------------

def tree_year(p):
    m = YEAR.search(str(p.get("b") or ""))
    return int(m.group(1)) if m else None


def tree_dead(p):
    """(record, flag): a death RECORD in the tree row (a date, a Death or Burial fact), and a bare flag
    (`alive` false with no record). Written here, apart from tools/living_v2.py."""
    rec = False
    if str(p.get("d") or "").strip():
        rec = True
    for f in p.get("facts") or []:
        t = str(f.get("t") or "").strip().lower()
        if t.startswith("death") and not t.startswith("death of"):
            rec = True
        if t.startswith(("burial", "funeral", "cremation")):
            rec = True
    return rec, (not p.get("alive")) and not rec


def record_evidence(rec, line):
    """Death and citations that people.json itself carries for a person (the
    register events merged into them), and the line's own word for a generation."""
    dead, flag, cites, by = False, False, [], None
    for e in rec.get("events") or []:
        ev = str(e.get("event") or "").strip().lower()
        for k in ("death", "burial", "buried", "died", "funeral"):
            if ev.startswith(k) and not ev[len(k):].lstrip().startswith("of "):
                dead = True
        a = str(e.get("ark") or "").strip()
        if a:
            low = a.lower()
            if "an_u" in low or "antenati" in low:
                cites.append("antenati.cultura.gov.it " + a)
            elif re.search(r"\bnaa\b", low) or "recordsearch" in low:
                cites.append("recordsearch.naa.gov.au " + a)
            elif re.match(r"^[0-9A-Z]{3,4}(-[0-9A-Z]{3,4})+$", a):
                cites.append("familysearch.org/ark:/61903/3:1:" + a)
            else:
                cites.append(a)
        if (ev.startswith("birth") or ev.startswith("baptism")) and not ev.split(" ", 1)[-1].startswith("of "):
            m = YEAR.search(str(e.get("date") or ""))
            if m and (by is None or int(m.group(1)) < by):
                by = int(m.group(1))
    if rec.get("gen"):
        g = next((x for x in line if x.get("gen") == rec["gen"]), None)
        if g and g.get("died"):
            dead = True
        elif g and g.get("living") is False:
            flag = True                  # the line says only «no longer living»: a flag, not a record
    return dead, flag, cites, by


def youngest_child_years(tree, info):
    """tree id -> the birth year of the person's youngest child with a known year (17 October 2026: the kit's
    recent-child step). Written here from the tree's own labels, apart from tools/living_v2.py, so that the
    generator and this gate cannot share a mistake: a parent says «His son» / «Her daughter», a child says
    «His father» / «Her mother» / «His parent»; either side is enough."""
    kids = collections.defaultdict(set)
    for t in tree:
        for r in t.get("relatives") or []:
            lab = re.sub(r"\s+", " ", str(r.get("rel") or "").strip().lower())
            last = lab.split(" ")[-1] if lab else ""
            if last in ("son", "daughter"):
                kids[t["id"]].add(r["id"])
            elif last in ("father", "mother", "parent"):
                kids[r["id"]].add(t["id"])
    out = {}
    for pid, ks in kids.items():
        ys = [info[k]["by"] for k in ks if k in info and info[k]["by"] is not None]
        if ys:
            out[pid] = max(ys)
    return out


# ---------------------------------------------------------------------------
# the undated tree-only people treated as living by inference (David, 17 October 2026)
# ---------------------------------------------------------------------------
# The kit calls an undated person not living. For a tree-only branch whose recorded ancestors were born in the
# 1920s that is almost certainly wrong (the kit's own recent-child step reaches only people with a child of a
# known year), and the harm is one-sided: a dead person shown by name, relationships and place only, against a
# living person's page indexed. So, until David says who is dead, such a person is treated as living. WHICH people
# is a DECISION recorded by tree id in data/living-by-inference.json (never names), passed to the kit's rule as
# said_living=True. THIS GATE reads that file on its own and recomputes the inference below, so a file that is
# stale, padded, or ignored by the generator is refused.
DECISION = os.path.join(ROOT, "data", "living-by-inference.json")
YEARS_PER_GENERATION = 20
MAX_GENERATIONS_UP = 3
INFERENCE_RULE = (
    "An undated person with no recorded death and no public source is treated as living when their NEAREST DATED "
    "ANCESTOR (their parents first, then grandparents, then great-grandparents, up to 3 generations, both lines) "
    "was born in year Y, g generations up, and Y + 20*g is 1946 or later, that is, 80 or younger in 2026; when "
    "several ancestors tie for nearest, the latest Y counts. An undated spouse of a person so treated is treated "
    "as living too. Only David can rule a person dead: ids he rules dead go in 'overridden'. 'byHand' lists "
    "people David asked to include although the estimate falls just short (an estimate of 1941 or 1945).")


def load_decision(path=None):
    """The committed decision file as {'ids': set, 'byHand': set, 'overridden': set, 'rule': str, ...}.
    Raises ValueError with a plain message when it is missing or malformed."""
    path = path or DECISION
    try:
        d = json.load(open(path, encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError("the decision file %s is missing" % os.path.relpath(path, ROOT))
    except (OSError, json.JSONDecodeError) as e:
        raise ValueError("the decision file cannot be read (%s)" % e)
    out = {"rule": d.get("rule")}
    for k in ("ids", "byHand", "overridden"):
        v = d.get(k)
        if not isinstance(v, list) or not all(isinstance(x, int) and not isinstance(x, bool) for x in v):
            raise ValueError("the decision file's '%s' must be a list of integer tree ids" % k)
        if len(set(v)) != len(v):
            raise ValueError("the decision file's '%s' repeats an id" % k)
        out[k] = set(v)
    # why a person is 'byHand' when the estimate is not what put them there: tree id (as text) -> a reason, never a name
    notes = d.get("handNotes", {})
    if not isinstance(notes, dict) or not all(str(k).isdigit() and isinstance(v, str) and len(v) >= 20
                                              for k, v in notes.items()):
        raise ValueError("the decision file's 'handNotes' must map a tree id to a reason of at least 20 characters")
    out["handNotes"] = {str(k): v for k, v in notes.items()}
    return out


def effective_ids(dec):
    """The tree ids said to be living: on the list and not ruled dead by David."""
    return dec["ids"] - dec["overridden"]


def _decision_ids_or_none(path=None):
    try:
        return effective_ids(load_decision(path))
    except ValueError:
        return set()      # _check reports a bad file as a failure of its own


def infer_living(info, this_year=None):
    """The inference, from the BASELINE `info` of recompute(..., said=set()) (the kit's rule alone).
    returns {tree id: dict(kind='ancestor'|'spouse', g=.., year=.., est=..)} for every undated person the kit calls
    not living (and does not hold out) that the rule in INFERENCE_RULE treats as living."""
    ty = this_year or THIS_YEAR
    floor = ty - lr.LIVING_YEARS                  # born this year or later is 80 or younger
    pool = {t for t, d in info.items()
            if d["by"] is None and not d["dead"] and not d["flag"] and not lr.public_source(d["cites"])
            and not d["living"] and not d["held"]}
    out = {}
    for tid in sorted(pool):
        level, seen = {tid}, {tid}
        for g in range(1, MAX_GENERATIONS_UP + 1):
            nxt = set()
            for x in level:
                nxt |= set(info[x]["parents"]) - seen
            nxt &= set(info)
            seen |= nxt
            ys = [info[q]["by"] for q in nxt if info[q]["by"] is not None]
            if ys:
                y = max(ys)                       # the latest tying ancestor: the youngest estimate, the safer side
                est = y + YEARS_PER_GENERATION * g
                if est >= floor:
                    out[tid] = {"kind": "ancestor", "g": g, "year": y, "est": est}
                break                             # only the NEAREST dated ancestor decides
            level = nxt
            if not level:
                break
    by_ancestor = set(out)                        # a spouse of a spouse is not reached: one step only
    for tid in sorted(pool - by_ancestor):
        mates = [s for s in info[tid]["spouses"] if s in by_ancestor]
        if mates:
            out[tid] = {"kind": "spouse", "g": None, "year": None, "est": None, "spouseOf": mates[0]}
    return out


def recompute(tree, people, line, said=None):
    """expected status for every non-placeholder tree person.
    returns {tree id: dict(kind='living'|'dead'|'held', ...)}
    `said`: the tree ids said to be living by the decision file (default: read data/living-by-inference.json);
    pass set() for the kit's rule alone."""
    if said is None:
        said = _decision_ids_or_none()
    by_rec = {p["treeId"]: p for p in people if p.get("treeId") is not None}
    info = {}
    for t in tree:
        if is_placeholder(t.get("name")):
            continue
        rec = by_rec.get(t["id"])
        dead, flag, cites, ry = record_evidence(rec, line) if rec else (False, False, [], None)
        by = tree_year(t)
        if by is None:
            by = ry
        t_rec, t_flag = tree_dead(t)
        info[t["id"]] = {"by": by, "dead": t_rec or dead, "flag": (t_flag or flag) and not (t_rec or dead), "cites": cites}
    yc = youngest_child_years(tree, info)
    parents = collections.defaultdict(list)
    spouses = collections.defaultdict(set)
    for t in tree:
        for r in t.get("relatives") or []:
            lab = str(r.get("rel") or "").strip().lower()
            if lab.endswith(("father", "mother")):
                parents[t["id"]].append(r["id"])
            elif lab.split(" ")[-1] in ("wife", "husband", "spouse", "partner") and not lab.startswith(("ex", "his ex", "her ex")):
                spouses[t["id"]].add(r["id"])
                spouses[r["id"]].add(t["id"])
    # people.json's own parent edges also count (the registers name parents too)
    slug2tid = {p["slug"]: p.get("treeId") for p in people}
    for p in people:
        if p.get("treeId") is None:
            continue
        for e in p.get("parents") or []:
            tid = slug2tid.get(e["slug"])
            if tid is not None:
                parents[p["treeId"]].append(tid)
    for tid, d in info.items():
        d["yc"] = yc.get(tid)
        d["said"] = tid in said
        d["parents"] = sorted(set(parents.get(tid, [])))
        d["spouses"] = sorted(spouses.get(tid, set()))
        d["living"] = lr.is_living(d["by"], d["dead"], d["cites"], THIS_YEAR, youngest_child_year=d["yc"],
                                   said_living=d["said"], undated_dead=d["flag"])
    for tid, d in info.items():
        pl = any(info.get(q, {}).get("living") for q in parents.get(tid, []))
        d["held"] = lr.is_held_out(tid, d["by"], d["dead"], d["cites"], pl, held_ids=(), today_year=THIS_YEAR,
                                   youngest_child_year=d["yc"], undated_dead=d["flag"])
    return info, by_rec


# ---------------------------------------------------------------------------
# the checks
# ---------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.fails, self.notes, self.table = [], [], {}

    def fail(self, msg):
        self.fails.append(msg)

    def note(self, msg):
        self.notes.append(msg)


def check(dist, tree_path=TREE, tracked=None, quiet=False, data_dir=None, held_scan=True, decision_path=None, ages=True):
    """Run every check against `dist` and return a Report. `tracked` is the
    list of committed files to search for held-out names (default: git's)."""
    global DATA, DECISION
    keep, keep_d = DATA, DECISION
    if data_dir:
        DATA = data_dir
    if decision_path:
        DECISION = decision_path
    try:
        return _check(dist, tree_path, tracked, held_scan, ages)
    finally:
        DATA, DECISION = keep, keep_d


def _check(dist, tree_path, tracked, held_scan=True, ages=True):
    R = Report()
    if not os.path.isdir(dist):
        R.fail(f"no built site at {dist} — build first")
        return R
    people = load("people.json")
    line = load("line.json")
    pages = {}
    for f in glob.glob(os.path.join(dist, "**", "index.html"), recursive=True):
        pages[os.path.relpath(os.path.dirname(f), dist).replace(os.sep, "/")] = f

    # ---- f. refuse an empty build
    person_dirs = {k for k in pages if k.startswith("people/") and k.count("/") == 1}
    if not people:
        R.fail("EMPTY: people.json holds nobody")
    if len(pages) < 200 or len(person_dirs) < max(1, len(people) // 2):
        R.fail(f"EMPTY BUILD: {len(pages)} pages and {len(person_dirs)} person pages for "
               f"{len(people)} people — this is not the site; refusing to say it is clean")
    if not os.path.exists(os.path.join(dist, "sitemap.xml")):
        R.fail("no sitemap.xml in the build — the sitemap step did not run, so its content "
               "cannot be checked")
    sitemap = open(os.path.join(dist, "sitemap.xml"), encoding="utf-8").read() \
        if os.path.exists(os.path.join(dist, "sitemap.xml")) else ""
    sidx_paths = [os.path.join(dist, "searchindex.json"),
                  os.path.join(DATA, "searchindex.json"),
                  os.path.join(os.path.dirname(DATA), "..", "public", "searchindex.json")]
    sidx = ""
    for p in sidx_paths:
        if os.path.exists(p):
            sidx += open(p, encoding="utf-8").read()
    if not sidx:
        R.fail("no search index found in the build or the data — cannot check that living pages are out of it")

    by_slug = {p["slug"]: p for p in people}
    living = [p for p in people if p.get("living")]
    dead = [p for p in people if not p.get("living")]
    live_slugs = {p["slug"] for p in living}
    if not living:
        R.note("NOBODY IS LIVING in people.json. If the private tree is present this is compared "
               "against the recomputation below, which would fail if the tree has living people.")

    # ---- a0. the decision file: who is treated as living by inference (17 October 2026)
    dec = None
    try:
        dec = load_decision()
    except ValueError as e:
        R.fail("DECISION FILE: " + str(e))
    if dec is not None:
        if dec["rule"] != INFERENCE_RULE:
            R.fail("DECISION FILE: its rule text is not the rule this gate enforces (data/living-by-inference.json)")
        if not dec["ids"]:
            R.fail("DECISION FILE: it lists nobody, so the undated people it was made for are published as dead")
        for k in ("byHand", "overridden"):
            for i in sorted(dec[k] - dec["ids"]):
                R.fail("DECISION FILE: tree id %s is in '%s' but not in 'ids'" % (i, k))
        for i in sorted(set(dec["handNotes"]) - {str(x) for x in dec["byHand"]}):
            R.fail("DECISION FILE: 'handNotes' explains tree id %s, who is not 'byHand'" % i)
        # without the private tree this much still holds: whoever the file says is living is living in people.json
        said_recs = {p.get("treeId"): p for p in people if p.get("treeId") is not None}
        for i in sorted(effective_ids(dec)):
            rec = said_recs.get(i)
            if rec is not None and not rec.get("living"):
                R.fail("A PERSON THE DECISION FILE TREATS AS LIVING IS PUBLISHED AS NOT LIVING: tree id %s "
                       "(the generator did not use data/living-by-inference.json)" % i)

    # ---- a. who is living, recomputed independently; d. who is held out
    tree_ran = False
    held_names = []
    if os.path.exists(tree_path):
        tree = json.load(open(tree_path, encoding="utf-8"))
        info, by_rec = recompute(tree, people, line)
        tree_ran = True
        n_live = n_held = 0
        for t in tree:
            i = info.get(t["id"])
            if i is None:
                continue
            rec = by_rec.get(t["id"])
            if i["held"]:
                n_held += 1
                held_names.append(bare_name(t["name"]))
                if rec:
                    R.fail(f"HELD-OUT PERSON HAS A PAGE: tree id {t['id']} is held out "
                           "(or promised privacy) and must have no page and no name anywhere")
                continue
            if not rec:
                R.fail(f"A NAMED PERSON HAS NO PAGE: tree person {t['id']} is neither held out "
                       "nor in people.json")
                continue
            if i["living"]:
                n_live += 1
            if bool(rec.get("living")) != bool(i["living"]):
                R.fail(f"WRONG LIVING STATUS: tree id {t['id']} people.json says living={rec.get('living')}, "
                       f"the kit's rule on the tree says {i['living']}")
        R.table["recomputed"] = (n_live, n_held)
        if dec is not None:
            base, _ = recompute(tree, people, line, said=set())
            inferred = infer_living(base)
            treeids = {t["id"] for t in tree}
            for i in sorted(dec["ids"] - treeids):
                R.fail("DECISION FILE: tree id %s is not a person in the tree (an invented id)" % i)
            for i in sorted((dec["ids"] - dec["byHand"]) & treeids):
                if i not in inferred:
                    R.fail("DECISION FILE: tree id %s is on the list but the rule does not infer them living and "
                           "they are not 'byHand'" % i)
            for i in sorted(dec["byHand"] & treeids):
                d_ = base.get(i)
                if d_ is None or d_["by"] is not None or d_["dead"] or d_["flag"] or lr.public_source(d_["cites"]) \
                        or d_["living"] or d_["held"]:
                    R.fail("DECISION FILE: 'byHand' tree id %s is not an undated person the kit would publish as dead" % i)
            for i in sorted(set(inferred) - dec["ids"] - dec["overridden"]):
                R.fail("DECISION FILE IS MISSING A PERSON THE RULE INFERS LIVING: tree id %s (%s)"
                       % (i, inferred[i]["kind"]))
            R.table["inference"] = (len(inferred), len(dec["ids"]), len(dec["byHand"]), len(dec["overridden"]))
        if not n_live and not n_held:
            R.fail("the recomputation found nobody living and nobody held out — it cannot be "
                   "trusted to be looking at the tree (is the data empty?)")
    else:
        R.note("NOT RUN — who is living, and who is held out, cannot be recomputed: the private "
               "tree (data/myheritage-falco-tree.json) is not on this machine. Checks (b), (c) "
               "and (e) still ran against the committed data and the built pages; the rule "
               "itself is proved by the kit's own self-test and by a run where the tree exists.")

    # ---- b. what a living person's data may hold
    for p in living:
        extra = set(p) - LIVING_KEYS
        if extra:
            R.fail(f"LIVING DATA: {tag(p)} carries {sorted(extra)} — a living person is a name, "
                   "relationships and a town and country")
        if p.get("events"):
            R.fail(f"LIVING DATA: {tag(p)} carries events")
        if p.get("household") or p.get("role"):
            R.fail(f"LIVING DATA: {tag(p)} carries a household or a role")
        if p.get("line") and set(p["line"]) - LINE_KEYS:
            R.fail(f"LIVING DATA: {tag(p)}'s line entry carries {sorted(set(p['line']) - LINE_KEYS)}")
        pl = p.get("place", "")
        if pl:
            bad = (re.search(r"\d", pl) or re.search(
                r"(?i)\b(hospital|clinic|nursing|care|home|hospice|centre|center|street|road|avenue|"
                r"lane|drive|via|viale|piazza|strada|corso)\b", pl)
                or len(pl.split(",")) > 2 or len(pl) > 60)
            if bad:
                R.fail(f"LIVING PLACE is not a town and country: {tag(p)}")
        for b in ("parents", "spouses", "children", "siblings"):
            for e in p.get(b) or []:
                if set(e) - EDGE_KEYS:
                    R.fail(f"LIVING EDGE: {tag(p)}.{b} carries {sorted(set(e) - EDGE_KEYS)}")
        for f in ("b", "d", "bp", "dp", "dateFrom", "mergedOn"):
            if p.get(f):
                R.fail(f"LIVING DATA: {tag(p)} carries {f}")
    # the place must be a town the tree really gives (when the tree is here)
    if tree_ran:
        tbyid = {t["id"]: t for t in tree}
        for p in living:
            t = tbyid.get(p.get("treeId"))
            if t and p.get("place"):
                town = p["place"].split(",")[0].strip().lower()
                if town not in [x.strip().lower() for x in re.split(r"[,]| (?=Qld\b)", str(t.get("bp") or ""))] \
                        and town not in str(t.get("bp") or "").lower():
                    R.fail(f"LIVING PLACE is not from the tree: {tag(p)}")
    # an institution or an address inside a living person's tree place must not
    # reach their page or their record, whatever else the reduction did
    INST = re.compile(r"(?i)\b(hospital|clinic|nursing|care|home|hospice|centre|center|maternity|"
                      r"street|road|avenue|lane|drive|via|viale|piazza|strada|corso)\b|\d")
    frags = {}
    if tree_ran:
        for p in living:
            t = tbyid.get(p.get("treeId"))
            if t:
                fr = [x.strip() for x in str(t.get("bp") or "").split(",") if INST.search(x)]
                if fr:
                    frags[p["slug"]] = fr

    # ---- c. the built pages of living people, and the rest of the site
    stats = {"living": collections.Counter(), "dead": collections.Counter()}
    for grp, rows in (("living", living), ("dead", dead)):
        for p in rows:
            d = "people/" + p["slug"]
            dl = "people/<" + tag(p) + ">" if grp == "living" else d      # what a message may print
            f = pages.get(d)
            if not f:
                R.fail(f"NO PAGE BUILT for {tag(p)} — every person named has a page")
                continue
            raw = open(f, encoding="utf-8", errors="replace").read()
            s = stats[grp]
            s["pages"] += 1
            noindex = bool(re.search(r'<meta name="robots"[^>]*noindex', head_of(raw), re.I))
            s["noindex"] += noindex
            s["in sitemap"] += (("/" + d + "/") in sitemap)
            s["in search index"] += (("/" + d) in sidx and ('"/people/%s"' % p["slug"] in sidx
                                                          or '/people/%s/"' % p["slug"] in sidx
                                                          or '/people/%s"' % p["slug"] in sidx))
            ld = "application/ld+json" in raw
            s["JSON-LD"] += ld
            m = main_of(raw)
            tbl = "<table" in m
            img = "<img" in m or "<picture" in m or "<svg" in m.split("<figure class=\"ptree\"")[0] and False
            s["tables"] += tbl
            s["images"] += ("<img" in raw)
            if grp == "living":
                for fr in frags.get(p["slug"], []):
                    if fr.lower() in htmllib.unescape(raw).lower() or fr.lower() in json.dumps(p).lower():
                        R.fail(f"A LIVING PERSON'S INSTITUTION OR ADDRESS IS PUBLISHED: /{dl}/ or their record")
                if not noindex:
                    R.fail(f"LIVING PAGE IS INDEXED: /{dl}/ lacks noindex")
                if ("/" + d + "/") in sitemap:
                    R.fail(f"LIVING PAGE IS IN THE SITEMAP: /{dl}/")
                if re.search(r'"(?:u|h)"\s*:\s*"/people/%s/?"' % re.escape(p["slug"]), sidx) or \
                        ("/people/%s\"" % p["slug"]) in sidx or ("/people/%s/\"" % p["slug"]) in sidx:
                    R.fail(f"LIVING PAGE IS IN THE SEARCH INDEX: /{dl}/")
                if ld:
                    R.fail(f"LIVING PAGE CARRIES STRUCTURED DATA: /{dl}/")
                if tbl:
                    R.fail(f"LIVING PAGE HAS A TABLE (a table of records): /{dl}/")
                if "<img" in raw or "<picture" in raw:
                    R.fail(f"LIVING PAGE HAS AN IMAGE: /{dl}/")
                # a year: anywhere in the main text EXCEPT in the nodes of other (dead) people
                chart = re.search(r'(?is)<figure class="ptree".*?</figure>', m)
                outside = m.replace(chart.group(0), " ") if chart else m
                years = YEAR.findall(text_of(outside))
                if years:
                    R.fail(f"LIVING PAGE CARRIES A YEAR: /{dl}/ ({len(years)} outside the chart)")
                s["years"] += len(years)
                if chart:
                    me = re.search(r'(?is)<div class="node me".*?</div>', chart.group(0))
                    if me and YEAR.search(text_of(me.group(0))):
                        R.fail(f"LIVING PAGE: the person's own node carries a year: /{dl}/")
                        s["years"] += 1
            else:
                if noindex:
                    R.fail(f"A DEAD PERSON'S PAGE IS NOINDEX: /{d}/ — only a living person's page is")
                if ("/" + d + "/") not in sitemap:
                    R.fail(f"A DEAD PERSON'S PAGE IS NOT IN THE SITEMAP: /{d}/")
            # (e) every node that is a person links to a page
            for chartm in re.finditer(r'(?is)<figure class="ptree".*?</figure>', m):
                for nd in re.finditer(r'(?is)<div class="node([^"]*)"[^>]*>', chartm.group(0)):
                    cls = nd.group(1).split()
                    if "me" in cls:
                        continue
                    R.fail(f"A NAMED PERSON HAS NO PAGE LINK: a chart node on /{dl}/ is not a link")
                for a in re.finditer(r'(?is)<a class="node[^"]*" href="([^"]+)"', chartm.group(0)):
                    h = a.group(1).split("#")[0].strip("/")
                    if h not in pages:
                        R.fail(f"A CHART LINKS TO NO PAGE: /{dl}/ -> a page that was not built")
    R.table["stats"] = stats

    # every edge resolves to a person, who has a page
    for p in people:
        for b in ("parents", "spouses", "children", "siblings"):
            for e in p.get(b) or []:
                if e["slug"] not in by_slug:
                    R.fail(f"AN EDGE TO NOBODY: {tag(p)}.{b} -> a person who does not exist")

    # other pages: a living person drawn anywhere carries no year beside their name
    leak = 0
    live_hrefs = {"/people/%s/" % s: s for s in live_slugs} | {"/people/%s" % s: s for s in live_slugs}
    live_re = re.compile(r'href="/people/(?:%s)/?[#"?]' % "|".join(re.escape(x) for x in sorted(live_slugs))) if live_slugs else None
    anchor = re.compile(r'(?is)<a\b[^>]*\bhref="(/people/[^"#?]+)"[^>]*>(.*?)</a>(.{0,160})')
    for d, f in pages.items():
        if d.startswith("people/") and d.count("/") == 1:
            continue
        raw = open(f, encoding="utf-8", errors="replace").read()
        if live_re is None or not live_re.search(raw):
            continue                      # no living person is linked from this page
        for m_ in anchor.finditer(raw):
            href = m_.group(1)
            if href not in live_hrefs:
                continue
            inner = text_of(m_.group(2))
            # what follows belongs to this person only up to the next link or the end of the block: in a row of sibling
            # nodes the next node's dates follow this one's name (25 October 2026: a living sibling listed before a dated one)
            after = text_of(re.split(r"(?is)<a\b|</(?:p|li|td|tr|div|h\d|article|section)>", m_.group(3))[0])
            near = inner + " " + after[:90]
            if YEAR.search(near) and not re.search(r"(?i)\b(generation|gen\.?)\b", near):
                leak += 1
                R.fail(f"A LIVING PERSON WITH A YEAR BESIDE THEM: /{d}/ -> a living person's page")
    R.table["other pages"] = leak

    # ---- c3. a living person's AGE, a birth year DERIVED for them, and a PASSENGER record naming them, on any page
    #      (tools/living_ages.py; 25 October 2026). The true birth years come from the private tree when it is here.
    if ages:
        tyears = {}
        if tree_ran:
            for p_ in living:
                t_ = tbyid.get(p_.get("treeId"))
                y_ = tree_year(t_) if t_ else None
                if y_:
                    tyears[p_["slug"]] = y_
        try:
            af, ast = la.scan_dist(dist, people, tyears)
        except ValueError as e:
            af, ast = ["LIVING AGES: %s" % e], {}
        for x in af:
            R.fail(x)
        R.table["ages"] = (ast.get("files", 0), ast.get("blocks", 0), len(set(af)), ast.get("allowed", 0), len(tyears))

    # ---- c2. who pages: noindex exactly when every bearer is living
    def key(n):
        return re.sub(r"[^a-z0-9]+", "-", bare_name(n).lower()).strip("-")
    bearers = collections.defaultdict(list)
    for p in people:
        bearers[key(p["name"])].append(p)
    n_who = n_who_noindex = 0
    for d, f in pages.items():
        if not (d.startswith("who/") and d.count("/") == 1):
            continue
        n_who += 1
        raw = open(f, encoding="utf-8", errors="replace").read()
        noindex = bool(re.search(r'<meta name="robots"[^>]*noindex', head_of(raw), re.I))
        n_who_noindex += noindex
        b = bearers.get(d.split("/")[1], [])
        want = bool(b) and all(x.get("living") for x in b)
        wl = "who/<a name with a living bearer>" if any(x.get("living") for x in b) else d
        if noindex != want:
            R.fail(f"NAME PAGE /{wl}/ is {'noindex' if noindex else 'indexed'} but "
                   f"{'every' if want else 'not every'} bearer is living")
        for cm in re.finditer(r'<link rel="canonical" href="([^"]+)"', raw):
            if not cm.group(1).rstrip("/").endswith("/" + d):
                R.fail(f"NAME PAGE /{wl}/ names a canonical elsewhere: {cm.group(1)}")
    R.table["who"] = (n_who, n_who_noindex)

    # ---- e. the family and marriage data: every named tree person has a page
    try:
        mi = load("married-in.json")
        bad = 0
        for g in mi:
            for q in g.get("people", []):
                if q.get("src") == "Nudgee Cemetery":
                    continue                      # a cemetery index entry, not a tree person
                if not q.get("slug") or q["slug"] not in by_slug:
                    bad += 1
                    R.fail(f"A NAMED PERSON HAS NO PAGE: married-in.json {g['surname']} lists someone with no page")
            for mm in g.get("marriages", []):
                for k in ("whoSlug", "toSlug"):
                    if not mm.get(k) or mm[k] not in by_slug:
                        bad += 1
                        R.fail(f"A NAMED PERSON HAS NO PAGE: married-in.json marriage in {g['surname']} ({k})")
            if g.get("withheld"):
                R.fail(f"married-in.json {g['surname']}: {g['withheld']} withheld — under standard v2 "
                       "the living are named, none are withheld")
        R.table["married-in unpaged"] = bad
    except FileNotFoundError:
        R.fail("married-in.json is missing")

    # ---- d. a held-out person appears nowhere
    if tree_ran and held_scan:
        published = set()
        for p in people:
            published.add(bare_name(p["name"]).lower())
        for r in load("register.json"):
            nm = bare_name(r.get("name")).lower()
            if nm:
                published.add(nm)
        phrases = {}
        for nm in held_names:
            toks = nm.split()
            if len(toks) < 2:
                continue
            for ph in {" ".join(toks), toks[0] + " " + toks[-1]}:
                phrases[ph.lower()] = nm
        # a held-out name that is also a published name (a namesake) cannot be told apart
        ph_re = {ph: re.compile(r"(?<![a-z])" + re.escape(ph) + r"(?![a-z])") for ph in phrases}
        longer = {ph: sorted([n for n in published if n != ph and ph_re[ph].search(n)], key=len, reverse=True)
                  for ph in phrases}
        equal = {ph for ph in phrases if ph in published}
        files = []
        for root, _, fns in os.walk(dist):
            for fn in fns:
                if fn.endswith((".html", ".json", ".xml", ".txt", ".js", ".css", ".svg", ".tsv", ".md")):
                    files.append(os.path.join(root, fn))
        tr = tracked
        if tr is None:
            try:
                out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
                tr = [os.path.join(ROOT, x) for x in out.splitlines()
                      if x.endswith((".json", ".tsv", ".md", ".astro", ".py", ".js", ".txt", ".mjs", ".yml", ".css"))
                      and not x.endswith("package-lock.json")]
            except Exception:
                tr = []
        def scan(path, label):
            try:
                raw = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                return
            txt = re.sub(r"\s+", " ", htmllib.unescape(raw)).lower()
            slugs = txt
            for ph, nm in phrases.items():
                if ph not in txt and ph.replace(" ", "-") not in slugs:
                    continue
                t2 = txt
                for ln in longer[ph]:
                    t2 = t2.replace(ln, " ").replace(re.sub(r"[^a-z0-9]+", "-", ln), " ")
                hit = ph_re[ph].search(t2) is not None
                if not hit:
                    k = ph.replace(" ", "-")
                    hit = re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", t2) is not None
                if hit and ph not in equal:
                    R.fail(f"A HELD-OUT PERSON APPEARS: {label}")
                    return
        for pth in files:
            scan(pth, "built file " + os.path.relpath(pth, dist))
        for pth in tr:
            scan(pth, "committed file " + os.path.relpath(pth, ROOT))
        R.table["held names searched"] = (len(phrases), len(files), len(tr), len(equal))
    return R


def render(R, label=""):
    t = R.table
    print("check_living_v2:", label or "the living-people standard, version 2")
    if "recomputed" in t:
        print("  recomputed from the private tree with the kit's rule: "
              f"{t['recomputed'][0]} living, {t['recomputed'][1]} held out")
    if "inference" in t:
        a, b, c, d = t["inference"]
        print(f"  decision file (undated people treated as living by inference): the rule infers {a}; "
              f"{b} listed, {c} by hand, {d} overridden")
    st = t.get("stats")
    if st:
        cols = ["pages", "noindex", "in sitemap", "in search index", "JSON-LD", "tables", "images", "years"]
        print("  rendered person pages        " + "".join(f"{c:>17}" for c in cols))
        for g in ("living", "dead"):
            print(f"    {g:<24}" + "".join(f"{st[g][c]:>17}" for c in cols))
    if "who" in t:
        print(f"  name pages: {t['who'][0]} built, {t['who'][1]} noindex (every bearer living)")
    if "held names searched" in t:
        a, b, c, d = t["held names searched"]
        print(f"  held-out names: {a} phrase(s) searched in {b} built file(s) and {c} committed file(s)"
              f" ({d} are also a published namesake and cannot be told apart)")
    if "other pages" in t:
        print(f"  a year beside a living name on another page: {t['other pages']}")
    if "ages" in t:
        f_, b_, n_, al_, ty_ = t["ages"]
        print(f"  ages, derived birth years and passenger records of the living: {f_} files, {b_} blocks read, {n_} found, "
              f"{al_} allowed by site/living-ages-allow.json; "
              + (f"the tree's own birth years were compared ({ty_})" if ty_ else "no private tree here, so the tree's birth years were not compared"))
    for n in R.notes:
        print("  NOTE", n)
    if R.fails:
        print(f"\nFAILED — {len(R.fails)} problem(s):\n")
        for x in sorted(set(R.fails))[:60]:
            print("   ", x)
        if len(set(R.fails)) > 60:
            print(f"    … and {len(set(R.fails)) - 60} more")
    else:
        print("check_living_v2: clean")


# ---------------------------------------------------------------------------
# the self-test: plant a fault of each kind in a COPY and prove it is refused
# ---------------------------------------------------------------------------

def clone(src, dst):
    if subprocess.run(["cp", "-Rc", src, dst]).returncode != 0:
        subprocess.run(["cp", "-R", src, dst], check=True)


class Sandbox:
    """One COPY of the build and of the data, in which faults are planted one at a
    time and then taken out again (every edit records how to undo itself), so the
    real files are never touched and a copy is made once, not once per fault."""

    def __init__(self, dist, data):
        self.root = tempfile.mkdtemp(prefix="livingv2-")
        self.dist = os.path.join(self.root, "dist")
        self.data = os.path.join(self.root, "data")
        clone(dist, self.dist)
        clone(data, self.data)
        self.decision = os.path.join(self.root, "living-by-inference.json")
        if os.path.exists(DECISION):
            shutil.copy(DECISION, self.decision)
        self.undo = []

    def edit(self, path, fn):
        old = open(path, encoding="utf-8").read()
        self.undo.append(lambda: open(path, "w", encoding="utf-8").write(old))
        open(path, "w", encoding="utf-8").write(fn(old))

    def create(self, path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.undo.append(lambda: shutil.rmtree(os.path.dirname(path), ignore_errors=True))
        open(path, "w", encoding="utf-8").write(text)

    def remove_dir(self, path):
        hold = path + ".held"
        os.rename(path, hold)
        self.undo.append(lambda: os.rename(hold, path))

    def restore(self):
        while self.undo:
            self.undo.pop()()

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


def selftest(dist):
    base = check(dist)
    if base.fails:
        print("selftest: the real build is not clean, so a planted fault would prove nothing")
        render(base)
        return 1
    people = load("people.json")
    living = [p for p in people if p.get("living")]
    dead = [p for p in people if not p.get("living")]
    if not living:
        print("selftest: nobody is living, so there is nothing to plant a fault on")
        return 1
    L, D = living[0], dead[0]
    sb = Sandbox(dist, DATA)
    results = []
    PJ = os.path.join(sb.data, "people.json")

    def pg(slug):
        return os.path.join(sb.dist, "people", slug, "index.html")

    def people_edit(fn):
        def m():
            sb.edit(PJ, lambda s: json.dumps((lambda j: (fn(j), j)[1])(json.loads(s))))
        return m

    def page_edit(slug, fn):
        return lambda: sb.edit(pg(slug), fn)

    def trial(name, mutate, expect, need_tree=False, **kw):
        if need_tree and not os.path.exists(TREE):
            results.append((name, None))
            return
        kw.setdefault("held_scan", bool(need_tree))
        kw.setdefault("decision_path", sb.decision)
        kw.setdefault("ages", False)               # the ages scan has trials of its own (ages_trials, below)
        try:
            mutate()
            R = check(sb.dist, data_dir=sb.data, **kw)
        finally:
            sb.restore()
        results.append((name, any(expect in x for x in R.fails)))

    trial("a living page loses its noindex",
          page_edit(L["slug"], lambda s: re.sub(r'<meta name="robots"[^>]*>', "", s)), "IS INDEXED")
    trial("a year (1799) on a living page",
          page_edit(L["slug"], lambda s: s.replace("</main>", "<p>1799</p></main>", 1)), "CARRIES A YEAR")
    trial("JSON-LD on a living page",
          page_edit(L["slug"], lambda s: s.replace("</head>", '<script type="application/ld+json">{}</script></head>', 1)),
          "STRUCTURED DATA")
    trial("a table on a living page",
          page_edit(L["slug"], lambda s: s.replace("</main>", "<table><tr><td>x</td></tr></table></main>", 1)), "HAS A TABLE")
    trial("an image on a living page",
          page_edit(L["slug"], lambda s: s.replace("</main>", '<img src="x.jpg" alt=""></main>', 1)), "HAS AN IMAGE")
    trial("a living page in the sitemap",
          lambda: sb.edit(os.path.join(sb.dist, "sitemap.xml"),
                          lambda s: s + "<url><loc>https://x/people/%s/</loc></url>" % L["slug"]), "IN THE SITEMAP")
    sidx = os.path.join(sb.dist, "searchindex.json")
    trial("a living person in the search index",
          lambda: sb.edit(sidx, lambda s: json.dumps(json.loads(s) + [
              {"k": "Person", "t": L["name"], "s": "", "h": "/people/%s" % L["slug"], "q": "x"}])),
          "SEARCH INDEX")
    trial("a date (1799) in a living person's data",
          people_edit(lambda j: [x.update(b="1799") for x in j if x["slug"] == L["slug"]]), "carries b")
    trial("an event in a living person's data",
          people_edit(lambda j: [x.update(events=[{"event": "birth", "date": "1799"}]) for x in j if x["slug"] == L["slug"]]),
          "carries events")
    trial("a street address as a living person's place",
          people_edit(lambda j: [x.update(place="12 High Street, Brisbane") for x in j if x["slug"] == L["slug"]]),
          "not a town and country")
    trial("a hospital as a living person's place",
          people_edit(lambda j: [x.update(place="Mater Hospital, Australia") for x in j if x["slug"] == L["slug"]]),
          "not a town and country")
    trial("a dead person's page made noindex",
          page_edit(D["slug"], lambda s: s.replace("</head>", '<meta name="robots" content="noindex, nofollow"></head>', 1)),
          "DEAD PERSON'S PAGE IS NOINDEX")
    def unlink():
        for p in people:
            f = pg(p["slug"])
            s_ = open(f, encoding="utf-8").read()
            m = re.search(r'(?is)<figure class="ptree".*?</figure>', s_)
            if m and re.search(r'<a class="node', m.group(0)):
                new_ = re.sub(r'<a (class="node[^"]*") href="[^"]*"([^>]*)>', r"<div \1\2>", m.group(0), count=1)
                sb.edit(f, lambda t: t.replace(m.group(0), new_, 1))
                return
    trial("a chart node with no link", unlink, "NO PAGE LINK")
    trial("an edge to nobody",
          people_edit(lambda j: [x["parents"].append({"slug": "nobody-at-all", "name": "x", "via": "tree", "vias": ["tree"]})
                                 for x in j if x["slug"] == D["slug"]]), "EDGE TO NOBODY")
    trial("a person's page missing from the build",
          lambda: sb.remove_dir(os.path.join(sb.dist, "people", D["slug"])), "NO PAGE BUILT")
    def mi():
        p = os.path.join(sb.data, "married-in.json")
        def fn(s):
            j = json.loads(s)
            for g in j:
                for q in g.get("people", []):
                    if q.get("slug") and q.get("src") != "Nudgee Cemetery":
                        q["slug"] = "no-such-person"
                        return json.dumps(j)
            return s
        sb.edit(p, fn)
    trial("a married-in person with no page", mi, "married-in.json")
    home = os.path.join(sb.dist, "index.html")
    trial("a year beside a living person's name on another page",
          lambda: sb.edit(home, lambda t: t.replace("</main>", '<p><a href="/people/%s/">%s</a> b. 1799</p></main>' % (L["slug"], L["name"]), 1)),
          "A LIVING PERSON WITH A YEAR BESIDE THEM")
    whos = [d for d in os.listdir(os.path.join(sb.dist, "who"))
            if os.path.isfile(os.path.join(sb.dist, "who", d, "index.html"))]
    trial("a name page that names a canonical elsewhere",
          lambda: sb.edit(os.path.join(sb.dist, "who", whos[0], "index.html"),
                          lambda t: t.replace("</head>", '<link rel="canonical" href="https://elsewhere.example/x/"></head>', 1)),
          "names a canonical elsewhere")
    trial("a living person withheld in married-in (the old rule)",
          lambda: sb.edit(os.path.join(sb.data, "married-in.json"),
                          lambda t: json.dumps((lambda j: (j[0].update(withheld=3), j)[1])(json.loads(t)))),
          "withheld")
    def inst():
        t = json.load(open(TREE, encoding="utf-8"))
        tb = {x["id"]: x for x in t}
        for p_ in living:
            x = tb.get(p_.get("treeId"))
            fr = [y.strip() for y in str((x or {}).get("bp") or "").split(",")
                  if re.search(r"(?i)\b(hospital|clinic|nursing|care|home|street|road)\b|\d", y)]
            if fr:
                sb.edit(pg(p_["slug"]), lambda s_: s_.replace("</main>", "<p>%s</p></main>" % fr[0], 1))
                return
        raise SystemExit("selftest: no living person has an institution in their tree place")
    if os.path.exists(TREE):
        try:
            trial("an institution from a living person's tree place on their page", inst, "INSTITUTION OR ADDRESS", need_tree=True)
        except SystemExit:
            results.append(("an institution from a living person's tree place on their page", None))
    else:
        results.append(("an institution from a living person's tree place on their page", None))
    def who_all_living():
        sb.create(os.path.join(sb.dist, "who", "planted-name-xx", "index.html"),
                  "<html><head><title>x</title></head><body><main>x</main></body></html>")
        def fn(s):
            j = json.loads(s)
            [x.update(name="Planted Name Xx") for x in j if x["slug"] == L["slug"]]
            return json.dumps(j)
        sb.edit(PJ, fn)
    trial("a name page of an all-living name that is indexed", who_all_living, "NAME PAGE")
    def empty():
        for x in os.listdir(sb.dist):
            if os.path.isdir(os.path.join(sb.dist, x)):
                sb.remove_dir(os.path.join(sb.dist, x))
    trial("an empty build", empty, "EMPTY BUILD")
    # the ones that need the private tree: held-out names and the rule itself
    held = _held_for_selftest() if os.path.exists(TREE) else []
    trial("a held-out person's name in a built page",
          lambda: sb.edit(pg(D["slug"]), lambda s: s.replace("</main>", "<p>%s</p></main>" % held[0], 1)),
          "HELD-OUT PERSON APPEARS", need_tree=True)
    if os.path.exists(TREE):
        f = os.path.join(sb.root, "planted.json")
        open(f, "w").write(json.dumps({"x": "a note naming " + held[0]}))
        R = check(sb.dist, data_dir=sb.data, tracked=[f])
        results.append(("a held-out person's name in a committed data file",
                        any("HELD-OUT PERSON APPEARS" in x for x in R.fails)))
    else:
        results.append(("a held-out person's name in a committed data file", None))
    def parent_of_recent_child_dead():
        t = json.load(open(TREE, encoding="utf-8"))
        pj = json.load(open(PJ, encoding="utf-8"))
        info, by_rec = recompute(t, pj, load("line.json"))
        who = [tid for tid, v in info.items() if v["by"] is None and v["yc"] is not None and v["living"] and tid in by_rec]
        if not who:
            raise SystemExit("no undated parent of a recent child")
        slug = by_rec[who[0]]["slug"]
        sb.edit(PJ, lambda s_: json.dumps([dict(x, living=False) if x["slug"] == slug else x for x in json.loads(s_)]))
    if os.path.exists(TREE):
        try:
            trial("an undated parent of a recent child published as dead", parent_of_recent_child_dead,
                  "WRONG LIVING STATUS", need_tree=True)
        except SystemExit:
            results.append(("an undated parent of a recent child published as dead", False))
    else:
        results.append(("an undated parent of a recent child published as dead", None))
    trial("a living person recorded as not living",
          people_edit(lambda j: [x.update(living=False) for x in j if x["slug"] == L["slug"]]),
          "WRONG LIVING STATUS", need_tree=True)
    def held_has_page():
        t = json.load(open(TREE, encoding="utf-8"))
        pj = json.load(open(PJ, encoding="utf-8"))
        have = {p.get("treeId") for p in pj}
        info, _ = recompute(t, pj, load("line.json"))
        tid = next(k for k, v in info.items() if v["held"] and k not in have)
        def fn(s):
            j = json.loads(s)
            j.append({"slug": "planted-held", "name": "Planted Held", "surname": "HELD", "household": None,
                      "role": None, "events": [], "sources": ["tree"], "living": False,
                      "parents": [], "spouses": [], "children": [], "siblings": [], "treeId": tid})
            return json.dumps(j)
        sb.edit(PJ, fn)
    trial("an undated person with a living parent given a page", held_has_page, "HELD-OUT PERSON HAS A PAGE", need_tree=True)
    def child_held_out():
        t = json.load(open(TREE, encoding="utf-8"))
        pj = json.load(open(PJ, encoding="utf-8"))
        info, by_rec = recompute(t, pj, load("line.json"))
        kids = [tid for tid, v in info.items() if v["by"] and THIS_YEAR - v["by"] < 18 and not v["dead"] and tid in by_rec]
        if not kids:
            raise SystemExit("no dated child")
        slug = by_rec[kids[0]]["slug"]
        sb.edit(PJ, lambda s_: json.dumps([x for x in json.loads(s_) if x["slug"] != slug]))
        sb.remove_dir(os.path.join(sb.dist, "people", slug))
    if os.path.exists(TREE):
        try:
            trial("a dated child under 18 wrongly held out (no page)", child_held_out, "A NAMED PERSON HAS NO PAGE", need_tree=True)
        except SystemExit:
            results.append(("a dated child under 18 wrongly held out (no page)", False))
    else:
        results.append(("a dated child under 18 wrongly held out (no page)", None))
    # ---- the people treated as living by inference (17 October 2026)
    try:
        dec0 = load_decision()
    except ValueError:
        dec0 = None
    inferred_pub = [p for p in people if dec0 and p.get("treeId") in effective_ids(dec0) and p.get("living")]
    if inferred_pub:
        I = inferred_pub[0]
        trial("a person on the decision list left indexed (no noindex)",
              page_edit(I["slug"], lambda s_: re.sub(r'<meta name="robots"[^>]*>', "", s_)), "IS INDEXED")
        trial("a year (1899) on the page of a person on the decision list",
              page_edit(I["slug"], lambda s_: s_.replace("</main>", "<p>1899</p></main>", 1)), "CARRIES A YEAR")
        trial("a person on the decision list in the sitemap",
              lambda: sb.edit(os.path.join(sb.dist, "sitemap.xml"),
                              lambda s_: s_ + "<url><loc>https://x/people/%s/</loc></url>" % I["slug"]), "IN THE SITEMAP")
        trial("a person on the decision list in the search index",
              lambda: sb.edit(sidx, lambda s_: json.dumps(json.loads(s_) + [
                  {"k": "Person", "t": I["name"], "s": "", "h": "/people/%s" % I["slug"], "q": "x"}])),
              "SEARCH INDEX")
        trial("a date (1899) in the data of a person on the decision list",
              people_edit(lambda j: [x.update(b="1899") for x in j if x["slug"] == I["slug"]]), "carries b")
        trial("the generator forgets the decision file (a listed person published as not living)",
              people_edit(lambda j: [x.update(living=False) for x in j if x.get("treeId") in effective_ids(dec0)]),
              "THE DECISION FILE TREATS AS LIVING IS PUBLISHED AS NOT LIVING")
        def _edit_dec(fn):
            return lambda: sb.edit(sb.decision, lambda s_: json.dumps((lambda j: (fn(j), j)[1])(json.loads(s_))))
        trial("a decision file that lists nobody",
              _edit_dec(lambda j: j.update(ids=[], byHand=[])), "lists nobody")
        trial("a decision file whose rule text is not the gate's",
              _edit_dec(lambda j: j.update(rule="anybody")), "rule text")
        trial("invented ids in the decision file",
              _edit_dec(lambda j: j["ids"].extend([1999991, 1999992])), "an invented id", need_tree=True)
        trial("a decision file with an id left off that the rule infers",
              _edit_dec(lambda j: j.update(ids=[x for x in j["ids"] if x not in j["byHand"]][1:] + j["byHand"])),
              "MISSING A PERSON THE RULE INFERS", need_tree=True)
        trial("a dated person's id in the decision file",
              _edit_dec(lambda j: j["ids"].append(_dated_tree_id())), "does not infer", need_tree=True)
        trial("an id the rule does not infer, claimed as 'byHand'",
              _edit_dec(lambda j: (j["ids"].append(_dated_tree_id()), j["byHand"].append(_dated_tree_id()))),
              "'byHand' tree id", need_tree=True)
    else:
        results.append(("the people treated as living by inference", None))
    # ---- a living person's AGE, derived BIRTH YEAR and PASSENGER record (tools/living_ages.py; 25 October 2026)
    def ages_trials():
        by_slug = {x["slug"]: x for x in people}
        # a living person with a surname and a parent whose own name is a full name: the shape the real faults had
        cand = [x for x in living if len(bare_name(x["name"]).split()) >= 2
                and any(len(bare_name(by_slug[e["slug"]]["name"]).split()) >= 2 for e in x.get("parents", []) if e["slug"] in by_slug)]
        if not cand:
            results.append(("a living person's age, birth year and passenger record", None))
            return
        X = cand[0]
        full = bare_name(X["name"])
        given = full.split()[0]
        par = bare_name(by_slug[next(e["slug"] for e in X["parents"] if e["slug"] in by_slug
                                       and len(bare_name(by_slug[e["slug"]]["name"]).split()) >= 2)]["name"])
        rel_page = "planted-ages.html"
        planted = os.path.join(sb.dist, rel_page)
        tyears = {}
        if os.path.exists(TREE):
            tt = {t_["id"]: t_ for t_ in json.load(open(TREE, encoding="utf-8"))}
            for p_ in living:
                y_ = tree_year(tt.get(p_.get("treeId"), {})) if tt.get(p_.get("treeId")) else None
                if y_:
                    tyears[p_["slug"]] = y_
        yr = la.CUTOFF + 5

        def page(body, head=""):
            return "<html><head><title>x</title>%s</head><body><main>%s</main></body></html>" % (head, body)

        def ages_trial(name, html_, expect, tree=False, path=rel_page, allow=None):
            full_path = os.path.join(sb.dist, path)
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                open(full_path, "w", encoding="utf-8").write(html_)
                fails, _ = la.scan_dist(sb.dist, people, tyears if tree else {}, allow=[] if allow is None else allow, only={path})
            finally:
                if os.path.exists(full_path):
                    os.remove(full_path)
            hit = any(expect in x for x in fails) if expect else (not fails)
            results.append((name, hit))

        ages_trial("an age (aged 14) beside a living person's full name", page("<p>%s was aged 14 at the time.</p>" % full), "AGE")
        ages_trial("an age written in words (eight years old) beside a living person's first name, parents named",
                   page("<p>%s and their child %s, eight years old, came by sea.</p>" % (par, given)), "AGE")
        ages_trial("an age in a text attribute (data-why)",
                   page('<div data-why="%s and their child %s was eight."></div>' % (par, given)), "AGE")
        fj = os.path.join(sb.dist, "planted-ages.json")
        try:
            open(fj, "w", encoding="utf-8").write(json.dumps([{"t": "Her daughter %s, aged 9" % full}]))
            fl, _ = la.scan_dist(sb.dist, people, {}, allow=[], only={"planted-ages.json"})
        finally:
            os.remove(fj)
        results.append(("an age in a JSON string value", any("AGE" in x for x in fl)))
        ages_trial("an age (14 years old) in JSON-LD", page("", '<script type="application/ld+json">%s</script>'
                                                           % json.dumps({"description": "%s, 14 years old" % full})), "AGE")
        ages_trial("a birth year (born %d) beside a living person's name" % yr, page("<p>%s, born %d, of Brisbane.</p>" % (full, yr)), "BORN-YEAR")
        ages_trial("a birth year (b. %d) written as b." % yr, page("<p>%s (b. %d)</p>" % (full, yr)), "BORN-YEAR")
        ages_trial("a birth year derived (born the same year)", page("<p>%s and %s: %s is born the same year.</p>" % (par, par, given)), "BORN-YEAR")
        ages_trial("a passenger-list row in a ship table",
                   page("<table><thead><tr><th>Name</th><th>Arrived</th><th>Ship</th></tr></thead><tbody>"
                        "<tr><td>%s</td><td>1964</td><td>Sydney</td></tr></tbody></table>" % full), "PASSENGER ROW")
        ages_trial("a passenger record in a sentence (embarked, with a year)",
                   page("<p>%s and %s embarked at Naples in 1964, per the passenger list.</p>" % (par, given)), "PASSENGER RECORD")
        if tyears:
            s_ = next(x for x in living if x["slug"] in tyears)
            ages_trial("a living person's own birth year from the tree, beside their name",
                       page("<p>%s (%d)</p>" % (bare_name(s_["name"]), tyears[s_["slug"]])), "BORN-YEAR", tree=True)
        else:
            results.append(("a living person's own birth year from the tree, beside their name", None))
        # the registry: an allowed hit passes, an entry that matches nothing is a failure
        ages_trial("an age allowed by a reviewed registry entry passes",
                   page("<p>%s was aged 14 at the time.</p>" % full), None,
                   allow=[{"contains": "was aged 14 at the time", "why": "planted, with a reason", "used": 0}])
        ages_trial("a registry entry that matches nothing is stale", page("<p>Nothing here.</p>"), "stale",
                   allow=[{"contains": "no such sentence anywhere", "why": "planted, with a reason", "used": 0}])
        # clean text must stay clean: a dead person's age beside a living relative's name, and a dead namesake's age
        dp = next(((bare_name(by_slug[e["slug"]]["name"]), bare_name(x["name"])) for x in living for e in x.get("parents", [])
                   if e["slug"] in by_slug and not by_slug[e["slug"]].get("living")
                   and len(bare_name(by_slug[e["slug"]]["name"]).split()) >= 2 and len(bare_name(x["name"]).split()) >= 2), None)
        if dp:
            ages_trial("a dead parent's age beside a living child's name is clean",
                       page("<p>%s died aged 94. Their child %s lives at Brisbane.</p>" % dp), None)
        else:
            results.append(("a dead parent's age beside a living child's name is clean", None))
        ages_trial("an age with no living person in the sentence is clean",
                   page("<p>Pasquale Falco, three years old, dies on strada Camellara in 1805.</p>"), None)
    ages_trials()
    sb.close()
    bad = 0
    print("selftest: every planted fault must be refused")
    for name, ok in results:
        if ok is None:
            print(f"  SKIPPED  {name}  (needs the private tree)")
        else:
            print(f"  {'caught ' if ok else 'MISSED '}  {name}")
            bad += (not ok)
    n = sum(1 for _, ok in results if ok is not None)
    print(f"selftest: {sum(1 for _, ok in results if ok)} of {n} planted faults caught"
          + (f", {sum(1 for _, ok in results if ok is None)} skipped" if any(ok is None for _, ok in results) else ""))
    return 1 if bad else 0


def _dated_tree_id():
    """A tree id of a person with a birth year: never someone the inference can name."""
    t = json.load(open(TREE, encoding="utf-8"))
    return next(x["id"] for x in t if tree_year(x) is not None and not is_placeholder(x.get("name")))


def _held_for_selftest():
    t = json.load(open(TREE, encoding="utf-8"))
    people = load("people.json")
    info, _ = recompute(t, people, load("line.json"))
    return [bare_name(x["name"]) for x in t if info.get(x["id"], {}).get("held")
            and len(bare_name(x["name"]).split()) >= 2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    dist = os.path.join(ROOT, "site", _resolve(a.dist)) if not os.path.isabs(a.dist) else a.dist
    if a.selftest:
        sys.exit(selftest(dist))
    R = check(dist)
    render(R)
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
