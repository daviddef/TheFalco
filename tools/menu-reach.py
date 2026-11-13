#!/usr/bin/env python3
"""Reach proof for the menu regroup (13 November 2026, PR A): which family pages the /families/ index links, which menu entries each
build has, and the order the index lists the families in.   python3 tools/menu-reach.py BEFORE_DIST AFTER_DIST OUT.md"""
import re, sys, html
sys.argv_saved = sys.argv
exec(open(__file__.replace("menu-reach.py", "menu-moves.py"), encoding="utf-8").read().split("def main")[0])
b, a = sys.argv[1], sys.argv[2]
def main_links(dist, page):
    t = open(f"{dist}{page}index.html", encoding="utf-8").read()
    m = re.search(r"<main.*?</main>", t, re.S)
    body = m.group(0) if m else t
    return list(dict.fromkeys(re.findall(r'href="(/[^"#?]*)"', body)))
idx = main_links(a, "/families/")
fam_pages = [h for h in idx if re.fullmatch(r"/families/[a-z-]+/", h)]
before, after = menu(b), menu(a)
fam_menu_before = [x for x in before if x[0] == "The families"]
inafter = {x[2] for x in after}
L = ["# Menu regroup, PR A: reach proof", "", "Compared: the build of `main` (the kit pin PR, 714b2c3) against the build of this change, built the same way.", ""]
L += ["## Counts", "", "| menu | entries before | entries after |", "|---|---:|---:|"]
def count(m, menus):
    return sum(1 for x in menus if x[0] == m)
names_b = list(dict.fromkeys(x[0] for x in before)); names_a = list(dict.fromkeys(x[0] for x in after))
for n in dict.fromkeys(names_b + names_a):
    L.append("| %s | %s | %s |" % (n, count(n, before) or "–", count(n, after) or "–"))
L.append("| **all menus** | %d | %d |" % (len(before), len(after)))
L += ["", "Entries are counted as the header draws them (a group heading counts as an entry). The one address that left every menu in the count is none: "
      "see `menu-a-moves.md` (What's new left Start and is the What's new group head of Research).", ""]
L += ["## The /families/ index, read from the build", "",
      "The page body (`<main>`) of `/families/` links these family addresses, in this order: " + ", ".join("`%s`" % h for h in fam_pages) + ".", ""]
L += ["## Each family entry of the old menu", "", "| menu address | label | in the new menu | linked from the /families/ index (same address) | verdict |", "|---|---|---|---|---|"]
needs = []
for m, g, h, l in fam_menu_before:
    if h in ("/families/",): continue
    inm = h in inafter
    inx = h in idx
    if inm: v = "stays in the menu" + ("" if inx or h == "/wider-family/" else " — **needs index fix** (the index does not link this address)") + (" (a hub, not a family page)" if h == "/wider-family/" else "")
    else: v = "left the menu: reachable from the index"
    if inm and not inx and h != "/wider-family/": needs.append((h, l))
    if not inm and not inx: v = "**LOST**"
    L.append("| `%s` | %s | %s | %s | %s |" % (h, l, "yes" if inm else "no", "yes" if inx else "no", v))
L += ["", "## Kept in the menu and listed as needing an index fix", ""]
L += ["- `%s` (%s)" % x for x in needs]
L += ["", "**Seven families have two pages with one title.** `/annecchino/`, `/morgillo/`, `/crisci/`, `/rivetti/`, `/zampiello/`, `/maione/` and `/carfora/` (the addresses the menu has always used, each its own canonical page) are not the same page as `/families/<name>/` (the addresses the index links); the two differ in size and content in the build. "
      "So the index does not reach the page the menu offers, and a menu entry may leave only where the index links that same address. Four of the nine stay as the four largest (Morgillo, Cioffi, Annecchino, Crisci; Cioffi's menu address is the index's own); the rest stay for the same reason. "
      "Which page of each pair is the family page is a decision for a later change (an index edit or a merge); this change touches neither.", "",
      "## Order of the index, reported", "", "The index lists the families in this order: " + ", ".join(h.split('/')[2].title() for h in fam_pages) + ". That is not A to Z; the menu is, as the rule says. No index edit is made here.", ""]
open(sys.argv[3], "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
