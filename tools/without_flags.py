#!/usr/bin/env python3
"""A copy of story.json or family-lines.json with the ribbon cards' `flags` taken off, for the kit's two contract gates.

WHY. The kit's mini flags (kit/docs/ribbon-flags.md, kit 1fa6b54) write `flags` on each ribbon card, but the kit's own
contracts at that pin (kit/data/story-schema.json for checkfamilystory.py, and checkfamilyribbon.py's family-lines schema)
do not list the field yet, so both fail every card with a flag (S0 / F0 «a field the contract does not know»). The archive
may not edit the kit. The flags themselves are checked in full by the kit's checkribbonflags.py (check:ribbonflags: every
flag recomputed, the built pages read back), so those two gates are given the cards without them; everything else in the
files, and the built pages, they check as before.

REMOVE THIS once the kit's contracts know `flags`: point check:story and check:familyribbon back at src/data directly.

    python3 tools/without_flags.py IN.json OUT.json
"""
import json, sys


def strip(doc):
    cards = list(((doc.get("ribbon") or {}).get("cards")) or [])
    fams = doc.get("families") if isinstance(doc.get("families"), list) else []
    for fam in fams:
        cards += fam.get("cards") or []
    for c in cards:
        c.pop("flags", None)
    return doc


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as fh:
        doc = json.load(fh)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(json.dumps(strip(doc), ensure_ascii=False, indent=2) + "\n")
