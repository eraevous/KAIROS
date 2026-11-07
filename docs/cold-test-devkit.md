# Cold test: the Dev Kit, first tester

One page for whoever runs the first cold test of `kairos.py` with a non-developer on their own Windows PC, with no administrator rights. The point is to learn where the instructions fail a stranger, not to get the install done. The install is the tester's job; watching is yours.

## Before

- **Send them one thing: the README link.** `https://github.com/eraevous/kairos#install-the-dev-kit-10-minutes`. No zip, no extra notes, no "by the way you'll need…". If the README is not enough, that is the finding.
- Ask for a time when they have 30 undisturbed minutes and their own PC. A screen share or sitting beside them both work; sitting beside them is better, because you see where the eyes go.
- Ask them, before they start, whether Python or git is already on the machine. Note the answer; do not act on it.
- Start a timer when they open the link.

## Ask them to say aloud

- what they are reading, each time they look at the page;
- what they think a step wants them to do, *before* they do it;
- what they are about to type, as they type it;
- what they expected to happen, each time something happens;
- when they feel stuck, the moment they feel it (not after they solve it).

Tell them nothing they say is wrong. Confusion is the data.

## What to record

Keep one line per event, in order. A phone's notes app is enough.

- **Hesitations**: where they paused for more than ten seconds, and what was on screen.
- **What they typed**, exactly, including mistakes and the command they chose when two were offered.
- **Every error text, verbatim.** Photograph the screen if that is faster. The `check` table and `~/Kairos/devkit-log.txt` can be sent afterwards, but the wording they saw on screen at the moment matters most.
- **Minutes per step**: downloading, opening PowerShell, `cd`, `install`, reading the table, `next`, `open`.
- **Where they looked for help**: the README, a search engine, a friend, you.
- **The moment they gave up**, if they did, and the words they used.

## What not to do

- **Do not help until they give up.** Giving up means they say so in words ("I don't know what to do next", "can you just do it"). Looking frustrated is not giving up.
- Do not point at the screen, do not read the README to them, do not say "scroll down".
- Do not fix anything on their machine. If the install fails, it fails; `python kairos.py check` and the log are the result.
- Do not explain what Kairos is for before the test. Afterwards, gladly.
- Do not record their name in the notes or in any issue; write "the tester".

## Afterwards: the five questions

1. In your own words, what did the script just do to your computer?
2. Which step were you least sure about, and what would have made it clear?
3. Was there a moment you thought you had broken something? What were you looking at?
4. What do you think happens if you delete the `Kairos` folder now?
5. Would you run `python kairos.py next` on your own tomorrow? If not, why not?

Write their answers down as said, then thank them properly: a cold tester gives the project something no developer can.

## Filing the result

Open one issue in the kairos repo titled `Cold test 1: <date>`, with the timeline, the verbatim errors, the five answers, and the `check` table. Mark what the tester said separately from what you inferred. Each error text that a non-developer could not act on is a bug in `kairos.py`, not in the tester.
