# Four sources this archive had never opened — 15 September 2026

Find a Grave, BillionGraves, Trove and Matricula had **zero mentions** in an archive of 11,760
register rows. One of them rewrote a generation; three are now closed with reasons.

## 1. FIND A GRAVE — the largest single find of the year

See [nudgee-graves.md](nudgee-graves.md) and `data/nudgee-graves.tsv`. Five Falco memorials in
**Nudgee Cemetery and Crematorium**, Brisbane, four carrying **transcribed Queensland death
registrations with the parents named**. It dated Carminantonio (1900–1985) and Filomena (1897–1988),
**settled Filomena's contested birth at Forchia**, produced **a whole generation the archive lacked**
— Raffaele Falco, b. Forchia 25 Aug 1925 — and **joined the Falco to the Zampiello** through his wife
Caterina.

**HOW IT NEARLY PRODUCED TWO FALSE NILS.** Find a Grave's `locationId` values are opaque integers and
**not guessable**:

| place | id |
|---|---|
| **Australia** | `country_15` |
| **Queensland** | `state_576` |
| City of Brisbane | `county_14218` |
| Nudgee | `city_599794` |

A guessed **`country_14` is SWITZERLAND**. It returned «*13 matching records found for Falco ×
Australia*» — thirteen graves in **Basel, Ticino, Vaud and Fribourg** — under a heading that says
Australia. The first Queensland search used an invented `state_2681` and reported a clean **"No
matches found"**. **Both of this session's opening searches were fiction, and one of them was fiction
that looked like data.** Take ids from the "See more … memorials in:" links at the foot of any
memorial. And set `includeMaidenName=true`: it is the only reason **Caterina *Zampiello* Falco** is
findable, since she is indexed under FALCO.

## 2. BILLIONGRAVES — already held, by another name

Its own search would not complete in a headless browser: the page sits on «*Please wait while we
search*» indefinitely.

**It did not need to.** FindMyPast indexes the **Australia BillionGraves Cemetery Index**, and this
session enumerated it for the relevant surnames. Every Australian BillionGraves entry for these names
is **South Australian** — Falco Filomenia at Port Elliot, Falco Francesco and Luigia at Cheltenham,
Maione Pasquale at Payneham South, Maione Giuseppe at Cheltenham. **None in Queensland.**

**Worth saying plainly:** a source can be covered through an aggregator, and checking the aggregator
first would have saved the attempt.

## 3. TROVE — a real nil, and an assumption of mine that the data killed

- **ANNECCHINO — no results.**
- **ZAMPIELLO — no results.**
- **FALCO** returns plenty and **none of it is this family**: Queensland hits are all pre-1947 and
  dominated by a serial called *Falconhurst* and by OCR breaking «Falcon» into «Falco[?]».

**I assumed the nils were explained by copyright — that Trove's digitised newspapers stop about 1954,
before this family arrived in 1964. That was wrong, and the search said so:** Falco across Australia
in **1960–1969 returns 753 results** (the *Snowy River Mail* to 1970, the *Australian Jewish News* to
1999). **Trove reaches the decades in question.** The Annecchino and Zampiello nils are therefore
**real absences, not coverage artefacts**.

**What is NOT established:** whether Trove digitises any *Queensland* paper for the 1960s. The
`l-state=Queensland` + `l-decade=196` combination renders an empty results panel with no count and no
"no results" message, and no reading could be got from it. **No coverage claim is made here**, and the
convenient explanation — "the Courier-Mail isn't in Trove" — is **not asserted**, because it was not
tested.

## 4. MATRICULA — closed in a single pass

Matricula Online's **entire Italian holding is two dioceses**: **Reggio Calabria** and
**Südtirol / Bozen-Brixen**. There is **no Campania**, so nothing for Arienzo, Forchia, Arpaia,
Moiano or anywhere in Caserta or Benevento.

**This is the cheapest negative in the archive** — one page of a dropdown — and it is worth recording
precisely because it looks like it ought to be a good source and is not.

## Still not done

**Ancestry and MyHeritage for the Australian end.** Ancestry's *Australia, Electoral Rolls
1903–1980* was visible on the Find a Grave pages for Raffaele Falco and Caterina Zampiello, which
means the rolls place them at an address. Naturalisation files are the other target. Both need a
subscription this archive does not currently hold.
