#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Roots & Routes: the tree page for this archive, built from this archive's own committed data.

    python3 tools/build-tree-page.py   # rebuild data/tree-page/ (tree.json, atlas-data.json, roots.html, roots.embed.html)
    python3 tools/build-tree-page.py --check            # exit 1 if the page is older than the data it was built from

WHERE THE PEOPLE COME FROM. There is no committed GEDCOM (the tree export is private and carries every living person). The people are the ones
site/src/data/people.json holds, which tools/build_people.py writes from the register work and the tree under the living standard (a living person is
there as a name and a relationship, flagged `living`). Those who are not living are turned into a small GEDCOM (data/tree-page/people.ged, not committed)
and handed to the family-tree-page skill's converter, vendored in tools/tree-page/ so CI and other sessions do not depend on ~/.claude. On top of the
archive's own flag this adapter omits (a) anyone data/living-by-inference.json lists, (b) an undated person who has a living parent, spouse or child, and
(c) anyone with no name. The converter then adds its floor: nobody with no death recorded and a birth year (estimated ones included) in the last 110
years is drawn.

WHAT THE ARCHIVE DOES NOT HOLD, AND THIS FILE DOES NOT PRETEND IT DOES. people.json has no sex. The page needs one (the father is the left of the fan,
"uncle" or "aunt" in Kinship). It is taken, in this order, from (1) the person's role in a register household (father, mother, bride...), (2) the order
of the household's name («Husband & Wife»), (3) what the register events say of them (named as mother, her own age), (4) the ending of the first given
name (Italian and Latin forms: -a is feminine, bar a short list of masculine ones), and tools/build-tree-page.py counts how many came from each and how
often (4) disagrees with (1)-(3). A parent pair that comes out the same sex is reported, not hidden. It is a drawing aid, not a finding about anybody.

COLOUR is the surname family from the Record Atlas catalogue (data/surname-families.json, read only, through its own lookup) where the catalogue has the
name, and the surname otherwise: which spellings are one name is the catalogue's to say (surname-variants skill), and this archive keeps no list of them.
The person's catalogue family id is also written as `sk` for the Surnames view.

PLACES are resolved through data/tree-page/place_map.json, never guessed. A place string is taken from data/era-ground.tsv (the town decided for the string
AS PRINTED in people.json) and data/era-towns.tsv (that town's point), its country from the Atlas's own geo.country_of on the point; a string that file
refuses (a country only, a ship, a string that carries another person's birth) stays unresolved. Nothing is accepted from the Atlas by its name alone
(the converter's --accept-unique is not used: it took «Italy», a country, for a place); data/tree-page/place-additions.json holds any decided by hand, each
with its reason.
A person whose own birth place does not resolve is drawn at a relative's birth place and marked `bpe`, which the page says in their panel.

PARENT LINKS are the archive's `parents`, less a retracted one (`superseded`) and a duplicate it keeps apart on purpose (`sameAs`). A link read in a
register is drawn solid, one that only the (unverified) family tree gives is drawn dashed (`fg`/`mg` 0).
"""
import argparse, collections, datetime, hashlib, io, json, os, re, subprocess, sys, unicodedata

sys.dont_write_bytecode = True      # the Atlas is read only: importing its scripts must not leave a __pycache__ there

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "src", "data")
OUT = os.path.join(ROOT, "data", "tree-page")
TP = os.path.join(ROOT, "tools", "tree-page")
EXT = os.path.join(TP, "painted-lines.ext.html")
HOST = "falco.defranceski.com"
ATLAS_CANDIDATES = [os.environ.get("RECORD_ATLAS", ""), os.path.expanduser("~/Projects/Family Projects/Record Atlas"),
                    os.path.join(os.path.dirname(ROOT), "Record Atlas")]
INPUTS = [os.path.join(DATA, "people.json"), os.path.join(ROOT, "data", "living-by-inference.json"),
          os.path.join(ROOT, "data", "era-ground.tsv"), os.path.join(ROOT, "data", "era-towns.tsv")]

def jl(path): return json.load(io.open(path, encoding="utf-8"))
def run(args):
    print("$", " ".join(os.path.relpath(a, ROOT) if os.path.isabs(a) and a.startswith(ROOT) else a for a in args)); r = subprocess.run(args)
    if r.returncode: sys.exit(r.returncode)
def inputs_hash():
    h = hashlib.sha1()
    for n in INPUTS: h.update(io.open(n, "rb").read())
    for n in ("tree-views.template.html", "painted-lines.ext.html", "gedcom_to_tree.py"): h.update(io.open(os.path.join(TP, n), "rb").read())
    h.update(io.open(os.path.abspath(__file__), "rb").read())
    for n in ("place_map.json", "place-additions.json"):
        pm = os.path.join(OUT, n)
        if os.path.exists(pm): h.update(io.open(pm, "rb").read())
    return h.hexdigest()[:16]
def atlas_path():
    for c in ATLAS_CANDIDATES:
        if c and os.path.exists(os.path.join(c, "data", "places.json")): return c
    sys.exit("Record Atlas checkout not found (set RECORD_ATLAS)")

def fold(s): return re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()).strip()
def km(a, b, c, d):
    import math
    p = math.pi / 180; x = math.sin((c - a) * p / 2) ** 2 + math.cos(a * p) * math.cos(c * p) * math.sin((d - b) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(x))
YEAR = re.compile(r"(?<!\d)(1[0-9]{3}|20[0-9]{2})(?!\d)")
def year_of(s):
    m = YEAR.search(str(s or "")); return int(m.group(1)) if m else None
BOUND = re.compile(r"^\s*(before|dead by|died before|by|after)\b", re.I)    # a date that is a limit, not the day

# ---------------------------------------------------------------- the archive's own people
OWN_BIRTH = re.compile(r"^(birth|baptism)\b(?!\s+of\b)", re.I)
OWN_DEATH = re.compile(r"^(death|burial)\b(?!\s+(of|window)\b)", re.I)
def own_event(p, rx):
    for e in p.get("events") or []:
        if rx.match(e.get("event") or "") and (e.get("date") or e.get("place")): return e
    return None

ROLE_SEX = {"father": "m", "grandfather": "m", "great-grandfather": "m", "great-grandfather of the children": "m", "son": "m", "husband": "m", "groom": "m",
            "father of the bride": "m", "father of the groom": "m", "mother": "f", "grandmother": "f", "great-grandmother": "f", "daughter": "f", "wife": "f",
            "bride": "f", "mother of the bride": "f", "mother of the groom": "f", "sister of the bride": "f", "wife of the son": "f", "midwife": "f"}
F_TOK = re.compile(r"\b(mother|her|wife|widow|bride|midwife|levatrice|matrina|sister)\b", re.I)
M_TOK = re.compile(r"\b(father|his|husband|groom|brother)\b", re.I)
MALE_A = {"andrea", "nicola", "luca", "elia", "mattia", "tobia", "zaccaria", "geremia", "isaia", "sila", "enea", "gaspare"}
FEM_NOT_A = {"beatrice", "agnese", "ester", "esther", "ines", "carmen", "elisabeth", "elizabeth", "rachel", "ruth", "dolores", "mercede", "mercedes", "agnes",
             "judith", "margaret", "ann", "susan", "jean", "joan", "edith", "alice", "grace", "rose", "mary", "helen"}
def clean_base(name): return re.sub(r"\s*\([^()]*\)\s*$", "", str(name or "")).strip()
def split_name(p):
    base = clean_base(p["name"]); sur = str(p.get("surname") or "")
    m = re.search(r"\s+" + re.escape(sur.title()) + r"\s*$", base, re.I)
    if m: return base[:m.start()].strip(), base[m.start():].strip()
    toks = base.split()
    f = fold(sur).split()
    if f and len(toks) > len(f) and fold(" ".join(toks[-len(f):])) == " ".join(f): return " ".join(toks[:-len(f)]), " ".join(toks[-len(f):])
    return base, sur.title()
def name_sex(given):
    first = re.sub(r"[()\[\]]", " ", given).split()
    if not first: return None
    f = fold(first[0])
    if f in FEM_NOT_A: return "f"
    if f in MALE_A: return "m"
    return "f" if f.endswith("a") else "m"

def sex_table(people):
    """-> {slug: (sex, how)}. how in role, household, event, name."""
    out, hh = {}, {}
    for p in people:
        s = ROLE_SEX.get(p.get("role") or "")
        if s: out[p["slug"]] = (s, "role")
    for p in people:
        if p["slug"] in out or not p.get("household") or "&" not in p["household"]: continue
        a, b = [x.strip() for x in p["household"].split("&", 1)]
        me = fold(clean_base(p["name"]))
        if me == fold(clean_base(a)): out[p["slug"]] = ("m", "household")
        elif me == fold(clean_base(b)): out[p["slug"]] = ("f", "household")
    for p in people:
        if p["slug"] in out: continue
        txt = " ".join(e.get("event") or "" for e in p.get("events") or [])
        f, m = len(F_TOK.findall(txt)), len(M_TOK.findall(txt))
        if f and not m: out[p["slug"]] = ("f", "event")
        elif m and not f: out[p["slug"]] = ("m", "event")
    for p in people:
        if p["slug"] not in out:
            s = name_sex(split_name(p)[0])
            if s: out[p["slug"]] = (s, "name")
    return out

def who_is_drawable(all_people, rep):
    """The archive's own flag, then the extra belts. Returns the people who may go into the GEDCOM at all."""
    inf = jl(os.path.join(ROOT, "data", "living-by-inference.json"))
    inferred = {str(i) for i in inf.get("ids", [])} | {str(i) for i in inf.get("byHand", [])}
    overridden = {str(i) for i in inf.get("overridden", [])}
    inferred -= overridden
    by = {p["slug"]: p for p in all_people}
    living = {p["slug"] for p in all_people if p.get("living") or str(p.get("treeId")) in inferred}
    rep["living_flag_in_people_json"] = sum(1 for p in all_people if p.get("living"))
    rep["living_by_inference_extra"] = sum(1 for p in all_people if not p.get("living") and str(p.get("treeId")) in inferred)
    def dated(p): return bool(p.get("b") or p.get("d") or own_event(p, OWN_BIRTH) or own_event(p, OWN_DEATH))
    keep, adj, noname = [], 0, 0
    for p in all_people:
        if p["slug"] in living: continue
        if not dated(p) and any(r["slug"] in living for k in ("parents", "spouses", "children") for r in p.get(k) or []):
            adj += 1; continue
        if not clean_base(p["name"]) or p.get("surname") in (None, "", "—") or "unnamed" in p["name"].lower():
            noname += 1; continue
        keep.append(p)
    rep["undated_beside_a_living_person_omitted"] = adj
    rep["no_name_not_drawn"] = noname
    return keep

def gedcom(people, path, sexes, rep):
    ids = {p["slug"] for p in people}
    bys = {p["slug"]: p for p in people}
    out = ["0 HEAD", "1 CHAR UTF-8"]
    fams, fam_of_child, fam_of_spouse = {}, {}, collections.defaultdict(list)
    def fam(h, w):
        k = (h or "", w or "")
        if k not in fams: fams[k] = "@F%d@" % (len(fams) + 1)
        return fams[k]
    def usable_parents(p):
        ps = [r for r in p.get("parents") or [] if r["slug"] in ids and "superseded" not in r and "sameAs" not in r]
        return ps
    link_via = {}
    same_sex_pairs = 0
    for p in people:
        par = usable_parents(p)
        if not par: continue
        men = [r for r in par if sexes[r["slug"]][0] == "m"]; wom = [r for r in par if sexes[r["slug"]][0] == "f"]
        # prefer a parent read in a register to one only the family tree gives
        rank = lambda r: 0 if set(r.get("vias") or [r.get("via")]) & {"register", "line"} else 1
        men.sort(key=rank); wom.sort(key=rank)
        f = men[0] if men else None; m = wom[0] if wom else None
        if not f and not m: continue
        if len(par) >= 2 and (not f or not m): same_sex_pairs += 1
        fam_of_child[p["slug"]] = fam(f and f["slug"], m and m["slug"])
        link_via[p["slug"]] = (rank(f) if f else None, rank(m) if m else None)
    for p in people:
        for s in p.get("spouses") or []:
            if s["slug"] in ids:
                a, b = (p["slug"], s["slug"]) if sexes[p["slug"]][0] == "m" else (s["slug"], p["slug"])
                if sexes[a][0] == sexes[b][0]: rep["spouse_pairs_same_sex_as_inferred"] = rep.get("spouse_pairs_same_sex_as_inferred", 0) + 1; continue
                k = fam(a, b)
                if k not in fam_of_spouse[p["slug"]]: fam_of_spouse[p["slug"]].append(k)
    rep["child_links_with_one_parent_only_because_the_pair_came_out_one_sex"] = same_sex_pairs
    bounds = {}
    for p in people:
        g, s = split_name(p)
        out += ["0 @%s@ INDI" % p["slug"], "1 NAME %s /%s/" % (g.replace("/", " "), s.replace("/", " ")), "1 SEX %s" % sexes[p["slug"]][0].upper()]
        b = p.get("b") or (own_event(p, OWN_BIRTH) or {}).get("date")
        bpl = p.get("bp") or (own_event(p, OWN_BIRTH) or {}).get("place")
        d = p.get("d") or (own_event(p, OWN_DEATH) or {}).get("date")
        dpl = p.get("dp") or (own_event(p, OWN_DEATH) or {}).get("place")
        if b or bpl:
            out.append("1 BIRT")
            if b and not BOUND.match(b) and year_of(b): out.append("2 DATE %s" % b)
            if bpl: out.append("2 PLAC %s" % bpl)
        if d or dpl or own_event(p, OWN_DEATH):
            out.append("1 DEAT")
            if d and BOUND.match(d) and year_of(d): bounds[p["slug"]] = year_of(d)
            elif d and year_of(d): out.append("2 DATE %s" % d)
            if dpl: out.append("2 PLAC %s" % dpl)
        if p["slug"] in fam_of_child: out.append("1 FAMC %s" % fam_of_child[p["slug"]])
        for fx in fam_of_spouse.get(p["slug"], []): out.append("1 FAMS %s" % fx)
    for (h, w), fx in fams.items():
        out.append("0 %s FAM" % fx)
        if h: out.append("1 HUSB @%s@" % h)
        if w: out.append("1 WIFE @%s@" % w)
        for cid, f in fam_of_child.items():
            if f == fx: out.append("1 CHIL @%s@" % cid)
    out.append("0 TRLR")
    io.open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    return link_via, bounds

# ---------------------------------------------------------------- places the archive has already placed
def town_points():
    pts = {}
    for line in io.open(os.path.join(ROOT, "data", "era-towns.tsv"), encoding="utf-8"):
        if line.startswith("#") or not line.strip(): continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 3 or c[0] == "town": continue
        pts[c[0]] = (float(c[1]), float(c[2]), c[3] if len(c) > 3 else "")
    return pts

def seed_place_map(atlas, rep):
    """data/era-ground.tsv decided, for every place string AS PRINTED in people.json, the town it belongs to (column 4) and REFUSED a string that is a
    country only, a ship, a journey or a string that carries another person's birth: those rows have no town and stay unresolved here. data/era-towns.tsv
    holds each town's point. The country is the Atlas's own geo.country_of on the point, never a guess from the string; a Record Atlas place is linked
    only where it has the same name within 15 km."""
    sys.path.insert(0, os.path.join(atlas, "scripts")); import geo
    cj = jl(os.path.join(atlas, "data", "countries.json"))["countries"]
    pj = jl(os.path.join(atlas, "data", "places.json"))["places"]
    byname = collections.defaultdict(list)
    for x in pj:
        for nm in [x["name"]] + [n["n"].split(",")[0] for n in x.get("names", [])]: byname[fold(nm)].append(x)
    pm_path = os.path.join(OUT, "place_map.json")
    pm = jl(pm_path) if os.path.exists(pm_path) else {}
    pts = town_points()
    seeded = 0
    for line in io.open(os.path.join(ROOT, "data", "era-ground.tsv"), encoding="utf-8"):
        if line.startswith("#") or not line.strip(): continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 4 or c[0] == "place": continue
        raw, town = c[0], c[3].strip()
        if not town or town not in pts or (pm.get(raw) or {}).get("lat") is not None: continue
        lat, lon, how = pts[town]
        iso = geo.country_of(lat, lon)
        if not iso: continue
        hit = next((x for x in byname.get(fold(town), []) if x.get("country") == iso and km(lat, lon, x["lat"], x["lon"]) <= 15), None)
        pm[raw] = {"name": town, "lat": lat, "lon": lon, "country": cj.get(iso, {}).get("name", iso), "iso": iso, "atlas_id": hit["id"] if hit else None,
                   "how": "data/era-ground.tsv town; point from data/era-towns.tsv (%s); country by the Atlas's geo.country_of" % how}
        seeded += 1
    added = 0
    ap_ = os.path.join(OUT, "place-additions.json")
    if os.path.exists(ap_):
        for k, v in jl(ap_)["places"].items():
            if (pm.get(k) or {}).get("lat") is None: pm[k] = v; added += 1
    io.open(pm_path, "w", encoding="utf-8").write(json.dumps(pm, indent=1, ensure_ascii=False))
    rep["place_strings_from_era_ground"] = seeded; rep["place_strings_from_additions"] = added
    print("place_map: %d place strings from era-ground.tsv, %d from place-additions.json" % (seeded, added))

# ---------------------------------------------------------------- colour from the Atlas catalogue
def surname_groups(atlas, people):
    sys.path.insert(0, os.path.join(atlas, "scripts")); import surname_variants as sv
    cat = sv.load()
    out = {}
    for p in people:
        sur = split_name(p)[1]
        hit = sv.lookup(cat, sur) if sur else None
        if hit and hit[2] == "member": out[p["slug"]] = (hit[0]["id"], hit[0]["name"], True)
        else: out[p["slug"]] = (fold(sur).replace(" ", ""), sur.title() if sur.isupper() else sur, False)
    return out

def build(a, rep):
    os.makedirs(OUT, exist_ok=True)
    allp = jl(os.path.join(DATA, "people.json"))
    rep["people_in_people_json"] = len(allp)
    people = who_is_drawable(allp, rep)
    rep["offered_to_the_converter"] = len(people)
    sexes = sex_table(people)
    rep["sex_from"] = dict(collections.Counter(v[1] for v in sexes.values()))
    # how often the name ending disagrees with the register's own words (a measure of the fallback, over the people who have both)
    ev = [(p["slug"], sexes[p["slug"]][0]) for p in people if sexes[p["slug"]][1] != "name"]
    pby = {p["slug"]: p for p in people}
    dis = sum(1 for s, x in ev if name_sex(split_name(pby[s])[0]) not in (None, x))
    rep["name_ending_disagrees_with_record_for"] = "%d of %d" % (dis, len(ev))
    ged = os.path.join(OUT, "people.ged")
    link_via, bounds = gedcom(people, ged, sexes, rep)
    slugs = {p["slug"]: p["slug"] for p in people}
    io.open(os.path.join(OUT, "slugs.json"), "w", encoding="utf-8").write(json.dumps(slugs, ensure_ascii=False))
    atlas = atlas_path(); seed_place_map(atlas, rep)
    tree, pm = os.path.join(OUT, "tree.json"), os.path.join(OUT, "place_map.json")
    cmd = [sys.executable, os.path.join(TP, "gedcom_to_tree.py"), ged, "--out", tree, "--place-map", pm, "--atlas", atlas, "--living", "omit",
           "--lines", "8", "--slugs", os.path.join(OUT, "slugs.json"), "--title", "Roots & Routes",
           "--subtitle", "Explore the family tree ten ways: by generation, place, era and relationship. Click anyone and every view follows."]
    run(cmd)
    t = jl(tree)
    grp = surname_groups(atlas, people)
    counts = collections.Counter(grp[p["id"]][:2] for p in t["people"] if p["id"] in grp)
    top = [g for g, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0][1]))][:7]
    idx = {g: i for i, g in enumerate(top)}
    pmj = jl(pm)
    ok = lambda k: bool(k) and pmj.get(k) and pmj[k].get("lat") is not None and pmj[k].get("name")
    by = {p["slug"]: p for p in people}
    bpe = 0
    for p in t["people"]:
        src = by[p["id"]]
        g = grp[p["id"]]
        p["line"] = idx.get(g[:2], 7)
        if g[2]: p["sk"] = g[0]          # the catalogue's family id, for the Surnames view; a name the catalogue lacks is grouped by its own folded spelling there
        p["page"] = "/people/%s/" % p["id"]
        own_bp = src.get("bp") or (own_event(src, OWN_BIRTH) or {}).get("place")
        if not ok(own_bp): p["bpe"] = 1; bpe += 1
        fv = link_via.get(p["id"])
        if fv:
            if p.get("father") and fv[0] is not None: p["fg"] = 0 if fv[0] else 2
            if p.get("mother") and fv[1] is not None: p["mg"] = 0 if fv[1] else 2
        if p["id"] in bounds:     # «dead by 1878» / «before 1825» is a limit, not the year of death
            lim = bounds[p["id"]]
            if p.get("dy") is None or p["dy"] > lim: p["dy"] = lim
            p["dye"] = True
    rep["people_drawn_at_a_relatives_birth_place"] = bpe
    t["lines"] = [{"sur": g[1], "host": HOST} for g in top] + [{"sur": "Other", "host": HOST}]
    t["meta"].update({"rowLabel": "Surname family", "lineLabel": "Surname family"})
    drop_conflicts(t, tree)
    io.open(tree, "w", encoding="utf-8").write(json.dumps(t, ensure_ascii=False, separators=(",", ":")))
    rep["colour_families"] = [g[1] for g in top]

def drop_conflicts(t, tree):
    """A person whose recorded death comes before their birth, or more than 110 years after it, is not one life. They are not drawn, they are named in tree.report.json (conflicts) for the
    research to settle, and every relation to them is removed so the page stays symmetric."""
    bad = {p["id"] for p in t["people"] if p.get("dy") is not None and not 0 <= p["dy"] - p["by"] <= 110}
    rep_path = os.path.splitext(tree)[0] + ".report.json"; rep = jl(rep_path)
    rep["conflicts"] = [{"id": p["id"], "born": p["by"], "died": p["dy"], "birth_is_an_estimate": bool(p.get("bye"))} for p in t["people"] if p["id"] in bad]
    if bad:
        t["people"] = [p for p in t["people"] if p["id"] not in bad]
        for p in t["people"]:
            for k in ("father", "mother"):
                if p.get(k) in bad: p[k] = None; p.pop("fg" if k == "father" else "mg", None)
            p["spouse"] = [x for x in p["spouse"] if x not in bad]; p["kids"] = [x for x in p["kids"] if x not in bad]
        if t.get("focus") in bad: t["focus"] = t["people"][0]["id"]
        print("conflicts: %d people whose death is before their birth (or over 110 years) are not drawn" % len(bad))
    io.open(rep_path, "w", encoding="utf-8").write(json.dumps(rep, indent=1, ensure_ascii=False))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        try: have = jl(os.path.join(OUT, "tree.json"))["meta"]["inputs"]
        except Exception: print("tree page: not built yet. python3 tools/build-tree-page.py"); sys.exit(1)
        if have != inputs_hash(): print("tree page is STALE: the people, the living list, era-ground, the place map or the builder changed since it was built.\n  python3 tools/build-tree-page.py"); sys.exit(1)
        print("tree page is current"); return
    rep = {}
    build(a, rep)
    tree = os.path.join(OUT, "tree.json"); pm = os.path.join(OUT, "place_map.json"); ad = os.path.join(OUT, "atlas-data.json"); page = os.path.join(OUT, "roots.html")
    run([sys.executable, os.path.join(TP, "build_atlas_data.py"), "--atlas", atlas_path(), "--tree", tree, "--place-map", pm, "--out", ad])
    t = jl(tree); t["meta"]["inputs"] = inputs_hash()
    io.open(tree, "w", encoding="utf-8").write(json.dumps(t, ensure_ascii=False, separators=(",", ":")))
    # the adapter's own numbers go beside the converter's in tree.report.json
    rp = os.path.join(OUT, "tree.report.json"); r = jl(rp)
    r["adapter"] = rep
    r["people_drawn"] = len(t["people"])
    io.open(rp, "w", encoding="utf-8").write(json.dumps(r, indent=1, ensure_ascii=False))
    tpl = os.path.join(TP, "tree-views.template.html")
    run([sys.executable, os.path.join(TP, "build_page.py"), "--template", tpl, "--tree", tree, "--atlas-data", ad, "--out", page, "--ext", EXT])
    embed = os.path.join(OUT, "roots.embed.html")
    run([sys.executable, os.path.join(TP, "build_page.py"), "--template", tpl, "--tree", tree, "--atlas-data", ad, "--out", embed, "--embed", "--ext", EXT])
    run([sys.executable, os.path.join(TP, "check_tree_page.py"), "--tree", tree, "--atlas-data", ad, "--page", page])
    run([sys.executable, os.path.join(TP, "check_tree_page.py"), "--tree", tree, "--atlas-data", ad, "--page", embed])

if __name__ == "__main__": main()
