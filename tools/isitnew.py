#!/usr/bin/env python3
"""Ask whether a finding is already in this archive, BEFORE writing it up.

Six times in one week a finding was announced that this archive already held,
and five of the six were re-derived from something it had already written down:

  the Nudgee graves were in three files when they were announced; the Cioffi
  correction was standing in the household file when it was re-broken; the
  deacon's death act was in the corrections log and in no data file; the
  printed-year trap and the 1817 nil were both in notes/; and "1859 opened"
  duplicated an entry on the corrections page itself, from the same tavola, on
  the previous day.

Reading the notes first is a habit, and habits have now failed six times. This
is the check that runs instead: one command, every corpus, before the write-up.

    python3 tools/isitnew.py an_ua14416 "Crescenzo Falco" atto99
    python3 tools/isitnew.py "Pasqua Falco" Carfora 1880

Every argument is searched independently, case-insensitively, across the
corrections, the work list, the household files, the people and register data,
the searched page, and all 80-odd progress notes. It prints where each term
already appears. It does not judge — a hit is not proof the finding is old, and
a miss is not proof it is new. It just means nobody can say they did not look.
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPORA = [
    ("corrections",   [os.path.join(ROOT, "site/src/data/corrections.json")]),
    ("work list",     [os.path.join(ROOT, "site/src/data/worklist.json")]),
    ("households",    [os.path.join(ROOT, "site/src/data/households.json"),
                       os.path.join(ROOT, "data/households.tsv")]),
    ("people",        [os.path.join(ROOT, "site/src/data/people.json")]),
    ("register",      [os.path.join(ROOT, "site/src/data/register.json"),
                       os.path.join(ROOT, "data/people-register.tsv")]),
    ("searched page", [os.path.join(ROOT, "site/src/pages/searched.astro")]),
    ("notes/",        sorted(glob.glob(os.path.join(ROOT, "notes", "*.md")))),
]

def load(paths):
    out = []
    for p in paths:
        if os.path.exists(p):
            out.append((os.path.relpath(p, ROOT),
                        open(p, encoding="utf-8", errors="replace").read()))
    return out

def context(text, i, n=90):
    seg = re.sub(r"\s+", " ", text[max(0, i - n): i + n])
    return seg.strip()

def main():
    terms = [t for t in sys.argv[1:] if t.strip()]
    if not terms:
        sys.exit(__doc__)
    corpora = [(name, load(paths)) for name, paths in CORPORA]
    total = 0
    for t in terms:
        pat = re.compile(re.escape(t), re.I)
        print(f"\n=== {t!r}")
        found = False
        for name, files in corpora:
            hits = []
            for rel, text in files:
                for m in list(pat.finditer(text))[:3]:
                    hits.append((rel, context(text, m.start())))
            if hits:
                found = True
                print(f"  {name}: {len(hits)} hit(s)")
                for rel, ctx in hits[:3]:
                    print(f"     {rel}")
                    print(f"       …{ctx}…")
        if not found:
            print("  nothing, in any corpus")
        else:
            total += 1
    print(f"\n{total} of {len(terms)} term(s) already appear somewhere in this archive.")
    print("A hit is not proof the finding is old. A miss is not proof it is new.")
    print("It means nobody can say they did not look.")

if __name__ == "__main__":
    main()
