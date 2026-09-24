# Four people here died before they were born, and two are still merged on a name

Written 24 September 2026 by the estate session, at David's request, for
whoever next works in this archive. **This is data, not a task.** Nothing has
been changed here.

## The four

| person | born | died | sources | mergedOn |
|---|---|---|---|---|
| **Vittoria Cimmino (Falco)** | 1877 | Feb 7 1857 | tree | — |
| **Carmina Falco** | July 8 1891 | 19 Dec 1832 | register, tree | **name alone** |
| **Pasqualina Falco** | Feb 1 1877 | 14 Sep 1836 | register, tree | **name alone** |
| **Raffaele Falco** | 10 May 1818 | 28 Oct 1817 | register | — |

## Carmina and Pasqualina are the Angela Maria Falco shape

A tree birth and a register death belonging to two different women, welded
into one record. **The date-kind rule added on 23 September cannot see
these**, and that is worth understanding rather than patching: it compares
birth against `b` and death against `d`, and refuses only when a pair both
exists and disagrees. Here the two dates it holds are *different kinds* and
each is individually plausible. A birth in 1891 and a death in 1832 are
never compared with one another, so nothing objects.

## Vittoria Cimmino is the one to open first

She is **tree-only**, so nothing here was merged badly — the tree itself
holds a woman born 1877 who died in 1857. And she is **the mother of Matteo
Falco**, with Gioacchino Falco as her husband. The head of this archive's
line has a mother whose dates cannot both be true.

## Raffaele is probably not a merge

`b 10 May 1818`, `d 28 Oct 1817` — register-sourced and off by a year.
Likelier a transcription slip, or a third Raffaele. This archive already
tells two men of that name apart with a trailing qualifier — «(of Giuseppe,
d. 1811)» against «(the second, d. 1815)» — so a third would fit the
convention.

## How this was found

Checking every archive for the fault fixed in the Defranceski archive that
day: a person who died a child being given a spouse and children. That test
is `died - born < 15`, and a **negative** span passes it trivially, so the
impossible dates fell out sideways.

Across the estate: **121 dated people here with 4 impossible**, against 0 in
Booyzen, D'Arcy, Defranceski and Mazza, and 1 in Blazevic. Four of the
estate's six are here, and two of those are a live class rather than four
separate typos.

**The first version of that check reported eleven infant-parents in another
archive and every one was the checker's own parser** — a ternary bound the
wrong way, so a person with no birth year came out as «died at 0». The
rewrite prints the raw birth and death strings beside every hit, which is
why the table above reads `Feb 7 1857` and not `1857`: so any of it can be
refused without taking the report on trust.

## A cheap gate, offered rather than asserted

`died_year < born_year` on every row, run against the data rather than the
build. It would have caught all four the moment they were written, needs no
merge logic, and cannot be argued with. `tools/check_households.py` already
has the shape for it.
