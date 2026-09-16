# FindMyPast, 16 September 2026 — the method notes are wrong about the domain

**David opened a one-month full subscription and asked whether FindMyPast had been run through.**

## It had — twice, and both times signed in

- `notes/findmypast-sweep-2026-09-09.md` — full surname sweep **on a subscription, signed in**.
- `notes/findmypast-arrivals-2026-09-13.md` — re-swept **from inside the paywall**.

The memory line about a verdict «measured from outside the paywall» refers to an **earlier September
verdict that those two sweeps corrected**, not to the sweeps themselves.

**What they established:** no FMP tree; the Italian sets are the **IGI re-hosted** («Index (c) IRI.
Used by permission of FamilySearch Intl») and are not a second source; the Australian holding for
this family is **six passenger-list records**; **Annecchino 0**; Zampiello's 218 worldwide records
are a **United States** migration entirely.

## THE DOMAIN IS `findmypast.co.uk`, NOT `.com.au`

**This is the finding.** Every method note in this archive says `www.findmypast.com.au`. The live
subscription session answers on **`www.findmypast.co.uk`**. Hitting `.com.au` redirects to
`auth.findmypast.com/login` with `initialScreen=signUp` — **indistinguishable from not having a
subscription at all**, which is exactly how an hour gets lost.

    https://www.findmypast.co.uk/search/results?sourcecountry=australasia&lastname=<X>&lastnamevariants=true

## Two more corrections to the recorded method

1. **Offscreen iframes no longer render.** The 9 September note says to «load the URL in a hidden
   same-origin iframe and poll for `tr` elements». Five iframes reached `readyState: complete` on
   the right path with **`body.innerText.length === 0`**. The SPA does not paint offscreen. Navigate
   the tab instead.
2. **The render takes longer than six seconds.** A read issued in the same batch as the navigate
   returned `rows: 0, text: ""` for a search that returns twenty-one rows. **Poll until `tr` > 0 or
   a no-results string appears** — never record a zero that arrived with an empty body. This is the
   false nil the 9 September note warned about, and it is still the main hazard.

## First tranche — the branch surnames never swept

Australasia, name variants on. **These are PAGE ONE counts, not totals**, and «no Queensland» below
means *not on page one* — it is not a nil.

| Surname | rows p1 | Queensland p1 | record sets seen |
|---|---|---|---|
| **Falcone** | 21 | 0 | Passenger Lists 1826–1972 (Victoria, NSW) |
| **Biondo** | 21 | 0 | Passenger Lists; **NSW Deceased Estate Files 1880–1923**; WW2 Allies |
| **Mazza** | 21 | 0 | Passenger Lists |
| **Abatiello** | **5** | 0 | **WW2 Allies only — every row a UNITED STATES record** mis-tagged into the Australasia filter, the same fault the 9 September sweep found for Zampiello |
| **Zavaglia** | 21 | 0 | Passenger Lists; WW2 Allies; **Australia, Parish Deaths & Burials 1814–2014** |

**Two record sets here were not in the 9 September list of «holdings worth remembering»:** *NSW
Deceased Estate Files 1880–1923* and *Australia, Parish Deaths & Burials 1814–2014*.

## Still to do

The surnames above were **never swept** — 9 September covered Falco, Raffaele Falco, Annecchino,
Zampiello, Servodio and Maione only. Remaining: **Zaino, Militano, Isla, Reid, Halliday, Ellevsen,
Dreghorn, Arricale, Carfora, Cimmino, Crisci, Vigliotta, Morgillo, Diglio, Rivetti, Cioffi**, and
the living branches' names — for which **the living-people rule binds anything published**.

**Do not bother with the Italian sets.** They are the IGI, already harvested.
