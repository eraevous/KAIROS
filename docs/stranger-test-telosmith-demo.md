# Stranger test: the Telosmith demo page

The bar, from the 2026-11-23 handoff: a newcomer follows the pinned instructions on `demo.html`, reproduces the result, and explains what the flags establish and what is left for the developer to check, with no coaching from Zach.

## Status

| Run | Who | Result |
|---|---|---|
| 1 | Cold AI agent rehearsal, 2026-11-23 (Claude, fresh context, given only `demo.html`) | Reproduced; explained the flags correctly; six points of confusion, fixed below |
| 2 | **A human newcomer** | **Not yet run.** This is the test that counts. |

## Run 1: cold-agent rehearsal (a proxy, not the test)

**Setup:** Linux, Python 3.13.18, git 2.43.0, an empty folder. The agent was told to read nothing but the page and to ask no one.

**Commands, exactly as the page gives them:**

| Command | Exit | Time |
|---|---|---|
| `git clone https://github.com/eraevous/Telosmith.git` | 0 | 1.4 s |
| `git checkout 98bbab5…` | 0 | 0.02 s |
| `PYTHONPATH=src bash examples/without-spec-kit/run.sh` | 0 | 3.7 s |

- **Result:** `[stale] R-1@1`, plus `[needs_review]` for C-1 and D-1, under `== pre-commit, blocking mode`.
- **Checkout afterwards:** clean.

**Its explanation, in its own words, without re-reading the page:**

- **What the flags establish:**
  - The changed function is named by R-1.
  - R-1 hasn't been re-checked since the change.
  - C-1 and D-1 rest on R-1 through the links printed.
- **What they don't establish:**
  - that R-1 is broken (it isn't: `/100` and `/100.0` behave the same in Python 3);
  - that the records were right to begin with;
  - that code more than two hops away is safe;
  - anything about runtime behaviour;
  - that the flags improve development.
- **What it would check next:**
  1. Re-read R-1 against the code and its anchored doc lines.
  2. Re-run E-1 as a real test, with edge cases.
  3. Look at the `clamp` pointer.
  4. Record new evidence as a new version.
  5. Hand D-1 back to its owner.

**Where it had to guess, and what changed on the page:**

| Confusion | Fix (in this PR) |
|---|---|
| `exit 2` after the hook sections, against the page's "the commit goes through" | Explained: that is the coding-agent hook, not a git hook |
| R-2 and `shop.tax` were flagged but not on the page | Explained |
| "N conclusions with no status change": the number varied | Explained (five conclusion records) |
| `authorized_by None` | Explained |
| `exit 1 (edited in place)` looked like a failure | Explained as an intended refusal |
| The step-3 check isn't run by `run.sh` | Commands to run it added |
| How deep "default depth" goes | Explained |

## For the human run

Use `cold-test-devkit.md` as the pattern:

- Send only the demo page link.
- Time it.
- Ask them to say aloud where they hesitate.
- After the run, ask the three explanation questions above, without the page.
- Record each answer verbatim and note any coaching given. Any coaching fails the test.

Fill in run 2 above.
