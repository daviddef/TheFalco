#!/usr/bin/env python3
"""check:book for the Falco archive: the kit's checkbook.py, run over the built site WITHOUT its redirect stubs.

    python3 ../tools/check_book.py          (from site/; ARCHIVE_OUT names the build, as for every other gate here)

WHY A WRAPPER. This archive builds about five thousand redirect stubs (/names/<slug>/ to /who/<slug>/, the retired
/people/<slug>/ addresses, /emigration/, /married-in/): a stub is a one-line HTML file that sends the reader on. It is
not a chapter and has no running head, so the kit's checkbook.py would count every one as a page nobody placed. The
stubs are set aside here, each one is held to a rule of its own (it must send the reader to a page that was built, and
that page is not itself a stub), and everything else is handed to the kit's checkbook.py unchanged.

It prints how many stubs it set aside, so a build that set every page aside cannot pass: the kit's own refusal on an
empty build covers that case. Nothing here names a person.
"""
import os
import re
import sys
import shutil
import tempfile
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(HERE), "site")
KIT = os.path.join(SITE, "node_modules", "@daviddef", "archive-kit", "kit", "tools", "checkbook.py")
STUB = re.compile(r'<meta http-equiv="refresh" content="0;\s*url=([^"]+)"', re.I)


def dist_dir():
    out = os.environ.get("ARCHIVE_OUT") or "dist"
    return out if os.path.isabs(out) else os.path.join(SITE, out)


def urlpath(dist, d):
    rel = os.path.relpath(d, dist).replace(os.sep, "/")
    return "/" if rel == "." else "/" + rel + "/"


def main(argv):
    dist = dist_dir()
    book = os.path.join(SITE, "src", "data", "book.json")
    if "--dist" in argv:
        dist = argv[argv.index("--dist") + 1]
    if "--book" in argv:
        book = argv[argv.index("--book") + 1]
    if not os.path.isdir(dist):
        print("check_book: no build at %s: nothing was examined" % dist)
        return 1
    if not os.path.exists(KIT):
        print("check_book: the kit's checkbook.py is not installed (%s)" % KIT)
        return 1
    tmp = tempfile.mkdtemp(prefix="falco-book-")
    stubs, kept, problems = {}, 0, []
    try:
        for d, ds, fs in os.walk(dist):
            ds[:] = [x for x in ds if x not in ("node_modules", "_astro", ".git")]
            if "index.html" not in fs:
                continue
            f = os.path.join(d, "index.html")
            head = open(f, encoding="utf-8", errors="replace").read(1500)
            m = STUB.search(head) if "Redirecting to" in head[:300] else None
            url = urlpath(dist, d)
            if m:
                stubs[url] = m.group(1)
                continue
            dst = os.path.join(tmp, os.path.relpath(d, dist), "index.html") if url != "/" else os.path.join(tmp, "index.html")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.symlink(os.path.abspath(f), dst)
            kept += 1
        for url, target in sorted(stubs.items()):
            t = re.sub(r"[?#].*$", "", target)
            if not t.startswith("/"):
                problems.append("stub %s sends the reader to %s, which is not a path on this site" % (url, target))
                continue
            t = t if t.endswith("/") else t + "/"
            if t in stubs:
                problems.append("stub %s sends the reader to another stub, %s" % (url, t))
            elif not os.path.exists(os.path.join(dist, t.lstrip("/"), "index.html")):
                problems.append("stub %s sends the reader to %s, which was not built" % (url, t))
        if problems:
            print("check_book: FAIL (%d redirect stub(s) lead nowhere)" % len(problems))
            for p in problems[:20]:
                print("  - " + p)
            return 1
        r = subprocess.run([sys.executable, KIT, "--dist", tmp, "--book", book], capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        sys.stderr.write(r.stderr)
        print("check_book: %d built pages examined, %d redirect stubs set aside (each leads to a built page)" % (kept, len(stubs)))
        return r.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
