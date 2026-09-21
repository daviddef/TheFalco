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
# An optional FOURTH element narrows a rule to ONE person's forename. It is there
# because on 20 September 2026 a declarant published as «Antonio Cioffi» turned
# out not to be a Cioffi at all — while GIOVANNI CIOFFI, genuinely a Cioffi, sits
# in the same household two lines below him in the same act. A household-wide
# rule would have refused the build over a name that is correct.
#
# An optional FIFTH element is the mirror of the fourth: forenames the rule must
# NOT fire on. On 21 September 2026 the 1819 birth register gave **ANDREA COSSI,
# thirty-seven, contadino, of STRADA COSSI**, witness at a Cioffi child's birth.
# He belongs to the household only as a witness, and **his surname really is
# Cossi** — this archive's own correction says so in as many words: the strada
# Cossi family are Cossi, and it is the strada Camellara family who are Cioffi.
# A household-wide rule refused the build over a reading that is right, which is
# the same fault the fourth element was added for, arriving from the other side.
# **A witness is not a member of the family whose act he signs.**
RETIRED = [
    ("Cossi",  "Francesco Cioffi & Maria Falco",
     "the strada Camellara household is CIOFFI — corrected from the 1825 register at full resolution",
     None, ("Andrea",)),
    ("Cioffi", "Michele Falco & Antonia Migliore",
     "the first declarant of Morti 1842 act 55 has no double-f ligature and is not a Cioffi; "
     "read as GASPARO, probable and unsettled", "Antonio"),
    ("Serafina", "Stefano Scarpati & Faustina Cimmino",
     "both the 1840 and the 1842 act name her FAUSTINA; Serafina was this archive's misreading"),
    ("Cioffi", "Gioacchino Crisci & Francesca Falco",
     "both acts this household rests on — Luca's of 1829 and Aniello's of 1843 — read CRISCI at "
     "magnification: a narrow r, no round o, no double-f ascender"),
]

fails = []
H = load("households.json")
for rule in RETIRED:
    rule_name, household, why = rule[0], rule[1], rule[2]
    only = rule[3] if len(rule) > 3 else None
    exempt = rule[4] if len(rule) > 4 else ()
    pat = re.compile(r"\b" + re.escape(rule_name) + r"\b")
    for h in H:
        if h["name"] != household:
            continue
        for m in h["members"]:
            if only and not str(m.get("person") or "").startswith(only):
                continue
            if any(str(m.get("person") or "").startswith(e) for e in exempt):
                continue
            # the ACT may spell it the retired way; the PERSON may not.
            if pat.search(str(m.get("person") or "")):
                fails.append(f"{household}: person «{m['person']}» still carries the retired "
                             f"reading «{rule_name}» — {why}")
            # A PROSE CHECK WAS WRITTEN HERE ON 20 SEPTEMBER 2026 AND TAKEN OUT
            # THE SAME HOUR, and the reason is worth more than the check was.
            #
            # It stripped every «…» quotation from the evidence and looked for the
            # retired reading in what was left. The motive was real: «Cossi» was
            # found that morning still standing in the prose of atto 54 of 1828,
            # beside the corrected person name, months after the rule above was
            # written to hold it.
            #
            # It found that one. It also raised EIGHT false alarms, and six of
            # them were sentences like «the strada Camellara household is CIOFFI,
            # NOT COSSI» — the archive's own withdrawals, saying so. One was a
            # DIFFERENT family, the Cossi of strada Cossi, correctly named.
            #
            # THE HOUSE STYLE AND THE GATE CANNOT BOTH EXIST. This archive leaves
            # a correction visible beside the thing it corrected, on purpose. To a
            # regular expression a visible withdrawal is indistinguishable from a
            # correction that never happened. Narrowing it — «flag only when the
            # right reading is absent from the same sentence» — still failed on
            # the strada Cossi family, and each narrowing is another rule nobody
            # will remember. The docstring above already says it: a general
            # «does the data agree with the prose» checker is not writable, and a
            # gate that cries wolf gets switched off.
            #
            # So the prose is not checked, and that is a known hole, recorded on
            # the corrections page rather than papered over.

# ---------------------------------------------------------------------------
# RETIRED PHRASES — the hole the comment above describes, closed for the cases
# where it CAN be closed.
#
# Added 20 September 2026, the day «act 26 of 15 December 1814» was found alive
# in NINE files and on six published pages, a week after the marriage index had
# given 15 October. Nothing compared them. The surname rules above could not see
# it, because it is not a surname and not in a `person` field.
#
# Why this one is safe where the general prose check was not. A retired SURNAME
# is a word the documents themselves legitimately contain, so a regex cannot tell
# the archive's own withdrawal from an uncorrected claim. A retired PHRASE here is
# this archive's own wording — «act 26 of 15 December 1814» is not something a
# register says — so any unquoted occurrence is a claim, not a quotation.
#
# The one exemption is the house style: this archive shows a retired reading
# inside GUILLEMETS, beside the thing that replaced it. So guillemet spans are
# stripped before the search, which lets «…» quote the dead reading forever and
# still refuses it as a live statement.
RETIRED_PHRASES = [
    ("act 26 of 15 December 1814",
     "the marriage is ACT 16 of 15 OCTOBER 1814 — read from an_ua14218 img 9, and proved by the "
     "register's order: act 14 is 2 Oct, act 15 is 6 Oct, act 17 is 2 Dec"),
    ("ACT No. 26",
     "same — there is no act 26 in the 1814 Arienzo marriage register; it runs to act 17"),
    ("8 December 1814",
     "the notarial consents are 8 SEPTEMBER 1814, registered at Arienzo 12 September"),
    ("Salvio Morgillo",
     "both 1814 consents were taken by FELICE MORGILLO; no Salvio Morgillo appears in the dossier"),
    ("VALERIO CARFORA",
     "the bride's father is FRANCESCO CARFORA \u2014 his own consent of 1 January 1860 (an_ua14207 "
     "bundle 3 img 33) spells it in full, and Nati 1830 act 142 (an_ua14427 img 145R) names him "
     "twice; \u00abVa-/lerio\u00bb was this archive's reading of \u00abFran-/cesco\u00bb"),
    ("Valerio Carfora", "same \u2014 the forename is FRANCESCO"),
    ("D'AMBROGIO maggiore, di anni DICIANNOVE",
     "she is «di anni TRENOVE» \u2014 thirty-nine \u2014 read at the leaf's full 3,200 pixels; the initial is a "
     "crossed ascender, and the act calls her MAGGIORE, which nineteen could not be"),
]

GUILLEMET = re.compile(r"\u00ab.*?\u00bb", re.S)
SKIP = {"corrections.json", "searchindex.json", "changes.json", "researchlog.json",
        "people.json", "register.json", "living.json", "married-in.json",
        "people-aliases.json", "people-register.tsv"}

def _scan_dir(d, rel):
    for name in sorted(os.listdir(d)):
        if name in SKIP or not name.endswith((".json", ".tsv", ".md")):
            continue
        p = os.path.join(d, name)
        if not os.path.isfile(p):
            continue
        try:
            body = open(p, encoding="utf-8").read()
        except OSError:
            continue
        stripped = GUILLEMET.sub(" ", body)
        for phrase, why in RETIRED_PHRASES:
            if phrase in stripped:
                fails.append(f"{rel}/{name}: the retired reading \u00ab{phrase}\u00bb is still stated "
                             f"as fact (not inside \u00ab\u00bb) \u2014 {why}")

_scan_dir(DATA, "site/src/data")
_scan_dir(os.path.join(ROOT, "data"), "data")


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
print(f"check_corrections: {len(H)} households, {kids} child records, "
      f"{len(RETIRED)} retired surname(s) and {len(RETIRED_PHRASES)} retired phrase(s) held")
if fails:
    print(f"\nFAILED — {len(fails)} place(s) where a published correction has not reached the data:\n")
    for f in fails:
        print("   ", f)
    sys.exit(1)
print("check_corrections: clean — no retired reading is still standing in the data")
