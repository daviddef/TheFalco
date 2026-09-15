#!/usr/bin/env python3
"""Consolidate every named individual this archive has found into one register,
each with the source that names them and, where one exists, a link to it."""
import csv, json, re, os, collections

ROWS = []
def add(name, surname, detail, source, link, kind, sortkey=""):
    name = (name or "").strip()
    if not name or len(name) < 3: return
    ROWS.append(dict(name=name, surname=surname, detail=detail.strip(" ·—"),
                     source=source, link=link, kind=kind, sort=sortkey))

# Trades and descriptors the registers append to a name. They are NOT surnames, and
# taking the last word blindly filed 179 real people under "CONTADINO" — unfindable by
# the name they actually had. Stripped before the surname is taken; never discarded,
# because the trade is carried in the detail line already.
# Two lists, because one word can be two things.
#
# «Contadino» is never anybody's surname in this corpus, so it can be stripped
# wherever it falls. But FERRARO is a blacksmith AND a surname — it is the
# Zampiello maternal name — and SARTORE and MASSARO are the same. Stripping
# those blind filed Giuseppa Ferraro under MARIA, her middle name, and put
# Maria Rosa Ferraro under ROSA.
#
# The registers themselves settle it: in 555 of 568 rows a trade is written
# after a COMMA and a surname is not. So an ambiguous word is only a trade
# when the comma says so.
TRADES_ONLY = {
    "contadino", "contadina", "colono", "colona", "vaticale", "possidente",
    "proprietario", "proprietaria", "calzolajo", "calzolaio", "locandiere",
    "bottegajo", "bottegaio", "panettiere", "filatrice", "tessitrice",
    "guarniciere", "guarnitore", "ortolano", "pettinatore", "cappellaio",
    "cappellajo", "sportaro", "vinivendolo", "rivenditore", "rivendugliolo",
    "serviente", "gentildonna", "gentiluomo", "monaca", "conversa",
    "arciprete", "sacerdote", "corattiere", "recimaro", "recimatore",
    "vaticaro", "gabelloto", "pizzajolo", "inservidente", "sensale",
    "defunto", "defunta", "vedovo", "vedova", "regnicolo", "regnicola",
}
TRADE_OR_SURNAME = {
    "ferraro", "sartore", "sarto", "sarta", "massaro", "fabbro",
    "barbiere", "macellajo", "macellaio", "oste", "pastaio", "pastajo",
    "notaro", "notaio", "corriere", "falegname", "muratore", "fornaro",
}

PARTICLES = {"di", "de", "de'", "del", "della", "dell'", "d'", "lo", "la", "le", "li"}

def _clean(n):
    """Drop trailing trade words and record-keeping tails, so the surname is
    the surname — without eating a surname that happens to name a trade."""
    n = re.sub(r"\s+", " ", (n or "").strip())
    had_comma = "," in n

    # record-keeping tails the index adds: "(b. 1930)", "m. Francesca …",
    # "Coniuge Maria …", "fu Simone", "del fu Simone". None is part of the name.
    n = re.sub(r"\s*\([^)]*\)", " ", n)
    n = re.sub(r"\s+(?:m\.|Coniuge|coniuge)\s.*$", "", n)
    n = re.sub(r"\s+(?:del\s+)?fu\s+\S+.*$", "", n, flags=re.I)
    n = re.sub(r"\s*—.*$", "", n)          # "Maria —" records no surname at all
    n = re.sub(r"\s+\d+\b.*$", "", n)       # "Chiara Rivetti 80" — the age is not a name
    n = re.sub(r"[⚠★✔]", "", n)             # reading-flags the notes carry, not part of the name
    n = re.sub(r"\s+[-–]\s+\S+$", "", n)    # "ZAMPIELLO Giovanni - PWI60047" — a file reference
    n = re.sub(r"[,;]\s*$", "", n)

    parts = [p for p in n.split(" ") if p and p.strip(",.;·—-")]
    # Trailing scraps that are not names: an abbreviation left behind by the
    # date-strip ("b."), a multiplicity marker ("x2"), any token with a digit.
    while len(parts) > 1 and (
            re.fullmatch(r"[a-z]{1,2}\.?", parts[-1]) or
            re.fullmatch(r"[xX]\d+", parts[-1]) or
            re.search(r"\d", parts[-1])):
        parts.pop()
    # This archive's own doubt-marker is not a surname: an uncertain reading is
    # published as "Cioffi [?]", which left alone files her under [?].
    #
    # "maggiore" and "minore" are NOT stripped here even though a civil marriage
    # act uses them for of-age and under-age. MAGGIORE IS A REAL ARIENZO SURNAME
    # — Silvestro, Carmine the declarant, Maria Carmina — and stripping it
    # globally deleted eleven real people and refiled a twelfth under CARMINA.
    # The act register strips it locally, where the source settles the meaning.
    NOT_SURNAMES = {"[?]", "(?)", "?", "dec.", "defunto", "defunta"}
    while len(parts) > 1 and parts[-1].strip(",.;").lower() in NOT_SURNAMES:
        parts.pop()
    while len(parts) > 1:
        w = parts[-1].strip(",.;").lower()
        if w in TRADES_ONLY or (had_comma and w in TRADE_OR_SURNAME):
            parts.pop()
        else:
            break
    if parts:
        parts[-1] = parts[-1].rstrip(",;")
    # "LUCIA COPPA /CIOFFI" is one surname the archive reads two ways; keep it
    # as the pair rather than filing her under a slash.
    if len(parts) > 1 and parts[-1].startswith("/"):
        parts[-2:] = [parts[-2] + parts[-1]]
    return parts

# Some "names" in the sources are not names at all but a description of what
# could not be read — "a daughter, name not legible (machine gives «proja»)".
# Fed to the surname deriver those file the child under LEGIBLE, which invents
# a family. A description opens with an article, or says in words that the
# reading failed.
#
# NOT a comma test. A comma here almost always separates a name from a trade —
# "Agostino Anigale, vaticale" — and screening on it re-filed 1,133 correctly
# surnamed people as unknown.
_NOT_A_NAME = ("not legible", "illegible", "name unknown", "machine gives",
               "not recorded", "unnamed", "no name")

def is_description(n):
    t = str(n or "").strip().lower()
    if not t:
        return False
    return (t.startswith(("a ", "an ", "the "))
            or any(k in t for k in _NOT_A_NAME))

# Surnames this archive already holds, used ONLY to detect the Italian index's
# SURNAME-FIRST order. THE THRESHOLD IS THE WHOLE POINT: a first attempt took
# every surname in people.json and the fix did not fire, because CARMELA had
# ALREADY become a "known surname" there, from this very bug. A mis-parse that
# teaches the detector its own mistake cannot be detected by it. Requiring
# several bearers breaks the loop — FALCO has hundreds, CARMELA had one.
def _known(min_bearers=5):
    import json as _j, os as _o, collections as _c
    d = _o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))),
                     "site", "src", "data")
    c = _c.Counter()
    p = _o.path.join(d, "people.json")
    if _o.path.exists(p):
        for x in _j.load(open(p, encoding="utf-8")):
            v = (x.get("surname") or "").strip().upper()
            if v and v != "?" and " " not in v:
                c[v] += 1
    return {k for k, n in c.items() if n >= min_bearers}
KNOWN_SURNAMES = _known()

def sur(n):
    if is_description(n):
        return "?"
    parts = _clean(n)
    if not parts:
        return "?"
    # A single word left over is a forename with the surname unrecorded —
    # "Maria —", "Antonio —". Filing those under MARIA and ANTONIO invented a
    # surname the register never gave, so they are marked unknown instead.
    if len(parts) == 1:
        return "?"
    last = parts[-1].upper()
    # "di Lucia", "de' Rosa", "d'Ambrosio" are one surname, not a particle
    # plus a name.
    if len(parts) > 1 and parts[-2].lower() in PARTICLES:
        last = (parts[-2] + " " + parts[-1]).upper()

    # THE ITALIAN INDEX WRITES THE SURNAME FIRST. Entries copied verbatim out of
    # a tavola read "FALCO CARMELA", and taking the last word filed sixteen
    # people under CARMELA, CLEMENTE, ANTONIO and COSTANZA — so a search for
    # FALCO did not return them. If the FIRST word is a well-attested surname
    # and the last is not, the index's order is the right one.
    first = parts[0].upper()
    if len(parts) > 1 and first in KNOWN_SURNAMES and last not in KNOWN_SURNAMES:
        return first
    return last or "?"


AN = "https://antenati.cultura.gov.it/ark:/12657/"
def fs(ark):
    ark = (ark or "").strip()
    if not ark: return ""
    if ark.startswith("3Q9M") or ark.count("-") >= 2:
        return "https://www.familysearch.org/ark:/61903/3:1:" + ark
    if re.fullmatch(r"[A-Z0-9]{4}-[A-Z0-9]{3,4}", ark):
        return "https://www.familysearch.org/ark:/61903/1:1:" + ark
    return ""

def rd(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

# --- Antenati name-index harvests: the two biggest seams ---
for path, place_col in [("data/antenati-valle-caudina.tsv", "town"),
                        ("data/antenati-zampiello-annecchino.tsv", "place")]:
    for r in rd(path):
        nm = r.get("name") or ""
        if not nm: continue
        bits = []
        if r.get("acttype"): bits.append(r["acttype"])
        if r.get("actdate") or r.get("birthdate"): bits.append(r.get("actdate") or r.get("birthdate"))
        if r.get(place_col): bits.append(r[place_col])
        rel = " · ".join(x for x in [r.get("father"), r.get("mother")] if x)
        if rel: bits.append("parents: " + rel)
        if r.get("child"): bits.append("child: " + r["child"])
        ark = (r.get("ark") or "").strip()
        # A source file's own surname column is trusted only when it looks
        # like a surname. One row arrived as "(B." — the head of "(b. 8 Jun
        # 1930)" — and filed a direct-line marriage under a bracket.
        given = (r.get("surname") or "").strip()
        if not re.fullmatch(r"[A-Za-zÀ-ÿ' ]{2,}", given):
            given = ""
        # This is the Antenati PORTAL harvest (the register search), not the
        # /search-nominative/ name index loaded further down. The two were both
        # labelled "Antenati name index" and mean different things: this one
        # carries an act and sometimes a parent, that one always carries parents.
        add(nm, given or sur(nm), " · ".join(bits),
            "Antenati portal harvest", AN + ark if ark.startswith("an_") else "", "index",
            r.get("actdate") or r.get("birthdate") or "")

# --- FamilySearch structured harvests ---
for r in rd("data/zampiello-arpaia.tsv"):
    rel = (r.get("related") or "").replace("|", " · ")
    add(r.get("principal"), sur(r.get("principal")),
        " · ".join(x for x in [r.get("date"), r.get("place"), ("with " + rel) if rel else ""] if x),
        "FamilySearch, Arpaia", fs(r.get("ark")), "record", r.get("date") or "")
# --- Benevento civil registration, harvested from FamilySearch 10 Sep 2026 ---
# 962 Annecchino from Italy, Benevento, Civil Registration (State Archive) 1810-1942,
# collection 2475030. No per-row ark was captured, so these carry a source but no link:
# they are evidence with a citable collection, not one-click documents.
def _split4(path):
    out = []
    with open(path) as f:
        head = f.readline().rstrip("\n").split("\t")
        for ln in f:
            parts = ln.rstrip("\n").split("\t")
            if len(parts) == len(head):
                out.append(dict(zip(head, parts)))
    return out

for r in _split4("data/annecchino-benevento-fs.tsv"):
    nm = r.get("name") or ""
    bits = [x for x in [r.get("birthdate"), r.get("place")] if x]
    par = (r.get("parents") or "").replace(" ; ", " · ")
    if par: bits.append("parents: " + par)
    add(nm, sur(nm), " · ".join(bits),
        "FamilySearch — Benevento Civil Registration (State Archive) 1810–1942", "",
        "index", r.get("birthdate") or "")

for r in rd("data/annecchino-forchia.tsv"):
    add(r.get("child"), sur(r.get("child")),
        " · ".join(x for x in [r.get("date"), r.get("place"),
                   "parents: " + " · ".join(y for y in [r.get("father"), r.get("mother")] if y)] if x),
        "FamilySearch, Forchia", fs(r.get("ark")), "record", r.get("date") or "")

# --- The archive's own citations ---
for r in rd("data/record-citations.tsv"):
    ark = (r.get("ark") or "").strip()
    link = AN + re.search(r"an_ua\d+", ark).group(0) if "an_ua" in ark else fs(ark.split()[0] if ark else "")
    add(r.get("subject"), sur(r.get("subject")),
        " · ".join(x for x in [r.get("event"), r.get("date"), r.get("place"),
                               r.get("father_or_spouse")] if x),
        r.get("collection") or "", link, "cited", r.get("date") or "")

# --- Arienzo parish books, opened 13 Sep 2026 ---
# The civil registers begin in 1809. Everything before that — and every child who
# died before one — lives only here. Rows carry READ: "image" means the handwriting
# itself was read at magnification; "transcription" means FamilySearch's
# handwriting-recognition only, which has already been caught turning 1802 into
# 1902. The distinction is published on the row, not buried in a note.
for r in rd("data/arienzo-parish-acts.tsv"):
    read = (r.get("read") or "").strip()
    mark = "READ FROM THE IMAGE" if read == "image" else "machine transcription — unverified"
    ev = (r.get("event") or "").strip()
    parents = " & ".join(x for x in [r.get("father"), r.get("mother")] if x)
    common = [r.get("date"), r.get("place"), r.get("priest")]
    # the principal
    bits = [ev, r.get("date"), r.get("place")]
    if r.get("spouse"): bits.append("m. " + r["spouse"])
    if parents: bits.append("of " + parents)
    for x in (r.get("priest"), r.get("others"), r.get("note")):
        if x: bits.append(x)
    bits.append(mark)
    link = fs(r.get("ark"))
    add(r.get("principal"), sur(r.get("principal")), " · ".join(x for x in bits if x),
        "Arienzo parish registers (FamilySearch)", link, "parish", r.get("date") or "")
    # everyone else the act names, so they are findable by their own name
    for role, who in [("father of", r.get("father")), ("mother of", r.get("mother")),
                      ("married", r.get("spouse"))]:
        if not who: continue
        add(who, sur(who), " · ".join(x for x in
            [role + " " + (r.get("principal") or ""), ev, r.get("date"), r.get("place"), mark] if x),
            "Arienzo parish registers (FamilySearch)", link, "parish", r.get("date") or "")

# --- Arienzo death-register INDEXES (tavole alfabetiche) ---------------------
# The year's own alphabetical table names the parents, which the acts would take
# a full reading to yield. One page per year instead of sixty-eight.
for r in rd("data/arienzo-deaths-1859-index.tsv"):
    who = (r.get("name") or "").strip()
    if not who:
        continue
    par = " & ".join(x for x in [r.get("father"), r.get("mother")] if x)
    bits = ["died " + (r.get("date") or ""), r.get("profession"), r.get("patria"),
            ("of " + par) if par else None,
            f"act {r.get('act')}",
            "read from the year's TAVOLA ALFABETICA, not from the act"]
    add(who, sur(who), " · ".join(x for x in bits if x),
        f"Arienzo Morti {r.get('year')} — tavola alfabetica (Antenati)",
        AN + (r.get("ark") or ""), "index", r.get("date") or "")

# --- Antenati's NAME index (Benevento province) ------------------------------
# `/search-nominative/` gives the person AND their parents, which the register
# search does not. It covers Forchia and Arpaia; it does NOT cover Arienzo —
# "Nessun risultato trovato … solo una parte dei registri è stata indicizzata".
import glob as _glob
for _f in sorted(_glob.glob("data/antenati-names-*.tsv")):
    _town = _f.rsplit("-", 1)[-1].replace(".tsv", "").title()
    for r in rd(_f):
        nm = (r.get("name") or "").strip()
        if not nm or is_description(nm):
            continue
        bits = []
        info = (r.get("info") or "").strip()
        if info: bits.append(info)
        rel = (r.get("rel") or "").replace("=", " ").replace(" ; ", " · ")
        if rel: bits.append(rel)
        acts = [a for a in (r.get("acts") or "").split(" ; ") if a]
        ark = ""
        for a in acts:
            parts = a.split("|")
            if len(parts) == 3:
                bits.append(parts[0] + (" " + parts[1] if parts[1] and "senza data" not in parts[1] else ""))
                ark = ark or parts[2]
        bits.append("INDEX ENTRY — the act itself is not read")
        add(nm, sur(nm), " · ".join(x for x in bits if x),
            f"Antenati name index (with parents) — {_town}", AN + ark if ark else "", "index",
            (re.search(r"\b(1[789]\d\d)\b", info + " " + (r.get("acts") or "")) or [""])[0] if re.search(r"\b(1[789]\d\d)\b", info + " " + (r.get("acts") or "")) else "")

# --- Arienzo civil marriage acts, 1843-1844 -----------------------------------
# Read out act by act looking for generation four's civil marriage, which is NOT
# in either volume. The people the search passed over are published anyway: a
# marriage act names both spouses with age, trade and street, and four parents
# besides, and none of that becomes less true because the act was not the one
# being hunted. Rows whose names could not be read carry NOT SECURELY READ and
# are not given a person of their own.
for r in rd("data/arienzo-civil-marriages-1843-1844.tsv"):
    ark = (r.get("ark") or "").strip()
    img = (r.get("image") or "").strip()
    link = "https://antenati.cultura.gov.it/ark:/12657/" + ark if ark else ""
    where = f"Arienzo civil marriages {r.get('year')}, act {r.get('act')}, image {img}"
    when = r.get("date") or ""
    def status(n):
        """In THIS source maggiore/minore are of-age/under-age, not a surname."""
        m = re.search(r"\b(maggiore|minore)\b\s*$", (n or "").strip(), re.I)
        return (re.sub(r"\s*\b(maggiore|minore)\b\s*$", "", n or "", flags=re.I).strip(),
                m.group(1).lower() if m else None)

    for who, detail, role in ((r.get("groom"), r.get("groom_detail"), "married"),
                              (r.get("bride"), r.get("bride_detail"), "married")):
        if not who or "NOT SECURELY READ" in who:
            continue
        other = r.get("bride") if who == r.get("groom") else r.get("groom")
        other, _ = status(other)
        who, st = status(who)
        bits = ["civil marriage act", when,
                (role + " " + other) if other and "NOT SECURELY" not in other else None,
                detail, ("«" + st + "» — of age" if st == "maggiore" else
                         "«minore» — under age" if st else None),
                "READ FROM THE IMAGE"]
        add(who, sur(who), " · ".join(x for x in bits if x), where, link, "civil", when)

# --- Australia ---
for r in rd("data/nudgee-burials.tsv"):
    nm = f"{r.get('given','')} {r.get('surname','')}".strip()
    add(nm, sur(nm), " · ".join(x for x in ["buried " + (r.get("interred") or ""),
        r.get("location"), r.get("cemetery"), r.get("identification")] if x),
        "Nudgee Cemetery", "", "burial", r.get("interred") or "")
# Queensland's own historical index, swept by surname in September 2026. The
# rows that are this family are marked «ours» in the TSV; the rest are carried
# too, because a Falco who is NOT ours is a name somebody would otherwise
# search a second time. The registration number is the point: it is what makes
# a certificate orderable, and the archive had none for the Brisbane deaths.
for r in rd("data/qld-bdm.tsv"):
    nm = f"{r.get('given','')} {r.get('surname','')}".strip()
    verdict = (r.get("verdict") or "").strip()
    parents = " & ".join(x for x in [r.get("father"), r.get("mother")] if x)
    bits = [(r.get("type") or "") + " registration " + (r.get("event_date") or ""),
            "registration " + r["reg"] if r.get("reg") else None,
            "born " + r["born"] if r.get("born") else None,
            "parents " + parents if parents else None,
            "spouse " + r["other_party"] if r.get("other_party") else None,
            None if verdict == "ours" else f"«{verdict}»",
            r.get("identification")]
    add(nm, sur(nm), " · ".join(x for x in bits if x),
        "Queensland BDM historical index", r.get("url") or "", "index",
        r.get("event_date") or "")

for r in rd("data/naa-records.tsv"):
    t = r.get("title") or ""
    link = ("https://recordsearch.naa.gov.au/SearchNRetrieve/Interface/DetailsReports/ItemDetail.aspx?Barcode="
            + (r.get("item_id") or "")) if r.get("item_id") else ""
    add(t.split(";")[0].replace("Falco, ", "").strip() or t, sur(t.split(",")[0]),
        " · ".join(x for x in [r.get("series", "") + " " + (r.get("control_symbol") or ""),
                               r.get("date_range"), r.get("location"), r.get("access")] if x),
        "National Archives of Australia", link, "file", r.get("date_range") or "")

# --- the family tree itself: every DECEASED person on the Falco side ---
# Living people are excluded entirely, as everywhere else in this build.
if os.path.exists("data/myheritage-falco-tree.json"):
    tree = json.load(open("data/myheritage-falco-tree.json"))
    for x in tree:
        if x.get("alive"): continue
        nm = re.sub(r"\s*[✔⭐]\s*", " ", x.get("name") or "").strip(" ,")
        if not nm or nm.startswith("["): continue
        bits = []
        if x.get("b"):  bits.append("b. " + x["b"] + (", " + x["bp"] if x.get("bp") else ""))
        elif x.get("bp"): bits.append("of " + x["bp"])
        if x.get("d"):  bits.append("d. " + x["d"] + (", " + x["dp"] if x.get("dp") else ""))
        rels = [f'{r["rel"]} {r["n"]}' for r in (x.get("relatives") or [])][:4]
        if rels: bits.append(" · ".join(rels))
        add(nm, sur(re.sub(r"\(.*?\)", "", nm)), " · ".join(bits),
            "The family tree (unverified unless a record is cited)", "", "tree",
            x.get("b") or "")

# --- everyone read act-by-act in the 1834 death-register sweep ---
if os.path.exists("data/sweep-people.tsv"):
    for r in rd("data/sweep-people.tsv"):
        # The sweep's name column sometimes holds a note about the LEAF rather
        # than a person — "A blank leaf, photographed at an angle. Not an act",
        # "The volume's own INDEX … Not an act". Those were being published as
        # people with an unknown surname. The observation is worth keeping; a
        # person page for it is not.
        if is_description(r["name"]):
            continue
        add(r["name"], sur(r["name"]),
            " · ".join(x for x in [(r["age"] if r["age"] not in ("", "—") else ""),
                                   r["detail"]] if x),
            f'Arienzo death register {r["year"]}, image {r["img"]}{r["side"]}',
            AN + r["ark"] if r["ark"] else "", "swept", r["year"])

# --- the reconstructed households (already have full pages) ---
hh = json.load(open("site/src/data/households.json"))
for h in hh:
    for m in h["members"]:
        ark = (m.get("ark") or "").strip()
        link = AN + re.search(r"an_ua\d+", ark).group(0) if "an_ua" in ark else fs(ark)
        add(m["person"], sur(m["person"]),
            " · ".join(x for x in [m.get("role"), m.get("event"), m.get("date"),
                                   m.get("place"), h["name"]] if x and x != "—"),
            "Reconstructed household", link, "household", m.get("date") or "")

# de-duplicate identical rows
seen, out = set(), []
for r in ROWS:
    k = (r["name"].lower(), r["detail"][:70].lower(), r["source"])
    if k in seen: continue
    seen.add(k); out.append(r)

out.sort(key=lambda r: (r["surname"], r["name"].lower(), r["sort"]))
with open("data/people-register.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, delimiter="\t", fieldnames=["surname","name","detail","source","link","kind"])
    w.writeheader()
    for r in out: w.writerow({k: r[k] for k in w.fieldnames})
json.dump(out, open("site/src/data/register.json", "w"), ensure_ascii=False)

names = {r["name"].lower() for r in out}
print(f"register rows : {len(out)}")
print(f"distinct names: {len(names)}")
print(f"with a link   : {sum(1 for r in out if r['link'])}")
c = collections.Counter(r["surname"] for r in out)
print("top surnames  :", ", ".join(f"{k} {v}" for k, v in c.most_common(10)))
