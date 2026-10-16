#!/usr/bin/env python3
"""Falco's side of the estate's living-people standard, version 2 (16 October 2026).

THE RULE (David, 16 October 2026) is not written here. It lives once, in the
kit: kit/tools/living_rule.py (`is_living`, `possible_minor`, `is_held_out`,
`public_source`) and kit/data/public-sources.json. This file only does what is
particular to Falco:

  * it reads the kit's rule from site/node_modules, so there is no second test
    in this archive;
  * it turns a MyHeritage tree row into the arguments that rule takes (a birth
    year, whether a death or burial is recorded, the citations);
  * it reduces a birth place to what a living person may show: a town and a
    country, never a street, an address-like string or an institution.

WHAT A LIVING PERSON SHOWS: a name, their relationships, and that town and
country. Nothing else.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT_TOOLS = os.path.join(ROOT, "site", "node_modules", "@daviddef", "archive-kit", "kit", "tools")
if KIT_TOOLS not in sys.path:
    sys.path.insert(0, KIT_TOOLS)
try:
    import living_rule as lr          # the one definition
except ImportError as e:              # a kit older than 0a56c86 has no rule to import
    raise SystemExit(f"living_v2: the kit's living_rule.py is not installed ({e}). "
                     "Re-pin the kit to 0a56c86 or later and run npm install.")

THIS_YEAR = lr.this_year()
YEAR = re.compile(r"\b(1[5-9]\d\d|20\d\d)\b")


def year_of(s):
    """The first four-digit year in a tree date string, or None."""
    m = YEAR.search(str(s or ""))
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------- the youngest child

def child_ids(tree):
    """tree person id -> the set of tree ids of their children, from the tree's own labels.

    A parent names a child «His son» / «Her daughter» / «Your son» / «Son»; a child names a parent «His father»
    / «Her mother» / «His parent». Either side is enough, so a child recorded on one side only still counts."""
    ids = {p["id"] for p in tree if p.get("id") is not None}
    kids = {}
    for p in tree:
        pid = p.get("id")
        for e in p.get("relatives") or []:
            r = str(e.get("rel") or "").strip().lower().split(" ")[-1]    # «his son» -> son; «his grandson» is not
            q = e.get("id")
            if q not in ids:
                continue
            if r in ("son", "daughter"):
                kids.setdefault(pid, set()).add(q)
            elif r in ("father", "mother", "parent"):
                kids.setdefault(q, set()).add(pid)
    return kids


def youngest_child_years(tree, child_year):
    """tree person id -> the birth year of their youngest child whose birth year is known, for the kit's
    recent-child step (living_rule.is_living(..., youngest_child_year=)). `child_year(tid)` gives a child's year
    or None; a parent with no child of a known year is simply absent."""
    out = {}
    for pid, kids in child_ids(tree).items():
        ys = [y for y in (child_year(k) for k in kids) if y is not None]
        if ys:
            out[pid] = max(ys)
    return out


# ---------------------------------------------------------------- recorded death

def tree_death_recorded(p):
    """A recorded death or burial, dated or not, in a MyHeritage tree row.

    The tree's own `alive` flag being false is the tree saying the person has
    died; a death date; or a Death or Burial fact (even one with no value) all
    count. Absence of all four is not proof of life, only the lack of a record
    of death, which is exactly the test the standard sets."""
    if not p.get("alive"):
        return True
    if str(p.get("d") or "").strip():
        return True
    for f in p.get("facts") or []:
        t = str(f.get("t") or "").lower()
        if t.startswith("death") and not t.startswith("death of"):
            return True
        if t.startswith("burial") or t.startswith("funeral") or t.startswith("cremation"):
            return True
    return False


def event_is_death(ev):
    """A register event that is this person's own death or burial."""
    e = str(ev or "").strip().lower()
    for kind in ("death", "burial", "buried", "died", "funeral"):
        if e.startswith(kind):
            rest = e[len(kind):].lstrip()
            return not rest.startswith("of ")
    return False


# ---------------------------------------------------------------- citations

_FS_ARK = re.compile(r"^(?:ark:/61903/)?(?:3:1:|1:1:)?[0-9A-Z]{3,4}-[0-9A-Z]{3,4}(?:-[0-9A-Z]{3,4})*$")


def citation_strings(events):
    """The citations a register person carries, in the form the kit's rule reads.

    Only the `ark` field, the citation, is used. The `evidence` field is prose
    and may mention a provider in passing; it is never a citation. A FamilySearch
    arks is written as such; an Antenati identifier as Antenati; anything else is
    passed through as written, so a source that is on the kit's list is found by
    its own name and one that is not (a family-papers note, the private tree's
    TSV) is not."""
    out = []
    for e in events or []:
        a = str(e.get("ark") or "").strip()
        if not a:
            continue
        low = a.lower()
        if "an_ua" in low or "an_ud" in low or "antenati" in low:
            out.append("antenati.cultura.gov.it " + a)
        elif re.search(r"\bnaa\b", low) or "recordsearch" in low:
            out.append("recordsearch.naa.gov.au " + a)         # National Archives of Australia
        elif _FS_ARK.match(a) or low.startswith("ark:/61903") or "familysearch" in low:
            out.append("familysearch.org/ark:/61903/3:1:" + a if _FS_ARK.match(a) else a)
        else:
            out.append(a)
    return out


# ---------------------------------------------------------------- place

COUNTRY = {
    "italy": "Italy", "italia": "Italy", "itália": "Italy",
    "australia": "Australia",
    "south africa": "South Africa",
    "united states": "United States", "usa": "United States", "u.s.a.": "United States",
    "united kingdom": "United Kingdom", "uk": "United Kingdom", "england": "England",
    "scotland": "Scotland", "wales": "Wales", "ireland": "Ireland",
    "new zealand": "New Zealand", "canada": "Canada", "france": "France",
    "germany": "Germany", "croatia": "Croatia", "argentina": "Argentina",
    "brazil": "Brazil", "switzerland": "Switzerland", "spain": "Spain",
    "zimbabwe": "Zimbabwe", "poland": "Poland",
}
STATE = {"qld", "nsw", "vic", "tas", "wa", "sa", "nt", "act", "queensland",
         "new south wales", "victoria", "tasmania", "western australia",
         "south australia", "northern territory"}
# an institution is never a town; neither is anything that reads as a street
INSTITUTION = re.compile(
    r"\b(hospital|hospice|clinic|nursing|care|aged|home|homes|centre|center|"
    r"maternity|infirmary|sanatorium|ward|school|college|university|church|"
    r"convent|cathedral|prison|jail|barracks|cemetery|crematorium|private|"
    r"medical|health|lodge|retirement|village|manor)\b", re.I)
ADDRESS = re.compile(
    r"\d|^(via|viale|piazza|strada|contrada|borgo|corso|c/o|po box)\b|"
    r"\b(street|road|avenue|lane|drive|highway|boulevard|terrace|crescent|"
    r"st|rd|ave|ln|dr|blvd)\.?$", re.I)
JUNK = re.compile(r"^(of|about|circa|unknown|certificate number)\b", re.I)


def _country_of(token):
    return COUNTRY.get(token.strip().lower().rstrip("."))


def learn_countries(places):
    """town -> country, learned from this tree's own places, so that a place
    written 'Brisbane' alone is read the way the same tree writes it elsewhere.
    A town that two countries claim is left out rather than guessed."""
    seen = {}
    for raw in places:
        toks = [t.strip() for t in str(raw or "").split(",") if t.strip()]
        if len(toks) < 2:
            continue
        c = _country_of(toks[-1])
        if not c:
            continue
        for t in toks[:-1]:
            k = t.lower()
            if k in seen and seen[k] != c:
                seen[k] = None
            else:
                seen.setdefault(k, c)
    return {k: v for k, v in seen.items() if v}


def town_country(raw, known=None):
    """'Town, Country' from a tree birth place, or '' when there is no town.

    The first level that is a town (not an institution, not address-like, not a
    state) is the town; the last level that names a country is the country. A
    place with a town and no stated country takes the country the same tree gives
    that town elsewhere, and is left as the town alone when it has none."""
    s = re.sub(r"\[[^\]]*\]", " ", str(raw or ""))
    s = re.split(r"\s+[–—]\s+", s)[0]            # a gloss after a dash
    toks = [t.strip() for t in s.split(",") if t.strip()]
    if len(toks) == 1:                                    # 'Brisbane Qld Australia'
        words = toks[0].split()
        c2 = _country_of(" ".join(words[-2:])) if len(words) > 2 else None
        c1 = _country_of(words[-1]) if words else None
        c = c2 or c1
        if c and len(words) > 1:
            head = words[:len(words) - (2 if c2 else 1)]
            while head and head[-1].lower() in STATE:
                head.pop()
            toks = [" ".join(head), c] if head else [c]
        elif c:
            toks = [c]
    country = None
    if toks and _country_of(toks[-1]):
        country = _country_of(toks[-1])
        toks = toks[:-1]
    town = ""
    for t in toks:
        if JUNK.match(t) or t.lower() in STATE or _country_of(t):
            continue
        if ADDRESS.search(t) or INSTITUTION.search(t):
            continue
        town = t
        break
    if not town:
        return ""
    if not country and known:
        country = known.get(town.lower())
    return f"{town}, {country}" if country else town
