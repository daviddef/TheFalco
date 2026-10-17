#!/usr/bin/env python3
"""A living-people feed that CI can read, without the private tree and without leaking what it guards.

    python3 tools/living_feed.py build  [--dist DIR]    # on a machine WITH the tree: writes data/living-feed.json
    python3 tools/living_feed.py check  [--dist DIR]    # anywhere, including CI: the build's gate
    python3 tools/living_feed.py selftest               # the scanner proves it can still fire

WHY THIS EXISTS. check_living_v2 and check_living_prose need the private MyHeritage tree, which is gitignored, so on a CI
runner they print «NOT RUN» and exit 0 (found by the 17 October 2026 sweep): a push from a machine without the tree could ship
a living person's date green. The tree cannot go in the repo, which is public. This is the part of it that can.

WHAT IT COMMITS, AND WHY EACH PART IS SAFE.

  dates       a KEYED HMAC (SHA-256, 128 bits kept) of every full date the tree gives a living or held-out person, in
              one canonical form (YYYY-MM-DD), so «Jan 6 1888», «6 January 1979» and «6 gennaio 1979» are one entry.
              **A plain hash would be worthless here: there are about 40,000 plausible birth dates, and anyone can hash
              them all in a second and read the answer off the committed file.** The key is a 256-bit secret that is
              never committed: private/living-feed.key locally, the LIVING_FEED_KEY secret in CI. Without it the list is
              noise. With it, CI hashes every date it finds in the built site and looks for a match.
  heldNames   the same, for the names of the people this archive HOLDS OUT (undated, with a living parent) and publishes
              nowhere. Living people who have pages are named on the public site by policy, so their names need no
              protection and CI reads them from people.json; these are the only names that must not appear.
  seal        the set of living people the generator publishes, as a digest. It carries no information a visitor cannot
              already read from the noindex pages. It is the proof that the people.json CI is looking at is the one a
              machine with the tree last confirmed: a person flipped from living to dead changes it, and CI fails until
              somebody with the tree re-runs `build` (which refuses if the tree disagrees).
  keycheck    an HMAC of a fixed word, so a WRONG key in CI is detected instead of silently matching nothing.

WHAT IT CANNOT DO, STATED. CI cannot recompute who is living: that needs birth years, which cannot be committed. So a new
tree person the generator wrongly publishes as dead is caught only where the tree is. The seal makes that check un-skippable
for any CHANGE to who is living; it cannot see a person who was never flagged. And if the key leaks, the committed dates
become recoverable: treat it like a password.

Counts and paths are printed, never a name or a date.
"""
import argparse
import hashlib
import hmac
import io
import json
import os
import re
import secrets
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")
DATA = os.path.join(SITE, "src", "data")
FEED = os.path.join(ROOT, "data", "living-feed.json")
KEYFILE = os.path.join(ROOT, "private", "living-feed.key")
TREE = os.path.join(ROOT, "data", "myheritage-falco-tree.json")

MONTHS = {}
for _i, _names in enumerate([
        ("january", "jan"), ("february", "feb"), ("march", "mar"), ("april", "apr"), ("may",), ("june", "jun"),
        ("july", "jul"), ("august", "aug"), ("september", "sep", "sept"), ("october", "oct"), ("november", "nov"),
        ("december", "dec"),
        ("gennaio", "gen"), ("febbraio",), ("marzo",), ("aprile",), ("maggio", "mag"), ("giugno", "giu"),
        ("luglio", "lug"), ("agosto", "ago"), ("settembre", "set"), ("ottobre", "ott"), ("novembre",),
        ("dicembre", "dic")], 1):
    for _n in _names:
        MONTHS[_n] = ((_i - 1) % 12) + 1
WORD = r"[A-Za-zÀ-ÿ]{3,10}"
DMY = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(" + WORD + r")\.?,?\s+(1[89]\d\d|20\d\d)\b")
MDY = re.compile(r"\b(" + WORD + r")\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(1[89]\d\d|20\d\d)\b")
TAGS = re.compile(r"<[^>]+>")
TOKEN = re.compile(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’\-]*")
CONNECT = {"di", "de", "del", "della", "dei", "degli", "d", "da", "la", "le", "van", "von", "du", "dal", "dello"}
TEXT_EXT = (".html", ".json", ".tsv", ".txt", ".xml", ".md", ".csv", ".js", ".astro", ".svg")


def iso_dates(text):
    """Every full date in `text`, canonicalised to YYYY-MM-DD, whatever its spelling or language."""
    out = set()
    s = str(text or "")
    for d, mon, y in DMY.findall(s):
        m = MONTHS.get(mon.lower())
        if m and 1 <= int(d) <= 31:
            out.add("%s-%02d-%02d" % (y, m, int(d)))
    for mon, d, y in MDY.findall(s):
        m = MONTHS.get(mon.lower())
        if m and 1 <= int(d) <= 31:
            out.add("%s-%02d-%02d" % (y, m, int(d)))
    return out


def norm(name):
    s = unicodedata.normalize("NFKD", str(name or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[’']", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def mac(key, tag, value):
    return hmac.new(key, (tag + ":" + value).encode("utf-8"), hashlib.sha256).hexdigest()[:32]


def name_variants(spelling):
    """'Given Family' as written, and the register's habit of putting the family name first."""
    toks = norm(spelling).split()
    out = set()
    if 2 <= len(toks) <= 5:
        out.add(" ".join(toks))
        out.add(" ".join(toks[-1:] + toks[:-1]))        # FAMILY given
        out.add(" ".join(toks[1:] + toks[:1]))          # given... then the first word last (Family-first registers)
    return out


def windows(text):
    """Every 2-5 word run of capitalised words (with lowercase connectors), normalised, as the hash candidates."""
    flat = TAGS.sub(" ", text)
    run, found = [], set()

    def flush():
        n = len(run)
        for i in range(n):
            for j in range(i + 2, min(n, i + 5) + 1):
                found.add(" ".join(run[i:j]))
        run.clear()
    for m in TOKEN.finditer(flat):
        w = m.group(0)
        gap = flat[m.end():m.end() + 1]
        if w[0].isupper():
            run.append(norm(w))
        elif run and w.lower() in CONNECT:
            run.append(norm(w))
        else:
            flush()
        # a run only continues across plain whitespace
        if gap not in (" ", "\n", "\t", "\xa0", "-"):
            flush()
    flush()
    return found


# --------------------------------------------------------------------------------------------- the key
def load_key(required=False):
    k = os.environ.get("LIVING_FEED_KEY", "").strip()
    if not k and os.path.exists(KEYFILE):
        k = open(KEYFILE, encoding="utf-8").read().strip()
    if not k:
        return None
    return k.encode("utf-8")


def make_key():
    os.makedirs(os.path.dirname(KEYFILE), exist_ok=True)
    k = secrets.token_hex(32)
    fd = os.open(KEYFILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(k + "\n")
    return k.encode("utf-8")


# ------------------------------------------------------------------------------------------- the seal
def seal_of(people):
    living = sorted(p["slug"] for p in people if p.get("living"))
    return hashlib.sha256(json.dumps(living, separators=(",", ":")).encode()).hexdigest(), len(living)


def _people():
    d = json.load(io.open(os.path.join(DATA, "people.json"), encoding="utf-8"))
    return d if isinstance(d, list) else d["people"]


# ------------------------------------------------------------------------------------------- scanning
def iter_files(dist, extra_dirs=()):
    for base in (dist,) + tuple(extra_dirs):
        for dp, _dn, fns in os.walk(base):
            for fn in fns:
                if fn.lower().endswith(TEXT_EXT):
                    yield os.path.join(dp, fn)


def scan(files, key, date_macs, name_macs, root):
    """Return (files with a guarded date, files with a guarded name, files read)."""
    date_hits, name_hits, n = [], [], 0
    date_cache, name_cache = {}, {}
    for path in files:
        try:
            raw = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        n += 1
        flat = TAGS.sub(" ", raw)
        hit_d = False
        for d in iso_dates(flat):
            v = date_cache.get(d)
            if v is None:
                v = date_cache[d] = mac(key, "d", d) in date_macs
            if v:
                hit_d = True
                break
        hit_n = False
        if name_macs:
            for w in windows(raw):
                v = name_cache.get(w)
                if v is None:
                    v = name_cache[w] = mac(key, "n", w) in name_macs
                if v:
                    hit_n = True
                    break
        rel = os.path.relpath(path, root)
        if hit_d:
            date_hits.append(rel)
        if hit_n:
            name_hits.append(rel)
    return date_hits, name_hits, n


def selftest(quiet=False):
    """The scanner finds a planted date and a planted name, and not a clean page. A guard watching nothing
    is indistinguishable from one that has stopped working."""
    key = secrets.token_hex(16).encode()
    date_macs = {mac(key, "d", "1888-03-04")}
    name_macs = {mac(key, "n", v) for v in name_variants("Zelda Quimby")}
    with tempfile.TemporaryDirectory() as t:
        for fn, body in (("clean.html", "<p>Born 5 March 1888 to Zelda Cooper</p>"),
                         ("date_us.html", "<p>b. <b>Mar</b> 4, 1888</p>"),
                         ("date_it.html", "<p>nata il 4 marzo 1888</p>"),
                         ("name.html", "<td>QUIMBY</td> <td>Zelda</td>"),
                         ("name2.html", "<p>Mrs Zelda Quimby of Brisbane</p>")):
            open(os.path.join(t, fn), "w").write(body)
        dh, nh, _ = scan([os.path.join(t, f) for f in sorted(os.listdir(t))], key, date_macs, name_macs, t)
    ok = (sorted(dh) == ["date_it.html", "date_us.html"]) and ("name2.html" in nh) and ("clean.html" not in dh + nh)
    # the family-first, two-cell shape «QUIMBY / Zelda» is found as the reversed variant
    ok = ok and ("name.html" in nh)
    if not quiet:
        print("living_feed selftest: %s (planted dates found: %d of 2, planted names found: %d of 2, clean page flagged: %s)" % (
            "ok" if ok else "FAILED", len(dh), len(nh), "clean.html" in dh + nh))
    return ok


# ---------------------------------------------------------------------------------------------- build
def build(dist, allow_collisions=False):
    if not os.path.exists(TREE):
        print("living_feed build: NOT RUN — the private tree (data/myheritage-falco-tree.json) is not on this machine, and "
              "nobody can write the feed without it.")
        return 2
    sys.path.insert(0, HERE)
    import build_checkprose_feed as fb
    import check_living_v2 as cl
    tree = json.load(io.open(TREE, encoding="utf-8"))
    tree = tree if isinstance(tree, list) else (tree.get("people") or tree.get("individuals") or [])
    people = _people()
    line = json.load(io.open(os.path.join(DATA, "line.json"), encoding="utf-8"))
    feed, stats = fb.build(TREE)
    if feed is None:
        print("living_feed build: NOT RUN — " + str(stats))
        return 2
    if stats["people.json living not living on the tree"]:
        print("living_feed build: FAIL — people.json calls somebody living whom the rule on the tree does not (or the "
              "reverse); the generator and the gate disagree and no seal can be written over that.")
        return 1
    info, by_rec = cl.recompute(tree, people, line)
    tby = {t["id"]: t for t in tree}

    # the people.json records the generator publishes as living must be exactly the tree's living (not held-out) people
    tree_living = {str(i) for i, d in info.items() if d["living"] and not d["held"]}
    rec_living = {str(p["treeId"]) for p in people if p.get("living") and p.get("treeId") is not None}
    if tree_living != rec_living:
        print("living_feed build: FAIL — the living people on the tree (%d) and those people.json publishes as living (%d) "
              "are not the same set; check_living_v2 names the record." % (len(tree_living), len(rec_living)))
        return 1

    dates, held_spell = set(), {}
    for tid, d in info.items():
        if not (d["living"] or d["held"]):
            continue
        t = tby.get(tid)
        if not t:
            continue
        for k in ("b", "d"):
            dates |= iso_dates(t.get(k))
        if d["held"]:
            held_spell[tid] = fb.spellings(t.get("name"), t.get("first"), t.get("last"))
            rec = by_rec.get(tid)
            if rec:
                held_spell[tid] |= fb.spellings(rec.get("name"))
    live_lower = {str(p.get("name", "")).split(" (")[0].strip().lower() for p in people if p.get("living")}
    for g in line:
        if str(g.get("name", "")).split(" (")[0].strip().lower() in live_lower:
            for k in ("born", "died", "married", "spouseBorn"):
                dates |= iso_dates(g.get(k))

    dead = set()
    for n in feed["deadNames"]:
        dead |= name_variants(n)
    names, shared, held_people = set(), 0, 0
    for tid, sp in held_spell.items():
        held_people += 1
        for s in sp:
            for v in name_variants(s):
                if v in dead:
                    shared += 1                       # a held-out person who shares a name with a dead one: unguardable
                else:
                    names.add(v)

    # a guarded date already standing on the built site is either a LEAK or a coincidence with a dead person's date;
    # this cannot tell which, so it stops and says so rather than quietly leaving it out of the feed
    if dist and os.path.isdir(dist):
        present = set()
        for p in iter_files(dist):
            try:
                present |= iso_dates(TAGS.sub(" ", open(p, encoding="utf-8", errors="replace").read()))
            except OSError:
                pass
        clash = dates & present
        if clash and not allow_collisions:
            print("living_feed build: FAIL — %d guarded date(s) already appear in the built site. Either a living person's "
                  "date has leaked (run check_release) or it coincides with a dead person's date (re-run with "
                  "--allow-collisions, which leaves those out and counts them)." % len(clash))
            return 1
        dates -= clash
        n_clash = len(clash)
    else:
        n_clash = 0
        print("living_feed build: NOTE no built site to check the dates against; pass --dist.")

    if not dates or not names:
        print("living_feed build: FAIL — %d dates and %d held-out names; refusing to write a feed that could pass on nothing."
              % (len(dates), len(names)))
        return 1

    had_key = load_key() is not None
    key = load_key() or make_key()
    seal, n_living = seal_of(people)
    out = {"v": 1, "alg": "HMAC-SHA256/128, key not in this repository",
           "made": __import__("datetime").date.today().isoformat(),
           "keycheck": mac(key, "k", "living-feed"),
           "seal": {"livingSet": seal, "living": n_living, "heldOut": held_people},
           "counts": {"dates": len(dates), "heldNames": len(names), "heldNamesSharedWithDead": shared,
                      "datesAlsoOnTheSite": n_clash},
           "dates": sorted(mac(key, "d", d) for d in dates),
           "heldNames": sorted(mac(key, "n", v) for v in names)}
    with io.open(FEED, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=0)
        f.write("\n")
    print("living_feed build: wrote data/living-feed.json — %d guarded dates, %d held-out name spellings for %d people "
          "(%d spellings shared with a dead person are NOT guarded), seal over %d living people"
          % (len(dates), len(names), held_people, shared, n_living))
    if not had_key or not os.environ.get("LIVING_FEED_KEY"):
        print("living_feed build: THE KEY is in private/living-feed.key (gitignored, mode 600). CI needs it as the secret "
              "LIVING_FEED_KEY:  gh secret set LIVING_FEED_KEY < private/living-feed.key")
    return 0


# ---------------------------------------------------------------------------------------------- check
def check(dist, require_key=False, tracked=False):
    fails = []
    if not os.path.exists(FEED):
        print("living_feed check: FAIL — data/living-feed.json is missing; run `python3 tools/living_feed.py build` on a "
              "machine with the tree.")
        return 1
    feed = json.load(io.open(FEED, encoding="utf-8"))
    if not selftest(quiet=True):
        print("living_feed check: FAIL — the scanner's own self-test failed, so a clean result would mean nothing.")
        return 1
    if not feed.get("dates") or not feed.get("heldNames"):
        print("living_feed check: FAIL — the feed holds %d dates and %d names; a guard watching nothing is not a guard."
              % (len(feed.get("dates") or []), len(feed.get("heldNames") or [])))
        return 1
    people = _people()
    seal, n = seal_of(people)
    if seal != feed["seal"]["livingSet"]:
        print("living_feed check: FAIL — the set of people published as living has CHANGED since a machine with the tree "
              "last confirmed it (%d living now, %d sealed). Run `python3 tools/living_feed.py build` where the tree is; it "
              "refuses if the tree disagrees." % (n, feed["seal"]["living"]))
        fails.append("seal")
    key = load_key()
    ci = bool(os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"))
    if key is None:
        msg = ("living_feed check: KEY NOT AVAILABLE — the dates and held-out names in the feed cannot be matched without "
               "LIVING_FEED_KEY. The seal was checked; the date and name scan was NOT RUN.")
        if require_key:
            print(msg.replace("NOT RUN.", "NOT RUN, and --require-key makes that a failure."))
            return 1
        if os.environ.get("GITHUB_ACTIONS"):
            print("::warning title=living-feed::LIVING_FEED_KEY is not set, so the living-people date and name scan did not run. "
                  "gh secret set LIVING_FEED_KEY < private/living-feed.key")
        print(msg)
        return 1 if fails else 0
    if mac(key, "k", "living-feed") != feed["keycheck"]:
        print("living_feed check: FAIL — the key does not belong to this feed (keycheck mismatch). A wrong key would match "
              "nothing and report clean, so this is a failure, not a pass.")
        return 1
    dist = os.path.abspath(dist)
    if not os.path.isdir(dist):
        print("living_feed check: FAIL — no built site at %s" % dist)
        return 1
    extra = [os.path.join(DATA)]
    if tracked:
        extra.append(os.path.join(ROOT, "data"))
    files = list(iter_files(dist, extra))
    dh, nh, nread = scan(files, key, set(feed["dates"]), set(feed["heldNames"]), ROOT)
    if nread < 1000:
        print("living_feed check: FAIL — only %d file(s) were read under %s; a built archive has thousands." % (nread, dist))
        return 1
    print("living_feed check: read %d files; guarding %d dates and %d held-out name spellings (%d held-out people); "
          "seal %s over %d living people"
          % (nread, len(feed["dates"]), len(feed["heldNames"]), feed["seal"]["heldOut"],
             "ok" if "seal" not in fails else "BROKEN", n))
    for f in dh[:20]:
        print("  FAIL  a living person's DATE is in %s" % f)
    for f in nh[:20]:
        print("  FAIL  a HELD-OUT person's NAME is in %s" % f)
    if dh or nh or fails:
        print("living_feed check: FAIL — %d file(s) carry a guarded date, %d a held-out name%s."
              % (len(dh), len(nh), ", and the seal is broken" if "seal" in fails else ""))
        return 1
    print("living_feed check: clean — no living person's date and no held-out person's name is on the built site or in its data")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "check", "selftest"])
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--allow-collisions", action="store_true")
    ap.add_argument("--require-key", action="store_true", help="a run without the key is a failure, not a warning")
    ap.add_argument("--tracked", action="store_true", help="also scan the repository's data/ directory")
    a = ap.parse_args(argv)
    dist = a.dist
    if not os.path.isabs(dist) and os.path.isdir(os.path.abspath(dist)) and os.path.abspath(dist) != os.path.join(SITE, "dist"):
        dist = os.path.abspath(dist)
    if not os.path.isabs(dist):
        try:
            sys.path.insert(0, os.path.join(SITE, "node_modules", "@daviddef", "archive-kit", "kit", "tools"))
            from outdir import resolve
            dist = os.path.join(SITE, resolve(dist))
        except Exception:
            dist = os.path.join(SITE, os.environ.get("ARCHIVE_OUT") or dist)
    if a.cmd == "selftest":
        return 0 if selftest() else 1
    if a.cmd == "build":
        return build(dist, a.allow_collisions)
    return check(dist, a.require_key, a.tracked)


if __name__ == "__main__":
    sys.exit(main())
