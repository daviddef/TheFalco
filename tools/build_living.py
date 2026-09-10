#!/usr/bin/env python3
"""Living people, names only.

The archive's standing rule was that the public build never named the living.
David asked on 10 September 2026 for them to be included ACROSS THE SITE, and
explicitly: "ONLY NAME, not dates of birth".

So this writes name, surname and relationship — and nothing else. No birth date,
no death date, no birthplace, no residence, no age, no record links. Those fields
exist in the tree and are deliberately dropped here.

It also computes the relationship to the anchor. The anchor is not guessed: the
MyHeritage tree marks one person «This is you».
"""
import json, re, collections

TREE = "data/myheritage-falco-tree.json"
OUT = "site/src/data/living.json"

people = json.load(open(TREE))
by_id = {p["id"]: p for p in people if p.get("id")}

anchor = next((p for p in people if p.get("rel") == "This is you"), None)
if not anchor:
    raise SystemExit("No person marked 'This is you' — cannot compute relationships.")

# The Falco line is the anchor's WIFE's maternal line, so relationships to the
# anchor run through her. Find her from the anchor's own edges.
spouse = None
for e in anchor.get("relatives") or []:
    if (e.get("rel") or "").lower() in ("your wife", "your husband", "your spouse"):
        spouse = by_id.get(e["id"])
        break

def edges(p, want):
    """ids joined to p by an edge whose label ends in `want` (mother/father/…)"""
    out = []
    for e in (p.get("relatives") or []):
        r = (e.get("rel") or "").lower()
        if r.endswith(want):
            out.append(e["id"])
    return out

# Walk straight up from the spouse: her parents, their parents, and so on.
# depth 1 = her mother/father, 2 = her grandparent, 3 = her great-grandparent…
ANCESTOR_REL = {}
if spouse:
    frontier = [(spouse["id"], 0)]
    seen = {spouse["id"]}
    while frontier:
        pid, depth = frontier.pop(0)
        p = by_id.get(pid)
        if not p:
            continue
        for want, word in (("mother", "mother"), ("father", "father")):
            for aid in edges(p, want):
                if aid in seen:
                    continue
                seen.add(aid)
                d = depth + 1
                if d == 1:
                    label = f"your wife's {word}"
                elif d == 2:
                    label = f"your wife's grand{word}"
                elif d == 3:
                    label = f"your wife's great-grand{word}"
                else:
                    label = f"your wife's {d - 2}× great-grand{word}"
                ANCESTOR_REL[aid] = label
                frontier.append((aid, d))

def clean_name(n):
    """Strip MyHeritage's verification ticks and stars; keep the maiden form."""
    n = re.sub(r"[✔⭐★]", "", str(n or ""))
    n = re.sub(r",\s*$", "", n.strip())
    return re.sub(r"\s+", " ", n).strip()

def birth_year(p):
    m = re.search(r"\b(1[6-9]\d\d|20\d\d)\b", str(p.get("b") or ""))
    return int(m.group(1)) if m else None

# MyHeritage's "alive" flag really means "no death date recorded", which is not
# the same thing. Left alone it marks a 3× great-grandfather born in 1832 as
# living. Three filters, each stated:
#   – "Unknown …" entries are placeholders for a gap, not people;
#   – a birth before 1920 means dead, whatever the flag says;
#   – anyone in the ancestor chain is by definition not living.
skipped = collections.Counter()
rows = []
for p in people:
    if not p.get("alive"):
        continue
    name = clean_name(p.get("name"))
    if not name:
        continue
    if name.lower().startswith("unknown") or "[" in name:
        skipped["placeholder"] += 1
        continue
    by = birth_year(p)
    if by is not None and by < 1920:
        skipped["born before 1920"] += 1
        continue
    if p.get("id") in ANCESTOR_REL:
        skipped["an ancestor"] += 1
        continue
    if p.get("rel") == "This is you":
        rel = "you"
    elif ANCESTOR_REL.get(p.get("id")):
        rel = ANCESTOR_REL[p["id"]]
    elif (p.get("rel") or "").lower().startswith("your "):
        rel = (p["rel"] or "").lower()          # your wife, your son…
    else:
        rel = "relative"
    rows.append({
        "name": name,
        "surname": (clean_name(p.get("last")) or "—").upper(),
        "rel": rel,
        # NOTHING ELSE. b, bp, d, dp, facts and relatives are dropped on purpose.
    })

rows.sort(key=lambda r: (r["surname"], r["name"]))
json.dump(rows, open(OUT, "w"), ensure_ascii=False, indent=1)

print(f"{len(rows)} living people written, names only")
print("  filtered out:", ", ".join(f"{v} {k}" for k, v in skipped.most_common()) or "none")
print("  anchor :", clean_name(anchor.get("name")))
print("  spouse :", clean_name(spouse.get("name")) if spouse else "—")
print("  with a computed relationship:",
      sum(1 for r in rows if r["rel"] not in ("relative",)))
print("  surnames:", ", ".join(f"{k} {v}" for k, v in
      collections.Counter(r["surname"] for r in rows).most_common(8)))
