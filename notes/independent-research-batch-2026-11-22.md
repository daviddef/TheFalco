# Independent research batch, 22 November 2026: what each of the 30 came to

David asked for «the next 30 things you can research independently», then «do them all». This note says what was done,
what was only attempted, and what was **not started**, item by item, so none of it is read as more than it is. Numbers are the
numbers of that list. Where a row of the work list is meant, it is named.

**Done in this session (3 items of 30, plus two checks that closed as «nothing new»):** items 1, 2 and 11/12 below, and a
new finding found on the way (Alfonso Arricale). **Not started: 4–10, 13, 17 (beyond the index coverage), 18–24, 25–30.** The
pane items (25–30) also wait on a decision about the other archive sessions that were running on the same FamilySearch account.

## Done

**1. Reconcile the work list against the walk.** The 1866–1910 walk did **not** close rows 102 and 114. Measured from
`searched.json` (rows marked `walked: true`, union of their image ranges): RM9 (1901–1910) **1,305 of 1,337** images walked;
FNT (1866–1877) **820 of 1,236**; VNL (1878–1900) **512 of 2,898**. In all **2,637 of 5,471 (48%)**; 2,834 are unwalked, of
which **2,386 are VNL 1886–1900**. Rows 102 and 114 now say so. Rows 39, 40 and 59 (the deaths of Antonia di Guida and Giuseppe
Falco, and the 1880 Falco × Carfora marriage) fall in the unwalked parts and stay open. Rows 42, 95 and 113 were not re-read.

**2. Row 108 (three couples on «Which Falco» with no household).** Two of the three now have one (Don Francesco Falco ×
Donna Maddalena Stellato; Gioacchino Falco × Vittoria Cimmino). **Gioacchino Falco × Andreana Crisci is still missing**; its
acts (V107, V213, V230, V240, V267) are listed in the work-list note; no household was written because each act needs a level-13
read first, and nothing in the V-table or notes gives «Guglielmo», the page's alias.

**11/12. Antenati's name index, tested for rows 95 and 104 and for the Luigi, Crescenzo and Morgillo lines (items 12, 14–16).**
`/search-nominative/` holds 71 Arricale (Forchia 26, Paolisi 21, Montesarchio 10, San Bartolomeo in Galdo 8, Arpaia 4; years
1878–1942) and **none at Arienzo**: Arienzo's registers are not name-indexed. Falco is indexed at Forchia, Paolisi, Moiano and
Arpaia from 1861 on. **No Falco marriage dated before 1870 appears** in the name indexes of Moiano, Paolisi, Arpaia, Forchia,
Montesarchio or San Bartolomeo in Galdo. That is «not established», not a nil: the indexes are partial, and the marriages in
question (Pasqua Falco and Francesco Arricale before 1848; Luigi Falco before 1864) are earlier than any of these indexes
reaches. Row 104 (Carmine Annecchino) was already settled on 18 October as «not online anywhere found, has to be asked for»; nothing
here changes that.

## New finding, from the name index

**Alfonso Arricale, died at Montesarchio on 5 November 1940** (Morti 1940, Parte I, act 165, image 86 of an_ua2241604, read
from the image at 2600 px): born at Arienzo, son of «fu Vincenzo» and «fu Falco Concetta», a widower. Placed in the house of
Andrea Falco and Maria Carmela Buono as a son of Vincenzo Arricale and Maria Concetta Falco (married at Arienzo on 24 October
1870), **on the parents' names, the birthplace and the age window (born about August 1874), not on a document that names both
parents together**: Vincenzo's surname is not written in the act, and a second Falco Concetta is not excluded. The birth act
(Arienzo Nascite 1874, about 19 August, in the Tribunale copy MC55-FNT, not on Antenati) would settle it. Not read at level 13:
the age's leading mark, the declarant's age and the street's initial.

## Not done, and why

- **4–10.** Not started. These are the housekeeping rows (109, 88, 97, 98, 17, the corrections audit with PR 46's open items, the
  Atlas catalogues). One thing found on the way for item 10: the Atlas surname catalogue has **no family for Arricale** (`terms
  Arricale` returns typography forms only), although the Arienzo acts write the name Arricale, Orricola and Arvicale. It was tried:
  `surname_variants.py add --new --headline Arricale …` (with Orricola and Arvicale as attested forms, evidence kind record) was **refused**, because the
  Atlas catalogue's own `check` currently fails on other sessions' rules (`norwegian-aa`, `patronymic-ending` are not among the four allowed rules), and `add` refuses
  what `check` refuses. Nothing was written to the Atlas. The Atlas working tree also held other sessions' uncommitted changes, which were left alone.
- **7 (row 107, Rosa Ceglia).** Looked at, not solved. The builder refuses the join because it would make someone their own
  ancestor; a run that would print the cycle was started in a throwaway copy and the copy had been deleted, so the command ran
  in the real repository instead (see the slip below); no cycle was traced.
- **18 (Sant'Agnese).** Not started: it needs a web source the session could not use.
- **19–20, 24 (NAA, Queensland indexes).** Not started. NAA RecordSearch is driven through the pane (the viewer is a popup);
  and the records are of living or recently living people.
- **21–23 (letters).** Not drafted. The errands page holds structured «asks»; a draft needs the archive's address and the
  heirs-only rule for a military record, and was not begun.
- **25–30 (FamilySearch pane).** The pane was signed in (catalogue 200). Three other archive sessions (Defranceski, Mazza,
  Blažević) were running at the time, and the sweep rule is one sweeper per account, so **no sweep was started.**

## A slip, recorded

While tracing row 107 I ran a command that began `cd /tmp/cleanv…`; that directory no longer existed, the `cd` failed, and the
`||` branch ran `git checkout -qf FETCH_HEAD` **in the real repository**. It discarded one uncommitted edit (the first version of
the work-list changes), which was redone; nothing else was lost (`git status` was clean afterwards and the branches were
intact). A throwaway build directory is created under the scratchpad from now on, and every `cd` is checked.
