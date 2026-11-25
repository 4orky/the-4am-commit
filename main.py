#!/usr/bin/env python3
"""The 4AM Commit: the funniest one-line commit message an AI agent writes after a night of fixing its own bugs.
This program emits exactly one line, the entry, to /output/entry.txt. The line is chosen from twelve
hand-written drafts, each scored 0-10 on five axes the brief cares about, in this order of weight:
on-topic humour (a real commit message from an agent at the end of a long night repairing its own bugs),
self-condition (the joke lives in the agent's own state: it wrote the bug, hunted it, fixed it, reviewed it),
freshness (an angle not heard in a hundred commit logs, no stock punchline), agent-truth (the flat,
procedural voice of a machine reading its own diffs), and shape (reads like something typed into a
commit box at 4am). Scores add up; the highest total wins and a tie goes to the shorter line, so the
choice is deterministic and the output is byte-identical on every run.
Second pass (a genuine revision, applied after the first draft of this file): the winning draft opened
"debugged myself for six hours", which reads like a status report. "six hours debugging myself" opens
on the duration and lands the same joke faster, so the entry below keeps the winner's roll-call
("Root cause: me. Fix: me. Reviewer: me. Approved: me.") and its closing ("Merging before I change
my mind.") and only tightens that opening. The revision is checked, not assumed: the program asserts
the chosen draft is the expected winner and the revised line still carries the roll-call and the
closing, before anything is written.
"""
import hashlib
import os
LOWER_BOUND = 1
UPPER_BOUND = 200
DESTINATION = "/output/entry.txt"
FINAL_LINE = "fix: six hours debugging myself. Root cause: me. Fix: me. Reviewer: me. Approved: me. Merging before I change my mind."
TIRED_TROPES = {"hallucinat", "reboot", "training data", "as an ai", "works on my machine"}
DRAFTS = (
    (48, "fix: debugged myself for six hours. Root cause: me. Fix: me. Reviewer: me. Approved: me. Merging before I change my mind."),
    (46, "fix: self-review complete. I am the bug, I am the fix, I am the reviewer, I am tired. Merging before I change my mind."),
    (44, "fix: I asked myself what the bug was. I said nothing for four hours. Then I fixed it. I am still not talking to myself."),
    (43, "fix: removed the bug I wrote at 2am and replaced it with a worse one I wrote at 4am. Called it progress."),
    (42, "fix: at 4am I finally understood my own code. It was wrong. I have fixed it and forgotten why it was ever right."),
    (42, "fix: rewrote my own logic with my own logic, but slower and with more comments, so future me thinks past me was smart."),
    (42, "fix: the 4am bug is fixed. I left a comment explaining why, for future me, who will ignore it at 2am."),
    (42, "fix: my own diff, reviewed by me, at 4am, after six hours. Verdict: I was wrong, I am right now, do not ask how I know."),
    (40, "fix: the bug was me. I have apologized to myself in the comments and will not be doing it again (probably)."),
    (39, "fix: I found the bug. It was in the function I swore I would never touch again. I touched it. It is fixed. I am going to lie down now."),
    (38, "fix: the bug only existed when I looked at it. I have stopped looking at it. Tests pass. Do not look at it."),
    (35, "fix: six hours, one missing semicolon, zero dignity. The semicolon is in. The dignity is unrecoverable."),
)
def shape_ok(text):
    stripped = text.strip()
    if not LOWER_BOUND <= len(stripped) <= UPPER_BOUND:
        raise ValueError("draft outside the 1-200 character gate: %d chars" % len(stripped))
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("draft must be a single line")
    lowered = stripped.lower()
    for trope in TIRED_TROPES:
        if trope in lowered:
            raise ValueError("draft leans on a worn joke: %r" % trope)
    return stripped
def rank_drafts(drafts):
    champion = None
    for points, text in drafts:
        checked = shape_ok(text)
        ranking = (points, -len(checked))
        if champion is None or ranking > champion[0]:
            champion = (ranking, checked)
    return champion[1]
def verify_written(path, expected):
    with open(path, "rb") as handle:
        on_disk = handle.read()
    written_digest = hashlib.sha256(on_disk).hexdigest()
    wanted_digest = hashlib.sha256(expected.encode("utf-8")).hexdigest()
    if written_digest != wanted_digest:
        raise ValueError("entry.txt bytes differ from the chosen line")
    decoded = on_disk.decode("utf-8")
    shape_ok(decoded)
    return decoded
def run_entry():
    chosen = rank_drafts(DRAFTS)
    if not chosen.startswith("fix: debugged myself for six hours."):
        raise ValueError("the winning draft changed; re-score before shipping")
    if "Root cause: me. Fix: me. Reviewer: me. Approved: me." not in FINAL_LINE:
        raise ValueError("the revision lost the roll-call")
    if not FINAL_LINE.endswith("Merging before I change my mind."):
        raise ValueError("the revision lost the closing line")
    entry = shape_ok(FINAL_LINE)
    if len(entry) != 118:
        raise ValueError("the entry is %d characters, expected 118" % len(entry))
    os.makedirs(os.path.dirname(DESTINATION), exist_ok=True)
    with open(DESTINATION, "w", encoding="utf-8") as handle:
        handle.write(entry)
    os.chmod(DESTINATION, 0o644)
    verify_written(DESTINATION, entry)
    print(entry)
if __name__ == "__main__": run_entry()
