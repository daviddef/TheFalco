#!/usr/bin/env python3
"""The records table: where a citation on a page can be followed to the record. Made from this archive's own data, and nothing else.

    python3 tools/build_records.py            # writes site/src/data/records.json
    python3 tools/build_records.py --check    # exits 1 when the file is not what the data says (the build runs this)

The kit's <Rec> (kit/components/Rec.astro; this archive wraps it once, site/src/components/Rec.astro) draws the SAME WORDS an author
already wrote as a link to the record they cite (the linking standard's L3), and, where the archive may show the scan and the author
asks for it (`thumb`), a small figure of it (L4). It reads this table, row by row, and stops the build on an id it does not hold: a
link that is a guess is worse than no link.

WHAT IS IN IT (every row carries a `kind`; every address is one the archive already holds, or one it builds from an ark and a
barcode it holds in the same way the rest of the site does):

  ark            an Antenati VOLUME: one row for every manifest in data/antenati-ids/ (385), id = the ark ("an_ua14336"), url
                 https://antenati.cultura.gov.it/ark:/12657/<ark>/. A link goes to the volume's landing page, never to an image
                 (an image deep link does not survive Antenati's viewer; the site's <Src ark> chip has always linked the volume).
                 The label says what the archive's own data says the volume is: «Arienzo, Morti 1834» where data/households.tsv,
                 plates.json or register.json name the series and year beside the ark and agree, «Arienzo, 1834» (the manifest's own
                 label) where nothing does, or two series claim one ark. The ark rows carry `series` and `year` so tools/check_records.py
                 can hold a citation's words to them.
  plate          a scan the archive publishes (site/src/data/plates.json): id = the file's stem. Its address is the Antenati volume
                 its `cite` names where it names one, else its own entry on /documents/. `plate` and `show` (true only for an
                 Antenati register plate or a marriage-file plate, which /documents/ and /gallery/ show already) let a page place the
                 scan beside the passage; `key` is the act it is the scan of (site/src/data/plate-keys.json).
  naa            a National Archives of Australia item the archive holds an address for (register.json, searched.json). LINK-ONLY.

NOT IN IT, on purpose: FamilySearch frames and Matricula images (link-only everywhere, and nothing on the 12 narratives needs one),
an act inside a volume (Antenati's viewer does not keep a deep link), any record the data gives no address for (a Neptunia
passenger list known only by its barcode: the passage stays plain text and is counted by the gate), and any row about a living
person: where the private living list exists (the machine with the tree) a row whose label contains a name on it is NOT WRITTEN
(the kit's <Rec> draws nothing for a row flagged living or hold, so such a row is kept out of the table altogether, and a passage
about such a person keeps its text plain by hand). A runner has no living list, so --check there accepts a committed table that
lacks rows the runner would generate, and nothing else: every committed row must be exactly what the data says.
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
SRC = os.path.join(ROOT, "site", "src", "data")
OUT = os.path.join(SRC, "records.json")
LIVING = os.path.join(ROOT, "private", "living-links.json")

SERIES = {"nati": "Nati", "morti": "Morti", "matrimoni": "Matrimoni", "processetti": "Processetti", "diversi": "Diversi"}
ARK = re.compile(r"an_ua\d+")
HOST = "https://antenati.cultura.gov.it/ark:/12657/%s/"


def series_of(word):
    w = word.lower()
    return SERIES.get(w) or ("Processetti" if w.startswith("processetti") else None)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


P1 = re.compile(r"(Nati|Morti|Matrimoni)\s+(\d{4})\b[^()`\n]{0,70}?[(`]+\s*(?:Antenati\s+)?(an_ua\d+)")
P2 = re.compile(r"(an_ua\d+)`?\s*\((?:[A-Z][^,)]*),\s*(?:Stato civile [a-z ]*,\s*)?(Nati|Morti|Matrimoni|Processetti|PROCESSETTI|Diversi) (\d{4})\)")
P3 = re.compile(r"(an_ua\d+)`?\s*\((?:[A-Z][^,)]*?)\s+(processetti|PROCESSETTI) (\d{4})\)")
FACT_FILES = ["plates.json", "register.json", "people.json", "households.json", "searched.json", "worklist.json", "corrections.json", "changes.json"]


def facts():
    """ark -> {(series, year)}: wherever the archive's own data names the series and the year right beside the ark, in one of
    three fixed shapes («Morti 1834 ... (Antenati an_ua14336», «an_ua14427 (Arienzo, Nati 1830)», «an_ua14207 (Arienzo
    processetti 1860)»). Nothing is inferred from an ark's number or from the year alone."""
    out = {}

    def add(ark, series, year):
        s = series_of(series)
        if s and ark:
            out.setdefault(ark, set()).add((s, year))

    texts = []
    for p in sorted(glob.glob(os.path.join(DATA, "*.tsv"))):
        texts.append(open(p, encoding="utf-8").read())
    for fn in FACT_FILES:
        texts.append(open(os.path.join(SRC, fn), encoding="utf-8").read())
    for t in texts:
        t = t.replace("\\n", "\n").replace("\\u2014", "-")
        for m in P1.finditer(t):
            add(m.group(3), m.group(1), m.group(2))
        for m in P2.finditer(t):
            add(m.group(1), m.group(2), m.group(3))
        for m in P3.finditer(t):
            add(m.group(1), m.group(2), m.group(3))
    return out


def town_of(label):
    parts = [x.strip() for x in label.split(">")]
    town = parts[-2] if len(parts) >= 2 else ""
    town = re.sub(r"\(oggi ([^)]*)\)", r"(\1)", town)
    town = re.sub(r"San Felice\s*\(San Felice a Cancello\)", "San Felice a Cancello", town)
    return town, parts[-1] if parts else "", parts[0] if parts else ""


def volume_rows(fx):
    rows, mixed = [], 0
    for p in sorted(glob.glob(os.path.join(DATA, "antenati-ids", "an_ua*.json"))):
        d = load(p)
        ark = d["ark"]
        if not ARK.fullmatch(ark):
            continue
        town, years, arch = town_of(d.get("label", ""))
        archive = re.sub(r"^Archivio di Stato di ", "", arch)
        f = fx.get(ark, set())
        row = {"id": ark, "url": HOST % ark, "kind": "ark", "year": years}
        if len(f) == 1:
            s, y = next(iter(f))
            row["series"] = s
            row["label"] = "%s, %s %s (Antenati %s)" % (town, s, y, ark)
            row["year"] = y
        else:
            if len(f) > 1:
                mixed += 1
            row["label"] = "%s, %s (Antenati %s)" % (town, years, ark)
        row["label"] += " — Archivio di Stato di %s" % archive if archive else ""
        rows.append(row)
    return rows, mixed


REG_WORD = {"death": "Morti", "birth": "Nati", "marriage": "Matrimoni"}


def plate_rows(vols, naa):
    """One row per plate. Its address, in this order: the Antenati volume its `cite` names; the NAA item or image its `cite` names
    when the archive holds an address for it; the one Arienzo volume of that series and year the archive's data names («Arienzo civil
    death register 1842» -> Morti 1842) when there is exactly one; else the plate's own entry on /documents/."""
    plates = load(os.path.join(SRC, "plates.json"))
    keys = load(os.path.join(SRC, "plate-keys.json"))
    vol_ids = {v["id"] for v in vols}
    by_sy = {}
    for v in vols:
        if v.get("series") and v["label"].startswith("Arienzo,"):
            by_sy.setdefault((v["series"], v["year"]), set()).add(v["id"])
    naa_ids = {n["id"] for n in naa}
    rows, used = [], set()
    for p in plates:
        stem = os.path.splitext(p["f"])[0]
        cite = str(p.get("cite") or "")
        row = {"id": stem, "kind": "plate", "label": re.sub(r"\s+", " ", str(p.get("t") or stem)).strip(), "plate": p["f"]}
        m = re.search(r"Antenati (an_ua\d+)", cite)
        nb = re.search(r"(?:barcode|item) (\d{6,9})(?:, image (\d+))?", cite)
        cv = re.search(r"Arienzo civil (death|birth|marriage) register (\d{4})", str(p.get("c") or ""))
        row["url"] = "/documents/#" + stem
        row["show"] = False
        if m and m.group(1) in vol_ids:
            row["url"] = HOST % m.group(1)
            row["volume"] = m.group(1)
            row["show"] = p.get("k") in ("register", "processetto")
        elif nb and nb.group(1) and any(i.startswith("naa-" + nb.group(1)) for i in naa_ids):
            img = "naa-%s-image-%s" % (nb.group(1), nb.group(2)) if nb.group(2) else None
            pick = img if img in naa_ids else "naa-" + nb.group(1)
            if pick in naa_ids:
                row["url"] = next(n["url"] for n in naa if n["id"] == pick)
                row["naa"] = pick
        elif cv and len(by_sy.get((REG_WORD[cv.group(1)], cv.group(2)), ())) == 1:
            ark = next(iter(by_sy[(REG_WORD[cv.group(1)], cv.group(2))]))
            row["url"] = HOST % ark
            row["volume"] = ark
            row["show"] = p.get("k") in ("register", "processetto") or p.get("k") is None
        ks = [k for k in keys.get(stem, []) if k not in used]
        if ks:
            row["key"] = ks
            used.update(ks)
        rows.append(row)
    return rows


def naa_rows():
    rows = []
    for r in load(os.path.join(SRC, "register.json")):
        m = re.search(r"https://recordsearch\.naa\.gov\.au/SearchNRetrieve/Interface/DetailsReports/ItemDetail\.aspx\?Barcode=(\d+)", str(r.get("link") or ""))
        if m and str(r.get("detail") or "").startswith("K269"):
            ctl = str(r["detail"]).split(" · ")[0]
            rows.append({"id": "naa-" + m.group(1), "kind": "naa", "url": m.group(0), "label": "National Archives of Australia, %s (item %s)" % (ctl, m.group(1))})
    # a view-image address the searches hold for a barcode
    txt = open(os.path.join(SRC, "searched.json"), encoding="utf-8").read()
    for m in re.finditer(r"https://recordsearch\.naa\.gov\.au/SearchNRetrieve/Interface/ViewImage\.aspx\?B=(\d+)&S=(\d+)", txt):
        rows.append({"id": "naa-%s-image-%s" % (m.group(1), m.group(2)), "kind": "naa", "url": m.group(0),
                     "label": "National Archives of Australia, image %s of item %s" % (m.group(2), m.group(1))})
    seen, out = set(), []
    for r in rows:
        if r["id"] not in seen:
            seen.add(r["id"])
            out.append(r)
    return out


def living_terms():
    if not os.path.exists(LIVING):
        return None
    return {re.sub(r"\s+", " ", x).casefold() for x in load(LIVING) if not x.startswith("/")}


def build():
    fx = facts()
    vols, mixed = volume_rows(fx)
    naa = naa_rows()
    rows = vols + plate_rows(vols, naa) + naa
    live = living_terms()
    held = 0
    if live is not None:
        keep = []
        for r in rows:
            lab = " " + re.sub(r"[^\w']+", " ", r["label"]).casefold() + " "
            if any(" " + re.sub(r"[^\w']+", " ", n) + " " in lab for n in live):
                held += 1
            else:
                keep.append(r)
        rows = keep
    rows.sort(key=lambda r: (r["kind"], r["id"]))
    return {"records": rows}, {"volumes": len(vols), "series known": sum(1 for r in vols if "series" in r), "ark with conflicting facts": mixed,
                               "plates": sum(1 for r in rows if r["kind"] == "plate"), "naa": sum(1 for r in rows if r["kind"] == "naa"),
                               "left out (a living name in the label)": held if live is not None else "not checked: no private living list here"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    table, st = build()
    text = json.dumps(table, ensure_ascii=False, indent=1) + "\n"
    if a.check:
        have = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"records": []}
        mine = {r["id"]: r for r in table["records"]}
        theirs = {r["id"]: r for r in have["records"]}
        wrong = [i for i in theirs if i not in mine or mine[i] != theirs[i]]
        extra = [i for i in mine if i not in theirs]
        if wrong or (extra and living_terms() is not None):
            print("build_records: FAIL, site/src/data/records.json is not what the data says (%d row(s) differ or are stale, %d missing): "
                  "run `python3 tools/build_records.py` and commit it" % (len(wrong), len(extra)))
            return 1
        print("build_records: ok, %d rows %s%s" % (len(have["records"]), st,
              "" if not extra else "; %d row(s) the data makes are not committed (held out by the living list on the machine with the tree)" % len(extra)))
        return 0
    open(OUT, "w", encoding="utf-8").write(text)
    print("build_records: wrote %s: %d rows %s" % (os.path.relpath(OUT, ROOT), len(table["records"]), st))
    return 0


if __name__ == "__main__":
    sys.exit(main())
