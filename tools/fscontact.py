#!/usr/bin/env python3
"""A contact sheet of a whole FamilySearch volume, from its thumbnails.

WHY THIS IS AFFORDABLE AND THE TILES ARE NOT.

`notes/familysearch-image-reading` measured the DeepZoom tile budget at about
**25 requests per half hour** — exceed it and every request returns 403 with an
Imperva page for ~30 minutes. On that budget a 1,236-image volume cannot be
surveyed at all: one act's band is ~15 tiles, so a volume is years of windows.

**The thumbnails are on a different endpoint and a far more generous
allowance.** Measured 8 October 2026: **fifty consecutive `thumb_p200.jpg` at
one a second, no block**, immediately after a tile run had been throttled.

    deepzoomcloud/dz/v1/<ark>/image_files/<L>/<c>_<r>.jpg   tight budget
    dascloud/das/v2/<ark>/thumb_p200.jpg                    one a second is fine

So the survey and the reading are two different jobs with two different costs.
**Survey on thumbnails; spend tiles only on the leaf the survey chose.**

A 200 px thumbnail will not give you a name or a date. It will give you, for
every image in a book: cover, blank, printed form, a page of running hand, a
TWO-COLUMN INDEX, a filmer's target board. That is what a layout proof needs —
see `notes/register-layout-proof.md`, which did the same job for the Antenati
volumes an image at a time.

    python3 tools/fscontact.py data/arienzo-fs-tribunale-images.tsv \\
        --waypoint MC55-FNT --out scratch/arz --cols 12 --rows 8

Writes `arz-001.jpg`, `arz-002.jpg`, … each a grid of thumbnails with the image
number burnt into every cell, so a sheet can be read and cited directly.

POLITENESS. One request a second, single threaded, with the session cookie the
user already holds in their browser. Nothing is impersonated and nothing is
worked around; a 403 stops the run and is reported, never recorded as absence.
"""
import argparse
import os
import subprocess
import sys
import time

from PIL import Image, ImageDraw

DAS = ("https://sg30p0.familysearch.org/service/records/storage/dascloud/"
       "das/v2/{ark}/thumb_p200.jpg")
REF = "https://www.familysearch.org/"
DEFAULT_SID = os.path.expanduser("~/.fs-sid")


def sid(path):
    try:
        return open(path, encoding="utf-8").read().strip()
    except OSError:
        sys.exit(f"  no session cookie at {path} — David signs in; this never "
                 f"enters credentials.")


def fetch(ark, s, dest, tries=3):
    """One thumbnail. Returns True on 200, False on anything else."""
    for attempt in range(tries):
        r = subprocess.run(
            ["curl", "-sS", "--max-time", "30", "-o", dest,
             "-w", "%{http_code}", "-b", f"fssessionid={s}",
             "-H", f"Referer: {REF}", DAS.format(ark=ark)],
            capture_output=True, text=True)
        code = (r.stdout or "").strip()[-3:]
        if code == "200":
            return True
        if code == "403":
            # The budget, or the security service. Either way stop — hammering
            # it converts a pause into a half-hour ban.
            return False
        time.sleep(2 * (attempt + 1))
    return False


def sheet(cells, cols, rows, cell, out, first):
    """One contact sheet, image numbers burnt in."""
    pad, lab = 4, 12
    w = cols * (cell + pad) + pad
    h = rows * (cell + pad + lab) + pad
    sh = Image.new("RGB", (w, h), (24, 24, 24))
    dr = ImageDraw.Draw(sh)
    for i, (num, path) in enumerate(cells):
        cx = pad + (i % cols) * (cell + pad)
        cy = pad + (i // cols) * (cell + pad + lab)
        try:
            im = Image.open(path).convert("RGB")
            im.thumbnail((cell, cell))
            sh.paste(im, (cx + (cell - im.width) // 2,
                          cy + (cell - im.height) // 2))
        except Exception:
            dr.rectangle([cx, cy, cx + cell, cy + cell], outline=(90, 40, 40))
        dr.text((cx + 2, cy + cell + 1), str(num), fill=(210, 210, 210))
    sh.save(out, quality=88)
    print(f"  -> {out}  images {first}–{first + len(cells) - 1}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("index", help="tsv from tools/fswaypoint.py")
    ap.add_argument("--waypoint", required=True)
    ap.add_argument("--out", required=True, help="prefix for the sheets")
    ap.add_argument("--cols", type=int, default=12)
    ap.add_argument("--rows", type=int, default=8)
    ap.add_argument("--cell", type=int, default=150)
    ap.add_argument("--from", dest="lo", type=int, default=1)
    ap.add_argument("--to", dest="hi", type=int, default=0)
    ap.add_argument("--pace", type=float, default=1.0)
    ap.add_argument("--sid-file", default=DEFAULT_SID)
    ap.add_argument("--cache", default="", help="where thumbnails live")
    args = ap.parse_args()

    s = sid(args.sid_file)
    cache = args.cache or (args.out + "-thumbs")
    os.makedirs(cache, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)

    arks = []
    with open(args.index, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) > 3 and f[1] == args.waypoint:
                arks.append((int(f[2]), f[3]))
    arks = [a for a in arks if a[0] >= args.lo and (not args.hi or a[0] <= args.hi)]
    if not arks:
        sys.exit(f"  no images for {args.waypoint} in {args.index}")

    per = args.cols * args.rows
    cells, n_sheet, got, refused = [], 0, 0, 0
    for num, ark in arks:
        dest = os.path.join(cache, f"{num:05d}.jpg")
        if not os.path.exists(dest) or os.path.getsize(dest) < 500:
            if not fetch(ark.replace("3:1:", "3:1:"), s, dest):
                refused += 1
                print(f"  REFUSED at image {num} ({ark}) after {got} fetched — "
                      f"stopping. This is a refusal, not an absence.")
                break
            got += 1
            time.sleep(args.pace)
        cells.append((num, dest))
        if len(cells) == per:
            n_sheet += 1
            sheet(cells, args.cols, args.rows, args.cell,
                  f"{args.out}-{n_sheet:03d}.jpg", cells[0][0])
            cells = []
    if cells:
        n_sheet += 1
        sheet(cells, args.cols, args.rows, args.cell,
              f"{args.out}-{n_sheet:03d}.jpg", cells[0][0])
    print(f"  {got} thumbnail(s) fetched, {n_sheet} sheet(s), "
          f"{refused} refusal(s)")


if __name__ == "__main__":
    main()
