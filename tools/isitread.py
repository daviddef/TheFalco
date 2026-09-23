#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
isitread — HAS THIS VOLUME ALREADY BEEN READ?

Written 23 September 2026, the day a sweep was spent twice.

Work-list rows 39 and 40 both said the Arienzo marriage registers for
1857-1860 «have never been swept for Falco». `site/src/data/searched.json` had
recorded all four volumes as read two days earlier, in terms — «1858 AND 1859
HOLD NO FALCO AT ALL, thirty-nine and twenty-eight images, every act read».
The work list was believed, `an_ua14262` and `an_ua14263` were read end to end
a second time, and the nil reproduced exactly.

THE TWO FILES ANSWER DIFFERENT QUESTIONS AND ONLY ONE OF THEM IS A RECORD.
The work list holds what somebody THOUGHT still needed doing. `searched.json`
holds what was actually opened. They drift, and nothing in the build chain
compares them — a gate is the wrong instrument anyway, because this archive
keeps superseded prose standing on purpose, so the stale sentence is supposed
to still be there with its correction beneath it.

What was missing was not a gate but a cheap habit: ONE COMMAND, BEFORE THE
FIRST TILE IS FETCHED.

    python3 tools/isitread.py an_ua14262 an_ua14263
    python3 tools/isitread.py 14262            # the digits are enough

It searches the coverage data, the work list, the corrections and notes/ for
the ark, and prints what each says. A hit is not proof the volume is finished
— a sweep may have read one band, or one surname. Read what it prints and
decide. A miss is not proof it is untouched either; it is proof nobody wrote
it down, which is its own finding.
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORPORA = [
    ("coverage  (searched.json — THE RECORD OF WHAT WAS READ)",
     os.path.join(ROOT, "site", "src", "data", "searched.json")),
    ("work list (what somebody THOUGHT still needed doing)",
     os.path.join(ROOT, "site", "src", "data", "worklist.json")),
    ("corrections", os.path.join(ROOT, "site", "src", "data", "corrections.json")),
    ("households", os.path.join(ROOT, "site", "src", "data", "households.json")),
]

def flat(path):
    try:
        return json.dumps(json.load(open(path, encoding="utf-8")), ensure_ascii=False)
    except Exception:
        try:
            return open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            return ""

def hits(text, needle, width=190):
    out = []
    for m in re.finditer(re.escape(needle), text, re.I):
        a = max(0, m.start() - width // 2)
        s = re.sub(r"\s+", " ", text[a:m.end() + width])
        out.append(s.strip())
    return out

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip())
        return 0
    any_hit = False
    for raw in args:
        ark = raw if raw.startswith("an_ua") else "an_ua" + re.sub(r"\D", "", raw)
        print(f"\n=== {ark}")
        found_here = False
        for label, path in CORPORA:
            hs = hits(flat(path), ark)
            if hs:
                found_here = any_hit = True
                print(f"  {label}: {len(hs)} mention(s)")
                for h in hs[:3]:
                    print("     …" + h[:300])
        ns = []
        for f in sorted(glob.glob(os.path.join(ROOT, "notes", "*.md"))):
            n = len(hits(open(f, encoding="utf-8", errors="replace").read(), ark))
            if n:
                ns.append((os.path.basename(f), n))
        if ns:
            found_here = any_hit = True
            print(f"  notes/: " + ", ".join(f"{f} ({n})" for f, n in ns[:6]))
        if not found_here:
            print("  NOT WRITTEN DOWN ANYWHERE — no coverage row, no work-list row, no note.")
    print("\nA hit is not proof the volume is finished: a sweep may have read one band,")
    print("one half, or one surname. Read what it says before deciding to read it again.")
    print("A miss is not proof it is untouched — only that nobody recorded it.")
    return 0 if any_hit else 1

if __name__ == "__main__":
    sys.exit(main())
