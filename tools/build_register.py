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
TRADES = {
    "contadino", "contadina", "colono", "colona", "vaticale", "possidente", "proprietario",
    "proprietaria", "sartore", "sarto", "sarta", "calzolajo", "calzolaio", "barbiere",
    "macellajo", "macellaio", "ferraro", "fabbro", "oste", "locandiere", "bottegajo",
    "bottegaio", "panettiere", "pastaio", "pastajo", "filatrice", "tessitrice", "massaro",
    "guarniciere", "guarnitore", "ortolano", "pettinatore", "cappellaio", "cappellajo",
    "sportaro", "vinivendolo", "rivenditore", "rivendugliolo", "serviente", "gentildonna",
    "gentiluomo", "monaca", "conversa", "arciprete", "sacerdote", "notaro", "notaio",
    "corattiere", "recimaro", "recimatore", "vaticaro", "gabelloto", "pizzajolo",
    "defunto", "defunta", "vedovo", "vedova", "regnicolo", "regnicola",
}

def _clean(n):
    """Drop trailing trade/descriptor words so the surname is the surname."""
    n = re.sub(r"\s+", " ", (n or "").strip())
    n = re.sub(r"[,;]\s*$", "", n)
    parts = [p for p in n.split(" ") if p and p.strip(",.;·—-")]
    while len(parts) > 1 and parts[-1].strip(",.;").lower() in TRADES:
        parts.pop()
    if parts:
        parts[-1] = parts[-1].rstrip(",;")
    return parts

def sur(n):
    parts = _clean(n)
    if not parts: return "?"
    last = parts[-1].upper()
    # "di Lucia", "de Guida", "d'Ambrosio" are one surname, not a particle plus a name.
    if len(parts) > 1 and parts[-2].lower() in {"di", "de", "del", "della", "lo", "la"}:
        last = (parts[-2] + " " + parts[-1]).upper()
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
        add(nm, r.get("surname") or sur(nm), " · ".join(bits),
            "Antenati name index", AN + ark if ark.startswith("an_") else "", "index",
            r.get("actdate") or r.get("birthdate") or "")

# --- FamilySearch structured harvests ---
for r in rd("data/zampiello-arpaia.tsv"):
    rel = (r.get("related") or "").replace("|", " · ")
    add(r.get("principal"), sur(r.get("principal")),
        " · ".join(x for x in [r.get("date"), r.get("place"), ("with " + rel) if rel else ""] if x),
        "FamilySearch, Arpaia", fs(r.get("ark")), "record", r.get("date") or "")
for r in rd("data/annecchino-forchia.tsv"):
    add(r.get("child"), sur(r.get("child")),
        " · ".join(x for x in [r.get("date"), r.get("place"),
                   "parents: " + " · ".join(y for y in [r.get("father"), r.get("mother")] if y)] if x),
        "FamilySearch, Forchia", fs(r.get("ark")), "record", r.get("date") or "")

# --- The archive's own citations ---
for r in rd("data/record-citations.tsv"):
    ark = (r.get("ark") or "").strip()
    link = AN + re.search(r"an_ua\d+", ark).group(0) if "an_ua" in ark else fs(ark.split()[0] if ark else "")
    add(r.get("subject"), sur(re.split(r",| \d", r.get("subject") or "")[0]),
        " · ".join(x for x in [r.get("event"), r.get("date"), r.get("place"),
                               r.get("father_or_spouse")] if x),
        r.get("collection") or "", link, "cited", r.get("date") or "")

# --- Australia ---
for r in rd("data/nudgee-burials.tsv"):
    nm = f"{r.get('given','')} {r.get('surname','')}".strip()
    add(nm, sur(nm), " · ".join(x for x in ["buried " + (r.get("interred") or ""),
        r.get("location"), r.get("cemetery"), r.get("identification")] if x),
        "Nudgee Cemetery", "", "burial", r.get("interred") or "")
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
