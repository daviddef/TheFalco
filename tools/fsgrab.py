#!/usr/bin/env python3
"""Read a FamilySearch register image at magnification, by its DeepZoom tiles.

WHY THIS EXISTS. The full-text transcription finds an act; it does not read it.
On the 1802 Falco marriages the machine had the year as 1902, gave no day,
implied two weddings shared a date three weeks apart, and invented a surname.
Every name it got right; almost every number it got wrong. **A machine
transcription is a candidate, exactly as a contact sheet is**, and nothing enters
a household until the image behind it has been read.

This was a shell script in a scratch directory on 27 September 2026, with a note
saying it was «worth promoting into tools/ if this is done again». It is being
done again — work-list row 69 — so here it is.

    python3 tools/fsgrab.py meta  3QS7-897N-5R1
    python3 tools/fsgrab.py grab  3QS7-897N-5R1 --level 10 --out page.jpg
    python3 tools/fsgrab.py grab  3QS7-897N-5R1 --level 12 --box 0 400 2400 300 --out band.jpg

THE SESSION COOKIE IS DAVID'S. He signs in; this never enters credentials. The
cookie is read from the scratch file written by the session that asked him, is
used only against familysearch.org, and must never be written into this
repository, which is public. Pass --sid-file to point at it.

THE RATE LIMIT IS THE REAL CONSTRAINT, and it is smaller than it looks: about
TWENTY-FIVE requests per half hour counting image.xml and tiles together. Exceed
it and everything returns 403 behind an Imperva page for about thirty minutes.
So: find the act on a LOW level (a whole leaf at L-2 is ~15 tiles, at native it
is ~200), then spend the budget on one band. This tool paces itself and refuses
to start a job it knows will blow the budget unless you say --yes.
"""
import argparse, math, os, re, subprocess, sys, time

HOST = "https://sg30p0.familysearch.org"
BASE = HOST + "/service/records/storage/deepzoomcloud/dz/v1/3:1:{ark}"
REF  = "https://www.familysearch.org/"
DEFAULT_SID = os.path.join(
    os.environ.get("FS_SCRATCH", "/private/tmp"), "sid")


def sid(path):
    if not os.path.exists(path):
        sys.exit(f"no session file at {path} — ask David to sign in, then write the "
                 f"fssessionid there. This tool never enters credentials.")
    return open(path).read().strip()


def get(url, s, binary=False, tries=3):
    for a in range(tries):
        r = subprocess.run(["curl", "-sS", "--max-time", "45",
                            "-b", f"fssessionid={s}", "-H", f"Referer: {REF}", url],
                           capture_output=True)
        b = r.stdout
        if binary and b[:2] == b"\xff\xd8":
            return b
        if not binary and b[:1] in (b"<", b"{"):
            if b"<html" in b[:200].lower() and b"Width" not in b[:400]:
                time.sleep(4 * (a + 1)); continue
            return b
        if b[:9].lower() == b"<!doctype" or b"Incapsula" in b or b"Imperva" in b:
            time.sleep(8 * (a + 1)); continue
        if binary:
            time.sleep(4 * (a + 1)); continue
        return b
    raise SystemExit("403/throttled — the rate limit is about 25 requests a half hour. "
                     "Wait and retry; do NOT record a negative from this.")


def meta(ark, s):
    x = get(BASE.format(ark=ark) + "/image.xml", s).decode("utf-8", "replace")
    g = lambda k: int(re.search(k + r'="(\d+)"', x).group(1))
    return dict(w=g("Width"), h=g("Height"), ts=g("TileSize"), ov=g("Overlap"))


def grab(ark, s, level, box, out, pace):
    from PIL import Image
    m = meta(ark, s)
    native = math.ceil(math.log2(max(m["w"], m["h"])))
    sc = 2.0 ** (native - level)
    W, H = math.ceil(m["w"] / sc), math.ceil(m["h"] / sc)
    x, y, w, h = box if box else (0, 0, W, H)
    x, y = max(0, x), max(0, y)
    w, h = min(w, W - x), min(h, H - y)
    ts, ov = m["ts"], m["ov"]
    c0, c1 = x // ts, (x + w - 1) // ts
    r0, r1 = y // ts, (y + h - 1) // ts
    n = (c1 - c0 + 1) * (r1 - r0 + 1)
    print(f"  {ark}  native L{native}  full {m['w']}x{m['h']}  "
          f"level {level} -> {W}x{H}  box {x},{y},{w},{h}  = {n} tile(s)")
    if n > 40 and not ARGS.yes:
        sys.exit(f"  {n} tiles would eat the whole rate budget. Use a lower --level "
                 f"to find the act first, or pass --yes if you mean it.")
    canvas = Image.new("L", (w, h), 255)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            u = BASE.format(ark=ark) + f"/image_files/{level}/{c}_{r}.jpg"
            t = Image.open(__import__("io").BytesIO(get(u, s, binary=True))).convert("L")
            px = c * ts - (ov if c else 0)
            py = r * ts - (ov if r else 0)
            canvas.paste(t, (px - x, py - y))
            time.sleep(pace)
    canvas.save(out, quality=92)
    print(f"  -> {out}  {canvas.size[0]}x{canvas.size[1]}")


ap = argparse.ArgumentParser()
ap.add_argument("cmd", choices=["meta", "grab"])
ap.add_argument("ark")
ap.add_argument("--level", type=int, default=None)
ap.add_argument("--box", type=int, nargs=4, default=None,
                help="x y w h, in pixels AT THE CHOSEN LEVEL")
ap.add_argument("--out", default="fs.jpg")
ap.add_argument("--sid-file", default=DEFAULT_SID)
ap.add_argument("--pace", type=float, default=0.9,
                help="seconds between tiles; 0.9 is what the limit tolerates")
ap.add_argument("--yes", action="store_true")
ARGS = ap.parse_args()

S = sid(ARGS.sid_file)
A = ARGS.ark.replace("3:1:", "")
if ARGS.cmd == "meta":
    m = meta(A, S)
    nat = math.ceil(math.log2(max(m["w"], m["h"])))
    print(f"  {A}  {m['w']}x{m['h']}  tile {m['ts']} overlap {m['ov']}  native level {nat}")
    for L in range(nat, nat - 4, -1):
        sc = 2.0 ** (nat - L)
        print(f"     L{L}: {math.ceil(m['w']/sc)}x{math.ceil(m['h']/sc)}  "
              f"~{math.ceil(math.ceil(m['w']/sc)/m['ts'])*math.ceil(math.ceil(m['h']/sc)/m['ts'])} tiles for the whole leaf")
else:
    grab(A, S, ARGS.level or 10, ARGS.box, ARGS.out, ARGS.pace)
