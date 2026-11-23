#!/usr/bin/env python3
"""Count the forenames in this archive's own person records, for the "The forenames" page (/your-name/).

    python3 tools/given_names.py            # writes site/src/data/givennames.json (counts only)
    python3 tools/given_names.py --counts   # prints, writes nothing
    python3 tools/given_names.py --check    # the build gate (npm run check:given-names), offline

THE GATE (--check) answers, in the direction that hurts, "what do the records hold that the catalogue does not?": it fails
(exit 2) if a form counted here is missing from site/src/data/given-names.json (the committed snapshot of the Atlas catalogue),
or if the committed counts are not what people.json now gives. The fix is never a table here: `given_name_variants.py add` in
Record Atlas (with the evidence), `publish`, then `npm run given-names` (which re-fetches the catalogue, strict) and commit.

THIS FILE KEEPS NO TABLE OF FORMS. Which forms are one name (Giovanni = Joannes = Zuane...) is the Record Atlas's
(data/given-name-families.json, https://recordatlas.org/given-names.json), fetched by the Archive Kit's
tools/atlas_given_names.py. This tool only says how many times THIS archive has met each form written down:
{"observed": {form: n}} where n is the number of PEOPLE whose recorded name carries the form.

WHAT IS COUNTED, and nothing else:
  * site/src/data/people.json, the people who have a page here (the same file the person pages are built from);
  * NOT a person the archive's own rule marks `living` (the kit's one rule, written by tools/build_people.py): a living
    person's name is never read into a count, so no form is counted because a living person bears it;
  * NOT the register rows (site/src/data/register.json, 13,498 rows behind /who/): they are index entries and machine
    readings, several rows to one man, with surnames guessed, and a count of them would say how often a CLERK wrote a
    name, not how many people bore it. /who/ is untouched.
A form is a word of the name in front of the surname: the parenthesis (a maiden name, "of Antonio, b. 1838") is
dropped, so is the surname field's words wherever they stand, a particle, a bracketed placeholder ("[daughter]"),
an honorific, and a word that holds a digit. Two forenames ("Maria Giuseppa") are two forms, each counted once for
that person; an apostrophe is typography (Carl'Antonio is Carlantonio); a form the Atlas holds as a slip is not counted. Only forms and counts are written; no name of a person and no slug.
"""
import json, pathlib, re, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "src" / "data"
OUT = DATA / "givennames.json"

PARTICLES = {"de", "del", "della", "dei", "di", "da", "d", "la", "le", "lo", "il", "of", "the", "detto", "alias", "fra",
             "padre", "don", "donna", "suor", "sor", "mr", "mrs", "miss", "dr", "sir", "rev", "and", "or", "e", "et",
             "commendatore", "fu", "vedova", "ved"}
# Words that stand in a name BEFORE the surname but are another family's surname (a maiden name written in the middle:
# "Maria Cimmino Falco"), not a forename. A word is one when it is the surname of three or more people here (derived, below);
# these two are the same thing met once, with no second bearer to prove it, read off the shape "Forename X Surname (Married)".
MIDDLE_SURNAMES = {"nobile", "amadio"}
CUT = re.compile(r"\s(?:fu|detto|vedova|ved\.?|alias)\s|\s[—–]\s|\s-\s")
WORD = re.compile(r"^[^\W\d_]+(?:['\-’][^\W\d_]+)*[?]?$")


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if not unicodedata.combining(c))


def forms_of(p, surnames=frozenset()):
    s = re.sub(r"\[.*?\]", " ", str(p.get("name") or ""))      # "[daughter] Falco": a placeholder, not a form
    s = re.sub(r"\(.*?\)", " ", s)                              # the parenthesis: maiden name, parents, dates
    s = CUT.split(" " + s + " ")[0].strip()                      # "Maria Guida fu Fabrizio", "X — Fra Angelo": what stands before the cut
    sur = {fold(w) for w in re.split(r"[\s/]+", str(p.get("surname") or "")) if w}
    words = [w for w in re.split(r"[\s/,]+", s) if w]
    out = []
    for i, w in enumerate(words):
        w = w.strip('"“”.,;:')
        k = fold(w)
        if i > 0 and (k in surnames or k in MIDDLE_SURNAMES):    # a maiden name in the middle, not a forename
            continue
        if i > 0 and fold(words[i - 1]) in {"del", "della", "dei", "di", "de"}:   # "Anna del Giudice Falco": a surname after a particle
            continue
        if not w or k in sur or k.rstrip("'") in PARTICLES or not WORD.match(w) or len(w) < 2:
            continue
        if len(w) >= 3 and w == w.upper() and w != "?":          # written in capitals: a surname, however it got here
            continue
        w = re.sub(r"['’]", "", w)                                # typography is never a spelling: Carl'Antonio is Carlantonio
        out.append(w[:1].upper() + w[1:])
    return list(dict.fromkeys(out))


def tfold(s):
    """Case and typography (apostrophe, hyphen, space) and NOTHING else: an accent is a spelling (Maria is not María), but the
    catalogue treats Michel'angelo and Michelangelo as one form, so a count is kept under the spelling the catalogue stores
    (the kit's fetcher matches without case or accents only)."""
    return re.sub(r"[^\w]|_", "", str(s).lower())


def stored_spellings():
    try:
        cat = json.load(open(DATA / "given-names.json", encoding="utf-8"))
    except Exception:
        return {}
    return {tfold(f["form"]): f["form"] for r in cat.get("rows", []) for fs in (r.get("langs") or {}).values() for f in fs}


def slips():
    """Forms the Atlas holds as SLIPS (a clerk or an indexer wrote it once by mistake): kept there so nobody counts them as variants,
    and so not counted here either. Read from the committed catalogue snapshot; an empty set before the first fetch."""
    try:
        cat = json.load(open(DATA / "given-names.json", encoding="utf-8"))
    except Exception:
        return set()
    return {fold(x["form"]).rstrip("?").strip() for r in cat.get("rows", []) for x in (r.get("slips") or [])}


def build():
    slip = slips()
    stored = stored_spellings()
    rows = json.load(open(DATA / "people.json", encoding="utf-8"))
    bear = {}
    for p in rows:
        if str(p.get("surname") or "?") != "?" and not CUT.search(" " + str(p.get("name")) + " "):
            bear[fold(p["surname"])] = bear.get(fold(p["surname"]), 0) + 1
    surnames = {k for k, c in bear.items() if c >= 3}
    counts, skipped, n = {}, 0, 0
    for p in rows:
        if p.get("living"):
            skipped += 1
            continue
        fs = forms_of(p, surnames)
        if not fs:
            continue
        n += 1
        for f in fs:
            if fold(f) in slip:
                continue
            f = stored.get(tfold(f), f)
            counts[f] = counts.get(f, 0) + 1
    return counts, n, skipped, len(rows)


def check():
    counts, n, skipped, total = build()
    try:
        have = json.load(open(OUT, encoding="utf-8"))
        cat = json.load(open(DATA / "given-names.json", encoding="utf-8"))
    except Exception as e:
        print("given_names --check: cannot read the committed files (%s)" % e)
        return 2
    held = {fold(f["form"]).rstrip("?").strip() for r in cat["rows"] for fs in (r.get("langs") or {}).values() for f in fs}
    missing = sorted(f for f in counts if fold(f).rstrip("?").strip() not in held)
    stale = have.get("observed") != dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))) or have.get("people") != n
    bad = False
    if missing:
        bad = True
        print("given_names --check: %d form(s) in the records are not in the Atlas catalogue snapshot: %s" % (len(missing), ", ".join(missing[:40])))
        print("  add each to Record Atlas (given_name_variants.py add, with its evidence), publish, then `npm run given-names`.")
    if stale:
        bad = True
        print("given_names --check: site/src/data/givennames.json is not what tools/given_names.py gives now; run `npm run given-names`.")
    if not bad:
        print("given_names --check: %d forms in %d people, every one in the catalogue snapshot (%d names)" % (len(counts), n, len(cat["rows"])))
    return 2 if bad else 0


def main(argv):
    if "--check" in argv:
        return check()
    counts, n, skipped, total = build()
    print(f"given_names: {len(counts)} forms in {n} people ({skipped} of {total} held out as living; register rows not counted)")
    if "--counts" in argv:
        return 0
    out = {"note": "Counts only: how many people of this archive's own person records (not living, not the register rows) carry each "
                   "forename. Written by tools/given_names.py; the forms themselves are the Record Atlas's, never kept here.",
           "people": n,
           "observed": dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("given_names: wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
