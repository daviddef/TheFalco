#!/usr/bin/env python3
"""Who the archive treats as living by inference: propose the list, write the decision file, write David's worksheet.

    python3 tools/living_by_inference.py propose                 # counts only, never a name
    python3 tools/living_by_inference.py write [--by-hand ID ...] # writes data/living-by-inference.json
    python3 tools/living_by_inference.py worksheet PATH           # PRIVATE: names people; PATH must be outside every repo

THE RULE (David, 17 October 2026) is INFERENCE_RULE in tools/check_living_v2.py and is printed into the decision file:
an undated person with no recorded death and no public source whose nearest dated ancestor (parents, then grandparents,
then great-grandparents, both lines) was born in year Y, g generations up, has an estimated birth of Y + 20*g; if that is
1946 or later (80 or younger in 2026) the person is treated as living, and so is an undated spouse of such a person.
Only David can say who is in fact dead: he moves an id into "overridden" and the generator and the gate both follow.

THE FILE holds tree ids and the rule text, never a name or a date. The generator (tools/build_people.py) reads it and
passes each id to the kit's rule as said_living=True. This tool computes the proposal with the gate's own function
(check_living_v2.infer_living), because the gate is what judges the file; the generator never runs the inference.
It needs the private tree and says so when it is not here.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_living_v2 as cl           # noqa: E402

ROOT = cl.ROOT


def load_all():
    if not os.path.exists(cl.TREE):
        raise SystemExit("living_by_inference: the private tree (data/myheritage-falco-tree.json) is not on this "
                         "machine; the inference cannot be computed here.")
    tree = json.load(open(cl.TREE, encoding="utf-8"))
    people = cl.load("people.json")
    line = cl.load("line.json")
    base, by_rec = cl.recompute(tree, people, line, said=set())     # the kit's rule alone
    return tree, people, line, base, by_rec


def current_file():
    try:
        return cl.load_decision()
    except ValueError:
        return {"ids": set(), "byHand": set(), "overridden": set(), "handNotes": {}}


def propose(show=True):
    tree, people, line, base, by_rec = load_all()
    inferred = cl.infer_living(base)
    dec = current_file()
    ids = set(inferred) | dec["byHand"]
    split = {}
    for tid, v in inferred.items():
        k = "spouse of a treated person" if v["kind"] == "spouse" else "g=%d" % v["g"]
        split[k] = split.get(k, 0) + 1
    if show:
        print("by the rule: %d people (%s)" % (len(inferred), ", ".join("%s: %d" % kv for kv in sorted(split.items()))))
        print("by hand (David's instruction, rule falls short): %d" % len(dec["byHand"]))
        print("on the list in all: %d" % len(ids))
    return tree, people, line, base, by_rec, inferred, ids, split


def write(by_hand):
    tree, people, line, base, by_rec, inferred, ids, split = propose(show=False)
    dec = current_file()
    hand = set(dec["byHand"]) | set(by_hand)
    ids = set(inferred) | hand
    out = {
        "decidedBy": "David Defranceski, in chat, 17 October 2026",
        "status": "provisional: these people are treated as living until David rules a person dead "
                  "(move that tree id to 'overridden')",
        "rule": cl.INFERENCE_RULE,
        "ids": sorted(ids),
        "byHand": sorted(hand),
        "overridden": sorted(dec["overridden"]),
    }
    if dec.get("handNotes"):
        out["handNotes"] = {k: dec["handNotes"][k] for k in sorted(dec["handNotes"], key=int)}
    with open(cl.DECISION, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print("wrote %s: %d ids (%d by hand, %d overridden)" % (os.path.relpath(cl.DECISION, ROOT), len(ids), len(hand),
                                                           len(out["overridden"])))


def inside_a_repo(path):
    d = os.path.dirname(os.path.abspath(path))
    while not os.path.isdir(d):
        d = os.path.dirname(d)
    r = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return r.returncode == 0


def worksheet(path):
    """A PRIVATE worksheet for David: it names people. It is written only outside every git repository."""
    if inside_a_repo(path):
        raise SystemExit("living_by_inference: %s is inside a git repository; the worksheet names people and "
                         "must be written outside every repo." % path)
    tree, people, line, base, by_rec = load_all()
    inferred = cl.infer_living(base)
    dec = cl.load_decision()
    ids = sorted(cl.effective_ids(dec))
    after, _ = cl.recompute(tree, people, line)              # with the decision file applied
    byid = {t["id"]: t for t in tree}

    def nm(i):
        return cl.strip_marks(byid[i]["name"]) if i in byid else "tree id %s" % i

    def rel_to(i, label_end):
        return [r["id"] for r in byid[i].get("relatives") or [] if str(r.get("rel") or "").lower().endswith(label_end)]

    def known(i):
        t = byid[i]
        bits = []
        if cl.strip_marks(t.get("bp")):
            bits.append("tree birthplace: " + cl.strip_marks(t["bp"]))
        facts = [f["t"].rstrip(":") + (": " + f["v"] if f.get("v") else "") for f in t.get("facts") or []
                 if f.get("v")]
        bits += facts[:4]
        rec = by_rec_cur.get(i)
        if rec and rec.get("sources") and rec["sources"] != ["tree"]:
            bits.append("also in the registers")
        return "; ".join(bits) or "name and family links only; no date, place or fact in the tree"

    by_rec_cur = {p["treeId"]: p for p in people if p.get("treeId") is not None}
    lines = [
        "# Falco archive: undated tree-only people treated as living (PRIVATE; names people)",
        "",
        "Written 17 October 2026 for David. Do not commit, publish or paste this anywhere public. It lives outside every repo.",
        "",
        "Why this list exists: the family tree gives these people no birth year and no death, and the estate's rule calls an "
        "undated person not living, so they were published as dead (name, relationships and place, pages indexed). "
        "The relatives the tree does date were born in the 20th century, which makes these people very probably alive. "
        "Until you say otherwise the archive treats every person below as LIVING: a name, how they are related, their town and "
        "country, a page that search engines are asked to skip, no dates, no photographs.",
        "",
        "How the list was worked out: an undated person with no recorded death and no public record is treated as living when "
        "their nearest dated ancestor (a parent, else a grandparent, else a great-grandparent) was born in year Y, g generations "
        "up, and Y + 20*g is 1946 or later (80 or younger in 2026). An undated spouse of such a person is included. A few "
        "people whose estimate falls just short (1941 or 1945) were included by hand, at your instruction (marked BY HAND).",
        "",
        "HOW TO ANSWER: for each person write DEAD (add the year if you know it), LIVING, or UNSURE. A person you rule dead "
        "goes back to being shown as a historical person; give me the tree id.",
        "",
        "A note on children: an undated child of a person treated as living is HELD OUT altogether by the estate's rule "
        "(no page, not named as anyone's relative), because they might be a minor. Those are marked HELD OUT below.",
        "",
        "| tree id | name | relationships (from the tree's own links) | status in the archive now | what is known | nearest dated ancestor | estimate | your answer |",
        "|---|---|---|---|---|---|---|---|",
    ]
    rows = []
    for i in ids:
        if i not in byid:
            continue
        v = inferred.get(i)
        hand = i in dec["byHand"]
        parents = base[i]["parents"] if i in base else []
        spouses = base[i]["spouses"] if i in base else []
        if v and v["kind"] == "ancestor":
            # find the ancestor(s) at that generation with that year
            level = {i}
            seen = {i}
            for g in range(v["g"]):
                nxt = set()
                for x in level:
                    nxt |= set(base[x]["parents"]) - seen
                nxt &= set(base)
                seen |= nxt
                level = nxt
            anc = sorted(q for q in level if base[q]["by"] == v["year"])
            near = "%s, born %s, %d generation%s up" % (nm(anc[0]), v["year"], v["g"], "" if v["g"] == 1 else "s")
            est = "%d (age %d)" % (v["est"], cl.THIS_YEAR - v["est"])
        elif v and v["kind"] == "spouse":
            near = "none of their own; spouse of tree id %s (%s)" % (v["spouseOf"], nm(v["spouseOf"]))
            est = "as their spouse"
        else:
            # by hand: report the nearest dated ancestor and its estimate honestly
            level, seen, near, est = {i}, {i}, "no dated ancestor within 3 generations", "-"
            for g in range(1, 4):
                nxt = set()
                for x in level:
                    nxt |= set(base[x]["parents"]) - seen if x in base else set()
                nxt &= set(base)
                seen |= nxt
                ys = [(base[q]["by"], q) for q in nxt if base[q]["by"] is not None]
                if ys:
                    y, q = max(ys)
                    near = "%s, born %s, %d generation%s up" % (nm(q), y, g, "" if g == 1 else "s")
                    est = "%d (age %d)" % (y + 20 * g, cl.THIS_YEAR - y - 20 * g)
                    break
                level = nxt
            if near.startswith("no dated"):
                mates = [s for s in spouses if s in base]
                near = "none; family links only (parents and spouse undated)" if not mates else near
        rels = []
        for q in parents:
            rels.append("child of " + nm(q))
        for q in spouses:
            rels.append("spouse of " + nm(q))
        kids = [r["id"] for r in byid[i].get("relatives") or []
                if str(r.get("rel") or "").lower().split(" ")[-1] in ("son", "daughter")]
        for q in kids[:4]:
            rels.append("parent of " + nm(q))
        status = "HELD OUT (no page)" if after[i]["held"] else ("living, noindex page" if after[i]["living"] else "?")
        tag = ("BY HAND; " if hand else "") + (status)
        rows.append("| %s | %s | %s | %s | %s | %s | %s | |" % (
            i, nm(i), "; ".join(rels) or "-", tag, known(i), near, est))
    lines += rows
    lines += ["", "Count: %d people." % len(rows), ""]

    # people NOT on the list who are affected or who sit just outside it, so nothing is hidden from David
    listed = set(ids)
    cascade = sorted(t for t, d in after.items() if d["held"] and not base[t]["held"] and t not in listed)
    pool = sorted(t for t, d in base.items() if d["by"] is None and not d["dead"] and not d["flag"] and not d["living"]
                  and not d["held"] and not cl.lr.public_source(d["cites"]) and t not in listed
                  and t not in cascade)

    def anc(i):
        level, seen = {i}, {i}
        for g in range(1, 4):
            nxt = set()
            for x in level:
                nxt |= set(base[x]["parents"]) - seen
            nxt &= set(base)
            seen |= nxt
            ys = [(base[q]["by"], q) for q in nxt if base[q]["by"] is not None]
            if ys:
                y, q = max(ys)
                return "%s, born %s, %d up -> estimate %d (age %d)" % (nm(q), y, g, y + 20 * g, cl.THIS_YEAR - y - 20 * g)
            level = nxt
        return "no dated ancestor within 3 generations"
    if cascade:
        lines += ["## Also held out (not on the list above)", "",
                  "These undated people have a parent who is now treated as living, so the estate's rule holds them out "
                  "(no page, not named as anyone's relative) as possible minors. They were published as dead before.", "",
                  "| tree id | name | relationships | your answer |", "|---|---|---|---|"]
        for i in cascade:
            rels = ["child of " + nm(q) for q in base[i]["parents"]] + ["spouse of " + nm(q) for q in base[i]["spouses"]]
            lines.append("| %s | %s | %s | |" % (i, nm(i), "; ".join(rels) or "-"))
        lines.append("")
    near_miss = []
    for i in pool:
        a_ = anc(i)
        m_ = __import__("re").search(r"estimate (\d+)", a_)
        if m_ and int(m_.group(1)) >= 1941:
            near_miss.append(i)
    if near_miss:
        lines += ["## Not added: estimate 1941 or later, like the people included by hand", "",
                  "Tree ids only; say if you want any of them treated as living: " + ", ".join(map(str, near_miss)), ""]
    if pool:
        lines += ["## Undated, not on the list: the rule does not reach them", "",
                  "No dated ancestor within three generations, or an estimate before 1946. They are still shown as historical "
                  "people. Say if any of them is alive.", "",
                  "| tree id | name | nearest dated ancestor | your answer |", "|---|---|---|---|"]
        for i in pool:
            lines.append("| %s | %s | %s | |" % (i, nm(i), anc(i)))
        lines.append("")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote a private worksheet of %d people (outside every repo)" % len(rows))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("propose")
    w = sub.add_parser("write")
    w.add_argument("--by-hand", type=int, nargs="*", default=[])
    ws = sub.add_parser("worksheet")
    ws.add_argument("path")
    a = ap.parse_args()
    if a.cmd == "propose":
        propose()
    elif a.cmd == "write":
        write(a.by_hand)
    else:
        worksheet(a.path)


if __name__ == "__main__":
    main()
