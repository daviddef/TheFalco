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

## The sweep — branch surnames, Australasia, name variants on

**Every count is PAGE ONE (twenty rows).** Totals are not captured and «no Queensland» means *not on
page one*. Only **Arricale** produced the rendered words «**No results found**», which is the one
result here that is a true nil.

| Surname | p1 | Queensland | what is in it |
|---|---|---|---|
| **Militano** | 20 | **4** | **THE ONE QUEENSLAND FIND** — see below |
| Falcone | 21 | 0 | Passenger Lists (Victoria, NSW) |
| Biondo | 21 | 0 | Passenger Lists (Vic); **NSW Deceased Estate Files 1880–1923**; WW2 Allies |
| Mazza | 21 | 0 | Passenger Lists |
| Zavaglia | 21 | 0 | Passenger Lists; WW2 Allies; **Australia, Parish Deaths & Burials 1814–2014** |
| Carfora | 21 | 0 | **Western Australia** arrivals 1959–67, plus US WW2 mis-tagged |
| Cimmino | 20 | 0 | 14 Australia, 6 United States |
| Zaino | 20 | 0 | 9 Australia, 11 United States |
| Crisci | 20 | 0 | Passenger Lists, US WW2 |
| Vigliotta | 9 | 0 | **Western Australia** arrivals, US WW2 |
| **Abatiello** | **5** | 0 | **every row a UNITED STATES WW2 record** mis-tagged into the Australasia filter — the same fault the September sweep found for Zampiello |
| **Arricale** | **0** | — | **«No results found» — a TRUE NIL** |

### The Queensland find, and why it is a lead and not a link

**CONCETTA MILITANO on the Australia Electoral Rolls at INNISFAIL** — Herbert division 1939 (as
«Coneetta») and 1941, Leichhardt division 1949 and 1959. Four entries across twenty years.

**Innisfail is North Queensland, about fourteen hundred kilometres from Brisbane**, and this archive
has already met that pattern: the FindMyPast Maione cluster is at **Winton and Charters Towers**,
also North Queensland, and was logged as unconnected. **Nothing joins Concetta Militano to this
family.** It is recorded because MILITANO is a branch surname here and the next reader will want it.

**And the living-people rule binds what can be said.** The Militano reach this family through a
marriage in the living generations; anything published about them is a name and a relationship.

### Record sets not in the September list of «holdings worth remembering»

**NSW Deceased Estate Files 1880–1923** · **Australia, Parish Deaths & Burials 1814–2014** ·
**Victoria Wills & Probate** · **Victoria Petty Sessions Registers** · **Britain & Ireland, Incoming
Passenger Lists 1878–1960**. The September note listed four; there are at least nine.

## Still to do

The surnames above were **never swept** — 9 September covered Falco, Raffaele Falco, Annecchino,
Zampiello, Servodio and Maione only. Remaining: **Zaino, Militano, Isla, Reid, Halliday, Ellevsen,
Dreghorn, Arricale, Carfora, Cimmino, Crisci, Vigliotta, Morgillo, Diglio, Rivetti, Cioffi**, and
the living branches' names — for which **the living-people rule binds anything published**.

**Do not bother with the Italian sets.** They are the IGI, already harvested.
