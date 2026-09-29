# Deliberate decisions about the build, and what they cost

*This archive leaves its corrections visible. It should leave its refusals visible too.* Both
entries below were decided in a chat window on 27–28 September 2026 and were never written down;
they are recorded here late, and said so.

---

## 1. The kit pin is held at `8ec58e6`, and that is hiding a real signal

`site/package.json` pins the shared kit:

    "@daviddef/archive-kit": "github:daviddef/TheArchiveKit#8ec58e6e09b526011e41a50d56c5e2c1a97ead4c"

A fresh clone on 28 September installed **`2790d856cd48`** instead, and the twenty-step chain
**failed at `check:pages`**:

>     FAIL  pages   9 shared page(s) still drawn by hand, and the ratchet is 4 — this number may only go down

The nine were *antenati, arms, australia, diaspora, graves, households, journeys, the-library,
walk*. Under `8ec58e6` the same gate passes with four exempt and the ratchet intact.

**The decision was to hold the pin.** The alternative that keeps the build green on the newer kit
is to raise `--max-bespoke` from 4 to 9, and that would be loosening a ratchet to make a failure
go away — exactly the move the ratchet exists to prevent.

**But holding the pin is a deferral, not an answer, and it should not be read as one.** The newer
kit is not wrong. It is saying that **nine pages of this archive are drawing by hand what other
archives in the estate already share a component for**, and every week the pin stays put is a week
that finding sits unacted on. The honest description of the current state is *«nine pages owe a
rewrite, and the gate that would say so has been switched off by pinning the version that cannot
see it.»*

*The shared kit, layouts and nav belong to another session. Upgrading the pin is that session's
call to make, not this one's — which is a reason to raise it with them, not a reason to leave it.*

---

## 2. No gate was wired for the unmerge that deleted two deaths

On 27 September a household row was split in two, and the person count went **863 → 863** when a
split can only ever raise it. Two documented deaths had been silently dropped. The cause was
`site/src/data/person-slugs.json`, which freezes thirty-four slugs against **two** keys — the
household and `tree:<id>` — and whose frozen branch had no collision guard: the new half took the
slug, the old half took nothing, and the old half's evidence went with it. The guard is now in
`tools/build_people.py` and the register half keeps the address.

**The tell was clean and general: a split must raise the person count.** A gate was considered,
and declined.

**Why.** The person count moves for a dozen honest reasons — a harvested act, a new household, a
name folded — so a bare count ratchet would fire constantly and be trained away within a week. The
invariant that actually holds is much narrower: *when the frozen-slug map is repointed, the count
must rise.* That is a condition inside one branch of one builder, and a check on it belongs next to
the code that can violate it, not in the chain.

**What this leaves undefended, stated plainly.** `check:evidence` reported «clean» through the whole
incident, because every person who still existed still carried their evidence — **the gate cannot
see a person who has stopped existing.** Nothing in the twenty steps ratchets the person count, and
nothing else in the estate would have caught this. *If the collision guard is ever edited out, the
same failure returns silently.* The decision was that the guard plus this paragraph is a better
defence than a noisy gate; **if that turns out to be wrong it will be wrong the same way, with two
true facts gone and every step green.**
