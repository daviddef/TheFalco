/* What is new here, and the archive in numbers: the kit computes it at build time from this archive's own logs (kit/docs/whats-new.md).
   This file is the only Falco-specific part: which JSON is which, and the one count no log holds.

   WHY `fields.when` POINTS AT `searchedOn`. In searched.json `when` is the year of the RECORD read ("1814", "1840–1969"), not the day the
   work was done, so the kit would date almost nothing from it. The rows that carry a real work date hold it in `searchedOn`
   (ISO, 2026-10-08), so that is the column used; a row without one stays on the What Has Been Read page, and /whats-new/ says how many.
   No date is made up and none is taken from git. `pending` and `not searched` are not outcomes of a search and are left out. */
import { buildPulse } from "@daviddef/archive-kit/lib/pulse.js";
import searched from "../data/searched.json";
import corrections from "../data/corrections.json";
import worklist from "../data/worklist.json";
import people from "../data/people.json";
import sources from "../data/sources.json";

export const pulse = buildPulse({
  searched, corrections, worklist,
  counts: { people: people.length, sources: sources.length },
  fields: { when: ["searchedOn"] },
});
