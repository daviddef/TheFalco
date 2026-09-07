# Falco — key findings

Established 7 September 2026, from the MyHeritage tree plus FamilySearch.

## The line

Nine generations, Arienzo → Arpaia/Forchia → Benevento → Brisbane. Eight rest on a named record.
Full table in `data/direct-line.tsv`.

## The three welds

A pedigree is only as good as its joins. Three records carry this one, each naming a father:

| Record | Ark | Joins |
|---|---|---|
| Death of Vincenzo Falco, 15 May 1875, Arienzo — "Vincenzo Falco and Pasquale" | `X36H-M66F` | gen 3 → 2 |
| Death of Raffaele Falco, 21 Apr 1880, Arienzo — "Raffaela [Raffaele] Falco and Vincenzo" | `X36H-P5SY` | gen 4 → 3 |
| Birth of Carmine Antonio Falco, 10 Jul 1850, Arienzo — "and Raffaele Falco" | `6Y2Z-5G8Q` | gen 5 → 4 |

## Pasquale Falco and Chiara Rivetti are real — found in the parish registers

Six baptism entries in the Arienzo registers name them together as a married couple of the parish:

- **24 Feb 1794** — "baptizavit infantem natam ex *Paschale Falco*, e *Clara Rivetta* Conjugibus huius
  Parochia, cui dedit nomen Maria Raphael[a]" (`3Q9M-CSD3-13CH-F`)
- **28 [Oct] 1795** — "ex *Pascale Falco*, et *Clara Rivetti* Conjugibus huius insig[nis]
  archipresb[yteralis] collegiat[a] eccles[ia] S[anc]ti Andreae" (`3Q9M-CSD3-13CC-6`)
- **18 Jun 1799** — son **Domenico** (two register copies: `3Q9M-CSD3-13KF-W`, `3Q9M-CSD3-1382-C`)
- **2 Feb 1802** — daughter **Maria Angela** (`3Q9M-CSD3-13LV-H`)
- one further entry read as **1780** (`3Q9M-CSD3-1386-4`) — see the date problem below

**The parish is named in full**: the *insignis archipresbyteralis collegiata ecclesia Sancti Andreae*
of Arienzo — the Collegiate Church of St Andrew the Apostle.

## The case against Agostino Falcone — generation 1 does not hold

The tree carries the line one further generation to **Agostino Falcone** (b. c.1740) and
**Elisabetta Sabina** (b. c.1745). This is not supported:

1. **Different surname** — *Falcone*, not *Falco*.
2. **Falcone is not an Arienzo name.** Across 361 Arienzo baptism-register pages mentioning a Falco,
   *Falcone* appears on **2**, both in index lists. Compare *Crisci* 113, *Morgillo* 76, *Martone* 49,
   *de Lucia* 40, *Rivetti* 17, *Arricale* 15. A family resident in the parish leaves a trace of that
   order of magnitude. Falcone did not.
3. **The Falcone in the baptism text is the officiating priest** — "de nostri licentia D. … Falcone
   baptizavi infantem" — not a parent.
4. **No citation exists** for either him or his wife, while every generation below carries one.
5. **FamilySearch's index conflates Falco and Falcone**, returning both for either query — verified:
   identical result counts in all four collections. A researcher can acquire a Falcone ancestor from
   that index without ever choosing to.

Conclusion: the honest frontier of this pedigree is **Pasquale Falco**, not Agostino Falcone.

## A date problem worth resolving

Tree gives Pasquale b. 1765, Chiara b. 1772. One baptism entry for the couple reads **1780** — at
which Chiara would have been 8. Either the machine reading of the date is wrong (most likely — digits
are the least reliable part of handwriting recognition) or the birth years are. Needs a human eye on
`3Q9M-CSD3-1386-4`.

## The move north was four kilometres, not a migration

Every Falco generation from Pasquale to Raffaele is born, married and buried at **Arienzo**. Then in
**1913** a son, Gerardo, is registered at **Arpaia** — 4 km away, but across the provincial line into
Benevento. From there: Forchia (1930, 1933, 1938), Benevento (1955), Brisbane.

The paper trail appears to break in 1913. It does not — the records simply move from the Archivio di
Stato di Caserta to the Archivio di Stato di Benevento.

## Geography and the Lombard question

Arienzo, Arpaia and Forchia lie along the **Valle Caudina**, in the orbit of **Benevento** — capital
of the Lombard duchy that outlasted the northern kingdom by three centuries. Since *Falco* is a
common **Lombard personal name**, the patronymic origin is the more likely of the two here. This is
a hypothesis consistent with the geography, not a documented fact, and is labelled as such.

**Forchia** is named for the *Forche Caudine* — the Caudine Forks, where a Roman consular army was
made to pass under the yoke in 321 BC.

## Zampiello (the maternal line)

- **Angelo Zampiello** b. 31 Aug 1895, d. 1972. **Military service in the Second Italo-Abyssinian
  War, 1935**; served in Eritrea; family record says he saved a large number of people and was
  decorated. *Unverified — no citation. Worth pursuing in Italian military records.*
- m. **Giuseppa Ferrara**. Children at Arpaia and Benevento 1921–1935. A son Angelo b. and d. Arpaia
  1935 (`QLK5-DKRD`).
- Daughter **Francesca Zampiello** b. 27 Apr 1928 Arpaia, d. 2022 Brisbane.
- Giuseppa Ferrara's identification with "Giuseppa Alfonsina Maria Ferraro, 1881" (`QGJ2-KRY1`) is
  flagged as uncertain in the tree and remains so.

## Access note

FamilySearch record *images* for several Caserta collections return "This record can only be
displayed on certain accounts" — restricted to FamilySearch centres and affiliate libraries. The
*index* and the *full-text transcriptions* remain reachable, which is what most of the above rests on.

## Method that worked, for repeating

FamilySearch full-text search over unindexed register images, via:

```
/service/search/fulltext/search?count=50&m.defaultFacets=on&m.queryRequireDefault=on
  &offset=0&c.collectionId=on&f.collectionId=<CID>&q.anyPlace=Arienzo&q.text=Falco
```

Collection IDs: `M9J1-7MY` Campania Religious 1551–1975 · `M9J1-SMK` Campania Deaths ·
`M9J1-9B4` Campania Marriages · `2043630` Caserta SMCV Civil 1866–1929 ·
`2718545` Caserta Civil 1809–1866 · `2475030` Benevento Civil 1810–1942 ·
`1483010` Archdiocese of Benevento Church Records 1575–1908.

`f.collectionId` binds the place properly; without it `q.anyPlace` is only weakly weighted and the
result set floods with the whole region.
