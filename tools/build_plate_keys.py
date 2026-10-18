#!/usr/bin/env python3
"""Which register act each plate is the scan of: site/src/data/plate-keys.json, for the linking standard's L4.

    python3 tools/build_plate_keys.py            # writes site/src/data/plate-keys.json
    python3 tools/build_plate_keys.py --check    # exits 1 when the file is not what the plates say (the build runs this)

Falco's plate files carry no act number (`pasquale-falco-death-1834.jpg`), so the standard's gate (kit checkstandard.py,
`scans.aliases_file` in site/standard.json) cannot read "1834, atto 69" off the image's name. The act is in the plate's own
citation (site/src/data/plates.json `cite`, or the caption `c` where `cite` is empty): "... Morti 1834, atto 69 ...". This reads it
from there and from nowhere else. A plate whose text gives no year and act number gets no key (a family photograph, a passport,
a passenger list): it is not a scan of an act, and L4 asks nothing of it.

The key is `YEAR-ACT` ("1834-69"). The register's series (Nati, Morti, Matrimoni) is not part of it, because the prose that cites an
act does not always name the series; the cost is that act 69 of 1834 in two series would share a key, and no plate does today
(the check below says so and fails if two plates of different series claim one key).

A key is written only if the year and act number are both in the plate's text. Nothing is guessed from a file name.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLATES = os.path.join(ROOT, "site", "src", "data", "plates.json")
OUT = os.path.join(ROOT, "site", "src", "data", "plate-keys.json")

# "Morti 1834, atto 69", "death register 1840, atto 50", "Nati 1816, atto 56", "Morti 1825, atti 30 and 5"
ACT = re.compile(r"\b(?P<y>1[6-9]\d\d)\b[^.;()]{0,60}?\batt[oi]\s+(?P<n>\d+)(?:\s+and\s+(?P<n2>\d+))?", re.I)
ACT2 = re.compile(r"\bact\s+(?:no\.\s*)?(?P<n>\d+)\b", re.I)
YEAR_IN_NAME = re.compile(r"-(?P<y>1[6-9]\d\d)(?:-|\.|$)")
SERIES = re.compile(r"\b(Morti|Nati|Matrimoni|Pubblicazioni|Processetti|death register|birth register|marriage register)\b", re.I)


def keys_of(p):
    out = []
    for field in ("cite", "c", "t"):
        text = str(p.get(field) or "")
        for m in ACT.finditer(text):
            for n in (m.group("n"), m.group("n2")):
                if n:
                    out.append("%s-%s" % (m.group("y"), int(n)))
        if out:
            return sorted(set(out), key=out.index), field
    return [], None


def build():
    plates = json.load(open(PLATES, encoding="utf-8"))
    keys, src = {}, {}
    for p in plates:
        ks, field = keys_of(p)
        if ks:
            stem = os.path.splitext(p["f"])[0]
            keys[stem] = ks
            src[stem] = (field, SERIES.search(str(p.get(field) or "")))
    # two plates of different series on one key would make a prose citation ambiguous
    owner = {}
    for stem, ks in keys.items():
        series = (src[stem][1].group(1).lower() if src[stem][1] else "")
        for k in ks:
            if k in owner and owner[k][1] and series and owner[k][1] != series:
                raise SystemExit("build_plate_keys: FAIL, key %s is claimed by plates of two series" % k)
            owner.setdefault(k, (stem, series))
    return dict(sorted(keys.items()))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    keys = build()
    text = json.dumps(keys, ensure_ascii=False, indent=1) + "\n"
    if a.check:
        have = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if have != text:
            print("build_plate_keys: FAIL, site/src/data/plate-keys.json is not what plates.json says: run `python3 tools/build_plate_keys.py` and commit it")
            return 1
        print("build_plate_keys: ok, %d plates keyed to %d acts" % (len(keys), sum(len(v) for v in keys.values())))
        return 0
    open(OUT, "w", encoding="utf-8").write(text)
    print("build_plate_keys: wrote %s: %d plates keyed to %d acts, %d plates with no act" % (
        os.path.relpath(OUT, ROOT), len(keys), sum(len(v) for v in keys.values()),
        len(json.load(open(PLATES, encoding="utf-8"))) - len(keys)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
