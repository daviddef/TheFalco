# The last harvest before the trial dies — FindMyPast, 15 September 2026

David's trial ends **16 September 2026**. This is the third and final sweep, and the first that
**enumerated the holding instead of stopping at the answer**.

`data/findmypast-australasia-2026-09-15.tsv` — **183 records**: 107 Falco travel, 39 Falco BMD and
cemetery, 21 Maione, 14 Carfora, 2 Zampiello.

## The thing worth taking through the paywall

**Not the transcripts. The identifiers.** A FindMyPast passenger transcript carries no age, no ship
and no port — only a name, a year and an **NAA barcode**, and *the NAA image is free forever*. So the
perishable asset was never the record; it was the list of pointers. That list is now saved.

**A trap caught before it was written down:** the id in the result href — `ANZ/AUSPASS/NAA/002630656`
— **is not the NAA barcode.** It is FindMyPast's own key. Carmine's 1964 arrival is `002630656` there
and **barcode 12100311** at the NAA. Recording 107 hrefs as barcodes would have produced a file of
plausible, checkable, wrong numbers.

## WHAT THIS CORRECTS IN THIS ARCHIVE

The September verdict said of this family: «*no electoral roll, no BDM, no cemetery index*», and
«**FindMyPast's entire holding for this family is passenger lists**».

**As a statement about the datasets, that was wrong.** With the travel-and-migration filter removed,
FALCO returns **56 BMD and cemetery records**, 39 of them Australian — Victoria and New South Wales
births, marriages and deaths from the 1890s, South Australian deaths, BillionGraves entries, and
four in Queensland — **three of which this archive had already assessed**, with more detail than FindMyPast gives:

| record | |
|---|---|
| **Bartolomeo Falco**, b. 1910, d. **1990** | Queensland Burials & Memorials |
| **Maria Margherita Falco**, b. 1913, d. **1986** | same register block — probably his wife |
| **Giuseppe Falco**, b. 1898, d. **1979** | buried **8 June 1979, Home Hill Cemetery**, aged 81 |
| **Giuseppe Falco**, m. **2 April 1932** | Queensland Marriages, reg. 1932/001027, to **Mary Rubiolo** |

**And this archive had already ruled on them.** `data/qld-bdm.tsv` carries Bartolomeo (1990/53930), Giuseppe (1979/C/1878 and the 1932 marriage) and Maria Margherita (1986/54962) — graded **candidate**, **candidate** and **not ours**, and naming a father FindMyPast never shows: **Domenico Falco**. Maria Margherita is not even a Falco by birth — her parents are Camisassia Francesco and Camilla Ramero. **My «never seen» was wrong.** What the FindMyPast pass adds is the burial place, *Home Hill*, and that is worth having: *Home Hill* is the **Burdekin sugar district of
North Queensland**, a thousand kilometres from Brisbane and the destination of a largely Sicilian and
northern-Italian cane-cutting migration; *Rubiolo* is a Piedmontese surname. Nothing ties them to Arienzo, and a **Domenico** Falco heads that household. The grading already in
`qld-bdm.tsv` stands; Home Hill strengthens it.

**The narrower claim survives**: for *this* family — Carminantonio, Filomena, Carmine — FindMyPast
still holds nothing but passenger lists.

## THE MAIONE LEAD, OPENED AND CLOSED THE SAME HOUR

Maione returns 66, and among them the first non-passenger Australian records this archive has met:

- **Antonio Maione** on the **Queensland electoral rolls** at **Winton (1913)** and **Charters Towers
  (1934, 1939)**, in the division of Kennedy;
- dead **28 September 1940**, buried **Charters Towers – Lynd**, **born 1864**, aged 76.

Costanza Maione, who married generation six at Arienzo in 1897, was born there in **1876**. A Maione
born 1864 and settled in Queensland by 1913 is exactly the shape of an elder brother — and it would
have explained why this family went to **Queensland** rather than Melbourne or Sydney.

**It is not him.** His civil death transcript names his father: «**Paschariels**» — Pasquale — and his
mother «Kogeta Saitaresa». **Costanza's father was ANIELLO Maione.** Different household.

**Recorded as a closed lead**, because it is the most attractive wrong answer this archive has been
offered in months: right surname, right state, right decade, and a motive.

## THE NILS, AND WHAT THEY ARE WORTH

- **ANNECCHINO — 0**, run twice, the second time on a nine-second render. Generation seven's wife's
  family is not on FindMyPast in any form.
- **ARRICALE — 0**, re-run on a ten-second render. A real nil.
- **ZAMPIELLO — 2 records on the entire site**, both **United States** WW2 draft cards (Anthony 1919,
  Sestilio E 1902). **Nothing Australasian at all.** The Arpaia line does not appear.
- **CARFORA — 86, of which 14 Australian**, all Western Australian and Victorian passenger lists plus
  Victoria Petty Sessions. **None in Queensland**, none reaching Maria Carfora of Forchia.

## Method, corrected

- **`sourcecountry=australasia` is a weighting, not a filter.** A Zampiello search under it returned
  two **United States** records and nothing else. Always read the record set per row.
- **The category filter hides whole classes of record.** The September nil was measured with
  travel-and-migration selected. **Run every surname with no category before calling anything a nil.**
- **A zero must be re-run** — a slow client render is indistinguishable from a real nil. Annecchino's
  zero survived a second pass at nine seconds; Arricale's has not been re-run yet.
- **Page the full surname list; never trust a truncated forename.** «carm» returns nothing where
  «carminantonio» returns the record.
- **Sequential FindMyPast ids mean one NAA volume**, not one voyage — the ids are assigned
  alphabetically within a batch. That is why Filomena (`010827216`) and the withheld Francesca
  (`010827217`) are adjacent although they arrived four months apart.
