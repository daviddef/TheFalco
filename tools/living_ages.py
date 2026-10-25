#!/usr/bin/env python3
"""A living person's AGE, a BIRTH YEAR derived for them, and a PASSENGER-LIST ROW naming them (25 October 2026).

    imported by tools/check_living_v2.py (the build's `check:living2` step);
    `python3 tools/living_ages.py [--dist site/dist]` runs it alone.

WHY IT EXISTS. David's rule: a living person (80 or younger, no death recorded) is named with their relationships and
their town and country, and nothing more: no dates, no ages, no records (passenger lists), no photographs. The build
already refused a YEAR printed beside a living person (check_living_v2 «c», the kit's printed-year gate), but nothing read
AGES. /journeys/ said a living woman «was eight years old» at the 1964 voyage and /australia/ listed her and a brother as
passengers of it; both passed, because (1) an age is not a year, (2) the sentence named her by her first name only, and
(3) a passenger table is a row of dates beside a name, not a «born» year. A living person's birth year was printable
without ever being written: «eight years old in 1964» is 1955.

WHAT IT REFUSES, in every built .html (visible text, JSON-LD and the text attributes), .json, .xml and .txt:

  AGE         an age expression («aged 14», «14 years old», «age of 12», «a 9-year-old», «was eight», «eight months
              old», a number in brackets straight after a name) whose nearest person-name is a living person;
  BORN-YEAR   a birth stated for a living person: «born 1955», «b. 1955», «(1955-)», «born the same year», «born three
              years later»; and, where the private tree is here, any mention of the living person's own birth year in a
              sentence that names them;
  PASSENGER   a sentence or list item that names a living person AND is a passenger record (voyage, embarked, aboard,
              passenger list ... with a year or date); and every row of a table whose header says ship, embarked,
              arrived, port or passenger that names a living person.

HOW A LIVING PERSON IS RECOGNISED. A full name («Given Surname», «Surname, Given», «SURNAME Given»; a nickname or a
married name is allowed for) is a STRONG reference unless a dead person in people.json bears the same name, in which case,
like a bare first name, it is WEAK. A weak reference counts only inside a block that also holds an ANCHOR: the full name of
one of the person's parents, siblings, spouse or children, or their surname together with two relatives' first names. «Giuseppina was eight years old» is caught because the same paragraph names her parents; a register
line about a dead Giuseppina of 1840 is not, because it does not.

WHICH PERSON AN AGE BELONGS TO is the nearest person-name in the sentence (a living reference, a dead person's full name from
people.json, or a capitalised run led by a known given name), within 140 characters. «Francesca Zampiello (Falco) aged 94 ·
Her daughter Giuseppina Falco» is clean; «Her daughter Giuseppina Falco, aged 9» is not.

ESCAPES. site/living-ages-allow.json: entries {contains, why} (a reason of at least 8 characters). A hit whose sentence
contains the text is allowed and counted; an entry that matched nothing is STALE and is a failure. Output names no one: a hit
prints the file, the kind and a few words of context with the living name masked.

WHAT IT CANNOT DO, STATED. A number that is not written as an age cannot be read as one (a bare «1955» is the kit's
printed-year gate and check_living_v2 «c»). Without the private tree it cannot compare a year with a person's true birth
year. A living person referred to by a pronoun alone is not recognised.
"""
import datetime
import html as htmllib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVED = (".html", ".json", ".xml", ".txt", ".webmanifest")
ALLOW = os.path.join(ROOT, "site", "living-ages-allow.json")
NEAR = 140
try:                                                   # the living line is derived, never typed
    sys.path.insert(0, os.path.join(ROOT, "site", "node_modules", "@daviddef", "archive-kit", "kit", "tools"))
    import living_rule as _lr
    CUTOFF = _lr.cutoff_year()
except Exception:                                      # pragma: no cover
    CUTOFF = datetime.date.today().year - 80

# ------------------------------------------------------------------------------------------------ what an age looks like
_ONES = "one|two|three|four|five|six|seven|eight|nine"
_TEENS = "ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen"
_TENS = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
NUM = r"(?:\d{1,3}|(?:%s)(?:[- ](?:%s))?|%s|%s)" % (_TENS, _ONES, _TEENS, _ONES)
UNIT = r"(?:years?|yrs?|months?|weeks?|days?)"
AGE = re.compile(
    r"(?ix)\b(?:"
    r"aged?\s+(?:about\s+|nearly\s+|almost\s+)?" + NUM + r"\b(?!\s*(?:th|st|nd|rd)\b)"
    r"|(?:at\s+the\s+)?age\s+of\s+" + NUM + r"\b"
    r"|" + NUM + r"[-\s]+" + UNIT + r"[-\s]+old\b"
    r"|" + NUM + r"[-\s]+year[-\s]old\b"
    r"|" + NUM + r"\s+" + UNIT + r"\s+of\s+age\b"
    r"|(?:was|is|were|are|turned|turning)\s+(?:only\s+|just\s+|about\s+|nearly\s+)?" + NUM +
    r"(?=\s*(?:[.,;:)—–-]|$|\s+(?:when|at|on|in|and|but)\b))"
    r"|(?:a|the)\s+(?:child|boy|girl|baby|infant|toddler|teenager|youth)\s+of\s+" + NUM + r"\b"
    r")")
PAREN_AGE = re.compile(r"\((\d{1,2})\)")
BORN = re.compile(
    r"(?ix)(?:\bborn\b|\bb\.(?=\s*[\d(c~])|\(b\.)"
    r"[^.;]{0,25}?"
    r"(?:(?<!\d)(19[4-9]\d|20[0-2]\d)(?!\d)|\bthe\s+same\s+year\b|\bthat\s+year\b|\b" + NUM + r"\s+(?:years?|months?)\s+(?:later|earlier|before|after)\b)")
BORN_SAME = re.compile(r"(?i)\bborn\s+(?:the\s+same|that|this)\s+year\b")
SPAN_OPEN = re.compile(r"\((19[4-9]\d|20[0-2]\d)\s*[-–—]\s*\)")
YEAR = re.compile(r"(?<!\d)(1[89]\d\d|20[0-2]\d)(?!\d)")
NEWYEAR = re.compile(r"(?<!\d)(19[4-9]\d|20[0-2]\d)(?!\d)")

PASS_CUE = re.compile(
    r"(?i)\b(passengers?|voyage|embark\w*|disembark\w*|aboard|sailed|steamer|steamship|liner|manifest|quarantine|"
    r"port of (?:arrival|landing|embarkation)|per the ss|per ship|arrived (?:at|in|on|per|by|from)|"
    r"landed (?:at|in|on)|crew list|ship)\b")
DATEISH = re.compile(r"(?<!\d)(?:1[89]\d\d|20[0-2]\d)(?!\d)|\b\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b|"
                     r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b", re.I)
PASS_HEAD = re.compile(r"(?i)\b(ship|vessel|embarked|arrived|arrival|port|passenger|voyage|steamer)\b")
CUE_QUICK = re.compile(r"(?i)\bage\b|\baged\b|years?\b|months?\b|\bweeks?\b|\byrs?\b|\(\d{1,2}\)|\bborn\b|\bb\.|\bbirth|"
                       r"\bwas\b|\bis\b|\bwere\b|\bare\b|\bturn|passenger|voyage|embark|aboard|sailed|steam|liner|manifest|"
                       r"quarantine|port of|per the ss|per ship|arrived|landed|crew|ship|\(\d{4}\s*[-–—]")


# ------------------------------------------------------------------------------------------------ names
def _norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def bare_name(n):
    """A name without brackets, nickname or marks: «Cristina Adele D'Arcy (Defranceski)» -> «Cristina Adele D'Arcy»."""
    n = re.sub(r"[✔⭐★⚠]", "", str(n or ""))
    n = re.sub(r"\s*\(.*?\)\s*", " ", n)
    n = re.sub(r'\s*["“”][^"“”]*["“”]\s*', " ", n)
    return _norm(n).strip(" ,;")


def _alts(n):
    """(given-name strings, surname spellings) a person is written with."""
    raw = str(n or "")
    nick = re.findall(r'["“]([^"”]+)["”]', raw)
    paren = re.findall(r"\(([^)]*)\)", raw)
    base = bare_name(raw).split()
    if len(base) < 2:
        return [], []
    sur = [base[-1]] + [p.strip() for p in paren if len(p.split()) == 1 and p.strip()[:1].isupper()]
    given = [" ".join(base[:-1])]
    if len(base) > 2:
        given.append(base[0])
    given += [x.strip() for x in nick if x.strip()]
    return list(dict.fromkeys(given)), list(dict.fromkeys(sur))


def _forms(given, sur):
    """The three ways «Given Surname» is written, as regular expressions."""
    g, s = re.escape(given), re.escape(sur)
    return [r"%s\s+%s" % (g, s), r"%s,\s*%s" % (s, g), r"%s\s+%s" % (s, g)]


def _literal_forms(given, sur):
    return ["%s %s" % (given, sur), "%s, %s" % (sur, given), "%s %s" % (sur, given)]


def _key(text):
    return re.sub(r"\s*,\s*", ", ", re.sub(r"\s+", " ", text.lower())).strip()


def _rx(pats):
    if not pats:
        return None
    return re.compile(r"(?<![\w'’])(?:%s)(?![\w'’])" % "|".join(sorted(pats, key=len, reverse=True)), re.I)


class Living:
    """Everyone who is living in people.json, and how each is written."""

    def __init__(self, people, tree_years=None):
        self.living = [p for p in people if p.get("living")]
        dead = [p for p in people if not p.get("living")]
        by_slug = {p["slug"]: p for p in people}
        dead_names = {_key(bare_name(p["name"])) for p in dead}
        self.tree_years = tree_years or {}
        self.entries = []
        strong, weak, bare = {}, {}, {}
        tokens = set()
        for p in self.living:
            given, sur = _alts(p["name"])
            if not given:
                continue
            kin_full, kin_given = [], set()
            for k in ("parents", "spouses", "children", "siblings"):
                for e in p.get(k) or []:
                    kg, ks = _alts(e.get("name") or (by_slug.get(e["slug"]) or {}).get("name"))
                    for g in kg:
                        kin_given.add(g.split()[0].lower())
                        for s in ks:
                            kin_full += _forms(g, s)
            ent = {"slug": p["slug"], "treeId": p.get("treeId"), "surnames": sur, "sur_rx": re.compile(r"\b(?:%s)s?\b" % "|".join(map(re.escape, sur)), re.I),
                   "ambiguous": _key(bare_name(p["name"])) in dead_names, "kin_given": kin_given,
                   "kin_full": re.compile(r"(?<![\w'’])(?:%s)(?![\w'’])" % "|".join(kin_full), re.I) if kin_full else None}
            self.entries.append(ent)
            for g in given:
                for i, sn in enumerate(sur):
                    for lit, rxs in zip(_literal_forms(g, sn), _forms(g, sn)):
                        weak_form = ent["ambiguous"] or i > 0 or _key("%s %s" % (g, sn)) in dead_names
                        (weak if weak_form else strong).setdefault(_key(lit), (rxs, []))[1].append(ent)
            first = given[0].split()[0]
            if len(first) >= 4:
                bare.setdefault(first.lower(), []).append(ent)
            tokens.add(first.lower())
            tokens.update(s.lower() for s in sur)
        self._strong = {k: v[1] for k, v in strong.items()}
        self._weak = {k: v[1] for k, v in weak.items()}
        self.strong_rx = _rx([v[0] for v in strong.values()])
        self.weak_rx = _rx([v[0] for v in weak.values()])
        self.bare = bare
        self.bare_rx = re.compile(r"(?<![\w'’])(?:%s)(?![\w'’])" % "|".join(
            "%s%s|%s" % (re.escape(k[0].upper()), re.escape(k[1:]), re.escape(k.upper())) for k in sorted(bare, key=len, reverse=True))) if bare else None
        self.tokens = tokens
        self.givens = {g.split()[0].lower() for p in people for g in _alts(p["name"])[0]}
        dn = set()
        for p in dead:
            g, s = _alts(p["name"])
            for gg in g:
                for ss in s:
                    dn.update(_forms(gg, ss))
        self.dead_rx = _rx(dn)
        givens = {g.split()[0] for p in people for g in _alts(p["name"])[0]}
        self.givenled_rx = re.compile(r"(?<![\w'’])(?:%s)(?:\s+(?:de|di|del|della|dei|degli|d'|van|von|la|le)?\s*[A-ZÀ-Ý][\w'’À-ÿ-]+){1,2}"
                                      % "|".join(sorted(map(re.escape, givens), key=len, reverse=True))) if givens else None

    def may_hold(self, block):
        return any(w in self.tokens for w in re.findall(r"[\w'’]+", block.lower()))

    def _part_of_longer_name(self, text, s, e, bare):
        """True when the match is only a piece of someone else's name: a known given name just before it
        («Carmine Antonio Falco» holds «Antonio Falco»), or, for a first name alone, a capitalised word after it that is
        not the person's own surname («Giuseppina Annecchino», «Maria Rosa Falco»)."""
        prev = re.search(r"([A-ZÀ-Ý][\w'’À-ÿ-]*)\s+$", text[max(0, s - 40):s])
        if prev and prev.group(1).lower() in self.givens and not re.match(r"[\w'’À-ÿ-]+,", text[s:e]):
            return True
        if bare:
            nxt = re.match(r"\s+([A-ZÀ-Ý][\w'’À-ÿ-]+)", text[e:e + 40])
            if nxt:
                return True if nxt.group(1).lower() not in self.surnames_of(bare) else False
        return False

    def surnames_of(self, ents):
        return {x.lower() for e in ents for x in e["surnames"]}

    def refs(self, text, ctx=None):
        """[(start, end, [entries])] for each living reference in `text`: strong ones, and weak ones only when anchored
        within 120 characters (see the module docstring)."""
        out = []
        if self.strong_rx:
            for m in self.strong_rx.finditer(text):
                ents = self._strong.get(_key(m.group(0))) or []
                if not ents:
                    continue
                if not self._part_of_longer_name(text, m.start(), m.end(), None):
                    out.append((m.start(), m.end(), ents))
        weak = []
        if self.weak_rx:
            for m in self.weak_rx.finditer(text):
                ents = self._weak.get(_key(m.group(0))) or []
                if ents and not self._part_of_longer_name(text, m.start(), m.end(), None):
                    weak.append((m.start(), m.end(), ents))
        if self.bare_rx:
            for m in self.bare_rx.finditer(text):
                ents = self.bare[m.group(0).lower()]
                if not self._part_of_longer_name(text, m.start(), m.end(), ents):
                    weak.append((m.start(), m.end(), ents))
        for s, e, ents in weak:
            if any(a <= s < b for a, b, _ in out):
                continue
            if ctx and len(ctx) <= 700:                     # the whole short block: «Giuseppina — eight years old — and Antonio»
                win = ctx                                   # is anchored by «the Anthony Falco of the family record» after it
            else:
                lo, hi = max(0, s - 120), min(len(text), e + 120)
                win = text[lo:hi]
            low = win.lower()
            ok = [x for x in ents if self._anchored(x, low, win)]
            if ok:
                out.append((s, e, ok))
        out.sort(key=lambda t: t[0])
        return out

    @staticmethod
    def _anchored(ent, low, text):
        if ent["kin_full"] is not None and ent["kin_full"].search(text):
            return True
        kg = [g for g in ent["kin_given"] if re.search(r"(?<![\w'’])%s(?![\w'’])" % re.escape(g), low)]
        return len(kg) >= 2 and bool(ent["sur_rx"].search(text))

    def others(self, text):
        spans = []
        for rx in (self.dead_rx, self.givenled_rx):
            if rx is not None:
                spans += [(m.start(), m.end()) for m in rx.finditer(text)]
        return spans


# ------------------------------------------------------------------------------------------------ reading a built file
_BLOCK_TAGS = re.compile(r"(?is)</?(?:p|li|tr|div|h[1-6]|figcaption|blockquote|section|article|br|dd|dt|summary|details|tbody|thead|"
                         r"tfoot|table|ul|ol|figure|main|header|footer|nav|aside|form|pre|caption|dl)\b[^>]*>")
_CELL = re.compile(r"(?is)</t[dh]\s*>")
_TAG = re.compile(r"(?s)<[^>]*>")
_SKIP_ATTR = {"href", "src", "srcset", "class", "style", "id", "d", "points", "viewbox", "xmlns", "rel", "type", "name", "target",
              "width", "height", "fill", "stroke", "transform", "role", "lang", "charset", "loading", "decoding", "media",
              "sizes", "crossorigin", "integrity", "as", "for", "tabindex", "method", "action", "data-astro-cid",
              "component-url", "renderer-url", "opts", "client", "ssr", "uid", "before-hydration-url"}
_ATTR = re.compile(r'(?s)\s([a-zA-Z_:][-\w:.]*)\s*=\s*"([^"]{12,})"')
_JSONLD = re.compile(r'(?is)<script[^>]*application/ld\+json[^>]*>(.*?)</script>')
_SCRIPT = re.compile(r"(?is)<script\b.*?</script>|<style\b.*?</style>")


def _leaves(obj, out):
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _leaves(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _leaves(v, out)


def _clean(s):
    return _norm(htmllib.unescape(_TAG.sub(" ", s)))


def blocks_of(path, raw):
    """The text blocks of one served file: visible text by block, text attributes, JSON-LD, JSON string values."""
    out = []
    if path.endswith(".html"):
        for m in _JSONLD.finditer(raw):
            try:
                lv = []
                _leaves(json.loads(m.group(1)), lv)
                out += [_norm(x) for x in lv]
            except ValueError:
                pass
        for m in _ATTR.finditer(raw):
            if m.group(1).lower() in _SKIP_ATTR:
                continue
            v = htmllib.unescape(m.group(2))
            if v[:1] in "{[":
                try:
                    lv = []
                    _leaves(json.loads(v), lv)
                    out += [_clean(x) for x in lv if len(x) > 11]
                    continue
                except ValueError:
                    pass
            if re.search(r"[A-Za-z]{3,} [A-Za-z]{2,}", v):
                out.append(_norm(v))
        body = _CELL.sub(" | ", _SCRIPT.sub(" ", raw))
        out += [_clean(seg) for seg in _BLOCK_TAGS.split(body)]
    elif path.endswith((".json", ".webmanifest")):
        try:
            lv = []
            _leaves(json.loads(raw), lv)
            out += [_clean(x) for x in lv]
        except ValueError:
            out += [_clean(x) for x in raw.split("\n")]
    else:
        out += [_clean(x) for x in raw.split("\n")]
    return [b for b in out if len(b) > 5]


def passenger_table_rows(raw):
    """The rows of every table whose header names two of ship / embarked / arrived / port / passenger / voyage."""
    rows = []
    for tm in re.finditer(r"(?is)<table\b.*?</table>", raw):
        t = tm.group(0)
        hm = re.search(r"(?is)<thead\b.*?</thead>", t)
        if hm is None and re.search(r"(?i)<th\b", t):
            hm = re.search(r"(?is)<tr\b[^>]*>(?:(?!</tr>).)*?<th\b.*?</tr>", t)
        if hm is None:
            continue
        if len({w.lower() for w in PASS_HEAD.findall(_clean(hm.group(0)))}) < 2:
            continue
        body = t.replace(hm.group(0), " ", 1)
        rows += [_clean(_CELL.sub(" | ", r.group(0))) for r in re.finditer(r"(?is)<tr\b.*?</tr>", body)]
    return rows


# ------------------------------------------------------------------------------------------------ the scan
def _sentences(block):
    return [s for s in re.split(r"(?<=[.!?;])\s+(?=[A-Z«“\"(])", block) if s]


def _mask(text, spans):
    out, last = [], 0
    for s, e in sorted(spans):
        if s < last:
            continue
        out += [text[last:s], "<living>"]
        last = e
    out.append(text[last:])
    return "".join(out)


def scan_sentence(L, sent, ctx=None):
    """Findings in one sentence/block: [(label, masked context)]. `ctx` is the whole block the sentence is in."""
    treeyr = bool(L.tree_years) and bool(NEWYEAR.search(sent))
    if not (treeyr or CUE_QUICK.search(sent)):
        return []
    ages = [m for m in AGE.finditer(sent)]
    born = [m for rx in (BORN, BORN_SAME, SPAN_OPEN) for m in rx.finditer(sent)]
    passg = bool(PASS_CUE.search(sent) and DATEISH.search(sent))
    parens = [m for m in PAREN_AGE.finditer(sent)]
    if not (ages or born or passg or treeyr or parens):
        return []
    if not L.may_hold(sent):
        return []
    refs = L.refs(sent, ctx)
    if not refs:
        return []
    rspans = [(s, e) for s, e, _ in refs]
    others = [(s, e) for s, e in L.others(sent) if not any(s < b and a < e for a, b in rspans)]
    mask = lambda lo, hi: _mask(sent[lo:hi], [(max(s, lo) - lo, min(e, hi) - lo) for s, e in rspans if e > lo and s < hi])

    def living_is_nearest(ps, pe):
        best = None
        for kind, spans in (("o", others), ("l", rspans)):
            for s, e in spans:
                d = 0 if (s < pe and ps < e) else min(abs(s - pe), abs(ps - e))
                key = (d, 0 if e <= ps else 1, 0 if kind == "l" else 1)
                if best is None or key < best[0]:
                    best = (key, kind)
        return best is not None and best[1] == "l" and best[0][0] <= NEAR

    found = []
    for m in ages:
        if living_is_nearest(m.start(), m.end()):
            found.append(("AGE", mask(max(0, m.start() - 70), m.end() + 40)))
    for m in parens:
        if any(0 <= m.start() - e <= 2 for _, e, _ in refs):
            found.append(("AGE", mask(max(0, m.start() - 60), m.end() + 30)))
    for m in born:
        yrs = [int(y) for y in YEAR.findall(m.group(0))]
        if yrs and min(yrs) < CUTOFF:
            continue
        if living_is_nearest(m.start(), m.end()):
            found.append(("BORN-YEAR", mask(max(0, m.start() - 60), m.end() + 30)))
    if passg:
        found.append(("PASSENGER RECORD", mask(0, 170)))
    if treeyr:
        # the person's own birth year (read from the private tree) straight after their name: «Name 1955», «Name (1955)»,
        # «Name, b. 1955». A year further off may belong to an event (a marriage in the same year) and is not read.
        for s, e, ents in refs:
            for ent in ents:
                ty = L.tree_years.get(ent["slug"])
                if not ty:
                    continue
                for m in YEAR.finditer(sent, e):
                    if int(m.group(1)) == ty and re.fullmatch(r"[\s,;:()\[\]·|\u2013\u2014-]*(?:b\.?|born|c\.?)?[\s(]*", sent[e:m.start()]):
                        found.append(("BORN-YEAR (the person's own, read from the tree)", mask(max(0, s - 20), m.end() + 20)))
    return found


def load_allow(path=None):
    path = path or ALLOW
    if not os.path.exists(path):
        return []
    out = []
    for e in json.load(open(path, encoding="utf-8")).get("allow", []):
        c, w = e.get("contains") or e.get("text"), e.get("why") or e.get("reason")
        if not c or not w or len(w) < 8:
            raise ValueError("living-ages-allow.json: every entry needs 'contains' and a 'why' of at least 8 characters")
        out.append({"contains": c.lower(), "why": w, "used": 0})
    return out


def scan_dist(dist, people, tree_years=None, allow=None, only=None):
    """Scan the built site. Returns (fails, stats). `only` (a set of dist-relative paths) limits the scan."""
    L = Living(people, tree_years)
    allow = load_allow() if allow is None else allow
    fails, stats = [], {"files": 0, "blocks": 0, "allowed": 0, "stale": 0}
    if not L.entries:
        return ["LIVING AGES: no living person with a surname to look for, so nothing was checked"], stats
    for root, _, fns in os.walk(dist):
        for fn in fns:
            if not fn.endswith(SERVED):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, dist).replace(os.sep, "/")
            if only is not None and rel not in only:
                continue
            try:
                raw = open(full, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            stats["files"] += 1
            seen = set()
            blocks = blocks_of(full, raw)
            stats["blocks"] += len(blocks)
            for b in blocks:
                for sent in ([b] if len(b) < 280 else _sentences(b)):
                    for label, ctx in scan_sentence(L, sent, b):
                        _record(fails, stats, allow, seen, rel, label, ctx, sent)
            if fn.endswith(".html") and "<table" in raw:
                for row in passenger_table_rows(raw):
                    refs = L.refs(row) if L.may_hold(row) else []
                    if refs:
                        _record(fails, stats, allow, seen, rel, "PASSENGER ROW (a living person in a passenger table)",
                                _mask(row[:170], [(s, e) for s, e, _ in refs]), row)
    for a in allow:
        if not a["used"]:
            stats["stale"] += 1
            fails.append("LIVING AGES: a registry entry in site/living-ages-allow.json matched nothing (stale): «%s»" % a["contains"][:60])
    return fails, stats


def _record(fails, stats, allow, seen, rel, label, ctx, sentence):
    low = sentence.lower()
    for a in allow:
        if a["contains"] in low:
            a["used"] += 1
            stats["allowed"] += 1
            return
    key = (rel, label, ctx)
    if key in seen:
        return
    seen.add(key)
    fails.append("A LIVING PERSON'S %s: /%s «%s»" % (label, rel, ctx[:190]))


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=os.path.join(ROOT, "site", "dist"))
    a = ap.parse_args(argv)
    people = json.load(open(os.path.join(ROOT, "site", "src", "data", "people.json"), encoding="utf-8"))
    fails, stats = scan_dist(a.dist, people)
    print("living_ages: %(files)d files, %(blocks)d blocks read, %(allowed)d allowed by the registry" % stats)
    for f in sorted(set(fails)):
        print("  " + f)
    print("living_ages: %s" % ("FAILED (%d)" % len(set(fails)) if fails else "clean"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
