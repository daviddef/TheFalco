# Falco Family

## Record Atlas

The shared map lives at `../Record Atlas`. Research done here is only
useful to the next person if it gets there.

Invoke the `record-atlas-feedback` skill whenever you finish a search,
open a register, write to an archive, or find a source the atlas does
not list — as you do it, not in a sweep at the end. Record the
FamilySearch waypoint, not just the film number; the skill explains why.

## Surname spellings

Surname spellings come only from the Record Atlas catalogue: run `terms` before searching, `cover` before any nil, `add` for every new spelling, `publish` once at the end. Keep no variants list here.
Pointer: Atlas surname page https://recordatlas.org/surname/falco/ and
`python3 "/Volumes/DJ - Crucial - 4TB-SSD/Claude Projects/Family Projects/Record Atlas/scripts/surname_variants.py" terms Falco`.
Use the `surname-variants` skill. The /name/ page table is a generated snapshot of the catalogue: after a `publish`, run `python3 tools/pull_surname_catalogue.py` and commit `site/src/data/atlas-surname-falco.json`. Person-level aliases (one person spelt two ways) stay here.

## Given names and old place names

Given-name forms (Ivan = Johann = Giovanni = Zuane = Joannes) and a place's name in the year of the record (Salisbury before 1982, Fiume before 1945) come only from the Record Atlas catalogues, as surnames do: invoke the user-level `name-variants` skill, run `given_name_variants.py terms` / `place_names.py at PLACE YEAR` before searching, `cover` before any nil, `add` (with evidence) for every new form, `publish` once at the end. Keep no table of given-name forms or old place names here. Nothing about a person goes in the catalogues; `lead` is never a finding.
