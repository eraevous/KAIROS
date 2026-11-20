# Making an author's work "pretty and slick" with AI, without losing the author

*Kairos Observatory, evidence packet 05. Preliminary draft written by an AI agent (Claude) from public sources, with research slices run by fresh-context instances of the same model, and a review by a model of another family (GPT) of a summary of the packet. The project owner asked the question, chose the first venues and approved publication, but has not otherwise reviewed or endorsed this text.*

**Literature checked:** 2026-11-18. **Re-check by:** 2027-02-18 (three months: AI writing and design tools change monthly; two products in this packet died or pivoted within the past 18 months), or sooner if any of these appear: a study of AI polish on a skilled author's own long-form draft; a stable Typst HTML export; final EPUB Accessibility 1.2.

Each claim carries one label: **[SG] source-grounded** (a published source says it), **[H] hypothesis** (testable, not yet tested), **[EI] exploratory interpretation** (our reading), **[DP] design proposal** (something we might do). Nothing here is a commitment, and nothing here is legal advice.

## The question

A single author writes articles, papers and books with an agent network that keeps every edit declared and reversible (an "editorial packet": original beside proposed edition, each change labelled and justified, the author decides). The author wants the output to look and read as polished as professional work. **What exists for AI-assisted writing, editing, formatting and layout, what does the evidence say about using it, and what should such a tool build first?**

Four routes: (A) writing and editing tools and practice; (B) formatting, typesetting and publishing pipelines; (C) AI visual design and layout, and judging aesthetics; (D) evidence on what AI assistance does to writing and authors, plus disclosure rules.

## Verdict (design proposal)

**"Pretty and slick" is two different jobs, and the evidence treats them very differently.**

1. **Presentation (format, typography, layout)** carries no documented risk to the author's voice (no study was found either way) and has mature, open, scriptable tools. It should come first and can be made deterministic: text rules proposed as declared changes, style rules pinned in a token file, rendering by a fixed engine, and quality checks that report but never silently fix.
2. **Prose polish (line edits and beyond)** is where the documented harms live: homogenisation toward a model's default voice, shifts in the writer's own stated views, factual errors introduced by conversational rewriting, and loss of felt ownership. These grow with how much text the model contributes and how large each rewrite is. For a skilled writer the measured quality gains are small or absent.

So the tool should **sort every change into a risk tier**, and let the tier set the review interface, the default granularity and the disclosure consequence. Its distinctive asset is one that none of the surveyed products shows: typed, justified, quotation-checked changes against a pinned original. "Slick" should mean better *renderings and reviews* of those packets, not a new editor.

## Evidence

Format per source: claim · methods · fit · counterevidence · our derivation · next step. Labels: **[SG]** source-grounded, **[H]** hypothesis, **[EI]** exploratory interpretation, **[DP]** design proposal.

### A. Writing and editing tools: how edits are presented

| Source | Claim [SG] | Methods | Fit | Counter | Derivation and next step |
|---|---|---|---|---|---|
| [Sudowrite Feedback/Chat, May 2026](https://feedback.sudowrite.com/changelog/your-personal-writing-partner-has-arrived) | Margin comments anchored to spans, each with an optional suggested edit, under named "lenses" (pacing, dialogue) and reader personas; chat edits need an approved plan | Changelog (marketing) | High for the pattern | No rationale taxonomy, no provenance; fiction tools widely criticised for generic prose | [DP] add an optional `lens` field to packet changes so a packet can be reviewed by lens |
| [Microsoft Copilot in Word (GA June 2026)](https://mc.merill.net/message/MC1384426) | Edits land as word-level tracked changes by default | Admin notice | Medium: confirms tracked changes as the professional default | Records *what*, not *why* | [DP] export packets as DOCX tracked changes with rationale in comments, for human editors |
| [Google Docs Gemini comment workflows, July 2026](https://workspaceupdates.googleblog.com/2026/07/streamline-collaboration-in-google-docs-with-Gemini-powered-comment-workflows.html) | Agent summarises open comment threads, drafts replies, proposes suggestions | Vendor post | Medium | Version history doesn't attribute agent vs human auditably (not found) | [DP] `queries` view: pending changes grouped by type |
| [Grammarly Authorship](https://www.grammarly.com/blog/academic-writing/grammarly-authorship-just-got-a-major-update/) | Opt-in capture-time provenance: typed / pasted / AI-generated / edited, with replay and percentages | Vendor blog; no accuracy figures; vendor itself calls categorisation incomplete | High in concept | Inferred from keystrokes, Docs/Word only | [EI] a packet ledger can compute this *exactly*; [DP] a provenance report: characters by origin and decision, plus a text replay |
| [Grammarly "Expert Review" withdrawn after a 2026 suit](https://www.plagiarismtoday.com/2026/03/12/grammarly-sued-over-expert-review-feature/amp/) | AI feedback was attributed to real, named experts without consent; feature disabled | Trade press; suit unresolved as found | High as a caution | General chatbots imitate named writers freely | [DP] lint: no agent rationale or persona may name a real living person as the edit's source |
| ChatGPT Canvas removal, mid-2026 ([secondary](https://ypyl.github.io/news/2026/06/01/openai-removes-canvas-gpt5.5-deprecations/), [forum](https://community.openai.com/t/please-restore-canvas-as-a-persistent-workspace-writing-blocks-are-not-an-equivalent-replacement/1398999)) | A tracked-changes editing surface was dropped; users lost persistent documents | Secondary news and complaints; OpenAI's own note **not found** | Lesson, not tool | Replacement may cover most uses | [EI] editing state locked in a vendor UI can vanish; keep packets plain, documented, vendor-neutral |
| [ProWritingAid Manuscript Analysis](https://prowritingaid.com/developmental-editor) | Developmental diagnosis (plot, pacing, structure) on long manuscripts; "not meant to replace" a human editor | Marketing | Medium | No evaluation | [EI] AI tools are clustering by editorial stage (below) |

**Building blocks (open, scriptable)** [SG]: [Vale](https://vale.sh/hub/) (YAML prose-lint rules; Microsoft, Google, proselint, write-good, alex, readability packages); [proselint](https://github.com/amperser/proselint) (usage-authority checks, BSD); [LanguageTool](https://dev.languagetool.org/http-server) (local HTTP server, JSON offsets and replacements); [CriticMarkup](https://pypi.org/project/pancritic/) plain-text track changes and [pandiff](https://www.github.com/davidar/pandiff) (structure-aware prose diff to CriticMarkup or DOCX; maintenance looks low). Fit [EI]: all can sit behind optional adapters that turn their findings into proposed changes with a rule id as the rationale; none needs to become a hard dependency. Vale's rule types (existence, substitution, occurrence, consistency) are a good schema for a personal style sheet even without running Vale. Counter: technical-writing rules produce many false positives on literary prose.

**Editorial practice** [SG]: the [EFA](https://www.the-efa.org/editorial-services-definitions/) separates developmental, line, copy and proof stages; copyediting produces a **style sheet**. [CIEP](https://ciep.uk/resource/queries-author.html): editors fix trivia silently and *query* judgement calls, located and with a proposed fix. Derivation [EI]: current AI tools map onto stages (diagnosis tools to developmental; rewriters to line; LanguageTool/Vale to copy; proofing barely served). **No surveyed tool keeps a living style sheet as a first-class artefact that edits are checked against.** [DP] tag packets by stage; restrict change types per stage (no agent additions at copy or proof); keep `style_sheet.json` (term, decision, source); batch-accept trivia, render the rest as queries.

### B. Formatting, typesetting and publishing

| Source | Claim [SG] | Fit | Counter / limits | Next step [DP] |
|---|---|---|---|---|
| [Typst 0.14](https://typst.app/blog/2025/typst-0.14), [0.15](https://typst.app/blog/2026/typst-0.15) | Tagged PDFs by default, opt-in PDF/UA-1 checks, PDF/A, Knuth-Plass paragraphs, character-level justification; variable fonts in 0.15; HTML and multi-file "bundle" export still experimental | High: one static binary, fast, diffable markup | Pre-1.0, breaking changes; company-governed; no native EPUB ([forum](https://forum.typst.app/t/can-typst-produce-epub-format-document/7344)); journals rarely accept it ([LWN](https://lwn.net/Articles/1092993/)) | Pin a version; render one essay with `--pdf-standard ua-1`, record warnings |
| [Pandoc 3.8](https://groups.google.com/g/pandoc-announce/c/U22SFKZE9Wk) | Hub: Markdown → Typst, HTML5, EPUB3, LaTeX; EPUB writes default accessibility metadata ([discussion](https://github.com/jgm/pandoc/discussions/9365)) | Very high | Its `smart` extension silently rewrites quotes and dashes at render time [EI, known behaviour, not re-fetched]: an *undeclared change* | Turn `smart` off downstream; make typographic normalisation a declared packet step; count what `smart` would have changed |
| [Quarto 1.9](https://opensource.posit.co/blog/2026-03-31_typst-books-and-more/) | Typst books and Tufte-style margins (sidenotes, margin figures); offline package vendoring | Medium: turnkey but heavy (bundles Pandoc + Deno) | No list of figures; book + margin quirks | Spike one essay; compare with plain Pandoc → Typst |
| [lua-typo](https://ctan.org/tex-archive/macros/luatex/latex/lua-typo) (LuaLaTeX) | Flags widows, orphans, hyphenated page breaks, stacked hyphens, short last lines, overfull boxes | Medium-low (TeX Live is huge) | — | Use its check list as the spec for render QA in any engine |
| CSS paged media: [Paged.js "next"](https://pagedjs.org/posts/paged.js-next), WeasyPrint, [Vivliostyle](https://docs.vivliostyle.org/en/cli/getting-started/) | One HTML+CSS source for web and print; Paged.js mid-rewrite; WeasyPrint active (recent SSRF CVE fixed) | Only if web-first | Print features weaker than Typst/TeX [H] | None now |
| [EPUB Accessibility 1.2 (CR, July 2026)](https://www.w3.org/TR/2026/CR-epub-a11y-12-20260721/), [EAA mapping](https://www.w3.org/TR/2025/NOTE-epub-a11y-eaa-mapping-20250819/), [DAISY Ace](https://kb.daisy.org/publishing/docs/epub/validation/ace.html) | `accessModeSufficient` becomes required; WCAG 2.0+; Ace is the standard checker | High for ebooks sold in the EU [H] | Whether a solo author falls under the EAA's micro-enterprise exemption: **not researched** | Per-book accessibility metadata file with an author-written summary; Pandoc → EPUB → Ace + EPUBCheck on one chapter |
| Web: [CSS sidenotes via anchor positioning](https://vincent.bernat.ch/en/blog/2026-css-sidenotes), `text-wrap: pretty` ([guidance](https://developer.chrome.com/docs/modern-web-guidance/guides/visual-design/improve-text-layout-and-legibility)), [Tufte CSS](https://github.com/edwardtufte/tufte-css) | JS-free sidenotes in all three engines with inline fallback; `pretty` for paragraphs only | High: one static HTML file + one CSS file | Substack/Ghost fix typography by platform [H] | ~150-line house CSS: measure ~66 ch, sidenotes, `hyphens: auto` with `lang` |
| Book GUIs (Vellum, Atticus, Kindle Create, Reedsy; [comparison](https://www.inkfluenceai.com/best-book-formatting-software), a vendor's own ranking) | Polished genre templates; Atticus advertises "no AI of any kind" | Low: closed formats break provenance | Their templates are good [H] | Use as visual benchmarks only |
| [Butterick's key rules](https://practicaltypography.com/summary-of-key-rules.html) | Encodable craft norms: 45–90 characters per line, 120–145% leading, curly quotes, real dashes, one space, indent *or* paragraph space | High | Norms, not studies; "avoid free fonts" conflicts with an open stack | Split into **text rules** (declared changes), **style rules** (one approved theme file), **render rules** (QA findings) |

**Where AI meets typesetting** [SG]: in [TeXFix-Bench](https://arxiv.org/pdf/2608.07617), LLM repairs of broken documents compiled 60% of the time for Typst (74% LaTeX, 90% Markdown), and **13.6–18.5% of compiling LaTeX repairs changed the content**. [VLMs are "typography-blind"](https://arxiv.org/abs/2603.08497): good at colour, poor at font style, not fixed by scale. Derivation [EI]: agents should propose small theme changes and semantic choices; they should not regenerate document source or judge typography alone. [DP] `render --verify`: extract the output's text and fail on any difference from the approved source.

### C. AI visual design and judging aesthetics

| Source | Claim [SG] | Fit | Counter | Derivation / next step |
|---|---|---|---|---|
| [Gamma 5, Oct 2026](https://siliconangle.com/2026/10/06/exclusive-gamma-revamps-presentation-platform-to-make-output-look-more-human/) | Rebuilt because complaints of "AI smell" and sameness grew; agent now renders and self-checks overflow and crops | Concept yes, product no (decks) | Reduction in sameness unverified | [EI] the market leader's fix is a render-check-revise loop |
| Tome ([shut down April 2025](https://www.chatslide.ai/articles/tome-ai-shut-down-what-happened)) | Standalone AI slide generator closed; founders pivoted | Caution | — | [EI] "pretty generation" alone is not a durable advantage |
| [Google Stitch, DESIGN.md](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/) | A markdown file of design rules for agents, portable between tools | Pattern fits a CLI well | Labs product | [DP] `DESIGN.md` (prose rules) + `tokens.json` (values), versioned |
| [Design Tokens 2025.10](https://www.designtokens.org/tr/2025.10/) | First stable vendor-neutral token format (OKLCH, P3, theming); Community Group report, **not** a W3C Recommendation | High: JSON, stdlib-readable | Reference tools are Node | [DP] tokens are the pinned visual identity; AI may change a value only by a labelled change |
| [WCAG 3 contrast status, April 2026](https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html) | APCA is not in WCAG 3; WCAG 2 governs | High | — | [DP] stdlib WCAG 2 contrast check on token colour pairs as a gate; APCA as advice |
| [GraphicDesignBench](https://arxiv.org/abs/2604.04192) | Frontier models handle design semantics but fail at spatial layout, faithful SVG and fine typographic perception | High as a warning | Marketing-template data, not book pages | [DP] agent proposes semantic `layout_intent`; the engine owns geometry |
| [Uni-Layout](https://arxiv.org/html/2508.02374v1) | Standard layout metrics disagree with people; a trained evaluator hit 85.5% vs GPT-4o 61.6% on pass/fail | Lesson transfers | Authors' own labels flatter their model | [EI] off-the-shelf VLM verdicts can't be a gate |
| [GPT-4o vs design principles](https://arxiv.org/html/2410.08885v1) | Beats heuristics on large flaws, worse on *small* alignment and whitespace shifts | High | 3 principles, 1 model, synthetic perturbations | [DP] two tiers: deterministic geometry checks gate; VLM critique advises |
| [UICrit](https://arxiv.org/abs/2407.08850), [iterative visual prompting](https://arxiv.org/abs/2412.16829), [VFLM (CVPR 2026)](https://cvpr.thecvf.com/virtual/2026/poster/39481) | Critique improves with expert few-shot examples and location-anchored boxes; layout made while *seeing the render* beats code-only | Method transfers | Mobile UI / posters; VFLM gives no numbers | [DP] critique items carry region, rule, severity, proposed change; the loop must include a real render; 5–10 of the author's annotated pages as examples |
| [Design homogenisation in vibe coding (MSR)](https://arxiv.org/abs/2603.13036) | Effortless generation intensifies sameness; proposes "productive friction" | Matches the augmentation purpose | Conceptual, no quantitative result | [DP] show 2–3 deliberately different variants, never one "best" |
| [Amazon KDP AI policy](https://kdp.amazon.com/en_US/help/topic/G200672390); [Thaler cert. denied, March 2026](https://pcgamer.com/software/ai/ai-generated-images-still-cant-be-copyrighted-as-us-supreme-court-declines-to-hear-case) | AI-generated text or images (covers included) must be disclosed even after heavy editing; AI-assisted need not. Purely AI-generated images aren't copyrightable in the US | Direct if self-publishing | Legal; not advice | [DP] per-asset `origin` field; a KDP disclosure summary export. Not legal advice. |

Also noted, low fit: Figma Config 2026, Canva AI 2.0, Claude Design, InDesign's generative features ("Auto Style" styles text within a template; even Adobe uses AI *inside* templates, not to invent book layout).

### D. What AI assistance does to writing and authors

| Source | Claim [SG] | Methods | Fit to a skilled long-form author | Counter | Derivation |
|---|---|---|---|---|---|
| [Doshi & Hauser 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11244532) | AI ideas raised individual creativity ratings but made stories ~10.7% more alike; **no gain for high-creativity writers** | ~300 amateurs, 8-sentence stories, crowd raters | Low task fit; the skilled-writer null is the relevant part | [Meta-analysis](https://research.tilburguniversity.edu/en/publications/does-generative-ai-make-us-think-alike-a-systematic-review-and-me-3/): small homogenisation effect across 19 studies | [EI] expected gain from AI *ideas* near zero for this author; the sameness cost remains |
| [Padmakumar & He, ICLR 2024](https://arxiv.org/abs/2309.05196v3) | Instruction-tuned co-writing reduced diversity; the effect came from **model-contributed text** | 3-arm essay study | High for mechanism | Base GPT-3 didn't homogenise | [DP] measure agent-originated share per packet |
| [Agarwal et al., CHI 2025](https://arxiv.org/abs/2409.11360) | Suggestions pulled writers toward the model's (Western) default style | 118 participants, autocomplete | Medium | Autocomplete, not declared edits | [H] polish erases whatever is idiosyncratic first |
| [Kobak et al. 2025](https://arxiv.org/abs/2406.07016v5) | ≥13.5% of 2024 PubMed abstracts LLM-processed, by excess vocabulary | 15M abstracts | High for papers | — | [DP] flag edits that introduce known excess-vocabulary words |
| [Chakrabarty et al., CHI 2025 (LAMP)](https://arxiv.org/abs/2409.14509v5) | Writers agree on a 7-category taxonomy of LLM prose faults (clichés, needless exposition…); experts preferred expert edits over automatic ones | 1,057 expert-edited LLM paragraphs | High: an "anti-slop" checklist | Tested on LLM-generated, not human, drafts | [DP] reject agent edits that *introduce* a LAMP fault |
| [Chakrabarty, Ginsburg & Dhillon 2025](https://arxiv.org/abs/2510.13939) | Prompted imitation of authors lost badly with expert readers; *fine-tuned* imitation won | 10,920 blind pairwise judgements; preprint | Medium | Blind; says nothing about disclosed use | [EI] "write in my voice" by prompting will read as worse to skilled readers |
| [Laban et al., "Beyond the Chat" (InkSync)](https://arxiv.org/pdf/2309.15337) | Chat editing introduced major factual errors in 14.8% of documents vs 6% for inline executable edits; flagging new unverified information caught 73% of bad edits | 52 + 35 participants, short emails | Very high: independent support for declared edits | Small, short tasks | [DP] every factual agent addition carries `unverified / verified / incorrect`; unverified can't be accepted silently |
| [Draxler et al., TOCHI 2024](https://arxiv.org/abs/2303.03283v1) | People don't feel they own AI text yet still don't declare the AI; ownership tracks how much they shaped it | n = 30, 96 | High | — | [DP] record *how* each change was accepted (single, bulk, modified) |
| [Dhillon et al., CHI 2024](https://arxiv.org/abs/2402.11723) | Paragraph-level help improved quality mainly for non-regular writers, at a cost in ownership; sentence-level brought no gain | 131, within-subjects | Medium | Essays | [DP] default granularity: phrase/sentence; paragraph rewrites opt-in |
| [Jakesch et al., CHI 2023](https://arxiv.org/pdf/2302.00560) | An opinionated assistant roughly doubled writing on its side and shifted later attitudes, mostly unnoticed | 1,506, one topic, strong bias | Medium-high for nonfiction | Single session | [DP] interpretation edits carry a stance note: what claim changed |
| [Kosmyna et al. 2025](https://www.media.mit.edu/publications/your-brain-on-chatgpt/) | Lower EEG connectivity and recall when ChatGPT generated essays | 54 (18 in crossover), preprint | Low: generation, not polish | [Methods critique](https://arxiv.org/pdf/2601.00856v1); author rejects "brain rot" framing | [EI] keep composition with the author; no claim about polish |
| [Reader disclosure penalty (2025)](https://arxiv.org/abs/2510.24011v2) | Disclosed AI involvement lowered trust and likability, least for AI-literate readers | 261 people | Medium | Doesn't separate assisted from generated | [H] a specific disclosure costs less than a vague one; untested |

**Disclosure rules converge on one line** [SG]: assistive copyediting vs generative or substantive change. Nature: AI copyediting of human text need not be declared, generative editorial work must ([secondary summary](https://www.enago.jp/responsible-ai-movement/publisher-ai-guidelines/nature-ai-guidelines); primary not read). ICMJE 2026: declare AI at any stage ([secondary](https://lifesciences.enago.com/blogs/key-changes-and-implications-for-medical-communication-and-publishing); primary not read). KDP: generated must be disclosed, assisted need not. [Authors Guild "Human Authored"](https://authorsguild.org/news/clarifications-regarding-the-human-authored-certification-terms/): only *de minimis* AI. [EU AI Act Art. 50](https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content), applicable from 2 Aug 2026: AI-generated or manipulated public-interest text must be disclosed unless under documented human editorial responsibility, and a substantive AI edit **after** that review voids the exception. Derivation [EI]: the packet's three labels (addition, transformation, interpretation) all sit on the substantive side; **there is no copyedit tier, which is the tier that carries the exemptions**. Not legal advice.

## Synthesis: a design proposal for the author's tool

**Five tiers, each with its own default, review and disclosure** [DP]. The tiers are a *classification to test*, not a mandatory review flow (see the cross-family review below):

| Tier | What | Default review | Checks | Disclosure effect |
|---|---|---|---|---|
| 0 Format & layout | tokens, theme, template, render | approve the theme once | text-fidelity diff (zero text change), WCAG 2 contrast, measure, render QA (widows, overflow) | none (no text changed) |
| 1 Copyedit | only explicitly enumerated mechanical operations (spelling, punctuation, typographic characters, house-style spellings) that keep propositions, attribution, modality, scope and emphasis; **never** paraphrase, terminology changes, numbers, citations or quoted text; ambiguity escalates | batch-accept allowed for enumerated operations only | style sheet, Vale/LanguageTool adapters with rule ids | generally exempt (ICMJE excepted) |
| 2 Line polish | phrase/sentence rewording | visible, local, each change shown (one-at-a-time acceptance is a hypothesis to test, not established) | LAMP-fault check, excess-vocabulary check, voice-drift metric | "AI-assisted" |
| 3 Transformation / interpretation | restructuring, paragraph rewrites, claim changes | opt-in per section; stance note for interpretation | as tier 2, plus stance note | substantive; venue-dependent |
| 4 Agent addition | new content or facts | opt-in; verification state required | unverified additions can't be accepted silently | "AI-generated" under KDP and Nature-type rules |

**Build order** (each small, each reusable alone) [DP]:
1. **Tier 0 first, as a baseline comparison:** Quarto + a good theme vs Markdown → Pandoc (pinned, `-smart`) → Typst PDF (PDF/UA) and HTML with a house CSS, `render --verify` on both, `tokens.json` + `DESIGN.md`; 2–3 representative documents; judged on output quality, text fidelity and author effort. Safest, most visible "slick".
2. **Packet renderings:** a side-by-side HTML review page (changes coloured by type, filter by tier/stage/lens, query list) and a CriticMarkup export.
3. **Copyedit tier:** typographic text rules as declared changes; a style sheet; optional linter adapters.
4. **Provenance report:** exact origin shares, how each change was accepted, a disclosure line generated per venue.
5. **Line-polish guards:** voice-drift metric, LAMP and excess-vocabulary checks; only then any "polish" agent.
6. **Visual critique (advisory):** render to PNG, location-anchored critique, 2–3 variants.

## What's missing: an expectation audit of the four analyses

Comparator: what a reader would expect from a market-and-literature survey meant to set direction for an author's polishing tool. Scope: the four slices' reports and search logs, 2026-11-18.

**Part A: expected strengths missing or under-developed**

| Candidate gap | Why expected | Status | Competing readings | Verification step |
|---|---|---|---|---|
| Any study of AI polish on a **skilled author's own long-form draft**, judged by editors or readers | It's the exact use case | NOT OBSERVED (searched for, not found) | Field gap; or it exists under other terms (e.g. "revision assistance", L2 academic editing) | Targeted search on revision/editing studies with professional writers; and the author's own packet history as an n = 1 instrument |
| Evidence on **readers' response to typography and layout** quality | "Slick" presumes readers notice | NOT OBSERVED | Legibility research exists (older, pre-AI) and wasn't in scope; or the effect is real but small | One search route into legibility/reading-speed literature (e.g. line length, font size) before claiming reader benefit |
| A **target and a budget for "pretty"**: where the work will appear (journal, KDP, site, Substack) | Pipelines differ by venue | NOT OBSERVED | Undecided by design; or decided elsewhere | Ask the author which two venues come first (since answered: a web essay and Substack; see the follow-up) |
| Audio, alt text for figures, translation, indexing | Common publishing deliverables | NOT OBSERVED (out of the brief) | Deliberately out of scope | List as later routes; alt text matters for EPUB accessibility already |
| Status of several 2026 products (Wordtune, Notion AI, Hemingway, Figma Make, v0/Framer) | Survey completeness | NOT OBSERVED (not searched) | Low relevance to a CLI tool | Leave unless a route needs them |
| Primary texts for Nature and ICMJE policy | Disclosure tier rests on them | UNCERTAIN (secondary summaries only) | Summaries accurate; or nuanced | Read primaries before any disclosure profile is built |

**Part B: expected weaknesses that turned out absent**

| Presumed weakness | Status | Note |
|---|---|---|
| "Open tools can't match commercial polish" | PRESENT / EXPECTATION WRONG for print | Typst and TeX match or beat GUI book tools on line-breaking and accessibility output; GUI tools win on ready templates |
| "Provenance machinery makes a tool slow and clunky, unlike slick products" | PRESENT / EXPECTATION WRONG (partly) | Every major vendor converged on tracked changes or suggestions; InkSync found declared inline edits made *fewer* factual errors than chat. The declared-change model is the industry direction, not a drag on it |
| "Formatting is where AI adds most" | UNCERTAIN, leaning wrong | AI is weakest exactly here (typography-blind VLMs, spatial-layout failures, destructive repairs). Deterministic tools do formatting; AI adds most as *critic and proposer* |
| "Disclosure would undercut the author" | UNCERTAIN | Penalty measured for vague AI involvement; specific, packet-derived disclosure is untested and might cost less |

**Conceptual inverse** (orthogonal frame): the brief frames "pretty" as something *added* to the text. Its complement is **subtraction**: the most consistent signal across slices is what to *remove or refuse*: silent changes (Pandoc `smart`, destructive repairs), model clichés (LAMP), excess vocabulary, look-alike AI visuals, unverified additions. A "slick" tool for a skilled author may be mostly a **refusal layer** with an excellent renderer, not a generator.

**Bottom line:** the most informative absence is the missing study of AI polish on skilled authors' long-form drafts. The tool's own packet history could be the first instrument for it, at n = 1. Not established: whether readers would notice tiers 0–1 at all.

## Follow-up: were the big absences real? (searched 2026-11-18, after the first pass)

Two targeted searches by fresh-context subagents (same family), each told to look under other terms and to be strict about what counts.

**1. AI polish on a skilled author's own long-form draft, judged by editors or readers.** Status: **SUPPORTED ABSENCE (narrowed)**. No study met all four conditions together: skilled author, their own draft, long-form text, and quality or voice judged by editors or readers. Adjacent evidence, which points the same way as section D:
- [Abdulhai et al. 2026, "How LLMs Distort Our Written Language"](https://arxiv.org/pdf/2603.18161) [SG]: three LLMs revised 86 human essays. **Even "minimal" and "grammar only" prompts** moved the essays, all in one direction, into a region no human revision reached: roughly 40–60% fewer pronouns and a stance pushed toward neutral. Limits: student essays, short texts, computational measures; the paper has internal number inconsistencies. **This is the strongest new finding. It weakens the packet's assumption that a copyedit tier is low-risk** unless its operations are mechanical and enumerated (the cross-family reviewer's definition).
- [August et al. 2026, PLOS ONE](https://www.news-medical.net/news/20260210/AI-editing-tools-make-more-corrections-but-reduce-writing-quality.aspx) [SG]: two researchers' own manuscripts, edited by a GPT tool, by Grammarly and by a human copyeditor. 61% of the GPT tool's readability edits improved the text, against 90% of the human's, and the GPT tool deleted citations. Limits: 8 paragraphs, judged by the research team.
- [Akpinar et al. 2026](https://arxiv.org/html/2601.15556v1) [SG]: 69 mostly doctoral readers couldn't tell human, LLM-generated and LLM-edited abstracts apart. With authorship disclosed, the LLM-edited ones rated clearest. Limits: abstracts only, no voice measure.
- [Teichholtz, Gero & Glassman 2024](https://cplusj2024.github.io/papers/CJ_2024_paper_23.pdf) (14 student journalists, own articles, inline suggestions; agreed with 64% of sentence suggestions) and [Hwang et al. 2025](https://arxiv.org/html/2411.13032v1) (19 professional writers, readers rated voice; AI generated rather than edited) [SG].

**2. Tracked changes vs inline suggestions vs chat, for voice.** Status: **SUPPORTED ABSENCE**. The only controlled comparison found is [AnchoredAI](https://arxiv.org/pdf/2509.16128), a preprint: anchored comments vs chat, 22 students, essays that weren't theirs. Anchored comments raised ownership and control, and cut the share of the document changed in local revisions from 22.5% to 6.8% [SG]. In [Nishal et al. (CHI 2026)](https://www.microsoft.com/en-us/research/wp-content/uploads/2026/02/designforagency.pdf), half of 20 professional science journalists ranked an accept/reject inline critic first, with voice as their main concern. Those were mockups, not real drafts [SG].

**3. Do readers notice typography?** Status: **PARTLY FILLED, so the original absence was wrong in part.**
- [Fogg et al.](https://advocacy.consumerreports.org/research/how-do-people-evaluate-a-web-sites-credibility/): readers notice presentation; "design look" came up in 46% of web credibility comments [SG]. That counts mentions, not effect size.
- In the competent range, comprehension effects are mostly null [SG]:
  - [Wallace et al. 2022](https://jeffhuang.com/papers/Readability_TOCHI22.pdf), n = 352: font had no overall effect on speed, though each reader's fastest font was 35% faster than their slowest. A reader's preferred font was their fastest only at chance rate.
  - [Beymer et al.](https://www.scienceopen.com/document_file/671b2d53-73ce-4a91-946d-fde0b7db381a/ScienceOpen/015_Beymer.pdf): font size changed fixation time, not comprehension.
  - [Atilgan et al. 2020](https://phys.org/news/2020-11-character-line-digital-text-affect.amp): reading slows only below about 13 characters per line.
- The much-cited "good type improves mood" study ([Larson & Picard](https://www.media.mit.edu/publications/the-aesthetics-of-reading-2)) used n = 20 and compared good against *terrible*, so it is weak support [SG].
- The aesthetic-usability halo was weak in [Grishin & Gillan 2019](https://uxpajournal.org/wp-content/uploads/sites/7/pdf/JUS_Grishin_Feb2019.pdf) [SG].
- The disfluent-font benefit failed a many-lab replication (Meyer et al. 2015, cited through [Korn et al. 2018](https://rd.springer.com/content/pdf/10.3758/s13423-017-1395-4.pdf)) [SG].
- Reading experiments on sidenotes vs footnotes: none found.
- Derivation [EI]: for essays, typography is **hygiene and trust**, not a comprehension lever. Aim for competent and readable, honour reader settings, and don't claim that "slick" improves understanding.

**Venue consequence (the author's first venues: a web essay and Substack)** [SG, mostly official Substack pages; custom CSS and API status partly third-party]:
- Substack offers preset themes and fonts. Custom CSS and font upload are not confirmed.
- It has native footnotes and LaTeX blocks. It has no tables and no sidenotes.
- There is no Markdown import; the usual route is Markdown → HTML → paste. There is no posting API.
- So for Substack, the job is **faithful transfer**, not typography. Typographic effort belongs on the author's own site.

## Stress-test of the verdict

- **Core claim:** build presentation first and deterministically; gate prose polish by risk tier.
- **Necessary premises:** the author's texts are Markdown or convertible; the author will review packets. **Unverified:** that the author wants print/EPUB as well as web; that tier sorting is cheap enough to do per change; that a voice-drift metric means anything at n = 1. **Value judgements:** voice preservation outranks speed; provenance outranks convenience.
- **Backfire:** the tier machinery becomes the product. The project's own working rules warn about effort going into machinery rather than decisions. Five tiers, three exports and six checks could bury "make it pretty" for months.
- **Strongest counterargument:** the author asked for *slick*, and the fastest slick is an existing product (Quarto with a good theme, or Claude Design/Canva for visuals). Wrapping everything in packets may trade visible quality for invisible accountability.
- **Reversal lens:** if polish were *not* risky for this author (a confident stylist who rejects bad edits fast), tiers 2–4 collapse into "one-at-a-time review", and the work is mostly tier 0. Part of the evidence fits that reading: skilled writers gain least from AI help. No study shows that skilled writers are also *less swayed* by it. Jakesch's participants mostly didn't notice the influence, which argues against the reversal.
- **Ethical echo:** disclosure profiles push the author toward honesty that venues reward unevenly; good. A voice-drift metric trained on the author's prose is personal data; it stays outside the tool's public repository, which holds no author texts.
- **Uncomfortable tweak:** **ship tier 0 alone first, as a thin wrapper over existing tools, and defer tiers 2–4 until the author has used it on one real piece.** Two tiers (layout; everything else reviewed one at a time) may be enough until data says otherwise.
- **What would change this:** the author's first real piece through tier 0, and a count of how many prose changes the author actually wanted.

## Cross-family review (GPT, 2026-11-18)

The reviewer, a GPT model, saw a summary of this packet, not the packet itself. Its points, with its own labels, and what was taken:
- [opinion] Presentation-first is a sound *experiment*, not yet a justified architecture. Five mandatory tiers risk making the review machinery the product. Taken: the tiers above are now a classification to test.
- [opinion] Steelman: Quarto with an excellent theme, preview and export, no tier taxonomy, originals kept, optional visible prose diffs. Compare it on quality, fidelity and author effort, because determinism doesn't establish attractiveness. Taken: build step 1 is now that comparison.
- [opinion/inferred] InkSync (short emails) motivates visible local edits and factual-change checks. It doesn't justify five tiers or one-at-a-time acceptance for long-form work. Taken: tier 2's review wording is softened.
- [opinion] Batch-accept copyediting is a loophole unless the eligible operations are explicitly enumerated. Even punctuation can change meaning. Taken: tier 1's definition is the reviewer's.
- [opinion] Missing evidence, in priority order: venue targets; a within-author pilot on real long-form drafts (polish, voice, semantic errors, review burden); blinded reader comparisons of typography (preference *and* comprehension).
- Not yet assessed: a packet-level review needs this file, the primary excerpts and the acceptance criteria.

## How this was searched

- **Date:** 2026-11-18, four parallel bounded searches by fresh-context subagents, then one synthesis, then two targeted follow-up searches on the absences (polish studies with skilled authors' own drafts; tracked-change vs inline vs chat interfaces; reader response to typography; Substack's formatting controls).
- **Routes and queries (logged by each slice):**
  - A (tools): Sudowrite 2026; Grammarly Authorship; Lex; NovelCrafter; Grammarly agents and Expert Review; Type.ai; Copilot Word tracked changes; Gemini Docs suggestions 2026; Vale; CriticMarkup/pandiff; proselint 2026; C2PA text; EFA/CIEP; Canvas removal; LanguageTool API; ProWritingAid; AI ghostwriter effect.
  - B (typesetting): Typst 0.14/0.15; Pandoc 3.8 Typst; Quarto 1.9 books; EAA EPUB a11y; Vivliostyle; Paged.js 2026; WeasyPrint; LLM Typst benchmark; VLM typography; `text-wrap: pretty`; Ace/Pandoc EPUB metadata; Vellum vs Atticus 2026; widows/rivers QA; Typst EPUB; Ghost 6; Tufte sidenotes; Butterick.
  - C (design): Tome/Lightfield; Gamma 2026; Design Tokens 2025.10; UICrit; KDP AI disclosure; Stitch; GDB; LayoutPrompter/PosterLlama/LayoutGPT; VLM critique refinement; APCA/WCAG 3; Figma/Canva/InDesign; USCO/Thaler; Microsoft Designer; MLLM aesthetic judges; layout metrics; publisher AI covers/C2PA; Mermaid/D2 benchmarks; homogenisation; Figma Config 2026.
  - D (evidence): Doshi & Hauser; Padmakumar & He; Agarwal et al.; LAMP; Draxler; Kosmyna and critiques; Dhillon; KDP; EU AI Act Art. 50; Nature; ICMJE; Authors Guild; Lee et al. design space; disclosure penalty; fine-tuned imitation; Gero/Biermann; Jakesch; Kobak; "Catch Me If You Can"; homogenisation meta-analysis; CoAuthor; executable edits.
- **Read at abstract or summary level** for most papers; full text was not read. Doshi & Hauser figures come from a press summary (PMC returned a captcha).
- **Looked for, not found:** AI polish on skilled authors' long-form drafts; a study comparing tracked-change vs inline-suggestion UIs for voice; any tool typing edits as addition/transformation/interpretation with rationales; an open-source river detector; render-critique loops on long-form typography; an official C2PA text binding; OpenAI's own Canvas removal note; EAA ruling for solo self-publishers; Nature and ICMJE primary pages (fetches failed or not attempted).
- **Not searched:** Wordtune, Hemingway, Notion AI, Figma Make, v0/Lovable/Framer status; legibility research; translation and audio.

