#!/usr/bin/env python3
"""Print every work-list «still to try» beside what the coverage page says was read.

WHY THIS EXISTS. On 21 September 2026 work-list row 79 said «still to try:
1830–1835». All six years had been read weeks earlier, in a continuous sweep of
the Arienzo death indexes for 1824–1843, and `searched.json` said so in two rows.
Nothing compares the two files, so the row would have sent a reader to open six
volumes for nothing.

WHY IT IS A REPORT AND NOT A GATE. The two files name sources differently and
neither is wrong to. `searched.json` has a structured `when` — a year or a range —
and names the ark. A work-list row names years in PROSE, inside an argument, and
often names no ark at all: row 79's six volumes appear only as the string
«1830–1835». Matching those is a judgement about whether two prose descriptions
mean the same shelf, and a gate that guesses would either cry wolf or miss the
case it was written for. So this prints the pairs and a human decides.

THE MATCH HAS TO BE ON THE KIND AS WELL AS THE YEAR. Arienzo has deaths, births,
marriages, and an index series for each, in the same years. «1830–1835 read» is
only an answer to «1830–1835 still to try» if both mean the same series — which
is why KIND below is not optional and an unclassifiable row is reported as such
rather than silently matched.

Run:  python3 tools/staleness_report.py [--all]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n): return json.load(open(os.path.join(ROOT, "site", "src", "data", n), encoding="utf-8"))

YEAR  = re.compile(r"\b(1[678]\d\d|19\d\d)\b")
RANGE = re.compile(r"\b(1[678]\d\d|19\d\d)\s*[-‐-―]\s*(1[678]\d\d|19\d\d)\b")
ARK   = re.compile(r"an_ua\d+")

# The words each series is actually called in this archive, in both files.
KINDS = {
    "deaths":    ("morti", "death"),
    "births":    ("nati", "birth", "nascite"),
    "marriages": ("matrimon", "marriage"),
    "processetti": ("processett",),
    "parish":    ("parish", "parrocch", "baptis", "battez"),
}
def kinds_of(text):
    # «ANTENATI» contains «nati», and every row in both files names it. Left in,
    # it makes every Antenati row a BIRTH row and the report is all noise. Found
    # on the first run.
    t = re.sub(r"antenati", " ", text.lower())
    found = {k for k, words in KINDS.items() if any(w in t for w in words)}
    # an INDEX of deaths is not the death register; keep them apart.
    if "indice" in t or "index" in t or "tavola" in t or "tavole" in t:
        found = {k + "-index" for k in found} or {"index"}
    return found

def years_in(text):
    out = set()
    for a, b in RANGE.findall(text):
        a, b = int(a), int(b)
        if b >= a and b - a < 120: out |= set(range(a, b + 1))
    out |= {int(y) for y in YEAR.findall(text)}
    return out

# --- what the coverage page says has been read -------------------------------
read = []   # (years, kinds, arks, label, outcome)
for r in load("searched.json"):
    blob = " ".join(str(r.get(k, "")) for k in ("when", "src", "what"))
    read.append((years_in(blob), kinds_of(blob), set(ARK.findall(json.dumps(r, ensure_ascii=False))),
                 (r.get("src") or "")[:78], r.get("outcome", "?")))

# --- what the open work list still asks for ----------------------------------
STILL = re.compile(r"(still to try|still to read|remains?|what remains|not read|never (?:been )?(?:read|opened)|"
                   r"to read|unread|next)\b[^.\n]{0,400}", re.I)
wl = load("worklist.json")
rows = wl["rows"] if isinstance(wl, dict) and "rows" in wl else wl
openrows = [r for r in rows if r.get("state") in ("next", "running", "open")]

hits = 0
for r in openrows:
    note = str(r.get("note", ""))
    for m in STILL.finditer(note):
        frag = " ".join(m.group(0).split())
        ys, ks = years_in(frag), kinds_of(frag + " " + str(r.get("what", "")))
        if not ys or not ks:
            continue
        for ryears, rkinds, rarks, label, outcome in read:
            overlap = ys & ryears
            shared  = ks & rkinds
            # A coverage row spanning a century — a commercial index, a whole
            # parish harvest — overlaps every question ever asked and answers
            # none of them. WIDE marks them instead of hiding them.
            wide = (max(ryears) - min(ryears)) > 60 if ryears else False
            if overlap and shared and (not wide or "--all" in sys.argv):
                hits += 1
                print(f"\nROW {r['n']} — {str(r.get('what'))[:74]}")
                print(f"   asks   : …{frag[:150]}…")
                print(f"   years  : {min(overlap)}–{max(overlap)} ({len(overlap)}) · {'/'.join(sorted(shared))}")
                print(f"   READ   : [{outcome}]{' WIDE' if wide else ''} {label}")
                if rarks: print(f"   arks   : {' '.join(sorted(rarks))}")
print(f"\nstaleness_report: {len(openrows)} open rows, {len(read)} coverage rows, "
      f"{hits} place(s) where an open row asks for a year and a series the coverage page records as read")
print("Each is a judgement, not a fault: a row may be re-reading at higher resolution on purpose.")
