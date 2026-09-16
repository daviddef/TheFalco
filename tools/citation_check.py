#!/usr/bin/env python3
"""List the ANTENATI citations that need following, hardest-load first.

Eight citations were found on 15 September pointing one page early — every one
copied from a note written on ZERO-BASED harvest numbering while
`tools/antenati.py` is one-based. They were found by accident, and nothing in
the build can find the rest: `checkarchive` verifies that links reach pages, and
no gate opens an image.

So this is a reading job, and the only sane way to spend it is in order of how
much each citation is holding up. A wrong image on a fact with three other
sources is untidy. A wrong image on a fact with none is a fact with none.

    python3 tools/citation_check.py            # the twenty most load-bearing
    python3 tools/citation_check.py --all      # every one
    python3 tools/citation_check.py --volume an_ua14319
    python3 tools/citation_check.py --json data/citation-check.json

Each line prints the render command that puts the cited band on screen, so
verifying one is a copy and a glance: does the act number match, does the date
match, is the name there.
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAT = re.compile(r"(an_ua\d+)\s+img(\d+)([lr])?\s*(?:act|atto)?\s*(\d+)?", re.I)

def load():
    H = json.load(open(os.path.join(ROOT, "site/src/data/households.json"), encoding="utf-8"))
    rows = []
    for h in H:
        for m in h["members"]:
            ark = str(m.get("ark") or "")
            g = PAT.search(ark)
            if not g:
                continue
            rows.append({"person": m.get("person"), "event": m.get("event"),
                         "date": m.get("date"), "household": h["name"],
                         "ark": g.group(1), "img": int(g.group(2)),
                         "half": (g.group(3) or "r").lower(), "act": g.group(4),
                         "corrected": "image number corrected" in ark})
    seen = collections.Counter((r["person"], r["event"]) for r in rows)
    for r in rows:
        r["others"] = seen[(r["person"], r["event"])] - 1
    # sole support first, then by volume so one fetch serves several checks
    rows.sort(key=lambda r: (r["others"], r["ark"], r["img"]))
    return rows

def year_of(ark):
    n = int(ark[5:])
    # births = year + 12597, deaths = year + 12502, marriage REGISTERS = year + 12404
    for base, kind in ((12597, "births"), (12502, "deaths"), (12404, "marriages")):
        y = n - base
        if 1809 <= y <= 1866:
            return f"{kind} {y}"
    return "?"

def main():
    rows = load()
    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump(rows, open(p, "w"), ensure_ascii=False, indent=1)
        print(f"{len(rows)} citations -> {p}")
        return
    if "--volume" in sys.argv:
        v = sys.argv[sys.argv.index("--volume") + 1]
        rows = [r for r in rows if r["ark"] == v]
    limit = len(rows) if "--all" in sys.argv or "--volume" in sys.argv else 20

    sole = sum(1 for r in rows if r["others"] == 0)
    print(f"{len(rows)} ANTENATI citations · {sole} are the SOLE support for their fact "
          f"· {sum(1 for r in rows if r['corrected'])} already corrected\n")
    for r in rows[:limit]:
        flag = "SOLE" if r["others"] == 0 else f"+{r['others']}"
        done = " [corrected 15 Sep]" if r["corrected"] else ""
        print(f"  {flag:>5}  {str(r['person'])[:30]:30} {str(r['event'])[:18]:18} "
              f"{str(r['date'])[:14]:14} {r['ark']} img{r['img']}{r['half'].upper()}"
              f"{' act'+r['act'] if r['act'] else ''}  ({year_of(r['ark'])}){done}")
        print(f"         python3 tools/antenati.py zoom {r['ark']} {r['img']} "
              f"--width 3000 --band 0.12 0.34 --half {r['half'].upper()} --out /tmp/c.jpg")
    if limit < len(rows):
        print(f"\n  … and {len(rows)-limit} more. --all for every one, "
              f"--volume an_uaNNNNN to do a whole volume in one sitting.")

if __name__ == "__main__":
    main()
