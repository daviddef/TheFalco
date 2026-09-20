#!/usr/bin/env python3
"""One index for the whole site, so /search can answer across everything.

Until now every list on this site searched only itself: the people page, the
register and each family page all had their own box, and none of them could
find a page. This builds a single index of

    every page of the site   (title, eyebrow, dek)
    every person             (547)
    every name               (4,820)
    every source             (17)
    every plate              (63)

It is deliberately NOT an index of all 10,432 records — that is what the
register and the name pages are for, and shipping them twice would put four
megabytes into a search box for no gain.
"""
import json, os, re, collections
import sys

# --- the shared row contract -------------------------------------------------
# All seven archives now emit {k,t,s,h,q}: kind, title, subtitle, href, and a
# lowercased accent-folded haystack. The box that reads it is one component in
# @daviddef/archive-kit, so the schema has to be the same everywhere.
# One fold, shared with the search box and the other six archives.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "site", "node_modules", "@daviddef", "archive-kit", "kit", "tools"))
import searchkit  # noqa: E402

_fold = searchkit.fold

def to_contract(rows):
    out = []
    for r in rows:
        k = r.get("k", "Page")
        t = r.get("t", "")
        s = r.get("s", r.get("d", ""))
        h = r.get("h", r.get("u", ""))
        q = r.get("q", r.get("x", ""))
        out.append(searchkit.row(k, t, s, h, q))
    return out

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def path(*p): return os.path.join(ROOT, *p)
def load(f): return json.load(open(path("site/src/data", f)))

out = []

# --- pages: read the title/eyebrow/dek straight out of each .astro ---
pages_dir = path("site/src/pages")
for fn in sorted(os.listdir(pages_dir)):
    if not fn.endswith(".astro"):
        continue
    # 404.astro is emitted as 404.html, not 404/index.html, so a search hit on
    # it would point at a page the archive check cannot find. It is also not a
    # destination anyone searches for. The stale index hid this for weeks.
    if fn == "404.astro":
        continue
    src = open(os.path.join(pages_dir, fn), encoding="utf-8").read()
    def grab(k):
        m = re.search(rf'{k}="([^"]{{3,400}})"', src) or re.search(rf'{k}=\{{`([^`]{{3,400}})`\}}', src)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    title = grab("title") or fn[:-6]
    slug = "/" if fn == "index.astro" else "/" + fn[:-6]
    out.append({"t": title, "u": slug, "k": "page",
                "d": (grab("eyebrow") + " — " + grab("dek")).strip(" —")[:300]})

# --- people ---
for p in load("people.json"):
    bits = [p.get("surname", "")]
    if p.get("gen"): bits.append(f"generation {p['gen']} of the direct line")
    if p.get("household"): bits.append(p["household"])
    if p.get("living"): bits.append("living")
    for f in ("b", "d", "bp", "dp"):
        if p.get(f): bits.append(str(p[f]))
    out.append({"t": p["name"], "u": "/people/" + p["slug"], "k": "person",
                "d": " · ".join(x for x in bits if x)[:300]})

# --- names, with how many records stand behind each ---
def bare(n):
    n = re.sub(r"\s*\(.*?\)\s*", " ", str(n or "")); n = re.sub(r"[’‘]", "'", n)
    return re.sub(r"\s+", " ", n).strip()
def slugify(s):
    import unicodedata
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s))
def is_name(t):
    t = t.strip()
    return 2 <= len(t) <= 64 and len(t.split()) <= 7 \
        and not re.search(r"[.;:—]\s|«|»|\bthe\b|\bnot an\b", t, re.I)

agg = collections.defaultdict(lambda: {"n": 0, "sur": "", "src": set()})
for r in load("register.json"):
    n = bare(r.get("name"))
    if not is_name(n): continue
    a = agg[n]; a["n"] += 1
    if r.get("surname") and r["surname"] not in ("?", "—"): a["sur"] = r["surname"]
    if r.get("source"): a["src"].add(r["source"])
for n, a in agg.items():
    out.append({"t": n, "u": "/names/" + slugify(n), "k": "name",
                "d": f"{a['n']} record{'s' if a['n'] != 1 else ''} · {a['sur']} · "
                     + " · ".join(sorted(a["src"])[:2])})

# --- sources and plates ---
for s in load("sources.json"):
    out.append({"t": s.get("t", ""), "u": "/sources", "k": "source",
                "d": (s.get("d", "") + " " + s.get("use", ""))[:300]})
for p in load("plates.json"):
    out.append({"t": p.get("t", ""), "u": "/documents#" + p["f"].replace(".jpg", ""),
                "k": "plate", "d": (str(p.get("when", "")) + " " + p.get("cite", ""))[:300]})

out = to_contract(out)

# --- spelling variants, for SEARCH only --------------------------------------
# `namefold.json` is built by kit/tools/namefold.py and lists variant -> canonical
# for surnames this archive spells more than one way. It is applied HERE, to the
# folded haystack, and nowhere else: a row keeps its own spelling, no record is
# merged with another, and no claim of kinship is made. All it does is let a
# reader who types the spelling their document uses reach the rows filed under
# the spelling this archive uses.
#
# SANZONE -> SANSONE is the case it was wired for. On 20 September 2026 a
# declarant published here as SANZONE was shown to be SANSONE: the initial is a
# long s, tested against the z in «Crescenzo» in the same hand. The wrong
# spelling stays visible on the row that carried it, which is the house style,
# and the fold means it is still findable.
_variants = collections.defaultdict(set)
try:
    _nf = load("namefold.json").get("fold", {})
except (FileNotFoundError, KeyError):
    _nf = {}
for _v, _c in _nf.items():
    if _fold(_v) == _fold(_c):
        continue
    _variants[_fold(_c)].add(_fold(_v))
    _variants[_fold(_v)].add(_fold(_c))
_widened = 0
if _variants:
    for _r in out:
        _q = _r.get("q", "")
        _extra = sorted({e for form, es in _variants.items() if form in _q for e in es if e not in _q})
        if _extra:
            _r["q"] = _q + " " + " ".join(_extra)
            _widened += 1
print(f"namefold: {len(_nf)} form(s), {len(_variants)} folded, {_widened} row(s) widened")

for _r in out:
    _r["k"] = _r["k"][:1].upper() + _r["k"][1:]
json.dump(out, open(path("site/src/data/searchindex.json"), "w"), ensure_ascii=False,
          separators=(",", ":"))
size = os.path.getsize(path("site/src/data/searchindex.json"))
print(f"{len(out)} entries · {size // 1024} KB")
print("  by kind:", dict(collections.Counter(e["k"] for e in out)))
