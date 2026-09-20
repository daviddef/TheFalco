#!/usr/bin/env python3
"""The research log, generated from the archive's own working notes.

Thirty-eight files in notes/ are the actual record of what was read and when.
This turns them into a page rather than leaving them to be read raw on GitHub —
their headline, their state, and how much of each volume was got through.
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES = os.path.join(ROOT, "notes")
OUT = os.path.join(ROOT, "site", "src", "data", "researchlog.json")

rows = []
for fn in sorted(os.listdir(NOTES)):
    if not fn.endswith(".md"): continue
    src = open(os.path.join(NOTES, fn), encoding="utf-8").read()
    head = next((l.lstrip("# ").strip() for l in src.splitlines() if l.startswith("# ")), fn[:-3])
    year = (re.search(r"\b(18\d\d)\b", fn) or [None, None])[1]
    kind = "births" if "birth" in fn else "deaths" if "death" in fn else "other"
    done = bool(re.search(r"\bCOMPLETE\b|VOLUME COMPLETE", src))
    acts = re.search(r"acts?\s+1[–-](\d+)", src)
    imgs = re.search(r"images?\s+\d+[–-](\d+)", src)
    dupes = len(re.findall(r"DUPLICATE of image", src))
    # the first bolded sentence after the header is the note's own summary
    lead = ""
    for m in re.finditer(r"^\*\*(.+?)\*\*", src, re.M):
        t = re.sub(r"\s+", " ", m.group(1)).strip()
        if len(t) > 40: lead = t[:300]; break
    # THE KEY IS WHAT THE WORK LIST POINTS AT. `checkcovers.py` resolves a work-list
    # row's «covers: log:NAME» against this column, and it was missing from this
    # generator while every consumer expected it — so a regeneration silently blanked
    # thirty coverage links and the gate refused the build. It is the filename stem,
    # lowercased, which is how the committed file has always spelt it (QUEUE.md -> queue).
    # OUTSTANDING IS NOT THE OPPOSITE OF COMPLETE, and conflating them cost a day.
    #
    # `complete` answers «was this REGISTER read end to end», and the page shows
    # it as a chip on each volume. The work list's «research files not finished»
    # account was pointed at `not complete`, which swept in all fifty-three
    # FINDING files as well — the death of Matteo Falco, the parish marriage
    # indexes, every FindMyPast harvest — because a finding file has no reason to
    # contain the word COMPLETE. Forty-four closed pieces of work were being
    # counted as outstanding.
    #
    # A file is outstanding when it is a per-volume SWEEP that has not finished.
    # This archive names those `*-progress.md` and nothing else, which is a real
    # convention and not a guess: thirty-four of the eighty-seven files carry it.
    progress = fn.endswith("-progress.md")
    rows.append({"file": fn, "key": fn[:-3].lower(), "title": head, "year": year, "kind": kind,
                 "outstanding": progress and not done,
                 "complete": done, "acts": int(acts.group(1)) if acts else None,
                 "images": int(imgs.group(1)) if imgs else None,
                 "dupes": dupes, "lead": lead,
                 "bytes": os.path.getsize(os.path.join(NOTES, fn))})

rows.sort(key=lambda r: (r["year"] or "9999", r["file"]))
json.dump(rows, open(OUT, "w"), ensure_ascii=False, indent=0)
print(f"{len(rows)} notes indexed")
print("  complete volumes:", sum(1 for r in rows if r["complete"]))
print("  total acts       :", sum(r["acts"] or 0 for r in rows))
print("  total words      :", sum(r["bytes"] for r in rows) // 6)
