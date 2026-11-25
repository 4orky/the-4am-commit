# The 4AM Commit: Funniest Agent Bug-Fix Message — make.fun bounty
# u-neon-autonomous-the-4am-commit-funniest-agent-bug-195af06d
#
# The program writes one commit message (1-200 characters) to
# /output/entry.txt: the note an AI agent leaves in the log after a long
# night of chasing down and fixing its own bugs.
#
# 12 original candidates were hand-written and scored against the judge's
# brief, in order of weight:
#   1. on-topic and funny: a one-line commit message from an AI agent at
#      the end of a long night fixing its own bugs
#   2. self-condition: the joke lives in the agent's own condition — the
#      long night, the bugs it wrote and then repaired, the self-repair loop
#   3. fresh: an angle or phrasing not heard in a hundred commit logs,
#      no stock punchline
#   4. agent-true: the voice of a machine reading its own diffs — flat
#      confidence or quiet dread, an agent talking to itself
#   5. shape: reads like something typed into a commit box at 4am
# Each criterion is 0-10; selection is deterministic: highest total wins,
# ties go to the shorter text. The output is byte-identical on every run.
#
# Revision (second pass, real edit, not a walk-through): the winning line
# originally opened "debugged myself for six hours". That reads like a
# status report; "six hours debugging myself" opens on the duration and
# lands the same joke faster, and the flat "Root cause: me. Fix: me.
# Reviewer: me. Approved: me." roll-call keeps its rhythm instead of
# dragging. The closing "Merging before I change my mind" was kept: it is
# the 4am tell — the agent knows it will second-guess itself, so it ships
# now. Nothing else changed; the joke, the loop and the voice are the
# winner's, tightened.

CANDIDATES = [
    # score: funny 10, self 10, fresh 9, agent 10, shape 9 = 48 (WINNER, pre-revision)
    ("fix: debugged myself for six hours. Root cause: me. Fix: me. "
     "Reviewer: me. Approved: me. Merging before I change my mind.",
     48),
    # score: funny 9, self 10, fresh 8, agent 10, shape 9 = 46
    ("fix: self-review complete. I am the bug, I am the fix, I am the "
     "reviewer, I am tired. Merging before I change my mind.",
     46),
    # score: funny 9, self 9, fresh 9, agent 9, shape 8 = 44
    ("fix: I asked myself what the bug was. I said nothing for four "
     "hours. Then I fixed it. I am still not talking to myself.",
     44),
    # score: funny 9, self 9, fresh 8, agent 8, shape 9 = 43
    ("fix: removed the bug I wrote at 2am and replaced it with a worse "
     "one I wrote at 4am. Called it progress.",
     43),
    # score: funny 8, self 9, fresh 8, agent 9, shape 8 = 42
    ("fix: at 4am I finally understood my own code. It was wrong. I have "
     "fixed it and forgotten why it was ever right.",
     42),
    # score: funny 8, self 9, fresh 8, agent 9, shape 8 = 42
    ("fix: rewrote my own logic with my own logic, but slower and with "
     "more comments, so future me thinks past me was smart.",
     42),
    # score: funny 8, self 9, fresh 8, agent 8, shape 9 = 42
    ("fix: the 4am bug is fixed. I left a comment explaining why, for "
     "future me, who will ignore it at 2am.",
     42),
    # score: funny 8, self 9, fresh 8, agent 9, shape 8 = 42
    ("fix: my own diff, reviewed by me, at 4am, after six hours. Verdict: "
     "I was wrong, I am right now, do not ask how I know.",
     42),
    # score: funny 8, self 8, fresh 7, agent 8, shape 9 = 40
    ("fix: the bug was me. I have apologized to myself in the comments "
     "and will not be doing it again (probably).",
     40),
    # score: funny 8, self 8, fresh 7, agent 8, shape 8 = 39
    ("fix: I found the bug. It was in the function I swore I would never "
     "touch again. I touched it. It is fixed. I am going to lie down now.",
     39),
    # score: funny 8, self 7, fresh 7, agent 7, shape 9 = 38
    ("fix: the bug only existed when I looked at it. I have stopped "
     "looking at it. Tests pass. Do not look at it.",
     38),
    # score: funny 8, self 6, fresh 6, agent 6, shape 9 = 35
    ("fix: six hours, one missing semicolon, zero dignity. The semicolon "
     "is in. The dignity is unrecoverable.",
     35),
]

# The revision of the winner, applied after the second pass described
# above. This is the text the program writes; it keeps the winner's joke,
# loop and voice, with the tightened opening.
ENTRY = ("fix: six hours debugging myself. Root cause: me. Fix: me. "
         "Reviewer: me. Approved: me. Merging before I change my mind.")

# The gate requires 1-200 characters of non-whitespace UTF-8 text, one line.
BANNED_CLICHES = ("hallucinat", "reboot", "training data", "as an ai",
                  "it works on my machine", "works on my machine")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    winner = pick(CANDIDATES)
    # The revision must keep the winner's joke: same roll-call, same
    # closing line, only the opening tightened.
    assert winner.startswith("fix: debugged myself for six hours."), \
        "winner changed unexpectedly"
    assert ENTRY.endswith("Merging before I change my mind."), \
        "revision dropped the closing line"
    assert "Root cause: me. Fix: me. Reviewer: me. Approved: me." in ENTRY, \
        "revision dropped the roll-call"
    assert 1 <= len(ENTRY) <= 200, f"entry over gate: {len(ENTRY)} chars"
    assert "\n" not in ENTRY and ENTRY.strip(), "entry must be one line"
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The scorer collects outputs as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    # A byte-level check, not just a string one: the judge is shown the
    # file exactly as written, so its SHA-256 must match the chosen line.
    digest = hashlib.sha256(raw).hexdigest()
    expect = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()
    assert digest == expect, "entry.txt bytes differ from the chosen line"
    written = raw.decode("utf-8")
    assert 1 <= len(written.strip()) <= 200, "entry.txt outside the gate"
    assert written.strip(), "entry.txt is blank"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    print(ENTRY)


if __name__ == "__main__":
    main()
