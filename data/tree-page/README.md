# Roots & Routes (the tree page)

Ten views of the people this archive holds who have died: hourglass, fan, whole-tree and close-family maps, Atlas map, movements, kinship, place lanes,
eras, lifespans, an Orphans tab, the five animated views (Night sky, Ink ledger, Household, Generations, Where they lived) and a Surnames cloud. It is served
at `/roots/`.

| File | What it is | Edit by hand? |
|---|---|---|
| `tree.json` | people, parent links, years, places | no, generated |
| `place_map.json` | each place string with coordinates, country and Record Atlas id | no, generated (see below) |
| `place-additions.json` | place strings decided by hand, each with its reason | yes, with a reason |
| `atlas-data.json` | the Record Atlas slice: outlines, regimes, flags, events, collections | no, generated |
| `roots.html`, `roots.embed.html` | the page, whole and as a fragment for the site layout | no, generated |
| `tree.report.json` | counts, the adapter's own numbers, and the 21 people whose estimated birth falls after their recorded death | read it |
| `people.ged`, `slugs.json` | intermediates, not committed | no |

## Rebuild

```bash
python3 tools/build-tree-page.py           # rebuild everything and run the page's own checks
python3 tools/build-tree-page.py --check   # exit 1 if the page is older than the data it was built from
```

Needs the Record Atlas checkout (`RECORD_ATLAS`, default `~/Projects/Family Projects/Record Atlas`), read only. The skill's scripts are vendored in
`tools/tree-page/` (the family-tree-page skill, template 1.7.0), so CI and other sessions do not depend on `~/.claude`.

## What is and is not on the page

- **No living person.** The people are `site/src/data/people.json`, less everyone it flags `living` (47), anyone `data/living-by-inference.json` lists, an
  undated person beside a living one, and a person with no name. The converter adds its floor: nobody with no death recorded and a birth year (estimated
  ones included) after 1916. The page's own check fails the build on a living person's name.
- **Not drawn, and why** (of 1,097 in people.json, 708 are drawn): 47 living; 13 held back by this adapter; 300 with no birth year, recorded or estimable
  from a relative, or born after 1916 with no death recorded; 8 with no place; 21 whose estimated birth falls after their recorded death (listed in
  `tree.report.json`, `conflicts`).
- **Colour is the surname family**, from the Record Atlas catalogue (`data/surname-families.json`, read only) where it has the name, and the surname itself
  where it does not. This archive keeps no list of spellings.
- **Sex is stated, never guessed.** people.json has no sex field. The page takes one only where the archive's own data states or entails it: a household
  role such as father, mother, husband or wife (315 people) or the register's own words such as "son of" (10). Everyone else (712 of the 1,037 offered to the
  converter; 521 of the 708 drawn) is `u`, unknown: the fan leaves the slot open and Kinship says "parent", "child", "sibling" and not "father" or "uncle".
  Sex is no longer inferred from the ending of a given name. A sex field in people.json would replace all of this.
- **Places are never guessed.** 181 place strings come from `data/era-ground.tsv` (the town decided for each string as printed, point from
  `data/era-towns.tsv`, country from the Atlas's `geo.country_of`); 3 from `place-additions.json` (Benevento, with the reason). Nothing is taken from the Atlas
  by name alone: `Italy` and `Italia` (a country), a ship or a journey, and two New York strings stay unresolved. A person with no recorded birth place is drawn
  at a relative's (284 people) and marked, in their panel and on the maps, as `place taken from a relative`.
- **Estimated years are flagged**: "c. 1809" is a birth estimated from a parent, child or spouse; "1809–?" is a death not recorded; a death date that is
  only a limit in the register ("before 1825", "dead by 1878") is shown as that limit, flagged.
- **A parent link read in a register is drawn solid; one that only the family tree gives is drawn dashed.** A retracted parentage (`superseded`) and a
  duplicate the archive keeps apart on purpose (`sameAs`) are not drawn.
- **Not in the Record Atlas yet** (grey pins): Capua, Frosinone, Galluccio, Nola, and Napoli (the Atlas has Naples without the Italian name).
