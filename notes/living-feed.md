# The living-people feed — what CI can now check, and what it still cannot (17 Oct 2026)

**Problem it solves.** `check_living_v2` and `check_living_prose` need the private tree, which is gitignored, so in CI they
printed «NOT RUN» and exited 0. A push from a machine without the tree could deploy a living person's date green.

## What is committed (`data/living-feed.json`) and why it is safe
- **A plain hash would have been worthless.** There are ~40,000 plausible birth dates; anyone hashes them all in a second and
  reads the answer off a public file. So the dates and held-out names are **keyed HMACs (SHA-256, 128 bits)**. The key is a
  256-bit secret that is *never* committed: `private/living-feed.key` locally (gitignored, mode 600), the **`LIVING_FEED_KEY`**
  secret in GitHub Actions. Without the key the file is noise.
- Dates are canonicalised to `YYYY-MM-DD`, so «[withheld]», «6 January 1979», «6 gennaio 1979» and «6th Jan, 1979» are one entry.
- **Held-out people** (undated, with a living parent; published nowhere) are guarded by name, both orders (`Given Family` /
  `FAMILY Given`). Living people with pages are named on the public site by policy, so their names need no protection.
- **The seal** is a digest of which people.json records are published as living. It tells CI whether the people.json it is looking
  at is the one a machine with the tree last confirmed. Flip anyone between living and dead and CI fails until `build` is re-run
  where the tree is; `build` refuses if the tree disagrees with people.json.
- **`keycheck`** makes a wrong key a failure; a wrong key would otherwise match nothing and report clean.

## What runs where
| | with the tree (David's machine / this session) | CI, secret set | CI, secret NOT set |
|---|---|---|---|
| living_feed seal | ✔ | ✔ | ✔ |
| living_feed dates + held-out names | ✔ | ✔ | warning, skipped |
| living-prose | from the tree | **from people.json (new)** | **from people.json (new)** |
| living2 recompute of who is living | ✔ | NOT RUN | NOT RUN |

## What it cannot do
- **Recompute who is living in CI.** That needs birth years, which cannot be committed in any form (there are ~120 plausible
  years; a hash of a birth year is a birth year). The seal makes any *change* to the living set un-skippable; it cannot see a
  tree person the generator never flagged.
- **Protect dates if the key leaks.** Treat it like a password. Rotate: delete `private/living-feed.key`, run `build`, set the new secret.
- **Guard a held-out person who shares a name with a dead one** — counted at build time (0 now) and left out of the feed.

## Using it
- After anything that changes who is living, or the tree: `python3 tools/living_feed.py build --dist site/<a built dir>` (needs
  the tree; refuses if people.json and the tree disagree or if a guarded date is already on the built site).
- First time, or a new machine: `gh secret set LIVING_FEED_KEY < private/living-feed.key`.
- `python3 tools/living_feed.py check --tracked` also scans the local `data/` directory (it will find the private exports there,
  which is expected and is why they are gitignored).

## The larger exposure this found
The full tree (427 people, **32 living with birth dates**) was committed to this public repository on 8 Sep and removed on
14 Sep (commit 7e672530). **It is still readable in git history** (`git show e1d56e9a:data/myheritage-falco-tree.json`). The feed
does not change that. See the end of the session summary for the options; scrubbing history is destructive and was not done.
