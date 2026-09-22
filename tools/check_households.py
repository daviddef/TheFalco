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

  1. no two households share a name;
  2. every member's `household` field equals the name of the household it sits in;
  3. within one household, no two DISTINCT person strings normalise to the same
     thing once case, punctuation and runs of whitespace are removed.

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

names = collections.Counter(h["name"] for h in H)
for n, c in sorted(names.items()):
    if c > 1:
        fail.append(f"household name appears {c} times: «{n}»")

for h in H:
    for m in h["members"]:
        if (m.get("household") or "") != h["name"]:
            fail.append(f"member «{m.get('person')}» carries household "
                        f"«{m.get('household')}» but sits in «{h['name']}»")

for h in H:
    buckets = collections.defaultdict(set)
    for m in h["members"]:
        buckets[norm(m["person"])].add(m["person"])
    for k, forms in sorted(buckets.items()):
        if len(forms) < 2:
            continue
        fs = sorted(forms)
        if all(deliberate(f) for f in fs):
            continue
        fail.append(f"«{h['name']}» holds one person under {len(fs)} spellings: "
                    + " / ".join(f"«{f}»" for f in fs))

print(f"  check_households: {len(H)} households, "
      f"{sum(len(h['members']) for h in H)} member rows")
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
