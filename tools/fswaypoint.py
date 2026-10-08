#!/usr/bin/env python3
"""Walk a FamilySearch BROWSE waypoint and list every image ark in it.

WHY THIS EXISTS, AND WHY IT IS NOT THE FULL-TEXT TOOL.

This archive spent weeks reaching Arienzo's 1866-1890 civil registers the hard
way — through certified copies quoted inside the marriage supplements of
1891-1910, two removes from the register — on a premise that turned out to be
wrong. The premise was: Antenati's year facet runs 1809-1865 and stops, and
FamilySearch's full-text search of collection 2043630 returns only 1891-1910
pages placed at Arienzo, therefore the registers of the missing years are lost.

**A FULL-TEXT SEARCH IS NOT A HOLDINGS LIST.** It reaches only the pages a
recogniser has processed. The browse tree is the holdings list, and it had
Arienzo's «Nati, matrimoni, morti 1866-1876» the whole time.

    https://api.familysearch.org/platform/records/waypoints/<WP>?cc=<COLL>

answers 200 to an ordinary identified request — **no cookie, no token, no
browser** — and returns up to 1000 image arks a page with `links.next` for the
rest. This is a different door from the tile host and from www.familysearch.org,
and it is not behind the security service that answers those with 403.

The arks it returns are DeepZoom arks: feed them to tools/fsgrab.py to read.

    python3 tools/fswaypoint.py MC55-FNT:349501401,954415201 --cc 2043630
    python3 tools/fswaypoint.py <WP> --cc <ID> --tsv data/some-index.tsv

POLITENESS. One request a second, single threaded, identified in the
User-Agent. Record Atlas harvests this same endpoint at that pace; there is
nothing here to work around and nothing is impersonated.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.familysearch.org/platform/records/waypoints"
UA = "FalcoFamilyArchive/1.0 (family history; volume index; github.com/daviddef/TheFalco)"
ARK = re.compile(r"ark:/61903/(3:1:[0-9A-Za-z-]+)")


def get(url, pause=1.0, tries=4):
    for attempt in range(tries):
        req = urllib.request.Request(
            url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                doc = json.load(r)
            time.sleep(pause)
            return doc
        except urllib.error.HTTPError as e:
            # Their server having a bad moment is not a reason to keep asking
            # at the same rate. A 403 here is NOT recorded as a negative by
            # anything downstream — it is a refusal, not an absence.
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(pause * (6 ** (attempt + 1)))
                continue
            sys.stderr.write(f"  HTTP {e.code} on {url}\n")
            return None
        except Exception as exc:
            if attempt < tries - 1:
                time.sleep(pause * 4)
                continue
            sys.stderr.write(f"  {exc} on {url}\n")
            return None
    return None


def title_of(doc):
    """The volume's own title, as the waypoint tree states it."""
    for sd in doc.get("sourceDescriptions", []):
        if sd.get("id") == "src_1":
            return (sd.get("titles") or [{}])[0].get("value", "").strip()
    return ""


def walk(wp, cc, pause=1.0):
    """Every image ark under one waypoint, in the order the film runs."""
    url = f"{API}/{urllib.parse.quote(wp, safe=':,')}?cc={cc}"
    arks, title, total = [], "", None
    while url:
        doc = get(url, pause)
        if doc is None:
            return arks, title, total, False
        if not title:
            title = title_of(doc)
        links = doc.get("links") or {}
        if total is None:
            total = ((links.get("self") or {}).get("results"))
        seen = set(arks)
        for sd in doc.get("sourceDescriptions", []):
            m = ARK.search(sd.get("about", "") or "")
            # The payload also describes the node, its ancestors and the
            # collection; only the image descriptions carry an ark.
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                arks.append(m.group(1))
        url = (links.get("next") or {}).get("href")
    return arks, title, total, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("waypoint", nargs="+", help="WP[:ancestors] — repeatable")
    ap.add_argument("--cc", required=True, help="collection id")
    ap.add_argument("--pause", type=float, default=1.0)
    ap.add_argument("--tsv", default="", help="write ark index here")
    ap.add_argument("--label", default="", help="place name for the tsv rows")
    args = ap.parse_args()

    rows = []
    for wp in args.waypoint:
        arks, title, total, complete = walk(wp, args.cc, args.pause)
        mark = "" if complete else "  ** INCOMPLETE — a request failed **"
        say = f"{len(arks)} ark(s)"
        if total is not None and total != len(arks):
            say += f" of {total} the API counts"
        print(f"  {wp.split(':')[0]:<12} {say:<28} {title[:70]}{mark}")
        for i, a in enumerate(arks, 1):
            rows.append((args.label or args.cc, wp.split(":")[0], str(i), a, title))

    if args.tsv:
        with open(args.tsv, "w", encoding="utf-8", newline="") as fh:
            fh.write("place\twaypoint\timage\tark\tvolume\n")
            for r in rows:
                fh.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
        print(f"  -> {args.tsv}  {len(rows)} row(s)")


if __name__ == "__main__":
    main()
