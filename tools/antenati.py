#!/usr/bin/env python3
"""Read Antenati register images without a browser.

THIS REPLACES THE BROWSER METHOD. Until 10 September 2026 every register image
came through a headless browser: inject `window.pstrip`, fetch the leaf inside
the page, crop on a canvas, return a data: URL, dodge a 45-second timeout, and
work around results too large to hand back — a whole apparatus, and it had to
be re-injected after every navigation.

None of it was necessary. The IIIF host serves the images to a plain HTTP
client; it only refuses curl's *default* identity. With a browser User-Agent
and a Referer it answers 200 in about two seconds.

    ark  ->  the volume page  ->  a DAM container manifest  ->  page ids
    id   ->  https://iiif-antenati.cultura.gov.it/iiif/2/<id>/full/<W>,/0/default.jpg

Usage
    python3 tools/antenati.py ids   an_ua14340
    python3 tools/antenati.py strip an_ua14340 2 3 --width 1800 --out d38-02-03.jpg
    python3 tools/antenati.py zoom  an_ua14340 63 --width 3400 --band 0.30 0.20 --half L
"""
import json, os, re, sys, time, subprocess, argparse, concurrent.futures
from io import BytesIO
from PIL import Image

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
IIIF = "https://iiif-antenati.cultura.gov.it/iiif/2/{id}/full/{w},/0/default.jpg"
ARK = "https://antenati.cultura.gov.it/ark:/12657/{ark}/"
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "data", "antenati-ids")

def fetch(url, referer="https://antenati.cultura.gov.it/", binary=False):
    """curl, because it is already here and honours the headers that matter."""
    out = subprocess.run(
        ["curl", "-sSL", "--compressed", "--max-time", "60",
         "-H", f"User-Agent: {UA}", "-H", f"Referer: {referer}", url],
        capture_output=True)
    if out.returncode != 0:
        raise RuntimeError(f"curl failed: {out.stderr.decode()[:200]}")
    return out.stdout if binary else out.stdout.decode("utf-8", "replace")

def ids_for(ark, refresh=False):
    """Every page id of a volume, in order. Cached — the manifest never changes."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, ark + ".json")
    if os.path.exists(path) and not refresh:
        return json.load(open(path))["ids"]

    page = fetch(ARK.format(ark=ark))
    m = re.search(r"https://dam-antenati\.cultura\.gov\.it/antenati/containers/[A-Za-z0-9]+/manifest", page)
    if not m:
        raise SystemExit(f"{ark}: no manifest link on the volume page — is the ark right?")
    mf = json.loads(fetch(m.group(0)))

    canvases = (mf.get("sequences") or [{}])[0].get("canvases") or mf.get("items") or []
    def one(c):
        try:
            return c["images"][0]["resource"]["service"]["@id"].rstrip("/").split("/")[-1]
        except Exception:
            try:
                return c["items"][0]["items"][0]["body"]["service"][0]["@id"].rstrip("/").split("/")[-1]
            except Exception:
                return None
    ids = [x for x in (one(c) for c in canvases) if x]
    json.dump({"ark": ark, "label": mf.get("label"), "manifest": m.group(0), "ids": ids},
              open(path, "w"), indent=1)
    return ids

def leaf(ark, n, width, refresh=False):
    """Image n of the volume, 1-based — the number the archive's notes use.

    The browser method indexed window.D from zero, so `D[27]` was image 28 and
    the off-by-one cost a re-read more than once. Here n IS the image number.
    """
    ids = ids_for(ark, refresh)
    if not 1 <= n <= len(ids):
        raise SystemExit(f"{ark} has {len(ids)} images; {n} is out of range")
    url = IIIF.format(id=ids[n - 1], w=width)
    # Cloudflare answers a burst of requests with an HTML challenge instead of
    # the image. It is a rate limit, not a width limit — the same URL succeeds
    # a moment later. Back off and retry rather than hunting for a "good" width,
    # which is what sent an earlier session chasing a self-inflicted block.
    for attempt in range(4):
        raw = fetch(url, binary=True)
        if raw[:2] == b"\xff\xd8":
            return Image.open(BytesIO(raw))
        if raw[:9].lower() == b"<!doctype":
            time.sleep(2 * (attempt + 1))
            continue
        break
    raise SystemExit(f"image {n}: not a JPEG — {raw[:80]!r}")

# The two halves of an opening, as fractions of the page. Arienzo's registers
# put one act per half from 1839 on; these are the bands the sweeps have used.
HALVES = {"L": (0.05, 0.52), "R": (0.47, 0.52)}

def band(img, half, top, height):
    w, h = img.size
    x, bw = HALVES[half]
    return img.crop((int(w * x), int(h * top), int(w * (x + bw)), int(h * (top + height))))

def stack(tiles, gap=14):
    if not tiles:
        raise SystemExit("nothing to stack")
    W = max(t.width for t in tiles)
    H = sum(t.height for t in tiles) + gap * (len(tiles) + 1)
    out = Image.new("L", (W, H), 136)
    y = gap
    for t in tiles:
        out.paste(t.convert("L"), (0, y)); y += t.height + gap
    return out


def grid(tiles, labels, cols, pad=6, label_h=16):
    """A contact sheet. Used to find where the BUNDLES start in a processetti
    volume: a bundle cover is a near-blank leaf with four lines at the top and a
    big pencil number, and that shape is recognisable long before the words are.
    One sheet of forty replaces forty page reads."""
    from PIL import ImageDraw
    tw = max(t.width for t in tiles); th = max(t.height for t in tiles)
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("L", (cols * (tw + pad) + pad,
                          rows * (th + label_h + pad) + pad), 255)
    d = ImageDraw.Draw(out)
    for i, (t, lab) in enumerate(zip(tiles, labels)):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad); y = pad + r * (th + label_h + pad)
        out.paste(t.convert("L").resize((tw, th)), (x, y))
        d.rectangle([x, y, x + tw, y + th], outline=0)
        d.text((x + 2, y + th + 2), str(lab), fill=0)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["ids", "strip", "zoom", "page", "sweep"])
    ap.add_argument("ark")
    ap.add_argument("pages", nargs="*", type=int)
    ap.add_argument("--width", type=int, default=1800)
    ap.add_argument("--band", nargs=2, type=float, default=[0.085, 0.48],
                    metavar=("TOP", "HEIGHT"))
    ap.add_argument("--half", default="LR", help="which halves: L, R or LR")
    ap.add_argument("--out", default="strip.jpg")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--range", nargs=2, type=int, metavar=("FROM", "TO"))
    a = ap.parse_args()

    if a.cmd == "ids":
        ids = ids_for(a.ark, a.refresh)
        meta = json.load(open(os.path.join(CACHE, a.ark + ".json")))
        print(f"{meta.get('label')}")
        print(f"{len(ids)} images  ->  {os.path.join(CACHE, a.ark + '.json')}")
        return

    if a.range:
        a.pages = list(range(a.range[0], a.range[1] + 1))

    imgs = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(leaf, a.ark, n, a.width, a.refresh): n for n in a.pages}
        for f in concurrent.futures.as_completed(futs):
            imgs[futs[f]] = f.result()

    if a.cmd == "sweep":
        top, height = a.band
        tiles, labels = [], []
        for n in a.pages:
            for h in a.half:
                tiles.append(band(imgs[n], h, top, height)); labels.append(f"{n}{h}")
        grid(tiles, labels, a.cols).save(a.out, quality=80)
        print(f"{a.out}  {len(tiles)} tiles from images {a.pages[0]}-{a.pages[-1]}")
        return

    if a.cmd == "page":
        for n in a.pages:
            p = a.out if len(a.pages) == 1 else a.out.replace(".jpg", f"-{n}.jpg")
            imgs[n].save(p, quality=82)
            print(f"{p}  {imgs[n].size[0]}x{imgs[n].size[1]}")
        return

    top, height = a.band
    tiles = [band(imgs[n], h, top, height) for n in a.pages for h in a.half]
    out = stack(tiles)
    out.save(a.out, quality=72 if a.cmd == "strip" else 85)
    print(f"{a.out}  {out.size[0]}x{out.size[1]}  "
          f"{len(tiles)} panels from images {a.pages}  ({os.path.getsize(a.out)//1024} KB)")

if __name__ == "__main__":
    main()
