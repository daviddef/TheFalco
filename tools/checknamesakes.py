#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One page per person: does every person's page list exactly the other people of their name?

    python3 ../tools/checknamesakes.py --dist "${ARCHIVE_OUT:-dist}"        # from site/; `npm run check:namesakes`
    python3 ../tools/checknamesakes.py --selftest                           # plants one fault per rule

WHAT THIS GUARDS (23 November 2026). A person has one page, /people/<slug>/. When other people in the archive carry the same name, the page
ends with "Others of the same name" (#namesakes), whose list (#others-of-this-name) is one link to each of THEIR pages. The /who/<name>/
pages are NOT redirected here, as they are on Booyzen: a /who/ page is a page about a NAME and gathers every register record that carries
it (a name is not a person, and most names never reach a person page), so it stays. What must hold between the two is checked from the BUILD
and from nothing the page generator used:

  sets      derived here, in Python, from the NAME of every person (site/src/data/people.json; the h1 of a page is the kit's reading of the
            name and is not always the whole name: "(Maria) Carmela di Guida / Guido (Falco)"), by the rule the /who/ pages have always
            used (site/src/lib/namesets.js): the parenthesis dropped, a "detto" nickname dropped, case folded; an accent or a question
            mark is a different name. The LISTS are read from the built pages, so the generator's own sets are not trusted.
  missing   a page's list lacks a person of its name.
  extra     it lists a page that does not carry the name, or itself.
  absent    a name is shared and the page has no list, or the page has a list and nobody shares its name.
  living    a living person's page (noindex) has a list: it is a name and a place and nothing else.
  who       a /who/<name>/ page's "Has the archive identified anyone of this name?" card does not list exactly the person pages of that name
            (the card and a person's own list are one rule), or a person page links a /who/ page that is not built, or /who/ lost an address.

A living person is never named in a message (their slug can carry a year): their page is reported as "a living person's page".
Exit 0 clean, 1 findings, 2 it could not see what it checks (no build, no person page, no /who/ page).
"""
import argparse
import html
import json
import os
import re
import sys

SECTION = "others-of-this-name"
CARD = "Has the archive identified anyone of this name?"


def text_of(x):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()


def key_of(name):
    """The /who/ rule: parenthesis dropped, apostrophes alike, a 'detto' nickname dropped, case folded. Nothing else."""
    n = html.unescape(name or "")
    n = re.sub(r"\s*\(.*?\)\s*", " ", n).replace("’", "'").replace("‘", "'")
    n = re.sub(r"\s+", " ", n).strip()
    return re.sub(r"\s+detto\s+.+$", "", n, flags=re.I).lower()


def written_key(name):
    """A /who/ page's own name: the same, without the nickname rule (a /who/ page of '... detto X' identifies nobody under the nickname)."""
    n = html.unescape(name or "")
    n = re.sub(r"\s*\(.*?\)\s*", " ", n).replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", n).strip().lower()


def read_pages(dist):
    pages = {}
    for root, _dirs, files in os.walk(dist):
        if "index.html" in files:
            rel = os.path.relpath(root, dist).replace(os.sep, "/")
            route = "/" if rel == "." else "/" + rel + "/"
            with open(os.path.join(root, "index.html"), encoding="utf-8", errors="replace") as f:
                pages[route] = f.read()
    sm = os.path.join(dist, "sitemap.xml")
    sitemap = open(sm, encoding="utf-8").read() if os.path.exists(sm) else ""
    return pages, sitemap


def h1_of(raw):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    return text_of(m.group(1)) if m else ""


def listed(raw):
    """(has the section, the person pages its list links to, in order)"""
    m = re.search(r'id="%s"' % SECTION, raw)
    if not m:
        return False, []
    ul = re.search(r"(.*?)</ul>", raw[m.end():], re.S)
    return True, re.findall(r'href="(/people/[^"#?]+/)"', ul.group(1) if ul else "")


def identified(raw):
    """The person pages a /who/ page's 'identified' card links."""
    i = raw.find(CARD)
    if i < 0:
        return None
    j = raw.find("</div>", i)
    return re.findall(r'href="(/people/[^"#?]+/)"', raw[i:j if j > 0 else len(raw)])


def check(pages, sitemap, names):
    """(findings, counts, setof) over an in-memory build: route -> html."""
    findings = []
    persons = {}
    unknown = []
    for route, raw in pages.items():
        if route.startswith("/people/") and route != "/people/" and "data-person-page" in raw:
            slug = route[len("/people/"):-1]
            if slug not in names:
                unknown.append(route)
                continue
            persons[route] = {"key": key_of(names[slug]), "living": bool(re.search(r'<meta name="robots" content="[^"]*noindex', raw[:6000]))}
    nopage = [s for s in names if "/people/%s/" % s not in pages]
    if unknown:
        findings.append("sets: %d built person page(s) are of nobody people.json holds" % len(unknown))
    if nopage:
        findings.append("sets: %d person(s) in people.json have no built page" % len(nopage))
    who = {r: s for r, s in pages.items() if r.startswith("/who/") and r != "/who/"}
    if not persons or not who or "/who/" not in pages:
        return None, {}, {}
    label = lambda r: "a living person's page" if persons.get(r, {}).get("living") else r

    group = {}
    for r, p in persons.items():
        group.setdefault(p["key"], []).append(r)
    setof = {r: set(group[p["key"]]) - {r} for r, p in persons.items()}
    shared = {k for k, m in group.items() if len(m) > 1}

    with_list = 0
    for r, others in sorted(setof.items()):
        has, got = listed(pages[r])
        if persons[r]["living"]:
            if has:
                findings.append("living: %s has a #%s section; a living person's page is a name and a place" % (label(r), SECTION))
            continue
        if has:
            with_list += 1
        if others and not has:
            findings.append("absent: %s shares its name with %d other page(s) and has no #%s list" % (label(r), len(others), SECTION))
            continue
        if has and not others:
            findings.append("absent: %s has a #%s list and nobody shares its name" % (label(r), SECTION))
        miss = sorted(others - set(got))
        extra = sorted(set(got) - others)
        if miss:
            findings.append("missing: %s does not list %d of its name: %s" % (label(r), len(miss), ", ".join(label(x) for x in miss)))
        if extra:
            findings.append("extra: %s lists %d that do not carry its name: %s" % (label(r), len(extra), ", ".join(label(x) for x in extra)))
        # a link from the person page to the /who/ page of the name must land on a built name page
        for w in set(re.findall(r'href="(/who/[^"#?]+/)"', pages[r])):
            if w not in who:
                findings.append("who: %s links %s, which is not built" % (label(r), w))

    # ---- the /who/ pages: the 'identified' card is the same set, said from the other side
    cards = 0
    for r, raw in sorted(who.items()):
        got = identified(raw)
        if got is None:
            findings.append("who: %s has no '%s' card" % (r, CARD))
            continue
        cards += 1
        want = set(group.get(written_key(h1_of(raw)), []))
        if set(got) != want:
            findings.append("who: %s lists %d person page(s) and the person pages of that name are %d (missing %d, extra %d)"
                            % (r, len(set(got)), len(want), len(want - set(got)), len(set(got) - want)))
    if "/who/" not in sitemap and not re.search(r"<loc>[^<]*/who/</loc>", sitemap):
        findings.append("who: /who/ (Every Name) is not in the sitemap")
    counts = {"person pages": len(persons), "with a list": with_list, "shared names": len(shared),
              "people who share a name": sum(len(group[k]) for k in shared), "/who/ name pages checked": cards}
    return findings, counts, setof


def selftest(pages, sitemap, names):
    f0, _c, setof = check(pages, sitemap, names)
    ok = True
    print("  control: the untouched build -> %d finding(s)%s" % (len(f0), "" if not f0 else "  <-- SHOULD BE 0"))
    if f0:
        ok = False
    live = lambda r: bool(re.search(r'<meta name="robots" content="[^"]*noindex', pages[r][:6000]))
    shared = sorted(r for r, o in setof.items() if o and not live(r))
    solo = sorted(r for r, o in setof.items() if not o and not live(r))
    lives = sorted(r for r in setof if live(r))
    if not shared or not solo or not lives:
        print("  no shared name, unshared person or living person to plant against: refusing")
        return False
    a = shared[0]

    def planted(name, mutate, want):
        nonlocal ok
        v = dict(pages)
        mutate(v)
        got, _c, _s = check(v, sitemap, names)
        hit = any(g.startswith(want) for g in (got or []))
        print("  %-52s %s" % (name, "caught" if hit else "MISSED  <-- the gate cannot see this"))
        ok = ok and hit

    other = sorted(setof[a])[0]

    def drop_from_list(v):
        i = v[a].index('id="%s"' % SECTION)
        v[a] = v[a][:i] + re.sub(r'<li[^>]*>(?:(?!</li>).)*?href="%s".*?</li>' % re.escape(other), "", v[a][i:], count=1, flags=re.S)
    planted("a person of the name left off a list", drop_from_list, "missing")

    def add_stranger(v):
        i = v[a].index('id="%s"' % SECTION)
        j = v[a].index("</ul>", i)
        v[a] = v[a][:j] + '<li><a href="%s">x</a></li>' % solo[0] + v[a][j:]
    planted("a stranger added to a list", add_stranger, "extra")
    planted("a list on a name nobody shares",
            lambda v: v.__setitem__(solo[0], v[solo[0]].replace("</main>", '<section><ul id="%s"><li><a href="%s">x</a></li></ul></section></main>' % (SECTION, a), 1)), "absent")
    planted("a shared name with no list", lambda v: v.__setitem__(a, v[a].replace('id="%s"' % SECTION, 'id="nothing"')), "absent")
    planted("a list on a living person's page",
            lambda v: v.__setitem__(lives[0], v[lives[0]].replace("</main>", '<ul id="%s"><li><a href="%s">x</a></li></ul></main>' % (SECTION, a), 1)), "living")
    planted("a link to a /who/ page that was never built",
            lambda v: v.__setitem__(a, v[a].replace('id="%s"' % SECTION, 'id="%s"' % SECTION, 1).replace("</main>", '<a href="/who/never-built-name/">x</a></main>', 1)), "who")
    w = next(r for r in sorted(pages) if r.startswith("/who/") and r != "/who/" and identified(pages[r]))
    planted("a /who/ card that drops a person",
            lambda v: v.__setitem__(w, v[w][:v[w].index(CARD)] + re.sub(r"<li[^>]*>.*?</li>", "", v[w][v[w].index(CARD):], count=1, flags=re.S)), "who")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--people", default="src/data/people.json", help="the people the site is built from (slug, name)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.dist):
        print("checknamesakes: %s is not a directory; nothing was checked" % a.dist)
        return 2
    if not os.path.isfile(a.people):
        print("checknamesakes: %s is not a file; nothing was checked" % a.people)
        return 2
    with open(a.people, encoding="utf-8") as fh:
        names = {p["slug"]: p["name"] for p in json.load(fh)}
    pages, sitemap = read_pages(a.dist)
    if a.selftest:
        return 0 if selftest(pages, sitemap, names) else 1
    findings, counts, _setof = check(pages, sitemap, names)
    if findings is None:
        print("checknamesakes: no person page or no /who/ page in %s; nothing was checked" % a.dist)
        return 2
    for f in findings:
        print("  FAIL  " + f)
    print("checknamesakes: " + ", ".join("%d %s" % (v, k) for k, v in counts.items()) + "; %d finding%s" % (len(findings), "" if len(findings) == 1 else "s"))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
