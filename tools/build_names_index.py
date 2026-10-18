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

THE SECOND SOURCE (added 18 October 2026, the linking standard's L2): THE NAMES READ FROM RECORDS. site/src/data/register.json holds
12,580 rows, one per person-in-a-record, and /who/<slug>/ is built from it: one page per NAME (a name is not a person; it never merges).
A person the archive has only READ (a declarant, a parent, a witness) has no /people/ page, so before this the linker could not link
the name in a narrative. Now the name page is the entry, as an `ambiguous` row with the address /who/<slug>/ (the page says in its
own words that it is a name, so it is the honest address even when one man bears the name). A /who/ name goes in when ALL of these hold:

    - it is not already an entry from people.json (that source decides those names, including the ones it leaves out);
    - its address is a built /who/ page (checked against the build, as the roster is);
    - it is a plain name that ends or begins with the register's own surname field for it, every word capitalised (a lower-case
      particle such as «di» or «d'» aside): not a given name pair, not an occupation, not «fu Andrea», not a machine reading;
    - THE LIVING RULE SHOWS EVERY ROW DEAD, by date. The kit's rule (living_rule.py) is applied to the latest year the rows give
      (the row's own date or any year written in its detail): a record dated Y names nobody born after Y, so if the rule says the
      person born in Y is not living (81 or more years old), nobody who bears the name in these rows is living. A burial row is a
      recorded death. A name with a row after that year, or with no year at all, is HELD OUT: not linked, and listed (by its
      /who/ address, a page that is public already) in the editorial table. The kit's second test (a record from a public source
      means not living) would admit more of them; the archive holds them out rather than guess;
    - no living or held-out person bears it, in any spelling the living list holds (accents, case, apostrophes and hyphens folded);
    - the site's own text never uses it as the tail of a saint's name or a place («Santa Maria Maggiore», «San Gaetano Morgillo»,
      «strada Giuseppe ...»): the built pages are read for a saint's or place word followed by capitalised words, and a name that
      equals any of those tails is left out (a linker that matches strings cannot tell «Maria Maggiore» the woman from the church).

It adds no page: every /who/ page is already built, listed in the sitemap and indexed unless every bearer is living. Aliases: 0. The
data states no variant of a register name (namefold.json is a search fold of two spellings; people-aliases.json is slug redirects), so
no alias is invented; the register-order form is a name page of its own where the register wrote it so.

THE GIVEN NAMES (given-names.json, also under private/): every word but the last of every name in people.json and the register, the
vocabulary the linking standard's gate (checkstandard.py, standard.json) reads to tell a bare given name from a surname. Made from
committed data only, so it is the same on a runner.

THE LIVING LIST (living-links.json) is the set of names (every recorded spelling) and /people/<slug>/ addresses of every living
or held-out person, from the same decision as the pages and the prose gate: tools/build_checkprose_feed.py, which applies the kit's
living_rule.py to the private tree. It lives in private/ (gitignored) because it holds held-out people's names. It is never committed.

CI. The tree is gitignored, so on a runner this falls back, as tools/check_living_prose.py does, to the living records of the
committed people.json (the living people of this archive are named on the public site by policy). THE INDEX MUST BE THE SAME
EVERYWHERE, and the run proves it: where the tree is, the second source is built twice (once with the tree's living list, once with
the list a runner would have) and the run FAILS if they differ, so a /who/ name that only the tree knows a living or held-out
person bears can never be indexed on a runner and not here (today the difference is 0). The first source is made from people.json
alone. What CI loses is only the extra net of the tree's own living spellings, and the held-out people (undated, with a living
parent) are not in people.json, have no page and are not named anywhere; tools/living_feed.py (check:living-feed) guards their
names by keyed hash over the built pages. The given-names file and the saint-and-place tails are made from committed data and the
build alone. Nothing a runner needs is private: the standard's gate (site/standard.json, .standardfloor.json) reads the index,
the given names and the living list this script writes in the same run.

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
OUT_GIVEN = os.path.join(ROOT, "private", "given-names.json")
OUT_HELD = os.path.join(ROOT, "private", "who-held-out.json")


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


def loose(s):
    """The comparison form for 'is it the same name': accents, case, apostrophes and hyphens folded, every other run of
    punctuation and space one space. Stricter than key(), used wherever a name is checked against the living list."""
    s = unicodedata.normalize("NFKD", _html.unescape(str(s or "")))
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold().replace("'", "").replace("’", "").replace("‘", "")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def _living_rule():
    """The kit's one rule, through the archive's adapter (tools/living_v2.py)."""
    sys.path.insert(0, HERE)
    import living_v2 as lv
    return lv.lr


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


# ---------------------------------------------------------------------------------------- the second source: names read from records

WHO_YEAR = re.compile(r"\b(1[0-9]\d\d|20\d\d)\b")
PARTICLES = {"de", "di", "del", "della", "dei", "degli", "delle", "dal", "dello", "da", "la", "lo", "le", "van", "von"}


def who_bare(n):
    """pages/who/[slug].astro bare(): parentheses out, quotes straightened, spaces collapsed."""
    s = re.sub(r"\s*\(.*?\)\s*", " ", str(n or "")).replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip()


def who_is_name(t):
    """pages/who/[slug].astro isName()."""
    t = t.strip()
    return 2 <= len(t) <= 64 and len(t.split()) <= 7 and not re.search(r"[.;:\u2014]\s|\u00ab|\u00bb|\bthe\b|\bnot an\b", t, re.I)


def who_slug(s):
    """pages/who/[slug].astro slugify()."""
    s = unicodedata.normalize("NFD", s.lower())
    s = re.sub(r"[\u0300-\u036f]", "", s)
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s))


def words_ok(name):
    """Every word capitalised, a lower-case particle («di», «d'») aside: a name, not a phrase («Francesco is», «Filippo Carfora
    contadino», «Angelo Cossi fu Andrea», «il Signor Don Saverio»)."""
    for w in name.split():
        if w.lower() in PARTICLES:
            continue
        base = re.sub(r"^(?:d|l|dell|dall|all)'", "", w, flags=re.I)
        if not base[:1].isupper():
            return False
    return True


def mixed_case(name):
    """A register row may print the name in capitals («SAVERIO MAJONE»); the index wants the form prose uses."""
    if name != name.upper():
        return name
    out = []
    for w in name.split():
        if w.lower() in PARTICLES:
            out.append(w.lower())
        elif re.match(r"(?i)^(d|l|dell|dall|all)'", w):
            head, tail = w.split("'", 1)
            out.append(head.lower() + "'" + tail[:1].upper() + tail[1:].lower())
        else:
            out.append(w[:1].upper() + w[1:].lower())
    return " ".join(out)


def row_years(r):
    """Every year a row gives: its sort date and any year written in its detail. A deliberate over-reading: a year in the
    detail that belongs to somebody else (a son's birth, a certificate's issue) only holds a name out, never lets one in."""
    return [int(y) for y in WHO_YEAR.findall(str(r.get("sort") or "") + " " + str(r.get("detail") or ""))]


PLACE_WORD = r"(?i:santa|santo|san|sant['’]|s\.|ss\.|via|strada|monte|piazza|contrada|chiesa|ospedale|porta|ave)"
PLACE_TAIL = re.compile(PLACE_WORD + r"\s+((?:[A-ZÀ-Ý][\w'’]*|d['’]|di|de|della|del|dei)(?:\s+(?:[A-ZÀ-Ý][\w'’]*|d['’]|di|de|della|del|dei)){0,3})")


def place_tails(dist):
    """loose forms of every run of capitalised words that follows a saint's or place word anywhere in the built pages, with its
    leading prefixes: «Santa Maria Maggiore» gives «maria» and «maria maggiore»."""
    tails = set()
    for root, _d, files in os.walk(dist):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            try:
                t = open(os.path.join(root, fn), encoding="utf-8").read()
            except OSError:
                continue
            t = re.sub(r"(?is)<style\b.*?</style>", " ", t)     # the era note draws its own <style> in the flow (kit era4): CSS is not text
            main = re.search(r"<main\b.*?</main>", t, re.S)
            t = _html.unescape(re.sub(r"<[^>]+>", " ", main.group(0) if main else t))
            for m in PLACE_TAIL.finditer(t):
                ws = m.group(1).split()
                for k in range(1, len(ws) + 1):
                    tails.add(loose(" ".join(ws[:k])))
    return tails


def who_names(register, existing, living_loose, who_dir, lr, this_year=None, tails=frozenset()):
    """The second source. Returns (entries, held, stats). `existing` = loose forms of every name people.json already decides
    (an entry, or left out on purpose); `living_loose` = loose forms of every living or held-out spelling; `who_dir` = the
    built /who/ directory (a set of slugs) or None."""
    by = {}
    for r in register:
        n = who_bare(r.get("name"))
        if not who_is_name(n):
            continue
        sl = who_slug(n)
        if sl:
            by.setdefault(sl, {"names": [], "rows": []})
            by[sl]["names"].append(n)
            by[sl]["rows"].append(r)
    st = {"/who/ names": len(by), "left out: one word": 0, "left out: already decided by people.json": 0,
          "left out: not a plain name": 0, "left out: not capitalised as a name": 0, "left out: no surname in the register for it": 0,
          "left out: not a built /who/ page": 0, "left out: a living or held-out bearer": 0, "left out: the tail of a saint's or place name in the site text": 0, "HELD OUT: no year": 0,
          "HELD OUT: a row the rule cannot show dead": 0, "added (dead by date)": 0}
    entries, held, seen_loose = [], [], {}
    cutoff = None
    for sl, v in sorted(by.items()):
        names = v["names"]
        display = next((n for n in names if n != n.upper()), None) or mixed_case(names[0])
        if len(display.split()) < 2:
            st["left out: one word"] += 1
            continue
        lk = loose(display)
        if lk in existing:
            st["left out: already decided by people.json"] += 1
            continue
        if not is_plain_name(display):
            st["left out: not a plain name"] += 1
            continue
        if not words_ok(display):
            st["left out: not capitalised as a name"] += 1
            continue
        fl = loose(display)
        sur_ok = True
        for r in v["rows"]:
            sur = loose(r.get("surname"))
            if not sur or sur == "?" or not (fl.endswith(sur) or fl.startswith(sur)) or len(sur) < 2:
                sur_ok = False
                break
        if not sur_ok:
            st["left out: no surname in the register for it"] += 1
            continue
        if who_dir is not None and sl not in who_dir:
            st["left out: not a built /who/ page"] += 1
            continue
        if lk in living_loose:
            st["left out: a living or held-out bearer"] += 1
            continue
        if lk in tails:
            st["left out: the tail of a saint's or place name in the site text"] += 1
            continue
        # the living rule, by date: the latest year the rows give; a burial is a recorded death
        latest, nodate = 0, False
        dead_rows = True
        for r in v["rows"]:
            if r.get("kind") == "burial":
                continue
            ys = row_years(r)
            if not ys:
                nodate = True
                dead_rows = False
                continue
            y = max(ys)
            latest = max(latest, y)
            if lr.is_living(y, False, (), this_year):
                dead_rows = False
        if nodate:
            held.append({"slug": sl, "why": "no year in a row", "latest": latest or None,
                         "kinds": sorted({r["kind"] for r in v["rows"]}), "rows": len(v["rows"])})
            st["HELD OUT: no year"] += 1
            continue
        if not dead_rows:
            held.append({"slug": sl, "why": "a row dated after the year the rule shows dead", "latest": latest,
                         "kinds": sorted({r["kind"] for r in v["rows"]}), "rows": len(v["rows"])})
            st["HELD OUT: a row the rule cannot show dead"] += 1
            continue
        if lk in seen_loose:                       # two pages whose names fold alike: neither is guessed
            seen_loose[lk]["clash"] = True
            continue
        e = {"name": display, "url": "/who/%s/" % sl}
        seen_loose[lk] = e
        entries.append(e)
    entries = [e for e in entries if not e.get("clash")]
    st["added (dead by date)"] = len(entries)
    return entries, held, st


def given_names(people, register):
    """The given-name vocabulary for the linking standard's gate: every word but the last of every plain name in people.json and
    the register, leaving out (a) the word that is the row's own surname field (a surname-first form, «Falco Antonio»), and
    (b) any word the register records as a SURNAME in at least 5 rows and more than twice as often as it appears in a given-name
    place (Falco, Crisci, Mauro...): the gate would otherwise count every bare «Falco» as a bare given name. A word that is
    both («Lucia», «Rosa», «Bernardo») stays."""
    sur, giv = {}, {}
    for r in register:
        for w in loose(r.get("surname")).split():
            if w != "?":
                sur[w] = sur.get(w, 0) + 1
    names = [(p["name"], "") for p in people] + [(r.get("name"), r.get("surname")) for r in register]
    spell = {}
    for name, surname in names:
        n = who_bare(name)
        if not is_plain_name(n):
            continue
        own = set(loose(surname).split())
        for w in n.split()[:-1]:
            w = w.strip(".,;:()[]")
            lw = loose(w)
            if len(w) < 2 or not w[:1].isalpha() or w.lower() in PARTICLES or lw in own:
                continue
            giv[lw] = giv.get(lw, 0) + 1
            spell.setdefault(lw, w)
    out = [spell[w] for w in giv if not (sur.get(w, 0) >= 5 and sur[w] > 2 * giv[w])]
    return sorted(out, key=lambda w: (w.casefold(), w))


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
    ap.add_argument("--given", default=OUT_GIVEN, help="the given-names vocabulary for the linking standard's gate")
    ap.add_argument("--held", default=OUT_HELD, help="the /who/ names held out by the living rule, for the editorial table (private)")
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
    # THE SECOND SOURCE: names read from records, /who/<slug>/ name pages
    with open(os.path.join(DATA, "register.json"), encoding="utf-8") as f:
        register = json.load(f)
    lr = _living_rule()
    who_dir = set(os.listdir(os.path.join(dist, "who"))) if os.path.isdir(os.path.join(dist, "who")) else None
    existing = {loose(clean(p["name"])) for p in people}
    living_loose = {loose(n) for x in feed["living"] for n in x["names"]}
    tails = place_tails(dist)
    entries, held, wst = who_names(register, existing, living_loose, who_dir, lr, tails=tails)
    # what a runner would build: the same, with the living list taken from people.json alone (the tree is not there)
    fb = load_module(os.path.join(HERE, "build_checkprose_feed.py"), "build_checkprose_feed")
    ci_feed = fb.build_from_people()
    ci_entries, _h, _s = who_names(register, existing, {loose(n) for x in ci_feed["living"] for n in x["names"]}, who_dir, lr, tails=tails)
    ci_diff = {e["url"] for e in entries} ^ {e["url"] for e in ci_entries}
    index["ambiguous"] = index["ambiguous"] + entries
    living = living_list(people, feed)
    if not index["people"] or not living:
        print("build_names_index: FAIL, %d people in the index, %d living terms; refusing to write something that could pass on nothing"
              % (len(index["people"]), len(living)))
        return 1
    print("build_names_index: living list from %s" % how)
    for k, v in st.items():
        print("  %-42s %d" % (k, v))
    print("  second source: names read from records (/who/ name pages), by the living rule on their dates")
    for k, v in wst.items():
        print("    %-50s %d" % (k, v))
    print("    %-50s %d" % ("of the added, a runner without the tree builds a different set", len(ci_diff)))
    print("  %-42s %d people, %d ambiguous (%d of them /who/ names), 0 aliases"
          % ("index", len(index["people"]), len(index["ambiguous"]), len(entries)))
    print("  %-42s %d names and addresses" % ("living list", len(living)))
    if ci_diff:
        print("build_names_index: FAIL, %d /who/ name(s) would be indexed (or not) differently on a runner that lacks the private tree: "
              "the tree knows a living or held-out bearer that people.json does not. Hold the name out (it is in private/living-links.json) "
              "and make the committed data say so; the index must be the same everywhere." % len(ci_diff))
        return 1
    if a.counts:
        return 0
    write_private(a.index, index)
    write_private(a.living, living)
    write_private(a.given, given_names(people, register))
    write_private(a.held, held)
    print("build_names_index: wrote %s, %s, %s and %s (gitignored; the living list and the held-out list hold names: never commit)"
          % tuple(os.path.relpath(x, ROOT) for x in (a.index, a.living, a.given, a.held)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
