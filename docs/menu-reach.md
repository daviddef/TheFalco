# Estate clean-up, 23 November 2026: menu reach proof

Compared: the build of `origin/main` (9b3cbf4f) against the build of this branch, both from a clean worktree, both with the same private inputs. The inventory is the kit's `menu_inventory.py` (`snapshot` of the old build, `compare` against the new one); the per-address check below was run on the new `dist`.

## Counts (links as the header draws them; a group heading that is a link counts, a plain label does not)

| menu | before | after |
|---|---:|---:|
| Start | 3 | 3 |
| Our line | 3 | 3 |
| People | 11 | 7 (Lists 6 + one link, "Drawn") |
| Places & families | 21 | 7 (Places, The Atlas, All the families, four named families) |
| The name | 4 | 4 |
| Research | 19 | 14 (three group heads, the eight core pages, Documents, Gallery, one "Deep dives" heading) |
| **all menus** | 61 | 38 |

The menu is one list now, `site/src/lib/site-menu.js` (Falco had no such file; the menu lived in `layouts/Base.astro`). The header, the drawer and the three hub lists below all read it, and `lib/research-menu.js` for Research, so a menu and the page that holds what left it cannot disagree.

## What left a menu, and where it is reached from

| address | was | now reached from (a link inside `<main>` of the hub) |
|---|---|---|
| `/tree/`, `/trees/`, `/bloodline/`, `/timeline/` | People / Drawn | `/drawn/` (new hub; `/direct-line/`, which stays in Our line, is listed there too) |
| `/roots/` | People / Drawn | removed; the address redirects to `/trees/` (see below) |
| `/carfora/`, `/ferrara/`, `/maione/`, `/rivetti/`, `/zampiello/`, `/wider-family/` | Places & families | `/families/` ("A page of its own", the kit's ResearchList) |
| `/arienzo/`, `/camellara/`, `/valle-caudina/`, `/walk/`, `/journeys/`, `/rule/`, `/diaspora/`, `/liguori/` | Places & families | `/places/` ("The place stories") |
| `/antenati/`, `/processetti/`, `/holdings/`, `/the-library/`, `/dna/`, `/research-log/` | Research | `/research/deep-dives/` (new hub; the first five were already under the "Deep dives" label, the Research Log was in What's new) |

`/families/cioffi/` and `/annecchino/`, `/crisci/`, `/morgillo/` stay named in the menu (the four largest, A to Z; the archive's own line is The Spine, which leads Our line). Every `/families/<slug>/` page was already linked from the `/families/` cards.

Checked on the built `dist`: every address in the table is an `<a href>` inside `<main>` of the hub named. The new hubs are in the sitemap and the search index, and have chapters in the book (`site/src/data/book.json`: `/drawn/` after The Spine's neighbours in "The line, drawn", `/research/deep-dives/` after Sources & method).

## Roots & Routes

`/roots/` is now a redirect stub to `/trees/` (Astro `redirects` in `astro.config.mjs`; the stub carries `noindex` and `tools/sitemap.py` withholds it). Its book chapter, its menu entry and `roots.embed.html` are gone. **Kept on purpose:** `/roots/view.html` (the frame behind "Where they lived" on 779 person pages), `site/public/roots-links.json`, `data/tree-page/` (`roots.html`, `tree.json`, `atlas-data.json`) and `tools/build-tree-page.py`: the per-person embed and the Atlas Tree Canvas read them.

## The inventory, in words

`menu_inventory.py compare` lists every old address as still answering (64 of 64). The blocks of text it reports as gone are all deliberate: the `/roots/` page itself (71 blocks), the sentences whose GitHub links became plain text (`/about/` 1, `/sources/` 2, `/documents/` 2, `/the-library/` 12, `/research-log/` 98, where a file name used to carry a trailing arrow), and the headings of `/changes/` (each now ends with the commit's short hash). `/people/` and `/who/` show "1 kept" in the same tool against an unchanged build of `origin/main` too (the tool does not index those two pages' rows); their `<main>` is byte-identical before and after.
