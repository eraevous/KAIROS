# Do published claim-checking methods apply to AI coordination records?

*Kairos Observatory, evidence packet 01. Preliminary draft written by an AI agent (Claude) from public sources, with a review by a model of another family (GPT) of a summary of an earlier draft. The project owner has not reviewed or endorsed this text.*

**Literature checked:** 2026-11-12. **Re-check by:** 2027-05-12, or sooner if an independent critique or replication of VeriScore appears (the gap noted in §2). After that date, read the verdicts as possibly out of date.

Each claim carries one label: **source-grounded** (a published source says it), **hypothesis** (testable, not yet tested), **exploratory interpretation** (our reading), **design proposal** (something we might do). Nothing here is a commitment.

## The question

Kairos keeps working records written mostly by AI assistants: handoffs between agents, decision logs, status reports and pull-request descriptions. We want to classify the claims in those records by how they go beyond their evidence, along two axes:

- **move:** imagination, supposition, estimation, inference, recall or projection;
- **standing:** grounded, marked (flagged as uncertain), or unmarked.

Three well-known methods are natural reference points: FActScore, VeriScore and semantic entropy. **Can their methods be used on records like ours, and which parts carry over?**

## Short answer

The main finding is negative. These methods mostly don't transfer to private coordination records. Their published critiques are the most useful part.

| Method | Use its… | Don't use its… | Label |
|---|---|---|---|
| FActScore | Pipeline shape: split into small claims, check each against a named source, keep per-claim labels | Single percentage, equal weighting of claims, Wikipedia as the source | design proposal |
| VeriScore | Scope step: decide how a claim should be checked before checking it | Its rule for what's out of scope, as written; web search as evidence; the F1@K score | design proposal |
| Semantic entropy | The lesson that consistency isn't correctness | The detector itself, on historical records | design proposal |

## 1. FActScore (Min et al., EMNLP 2023)

**What the source claims** [source-grounded]

- Long-form answers mix supported and unsupported material, so one true/false verdict per answer is too coarse.
- FActScore splits a generation into atomic facts and reports the share supported by a reliable knowledge source.
- In human evaluation of model-written biographies, ChatGPT scored 58%.
- An automated estimator (retrieval plus a strong language model) came within 2% of the human scores.

**How** [source-grounded]

- **Task:** biographies of people, checked against an April 2023 English Wikipedia dump.
- **Truth standard:** "supported" means supported by that source, not true in general.
- **Labels:** annotators marked each atomic fact Supported, Not-supported or Irrelevant.
- **Assumptions** (the authors chose biographies and Wikipedia because they fit these reasonably well): support is objectively checkable; every atomic fact counts equally; the source is internally consistent.
- **Tooling:** the released tool reports how often the model abstained, applies a length penalty that is on by default, and accepts a custom knowledge source.

**Does it apply to coordination records?**

- *Holds* [exploratory interpretation]:
  - Coordination records mix supported and unsupported claims in the same paragraph, which is the problem FActScore was built for.
  - "Supported by a named source" maps onto "supported by the records at a stated revision".
  - The custom-source option means the pipeline isn't tied to Wikipedia.
- *Fails* [exploratory interpretation]:
  - **The source isn't consistent.** Records that append corrections rather than rewrite contradict themselves over time by design. The source has to be pinned to a revision and a time, or a claim that was true when written is scored against a later correction.
  - **Claims don't weigh the same.** "Tests passed" or "the owner approved" matters far more than a correct file path. Equal weighting hides the claims that carry authority.
  - **Absent support doesn't mean false.** Record sets are often incomplete, so Not-supported has to stay separate from contradicted.
  - **The number doesn't transfer.** Biography scores say nothing about error rates in coordination records.

**Counterevidence** [source-grounded]

- **Wanner et al. (\*SEM 2024):** FActScore results change with the decomposition method. Errors made while splitting the text get blamed on the model that wrote it.
- **Jiang et al. (Core; Findings of ACL 2025):** precision metrics like FActScore can be gamed by padding an answer with trivially true or repeated claims. Core credits only informative, non-repetitive subclaims.

**Our reasoning**

- [hypothesis] Padding is a live risk. A status report that adds many trivially true lines ("branch created", "file exists") would score better on claim precision without becoming more trustworthy.
- [design proposal] Use FActScore's shape and drop its score: fix the decomposition rule and log it; verify each claim against the records at a pinned revision and time; keep per-claim labels; report counts with their denominators, never one percentage.
- [design proposal] Report results per claim type (authority and action claims apart from descriptive ones) rather than one weighted score. *Amended after cross-family review:* weighting moves the gaming to claim classification, splitting and weight choice. If weights are ever needed, declare them in advance and show how the result changes under alternatives.

**Possible next step:** decompose the same short records twice, independently, and measure how often the two decompositions disagree. This is a cheap check inspired by Wanner et al.'s finding, not their evaluation: they compare different decomposition methods (scoring each with DecompScore) and how each shifts FActScore.

## 2. VeriScore (Song, Kim and Iyyer, Findings of EMNLP 2024)

**What the source claims** [source-grounded]

- FActScore and SAFE assume every claim in a text is verifiable. That fails for answers that mix facts with advice, examples or hypotheticals, and it unfairly penalises them.
- VeriScore extracts only verifiable claims, which describe a single event or state.
- Human raters preferred its extracted claims to SAFE's about 93% of the time.
- A model's score on one task didn't predict its score on another.

**How** [source-grounded]

- **Extraction:** a sliding-window extractor skips advice, fiction and subjective opinion.
- **Evidence:** each claim is used as a Google search query (top 10 results).
- **Verdicts:** supported, contradicted or inconclusive; contradicted and inconclusive are merged into "unsupported" for the reported scores.
- **Score:** F1@K, where K is the median number of claims per response in a domain.
- **Stated limits:** "verifiable" is a working definition, not a formal one; long, complex claims often come back inconclusive from search snippets.

**Does it apply to coordination records?**

- *Holds* [exploratory interpretation]: deciding how a claim should be checked before checking it is the right first step. Its three verdicts are close to four we would keep (supported, contradicted, absent, ambiguous).
- *Fails*:
  - **The scope rule** [exploratory interpretation]. VeriScore drops hypotheticals and suggestions from scoring. For coordination records the error is usually the standing, not the move: a hypothesis presented as established fact is the failure we most want to catch. Filtering by kind of claim drops the cases that matter most.
  - **Evidence source.** Web search can't see private records, or claims about actions ("merged", "ran the tests").
  - **The score.** A recall target set by a domain median means nothing for a pilot of a dozen episodes.
  - **Merged verdicts.** Merging contradicted with inconclusive loses the difference between false and unknown.

**Counterevidence** [source-grounded]

- The authors list these limits themselves.
- No independent critique was found in a bounded search. That is a search result, not evidence that none exists.

**Our reasoning**

- [design proposal] Choose the check by standing, and never use standing to skip checking. *Amended after cross-family review*, which pointed out that "filter by standing" is circular if the standing under test also decides whether a claim is checked. So separate the **declared** standing (how the writer marked it) from the **assessed** standing (what the evidence supports), and use the declared one only to choose the test:
  - factual assertions are checked for support;
  - marked hypotheses and estimates are checked for accurate marking and for contradiction by the record;
  - proposals are checked for the factual premises embedded in them.
  - Without this, a hedge becomes a way to escape checking.
- [design proposal] Keep four verdicts. For action claims, add *stated time vs. recorded time*, which a search-based verifier can't express.

**Possible next step:** count the claims a VeriScore-style scope rule would have excluded that this rule keeps. If the count is zero on a small pilot, the change is unnecessary at that size.

## 3. Semantic entropy (Farquhar, Kossen, Kuhn and Gal, Nature 2024)

**What the source claims** [source-grounded]

- Uncertainty measured over meanings, rather than word sequences, detects one subset of hallucinations: confabulations, which are arbitrary and incorrect answers.
- It works across tasks without task-specific data.
- The authors say it doesn't address errors a model makes consistently, such as misconceptions learned in training.

**How** [source-grounded; method details from the abstract and secondary write-ups, not the full text]

- Sample several answers to the same prompt (about ten in the original work), cluster those that entail each other in both directions, and compute entropy over the clusters. A discrete variant counts cluster frequencies when token probabilities aren't available.
- For longer text: split into factoids, generate questions about each, then resample answers. The generated questions were a major source of error.
- Cost: sampling about ten answers costs on the order of ten single answers, before clustering. *(Corrected 2026-11-18: an earlier draft cited a follow-up reporting 5–10× the cost of one answer without recording which follow-up, so that figure is withdrawn.)*

**Does it apply to coordination records?**

- *Fails for historical records* [exploratory interpretation]. The method needs fresh samples from the same model given the same input. Coordination records are single outputs from past sessions whose context (files, tool results, conversation state) and model version can't be reproduced. Resampling today measures a different system.
- *Probably fails for the errors we expect* [hypothesis]. Two patterns we expect in agent records, a marked claim copied forward unmarked ("hardening") and drift between stated and actual times in action reports, look process-driven rather than arbitrary. A model that turns "designed" into "done" would probably do it again on resampling, so the samples would agree and entropy would stay low.
- *Might hold for recall* [hypothesis]. Recall errors, such as naming the wrong source document from partial context, could be arbitrary and differ on each resample. *Caveat from cross-family review:* "recall errors are arbitrary, projection errors are consistent" is a hypothesis, not an established error class, and repeated output shows consistency, not its cause.

**Counterevidence** [source-grounded]

- **Tan et al. (EMNLP 2025):** "self-consistent errors" (the same wrong answer across samples) stay stable or grow as models scale, while inconsistent errors shrink. All four families of detectors tested struggle with them. Their fix uses a second model, because self-consistent errors often differ across models.
- **Kim et al. (2025):** errors are correlated across models, which limits how far cross-model disagreement can stand in for verification.
- **Black-box estimation:** follow-up work finds the discrete variant underestimates entropy at typical sample sizes.

**Our reasoning**

- [design proposal] Don't use semantic entropy on historical coordination records.
- [design proposal] Keep its lesson as a review rule: **agreement isn't verification.** A claim repeated across records, or confirmed by a second model of the same family, still needs a source at a stated revision.
- [hypothesis] If recall errors are arbitrary and projection errors self-consistent, uncertainty sampling could help with one move and not the others, which would argue for move-specific checks rather than one detector.

**Possible next step:** a synthetic probe with the original context in hand: about 20 recall-style prompts ("which document said X?") over a small invented corpus and about 20 projection-style prompts ("report the status of this plan"), each resampled about ten times, comparing entropy on the wrong answers. Limit: an invented corpus may behave differently from real records.

## How this was searched

- **Date:** 2026-11-12, one bounded session by the drafting agent.
- **Starting set:** the three methods were chosen in advance as the reference points our question names (FActScore, VeriScore, semantic entropy); this packet didn't search for alternatives to them.
- **Routes:** each method's own paper and released code or documentation; then a web search for published critiques, replications and follow-up work citing each one (two to three critiques kept per method); and one extra source on correlated errors across models (Kim et al.), added for the cross-model question in §3.
- **Sources consulted:** the ones listed under Sources. For semantic entropy, method details came from the abstract, the authors' group page and one secondary write-up (all three listed under Sources), not the full text.
- **Looked for, not found:** an independent critique or replication of VeriScore.
- **Not recorded:** the exact search queries were not logged at the time; this section was reconstructed from the draft on 2026-11-18, when the packet format began requiring it. Later packets log their queries as they search.
- **Not searched:** non-English work, preprints after 2026-11-12, and claim-checking methods beyond the three named.

## What this packet doesn't show

- No error rates for any real record set, and no comparison with published numbers.
- No test of any method. Every applicability call is an argument from the methods, not a measurement.
- Search was bounded: three named sources, two to three critiques each. A missing critique of VeriScore isn't evidence of its robustness.

## Stress-test of the verdicts

- **Unverified premise:** that terse coordination records can be split into atomic claims at all. An action claim with a time ("merged at about 17:10 after tests passed") may have no stable atomic form; Wanner's result suggests the split will vary.
- **Backfire:** a scope rule keyed on marking rewards marking. Answered above by checking marked claims for contradiction.
- **Strongest counterargument:** a careful in-house schema may already do most of what these methods do, so this packet relabels internal practice with external names. Partial answer: the literature adds three concrete risks an in-house schema may not name: decomposition variance (Wanner), padding (Core) and self-consistent errors (Tan). Its methods transfer much less than its warnings do.
- **Reversal:** semantic entropy applied *prospectively*, sampling at the moment an agent writes a recall claim, removes the historical-record objection. Only cost and the self-consistency limit remain. That needs a build, so it isn't proposed here.

## Sources

- Min et al. 2023, FActScore: [arXiv 2305.14251](https://arxiv.org/abs/2305.14251); code and defaults: [factscore 0.1.5 on PyPI](https://pypi.org/project/factscore/0.1.5)
- Song, Kim, Iyyer 2024, VeriScore: [arXiv 2406.19276](https://arxiv.org/abs/2406.19276)
- Farquhar, Kossen, Kuhn, Gal 2024, semantic entropy, Nature 630:625–630: [doi:10.1038/s41586-024-07421-0](https://doi.org/10.1038/s41586-024-07421-0); authors' group page: [OATML](https://oatml.cs.ox.ac.uk/publications/202406_FarquharKossenKuhn_HallucinatingLLMs.html)
- Secondary, for semantic entropy method details only: [Rubin Lake technology radar, "LLM evaluation: semantic entropy"](https://rubinlake.com/en/technology-radar/ai-and-data-engineering/llm-evaluation-semantic-entropy)
- Wanner et al. 2024, A Closer Look at Claim Decomposition: [ACL Anthology, *SEM 2024](https://aclanthology.org/2024.starsem-1.13.pdf)
- Jiang et al. 2025, Core: Robust Factual Precision with Informative Sub-Claim Identification: [arXiv 2407.03572](https://arxiv.org/abs/2407.03572)
- Tan et al. 2025, Too Consistent to Detect: self-consistent errors: [arXiv 2505.17656](https://arxiv.org/abs/2505.17656)
- Estimating Semantic Alphabet Size for LLM Uncertainty Quantification (2025): [arXiv 2509.14478](https://arxiv.org/html/2509.14478v2)
- Kim et al. 2025, Correlated Errors in Large Language Models (ICML 2025): [PMLR v267](https://proceedings.mlr.press/v267/kim25e.html)
