#!/usr/bin/env python3
"""What changed, and when — generated from this archive's own commit history.

The de Franceschi site carries a «what changed» page. This is the Falco
equivalent, and it is not hand-written: it is read straight out of git, so it
cannot drift from what actually happened. Every entry is a real commit.

The subject line becomes the headline; the first paragraph of the body becomes
the summary. Merge commits and pure-chore commits are dropped.
"""
import json, subprocess, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "src", "data", "changes.json")

SEP = "\x1e"
raw = subprocess.run(
    ["git", "-C", ROOT, "log", "--no-merges", f"--pretty=format:%H{SEP}%ad{SEP}%s{SEP}%b\x1d",
     "--date=short"],
    capture_output=True, text=True).stdout

# What kind of work a commit was, from its own words.
def classify(subject, body):
    t = (subject + " " + body).lower()
    if re.search(r"\bread end to end|sweep|acts? \d|register read|volume\b", t): return "sweep"
    if re.search(r"\bfix|bug|leak|correct|withdraw|regression\b", t): return "fix"
    if re.search(r"\bfound|find\b|first record|names? \w+ at last", t): return "find"
    if re.search(r"\badd |page|publish|links?\b|render|design", t): return "site"
    return "other"

rows = []
for chunk in raw.split("\x1d"):
    chunk = chunk.strip("\n")
    if not chunk: continue
    parts = chunk.split(SEP)
    if len(parts) < 3: continue
    sha, date, subject = parts[0], parts[1], parts[2]
    body = parts[3] if len(parts) > 3 else ""
    if re.match(r"^(chore|wip|typo|bump)\b", subject, re.I): continue
    # first paragraph of the body, tidied to one line
    para = ""
    for block in body.strip().split("\n\n"):
        b = " ".join(x.strip() for x in block.splitlines()).strip()
        if b and not b.startswith(("Co-Authored", "🤖")):
            para = b; break
    para = re.sub(r"\s+", " ", para)
    rows.append({"sha": sha[:7], "date": date, "title": subject,
                 "summary": para[:420], "kind": classify(subject, body)})

json.dump(rows, open(OUT, "w"), ensure_ascii=False, indent=0)
import collections
print(f"{len(rows)} changes written")
print("  by kind:", dict(collections.Counter(r["kind"] for r in rows)))
print("  span   :", rows[-1]["date"], "→", rows[0]["date"])
