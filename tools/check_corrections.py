#!/usr/bin/env python3
"""Refuse to ship when a correction and the data disagree.

Three times in one week a correction was published and never reached the file
the site builds from, and every one was found by accident:

  1. "Giuseppa COSSI" was re-published while households.json carried the CIOFFI
     correction — caught by auditing eight people with too many parents.
  2. "Cossi, not Cioffi" stood on the corrections page for two days while the
     household file said Cioffi — caught by an audit of the corrections page.
  3. The household NAME was corrected to Cioffi months ago and every person
     inside it kept the retired surname — caught while collecting necronyms.

The pattern is always the same shape: a correction lands in the file it was
written in and nowhere else. This gate looks for the retired side of a published
correction still standing in the data, and it is deliberately narrow — it checks
the SURNAME conflations this archive has actually been caught by, because a
general "does the data agree with the prose" checker is not writable.

Run:  python3 tools/check_corrections.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "src", "data")
def load(n): return json.load(open(os.path.join(DATA, n), encoding="utf-8"))

# A retired reading, the household it was retired IN, and the correction that did it.
# Add a row here whenever a correction retires a name; the gate then holds it.
RETIRED = [
    ("Cossi",  "Francesco Cioffi & Maria Falco",
     "the strada Camellara household is CIOFFI — corrected from the 1825 register at full resolution"),
]

fails = []
H = load("households.json")
for rule_name, household, why in RETIRED:
    pat = re.compile(r"\b" + re.escape(rule_name) + r"\b")
    for h in H:
        if h["name"] != household:
            continue
        for m in h["members"]:
            # the ACT may spell it the retired way; the PERSON may not.
            if pat.search(str(m.get("person") or "")):
                fails.append(f"{household}: person «{m['person']}» still carries the retired "
                             f"reading «{rule_name}» — {why}")

# A CHILD must not exist twice under two spellings of one household's surname.
# Restricted to role=child on purpose: a household legitimately holds a mother
# and a daughter of one forename — Sara Ruggiero the matrina and Sara Falco her
# granddaughter — and flagging those is how a gate teaches people to ignore it.
HON = re.compile(r"^(Don|Donna|Fra|Padre|Suor)\s+", re.I)
def forename(n):
    n = HON.sub("", re.sub(r"\s*\(.*?\)", "", n or "").strip())
    return n.split(" ")[0] if n else ""
def surname(n):
    n = HON.sub("", re.sub(r"\s*\(.*?\)", "", n or "").strip())
    return n.split(" ")[-1] if n else ""

for h in H:
    kids = [m for m in h["members"] if m.get("role") == "child"]
    groups = {}
    for m in kids:
        groups.setdefault(forename(m.get("person")), set()).add(m.get("person"))
    for fore, names in groups.items():
        surs = {surname(n) for n in names}
        if len(names) > 1 and len(surs) > 1:
            fails.append(f"{h['name']}: the children «{fore} …» appear under {len(surs)} surnames "
                         f"{sorted(surs)} — one child spelled two ways, or two children needing "
                         f"(the first)/(the second)")

kids = sum(1 for h in H for m in h["members"] if m.get("role") == "child")
print(f"check_corrections: {len(H)} households, {kids} child records, {len(RETIRED)} retired reading(s) held")
if fails:
    print(f"\nFAILED — {len(fails)} place(s) where a published correction has not reached the data:\n")
    for f in fails:
        print("   ", f)
    sys.exit(1)
print("check_corrections: clean — no retired reading is still standing in the data")
