#!/usr/bin/env python3
"""Harvest Antenati's NAME index — the one that gives PARENTS.

    python3 tools/antenati_names.py Zampiello Arpaia out.tsv

`/search-nominative/?cognome=X&localita=Y&s_page=N` returns ten cards a page.
Each card is one PERSON with: the related people and how they relate (Figlio /
Padre / Madre / Coniuge), the act type, the act date and an `an_ud` ark.

Arienzo is NOT in this index — only part of the holdings are name-indexed, and
the Caserta napoleonic series is not among them. Forchia and Arpaia are.
"""
import re, sys, time, subprocess, html, os

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124"

def fetch(url, tries=6):
    """Antenati throttles the search endpoints hard, and CUMULATIVELY — a long
    session earns a block that short backoffs will not clear. Be patient."""
    for k in range(tries):
        r = subprocess.run(["curl","-s","--max-time","40","-A",UA,
                            "-H","Referer: https://antenati.cultura.gov.it/", url],
                           capture_output=True, text=True)
        if r.stdout and "search-item" in r.stdout:
            return r.stdout
        wait = [45, 90, 180, 300, 420, 600][k]
        print(f"  throttled, waiting {wait}s", file=sys.stderr)
        time.sleep(wait)
    return ""

def txt(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()

CARD = re.compile(r'<div class="search-item" data-id="(\d+)">(.*?)(?=<div class="search-item" data-id=|<div class="search-pagination)', re.S)

def parse(h):
    out = []
    for m in CARD.finditer(h):
        sid, body = m.group(1), m.group(2)
        nm = re.search(r'nominative-detail.*?<h3[^>]*>\s*<a[^>]*>(.*?)</a>', body, re.S)
        name = txt(nm.group(1)) if nm else ""
        # the "( Place, year - year )" line and Nascita/Morte lines
        info = " ".join(txt(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S))
        rels = []
        lk = re.search(r'nominative-links(.*?)(?=<div class="nominative-records"|<aside)', body, re.S)
        if lk:
            for li in re.findall(r'<li>(.*?)</li>', lk.group(1), re.S):
                role = txt(re.search(r'<h4[^>]*>(.*?)</h4>', li, re.S).group(1)) if re.search(r'<h4', li) else ""
                who = txt(re.sub(r'<h4[^>]*>.*?</h4>', '', li, flags=re.S))
                if who: rels.append(f"{role}={who}")
        acts = []
        rc = re.search(r'nominative-records(.*?)(?=<aside)', body, re.S)
        if rc:
            for li in re.findall(r'<li>(.*?)</li>', rc.group(1), re.S):
                ark = re.search(r'(an_u[dn]\d+)', li)
                kind = re.search(r'<strong>(.*?)</strong>', li, re.S)
                date = txt(re.sub(r'<strong>.*?</strong>', '', li, flags=re.S))
                acts.append(f"{txt(kind.group(1)) if kind else ''}|{date}|{ark.group(1) if ark else ''}")
        out.append({"sid": sid, "name": name, "info": info,
                    "rel": " ; ".join(rels), "acts": " ; ".join(acts)})
    return out

def write(dest, rows):
    with open(dest, "w", encoding="utf-8") as f:
        f.write("sid\tname\tinfo\trel\tacts\n")
        for r in rows:
            f.write("\t".join(r.get(k, "") for k in ("sid","name","info","rel","acts")) + "\n")

def main():
    sur, loc, dest = sys.argv[1], sys.argv[2], sys.argv[3]
    rows, page, total = [], 1, None
    # resume: keep whatever a previous run already wrote
    seen0 = set()
    if os.path.exists(dest):
        for ln in open(dest, encoding="utf-8").read().split("\n")[1:]:
            f = ln.split("\t")
            if len(f) >= 5:
                rows.append(dict(zip(("sid","name","info","rel","acts"), f)))
                seen0.add(f[0])
        if rows:
            page = len(rows) // 10 + 1
            print(f"resuming at page {page} with {len(rows)} rows", file=sys.stderr)
    while True:
        h = fetch(f"https://antenati.cultura.gov.it/search-nominative/"
                  f"?cognome={sur}&localita={loc}&s_page={page}")
        if not h:
            print(f"page {page}: throttled — stopping", file=sys.stderr); break
        if total is None:
            t = re.search(r'([\d.]+)\s*</?\w*>?\s*risultati', txt(h))
            total = t.group(1) if t else "?"
            print(f"{sur} at {loc}: {total} records", file=sys.stderr)
        got = parse(h)
        if not got: break
        fresh = [r for r in got if r["sid"] not in seen0]
        for r in fresh: seen0.add(r["sid"])
        rows += fresh
        write(dest, rows)                       # checkpoint every page
        print(f"  page {page}: +{len(fresh)} (total {len(rows)})", file=sys.stderr)
        if not fresh: break
        page += 1
        time.sleep(8)
        if page > 80: break
    write(dest, rows)
    print(f"{len(rows)} unique -> {dest}", file=sys.stderr)

main()
