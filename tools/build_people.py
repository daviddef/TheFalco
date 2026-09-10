#!/usr/bin/env python3
"""One person, everything the archive knows about them, and who they belong to.

Until now a person page was built from households.json alone. That file is the
register work — it is excellent on Arienzo before 1850 and nearly empty after
it, because the later generations lived at Arpaia and Brisbane and left civil
records this archive holds as citations, not as reconstructed households. So
Angelo Zampiello's page showed one box: him, in his father's house, with no
wife and no children — while the Ferrara page three clicks away named his wife
and five of his children.

The family tree has those edges. It has 427 people and full parent, spouse,
child and sibling links. It is also unverified, which is why the archive never
let it near a person page.

The answer is not to choose. It is to merge the two and SAY WHICH IS WHICH on
every single edge:

    register   the relationship is written in a record this archive has read
    tree       the relationship comes from the family tree and is unverified
    both       both say so

The merge is where this could go wrong, so the rule is narrow and its basis is
published per person:

  – a household person and a tree person are the same person only when the
    normalised name matches AND either their years agree, or the name is unique
    on both sides;
  – "name and dates" and "name alone" are recorded differently, and the page
    says which it used;
  – if two tree people share the name and neither matches on years, NOTHING is
    merged. Three Maria Falco is the reason this archive exists in this form.

Living people carry a name and their place in the family and NOTHING ELSE —
no dates, no places, no events — following the rule David set on 10 September
2026. The test for "living" is the one in build_living.py, not the tree's own
flag, which marks a man born in 1832 as alive.
"""
import json, re, collections, os, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def path(*p): return os.path.join(ROOT, *p)

households = json.load(open(path("site/src/data/households.json")))
line       = json.load(open(path("site/src/data/line.json")))
tree       = json.load(open(path("data/myheritage-falco-tree.json")))

# ---------------------------------------------------------------- helpers

def strip_ticks(n):
    return re.sub(r"[✔⭐★⚠]", "", str(n or "")).strip()

def clean(s):
    """Drop parenthetical married names and collapse space — the shape the old
    people.js used, kept identical so existing /people/<slug> URLs survive."""
    s = re.sub(r"\s*\(.*?\)\s*", " ", strip_ticks(s))
    return re.sub(r"\s+", " ", s).strip()

def kebab(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s))

def norm(s):
    return clean(s).lower()

def years(*bits):
    out = set()
    for b in bits:
        for m in re.finditer(r"\b(1[6-9]\d\d|20\d\d)\b", str(b or "")):
            out.add(int(m.group(1)))
    return out

def surname_of(n):
    parts = clean(n).split()
    if len(parts) < 2: return "—"
    if len(parts) > 2 and parts[-2].lower() in {"di","de","del","della","lo","la","d'"}:
        return (parts[-2] + " " + parts[-1]).upper()
    return parts[-1].upper()

def is_placeholder(n):
    n = strip_ticks(n)
    return (not n) or n.lower().startswith("unknown") or "[" in n

# ------------------------------------------------------- the direct line
#
# A generation is NOT identified by its forename. Matching on the name alone
# labelled four different Matteo Falco "Generation 1" — including the
# *possidente* of strada Porta di Sopra, whom this archive has always said is
# unjoined — and three Vincenzo Falco "Generation 3".
#
# line.json names both the ancestor AND their spouse for all nine generations,
# so a generation is identified by THE COUPLE. That is the identification the
# archive already publishes; nothing new is asserted here.

def forms(n):
    """"Andrea / Andreana Crisci" is one woman written two ways."""
    n = clean(n)
    out = {norm(n)}
    if "/" in n:
        head = n.split("/")[0].strip().split()
        tail = n.split("/")[-1].strip().split()
        # "Pasquale / Pascuale Falco" -> "Pasquale Falco", "Pascuale Falco"
        if tail and len(tail) > 1:
            out.add(norm(" ".join(head[:1] + tail[1:])))
            out.add(norm(" ".join(tail)))
        for piece in n.split("/"):
            out.add(norm(piece))
    return {f for f in out if f}

GEN = []
for g in line:
    GEN.append((g, forms(g["name"]), forms(g.get("spouse"))))

def generation_of(name, spouse_names):
    """The generation whose ancestor AND spouse both match. None otherwise."""
    nm = norm(name)
    sp = {norm(x) for x in spouse_names}
    hits = [g for g, nf, sf in GEN if nm in nf and (sf & sp)]
    return hits[0] if len(hits) == 1 else None

# ---------------------------------------------------- who is really living

by_id = {p["id"]: p for p in tree if p.get("id")}
anchor = next((p for p in tree if p.get("rel") == "This is you"), None)
spouse_of_anchor = None
if anchor:
    for e in anchor.get("relatives") or []:
        if (e.get("rel") or "").lower() in ("your wife", "your husband", "your spouse"):
            spouse_of_anchor = by_id.get(e["id"])

def edges(p, want):
    return [e["id"] for e in (p.get("relatives") or [])
            if (e.get("rel") or "").lower().endswith(want)]

ANCESTORS = set()
if spouse_of_anchor:
    frontier, seen = [spouse_of_anchor["id"]], {spouse_of_anchor["id"]}
    while frontier:
        pid = frontier.pop(0)
        p = by_id.get(pid)
        if not p: continue
        for want in ("mother", "father"):
            for aid in edges(p, want):
                if aid in seen: continue
                seen.add(aid); ANCESTORS.add(aid); frontier.append(aid)

def birth_year(p):
    m = re.search(r"\b(1[6-9]\d\d|20\d\d)\b", str(p.get("b") or ""))
    return int(m.group(1)) if m else None

# line.json marks a generation living in the archive's own words. That
# marking wins over anything the tree says.
LINE_LIVING = {clean(g["name"]).lower() for g in line if g.get("living")}

def really_living(p):
    """The tree's own flag means 'no death date recorded', which is not the
    same thing — left alone it marks a man born in 1832 as alive. Two filters
    correct it: a placeholder is not a person, and a birth before 1920 means
    dead whatever the flag says.

    What must NOT be used here is the ancestor test. build_living.py excludes
    ancestors because it is listing living *relatives* and an ancestor is not
    one. Reusing that predicate to decide REDACTION was a serious mistake: the
    wife's own mother is an ancestor AND alive, so it published the birth date
    of a living woman — the exact leak the direct-line page had already been
    fixed for. Ancestry has nothing to do with whether someone is alive.
    """
    if is_placeholder(p.get("name")):
        return False
    if clean(p.get("name")).lower() in LINE_LIVING:
        return True                      # the archive says so; that settles it
    if not p.get("alive"):
        return False
    by = birth_year(p)
    if by is not None and by < 1920:
        return False
    return True

# households.json does not use one word for a child. It uses «child», but also
# «daughter» and «son», and reading only «child» dropped real children into the
# parents' row — which is how Chiara Rivetti came to have her own father and
# mother listed as her husbands.
#
# «declarant» is the one role that must NEVER become kinship. A declarant is
# the man who walked to the town hall; he is very often a neighbour, and the
# whole point of the 1828 «parente della defunta» find is that the register
# says so explicitly WHEN he is kin. Turning every witness into family would
# throw that away.
PARENT_ROLES = {"father", "mother", "head", "husband", "wife"}
CHILD_ROLES  = {"child", "daughter", "son"}
NOT_KIN      = {"declarant", "—", ""}

# ------------------------------------------------- the household side

hh_people = {}        # key -> record
hh_order = []
for h in households:
    for m in h["members"]:
        key = h["name"] + "|" + m["person"]
        if key not in hh_people:
            hh_people[key] = {
                "name": strip_ticks(m["person"]), "household": h["name"],
                "role": m["role"], "events": [],
            }
            hh_order.append(key)
        p = hh_people[key]
        if m["role"] not in CHILD_ROLES and p["role"] in CHILD_ROLES:
            p["role"] = m["role"]
        if m.get("event") and m["event"] != "—":
            p["events"].append({k: m.get(k) for k in ("event","date","place","evidence","ark")})
        elif m.get("evidence"):
            p["events"].append({"event": "named", **{k: m.get(k) for k in ("date","place","evidence","ark")}})

_pre_join_order = list(hh_order)
_pre_join = {k: (hh_people[k]["name"], hh_people[k]["household"]) for k in hh_order}

# A woman is a daughter in her father's house and a wife in her husband's, and
# households.json keys people by household, so she arrives here as two records.
# Chiara Rivetti was a child in "Nicola Rivetti & Anna di Ruggio" and the head
# of "Pasquale Falco & Chiara Rivetti" — and her husband's page listed her
# twice, as two different wives.
#
# The old design kept them apart on purpose, because this parish has three
# Maria Falco and four Pasquale, and merging on a name is how an archive
# invents people. So the join is only made when the name leaves NO room:
# exactly one child of that name in the whole file, and exactly one head. Where
# a name repeats at all, nothing is joined.
kids_named   = collections.defaultdict(list)
heads_named  = collections.defaultdict(list)
for k in hh_order:
    q = hh_people[k]
    parts = [x.strip() for x in q["household"].split("&")]
    if any(clean(x) == clean(q["name"]) for x in parts):
        heads_named[norm(q["name"])].append(k)
    elif q["role"] in CHILD_ROLES:
        kids_named[norm(q["name"])].append(k)

# Even "exactly one of each name" is not enough, and the proof is in this very
# family. Vincenzo Falco and Andreana Crisci called a son PASQUALE. So did
# half the street. Joining that child record to the one head called Pasquale
# Falco made **generation two his own grandson** — a dead infant promoted into
# the direct line by a name, which is the precise failure the archive was built
# to avoid.
#
# So the name is only a candidate. The test is an invariant: a join is accepted
# only if NOBODY BECOMES THEIR OWN ANCESTOR. Anything that closes a loop in the
# parent graph is refused and counted.
parent_of = collections.defaultdict(set)     # household record -> its parents
for h in households:
    parts = [x.strip() for x in h["name"].split("&")]
    hs, ks = [], []
    for k in hh_order:
        q = hh_people[k]
        if q["household"] != h["name"]: continue
        if (q["role"] or "").lower() in NOT_KIN: continue
        if any(clean(x) == clean(q["name"]) for x in parts) or q["role"] in PARENT_ROLES:
            hs.append(k)
        elif q["role"] in CHILD_ROLES:
            ks.append(k)
    for k in ks:
        parent_of[k] |= set(hs)

def makes_cycle(joins):
    """Is anyone their own ancestor once these joins are applied?"""
    ident = dict(joins)
    who = lambda k: ident.get(k, k)
    up = collections.defaultdict(set)
    for k, ps in parent_of.items():
        up[who(k)] |= {who(x) for x in ps if who(x) != who(k)}
    seen_ok = set()
    def walk(n, stack):
        if n in stack: return True
        if n in seen_ok: return False
        stack.add(n)
        for q in up.get(n, ()):
            if walk(q, stack): return True
        stack.discard(n)
        seen_ok.add(n)
        return False
    return any(walk(n, set()) for n in list(up))

# The cycle test alone is not enough, because which join closes the loop
# depends on which was tried first — and tried alphabetically it accepted the
# WRONG one, joining the infant Pasquale to generation two and then refusing
# the Vincenzo join that is actually documented.
#
# The archive's own line breaks the tie. It is argued act by act on
# /direct-line and it says which of these people are which generation, so:
# A PARENT MUST BE AN EARLIER GENERATION THAN THEIR CHILD. The infant
# Pasquale's household is headed by generation three, and generation two
# cannot be generation three's son.
def gen_of_household(hname):
    parts = [x.strip() for x in hname.split("&")]
    for x in parts:
        g = generation_of(x, [y for y in parts if y != x])
        if g: return g["gen"]
    return None

def household_of_head(k):
    return hh_people[k]["household"]

same_person = {}
refused_join = []
cands = []
for nm, ks in kids_named.items():
    hs = heads_named.get(nm) or []
    if len(ks) == 1 and len(hs) == 1:
        cands.append((nm, ks[0], hs[0]))

for nm, ck, hk in sorted(cands):
    g_head = gen_of_household(household_of_head(hk))
    g_par  = gen_of_household(hh_people[ck]["household"])
    if g_head is not None and g_par is not None and g_par >= g_head:
        refused_join.append(f"{nm} (would make generation {g_head} a child of generation {g_par})")
        continue
    trial = dict(same_person); trial[ck] = hk
    if makes_cycle(trial):
        refused_join.append(f"{nm} (would make someone their own ancestor)")
        continue
    same_person = trial

for child_k, head_k in same_person.items():
    head, kid = hh_people[head_k], hh_people[child_k]
    head["events"] += kid["events"]
    head.setdefault("alsoChildIn", kid["household"])
hh_order = [k for k in hh_order if k not in same_person]
for k in list(hh_people):
    if k in same_person: del hh_people[k]
print(f"  households: {len(same_person)} people were one person recorded in two houses"
      + (f"; {len(refused_join)} REFUSED: " + "; ".join(refused_join) if refused_join else ""))

# Every address the previous scheme handed out, so none of them is orphaned
# when two half-records become one person.
old_slug = {}
_c = collections.Counter(kebab(clean(_pre_join[k][0])) for k in _pre_join_order)
_u = set()
for k in _pre_join_order:
    _b = kebab(clean(_pre_join[k][0]))
    _s = _b if _c[_b] == 1 else f"{_b}-of-{kebab(_pre_join[k][1])[:34]}"
    while _s in _u: _s += "-2"
    _u.add(_s); old_slug[k] = _s

# slugs, exactly as the old people.js assigned them, so no URL changes
counts = collections.Counter(kebab(clean(hh_people[k]["name"])) for k in hh_order)
used = set()
for k in hh_order:
    p = hh_people[k]
    base = kebab(clean(p["name"]))
    slug = base if counts[base] == 1 else f"{base}-of-{kebab(p['household'])[:34]}"
    while slug in used: slug += "-2"
    used.add(slug); p["slug"] = slug

def similar(a, b):
    """One forename spelled two ways. The tree writes CONSTANZA Maione where
    line.json writes COSTANZA; the surname is identical and one letter differs.
    Refusing that would drop a generation over an n. A difference of more than
    one letter is not accepted, and the page says a variant was used."""
    if a == b: return True
    pa, pb = a.split(), b.split()
    if len(pa) != len(pb) or not pa: return False
    if pa[-1] != pb[-1]: return False           # the surname must be exact
    diff = 0
    for x, y in zip(pa, pb):
        if x == y: continue
        if abs(len(x) - len(y)) > 1: return False
        # one insertion, deletion or substitution
        if len(x) == len(y):
            d = sum(1 for i, j in zip(x, y) if i != j)
        else:
            lo, hi = sorted((x, y), key=len)
            d = 0 if any(hi[:i] + hi[i+1:] == lo for i in range(len(hi))) else 2
        if d > 1: return False
        diff += 1
    return diff <= 1

# The spine as the family tree draws it — walked as a SINGLE CHAIN from the
# anchor's own spouse, because at each step the two people found are the two
# parents of one child, which is to say the couple. That matters: generation
# seven's Carmine Antonio Falco has no «wife» edge in the tree at all, and
# reading his partner off the child is the only way to identify the couple.
spine_tree = {}
spine_variant = set()
cur, depth = spouse_of_anchor, 0
while cur is not None and depth < 12:
    depth += 1
    rents = [by_id[i] for w in ("mother", "father") for i in edges(cur, w) if i in by_id]
    if not rents:
        break
    gen_no = 10 - depth
    g = next((x for x in line if x["gen"] == gen_no), None)
    nxt = None
    if g:
        nf, sf = forms(g["name"]), forms(g.get("spouse"))
        for q in rents:
            if not (forms(q["name"]) & nf):
                continue
            others = set()
            for o in rents:
                if o is not q: others |= forms(o["name"])
            for i in edges(q, "wife") + edges(q, "husband"):
                if i in by_id: others |= forms(by_id[i]["name"])
            exact = bool(sf & others)
            variant = exact or any(similar(a, b) for a in sf for b in others)
            # the ancestor's name AND the couple must both agree, or nothing
            # is claimed for this generation
            if variant:
                spine_tree[q["id"]] = g
                if not exact:
                    spine_variant.add(q["id"])
                nxt = q
            break
    if nxt is None:
        # The walk stops agreeing with line.json at generation one: the tree
        # still carries AGOSTINO FALCONE at the head, the ancestor this archive
        # discarded and replaced with Matteo Falco. Generation one is therefore
        # taken from the registers alone and the tree's own head of line is
        # left unlabelled. See /method.
        falco = [q for q in rents if "falco" in norm(q.get("name")) or "falco" in norm(q.get("last") or "")]
        nxt = falco[0] if len(falco) == 1 else None
    cur = nxt


# ------------------------------------------------------------- the merge

# One woman is written "Chiara (Clara) Rivetti" by a clerk and "Chiara Rivetti
# / Rivotti (Falco)" by the tree. Matching on the exact string left her on the
# page twice, as her own husband's two wives. Both spellings are indexed.
hh_by_name = collections.defaultdict(set)
for k in hh_order:
    for f in forms(hh_people[k]["name"]): hh_by_name[f].add(k)
tr_by_name = collections.defaultdict(set)
for p in tree:
    if not is_placeholder(p.get("name")):
        for f in forms(p["name"]): tr_by_name[f].add(p["id"])

merge = {}      # tree id -> household key
basis = {}      # tree id -> why
refused = []
for nm in sorted(tr_by_name):
    tids = sorted(tr_by_name[nm] - set(merge))
    hks = sorted((hh_by_name.get(nm) or set()) - set(merge.values()))
    if not tids or len(hks) != 1:
        continue
    hk = hks[0]
    hy = years(*[e.get("date") for e in hh_people[hk]["events"]],
               *[e.get("evidence") for e in hh_people[hk]["events"]])
    scored = [(len(hy & years(by_id[t].get("b"), by_id[t].get("d"))), t) for t in tids]
    best = max(s for s, _ in scored)
    top = [t for s, t in scored if s == best]
    if best > 0 and len(top) == 1:
        merge[top[0]] = hk; basis[top[0]] = "name and dates"
    elif best == 0 and len(tids) == 1:
        merge[tids[0]] = hk; basis[tids[0]] = "name alone"
    else:
        refused.append((nm, len(tids)))

# The couple identifies the generation on BOTH sides, so a register head and a
# tree person carrying the same generation are the same person — that is the
# identification the direct-line page already publishes, not a new one. This is
# what puts the register's cited acts and the tree's children on one page.
hh_gen = {}
for k in hh_order:
    p = hh_people[k]
    parts = [x.strip() for x in p["household"].split("&")]
    if any(clean(x) == clean(p["name"]) for x in parts):
        g = generation_of(p["name"], [x for x in parts if clean(x) != clean(p["name"])])
        if g:
            hh_gen.setdefault(g["gen"], k)
for tid, g in spine_tree.items():
    hk = hh_gen.get(g["gen"])
    if hk and tid not in merge and hk not in merge.values():
        merge[tid] = hk
        basis[tid] = "the same generation of the direct line — name and spouse both agree"

# ...and the same for the WIVES. Generation three's page drew Andreana Crisci
# twice — once as the register's household head and once as the tree's
# "Andrea / Andreana Crisci (Falco)" — because the tree holds two women of that
# name and the plain name test refuses to choose between them.
#
# The couple chooses. line.json names generation three's wife; exactly one of
# the two is married to the spine's Vincenzo; exactly one heads the register
# household beside him. Those are the same woman, on the archive's own
# published identification.
for tid, g in list(spine_tree.items()):
    sp_forms = forms(g.get("spouse") or "")
    if not sp_forms:
        continue
    cands = [i for i in edges(by_id[tid], "wife") + edges(by_id[tid], "husband")
             if i in by_id and (forms(by_id[i]["name"]) & sp_forms)]
    hk = hh_gen.get(g["gen"])
    if not hk or len(cands) != 1:
        continue
    parts = [x.strip() for x in hh_people[hk]["household"].split("&")]
    hh_sp = [k for k in hh_order
             if hh_people[k]["household"] == hh_people[hk]["household"]
             and (forms(hh_people[k]["name"]) & sp_forms)
             and any(clean(x) == clean(hh_people[k]["name"]) for x in parts)]
    if len(hh_sp) != 1:
        continue
    if cands[0] in merge or hh_sp[0] in merge.values():
        continue
    merge[cands[0]] = hh_sp[0]
    basis[cands[0]] = ("the same generation of the direct line — she is the wife the line names, "
                       "on both sides")

# ------------------------------------------------- one record per person

people = {}       # slug -> record
slug_of_tree = {}

for k in hh_order:
    p = hh_people[k]
    people[p["slug"]] = {
        "slug": p["slug"], "name": p["name"], "surname": surname_of(p["name"]),
        "household": p["household"], "role": p["role"], "events": p["events"],
        "sources": ["register"], "living": False,
        "parents": [], "spouses": [], "children": [], "siblings": [],
    }

for p in tree:
    if is_placeholder(p.get("name")): continue
    tid = p["id"]
    if tid in merge:
        slug = hh_people[merge[tid]]["slug"]
        slug_of_tree[tid] = slug
        r = people[slug]
        r["sources"].append("tree")
        r["mergedOn"] = basis[tid]
    else:
        base = kebab(clean(p["name"])) or ("person-" + str(tid))
        slug = base
        n = 2
        while slug in people:
            slug = f"{base}-{n}"; n += 1
        slug_of_tree[tid] = slug
        people[slug] = {
            "slug": slug, "name": strip_ticks(p["name"]),
            "surname": (strip_ticks(p.get("last")) or surname_of(p["name"])).upper(),
            "household": None, "role": None, "events": [],
            "sources": ["tree"], "living": False,
            "parents": [], "spouses": [], "children": [], "siblings": [],
        }
    r = people[slug]
    r["treeId"] = tid
    if really_living(p):
        # name and place in the family, nothing else. Deliberate.
        r["living"] = True
    else:
        for src, dst in (("b","b"),("d","d"),("bp","bp"),("dp","dp")):
            if p.get(src): r[dst] = strip_ticks(p[src])

# ----------------------------------------------------------- the edges

REL = {"parents": ("father", "mother"), "children": ("son", "daughter"),
       "spouses": ("wife", "husband", "spouse"), "siblings": ("brother", "sister")}

# How much a source is worth, strongest first. `line` is the archive's own
# argued identification; `register` is a clerk's own words; `tree` is
# unverified. An edge keeps ALL of its sources — knowing that two independent
# sources agree is worth more than either alone, and the page shows both.
RANK = {"line": 0, "register": 1, "tree": 2}

def put(rec, bucket, slug, name, via):
    for e in rec[bucket]:
        if e["slug"] == slug:
            if via not in e["vias"]:
                e["vias"] = sorted(set(e["vias"] + [via]), key=lambda v: RANK[v])
                e["via"] = e["vias"][0]
            return
    rec[bucket].append({"slug": slug, "name": name, "via": via, "vias": [via]})

# from the family tree
for p in tree:
    if is_placeholder(p.get("name")): continue
    me = people.get(slug_of_tree.get(p["id"]))
    if not me: continue
    for e in (p.get("relatives") or []):
        other = by_id.get(e.get("id"))
        if not other or is_placeholder(other.get("name")): continue
        oslug = slug_of_tree.get(other["id"])
        if not oslug or oslug == me["slug"]: continue
        rel = (e.get("rel") or "").lower()
        for bucket, words in REL.items():
            if any(rel.endswith(w) for w in words):
                put(me, bucket, oslug, strip_ticks(other["name"]), "tree")
                break

# from the registers: a household name is "Father & Mother", its children the
# members marked child. These are relationships a clerk wrote down.
for h in households:
    parts = [s.strip() for s in h["name"].split("&")]
    heads, kids = [], []
    for k in hh_order:
        p = hh_people[k]
        here = p["household"] == h["name"] or p.get("alsoChildIn") == h["name"]
        if not here: continue
        if p["household"] != h["name"] and p.get("alsoChildIn") == h["name"]:
            # she is a child in THIS house and a head in her own
            kids.append(p); continue
        if (p["role"] or "").lower() in NOT_KIN:
            continue                       # a witness is not a relative
        if any(clean(x) == clean(p["name"]) for x in parts) or p["role"] in PARENT_ROLES:
            heads.append(p)
        elif p["role"] in CHILD_ROLES:
            kids.append(p)
    for a in heads:
        for b in heads:
            if a is not b: put(people[a["slug"]], "spouses", b["slug"], b["name"], "register")
        for c in kids:
            put(people[a["slug"]], "children", c["slug"], c["name"], "register")
            put(people[c["slug"]], "parents", a["slug"], a["name"], "register")
    for c in kids:
        for d in kids:
            if c is not d: put(people[c["slug"]], "siblings", d["slug"], d["name"], "register")

for r in people.values():
    tid = r.get("treeId")
    if tid and tid in spine_tree:
        g = spine_tree[tid]
        r["gen"] = g["gen"]; r["line"] = g
        if tid in spine_variant:
            r["spouseVariant"] = True
        continue
    if r["household"]:
        parts = [x.strip() for x in r["household"].split("&")]
        if any(clean(x) == clean(r["name"]) for x in parts):
            g = generation_of(r["name"], [x for x in parts if clean(x) != clean(r["name"])])
            if g:
                r["gen"] = g["gen"]; r["line"] = g

# --------------------------------------- the line itself, as its own edges
#
# The direct line is the archive's own published identification, argued act by
# act on /direct-line. It is not in the tree (the tree still heads the line
# with Agostino Falcone) and it is only partly in the households. So it is
# written in as edges of its own, marked `line`, and the nine generations
# become walkable from any one of them.
gen_slug = {r["gen"]: r["slug"] for r in people.values() if r.get("gen")}
for n in sorted(gen_slug):
    child = people[gen_slug[n]]
    par = people.get(gen_slug.get(n - 1))
    if par:
        put(child, "parents", par["slug"], par["name"], "line")
        put(par, "children", child["slug"], child["name"], "line")
    # the spouse the line names, where that person has a record here
    g = child.get("line") or {}
    sp = clean(g.get("spouse") or "")
    if sp:
        cand = [r for r in people.values()
                if r["slug"] != child["slug"] and (forms(r["name"]) & forms(sp))]
        if len(cand) == 1:
            put(child, "spouses", cand[0]["slug"], cand[0]["name"], "line")
            put(cand[0], "spouses", child["slug"], child["name"], "line")

# ------------------------------- claims the archive has already superseded
#
# The family tree gives PASQUALE FALCO of generation two a father called
# AGOSTINO FALCONE. That is the ancestor this archive examined and DISCARDED —
# the whole of /method's first section is about replacing him with Matteo
# Falco. Drawing him as Pasquale's father without a word would quietly put a
# retracted claim back on the site.
#
# So: for a generation of the line, a tree parent who is not the generation
# before it is marked superseded, and the page says so instead of hiding it.
for n in sorted(gen_slug):
    if n < 2:
        continue
    child = people[gen_slug[n]]
    prev = gen_slug.get(n - 1)
    prev_sp = None
    g_prev = people.get(prev, {}).get("line") or {}
    for e in child["parents"]:
        if e["via"] != "tree":
            continue
        if e["slug"] == prev:
            continue
        if g_prev and (forms(e["name"]) & forms(g_prev.get("spouse") or "")):
            continue          # that is the previous generation's own wife
        e["superseded"] = (
            f"The family tree makes this person a parent of generation {n}. "
            f"This archive does not: it identifies generation {n - 1} as "
            f"{people[prev]['name'] if prev else 'someone else'}. "
            "The reasoning is on the Method page."
        )

# living people must not leak a date through a merged register event either
for r in people.values():
    if r["living"]:
        r["events"] = []
        for f in ("b","d","bp","dp"):
            r.pop(f, None)

# ------------------------------------------------------------- self-check
#
# A genealogy that contradicts itself is worse than one with gaps, and these
# checks exist because every one of them caught something real while this file
# was being written: a witness turned into a husband, a daughter filed as a
# parent, a wife listed twice as two women, and an infant son merged into his
# own grandfather so that generation two became generation three's child.
import sys as _sys
_sys.setrecursionlimit(6000)

def self_check(recs):
    ix = {r["slug"]: r for r in recs}
    problems = collections.Counter()
    detail = collections.defaultdict(list)
    def bad(kind, what):
        problems[kind] += 1
        if len(detail[kind]) < 4: detail[kind].append(what)
    for r in recs:
        me = r["slug"]
        for b in ("parents", "spouses", "children", "siblings"):
            for e in r[b]:
                if e["slug"] == me: bad("a person joined to themselves", f"{r['name']} ({b})")
                if e["slug"] not in ix: bad("an edge to nobody", f"{r['name']} -> {e['slug']}")
        for e in r["parents"]:
            q = ix.get(e["slug"])
            if q and not any(c["slug"] == me for c in q["children"]):
                bad("a parent who does not have the child back", f"{r['name']} <- {e['name']}")
        for e in r["spouses"]:
            q = ix.get(e["slug"])
            if q and not any(c["slug"] == me for c in q["spouses"]):
                bad("a marriage only one of them is in", f"{r['name']} ~ {e['name']}")
        ps = {e["slug"] for e in r["parents"]}
        if ps & {e["slug"] for e in r["children"]}: bad("parent AND child of one person", r["name"])
        if ps & {e["slug"] for e in r["spouses"]}: bad("parent AND spouse of one person", r["name"])
        if r["living"] and (r.get("b") or r.get("d") or r.get("bp") or r.get("dp") or r["events"]):
            bad("A LIVING PERSON CARRYING DATES", r["name"])
    def is_own_ancestor(sl, stack):
        for e in ix[sl]["parents"]:
            if e["slug"] in stack: return True
            if is_own_ancestor(e["slug"], stack | {e["slug"]}): return True
        return False
    for r in recs:
        if is_own_ancestor(r["slug"], {r["slug"]}):
            bad("somebody is their own ancestor", r["name"])
    return problems, detail

out = sorted(people.values(), key=lambda r: (r["surname"], clean(r["name"])))
_p, _d = self_check(out)
if _p:
    print("  SELF-CHECK FAILED:")
    for k, n in _p.most_common():
        print(f"    {n:4}  {k}   e.g. {'; '.join(_d[k])}")
    raise SystemExit("refusing to write a contradictory genealogy")
# ---------------------------------------------------------- old addresses
#
# Joining two half-records into one person changes that person's address.
# Chiara Rivetti used to live at two URLs — one per household — and now lives
# at one. Both old addresses are kept alive as redirects: a public archive
# that renumbers its own people and lets the old links rot is not much of an
# archive.
alias = {}
for ck, hk in same_person.items():
    new_slug = hh_people[hk]["slug"]
    for k in (ck, hk):
        if k in old_slug and old_slug[k] != new_slug:
            alias[old_slug[k]] = new_slug
json.dump(alias, open(path("site/src/data/people-aliases.json"), "w"),
          ensure_ascii=False, indent=0)
print(f"  {len(alias)} old person URLs kept alive as redirects")

print("  self-check: clean — no cycles, no one-sided marriages, no dates on the living")

json.dump(out, open(path("site/src/data/people.json"), "w"), ensure_ascii=False, indent=0)

# --------------------------------------------------------------- report
edge_via = collections.Counter(
    e["via"] for r in out for b in ("parents","spouses","children","siblings") for e in r[b])
print(f"{len(out)} people written")
print(f"  from the registers only : {sum(1 for r in out if r['sources'] == ['register'])}")
print(f"  from the tree only      : {sum(1 for r in out if r['sources'] == ['tree'])}")
print(f"  merged from both        : {sum(1 for r in out if len(r['sources']) > 1)}"
      f"  ({collections.Counter(r.get('mergedOn') for r in out if r.get('mergedOn'))})")
print(f"  living, name only       : {sum(1 for r in out if r['living'])}")
print(f"  with any relationship   : {sum(1 for r in out if any(r[b] for b in ('parents','spouses','children','siblings')))}")
print(f"  relationship edges      : {dict(edge_via)}")
print(f"  merges refused (same name, no date agreement): {len(refused)}")
for nm, n in refused[:6]: print(f"      {nm} — {n} in the tree")
