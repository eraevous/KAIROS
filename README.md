# Kairos — START HERE

> **We are building Cognitive Augmentation.**
> (The project's guiding light, in the owner's words. What it means in full is being written; until then every repo here is judged by one question: does it increase a person's capacity to realise their intentions?)

Kairos is Zach Rhodes's umbrella for his AI/cognition work: a set of tools, the operating environment that coordinates the people and AI agents who build them, and the research behind both. This repository is the front door. It holds the map, the directions, the honest status of everything else, and one script: the Dev Kit installer below.

---

## Install the Dev Kit (10 minutes)

One script, [`kairos.py`](kairos.py), sets up everything in a single folder, `Kairos`, inside your home folder, and ends by building you a **Cockpit**: a web page that shows what is waiting on you, what the tools are doing, and the decisions you've recorded, all read from files on your own machine. (A picture of one: [docs/assets/cockpit-choice.png](docs/assets/cockpit-choice.png).) It needs no administrator rights and no account.

Two free programs must be on the computer first. If you have never installed them, do this once:

- **Python** (the language the tools are written in): [python.org/downloads](https://www.python.org/downloads/), click the big download button, run it, and on the first screen **tick the checkbox that says "Add python.exe to PATH"** before clicking Install. That checkbox is what lets the next steps find Python.
- **git** (fetches the tools from GitHub): [git-scm.com/downloads](https://git-scm.com/downloads), run the installer, accept every default.

**Windows**

1. Download [`kairos.py`](https://raw.githubusercontent.com/eraevous/KAIROS/main/kairos.py) (right-click, *Save link as…*) into your Downloads folder.
2. Open PowerShell (Start menu, type `powershell`), then type: `cd Downloads` and press Enter.
3. Type `python kairos.py install` and press Enter. When it finishes with *All checks passed*, type `python kairos.py next`.

**macOS / Linux**

1. Download [`kairos.py`](https://raw.githubusercontent.com/eraevous/KAIROS/main/kairos.py) into your Downloads folder.
2. Open Terminal, then type `cd ~/Downloads` and press Enter.
3. Type `python3 kairos.py install` and press Enter. When it finishes with *All checks passed*, type `python3 kairos.py next`.

No clone needed: `kairos.py` alone clones the rest. (If you did clone this repo, `install.ps1` and `install.sh` do the same thing: `powershell -ExecutionPolicy Bypass -File install.ps1`, or `sh install.sh`.)

**What you'll have at the end**

- `~/Kairos/repos/`: shallow clones of [relay-kit](https://github.com/eraevous/relay-kit), [Telosmith](https://github.com/eraevous/Telosmith), [Fathom](https://github.com/eraevous/Fathom) and [QAT-Kits](https://github.com/eraevous/QAT-Kits).
- relay-kit and Telosmith installed for your user (`python -m relaykit`, `python -m aec`), editable, so a `git pull` in the clone updates them.
- `~/Kairos/records/`: a fresh, private records store that is yours, seeded with one decision (DEC-001: this is your store).
- `~/Kairos/cockpit/index.html`: the Cockpit page built from that store, branded Kairos. `python kairos.py open` shows it.
- A log of every run at `~/Kairos/devkit-log.txt`.

**If it says `python is not recognized`** (Windows): the PATH checkbox was missed. Run the Python installer again, choose *Modify*, and tick *Add python.exe to PATH*; or type `py kairos.py install` instead, which usually works.

**If something fails**: run `python kairos.py check` (`python3` on macOS/Linux) and send the output to whoever pointed you here, or open an issue on this repository. Every FAIL row carries a one-line fix. Running `install` again is always safe; it only redoes what is missing.

**What the kit does NOT do**: it never asks for administrator rights; nothing leaves your machine (the only network use is cloning from github.com and, if pip needs its build helper, pypi.org); no account, token or sign-in is created; it never writes outside `~/Kairos` except pip's own per-user package folder; it never touches a records store that already exists. To uninstall, delete `~/Kairos` (and, optionally, `python -m pip uninstall relay-kit telosmith`).

---

## Pick your path

| You are… | Start with | Then |
|---|---|---|
| **A user** who wants to try a tool | [Install the Dev Kit](#install-the-dev-kit-10-minutes) (or one tool: [Install](#install)) → the tool's own `README` and `docs/demo.md` | Open an issue in that repo with what confused you; first-contact confusion is the most valuable report we get |
| **A contributor** (human or AI agent) | [How we work](#how-we-work) → [Contributing](#contributing) | Pick an issue, or an item from a repo's `docs/` "needs owner" lists; open a PR, never merge |
| **An explorer** of the architecture | [The map](#the-map) → [Principles](#principles-that-recur) | Read a repo's `AGENTS.md` and `.aec/records.jsonl`: the written reasons live next to the code |
| **Curious** about the thesis | [What this is](#what-this-is-for) → [Research](#research) | Watch this file; the papers are coming |

---

## What this is for

Powerful AI tools let one person do work that used to need a team. The systems coordinating that work usually hide what was decided, why, on what evidence, and whether a later change quietly broke an earlier conclusion. Kairos is an attempt to keep those things attached to the work — in records a stranger can audit later — and to find out, by measurement rather than assertion, whether doing so makes a person more capable or just busier.

Three ideas recur in every repo:

- **The reason stays attached to the thing.** Purposes, requirements, claims, decisions and objections are records that link to code and to each other, append-only.
- **Information crosses freely; authority never crosses implicitly.** Agents read everything and propose anything. Only the owner accepts.
- **Count and ask; never fabricate meaning.** Every claim carries how it was established — measured, inferred, declared — and tools refuse to compute what the data cannot support.

---

## The map

| Repo | What it is | Who it serves | State |
|---|---|---|---|
| [**Telosmith**](https://github.com/eraevous/Telosmith) | Keeps the recorded reasons for code attached to the code. `check` validates the records; `code-impact` tells an agent (or a human) which written requirements, claims and decisions a change endangers. Standalone, with Spec Kit, or inside another agentic-coding setup. | Developers and teams using coding agents | 0.5.0 on `main`; tag pending; 300+ tests; `docs/demo.md` is a 90-second walkthrough |
| [**Fathom**](https://github.com/eraevous/Fathom) | Deterministic, offline data-review reports: a data dictionary, structure findings with the threshold printed beside each verdict, time-series and panel structure, a liftoff Brief that asks what the data *cannot* tell you. Byte-identical reruns; nothing leaves your machine. | Analysts; anyone handed a CSV they didn't make | specs 001–019 merged; two-stage flow (liftoff → profile) |
| [**relay-kit**](https://github.com/eraevous/relay-kit) | The coordination kit: handoffs with ids and states, append-only decision and challenge ledgers, chat capture and cross-model relay, read-only export, a static **Cockpit** control surface, an MCP server. | People running more than one AI assistant on one project | v0.1.0; export@1, mcp@1, cockpit@2+ |
| [**QAT-Kits**](https://github.com/eraevous/QAT-Kits) | Cognitive tools as contract-checked specs — StressTest, TruthWeight, FrameShift, NegativeSpace, ThreadMap, MetaDistill and more — chainable, with evals. | Anyone who wants a model to *think in a named way* rather than ramble | typed specs for two tools; the rest in prose; roadmap in progress |
| [**MtG**](https://github.com/eraevous/MtG) | Commander deck analysis on an interaction ontology and a card knowledge base; the first Telosmith pilot outside Telosmith. | Players; also a worked example of the records approach on a hobby | scorer, game log, KB pinned |
| [**Cognitive-Scaffolding**](https://github.com/eraevous/Cognitive-Scaffolding) | Document and conversation processing: chunking, enrichment, hybrid retrieval, reconstruction; the origin of several ideas above and a library of foundation notes. | Researchers of their own archives | working but uneven; its `AGENTS.md` describes planned machinery — read `docs/enforcement-audit.md` first |
| [**Anamnesis**](https://github.com/eraevous/Anamnesis) | Recovering, connecting and reconsidering what has accumulated in conversations and documents — attributed reconstruction, not summarisation. | The same researchers, later | placeholder; a rescued spike is being triaged |
| **Prospero** (formerly PlayWrite) | Creative collaboration for writers and artists — cultivation, not replacement. | Writers | idea; repo not yet renamed |
| **kairos-cockpit** (private) | The Kairos-specific layer over relay-kit's generic Cockpit: repo list, design, PR landing, deployment. | The owner | seeded |
| **relay-kit-private** (private) | The coordination records themselves: ledgers, handoffs, status, research notes. The Cockpit is generated from these. | The owner and the agents | daily |

Private repos are private because they hold personal records or credentials, not because the method is secret; the method is in the public kits.

---

## Install

All public tools are plain Python, stdlib-only in the kits, Python 3.12+ recommended. None is on PyPI yet.

**Telosmith**
```bash
pip install "git+https://github.com/eraevous/Telosmith.git@main"
aec --help        # the command; `telosmith` is an alias
```
Then follow `docs/demo.md` (90 seconds, real output).

**Fathom**
```bash
git clone https://github.com/eraevous/Fathom && cd Fathom
python3 -m venv .venv && .venv/bin/pip install -e '.[test,exports]'
.venv/bin/guide liftoff your.csv --out out/discovery     # stage 1: Brief + Configurations
.venv/bin/guide profile your.csv --config liftoff.yaml --out out/report   # stage 2
```
Runs with every socket blocked; the tests prove it.

**relay-kit**
```bash
pip install "relay-kit @ git+https://github.com/eraevous/relay-kit@v0.1.0"
relay-kit init my-records && relay-kit status --root my-records
relay-kit cockpit --root my-records --out ./cockpit      # a static page; open index.html
```
Not a Claude user? The kit is being made installable from instructions alone for ChatGPT, Codex and others; say what broke.

**QAT-Kits and MtG**: clone and read the README; both run from a checkout with no install.

---

## How we work

- **Records before builds.** A change that touches a purpose, a contract or a threshold starts as a proposed decision in the ledger, gets a dissent review from a reviewer who did not see the build conversation, and is accepted or refused by the owner. Agents propose; the owner decides.
- **Two families review before a merge.** Every substantive PR gets a fresh-context review and a review from a different model family (today: Claude and ChatGPT), with blocking findings fixed before merge. Agents never merge.
- **Everything is append-only.** Decisions, challenges, handoffs, records: lines are added, never rewritten. CI refuses rewrites.
- **Honest status.** Negative results are kept and cited. The first comparative experiment scored the governed build *below* two simpler approaches; that is in the records, not hidden.
- **Agents are visible.** Every commit carries its author trailer (which model, which session); every GitHub comment by an agent is signed with its actor id. An unsigned comment is the owner.

---

## Contributing

- **License and CLA.** Public repos are MIT. Each carries a `CLA.md`: contributing grants the owner a commercial-relicensing right so companies can use the code with minimal risk while he keeps his rights. Read it before your first PR. (Two repos — QAT-Kits and Anamnesis — are missing their LICENSE/CLA files; that is on the owner's list.)
- **What to open.** Issues for confusion, bugs and claims that don't hold; PRs for fixes. The best first PR is a docs-truth fix: find a README sentence that is not true and make it true. Several repos have a `docs/enforcement-audit.md` listing exactly those.
- **What not to do.** Don't rewrite record lines. Don't declare a canonical copy of a tool that has several (QAT). Don't change a threshold or a verdict rule in Fathom without a decision record. Don't paste private conversation text into public issues.
- **If you are an AI agent.** Read the repo's `AGENTS.md`; it is the contract. Sign your comments. Report what you observed and what you inferred as different things.

---

## Principles that recur

- Information crosses freely between agents; authority never crosses implicitly.
- Three records kept apart: historical evidence, current interpretation, authorised commitment.
- A record can be authentic, historically accurate, and no longer applicable.
- When an existing cognitive tool fits the problem, use it; when it doesn't, investigate whether the missing capability is worth building. (The owner calls this Wu Wei.)
- Parsimony, elegance, modularity — things that can be taken in or put back.

---

## Research

We study our own system as it runs, find what's broken or wonky, and fix it. Each finding, with its number, what we did about it, and how it was established, is on the [Findings page](docs/findings.html).

- **Written ontologies are rarely executed.** About 11% of Telosmith's own record links fall outside its documented vocabulary, and no check notices. *Fixing:* Telosmith's vocabulary is being made load-bearing, so misuse is flagged automatically.
- **Grounding beats citing.** 628 card-role assignments changed (candidate corrections, not yet reviewed) when the MtG evaluator read machine-checkable contracts instead of matching text, and tests prove the contracts are consumed. *Built;* a 60-case review comes before it becomes the default.
- **Work waits at the hand-offs.** The 90th-percentile pickup of a handed-off task was 16.7 h on 9 November, and the biggest single blocker was a relay between model families. *Shipped:* self-scheduling lanes and direct channels; *specified:* a fix for the stall detector; *next:* a handshake-and-heartbeat link layer.
- **Idea lineage survives days, not years.** Of the links in five traces from idea toward code, 19 were verified, 10 reconstructed and 3 unsourced; stable IDs alone wouldn't fix the gaps.
- **"Choice" vs "decision" has no stable meaning yet.** *Being built:* authorization fingerprints filled and checked by tooling; an ontology-first authority layer, and a proposed body for the decision register and structured challenges.
- **Borrow patterns, adopt no runtime.** Four orchestration systems were read at pinned commits: 0 adopted, 10 patterns credited; three are being adopted inside existing tools (one built, two proposed).
- **No comparable public baseline found** (our 5 November search) for tokens per merged change in human-directed agentic work, so this project measures its own.

Under way: interestingness (depth that keeps paying out), a programmatic catalogue of feedback loops, small local models with cognitive scaffolding, and minimum cognition per task kind.

---

## History

This repository previously held an unrelated 2025 scaffold; it is preserved on the branch `archive/govai-scaffold-2025-07`.
