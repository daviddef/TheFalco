#!/usr/bin/env python3
"""Margin-box sweep of a FamilySearch printed marriage register.

From 1866 the Italian form prints a NAME BOX down the outer edge of each act:
«Numero N» and under it the groom's and bride's surnames and forenames. Two
boxes to an opening — one per page. So a strip of the outer margins reads every
couple in the book without touching the body of a single act.

    fsmargin.py <tsv> <waypoint> <lo> <hi> <outprefix> [per]
"""
import sys, os, subprocess, time
from PIL import Image, ImageDraw

tsv, wp, lo, hi, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
per = int(sys.argv[6]) if len(sys.argv) > 6 else 14
SID = open(os.path.expanduser(os.environ.get("FS_SID", "")), encoding="utf-8").read().strip()
CACHE = out + "-cache"; os.makedirs(CACHE, exist_ok=True)
URL = ("https://sg30p0.familysearch.org/service/records/storage/dascloud/das/v2/"
       "{ark}/dist.jpg")

arks = {}
with open(tsv, encoding="utf-8") as fh:
    next(fh)
    for line in fh:
        f = line.rstrip("\n").split("\t")
        if len(f) > 3 and f[1] == wp:
            arks[int(f[2])] = f[3]

tiles, labels, k = [], [], 0
def sheet():
    global tiles, labels, k
    if not tiles: return
    tw = max(t.width for t in tiles); th = max(t.height for t in tiles)
    im = Image.new("L", (len(tiles)*(tw+6)+6, th+18), 240); d = ImageDraw.Draw(im)
    for i, (t, lab) in enumerate(zip(tiles, labels)):
        x = 6+i*(tw+6); im.paste(t.convert("L").resize((tw, th)), (x, 6))
        d.rectangle([x, 6, x+tw, 6+th], outline=0); d.text((x+2, th+8), lab, fill=0)
    k += 1; p = f"{out}-{k:02d}.jpg"; im.save(p, quality=86); print(p)
    tiles, labels = [], []

for n in range(lo, hi+1):
    if n not in arks: continue
    dest = os.path.join(CACHE, f"{n}.jpg")
    if not os.path.exists(dest) or os.path.getsize(dest) < 5000:
        r = subprocess.run(["curl","-sS","--max-time","90","-L","-o",dest,"-w","%{http_code}",
                            "-b", f"fssessionid={SID}",
                            "-H","Referer: https://www.familysearch.org/",
                            URL.format(ark=arks[n])], capture_output=True, text=True)
        if (r.stdout or "").strip()[-3:] != "200":
            print(f"  MISSING {n}: HTTP {r.stdout.strip()[-3:]}", file=sys.stderr); continue
        time.sleep(1.0)
    try: im = Image.open(dest).convert("L")
    except Exception as e:
        print(f"  MISSING {n}: {e}", file=sys.stderr); continue
    w, h = im.size
    # outer margin of the LEFT page, then of the RIGHT page
    for lab, x0, x1 in ((f"{n}L", 0.015, 0.175), (f"{n}R", 0.515, 0.675)):
        c = im.crop((int(w*x0), int(h*0.03), int(w*x1), int(h*0.97)))
        c.thumbnail((240, 1500)); tiles.append(c); labels.append(lab)
        if len(tiles) == per: sheet()
sheet()
