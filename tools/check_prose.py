#!/usr/bin/env python3
"""Refuse to ship a page whose PROSE contradicts the data it sits on.

Written 22 September 2026, after an audit found five pages making claims the
data had contradicted for up to nine days — while every other gate passed:

  antenati.astro    "the seam that has NOT BEEN TOUCHED" of the processetti,
                    and "258 volumes across these four towns, NONE OF THEM
                    READ".  It is 378 across six, and three bundles are read.
  antenati.astro    "FIVE annual death registers have been read in full — 1832
                    through 1836".  It is FIFTY, 1816 to 1865.
  searched.astro    the remaining births are "before 1816 and after 1818",
                    which stopped being true the day 1819 was read.
  sources.astro     "the Arienzo marriage supplements" listed as unread.
  processetti.astro "320 is 321 less the SINGLE BUNDLE that has been read" — in
                    the very comment block that says these counts are DERIVED
                    so they cannot drift, three lines above a literal `- 1`.

WHAT THIS CAN AND CANNOT DO.  A general "does the prose agree with the data"
checker is not writable, for the reason check_corrections.py gives at length:
this archive leaves a withdrawn reading visible beside the thing that replaced
it, and to a regular expression a visible withdrawal is indistinguishable from
an uncorrected claim.  So this gate does the narrow thing that works, and it is
the same shape as the retired-phrase list that has held since 20 September:

  * A FACT is computed from the data, every run, and can never be typed.
  * A CLAIM is a phrase this archive has actually been caught by.  If the phrase
    is on a page OUTSIDE guillemets, the build stops and the fact is printed
    beside it.

Guillemet spans are stripped before matching, so «…» may quote a dead claim for
ever and still be refused as a live statement.  That is the house style and the
gate has to respect it.

Run:  python3 tools/check_prose.py
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "src", "data")
PAGES = sorted(glob.glob(os.path.join(ROOT, "site", "src", "pages", "**", "*.astro"),
                         recursive=True))
load = lambda n: json.load(open(os.path.join(DATA, n), encoding="utf-8"))

# ---------------------------------------------------------------- the facts
searched = load("searched.json")
fams     = load("families.json")["families"]

def _tagged(tag):
    return [r for r in searched if tag in (r.get("tags") or [])]

def _years(prefix_base, lo, hi):
    """Years whose ark appears anywhere in the coverage page."""
    blob = json.dumps(searched, ensure_ascii=False)
    return {y for y in range(lo, hi + 1) if f"an_ua{y + prefix_base}" in blob}

FACTS = {
    "processetti bundles read":
        (lambda: len(_tagged("Processetti")),
         "counted off the coverage page, where a bundle is recorded when it is read. "
         "A BUNDLE IS A DOSSIER VOLUME WALKED IMAGE BY IMAGE — not any work touching the "
         "processetti. On 8 October 2026 three FamilySearch rows were tagged `Processetti` "
         "because they searched a processetti collection, and this number went from 4 to 7 "
         "without a single extra bundle having been opened. Tag the row for what was DONE to it"),
    "families on the families page":
        (lambda: len(fams), "counted from families.json"),
    "reconstructed households":
        (lambda: len(json.load(open(os.path.join(DATA, "households.json"), encoding="utf-8"))),
         "counted from households.json, which is what /households/ is built from"),
    "Arienzo death registers with a coverage row":
        (lambda: len(_years(12502, 1809, 1865)),
         "counted by ark from the coverage page; the 1844-1858 range row covers fifteen more. "
         "ANTENATI ONLY, and deliberately: this counts an_ua arks for 1809-1865, so FamilySearch's "
         "Arienzo death registers of 1866-1910 — found 8 October 2026, waypoints MC55-FNT and "
         "MC55-VNL — are not in it and must never be added to it. A number that silently spanned "
         "two shelves would be the kind of claim this gate exists to refuse"),
}

# ------------------------------------------------------------- the claims
# (regex, which fact it contradicts, what the archive was caught by)
CLAIMS = [
    (r"seam that has not been touched", "processetti bundles read",
     "said of the processetti while three bundles had been read"),
    (r"none of them read", "processetti bundles read",
     "said of the marriage supplements while three bundles had been read"),
    (r"single bundle that has been read", "processetti bundles read",
     "and three lines below it a literal `- 1`, in the block that says these counts are derived"),
    (r"exactly one bundle has\s*\n?\s*been read", "processetti bundles read",
     "on the coverage page's own summary"),
    (r"\bfive annual death registers\b", "Arienzo death registers with a coverage row",
     "1832 through 1836, written when that was all there was and left standing"),
    (r"fifty-three reconstructed households", "reconstructed households",
     "typed into tree.astro beside a sentence that derived ITS number, and left to drift to 111"),
    (r"\bEleven families\b", "families on the families page",
     "typed in an eyebrow beside a count that came from data"),
    (r"birth registers before 1816 and after 1818", "Arienzo death registers with a coverage row",
     "the remaining births, described in terms that stopped being true when 1819 was read"),
]

GUILLEMET = re.compile(r"«.*?»", re.S)
# A /* … */ block in an .astro frontmatter is a note to whoever edits the file,
# not something a reader ever sees — and this archive's notes routinely quote the
# claim they are explaining away («the eleven families were a JavaScript array in
# this file»). Stripping them is the same exemption the guillemets get, for the
# same reason: a gate that refuses an explanation of a fixed bug gets switched off.
COMMENT = re.compile(r"/\*.*?\*/", re.S)
fails = []
for path in PAGES:
    raw = open(path, encoding="utf-8").read()
    body = GUILLEMET.sub("", COMMENT.sub("", raw))
    rel = os.path.relpath(path, ROOT)
    for pat, factname, why in CLAIMS:
        if re.search(pat, body, re.I):
            fn, how = FACTS[factname]
            fails.append(f"{rel}: «{pat}» is stated as fact — but {factname} is "
                         f"{fn()} ({how}).\n      This archive was caught by it: {why}")

# WHAT THIS GATE GUARDS, AS OPPOSED TO WHAT IS ON THE PAGES — work-list row 98.
#
# A page is refused for one of two reasons: it repeats a phrase on the retired
# list, or it contradicts one of the facts computed above. Every other number in
# the prose is typed, and nothing here derives it or will notice when the data
# moves underneath it. That is exactly the failure this gate was written for —
# five pages carrying claims the data had contradicted for up to nine days — so
# the size of the unguarded remainder belongs in the output beside the verdict.
#
# The count is deliberately crude: multi-digit runs in page text with tags
# stripped. It is an order of magnitude, not an inventory, and it is labelled so.
_num = re.compile(r"(?<![\w/#.-])\d{2,}(?![\w%.-])")
_pages_with, _numbers = 0, 0
for _f in PAGES:
    _b = open(_f, encoding="utf-8").read()
    _body = re.sub(r"^---[\s\S]*?---", "", _b, count=1)
    _body = re.sub(r"<[^>]+>", " ", _body)
    _hits = _num.findall(_body)
    if _hits:
        _pages_with += 1
        _numbers += len(_hits)

print(f"check_prose: GUARDS {len(FACTS)} derived fact(s) and {len(CLAIMS)} retired "
      f"claim(s); roughly {_numbers} typed number(s) stand in the prose of "
      f"{_pages_with} of {len(PAGES)} pages with nothing deriving them")
print(f"check_prose: {len(PAGES)} pages, {len(FACTS)} fact(s) computed, "
      f"{len(CLAIMS)} retired claim(s) held")
for name, (fn, how) in FACTS.items():
    print(f"    {name}: {fn()}")
if fails:
    print(f"\nFAILED — {len(fails)} page claim(s) the data contradicts:\n")
    for f in fails:
        print("    " + f)
    print("\nFix the PAGE, or — better — derive the number so it cannot drift again.")
    sys.exit(1)
print("check_prose: clean — no page states a coverage claim the data contradicts")
