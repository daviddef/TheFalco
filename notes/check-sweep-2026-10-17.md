# Does every check fail when it should? A sweep of Falco's build — 17 Oct 2026

Method: for each check, (1) it passes on the clean build; (2) ONE realistic fault is planted — in the built output (a scratch copy)
or in a source file (restored byte for byte afterwards, `git status` clean) — and the check must fail; (3) it is fed an empty or
missing input, because a count of zero printed as «ok» is the Booyzen / Lerena fault. 19 checks + the builder's own refusals,
about eighty planted faults and empty-input runs. The harness lives only in the session scratchpad; the faults below are enough to repeat it.

## Caught (planted fault → the check fails)
- **kit/checkarchive** — dead internal link; missing #anchor; duplicate id *that a cross-page link targets* (a same-page `#x` link
  is deliberately not reported — my first fault was wrong, not the check); page with no `<title>`; `<img>` to nothing; search index deleted.
- **release** — a living person's full date in either spelling (needs the private tree); a living page with no noindex.
- **living2** — living page without noindex; with an `<img>`; in the sitemap; a year inside `<main>`. Its own `--selftest`: 28 of 28.
- **nav** (Evidence entry removed) · **kin** (father dead before birth) · **worklist** (bad state; no owner) · **covers** (a row
  covering a key that does not exist) · **templates** (unclosed `<div>`) · **sources** (three unreachable) · **pages** (a shared page
  drawn by hand again) · **inline** (a 17th inline evidence list) · **pin** (package.json ≠ lockfile) · **living-prose** (a living
  name with a year, typed on a page) · **households** (duplicate id) · **corrections** (a retired surname; a retired phrase) ·
  **prose** (a retired coverage claim) · **evidence** (a uniquely-named documented person's page loses its evidence).
- **build_people** — a join naming a missing record aborts; a published slug going dark without an alias aborts; a join that
  would make someone their own ancestor is REFUSED and skipped (by design, not an abort).

## Could NOT be made to fail, or failed only after a fix
| Check | What happened | Status |
|---|---|---|
| **rows** | All spouse marks removed from the spine page; stayed green. `.rowfloor` was **slack** (household 994 vs 1,139 real; ~145 could vanish) | **FIXED** — floor raised to today's counts; same fault now caught |
| **release** | Empty build printed «clean»; `people.json = []` printed «clean» | **FIXED** — refuses at zero pages or zero people |
| **corrections** | `households.json = []` printed «clean» | **FIXED** — refuses and prints what it examined |
| **prose** | `searched.json = []` printed «clean» | **FIXED** — refuses at zero pages / searched rows / families |
| **atlas** | A place with no coordinate printed «1 without a coordinate» and exited 0 | **FIXED** — exits 1 |
| **fscite** | Existed but was **not in the build at all**; with no citations it would print «clean» | **FIXED** — wired into `package.json`; refuses at zero |
| **rows / kin / templates** | «not run» exits 0 (missing built dir, missing data, missing `@astrojs/check`) | **FIXED here** with the kit's own `--require` |
| **pages** | Needs the OTHER archives checked out beside this one. On a CI runner (one checkout) it prints «not run» and passes; on an empty root it said «0 exempt» ok | **Cannot fail in CI.** `--require` would break the deploy. Kit-owned |
| **living (kit)** | A living person's date from the private tree is not caught: it harvests only committed data, and «25 flagged, not one date harvested». Tree dates are guarded by `release` alone | Kit-owned; stated in its own output |
| **pin** | `.kitpin` ≠ lockfile: not read by any check. **An installed kit file edited (print.css) passes** — the check reads the lockfile, never the installed files; this is exactly how the stale kit passed on 13 Oct | Kit-owned. Suggest hashing the installed `kit/` |
| **living2 / living-prose / release-tree** | **In CI the private tree is absent: `living2` prints «NOT RUN» and exits 0, `living-prose` prints «NOT RUN IN CI» and exits 0.** Both are documented in their own output. The deploy therefore cannot catch what they catch; protection depends on someone running the full chain on a machine that has the tree | **Design limit — the important one.** See below |

## The one that matters
**On a CI runner the living-people gates that need the private tree do not run, and pass.** Everything that protects a living
person from a leak of the tree's own dates or of typed prose runs only on David's machine (or a session on it). A push from a
machine without the tree, or a commit made after the chain was last run, can deploy such a leak green. Options: a salted-hash
feed of living names/dates committed to the repo (no names in the clear); or a private CI step with the tree as a secret; or at
minimum a pre-push hook that runs `npm run build` where the tree exists. This is a decision for David, not a fix to make here.
