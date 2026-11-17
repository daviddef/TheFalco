#!/usr/bin/env python3
"""The places the corrections page may link, and the flag table it draws beside them.

    python3 tools/build_correction_places.py            # writes site/src/data/correction-places.json and correction-place-flags.json

Rows are the places the Atlas map data (site/public/atlas-data.json) gives a page /places/<slug>/ ; nothing else is linked. The flags come from the
kit's placeflags.py over this archive's era snapshot (site/src/data/era-snapshot.json): where the snapshot is silent for a year the place gets
today's flag only. `npm run build` runs this before `astro build` (the corrections page reads both files)."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
atlas = json.load(open(os.path.join(SITE, "public", "atlas-data.json"), encoding="utf-8"))
rows = [{"name": p["name"], "href": "/places/%s/" % p["slug"]} for p in atlas["places"] if p.get("slug")]
rows_path = os.path.join(SITE, "src", "data", "correction-places.json")
open(rows_path, "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
out = os.path.join(SITE, "src", "data", "correction-place-flags.json")
r = subprocess.run([sys.executable, os.path.join(SITE, "node_modules", "@daviddef", "archive-kit", "kit", "tools", "placeflags.py"),
                    "--snapshot", os.path.join(SITE, "src", "data", "era-snapshot.json"), "--places", rows_path, "--out", out])
sys.exit(r.returncode)
