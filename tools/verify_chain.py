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
# A PRIVATE DIRECTORY MUST HAVE A PRIVATE NAME.
#
# This was `dist-verify`, which is what the whole estate standardised on — so
# two sessions verifying at once build into the same directory and each grades
# the other's half-written pages. It reported «spouse fell 585→489, household
# 962→905» on 23 September 2026 and not one of those numbers was true; built
# in isolation the same data matched the floor exactly. A gate that reports a
# loss that did not happen teaches people to ignore gates.
#
# ARCHIVE_OUT still wins, so a caller who wants a specific directory — to point
# a kit tool at the build it just made — keeps that. Otherwise the name carries
# this process's pid, which no other session can collide with.
OUT = os.environ.get("ARCHIVE_OUT") or f"dist-verify-{os.getpid()}"
pkg = json.load(open(os.path.join(SITE, "package.json"), encoding="utf-8"))
steps = [s.strip() for s in pkg["scripts"]["build"].split("&&")]

# --skip NAME — RUN THE REST OF THE CHAIN WHEN A STEP THAT IS NOT YOURS IS RED.
#
# Added 11 October 2026. On that morning `check:pin` failed in ALL SEVEN family
# archives at once: the kit-wide commit that added `check:nav` to every
# package.json pinned the kit at 3c9214e, and `kit/tools/checknav.py` landed in
# the NEXT kit commit, 8d2e6b2. An off-by-one in a shared pin, owned by the kit
# session, and it stopped every other session verifying anything at step one.
#
# THE WHOLE POINT OF THIS FLAG IS THAT IT CANNOT BE USED QUIETLY. A skipped step
# is announced where it would have run, it is listed again at the end, and the
# chain REFUSES to print ALL GREEN — because «all green» is the sentence people
# quote in a commit message, and it must never be true of a run that skipped a
# gate. Skip a step you do not own and are reporting; never one that is red
# because of your own work.
SKIP = []
_argv = sys.argv[1:]
while _argv:
    a = _argv.pop(0)
    if a == "--skip" and _argv:
        SKIP.append(_argv.pop(0))
    elif a.startswith("--skip="):
        SKIP.append(a.split("=", 1)[1])

def run(label, cmd, cap=60):
    print(f"== {label}", flush=True)
    # AND EVERY STEP MUST BE TOLD WHERE THE BUILD IS.
    #
    # Rewriting `--dist dist` is not enough: the kit tools that take no --dist
    # resolve the directory themselves through ARCHIVE_OUT, so without this
    # they grade the SHARED `site/dist` — another session's build — while this
    # chain builds somewhere else entirely. That is how `check:rows` reported
    # «spouse fell 585→489, household 962→905» against a build that had lost
    # nothing: it was not looking at it.
    env = dict(os.environ, ARCHIVE_OUT=OUT)
    r = subprocess.run(cmd, cwd=SITE, shell=True, text=True, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # SHOW EVERY LINE A GATE SAYS ABOUT ITSELF, AND NEVER DROP ONE SILENTLY.
    #
    # This printed the last SIX non-empty lines and nothing else. On
    # 7 October 2026 a line was added to check_release stating what its noindex
    # test examined — and that pushed the line stating what its DATE GUARD
    # examined off the top, so the chain stopped showing it. Nothing failed and
    # nothing said anything was missing; the gate's own account of its coverage
    # simply vanished from the only place anybody reads it.
    #
    # That is work-list row 98 one level up: a gate can state its coverage
    # perfectly and still be read as silent, because the harness truncated it.
    # A build runs twenty steps, so a cap exists to keep the astro step's page
    # list from burying everything — but the cap must SAY when it bit.
    # The cap is per step on purpose. A GATE says a handful of things about
    # itself and every one of them matters, so it gets room. `astro build`
    # narrates sixteen thousand page writes and only its last few lines carry
    # anything — give it the same room and it buries every gate beneath it.
    lines = [l for l in r.stdout.rstrip().split("\n") if l.strip()]
    shown = lines[-cap:]
    if len(lines) > cap:
        print(f"   … {len(lines) - cap} earlier line(s) of this step not shown")
    for l in shown:
        print("   " + l)
    if r.returncode != 0:
        print(f"\nFAILED at «{label}» (exit {r.returncode}). Full output:\n")
        print(r.stdout)
        sys.exit(r.returncode)

failed = []
for step in steps:
    _name = step.replace("npm run ", "").strip()
    if _name in SKIP:
        print(f"== {_name}\n   SKIPPED BY --skip — NOT RUN, NOT GRADED, NOT GREEN", flush=True)
        continue
    if step == "astro build":
        run("astro build --outDir " + OUT, f"npx astro build --outDir {OUT}", cap=4)
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
               "exec(compile(src,'sitemap.py','exec'),"
               "{'__name__':'__main__',"
               "'__file__':'node_modules/@daviddef/archive-kit/kit/tools/sitemap.py'})\"")
    run(name, cmd)

if SKIP:
    print("\nNOT ALL GREEN — " + str(len(SKIP)) + " step(s) were SKIPPED and did not run: "
          + ", ".join(SKIP) + "\nEverything else in package.json's build ran against " + OUT
          + ". A skipped gate has graded nothing.")
else:
    print("\nALL GREEN — every step in package.json's build ran, against " + OUT)
