# Book Generation Pipeline Plan (LLM-Assisted)

**Book:** *Rekayasa Fitur Modern: Representasi Data untuk Machine Learning dan Deep Learning*
**Audience for this doc:** Research Assistant building the pipeline.
**Goal:** Produce a first draft of the book (per subsection) via LLM agents, with layered quality control.

> **Working language:** All planning, prompts, and agent reasoning are in **English** — it is the stronger language for both the author and the models. The book's final output is **Bahasa Indonesia**, composed directly by the Writer Agent from a structured brief (see Track 1). Do not conflate the two: think in English, ship in Indonesian. **There is no full English prose draft** — the English artifacts are the brief/spec and planning notes; the writer never translates an English draft, it composes Indonesian from the spec (§5). This is deliberate: a complete English draft would contaminate the Indonesian with translation structure, the exact failure mode the pipeline exists to avoid.

---

## 1. Architecture: Three Sequential Tracks

The book has 17 chapters and hundreds of subsections. It is a **hybrid textbook**: the book is the canonical source (*what* & *why*); the companion repo is the implementation (*how*). Production runs as three strictly ordered tracks, each with its own generation logic and verification questions.

```
TRACK 1 — BOOK TEXT (prose)
  Outline → Compilation Agent → Structured Brief
                                     → Writer Agent → Draft
                                          → Technical Review → Editorial Review
                                              → Human Approval (per subsection)
                                                → Chapter Integrator (per chapter)
                                                  → Redundancy/Transition Review
                                                    → Whole-Book Coherence Pass ──┐
                                                                                  │
TRACK 2 — NOTEBOOKS (code, after chapter approved)               │
  Approved Chapter → Notebook Agent → Auto Execution Gate ───────┤
                                          → Human Spot-Check ─────┐
                                                                  │
TRACK 3 — PROJECTS (mini-projects + capstones, after notebooks)   │
  Approved Notebooks → Project Agent → Verify divergence + rubric ┘
```

**Why strictly sequential:** Track 2 uses approved prose + brief as its *spec* (the prose already decided which techniques, trade-offs, and case studies). Track 3 needs both prose *and* notebooks stable — per-chapter mini-projects reuse a chapter's datasets/transformers, and cross-chapter capstones flag prerequisite chapters. Order is forced: **book → notebook → project.**

**Why stages are split inside Track 1:** compilation demands *accuracy & coverage*; writing demands *language, coherence, tone*. One prompt doing both degrades both and blurs failure diagnosis. With separation: bad content = compilation problem; bad writing = writing problem.

**Why a Chapter Integrator stage:** subsections are generated independently, so assembled raw they repeat introductions, re-define terms, transition abruptly, vary in depth, and overuse "in this section" framing. After all of a chapter's subsections are approved, a **Chapter Integrator** assembles them and a **redundancy/transition review** removes duplicate definitions, smooths joins, and levels depth. After all chapters, a lighter **whole-book coherence pass** checks prerequisites, cross-references, repeated material, and terminology end-to-end. Chapter-level context (§5) reduces fragmentation but does not eliminate it, so integration is a real stage, not an afterthought.

---

## 2. Style Target (reference for all stages)

- **Tone:** academic but **as accessible as possible** — readers are undergraduates of varying ability.
- **Language:** natural Bahasa Indonesia, **not** a stiff translation of English. This is the critical quality bar.
- **Term policy:** keep established technical terms in English (*machine learning, feature, embedding, pipeline, leakage*); translate connective and conceptual vocabulary.
- **Core term pair (consistent book-wide):** *representasi yang **dirancang manusia*** ↔ *representasi yang **dipelajari mesin*** (designed by human ↔ learned by machine). The explicit agents *manusia / mesin* are load-bearing; never the bare *dirancang / dipelajari* (bare *dipelajari* wrongly reads as learned *by us*). See `glossary-seed.md` and `writer-system-prompt.md`.
- **Keep the spine subtle — mention it rarely.** It is the organizing thesis, but it is **introduced once (Ch 1), resolved at the synthesis (Ch 17), and carried by the book's *structure*** in between (the parts march designed→learned). Explicit mentions are **rare and default-off** — at most a light touch at the one or two most important turning points; **never a per-subsection callout.** The compiler flags it in a brief only at those few moments; the writer never adds it by reflex. Stated often, it stops landing.

**Indonesian-specific issues the Editorial Review must watch:** calques (visible English sentence structure), natural vs. careless passive *di-*, formulaic connectives (*oleh karena itu, dengan demikian*), correct *kita* vs. *kami*, and natural choice between loanwords and local terms.

### Length budget (planning anchor — the binding figure is Indonesian)

| | |
|---|---|
| **Physical target** | ~300 B5 pages (hard ceiling +5–10%, ≈330 pages) |
| **Binding word target (Bahasa Indonesia)** | **~52,000 words** (range 50–54k) — the shipped figure, allocated per chapter/subsection |
| **English planning estimate** | **~45,000 words** — a *brief-sizing* estimate only, **not an English prose draft** (none exists); used to reason about scope before Indonesian composition |

**Derivation:** 300 pages × ~240 words/full text page = ~72k words at 100% text; reserving 25–30% of space for figures/tables/headers/code leaves 70–75% for prose → ~50–54k Indonesian words. The ~45k English figure is a planning convenience (briefs and scope are reasoned in English, the working language); the writer never produces an English draft, it composes Indonesian directly from the spec (§5). *This supersedes the earlier 65k estimate — the page-based math is tighter.*

> **Provisional — calibrate with pilots before locking layout.** The 240-words/B5 density and the Indonesian expansion factor are planning assumptions, not measured facts. Before finalizing the book-wide budget, **typeset two pilot chapters** — one mainly textual (Ch 4) and one notation/figure-heavy (Ch 8 or Ch 14) — and use their actual page densities (equations, tables, caption and heading density, paragraph spacing) to confirm or adjust the number. Plan to the anchor now; do not treat it as physically verified.

**Consequences:**
- **Per-chapter average:** ~52k ÷ 17 ≈ **~3,000 Indonesian words/chapter** (core chapters more; intro/conclusion/appendix-pointers less). Allocate per chapter from the book budget, not uniformly.
- **The per-subsection word budget is set in Indonesian words** — the binding target the writer receives — once the subsection breakdown is frozen (see §9).
- **Verify in Indonesian.** The binding total is the Indonesian 50–54k. If a chapter overshoots, trim at the brief/spec level (cut scope), not by compressing finished Indonesian prose.
- Density discipline still applies — it reinforces keeping code in the repo (§5), not relaxing it.

---

## 3. Per-Agent Model Selection

The architecture allows a **different model per stage**. Evaluate each against its own criterion.

| Agent | Criterion | Evaluation method |
|---|---|---|
| **Writer** | Language & tone (subjective) | Shared system prompt across models → blind-score randomized outputs on the **3-dimension rubric** (1 Naturalness & correctness / 2 Register & accessibility / 3 Technical & terminological fidelity; tie-break on D1; see `writer-eval-rubric.md`). Test on a contiguous multi-subsection run (not one paragraph) so term consistency and transitions show. Pick top 2, then a second round with per-model prompt tuning. |
| **Compilation** | Accuracy & structure (objective) | Give topics you know well; run 2–3× per topic to catch hallucination variance; test with and without web search. Indonesian quality is irrelevant here (output is a structured brief, not prose). |
| **Technical Review** | Fidelity to brief (objective) | Plant known errors (missing concept, false claim, wrong term); measure catch rate and specificity. |
| **Editorial Review** | Indonesian prose (objective-ish) | Plant known errors (awkward sentence, calque, inconsistent term); measure catch rate and specificity. |

**Consistency note:** a model that scores a steady 8/10 every chapter beats one that swings 10/10 ↔ 5/10.

**Why Review is two sequential calls, Technical first:** asking one model to judge complex technical logic *and* nuanced linguistic register at once degrades both. Split into two API calls with different system prompts. Run **Technical first** — no point polishing prose that may be restructured for a missing concept.

- **Technical Review** runs **two checks**: (a) draft *against the Compilation Brief* — gap detection (brief points missing from draft), hallucination detection (claims not in the brief), terminology drift from earlier chapters; and (b) **high-risk claims against their original sources** — checking only against the brief catches writer drift but *not a wrong brief*. Because each factual brief item carries provenance (source, excerpt/location, type, date, confidence; §4), the reviewer can verify load-bearing or surprising claims at the source, so a compilation error does not silently become an "approved fact."
- **Editorial Review** focuses only on prose, flow, and translation nuance: specific language critique (name the calque/register issue, not "sounds unnatural"), core-term consistency (per Living Glossary), and calibration (flag real problems, not nitpicks).

---

## 4. Compilation: Sourcing

**Web search + library docs are sufficient for most chapters.** Feature engineering is a mature, practice-oriented topic; the best material is on the open web and better-pitched for undergraduates than academic papers.

**Academic API (arXiv / Semantic Scholar) is used for two purposes only:**
- *Primary source* (no good alternative): **Ch 8** (UMAP), **Ch 13** (GNN, Node2Vec), **Ch 14** (CLIP, multimodal), **Ch 15** (tabular DL: FT-Transformer / TabNet), **Ch 16** (CAAFE, Deep Feature Synthesis / AutoFE).
- *Recency layer* (all chapters): "Modern" in the title demands current developments — e.g. Ch 4 (new target-encoding/embedding variants), Ch 5 (MIWAE/diffusion imputation), Ch 7 (deep feature selection), Ch 9 (SHAP), Ch 10–11.

**Two-sublayer compilation — separate searching from synthesis:**

```
Subsection topic
  → GATHER LAYER:   web search + library docs + trusted blogs (+ academic API when needed)
  → SYNTHESIS LAYER: model with NO search → structured brief
  → Structured Brief → Writer Agent
```

**Two source tiers, handled differently:**
- **High-trust (hard-coded URLs, fetched directly first):** library docs, the trusted blogs below, `aikho/awesome-feature-engineering`. One relevant article here beats five generic search hits.
- **General search (Tavily, filtered to 2024+ and quality signals):** Towards Data Science, company blogs, Kaggle write-ups.

**Source priority stack:** (1) library docs → (2) trusted blogs → (3) web search (Tavily) + Kaggle → (4) Exa.ai semantic (optional) → (5) arXiv/Semantic Scholar (4 chapters as primary; cross-chapter recency). **Skip** Perplexity API (redundant with our own synthesis agent). **Deprioritize** Machine Learning Mastery and Analytics Vidhya (often oversimplified/outdated).

**Library docs per chapter:**

| Chapter | Primary docs |
|---|---|
| Ch 2–7, 9 | scikit-learn, Feature-engine |
| Ch 10 | tsfresh, tsfel, statsmodels |
| Ch 11, 15 | HuggingFace, SBERT |
| Ch 12 | HuggingFace, torchvision, torchaudio |
| Ch 13 | PyTorch Geometric, NetworkX |
| Ch 14 | HuggingFace multimodal, CLIP |
| Ch 16 | featuretools (DFS), AutoML (FLAML / auto-sklearn) |

**Hard-coded trusted blogs:** Train in Data / Soledad Galli (Feature-engine author; Ch 3–6, hard priority), Chip Huyen (production ML, feature stores; Ch 2, 17), Sebastian Raschka (tabular DL, scaling; Ch 3, 15), Hopsworks (feature stores; Ch 2, 17), Jay Alammar (visual embedding/attention; Ch 11, 15), Lilian Weng, Sebastian Ruder (NLP; Ch 11), distill.pub (Ch 8, 11, 12), company eng blogs — Airbnb/Uber/Spotify/Netflix (feature stores; Ch 2, 17), Google/Meta AI (latest pretrained; Ch 15).

**Brief format:** structured, not prose — labeled sections (key concepts, definitions, examples, relations to other chapters, terminology preferences). Subsection-level granularity (you control emphasis, not the model). **Explicitly mark what to exclude** — tangential detail to drop for undergraduate accessibility.

**Provenance is mandatory (per factual item).** Each load-bearing claim carries: `source` (id/URL), `excerpt_or_location` (the supporting quote or section), `type` (docs / blog / paper), `date` (publication or version), `confidence` (verified / uncertain). This is what lets Technical Review spot-check high-risk claims at the source (§3) rather than trusting the brief blindly — a compilation error must not be able to pass as an approved fact. Provenance lives in the brief's metadata, not in the prose the writer composes (it is spec, not text to render).

> **Hard rule — the brief is a spec, never a draft.** The compiler passes *what to say and in what order*, never the sentences to say it in. No full English sentences intended for rendering: concepts as bullets, definitions as 5–10 word glosses, examples *described* ("show X by comparing A vs. B") not written out, and the Indonesian target term given up front for each term. **Why it matters:** if the brief contains polished English prose, the writer anchors on it and *translates* instead of composing — which surfaces unnaturalness (a known failure mode for translation-style generation, e.g. Gemini). Keeping the brief skeletal forces the writer into freeform Indonesian composition, its strong mode. This is the whole point of separating compilation (accuracy/structure) from writing (language/tone) in §3.

---

## 5. Writer Agent: Context Structure

Three context layers feed the writer:

| Layer | Contents | Frequency |
|---|---|---|
| **Book-level** | Topic, audience, tone guide, **Global Notation Tracker**, **Living Glossary**, overall structure | Every call |
| **Chapter-level** | Chapter's place in the narrative — what precedes, what follows | Every call in chapter |
| **Section brief** | Compiled material for the specific subsection (+ LaTeX for notation chapters) | Every call |

Chapter-level context is easy to skip but matters — it stops each section reading as an isolated fragment. The writer needs to know "this builds toward X" and "the reader already understands Y."

**Global Notation Tracker.** For notation-heavy topics (UMAP, GNN, attention), notation drifts if left to the writer's discretion. Fix an explicit LaTeX standard in book-level context (matrices = capitals, $X \in \mathbb{R}^{n \times d}$; vectors = bold lowercase, $\mathbf{x}$; etc.). The **Compilation Agent supplies the required equations in the brief** for notation chapters (Ch 8, 13, 14, 15) — the writer only weaves notation into narrative, never derives it. This keeps derivation accuracy in the accuracy-focused agent and prevents cross-chapter inconsistency (invisible per-chapter, glaring book-wide).

**Living Glossary.** Across hundreds of subsections, new English terms needing a standard Indonesian rendering will appear, and terminology drift is near-certain. Maintain a dynamic `glossary.json`: whenever the human reviewer decides a rendering during review, it lands here and is **loaded into book-level context** for all later generations. It is **seeded up front** (`glossary-seed.md`) with the decisions already made — the spine pair, the Indonesian-used-as-is list (*fitur, distribusi, …*), the English-kept list, and the purist forms to avoid — so review only *extends* it. Bonus: this file **builds Appendix D (Glossary) as a by-product** of review.

**Code in the book body — capped, not banned.** The default is still *no code as the explanation*: prose names functions/components and describes the flow in words. The relaxation: a **small budget of short "signature" snippets** is allowed where the *shape of the call is the lesson*. Rules:
- **Inline one-liners** (`StandardScaler().fit(X_train)`) are free and uncapped. **Block snippets ≤ ~5 lines**, roughly **1 per chapter on average** (~15–20 book-wide), only where prose genuinely can't carry the call shape (e.g. the `Pipeline` fit/transform contract, a leaking-vs-correct split).
- **Snippets are copied verbatim from the chapter's verified notebook (Track 2), never hand-written in prose** — so in-book code cannot drift or hallucinate an API. A block snippet may only be filled in after its notebook exists and passed the auto gate.
- Still inside the **API-name accuracy** check (exact names from Priority-1 docs).

Consequences:
- Track 1 **still authors and executes no code.** The writer leaves a **placeholder** — `[KODE: <what to show>; sumber: notebook bab]` — exactly the way it specs a figure; the real snippet is dropped in at **chapter assembly**, copied from the notebook once Track 2 has built it. This keeps the book→notebook order intact (a block snippet is a Track-2 dependency, not a Track-1 one).
- Only **prose-level API-name accuracy** is checked in Track 1; full execution verification still belongs entirely to **Track 2** (§7), and the in-book snippet inherits its correctness from the notebook it was copied from.

**Referencing the repo from the prose (notebooks, exercises, mini-projects).** The book is the stable index; the repo is the living content (§8). How each surfaces in-chapter:
- **Notebooks — mentioned, not explained.** Where a subsection's concept is demonstrated in code, the prose points to the chapter notebook ("the chapter notebook runs this on dataset X") like a figure reference. The walkthrough lives in the repo. The **subsection writer** may drop this inline.
- **Exercises & conceptual questions — in the book.** End-of-chapter, part of the pedagogical package above (chapter-level).
- **Mini-projects — a brief pointer only.** In-book = task + the two axes + "→ repo"; the full menu, datasets, and rubric stay in the repo.
- **Capstones — appendix pointer only** (Appendix F).
- **Who writes what:** the subsection writer adds only inline notebook/figure pointers and `[KODE]`/`[GAMBAR]` placeholders. Exercises, the mini-project pointer, objectives, and summary are **chapter-level**, assembled at the chapter template / Integrator stage (§1) — the writer must not invent them mid-subsection.

### Pedagogical apparatus & figures (per-chapter package)

The page budget reserves 25–30% for figures, tables, headings, and apparatus, so these need an explicit process, not ad-hoc addition after the prose. Two parts:

**Fixed per-chapter pedagogical package (template, every chapter):** learning objectives, prerequisite reminder, an opening motivating problem, at least one worked example, one decision/comparison table or figure, a leakage/misconception callout, a chapter summary, conceptual questions, a practical exercise, and references/further reading. Freeze this as part of the reusable chapter template (§9, step 6) so every chapter ships the same scaffolding.

**Figure inventory & review gate.** Figures are content, not decoration. The writer **specs** each figure in place (the `[GAMBAR n]` callout: judul, tipe, what to depict, data source) and references/explains it in prose, but **does not draw it** (handled like code: spec in Track 1, produce later). Maintain a live `figures.json` (number, chapter, caption, type, data source/notebook, license/source check, status). A later production step renders them and a **figure technical-review** checks caption accuracy, numbering, that each figure is referenced and explained in text, and licensing. Data-plot figures sourced from notebooks are produced in Track 2; conceptual diagrams in a dedicated figure step. A figure is not "done" until it is numbered, captioned, referenced in text, explained, and license-cleared.

---

## 6. Orchestration (scaling to hundreds of subsections)

**API ≈ web UI.** The web UI only feels smarter because tools (esp. web search) are on by default. The same is available via API — Claude `web_search_20250305`, OpenAI `web_search_preview`, Gemini Google Search grounding. The compilation agent (search → synthesize) is fully reproducible via API.

**Design decisions:**
1. **State management is mandatory.** With hundreds of subsections the pipeline *will* fail mid-run. Track each subsection's status across the full cross-track lifecycle: `compile_pending → compiled → written → tech_reviewed → edit_reviewed → prose_approved → notebook_pending → notebook_passed_gate → notebook_approved → project_pending → project_done` (+ `failed` at any stage). Enables resume without restarting and keeps cross-track dependencies tracked.
2. **Async + rate limiting.** Run several subsections concurrently but respect limits: `asyncio` + `Semaphore` (~5–10 concurrent calls).
3. **Separate run per stage.** Don't chain compile→write→review in one long run. Compile all subsections, review the briefs, *then* write — human checkpoints between stages make failures cheap to recover. Same between tracks: approve a chapter's text before generating its notebooks; stabilize notebooks before projects.
4. **Files, not just memory.** Persist every brief and draft to disk immediately (`briefs/ch02_s03_*.json`, `drafts/ch02_s03_*.md`). Treat the filesystem as the project database.
5. **Three live state files built as you go:** `glossary.json` (Living Glossary → Appendix D), `dataset_chapter_matrix.json` (Dataset × Chapter Matrix → Appendix E), and `figures.json` (figure inventory → production + figure review, §5). All become single sources of truth that later tracks need, rather than reconstructing.

**Recommended stack:** Python + `asyncio`; `anthropic` SDK with `web_search_20250305`; `requests` to Semantic Scholar; SQLite or JSON state; Markdown drafts + JSON briefs; `asyncio.Semaphore` for rate limiting. **Avoid heavy frameworks** (LangChain/CrewAI) — the pipeline is a fairly linear DAG; a clean custom script is easier to debug while iterating.

---

## 7. Track 2 — Notebook Generation (after chapter approved)

Notebooks are the *"how"* half of the hybrid textbook. Run **after** the chapter's prose is approved.

**Consistency contract:** approved prose + brief is the notebook's *spec* — the prose already chose the techniques, trade-offs, and case studies; the notebook only implements them faithfully. The contract is directional and testable: the notebook must satisfy the book, and **the book is the canonical spec**. But canonical does not mean immutable — if implementation reveals the prose specifies an invalid parameter, an impractical workflow, or a misleading claim, the notebook failure may **open a controlled change request against the prose** (logged, reviewed, versioned), instead of the notebook silently diverging. The default stays book-leads-notebook; backward correction is the controlled exception, not a free-for-all. The review question is concrete: *"does this notebook do exactly what the approved chapter says — and if it can't, why, and does the book need a fix?"* The Notebook Agent also **pulls exact API names/params from Priority-1 docs** to prevent hallucinated/deprecated functions.

**Two-layer verification:**

```
Approved Chapter (prose + brief)
  → Notebook Agent (pulls exact API from Priority-1 docs)
  → Auto Execution Gate ──fail──> back to generation
       │ pass
  → Human Spot-Check (sampled) → approve / fix
```

- **Auto gate (cheap, every notebook):** execute top-to-bottom in a clean environment; fail on exception, import error, or deprecated-API warning. This is the right home for the "hallucinated/deprecated function" concern — always a notebook problem, not a book problem.
- **Human spot-check (expensive, sampled):** the RA verifies the notebook actually *demonstrates the concept*, not merely that it runs. Code can pass execution yet illustrate the wrong thing or give misleading results — only a human catches "runs but doesn't show the chapter's claim."

---

## 8. Track 3 — Mini-Projects & Capstones (after notebooks stable)

The last track. These artifacts are **pedagogically distinct** from prose and notebooks; the outline already fixes their design.

**Why separate and last:** mini-projects reuse a chapter's curated datasets and reusable transformers and point back to the repo — they can't finalize before that chapter's prose *and* notebooks are stable. Cross-chapter capstones are stricter: they flag prerequisite chapters (a capstone spanning Ch 4, 6, 9 needs all three stable). These live in the repo, not the printed book (only ~1 page/appendix as a pointer) — the outline deliberately wants them **updatable post-publication without a reprint** ("living content").

**Verification questions (unlike the other tracks) — does the divergence space actually work?**
- Do the 6–12 paths (3×2 up to 4×3) genuinely produce different student work?
- Does **one rubric** truly apply across all paths?
- Is the **mandatory comparison/ablation** requirement met?
- For the **capstone framework** (students design their own): does it inherit the book's discipline — anti-leakage validation, mandatory ablation, the *designed → learned* reflection question?

**Coordination backbone — Dataset × Chapter Matrix (Appendix E).** Mini-projects deliberately reuse datasets across chapters; capstones flag prerequisites. Both need one source of truth for "which dataset, in which chapter, for which axis." Building `dataset_chapter_matrix.json` as the pipeline runs (§6, like the Living Glossary builds Appendix D) gives the project stage a ready dependency map instead of reconstructing one.

---

## 9. Execution Order

1. **Fix the style target + shared system prompt first** (§2), and the **Global Notation Tracker**, before comparing any models.
2. **Evaluate models per agent** (§3): writer (blind scoring), compilation (ground-truth), technical & editorial review (planted errors each).
3. **Build Track 1 and test manually on 5–10 subsections** end-to-end (gather → synthesize → write → technical → editorial) to surface prompt/brief-format/model issues early. **Full automation comes after the pipeline is proven, not before.**
4. **Scale the text to hundreds of subsections** with orchestration (§6), stage by stage with human checkpoints. Build `glossary.json`, `dataset_chapter_matrix.json`, and `figures.json` as you go.
5. **Integrate per chapter, then book-wide:** after a chapter's subsections are approved, run the **Chapter Integrator** + redundancy/transition review; after all chapters are drafted, run the **whole-book coherence pass** (prerequisites, cross-references, repeated material, terminology) (§1).
6. Once a winning setup exists, freeze a reusable **chapter template** (prompt + structure + the per-chapter pedagogical package, §5).
7. **Track 2:** after a chapter is approved, generate notebooks → auto gate → human spot-check (§7).
8. **Track 3:** after notebooks stabilize, generate mini-projects then capstones; verify divergence space and rubric (§8).

---

## 10. Key Decisions at a Glance

- **Length anchor (planning; calibrate with pilots):** ~300 B5 pages → **~52k Indonesian words** shipped (binding); ~45k English is a brief-sizing estimate, **not a draft**; ~3k Indonesian words/chapter avg. **No full English prose draft exists** — the writer composes Indonesian from the spec. Typeset 2 pilot chapters before locking layout (§2).
- **Three strictly sequential tracks:** book → notebook → project, each with its own generation logic and verification questions.
- **Within Track 1:** separate compilation, writing, review — different model strengths, clear failure diagnosis.
- **Review = two calls:** Technical (fidelity to brief) then Editorial (Indonesian prose).
- **Source provenance in briefs:** every factual item carries source / excerpt / type / date / confidence; Technical Review spot-checks high-risk claims *at the source*, not only against the brief — so a wrong brief can't pass as approved fact.
- **Chapter Integrator + whole-book coherence pass:** assemble per chapter (de-dupe definitions, smooth transitions, level depth), then a book-wide consistency pass — because 100+ independently generated subsections fragment otherwise.
- **Pedagogical apparatus & figures are first-class:** fixed per-chapter package (objectives, worked example, callouts, summary, exercises, references) + a `figures.json` inventory and figure review gate; figures are specced by the writer, produced later, never inserted unexplained.
- **Notebook contract is directional, not rigid:** book is canonical but not immutable — a notebook failure can open a controlled change request against the prose.
- **Global Notation Tracker** in book context; Compilation Agent supplies LaTeX in briefs (Ch 8, 13, 14, 15).
- **Living Glossary** (`glossary.json`) → Appendix D; **Dataset × Chapter Matrix** → Appendix E; **figure inventory** (`figures.json`) → figure production/review; all built as the pipeline runs.
- **Code in the book is capped, not banned:** inline names free + a small budget of ≤5-line *signature* snippets copied verbatim from verified notebooks (~1/chapter). The writer leaves a `[KODE]` placeholder; the snippet is filled at chapter assembly from Track 2. Track 1 authors/executes no code; correctness is inherited from Track 2 (auto gate + human spot-check).
- **Mix models per stage** freely.
- **Web search + library docs suffice for most chapters;** academic API only for 4 chapters as primary + a cross-chapter recency layer.
- **Two source tiers:** high-trust (hard-coded, fetched first) vs. general search (filtered to 2024+).
- **Orchestration pillars:** cross-track state management, async + rate limiting, one run per stage, output to files; avoid heavy frameworks; prove on 5–10 subsections before full automation.
