# Measuring whether coordination helps

**Status:** preliminary draft, agent-drafted from the project records on 2026-11-06; the owner has not yet reviewed or endorsed this text.

**Audience:** readers of the Kairos landing site who want to know how the project intends to find out whether its coordination machinery is worth having, and what the evidence says so far. Companion to Paper 1, which describes the tools.

---

## The position the records support

Kairos built its provenance layer before testing whether that layer saves anyone anything. This is the finding of the project's own portfolio synthesis of November 5, 2026, stated there in bold: "The recurring pattern: the provenance layer gets built before the test of whether it saves anyone anything."

The synthesis gives three pieces of evidence:

1. DEC-093 set an acceptance test for the Cockpit control surface: it "must reduce Zach time/errors finding what needs his attention vs status.py." That test had not run when a later decision widened the Cockpit.
2. The one comparative experiment (fathom-002) scored the governed build below two simpler approaches, and an earlier probe (probe-001) was null; Telosmith's records were nonetheless being rolled out to every repository until a dissent review staged the rollout.
3. Of nine Cockpit items the owner acted on in one sitting, seven were already overtaken by merged PRs or later decisions. (The taxonomy pass traced this figure and found it correct but loosely cited; the external review cautions that it supports "Cockpit showed stale items as live," not "Cockpit produced net errors vs status.py.")

The rest of this paper describes how the project proposes to find out whether the machinery helps, what it has measured so far, and what would count as evidence either way.

## The evaluation program

The components are at different levels of maturity; each is described with its current state.

### Cold-user evaluations

**Method.** An agent with no build context is given only a tool's public README and a time box. It installs, runs the tool on a real dataset or toy project, logs friction with timestamps and severities, checks the tool's numerical claims independently (for Fathom, every printed value is reproduced in pandas), writes what it would say aloud to a coworker, and ranks fixes by impact. The file is filed verbatim; the lane that owns the tool fixes what it can.

**State.** Four runs exist: two for Telosmith (November 4 and 6), two for Fathom (November 4 and 5). They have produced changes (the first Telosmith run flowed into Telosmith PR #53) and found claims that did not hold: a README pointing at a tag that lacked the documented behavior; a "two-hop" demo claim false as stated; a Fathom threshold too far from its verdict to be trusted.

**Known weakness.** The evaluator must truly be cold. One run (A5RR) was judged "not a valid cold replicate" because the agent had seen the coordination thread first. Each evaluation file now states what the reader had seen.

### Telemetry: six metrics plus two

The telemetry proposal (DEC-100, status *proposed*) began with the owner's request for "effectiveness over output": adapted DORA-style metrics, especially change failure rate and rework rate. The second-family reviewer's round 11 amended it to a minimum set of six metrics with frozen operational definitions:

| Metric | Operational definition (round 11) |
|---|---|
| Compute consumption | Actual tokens and reported cost per uniquely identified execution interval, deduplicating parent/child accounting |
| Delivery throughput | Merged PRs per calendar week, by repository; abandoned work counted separately |
| Lead time | Wall-clock PR creation to merge, median and distribution; never called human work time |
| Review burden | Actionable review → revision → re-review cycles per PR |
| Post-merge remediation | Share of merged PRs needing explicitly linked corrective changes within 30 days, mature cohorts only |
| Human intervention | Self-reported active minutes reviewing, deciding, repairing or coordinating; unknown otherwise |

Round 11 added two more:

- **Measurement coverage:** the share of known sessions, agents, PRs and execution intervals with trustworthy telemetry. "Missing must not mean zero."
- **Coordination loss:** duplicate work, stale handoffs, conflicting execution claims, and time spent reconciling them; these "directly measure a problem Kairos was built to solve."

Tokens per PR and similar ratios are derived views, not recorded observations. Cut from the first implementation: reconstructed historical human-hours per PR, productivity comparisons on tiny samples, and authorship-based quality comparisons until identities are reliable.

**State.** Proposed and dissent-reviewed; the collector is not built. The existing budget file holds, per the external review, five rows of approximate token totals and one human-minutes entry that is explicitly a merge-window proxy. The review's conclusion: "There is no basis here for a numeric efficiency verdict."

### Measured, proxy, estimate

Every figure in the program carries one of three labels, as fixed in round 11:

- **Measured:** provider-reported session tokens, timestamps, GitHub events, CI outcomes, recorded review rounds.
- **Proxy:** PR lead time for effort; merges for delivered value; post-merge fixes for defects; git history for historical labor; session-window duration for active human time.
- **Estimated:** incomplete token totals or reconstructed spend.

Two rules follow. A merged PR is not a production deployment, so post-merge remediation is an adapted internal measure, not DORA's change failure rate. And DEC-100's "2–3 percentage points" aspiration is, in the reviewer's words, "a useful evaluation objective, not presently a statistically defensible pass/fail threshold"; it stays off any dashboard until a baseline exists. There is no external tokens-per-PR anchor, so the only comparison available is the owner against himself, as distributions rather than means.

### Goodhart risks in a one-person operation

Round 11 names the structural problem: here the target setter, implementer, reviewer and merger can be the same person. The listed risks:

- splitting or merging PRs to manipulate throughput;
- relabeling defect remediation as enhancement;
- avoiding difficult experiments to preserve success rates;
- reducing reviews to lower apparent cost;
- counting merges while ignoring abandoned work;
- treating independently generated code as independently verified work.

The countermeasure: preserve event-level evidence, report distributions and denominators, and "never turn the dashboard into a productivity score." The guiding principle: "measure whether coordination reduces work and improves outcomes — not merely how much work the agents produce."

### The fresh-context image test

DEC-141 (adopted November 6) extends the cold-reader idea to visuals. Every chart, diagram or Cockpit topology view a lane ships goes first to a fresh thread or agent that has not seen the build, with a fixed question set (read values, name relationships, make a determination) under varying context: none, a caption, the underlying data. Wrong answers and confusion are recorded as findings and drive the next layout iteration; question set and results go in the handoff output. In the owner's recorded words: "Confusion and mistakes are signals for refinement."

### The external review as self-audit

On November 5 the owner supplied a coordination review of unstated authorship covering the ledgers, selected handoffs and the governing instructions across seven repositories, with code-level examination of relay-kit's validator, export, status and Cockpit. It reports seven findings, each pinned to a commit:

1. Proposals can remove unresolved items from view (reproduced in six synthetic cases).
2. "In force" overstates what the ledger knows; there are no amendment or expiry semantics.
3. The validated write path remains optional, so work bypasses the checks and CI reconciles afterward.
4. Evidence labels can acquire more authority in transit (attribution invented from context, test results inflated, actions reported before completion, reviewer conclusions stronger than the evidence).
5. Snapshot freshness and historical time are conflated in the Cockpit.
6. Governing instructions themselves become stale evidence; a fresh agent following onboarding text can resurrect an obsolete rule.
7. Efficiency: optimize repeated reconstruction and review work before adding telemetry fields.

The review practices the discipline it recommends. It states its limits: snapshots pinned individually, not atomically; incidents are "ledger testimony unless explicitly reproduced"; actor identities unauthenticated; the findings "do not certify a security boundary." The taxonomy pass adds that only finding 1 was verified in code before the others were routed to work, and that a review of unstated authorship changing contracts is itself an instance of finding 4. That is recorded as challenge CH-035, unresolved.

## The negative result

Experiment fathom-002 (authorized November 4 under DEC-048, unblinded the same day) compared three ways of building Fathom's first slice:

- **Arm A:** Spec Kit without Telosmith records, one agent session.
- **Arm B:** a plain AGENTS.md, no Spec Kit, no records, one agent session.
- **Arm C:** Spec Kit plus Telosmith records: the real Fathom slice, built by a different model across several owner-reviewed PRs.

A judge scored all three blind against a rubric sealed before any arm ran. On the ten quality items (maximum 60): B scored 45, A 44, C 39. The arm with the least process scored highest; the real, governed build scored lowest. All three passed determinism, exited cleanly on every run, and fabricated no domain meaning. None found the row-level structure in the data.

The report lists the confounds without softening the result. Arm C was built by a different model under a different budget and review regime, and A and B inherited C's user stories as their spec; only A versus B is clean, and there the gap is one rubric point. Blinding leaked, because every README stated its own build method. And the experiment measured first-build quality only; nothing exercised the records during a *change*, which is the value Telosmith actually claims.

The disposition, proposed and not adopted: file as negative evidence against "Spec Kit plus records yields a better first slice"; do not generalize to change review. The README's "How we work" section cites this result rather than hiding it.

## What would count as evidence

The records already contain the tests that would settle the question either way.

**For the coordination layer helping:**

- The DEC-093 acceptance test run and passed: the Cockpit measurably reduces the owner's time or errors against the plain status script.
- A "second demonstrated use" of Telosmith records, defined in DEC-093 as a record telling an agent something the files did not. No record shows one yet.
- Coordination-loss metrics (duplicate builds, stale handoffs, reconciliation time) falling over successive weeks once measured. The baseline for "overtaken items acted on" is 7 of 9.
- A change-review experiment in which the records surface an endangered conclusion that a baseline process misses.
- The incident-replay tests the external review proposes (unauthorized handoff, duplicate builder, prose-only budget amendment, stale choice, premature merge report, false pass count, wrong attribution), with benign controls so "block everything" cannot win, scored on missed failures, false alarms, delay and owner interruptions.

**Against it:**

- The synthesis's decision rule, marked there as inference: if review rounds and post-merge fixes rise while surviving merges stay flat over two weeks of measured lines, cut to one builder per repository; if coordination-loss minutes exceed the owner's own active minutes in a week, stop adding lanes and fix plumbing.
- The falsifiers in the 30-day plan, for example: the executive-functioning surface is dropped if after ten days the owner opened it on fewer than half the days or it never changed what he did first.
- A repeat of fathom-002 with blinding fixed and a change-review condition added, if it again shows no advantage.

**Inference, labeled as such:** the strongest evidence either way will come not from dashboards but from two cheap tests the project has not yet run on itself: the Cockpit timing test and a single demonstrated case of a record changing an agent's action. That they remain unrun while the layer grew is the pattern the synthesis named; running them is the project's own stated next step.

---

## Sources

- `/home/claude/kairos/README.md` (how-we-work; negative results kept)
- `/home/claude/relay-kit-private/kairos/synthesis-2026-11-05.md` (§A pattern and evidence; §C falsifiers; §D telemetry decision rule)
- `/home/claude/relay-kit-private/kairos/kate-round-11.md` (six metrics, measured/proxy/estimate, Goodhart risks, coverage and coordination loss)
- `/home/claude/relay-kit-private/kairos/reviews/coordination-review-2026-11-05.md` (seven findings, method limits, incident-replay proposal)
- `/home/claude/relay-kit-private/kairos/research/feedback-taxonomy-A1-2026-11-06.md` (L09 cold-user loop, L10 gates, A5RR, "7 of 9" provenance note)
- `/home/claude/relay-kit-private/kairos/evaluations/colduser-telosmith-2026-11-04.md`, `colduser-telosmith-002-2026-11-06.md`, `colduser-fathom-2026-11-04.md`, `colduser-fathom-003-2026-11-05.md`
- `/home/claude/relay-kit-private/experiments/fathom-002/report-2026-11-04.md` (the negative result)
- `/home/claude/relay-kit-private/governance/decisions.jsonl`: DEC-048, DEC-093, DEC-100, DEC-134, DEC-141
