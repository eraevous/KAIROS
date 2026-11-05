# Kairos

Zach Rhodes's umbrella for his AI/cognition work: a portfolio of tools, the operating environment that coordinates them, and the research thesis behind both.

This repository is the front door. The work lives in the repositories below; this one holds the index, the roadmap pointer, and the deployed **Cockpit** (a static control surface generated from the coordination records — see `cockpit/` once deployed).

## Repositories

| Repo | What it is | State (2026-11-05) |
|---|---|---|
| [Telosmith](https://github.com/eraevous/Telosmith) | Records (purpose → requirements → claims → evidence) linked to code; `check` and `code-impact` tell an agent which written reasons a change endangers. Works standalone, with Spec Kit, or inside other agentic coding setups. | v0.5.0 on `main` (tag pending); docs/demo.md |
| [Fathom](https://github.com/eraevous/Fathom) | Deterministic, offline data-review reports that count and ask rather than assert meaning: column, row-level, interval and time-series structure; a configurator page; a liftoff stage in progress. | specs 001–012 merged |
| [relay-kit](https://github.com/eraevous/relay-kit) | The coordination kit: handoffs with ids and states, append-only decision/challenge ledgers, chat capture and relay, read-only export, Cockpit generator and an MCP server (both in review). | export@1 merged; cockpit@1, mcp@1 in review |
| [QAT-Kits](https://github.com/eraevous/QAT-Kits) | Modular prompt tools (StressTest, TruthWeight, FrameShift, NegativeSpace, …) as contract-checked specs; drift inventory across their copies. | inventory 2026-11-04 |
| [MtG](https://github.com/eraevous/MtG) | Commander deck analysis on an interaction ontology and a knowledge base; the first pilot of Telosmith outside its own code. | P-07 scorer, game log |
| [Anamnesis](https://github.com/eraevous/Anamnesis) | Recovering, connecting and reconsidering accumulated knowledge from conversations and documents. | placeholder |
| [PlayWrite](https://github.com/eraevous/PlayWrite) | Creative incubator. | drift |

Private: the coordination records (`relay-kit-private`) hold the ledgers, handoffs, status reports and the roadmap. The Cockpit is generated from them.

## Principles that recur across the repos
- Information crosses freely between agents; authority never crosses implicitly. Only the owner accepts.
- Three records: historical evidence, current interpretation, authorized commitment — kept apart.
- Count and ask; never fabricate meaning. Label every claim by how it was established.
- Append-only ledgers; reviews from more than one model family before merges.

## History
This repository previously held an unrelated 2025 scaffold; it is preserved on the branch `archive/govai-scaffold-2025-07`.
