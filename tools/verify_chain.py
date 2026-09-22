#!/usr/bin/env python3
"""Run the REAL build chain against an isolated build, derived from package.json.

Written 22 September 2026, after a hand-rolled copy of the chain went wrong
three times in two days:

  * `set -e` without `set -o pipefail`: every step was piped to `tail` for a
    readable log, so the shell read TAIL's exit status.  The other session
    reinstalled the kit mid-run, SIX checks printed "can't open file", and the
    script printed ALL GREEN.
  * `check_release.py` takes `--dist` and silently defaults to `site/dist` — the
    directory another session rebuilds continuously, and the one the tool's own
    docstring says reading mid-write is the hazard.  It failed on a living
    person's page that was correct in dist-verify and stale in dist.
  * And the chain GREW.  check:pin, check:pages, check:inline and check:rows were
    added to package.json and the hand-rolled copy never learned about them, so
    four gates had not run for a day.

The fix is to stop keeping a copy.  This reads `scripts.build` out of
package.json, drops the astro build (it runs it itself, into dist-verify), and
points every `--dist dist` at `dist-verify`.  A step added to package.json is
run here the next time without anyone remembering.

Run:  python3 tools/verify_chain.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = "dist-verify"
pkg = json.load(open(os.path.join(SITE, "package.json"), encoding="utf-8"))
steps = [s.strip() for s in pkg["scripts"]["build"].split("&&")]

def run(label, cmd):
    print(f"== {label}", flush=True)
    r = subprocess.run(cmd, cwd=SITE, shell=True, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tail = [l for l in r.stdout.rstrip().split("\n") if l.strip()][-6:]
    for l in tail:
        print("   " + l)
    if r.returncode != 0:
        print(f"\nFAILED at «{label}» (exit {r.returncode}). Full output:\n")
        print(r.stdout)
        sys.exit(r.returncode)

failed = []
for step in steps:
    if step == "astro build":
        run("astro build --outDir " + OUT, f"npx astro build --outDir {OUT}")
        continue
    name = step.replace("npm run ", "").strip()
    script = pkg["scripts"].get(name)
    if script is None:
        run(step, step); continue
    # every gate that takes --dist must be pointed at the isolated build, and
    # check_release takes it without advertising it in the script line.
    cmd = script.replace("--dist dist", f"--dist {OUT}")
    if "check_release.py" in cmd and "--dist" not in cmd:
        cmd += f" --dist {OUT}"
    if "sitemap.py" in cmd:
        cmd = ("python3 -c \"src=open('node_modules/@daviddef/archive-kit/kit/tools/sitemap.py')"
               ".read().replace('dist = os.path.join(site, \\\"dist\\\")',"
               "'dist = os.path.join(site, \\\"" + OUT + "\\\")');"
               "exec(compile(src,'sitemap.py','exec'),{'__name__':'__main__'})\"")
    run(name, cmd)

print("\nALL GREEN — every step in package.json's build ran, against " + OUT)
