#!/usr/bin/env python3
"""Turn bolded person names in the prose into links to that person.

David asked on 10 September 2026 why a name on a family page does not take you
to the person. It should. But retyping thirty pages by hand would be both slow
and unreviewable, so this does it as a pass that can be re-run and re-checked.

It rewrites `<strong>Vincenzo Falco</strong>` into `<P n="Vincenzo Falco"
bold={true} />` — and ONLY when the name resolves to somewhere real. The
resolution itself lives in site/src/lib/links.js; this file only decides which
strings are worth offering to it, using the same three sources.

What it deliberately will not touch:
  – anything in the frontmatter or in the <Base> props, where a `<strong>` is
    inside a JavaScript string and rewriting it would break the build;
  – bolded text that is not a name (streets, trades, dates, whole sentences);
  – names the archive cannot back with a page or a record.
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "site", "src", "data")

def load(f):
    return json.load(open(os.path.join(D, f)))

def norm(s):
    """Must agree exactly with norm() in site/src/lib/links.js."""
    s = re.sub(r"\s*\(.*?\)\s*", " ", str(s or ""))
    s = re.sub(r"[’‘]", "'", s)        # d’Addio and d'Addio are one name
    s = re.sub(r"[«»\"]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()

# the same universe links.js resolves against
known = set()
for h in load("households.json"):
    for m in h["members"]:
        known.add(norm(m["person"]))
for g in load("line.json"):
    raw = str(g.get("name") or "")
    known.add(norm(raw))
    alt = re.search(r"\(([^)]+)\)", raw)
    if alt:
        known.add(norm(re.sub(r"\s*\([^)]*\)\s*", " ", raw)))
        known.add(norm(re.sub(r"\S+\s*\([^)]*\)", alt.group(1), raw)))
for r in load("living.json"):
    known.add(norm(r["name"]))

register_names = [norm(r.get("name")) for r in load("register.json")]

HONORIFIC = re.compile(r"^(?:donn'|donna|don|suor|fra|il dottor|dottor)\s*", re.I)

def in_register(n):
    """The prose keeps the register's own courtesy title; the register's name
    field usually drops it. Try the name both ways."""
    if len(n) < 5:
        return False
    forms = [n]
    b = HONORIFIC.sub("", n).strip()
    if b and b != n:
        forms.append(b)
    return any(any(f in r for f in forms) for r in register_names)

# A name: two to four capitalised words, allowing the Italian particles and the
# honorifics the registers use. Not a street ("strada Camellara" is lower-case
# first), not a trade, not a date.
NAME = re.compile(
    r"^(?:Don |Donna |Donn'|Suor |Fra )?"
    r"[A-Z][a-zà-ù']+(?:\s+(?:di|de|del|della|dell'|lo|la|d')?\s*[A-Z][a-zà-ù']+){1,3}$"
)
STOP = {"the", "and", "of", "strada", "arienzo", "brisbane", "camellara"}

def looks_like_name(t):
    if not NAME.match(t):
        return False
    if any(w.lower() in STOP for w in t.split()):
        return False
    if re.search(r"\d", t):
        return False
    return True

def body_start(s):
    """Everything before the <Base …> tag closes is props and frontmatter."""
    m = re.search(r"<Base\b[\s\S]*?>", s)
    return m.end() if m else 0

def process(path, apply=True):
    s = open(path).read()
    start = body_start(s)
    head, body = s[:start], s[start:]
    hits, misses = [], []

    def repl(m):
        t = m.group(1)
        if not looks_like_name(t):
            return m.group(0)
        n = norm(t)
        if n in known or in_register(n):
            hits.append(t)
            # the source wraps prose, so a name can arrive split over two
            # lines; the attribute wants it on one.
            flat = re.sub(r"\s+", " ", t).strip().replace('"', "&quot;")
            return '<P n="%s" bold={true} />' % flat
        misses.append(t)
        return m.group(0)

    body = re.sub(r"<strong>([^<>{}]+?)</strong>", repl, body)

    if hits and apply:
        if 'components/P.astro' not in head:
            head = re.sub(r'(import Base from "[^"]+";\n)',
                          r'\1import P from "../components/P.astro";\n', head, count=1)
        open(path, "w").write(head + body)
    return hits, misses

if __name__ == "__main__":
    pages = sys.argv[1:]
    total = 0
    for p in pages:
        hits, misses = process(p)
        total += len(hits)
        print(f"{os.path.basename(p):22} {len(hits):3} linked   {len(misses):3} left plain")
        if misses:
            print("      not linked:", ", ".join(sorted(set(misses))[:8]))
    print(f"\n{total} person mentions linked")
