#!/usr/bin/env python3
"""The family ribbons and the 'how our line connects' blocks of the family pages, made from this archive's own data.

David, 27 October 2026: every family page carries the mini horizontal tree the story draws (the kit's FamilyRibbon), the
places where our direct line touches that family as small blocks under it, and the direct line in its own tint. The kit's
contract is node_modules/@daviddef/archive-kit/kit/docs/family-ribbon.md. This tool writes the archive's half of it:

  site/src/data/family-lines.json   the family pages that HAVE a ribbon (the kit's schema; its gate checkfamilyribbon.py)
  site/src/data/family-blocks.json  the family pages that do NOT: the same family entry with no cards, and why not. The
                                    page still shows the blocks (or the 'not connected' block); the kit's component draws
                                    nothing without a card, so src/components/FamilyLine.astro draws these in the kit's markup.

THIS ARCHIVE IS NOT A PEDIGREE. A ribbon is drawn only where a chain of the family is DOCUMENTED: two or more generations of
the name, each joined to the next by a parent link people.json has from a register act (via `register` or `line`), or by a
sentence of the Spine (line.json) quoted below in STATED, which this tool finds in the file or refuses to run. A link that
only the family tree holds is not a join. No generation, origin or spouse is typed here: a card is a person page, its years
are people.json's, its origin is the person's birth place (or 'place not known'), its spouse the other parent of the next
card (only where that link is documented; otherwise 'spouse not named in the records').

WHICH PAGES. The family pages are the ones in the site menu's "The families" group (layouts/Base.astro) and every page
/families/<slug>/ of families.json. /families/ (the index) and /wider-family/ are lists of families, not one family, and
/liguori/ is a page about one man (the bishop next door), not a family of this line.

HOW OUR LINE CONNECTS. Our direct line is src/data/direct-line.json (made from the story's ribbon by the kit's
directline.py): the nine Falco of the ribbon ('people': the eight men of the line, whose parent link reads 'son of', and
the living ninth generation, 'child of') and the seven wives the story marks spouseDirect ('partners', so 'daughter of').
A touch point is
  * a marriage: a person of ours whose spouse (people.json) is of the family. The story's own couple is graded by the
    story's chapter tree (the grade it gives the wife); any other spouse by the link's own source;
  * a parent: a person of ours whose parent (people.json) is of the family. Where a wife of ours is that parent, the story's
    chapter tree grades it; otherwise the link's source does (register or line: documented; tree only: family's tree), or
    a sentence of the Spine in STATED. Where people.json gives one person two parent records of the same family (the
    archive keeps duplicates rather than merging on a name), the best-graded is kept and the other is reported.
A family no person of ours touches says why, in the archive's own terms (NOT_CONNECTED_WHY).

    python3 tools/build_family_lines.py            write both files
    python3 tools/build_family_lines.py --check    exit 1 if either file is not what the data makes (the build runs this)
    python3 tools/build_family_lines.py --report   print what it found, family by family, and every duplicate it set aside
"""
import argparse, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "src", "data")
OUT_LINES = os.path.join(DATA, "family-lines.json")
OUT_BLOCKS = os.path.join(DATA, "family-blocks.json")


def load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


PEOPLE = load("people.json")
P = {p["slug"]: p for p in PEOPLE}
FAMS = load("families.json")["families"]
STORY = load("story.json")
DL = load("direct-line.json")
LINE = load("line.json")

DOC_VIAS = {"register", "line"}
COUNTRIES = {"italy", "italia", "australia"}

# A parent link the people graph has from the family tree only, which the Spine states from a record. Each is used only if
# its sentence is in line.json, word for word (markdown emphasis removed), at the generation named.
STATED = [
    # (child, parent, generation in line.json, the sentence)
    ("angela-rosa-morgillo", "orazio-morgillo", 4, "His wife Angela Rosa Morgillo, daughter of Orazio, died six days before him."),
    ("constanza-maione", "aniello-maione-majone", 6, "So Costanza Maione was the daughter of ANIELLO MAIONE, born about 1841, and ANNA MARTONE."),
    ("constanza-maione", "anna-martone", 6, "So Costanza Maione was the daughter of ANIELLO MAIONE, born about 1841, and ANNA MARTONE."),
]
# A birth place the people graph does not hold, which the Spine states from a record (same rule).
STATED_ORIGIN = [
    ("andreana-crisci-of-vincenzo-falco-andreana-crisci", "Arienzo", 3, "baptised at Arienzo on 30 November 1796"),
    ("angela-rosa-morgillo", "San Felice a Cancello", 4, "Her own birth act has been found. Not at Arienzo — at San Felice a Cancello"),
]

# Not one family: the menu entries in "The families" that are not a family page.
NOT_FAMILY = {
    "/families/": "the index of every family",
    "/wider-family/": "the wider family: many families on one page",
    "/liguori/": "a page about one man, the bishop next door, not a family of this line",
}

# Why a family is not connected, in the archive's own terms (src/pages/families.astro and families/[slug].astro).
NOT_CONNECTED_WHY = {
    "collateral": "The marriages that carried this name into the Falco were with collateral households (the table below "
                  "marks them «collateral»), not with the direct line, and no person of the line has a parent of the name.",
    "derived": "No marriage into the direct line is recorded for this name. The archive keeps the page because it names "
               "eight or more people of it, or its work list or open questions are about it.",
}


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", str(s or ""))).strip()


def line_note(gen):
    for g in LINE:
        if g.get("gen") == gen:
            return plain(g.get("note", ""))
    return ""


for child, parent, gen, quote in STATED:
    if quote not in line_note(gen):
        sys.exit("build_family_lines: the Spine (line.json generation %d) no longer says %r: the link %s -> %s is not stated"
                 % (gen, quote, child, parent))
for slug, place, gen, quote in STATED_ORIGIN:
    if quote not in line_note(gen):
        sys.exit("build_family_lines: the Spine (line.json generation %d) no longer says %r" % (gen, quote))
STATED_LINK = {(c, p): "the Spine, generation %d: «%s»" % (g, q) for c, p, g, q in STATED}
STATED_PLACE = {s: (pl, "the Spine, generation %d" % g) for s, pl, g, q in STATED_ORIGIN}


def slugify(x):
    s = unicodedata.normalize("NFD", str(x).lower())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s))


def norm(s):
    """families/[slug].astro's rule: a leading particle is not part of which family it is."""
    return re.sub(r"^(DI|DE|DEL|DELLA|DELLO|DEI|LA|LO)\s+", "", str(s or "").strip().upper())


def surnames(p):
    """«MAIONE / MAJONE»: the register writes both spellings of one name into one field."""
    return {norm(x) for x in re.split(r"\s*/\s*", str(p.get("surname") or "")) if x.strip()}


def clean(name):
    return re.sub(r"\s+", " ", re.sub(r"\s*\(.*?\)\s*", " ", str(name or ""))).strip()


def year(s):
    m = re.search(r"\b(1[5-9]\d\d|20\d\d)\b", str(s or ""))
    return m.group(1) if m else ""


def town(s):
    t = re.split(r"[,;]", str(s or ""))[0].strip()
    if not t or t in ("—", "-") or t.lower() in COUNTRIES or " to " in t:
        return ""
    return t


def grade_of(edge):
    return "doc" if set(edge.get("vias") or [edge.get("via")]) & DOC_VIAS else "lore"


# ---------------------------------------------------------------- the direct line
RIBBON = STORY["ribbon"]["cards"]
OURS = {}                                    # slug -> {generation, role, chapter, card}
for e in DL.get("people") or []:
    OURS[e["slug"]] = dict(e, role="line")
for e in DL.get("partners") or []:
    OURS.setdefault(e["slug"], dict(e, role="partner"))
for s, e in OURS.items():
    if s not in P:
        sys.exit("build_family_lines: %s is on the direct line and has no entry in people.json" % s)
    card = RIBBON[e["generation"] - 1]
    e["card"] = card
    if e["role"] == "partner" and card.get("spousePerson") != s:
        sys.exit("build_family_lines: partner %s is not the spouse on ribbon card %d" % (s, e["generation"]))


def tree_grade(chapter, slug):
    """The grade the story's chapter tree gives this person (None if the tree does not draw them)."""
    for ch in STORY.get("chapters") or []:
        if ch.get("id") != chapter:
            continue
        for row in (ch.get("tree") or {}).get("rows") or []:
            for n in row.get("nodes") or []:
                if n.get("person") == slug:
                    return n.get("grade")
    return None


def chapter_children(chapter):
    for ch in STORY.get("chapters") or []:
        if ch.get("id") == chapter:
            for row in (ch.get("tree") or {}).get("rows") or []:
                if row.get("kind") == "children":
                    return {n.get("person"): n.get("grade") for n in row.get("nodes") or [] if n.get("person")}
    return {}


# ---------------------------------------------------------------- the family pages
def menu_families():
    src = open(os.path.join(ROOT, "site", "src", "layouts", "Base.astro"), encoding="utf-8").read()
    m = re.search(r'\["The families",\s*\[(.*?)\]\]\]', src, re.S)
    if not m:
        sys.exit("build_family_lines: the menu has no «The families» group (site/src/layouts/Base.astro)")
    return re.findall(r'\["(/[^"]*)",\s*"([^"]*)"\]', m.group(1))


def written_up():
    src = open(os.path.join(ROOT, "site", "src", "lib", "writtenup.js"), encoding="utf-8").read()
    return {k: v for k, v in re.findall(r'([A-Z]+):\s*\["(/[^"]+)",', src)}


def family_pages():
    wu = written_up()
    by_slug = {slugify(f["sn"]): f for f in FAMS}
    pages, skipped = [], []
    for href, label in menu_families():
        if href in NOT_FAMILY:
            skipped.append((href, label, NOT_FAMILY[href]))
            continue
        if href.startswith("/families/"):
            continue                                       # drawn below, from families.json
        slug = href.strip("/")
        f = by_slug.get(slug)
        names = {norm(k) for k, v in wu.items() if v.rstrip("/") == "/" + slug}
        if f:
            names |= {norm(f["sn"])} | {norm(x) for x in f.get("also") or []}
        if not names:
            sys.exit("build_family_lines: the menu's family page %s names no surname (families.json, lib/writtenup.js)" % href)
        pages.append({"id": slug, "title": f["name"] if f else label, "page": href, "names": names, "fam": f})
    for f in FAMS:
        slug = slugify(f["sn"])
        pages.append({"id": "families-" + slug, "title": f["name"], "page": "/families/%s/" % slug,
                      "names": {norm(f["sn"])} | {norm(x) for x in f.get("also") or []}, "fam": f})
    return pages, skipped


# ---------------------------------------------------------------- the connections
DUPLICATES = []                               # (our person, family, kept, set aside) for the report
SET_ASIDE = []                                # (our person, record, why): a spouse record that cannot be the spouse


def close(a, b):
    """Two spellings of one name, one letter apart («Constanza» and «Costanza»): the archive's two records of one wife."""
    a, b = a.lower(), b.lower()
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return a[i + 1:] == b[i + 1:] or a[i + 1:] == b[i:] or a[i:] == b[i + 1:]


def connections_for(names):
    out = []
    for s, e in sorted(OURS.items(), key=lambda kv: (kv[1]["generation"], kv[1]["role"] != "line")):
        p = P[s]
        g, chap = e["generation"], e["storyChapter"]
        href = "/story/#" + chap
        # marriages
        couple = P.get(e["card"].get("spousePerson") or "") if e["role"] == "line" else None
        died = year(str(e["card"].get("years", "")).split("–")[-1]) if "–" in str(e["card"].get("years", "")) else ""
        for sp in p.get("spouses") or []:
            q = P.get(sp["slug"])
            if not q or not (surnames(q) & names):
                continue
            ours_couple = couple is not None and couple["slug"] == q["slug"]
            if not ours_couple and couple is not None and surnames(couple) & names and close(clean(couple["name"]), clean(q["name"])):
                DUPLICATES.append((s, sorted(names), couple["slug"], q["slug"]))      # a second record of the story's own wife
                continue
            if died and year(q.get("b")) and int(year(q.get("b"))) > int(died):
                SET_ASIDE.append((s, q["slug"], "born %s, after %s died (%s)" % (year(q.get("b")), clean(p["name"]), died)))
                continue
            if ours_couple:
                gr = tree_grade(chap, q["slug"]) or grade_of(sp)
                note = "The story's couple of generation %d." % g
            else:
                gr = grade_of(sp)
                note = "A marriage %s." % ("read in a register act" if gr == "doc" else "from the family tree only, unverified")
            out.append(conn(s, g, q, "married", gr, href, note))
        # parents
        fam_parents = [ed for ed in p.get("parents") or [] if P.get(ed["slug"]) and surnames(P[ed["slug"]]) & names]
        if not fam_parents:
            continue
        scored = []
        for ed in fam_parents:
            q = P[ed["slug"]]
            if q["slug"] in OURS and OURS[q["slug"]]["role"] == "partner":
                pe = OURS[q["slug"]]
                kid = chapter_children(pe["storyChapter"]).get(s)
                gr, note, rank = (kid or grade_of(ed)), "The story's chapter names her as his mother.", 0
            elif (s, q["slug"]) in STATED_LINK:
                gr, note, rank = "doc", "Stated by " + STATED_LINK[(s, q["slug"])] + ".", 1
            else:
                gr = grade_of(ed)
                note = "Named as a parent in a register act this archive has read." if gr == "doc" else "From the family tree only, unverified."
                rank = 1 if gr == "doc" else 2
            scored.append((rank, ed["slug"], gr, note, q))
        scored.sort(key=lambda t: (t[0], t[1]))
        best = scored[0][0]
        for rank, slug, gr, note, q in scored:
            if rank != best:
                DUPLICATES.append((s, sorted(names), scored[0][1], slug))
                continue
            # A partner is a wife (daughter of); a man of the line is a husband whose wife the story marks spouseDirect
            # (son of). The ninth generation's card has no such wife, and its person is called by relationship only.
            rel = "daughter of" if e["role"] == "partner" else ("son of" if e["card"].get("spouseDirect") else "child of")
            out.append(conn(s, g, q, rel, gr, href, note))
    return out


def origin_of(q):
    """Where a person was born: a register act first (people.json's bp from an act, a birth event with its source, a
       sentence of the Spine), then the family tree's birth place (graded lore), else nothing."""
    t = town(q.get("bp"))
    if t and (q.get("dateFrom") or {}).get("bp") in ("act", "register"):
        return t, "doc"
    for ev in q.get("events") or []:
        if str(ev.get("event", "")).lower() == "birth" and ev.get("ark") and town(ev.get("place")):
            return town(ev.get("place")), "doc"
    if q["slug"] in STATED_PLACE:
        return STATED_PLACE[q["slug"]][0], "doc"
    if t:
        return t, "lore"
    return "", ""


def conn(our, gen, q, rel, grade, href, note):
    o, _ = origin_of(q)
    c = {"ourSlug": our, "ourGeneration": gen, "theirSlug": q["slug"], "theirName": clean(q["name"]),
         "relation": rel, "grade": grade, "storyHref": href}
    if o:
        c["theirOrigin"] = "of " + o
    if note:
        c["note"] = note
    return c


# ---------------------------------------------------------------- the chain and its cards
def doc_parents(slug, names):
    out = []
    for ed in P[slug].get("parents") or []:
        q = P.get(ed["slug"])
        if not q or not (surnames(q) & names):
            continue
        if grade_of(ed) == "doc" or (slug, q["slug"]) in STATED_LINK:
            out.append(q["slug"])
    return sorted(set(out))


def chain_up(slug, names, seen=()):
    best = [slug]
    for q in doc_parents(slug, names):
        if q in seen:
            continue
        c = chain_up(q, names, seen + (slug,)) + [slug]
        if len(c) > len(best):
            best = c
    return best


def birth_year(slug):
    return int(year(P[slug].get("b")) or 9999)


AT_EVENT = re.compile(r"^(named|death|marriage|civil marriage|burial|baptism)", re.I)


def at_of(q, origin):
    dp = town(q.get("dp"))
    if dp and dp != origin and not q.get("living"):
        return dp, year(q.get("d"))
    cands = []
    for ev in q.get("events") or []:
        if not AT_EVENT.match(str(ev.get("event", ""))) or "probable" in str(ev.get("event", "")):
            continue
        if str(ev.get("event", "")).lower() == "birth":
            continue
        t = town(ev.get("place"))
        if not t or t == origin:
            continue
        d = str(ev.get("date") or "")
        y = "" if d.strip().startswith("b.") else year(d)
        cands.append((0 if y else 1, int(y or 9999), t, y))
    if not cands:
        return "", ""
    cands.sort()
    return cands[0][2], cands[0][3]


def spouse_link(slug, chain, i, names, end_ours):
    """The spouse a card shows: for a card that is not the last, the other parent of the next card; for the last, the
       direct-line husband it married (a connection), else the person's own first documented spouse."""
    p = P[slug]
    if i + 1 < len(chain):
        nxt = P[chain[i + 1]]
        other = [ed for ed in nxt.get("parents") or [] if ed["slug"] != slug]
        docd = [ed for ed in other if grade_of(ed) == "doc" or (nxt["slug"], ed["slug"]) in STATED_LINK]
        return docd[0]["slug"] if docd else None
    if end_ours:
        return end_ours
    docd = [ed for ed in p.get("spouses") or [] if grade_of(ed) == "doc"]
    return docd[0]["slug"] if docd else None


def card_of(slug, chain, i, names, end_ours):
    q = P[slug]
    living = bool(q.get("living"))
    o, og = origin_of(q)
    b, d = year(q.get("b")), year(q.get("d"))
    years = "" if living else ("%s–%s" % (b, d) if b and d else ("b. " + b if b else ("d. " + d if d else "")))
    at_place, at_year = at_of(q, o)
    sp = spouse_link(slug, chain, i, names, end_ours)
    if sp:
        s = P[sp]
        if s["slug"] in OURS and OURS[s["slug"]]["role"] == "line":
            so = OURS[s["slug"]]["card"].get("origin", "")
        else:
            so, _ = origin_of(s)
        spouse, spouse_origin = clean(s["name"]), ("of " + so if so else "place not known")
    else:
        spouse, spouse_origin = "spouse not named in the records", ""
    title = ""
    if i + 1 < len(chain):
        nxt = P[chain[i + 1]]
        stated = STATED_LINK.get((nxt["slug"], slug))
        title = "Parent of %s, %s" % (clean(nxt["name"]), ("as " + stated) if stated else "named in a register act this archive has read")
    c = {"name": clean(q["name"]), "years": years, "origin": o or "place not known", "originGrade": og or "doc",
         "spouse": spouse, "spouseOrigin": spouse_origin, "atPlace": at_place, "atYear": "" if living else at_year,
         "living": living, "person": slug}
    if sp:
        c["spousePerson"] = sp
    if title:
        c["title"] = title
    return c


def status_of(cards):
    first = cards[0]
    ys = [int(y) for c in cards for y in re.findall(r"\b(1[5-9]\d\d|20\d\d)\b", c["years"] + " " + c["atYear"])]
    span = [min(ys), None] if ys else None
    # Every generation of a ribbon is joined to the next by a record (that is the rule for drawing one), so a family is
    # never family lore here; what can be missing is where the first of it came from.
    n = len(cards)
    note = "%d generations, each joined to the next by a record" % n
    if first["origin"] == "place not known":
        st = "origin-unknown"
        note += " · where the first was born is not known"
    else:
        st = "documented"
        if first["originGrade"] == "lore":
            note += " · the first one's birthplace is the family tree's"
    return st, note, span


# ---------------------------------------------------------------- build
def build():
    pages, skipped = family_pages()
    lines, blocks, report = [], [], []
    for pg in pages:
        names = pg["names"]
        conns = connections_for(names)
        theirs = [c["theirSlug"] for c in conns if surnames(P[c["theirSlug"]]) & names]
        chain = []
        if conns:
            for t in theirs:                               # the chain through the person our line touches
                c = chain_up(t, names)
                if len(c) > len(chain):
                    chain = c
            why_none = ("this archive's people file joins the person our line touches to no parent of the name by a record"
                        if len(chain) < 2 else "")
        else:
            into = {clean(b) for row in (pg["fam"] or {}).get("into") or [] for b in row[1:]}
            best = None
            for s in sorted(p["slug"] for p in PEOPLE if surnames(p) & names):
                c = chain_up(s, names)
                key = (len(c), any(clean(P[x]["name"]) in into for x in c), -birth_year(c[-1]), "".join(c))
                if best is None or key > best[0]:
                    best = (key, c)
            chain = best[1] if best else []
            why_none = "no two generations of the name are joined by a record in this archive's people file" if len(chain) < 2 else ""
        fam = {"id": pg["id"], "title": pg["title"], "page": pg["page"]}
        if conns:
            fam_conns = conns
        else:
            kind = "derived" if (pg["fam"] or {}).get("derived") else "collateral"
            fam_conns = None
        entry_tail = {"connections": fam_conns} if fam_conns else {"notConnected": {"why": NOT_CONNECTED_WHY[kind]}}
        if len(chain) >= 2:
            end = chain[-1]
            end_ours = None
            for c in conns:
                if c["theirSlug"] == end and c["relation"] == "married":
                    end_ours = c["ourSlug"]
            cards = [card_of(s, chain, i, names, end_ours) for i, s in enumerate(chain)]
            st, note, span = status_of(cards)
            f = dict(fam, status=st, statusNote=note)
            if span:
                f["span"] = span
            f["cards"] = cards
            f.update(entry_tail)
            lines.append(f)
        else:
            f = dict(fam, noRibbon=why_none)
            f.update(entry_tail)
            blocks.append(f)
        report.append((pg, chain, conns))
    return lines, blocks, report, skipped


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--dist", help="with --check: also read the built family pages of family-blocks.json back")
    a = ap.parse_args()
    lines, blocks, report, skipped = build()
    note = ("Made by tools/build_family_lines.py from people.json, families.json, story.json, direct-line.json and the "
            "Spine; do not edit by hand. Contract: kit/docs/family-ribbon.md.")
    out_lines = dump({"_note": note, "families": lines})
    out_blocks = dump({"_note": note + " These family pages have no documented chain of two generations, so no ribbon: "
                                       "src/components/FamilyLine.astro draws their blocks alone.", "families": blocks})
    if a.report:
        for pg, chain, conns in report:
            print("%-22s %-28s ribbon %s  connections %d" % (pg["id"], pg["page"], len(chain) if len(chain) >= 2 else "-", len(conns)))
            for c in conns:
                print("      gen %d %s %s %s (%s)" % (c["ourGeneration"], c["ourSlug"], c["relation"], c["theirSlug"], c["grade"]))
        for s in skipped:
            print("not a family page: %s (%s): %s" % s)
        for d in sorted(set(SET_ASIDE)):
            print("spouse record set aside: %s has %s as a spouse, %s" % d)
        for d in sorted(set((x[0], tuple(x[1]), x[2], x[3]) for x in DUPLICATES)):
            print("duplicate record: %s has %s and %s, two records of one person of the family %s; kept the first" % (d[0], d[2], d[3], "/".join(d[1])))
        return 0
    if a.check:
        bad = []
        for path, want in ((OUT_LINES, out_lines), (OUT_BLOCKS, out_blocks)):
            try:
                have = open(path, encoding="utf-8").read()
            except OSError:
                have = None
            if have != want:
                bad.append(os.path.relpath(path, ROOT))
        if bad:
            print("build_family_lines: %s is not what the data makes: run python3 tools/build_family_lines.py" % ", ".join(bad))
            return 1
        if a.dist:
            # The kit's gate (checkfamilyribbon.py) reads back the pages of family-lines.json. The pages with no ribbon are
            # this archive's own, so they are read back here: the section for the family, one block per connection with
            # our side tinted and naming our person, or the one «not connected» block, and the legend.
            errs = []
            for f in blocks:
                path = os.path.join(a.dist, f["page"].strip("/"), "index.html")
                try:
                    html = open(path, encoding="utf-8").read()
                except OSError:
                    errs.append("%s: the page %s is not built" % (f["id"], f["page"]))
                    continue
                m = re.search(r'<section[^>]*\bdata-family="%s"[^>]*>(.*?)</section>' % re.escape(f["id"]), html, re.S)
                if not m:
                    errs.append("%s: %s has no section for the family" % (f["id"], f["page"]))
                    continue
                sec = m.group(1)
                built = re.findall(r'<li class="fr-b fr-b-(\w+)"[^>]*data-relation="([^"]+)" data-our="([^"]+)" data-their="([^"]+)"', sec)
                want = [(c["grade"], c["relation"], c["ourSlug"], c["theirSlug"]) for c in f.get("connections") or []]
                if sorted(built) != sorted(want):
                    errs.append("%s: built blocks %s, the data has %s" % (f["id"], sorted(built), sorted(want)))
                for c in f.get("connections") or []:
                    if not re.search(r'class="fr-b-our is-ours" data-ours="%s"' % re.escape(c["ourSlug"]), sec):
                        errs.append("%s: our side %s is not tinted" % (f["id"], c["ourSlug"]))
                if f.get("notConnected") and 'data-not-connected="1"' not in sec:
                    errs.append("%s: no «not connected» block" % f["id"])
                if f.get("connections") and "tinted = our direct line" not in sec:
                    errs.append("%s: no legend" % f["id"])
            for e in errs:
                print("FAIL " + e)
            if errs:
                return 1
        print("build_family_lines: ok, %d family pages with a ribbon, %d without (%d connections)" % (
            len(lines), len(blocks), sum(len(f.get("connections") or []) for f in lines + blocks)))
        return 0
    open(OUT_LINES, "w", encoding="utf-8").write(out_lines)
    open(OUT_BLOCKS, "w", encoding="utf-8").write(out_blocks)
    print("build_family_lines: wrote %d family pages with a ribbon, %d without" % (len(lines), len(blocks)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
