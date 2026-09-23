#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_households — the gate that was missing on 23 September 2026.

On that night four household names were duplicated in one session. A publishing
script appended a fresh entry instead of finding the existing one, and twice the
new entry carried a claim that the household was new when this archive had held
it for weeks. The full verification chain ran green after every one of those
commits, because nothing in it looked at whether two households shared a name.

It also catches the other half of the same mistake: a member written into an
existing household under a person string that differs from the one already
there only by punctuation or case. That splits one person into two, and on the
same night it silently broke the merge that joins Chiara Rivetti to the family
tree — which the row gate caught only as «place fell from 52 to 51».

Three checks, all on the data and none on the build:

  1. every household has an `id`, and no two share one — nor a name;
  2. every member's `hid` is its household's id, and its `household` its name;
  3. within one household, no two DISTINCT person strings normalise to the same
     thing once case, punctuation and runs of whitespace are removed — and on a
     PARENT role that is absolute, because a house has one father and one
     mother however the qualifier is written.

Check 3 reports rather than fails when the two strings differ by a parenthetical
qualifier — «Chiara Rivetti» against «Chiara (Clara) Rivetti» is a real split,
but «Raffaele Falco» against «Raffaele Falco (of Giuseppe, d. 1811)» is this
archive's deliberate way of telling two people of one name apart.
"""
import json, os, re, sys, collections, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "site", "src", "data", "households.json")

def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\(.*?\)", " ", s)          # drop qualifiers: they are on purpose
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()

TRAILING = re.compile(r"\s*\([^()]*\)\s*$")

def deliberate(s):
    """
    This archive tells two people of one name apart with a qualifier at the END
    of the string — «Raffaele Falco (of Giuseppe, d. 1811)», «Vincenzo Crisci
    (the second, d. 1812)». That is on purpose and must not be flagged.

    The mistake it is worth failing on looks different: a parenthetical in the
    MIDDLE, which is an alias spelling rather than a qualifier. «Chiara Rivetti»
    against «Chiara (Clara) Rivetti» is one person written two ways, and on 23
    September 2026 it split her in two and broke her link to the family tree.
    """
    return TRAILING.search(s) is not None or "(" not in s

H = json.load(open(P, encoding="utf-8"))
fail, warn = [], []

# 1. IDENTITY. Since 23 September 2026 a household is identified by its `id`
#    and not by the string on the page, so this is the structural check David
#    asked for: two entries cannot share an id, and an entry without one has no
#    identity at all. The NAME is still required to be unique, but now as a
#    courtesy to readers rather than as the thing holding the file together.
for h in H:
    if not (h.get("id") or "").strip():
        fail.append(f"household has no id: «{h.get('name')}»")
ids = collections.Counter(h.get("id") for h in H if h.get("id"))
for i, c in sorted(ids.items()):
    if c > 1:
        fail.append(f"household id appears {c} times: «{i}»")
names = collections.Counter(h["name"] for h in H)
for n, c in sorted(names.items()):
    if c > 1:
        fail.append(f"household name appears {c} times: «{n}»")

# 2. BACK-REFERENCES. A member points at its household by id. The name is
#    carried too and must still agree, but renaming a household is now one
#    field rather than a lockstep rewrite of every member — which is the thing
#    that went wrong when a rename was done by popping from an index.
by_id = {h.get("id"): h for h in H if h.get("id")}
for h in H:
    for m in h["members"]:
        if (m.get("hid") or "") != (h.get("id") or ""):
            fail.append(f"member «{m.get('person')}» carries hid «{m.get('hid')}» "
                        f"but sits in «{h.get('id')}»")
        if (m.get("household") or "") != h["name"]:
            fail.append(f"member «{m.get('person')}» carries household "
                        f"«{m.get('household')}» but sits in «{h['name']}»")

# A HOUSE HAS ONE FATHER AND ONE MOTHER. It may have two sons called Raffaele —
# this archive holds fourteen such groups and they are on purpose. So the
# trailing-qualifier exemption below applies to CHILDREN ONLY. On a parent role
# it does not: «Giuseppe Falco» and «Giuseppe Falco (of Gelsomina Vigliotta)»
# were both the father of one household on 23 September 2026, listed as each
# other's spouse, and standing on nine of their own children's pages twice.
# Three households were in that state, all three from merging duplicate
# households earlier the same day and concatenating the member lists without
# folding the parents.
PARENT = {"father", "mother", "head", "husband", "wife"}
for h in H:
    pb = collections.defaultdict(set)
    for m in h["members"]:
        if m["role"] in PARENT:
            pb[norm(m["person"])].add(m["person"])
    for k, forms in sorted(pb.items()):
        if len(forms) > 1:
            fail.append(f"«{h['name']}» names one PARENT {len(forms)} ways — a house has one "
                        f"father and one mother: " + " / ".join(f"«{f}»" for f in sorted(forms)))

for h in H:
    buckets = collections.defaultdict(set)
    for m in h["members"]:
        if m["role"] in PARENT:
            continue                      # handled above, and stricter
        buckets[norm(m["person"])].add(m["person"])
    for k, forms in sorted(buckets.items()):
        if len(forms) < 2:
            continue
        fs = sorted(forms)
        if all(deliberate(f) for f in fs):
            # COUNTED, NOT SWALLOWED. A refusal nobody counts is
            # indistinguishable from a match — which is the fault that let
            # Luigi Falco stand on two pages, and this gate had it too until
            # 23 September 2026. Every skip is now reported, so the number of
            # deliberate splits is visible and a change in it is noticeable.
            warn.append(f"«{h['name']}» tells {len(fs)} people of one name apart "
                        f"by a trailing qualifier: " + " / ".join(f"«{f}»" for f in fs))
            continue
        fail.append(f"«{h['name']}» holds one person under {len(fs)} spellings: "
                    + " / ".join(f"«{f}»" for f in fs))

print(f"  check_households: {len(H)} households, "
      f"{sum(len(h['members']) for h in H)} member rows, "
      f"{len(warn)} deliberate same-name split(s) allowed")
for w in warn:
    print("    note  " + w)
if fail:
    for f in fail:
        print("    FAIL  " + f)
    print(f"  check_households: {len(fail)} problem(s) — this file is the archive, "
          f"not a build artefact, so nothing downstream can correct it")
    sys.exit(1)
print("  check_households: clean — no duplicated household, no member in the "
      "wrong house, no person split across two spellings")
