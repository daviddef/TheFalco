#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One page per person: is exactly the register text that is honestly about a person on that person's page, and nowhere else?

    python3 ../tools/checkdossiers.py --dist "${ARCHIVE_OUT:-dist}"        # from site/; `npm run check:dossiers`
    python3 ../tools/checkdossiers.py --selftest                           # plants one fault per rule

WHAT THIS GUARDS (23 November 2026). /who/<name>/ is a page about a NAME: it gathers every register row that carries the name and stays where it
is. A person's page may repeat, word for word and with its source link, the rows the DATA ties to that person (site/src/lib/dossier.js; the
rule is in its header): a row that is a line of a register page or act the person's own events already cite, or that names both of the parents
the page draws on a day of one of the person's events; never an ambiguous one, never a row already printed in an event, never the archive's own
household and tree rows, never a living person, never a row dated 1946 or later. What is checked comes from the BUILD and from the data files,
and nothing the page generator computed:

  derive    the designated rows of every person are derived HERE, in Python, from register.json and people.json (a second implementation of the
            rule: the page's own is not trusted); a person's page is read from dist.
  missing   a designated row is not on its person's page.
  extra     a page carries a row that is not designated to that person, or a row id that is not a register row.
  twice     the same row is on two person pages (a row is never split across people), or on one page twice.
  verbatim  a folded row's words, source text or link are not the register row's.
  why       the reason printed under a row is not the reason the data gives (page / parents).
  living    a living person's page has the section or a row (a living person is a name and a place and nothing else).
  who       a folded row is not on the name's /who/ page, or the page's link to /who/ is not built, or its count is not the name's row count.

A living person is never named in a message. Exit 0 clean, 1 findings, 2 it could not see what it checks.
"""
import argparse
import hashlib
import html
import json
import os
import re
import sys
import unicodedata

KIND_OWN = {"household", "tree"}
MON = {"jan": 1, "gen": 1, "gennaio": 1, "january": 1, "feb": 2, "febbraio": 2, "february": 2, "mar": 3, "marzo": 3, "march": 3, "apr": 4,
       "aprile": 4, "april": 4, "may": 5, "mag": 5, "maggio": 5, "jun": 6, "giu": 6, "giugno": 6, "june": 6, "jul": 7, "lug": 7, "luglio": 7,
       "july": 7, "aug": 8, "ago": 8, "agosto": 8, "august": 8, "sep": 9, "set": 9, "sept": 9, "settembre": 9, "september": 9, "oct": 10,
       "ott": 10, "ottobre": 10, "october": 10, "nov": 11, "novembre": 11, "november": 11, "dec": 12, "dic": 12, "dicembre": 12, "december": 12}


def bare(n):
    n = re.sub(r"\s*\(.*?\)\s*", " ", str(n or "")).replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", n).strip()


def name_key(n):
    return re.sub(r"\s+detto\s+.+$", "", bare(n), flags=re.I).lower()


def slugify(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s))


def is_name(n):
    t = str(n or "").strip()
    return 2 <= len(t) <= 64 and len(t.split()) <= 7 and not re.search(r"[.;:—]\s|«|»|\bthe\b|\bnot an\b", t, re.I)


def who_slug_of_row(r):
    n = bare(r.get("name"))
    return slugify(n) if is_name(n) and slugify(n) else None


def row_id(r):
    return hashlib.sha1("␟".join([r.get("name") or "", r.get("detail") or "", r.get("link") or "", r.get("source") or ""]).encode("utf-8")).hexdigest()[:10]


def days_in(text):
    s = str(text or "").lower()
    out = set()
    for m in re.finditer(r"\b(\d{1,2})\s+([a-z]+)\.?\s+(\d{4})\b", s):
        if m.group(2) in MON:
            out.add((int(m.group(3)), MON[m.group(2)], int(m.group(1))))
    for m in re.finditer(r"\b([a-z]{3,9})\s+(\d{1,2}),?\s+(\d{4})\b", s):
        if m.group(1) in MON:
            out.add((int(m.group(3)), MON[m.group(1)], int(m.group(2))))
    for m in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", s):
        out.add((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    for m in re.finditer(r"\b(\d{2})/(\d{2})/(\d{4})\b", s):
        out.add((int(m.group(3)), int(m.group(2)), int(m.group(1))))
    return out


def has_tok(text, tok):
    return re.search(r"(?<![A-Za-z0-9_-])" + re.escape(tok) + r"(?![A-Za-z0-9_])", text) is not None


def img_of(t):
    t = str(t or "")
    m = re.search(r"\bimg\.?\s*(\d+)\s*([lr])?\b", t, re.I) or re.search(r"\bimage\s+(\d+)\s*([LR])?\b", t)
    return (int(m.group(1)), (m.group(2) or "").lower()) if m else None


def same_page(r, p):
    link = r.get("link") or ""
    evs = [str(e.get("ark") or "") for e in p.get("events") or []]
    m = re.match(r"^https://antenati\.cultura\.gov\.it/ark:/12657/(an_u[ad]\d+)$", link)
    if m:
        i = m.group(1)
        if i.startswith("an_ud"):
            return any(has_tok(a, i) for a in evs)
        ri = img_of(r.get("source"))
        if not ri:
            return False
        for a in evs:
            if has_tok(a, i):
                ei = img_of(a)
                if ei and ei[0] == ri[0] and (not ei[1] or not ri[1] or ei[1] == ri[1]):
                    return True
        return False
    m = re.match(r"^https://www\.familysearch\.org/ark:/61903/(?:1:1|3:1):([0-9A-Z]{4}-[0-9A-Z]{3,4}(?:-[0-9A-Z0-9]{1,4}){0,2})$", link)
    return bool(m) and any(has_tok(a, m.group(1)) for a in evs)


def same_parents(r, p):
    par = [bare(e.get("name")).lower() for e in p.get("parents") or [] if not e.get("superseded")]
    if len(par) < 2:
        return False
    d = str(r.get("detail") or "").lower()
    if not all(x and x in d for x in par[:2]):
        return False
    mine = set()
    for e in p.get("events") or []:
        mine |= days_in(e.get("date"))
    return bool(days_in(r.get("detail")) & mine)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", str(s or ""))).strip().lower()


def year_of(s):
    ys = [int(x) for x in re.findall(r"\b(1[5-9]\d\d|20\d\d)\b", str(s or ""))]
    return max(ys) if ys else 0


def derive(people, register):
    """slug of person -> {'who': slug, 'rows': {id: (row, why)}, 'total': n, 'own': n}, the rule of dossier.js, written again."""
    rows_of, bearers = {}, {}
    for r in register:
        s = who_slug_of_row(r)
        if s:
            rows_of.setdefault(s, []).append(r)
    for p in people:
        s = slugify(name_key(p["name"]))
        if s and s in rows_of:
            bearers.setdefault(s, []).append(p)
    out = {}
    for s, bs in bearers.items():
        rows = rows_of[s]
        own = sum(1 for r in rows if r.get("kind") in KIND_OWN)
        for p in bs:
            rec = {"who": s, "rows": {}, "total": len(rows), "own": own, "living": bool(p.get("living"))}
            out[p["slug"]] = rec
            if p.get("living"):
                continue
            evid = [plain(e.get("evidence")) for e in p.get("events") or []]
            for r in rows:
                if r.get("kind") in KIND_OWN:
                    continue
                why = "page" if same_page(r, p) else "parents" if same_parents(r, p) else None
                if not why:
                    continue
                if any(q["slug"] != p["slug"] and (same_page(r, q) or same_parents(r, q)) for q in bs):
                    continue
                if year_of(r.get("detail")) >= 1946:
                    continue
                t = plain(r.get("detail"))
                if t and any(t in e for e in evid):
                    continue
                out[p["slug"]]["rows"][row_id(r)] = (r, why)
    return out


# ---- the built pages
def read_pages(dist):
    pages = {}
    for root, _dirs, files in os.walk(dist):
        if "index.html" in files:
            rel = os.path.relpath(root, dist).replace(os.sep, "/")
            route = "/" if rel == "." else "/" + rel + "/"
            if route.startswith("/people/") or route.startswith("/who/"):
                with open(os.path.join(root, "index.html"), encoding="utf-8", errors="replace") as f:
                    pages[route] = f.read()
    return pages


def text_of(x):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()


def md_plain(s):
    """The words a row's markdown prints: the same text without the marks (bold, italic, code, [label](url) -> label)."""
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r"\1", str(s or ""))
    s = re.sub(r"[*`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def section_of(raw):
    """The folded rows on a page: id -> (the three cells' text, link, why text), and whether the section is there."""
    m = re.search(r'<section[^>]*id="more-from-this-name-s-register-page"[^>]*>(.*?)</section>', raw, re.S)
    if not m:
        return None, {}, 0
    sec = m.group(1)
    rows, n = {}, 0
    for li in re.finditer(r'<li[^>]*data-who-row="([0-9a-f]{10})"[^>]*>(.*?)</li>', sec, re.S):
        n += 1
        body = li.group(2)
        divs = re.findall(r"<div[^>]*>(.*?)</div>", body, re.S)
        link = re.search(r'<a href="([^"]+)"[^>]*>[^<]*</a>', divs[2]) if len(divs) > 2 else None
        rows.setdefault(li.group(1), []).append({"as": text_of(divs[0]) if divs else "", "detail": text_of(divs[1]) if len(divs) > 1 else "",
                                                 "src": text_of(divs[2]) if len(divs) > 2 else "", "link": html.unescape(link.group(1)) if link else "",
                                                 "why": text_of(divs[3]) if len(divs) > 3 else ""})
    return sec, rows, n


WHY_WORD = {"page": "a line of the register page this person's own record above already cites", "parents": "it names the same two parents this page draws"}


def check(pages, people, register):
    findings = []
    reg_by_id = {}
    for r in register:
        reg_by_id.setdefault(row_id(r), r)
    want = derive(people, register)
    by_slug = {p["slug"]: p for p in people}
    seen = {}
    folded_pages = 0
    folded_rows = 0
    who_pages = {r for r in pages if r.startswith("/who/") and r != "/who/"}
    for slug, p in sorted(by_slug.items()):
        route = "/people/%s/" % slug
        raw = pages.get(route)
        if raw is None:
            continue
        label = "a living person's page" if p.get("living") else route
        sec, got, n = section_of(raw)
        w = want.get(slug)
        if p.get("living"):
            if sec is not None or "data-who-row" in raw:
                findings.append("living: %s has the register-page section or a folded row" % label)
            continue
        wrows = w["rows"] if w else {}
        if sec is not None:
            folded_pages += bool(got)
        for rid, rec in got.items():
            folded_rows += len(rec)
            if len(rec) > 1:
                findings.append("twice: %s carries row %s %d times" % (label, rid, len(rec)))
            seen.setdefault(rid, []).append(route)
            r = reg_by_id.get(rid)
            if r is None:
                findings.append("extra: %s carries row %s, which is not a register row" % (label, rid))
                continue
            if rid not in wrows:
                findings.append("extra: %s carries a row of the name «%s» (%s) that the data does not tie to this person" % (label, r.get("name"), rid))
                continue
            c = rec[0]
            want_text = md_plain(r.get("detail"))
            if c["detail"] != want_text:
                findings.append("verbatim: %s row %s words differ from the register row" % (label, rid))
            if (c["link"] or "") != (r.get("link") or ""):
                findings.append("verbatim: %s row %s link differs from the register row's" % (label, rid))
            if (r.get("source") or "") not in c["src"]:
                findings.append("verbatim: %s row %s source text differs from the register row's" % (label, rid))
            if c["as"] != "As written: " + str(r.get("name")):
                findings.append("verbatim: %s row %s name as written differs" % (label, rid))
            if WHY_WORD[wrows[rid][1]] not in c["why"]:
                findings.append("why: %s row %s says a reason the data does not give (the data: %s)" % (label, rid, wrows[rid][1]))
            if "/who/%s/" % w["who"] not in who_pages:
                findings.append("who: %s row %s: the name's /who/ page is not built" % (label, rid))
        for rid in wrows:
            if rid not in got:
                findings.append("missing: %s lacks the row %s of «%s» that the data ties to it" % (label, rid, wrows[rid][0].get("name")))
        if sec is not None and w and w["rows"] == {} and not re.search(r"<strong[^>]*>\d+</strong> other record", sec):
            findings.append("absent: %s has the section and nothing in it" % label)
        if sec is not None:
            m = re.search(r"gathers every record in this archive that carries it:\s*<strong[^>]*>(\d+)</strong>", sec)
            if not m or not w or int(m.group(1)) != w["total"]:
                findings.append("who: %s says the name's page holds %s records and it holds %s" % (label, m.group(1) if m else "?", w["total"] if w else "?"))
            else:
                mo = re.search(r"<strong[^>]*>(\d+)</strong> other record", sec)
                want_other = w["total"] - w["own"] - len(wrows)
                if (int(mo.group(1)) if mo else 0) != max(want_other, 0):
                    findings.append("who: %s counts %s other records and the data gives %d" % (label, mo.group(1) if mo else 0, want_other))
    for rid, where in seen.items():
        if len(set(where)) > 1:
            findings.append("twice: row %s is on %d person pages" % (rid, len(set(where))))
    counts = {"people with folded rows": folded_pages, "rows folded": folded_rows,
              "people the data ties rows to": sum(1 for v in want.values() if v["rows"]), "rows the data ties": sum(len(v["rows"]) for v in want.values())}
    return findings, counts, want


def selftest(pages, people, register):
    f0, _c, want = check(pages, people, register)
    ok = True
    print("  control: the untouched build -> %d finding(s)%s" % (len(f0), "" if not f0 else "  <-- SHOULD BE 0"))
    if f0:
        ok = False
    tied = sorted(s for s, v in want.items() if v["rows"] and not v["living"])
    lives = sorted(p["slug"] for p in people if p.get("living") and "/people/%s/" % p["slug"] in pages)
    if len(tied) < 2 or not lives:
        print("  too few folded rows or no living person to plant against: refusing")
        return False
    a, b = tied[0], tied[1]
    ra, rb = "/people/%s/" % a, "/people/%s/" % b
    ida = sorted(want[a]["rows"])[0]
    idb = sorted(want[b]["rows"])[0]

    def li_of(raw, rid):
        return re.search(r'<li[^>]*data-who-row="%s"[^>]*>.*?</li>' % rid, raw, re.S)

    def planted(name, mutate, want_prefix, people_=None, register_=None):
        nonlocal ok
        v = dict(pages)
        mutate(v)
        got, _c, _w = check(v, people_ or people, register_ or register)
        hit = any(g.startswith(want_prefix) for g in got)
        print("  %-56s %s" % (name, "caught" if hit else "MISSED  <-- the gate cannot see this"))
        ok = ok and hit

    planted("a folded row dropped from its page", lambda v: v.__setitem__(ra, v[ra].replace(li_of(v[ra], ida).group(0), "", 1)), "missing")
    planted("a row moved to another person's page", lambda v: (v.__setitem__(rb, v[rb].replace('<ul class="dos-list"', "<ul class=\"dos-list\"", 1).replace(li_of(v[rb], idb).group(0), li_of(v[ra], ida).group(0), 1))), "extra")
    planted("one row on two person pages", lambda v: v.__setitem__(rb, v[rb].replace(li_of(v[rb], idb).group(0), li_of(v[rb], idb).group(0) + li_of(v[ra], ida).group(0), 1)), "twice")
    planted("a row's words changed", lambda v: v.__setitem__(ra, re.sub(r'(data-who-row="%s".*?<div[^>]*>.*?</div>\s*<div[^>]*>)' % ida, r"\1A word that is not the register's. ", v[ra], count=1, flags=re.S)), "verbatim")
    planted("a row's link changed", lambda v: v.__setitem__(ra, re.sub(r'(data-who-row="%s".*?<a href=")[^"]+' % ida, r"\1https://example.org/other", v[ra], count=1, flags=re.S)), "verbatim")
    other = "parents" if want[a]["rows"][ida][1] == "page" else "page"
    planted("the wrong reason printed under a row",
            lambda v: v.__setitem__(ra, re.sub(r'(data-who-row="%s".*?<div[^>]*dos-why[^>]*>).*?(</div>)' % ida, lambda m: m.group(1) + "Why it is here: " + WHY_WORD[other] + m.group(2), v[ra], count=1, flags=re.S)), "why")
    planted("the section on a living person's page",
            lambda v: v.__setitem__("/people/%s/" % lives[0], v["/people/%s/" % lives[0]].replace("</main>", '<section id="more-from-this-name-s-register-page"><ul><li data-who-row="%s"><div>As written: x</div></li></ul></section></main>' % ida, 1)), "living")
    planted("a row the data does not tie, added to a page",
            lambda v: v.__setitem__(ra, v[ra].replace(li_of(v[ra], ida).group(0), li_of(v[ra], ida).group(0).replace(ida, idb), 1)), "extra")
    # a row the data would not tie any more: take the person's parents away from the data, the page still carries the row
    pw = [s for s in tied if any(w == "parents" for _r, w in want[s]["rows"].values())]
    if pw:
        s = pw[0]
        people2 = [dict(p, parents=[]) if p["slug"] == s else p for p in people]
        planted("a tie the data no longer gives (parents gone)", lambda v: None, "extra", people_=people2)
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--people", default="src/data/people.json")
    ap.add_argument("--register", default="src/data/register.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    for pth in (a.dist, a.people, a.register):
        if not os.path.exists(pth):
            print("checkdossiers: %s is not there; nothing was checked" % pth)
            return 2
    with open(a.people, encoding="utf-8") as fh:
        people = json.load(fh)
    with open(a.register, encoding="utf-8") as fh:
        register = json.load(fh)
    pages = read_pages(a.dist)
    if not any(r.startswith("/people/") and r != "/people/" for r in pages) or not any(r.startswith("/who/") and r != "/who/" for r in pages):
        print("checkdossiers: no person page or no /who/ page in %s; nothing was checked" % a.dist)
        return 2
    if a.selftest:
        return 0 if selftest(pages, people, register) else 1
    findings, counts, _w = check(pages, people, register)
    for f in findings:
        print("  FAIL  " + f)
    print("checkdossiers: " + ", ".join("%d %s" % (v, k) for k, v in counts.items()) + "; %d finding%s" % (len(findings), "" if len(findings) == 1 else "s"))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
