# FindMyPast — full sweep of the family surnames, 9 September 2026

Searched on a subscription trial, signed in, with name variants on. Every count below is
FindMyPast's own. The verdict first, because it is mostly a negative one.

## Verdict

**FindMyPast adds almost nothing to this family — with one exception that may matter a great deal.**

- **Its Italian records are the FamilySearch index this archive has already harvested.** Every
  transcript in *Italy Births & Baptisms 1806–1900*, *Italy Deaths & Burials 1809–1900* and *Italy
  Marriages 1809–1900* carries the line **«Index (c) IRI. Used by permission of FamilySearch Intl»**
  — it is the IGI, re-hosted. Nothing there is new.
- **Its Australian records do not contain the Brisbane family at all.** Not one of them.
- **The exception:** a Brisbane arrival that fits Carminantonio Falco, from a record set this
  archive had not searched — the National Archives passenger lists, indexed by FMP.

## The one real lead

### Carmine Falco — arrived Brisbane, 26 March 1964, per the *Sydney*, out of Naples

> First name(s) **Carmine** · Last name **Falco** · Arrival date **26 Mar 1964** ·
> Ship name **Sydney** · Departure port **Naples** · Destination port **Brisbane** ·
> State **Queensland** · NAA barcode **12100311**
> *Australia, Inward, Outward & Coastal Passenger Lists 1826–1972* (National Archives of Australia)
> Image: `https://recordsearch.naa.gov.au/SearchNRetrieve/Interface/ViewImage.aspx?B=12100311&S=1`

This archive's standing question reads: *«When did Carminantonio and Filomena arrive? Before 1964.
Both died in Brisbane, but neither appears in the passenger arrivals index… the voyage is
untraced.»* This is a Falco with his forename, sailing from **the port that serves Arienzo**, into
**Brisbane**, in **1964**.

**It is a lead and not a finding.** The index gives no age, no birth year and no companion. The
name Carmine Falco is not rare among Campanian emigrants. What would settle it is the **image
itself** — barcode 12100311 at NAA RecordSearch, which lists age, occupation, last address and
often the nominator. That is an ordinary next step, not a blocked door.

### Filomena Falco — arrived 5 February 1968

> Arrival date **05 Feb 1968** · Ship **—** · State **—** · NAA barcode **9788535**, page 251

Weaker: the index gives no ship, no port and no state, so it does not even place her in Queensland.
Filomena Annecchino married Carminantonio Falco and would be indexed as Filomena Falco. Worth
pulling the image; worth asserting nothing until then.

Both are recorded in `data/findmypast-harvest.tsv`.

## The nulls, which are most of the result

| Search | Scope | Result |
|---|---|---|
| **Raffaele Falco** | Australia & New Zealand, all sets | **0** |
| **Annecchino** (variants on) | Australia & New Zealand, all sets | **0** |
| **Zampiello** (variants on) | Australia & New Zealand, all sets | **2 — and both are United States WW2 records** that the region filter has mis-tagged. Nothing Australian. |
| **Zampiello**, travel & migration | worldwide | **81, every single one to the United States** — Connecticut, New York, Vermont border crossings. Not one to Australia. |
| **Zampiello** | worldwide, all sets | 218 — Connecticut, California, Rhode Island, New Jersey. A different Zampiello migration entirely. |
| **Annecchino** | worldwide | 329 — Italy (the IGI index), New York, New Jersey, one London electoral register. |

So the **Zampiello of Arpaia who reached Queensland, and the Annecchino of Forchia, leave no trace
whatever in FindMyPast.** That is worth knowing: it closes a search rather than opening one.

## The Queensland Falco are a different family

Falco in Australia & New Zealand: **549** — of which Birth/Marriage/Death **56**, census & land
**31** (all *Australia Electoral Rolls*), directories **42**, travel & migration **170**, and
"military" **233** which on inspection are **United States** WW2 records leaking through the region
filter. All 56 BMD and all 31 electoral-roll entries were read.

Every Queensland Falco in them belongs to one household in the **Burdekin**, the North Queensland
cane country — about 1,200 km from Brisbane:

- **Giuseppe Falco**, b. 1898, married **Mary Rubiolo** on 2 April 1932 (Queensland reg
  1932/001027), buried **8 June 1979, aged 81, Home Hill Cemetery**; on the electoral roll at
  **Ayr** in 1934, 1939, 1941, 1949 and 1959.
- **Bartolomeo Falco** (1910–1990), **Maria Margherita Falco** (1913–1986), **Primo**, **Raymond**
  and **Laurence** Falco, all at Ayr; **Arthur Michael Falco** at Mount Isa, 1959.

**This bears on an open question.** The archive wondered whether the *Giuseppe Falco* who reached
Brisbane on the *Palermo* on 15 September 1925 was Raffaele's brother, born 1883, and the anchor the
chain hung from. The Giuseppe Falco FindMyPast has in Queensland was **born about 1898, married a
Piedmontese wife, and lived and died in the Burdekin**. He is almost certainly **not** that man, and
the 1925 Giuseppe remains untraced.

The rest of the Australian Falco are at Ayr, Mount Isa, Port Pirie, Carlton, Richmond and Sydney —
Sicilian, Basque and North-Italian families with no connection here.

## Also searched

- **Servodio**: 261 worldwide; **14** in Australia & New Zealand, of which 8 are Western Australian
  passenger arrivals 1952–1972 (Angelo, Antonio, Giovanni, Maria, Maria Luigi, Michele, Pasqualina,
  Raffaela). The archive's Servodio is a **Queensland** married name. Different stream; logged as a
  lead, not a link.
- **Maione**: 66 in Australia & New Zealand, with a genuine Queensland cluster — **Antonio Maione**,
  b. 1864, on the electoral roll at **Winton** in 1913 and **Charters Towers** in 1934 and 1939,
  died 1940. North Queensland again, and unconnected to Costanza Maione of Arienzo so far as
  anything here shows.

## Record sets worth remembering

FindMyPast's genuinely distinctive holdings for this family, should a name ever surface:
**Australia Electoral Rolls**; **Queensland Burials & Memorials** (Genealogical Society of
Queensland); **Queensland Marriages 1829–1939**; and **Australia, Inward, Outward & Coastal
Passenger Lists 1826–1972**, which is the NAA index and the one that produced the Carmine Falco
arrival.

## Method

Results are client-rendered; the HTML fetched directly is an empty shell. What works is to navigate
the tab and read the rendered table, or to load the URL in a hidden same-origin iframe and poll for
`tr` elements. Useful parameters: `lastname`, `firstname`, `lastnamevariants=true`,
`firstnamevariants=true`, `sourcecountry=australasia`, `sourcecategory=…`, `_page=N`.
**A page that renders slowly returns zero rows and looks exactly like a genuine nil result** — every
zero above was re-run before being written down.
