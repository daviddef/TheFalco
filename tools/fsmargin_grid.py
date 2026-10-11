#!/usr/bin/env python3
"""Margin boxes in a GRID, not a single row — twice the legible width per box.

A delivered screenshot is capped at about 2,000 px wide whatever the sheet's own
size, so fourteen strips in one row give each surname 143 px and that is where
«Falco Matteo» was read as «Fatto Mattia» on 11 October 2026 — a real birth,
screened out by a sweep that called the year clean. Fourteen strips as 7x2 give
each one 285 px in the same delivered image. Same cost, double the resolution.

    mcol2.py <cachedir> <outprefix> [cols] [rows] [lx0] [lx1] [rx0] [rx1]
"""
import os, sys
from PIL import Image, ImageOps, ImageDraw
C, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 7
rows = int(sys.argv[4]) if len(sys.argv) > 4 else 2
lx0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.015
lx1 = float(sys.argv[6]) if len(sys.argv) > 6 else 0.175
rx0 = float(sys.argv[7]) if len(sys.argv) > 7 else 0.79
rx1 = float(sys.argv[8]) if len(sys.argv) > 8 else 0.95
per = cols*rows
ns = sorted(int(f[:-4]) for f in os.listdir(C) if f.endswith(".jpg"))
tiles, labs, k = [], [], 0
def sheet():
    global tiles, labs, k
    if not tiles: return
    tw = max(t.width for t in tiles); th = max(t.height for t in tiles)
    nr = (len(tiles)+cols-1)//cols
    im = Image.new("L", (cols*(tw+6)+6, nr*(th+20)+6), 243); d = ImageDraw.Draw(im)
    for i, (t, lab) in enumerate(zip(tiles, labs)):
        x = 6+(i % cols)*(tw+6); y = 6+(i//cols)*(th+20)
        im.paste(t.resize((tw, th)), (x, y))
        d.rectangle([x, y, x+tw, y+th], outline=0); d.text((x+2, y+th+4), lab, fill=0)
    k += 1; p = f"{out}-{k:02d}.jpg"; im.save(p, quality=92); print(p)
    tiles, labs = [], []
for n in ns:
    im = Image.open(os.path.join(C, f"{n}.jpg")).convert("L"); w, h = im.size
    for lab, a, b in ((f"{n}L", lx0, lx1), (f"{n}R", rx0, rx1)):
        c = im.crop((int(w*a), int(h*0.02), int(w*b), int(h*0.98)))
        c = ImageOps.autocontrast(c, cutoff=1)
        c.thumbnail((520, 3000)); tiles.append(c); labs.append(lab)
        if len(tiles) == per: sheet()
sheet()
