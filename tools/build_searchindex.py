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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def path(*p): return os.path.join(ROOT, *p)
def load(f): return json.load(open(path("site/src/data", f)))

out = []

# --- pages: read the title/eyebrow/dek straight out of each .astro ---
pages_dir = path("site/src/pages")
for fn in sorted(os.listdir(pages_dir)):
    if not fn.endswith(".astro"):
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

json.dump(out, open(path("site/src/data/searchindex.json"), "w"), ensure_ascii=False,
          separators=(",", ":"))
size = os.path.getsize(path("site/src/data/searchindex.json"))
print(f"{len(out)} entries · {size // 1024} KB")
print("  by kind:", dict(collections.Counter(e["k"] for e in out)))
