# What FamilySearch holds, town by town, against what this archive has read — 18 October 2026

**Method.** FamilySearch's browse trees (open, no login: `…/service/cds/recapi/collections/<id>/waypoints`, add `&offset=0&count=1000`) were walked
for the three civil collections, every volume's image count taken from the volume's own `results`, and 5,492 volumes tallied. The «read» side
was extracted by a separate pass over `searched.json` (184 rows), the per-year notes and the work list, conservatively: **«full» only where a row
says every act was read.** The extraction is in the session scratchpad, not the repo; the figures below are the ones to rely on.

## What FamilySearch actually holds
| Collection (id) | Towns | Years held | Notes |
|---|---|---|---|
| Caserta State Archive 1809–1866 (2718545) | **Arienzo** 820 vols / 67,924 images | Nati, Matrimoni, Morti **1809–1865 complete**; processetti 1809–35, 1837–65; marriage and death indexes 1809–49 | the richest holding |
| | Cervino 774 vols / 27,552 | N/M/D 1809–1865 | |
| | **Santa Maria a Vico** 694 vols / 64,638 | N 1811, 1813–14, 1817–65; M 1809–11, 1813–14, 1817–65; D 1809–14, 1817–64 | |
| | **San Felice a Cancello** 32 vols / 7,646 | **1863–1866 only** | nothing earlier on FamilySearch |
| | **Forchia** 606 vols / 13,898 | N/M/D 1820–1865 | Forchia was in Terra di Lavoro until 1861 |
| | San Marco Evangelista, Valle di Maddaloni | 1863–65 only | |
| Caserta Tribunale 1866–1929 (2043630) | Arienzo 5 vols / 9,884 · Cervino 11 / 9,908 · San Felice 8 / 19,233 · Santa Maria a Vico 7 / 16,079 | **1866–1910 only, not to 1929** | the collection title says 1929; the towns stop at 1910 |
| Benevento State Archive 1810–1942 (2475030) | **Forchia** 199 vols / 9,684 | N 1809–1915 (gaps incl. 1897); M and D **1809–1860 and 1931–1942 only** | |
| | **Arpaia** 315 / 12,213 · Moiano 329 / 23,118 · Airola 338 / 41,621 · Durazzano 201 / 17,070 · Paolisi 522 / 23,763 · Montesarchio 403 / 43,917 | N to 1915 with gaps; M and D 1809–1860 and 1931–1942 | Arpaia: marriage **banns 1887**, an index 1866–75 |

**The structural finding: for the Benevento towns there is NO civil marriage or death register on FamilySearch for 1861–1930** (marriages for that span
exist for 19 of the collection's 100 comuni, deaths for 8, mostly one stray volume), and **for Arienzo, Cervino, San Felice and Santa Maria a Vico the
Tribunale copy ends in 1910 — nothing for 1911–1929 anywhere online.** Antenati has the same gaps. Parish (church) registers are a separate layer
(FamilySearch full text) that was **not walked here**.

## What this archive has read (conservative)
- **Arienzo, Antenati 1809–1865.** Deaths: **40 of 57 years read in full** (1809–1843, 1860–1864 by tagged rows); 1844–59 through the annual indexes with acts opened for Falco hits;
  the 45-volume *Diversi* series read end to end. Births: 1809–1838 read in full (1834 doubtful), 1839–1852 swept at one or two bands (the archive's own rule
  says one band can miss a Falco father), **1853–1865 not read**. Marriage *registers*: 1814–15, 1843–48, 1850–65 in full; 1809–13 and 1816–42 through the indexes. **Processetti: about 5 of 63 volumes opened.**
- **Arienzo, FamilySearch Tribunale 1866–1910.** Deaths 1868–1886 read in full; births and marriages 1884–86 and 1878–86 in full; 1866–77 scattered; **almost nothing read after 1889**; all banns and the 1901–10 volume unread.
- **Arienzo parish (full text).** Searched by surname with a few dozen acts read from the image: partial.
- **San Felice a Cancello.** Marriages 1809–14 and 1816–17 in full; the rest unread.
- **Santa Maria a Vico.** Marriages 1866–87 a mixture of index and full; a few deaths; births almost unread.
- **Forchia, Arpaia, Moiano, Paolisi, Airola, Durazzano, Cervino, Valle di Maddaloni.** Name-index searches and **selected acts only** (Forchia births 1857 and 1883, a handful of 1937–39 acts); no register read end to end.

## Corrections this produced
The pages said «**68 consecutive annual death registers read in full, 1809 through 1883, every year Antenati holds**». It was **40 of 57 (1809–1843, 1860–1864)**: the *Diversi* series, which carries the tags «Deaths · read in full» and the range 1812–1865, filled in 17 years it never read, and years after 1865 are FamilySearch's, not Antenati's. Retagged and the three sentences rewritten.
The extraction also names 19 unsupported or inconsistent claims, now work-list row 109 (processetti «three bundles read» vs five opened, «258 unread», «eleven registers», «21 volumes», and others).


## Addendum, 18 October 2026 — births 1853–1865 now read

The thirteen Arienzo birth registers of 1853–1865 (`an_ua14450`–`an_ua14462`) were read end to end the
same day this table was written; work-list row 110 and the thirteen `searched.json` rows of that date
record it. **Births at Arienzo are now read in full for 1809–1838 and 1853–1865; 1839–1852 remain
swept at one or two bands.** Nothing else in the table above changes.
