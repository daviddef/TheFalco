# THE PARENTS FOLLOWED THE SON — Carminantonio and Filomena's arrivals, found at last

**FindMyPast, 13 September 2026, on David's trial subscription** — and this time **from inside the
paywall**, which is the whole difference.

## The question this closes

`/open-questions` has carried, for weeks:

> «**When did Carminantonio and Filomena arrive?** Neither is in the passenger index. …neither has
> been found in any passenger list.»

**They are both in it.**

| | arrival | NAA barcode | page |
|---|---|---|---|
| **FILOMENA FALCO** | **5 February 1968** | **9788535** | S=251 |
| **CARMINANTONIO FALCO** | **19 May 1969** | **12211391** | S=1711 |
| *(and again)* **CARMINATONIO FALCO** | **24 July 1972** | **12047001** | S=1605 |

Set beside the arrival this archive already held — **Carmine Falco and his wife, 26 March 1964, per
the *Sydney* out of Naples, barcode 12100311** — the shape of it is plain:

> **The son crossed first. His mother followed nearly four years later, and his father sixteen months
> after her.** Then, in 1972, the father crossed again.

That is chain migration as it actually happened in one family, and the archive now has the dates for it.

## What is NOT established

- **The transcripts give no age, no ship and no port.** Only a name, a year, an arrival date and an
  NAA barcode. **The identification rests on the forename** — *Carminantonio* is not a name that turns
  up twice — **and on the dates falling exactly where the family's own account puts them.**
- **The NAA images are the proof**, and they are one click away for each:
  `recordsearch.naa.gov.au/SearchNRetrieve/Interface/ViewImage.aspx?B=<barcode>&S=<page>`. That is
  exactly how the 1964 voyage was proved, and none of these three has been pulled yet.
- Two further records sit beside these and are **deliberately not published**: a **Francesca Falco**
  arriving 9 June 1968 (same NAA volume as Filomena, S=253) and a **Giorgia Falco** arriving 28 August
  1972 (same volume as the 1972 crossing, S=1607). They may be family and they may not, **and this
  archive cannot show that either is deceased**, so no date for either goes on the site.

## AND IT CORRECTS THIS ARCHIVE'S OWN VERDICT ON FINDMYPAST

On 9 September this archive swept FindMyPast on a trial and concluded:

> «**Its Australian records do not contain the Brisbane family.**» …with the single exception of
> Carmine's 1964 arrival.

**That was measured from outside the paywall and it was too strong.** The travel-and-migration
category alone holds **170 Falco records for Australasia**, and **six of them are this family**.

**What the September verdict got right stands**: *Raffaele Falco: 0. Annecchino: 0.* Re-run today,
**Annecchino still returns nothing at all** in travel and migration, and neither Carminantonio nor
Filomena appears in **any** other Australasian category — no electoral roll, no BDM, no cemetery
index. **FindMyPast's entire holding for this family is passenger lists.** It is just six records
deep, not one.

## And the answer to «is there a FindMyPast tree?»

**No.** `/tree/all-trees` redirects to a tree-creation form. The family tree lives on **MyHeritage**,
which this archive already harvests — there is nothing on FindMyPast to read.

## Method note

The record is client-rendered and the search URL takes `sourcecategory`, `sourcecountry`, `lastname`,
`firstname`, `lastnamevariants`, `firstnamevariants` and `_page`. **A transcript is at
`/transcript?id=<the row's href>` and carries the NAA barcode and page** — which is the only part
worth having, because the image is at the NAA and free.

**A first-name filter that returns zero is not a nil.** «carm» returned 0; «carminantonio» returned
the record. **Page the full list instead of trusting a truncated forename.**

## The living-people check, and what it nearly did

Before any of this was published the archive's rule was applied: **living people are named and
nothing more.** `site/src/data/living.json` contains **«Carmine Falco»** — and the site already
prints a Carmine Falco's 1964 arrival with a date and a Brisbane street address. That looks exactly
like a breach, and the entry was about to be pulled.

**It was a homonym.** Read by tree id rather than by name:

- **id 4512779 — «Carmine Falco», no dates at all.** This is the man on the living list.
- **id 4000025 — «Carmine Falco», born Forchia 8 June 1930.** Generation eight, David's wife's
  grandfather, **died 2026**, already excluded from the living list by `build_living.py`'s ancestor
  filter and already carrying his dates in `line.json`.

Nothing was published in breach. But the near-miss is worth keeping, because it runs the opposite way
to the three leaks the release gate was built to stop: **a name-level check was about to delete a
true fact about a dead man.** Redaction needs identification exactly as much as publication does.
