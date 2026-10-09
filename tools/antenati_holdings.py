#!/usr/bin/env python3
"""What Antenati actually HOLDS for a town — from the year facet, not by probing.

The volume pages have always been reachable by ark; what was missing was a way
to learn WHICH arks exist. Guessing them by arithmetic is how San Felice a
Cancello was believed unavailable for five years, and probing them one at a time
is slow and inconclusive — a missing manifest tells you nothing about whether
the series ended or merely has a hole.

`/search-registry/` renders only ten results a page, but it leaves its Solr
query in an HTML comment, and that query asks for `facet.field=anni_is` with
`facet.limit=200`. The rendered page therefore contains EVERY YEAR the town has
for that record type, whether or not the ten shown include it. Reading the years
off the page is a complete answer in one request.

    python3 tools/antenati_holdings.py Arienzo
    python3 tools/antenati_holdings.py "Santa Maria a Vico" Morti

NOTE: this host rate-limits. A run of requests gets 403 on everything, including
the ark pages, and recovers after a few minutes — so the 403 means "wait", not
"blocked", and certainly not "the endpoint is gone". Spaced by a second here.
"""
import re, subprocess, sys, time, urllib.parse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
# THE KINDS ARE NOT GUESSABLE AND THIS LIST WAS WRONG FOR A MONTH.
#
# It read: ["Nati", "Matrimoni", "Morti", "Diversi", "Allegati", "Cittadinanze"].
# **«Allegati» is not a value Antenati uses.** Asking for it returns the facet's
# own empty answer — «1 years: 1703», the artefact year that appears in every
# query — and this archive read that as «the processetti are not online» for
# **Moiano, Paolisi and San Felice a Cancello**, three towns whose work-list
# rows have said «unexamined» ever since.
#
# **The real value is «Matrimoni, processetti», and all four towns have it.**
# So do a dozen others nobody was asking for: «Matrimoni, pubblicazioni»,
# «Nati, indice», «Morti, indice», «Matrimoni, indici decennali» — San Felice a
# Cancello alone offers thirty-four.
#
# So the kinds are READ OFF THE TOWN'S OWN PAGE rather than hard-coded, which
# is the same principle the rest of this file already follows: the page carries
# its Solr facet query in an HTML comment, and the rendered filters carry every
# `tipologia_ss` value that town actually has.
KINDS = ["Nati", "Matrimoni", "Morti", "Diversi", "Cittadinanze", "Matrimoni, processetti"]

def kinds_for(town):
    """Every tipologia this town actually has, from its own facet."""
    import html as _html
    h = fetch(town, None)
    vals = set()
    for m in re.finditer(r'tipologia_ss:(?:&quot;|")?([^"&<]{2,60})', h):
        v = _html.unescape(m.group(1)).strip().strip('"')
        if v and not v.startswith(("&", "tipolog")):
            vals.add(v)
    return sorted(vals)

def fetch(town, kind):
    q = {"localita": town}
    if kind:
        q["tipologia"] = kind
    url = "https://antenati.cultura.gov.it/search-registry/?" + urllib.parse.urlencode(q)
    out = subprocess.run(["curl", "-sSL", "--compressed", "--max-time", "45",
                          "-A", UA, "-H", "Referer: https://antenati.cultura.gov.it/", url],
                         capture_output=True)
    return out.stdout.decode("utf-8", "replace")

def report(town, kind):
    h = fetch(town, kind)
    if "403 Forbidden" in h[:400]:
        print(f"  {kind or 'ALL':14} 403 — rate limited, wait a few minutes and retry")
        return
    years = sorted({int(y) for y in re.findall(r"\b(1[6-9]\d\d)\b", h)})
    arks = sorted({int(a) for a in re.findall(r"an_ua(\d+)", h)})
    if not years:
        print(f"  {kind or 'ALL':14} nothing")
        return
    # contiguous runs, so a gap in the middle is visible rather than averaged away
    runs, start, prev = [], years[0], years[0]
    for y in years[1:]:
        if y != prev + 1:
            runs.append((start, prev)); start = y
        prev = y
    runs.append((start, prev))
    span = ", ".join(f"{a}" if a == b else f"{a}–{b}" for a, b in runs)
    print(f"  {kind or 'ALL':14} {len(years):3} years: {span}")
    if arks:
        print(f"  {'':14}     first ark an_ua{arks[0]}, last an_ua{arks[-1]} (of the ten shown)")

def main():
    town = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    kinds = sys.argv[2:]
    if not kinds:
        kinds = kinds_for(town) or KINDS
        print(f"  (the town's own facet offers {len(kinds)} record type(s))")
    print(f"ANTENATI HOLDINGS — {town}")
    for k in kinds:
        report(town, k)
        time.sleep(1.2)

if __name__ == "__main__":
    main()
