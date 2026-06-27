---
chapter: ch16
title: Automated Feature Engineering & Human–AI Collaboration
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 16 Resources — Automated Feature Engineering & Human–AI Collaboration

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence).

## Coverage baseline (what the drafts already have)

- **ch16_s01 (DFS & Search Space):** DFS algorithm mechanics (transformation vs. aggregation primitives), depth concept (depth-2 stacking example), feature space explosion problem. No mention of FeatureTools library, its API, performance characteristics, or recent enhancements.
- **ch16_s02 (AutoML & Feature Pipelines):** Abstract AutoML pipeline search, combinatorial explosion, baseline-generation value, "burning compute" risk. No mention of specific AutoML frameworks (AutoGluon, H2O, MLJAR) or their concrete FE strategies.
- **ch16_s03 (GenAI & Spurious Features):** CAAFE framework at high level, plausible-but-spurious risk, cross-validation validator. Mentions only CAAFE; no follow-up LLM-FE systems, no fine-tuning approaches, no benchmarks.
- **ch16_s04 (Human-in-the-Loop):** HITL architecture conceptually, role shift from coder to auditor, positioning on the *dirancang manusia* spectrum. No specific HITL frameworks, no empirical user studies.
- **ch16_s05 (Case Study):** Retail churn prediction with DFS→filter→human curation→final model. Concrete but self-contained; no reference to published results or benchmarks.

---

## Resources by subsection

### ch16_s01 — Automated Feature Generation: Deep Feature Synthesis and the Search Space

- **FeatureTools v1.31.0 — Current DFS API & EntitySet**  [NEW]  (confidence: verified)
  - Summary: FeatureTools (now by Alteryx, latest v1.31.0 May 2024 supporting Python 3.12) uses `EntitySet` to describe relational schemas (tables + relationships) and `ft.dfs()` to run Deep Feature Synthesis. The API exposes `ft.graph_feature()` for feature lineage visualization and `ft.describe_feature()` for English descriptions of generated features. Guides cover tuning DFS (`max_depth`, `ignore_variables`), specifying primitive options, and improving computational performance.
  - Why relevant: The draft describes DFS abstractly but never names FeatureTools. This provides the concrete library, the canonical `EntitySet` abstraction, and feature lineage tooling that directly supports the ch16_s05 case study. Also supplies the cutoff-time mechanism (point-in-time correctness) that bridges to ch06_s04.
  - Source: https://featuretools.alteryx.com/en/stable/ · type: docs · date: v1.31.0 (May 2024)

- **FeatureTools Release History — Single-Table DFS & Performance Gains**  [NEW]  (confidence: verified)
  - Summary: Key milestones: v1.26 (Apr 2023) introduced experimental **single-table DFS** algorithm. v1.14 (Sep 2022) refactored `build_features` for **~50% speedup** on long-running DFS calls. v1.15 changed default `gap` for rolling primitives from 0→1 to prevent accidental leakage. v1.25 removed `Correlation` and `AutoCorrelation` primitives specifically because they could leak data. Dask became optional (v1.26), removing heavy dependency.
  - Why relevant: The draft's "feature space explosion" discussion gains concreteness from real-world lessons — FeatureTools maintainers removed primitives due to leakage risk, optimized computational backends, and experimented with single-table use cases. These are concrete examples of the explosion/mitigation tension the draft describes.
  - Source: https://featuretools.alteryx.com/en/stable/release_notes.html · type: docs/changelog · date: through v1.31.0 (May 2024)

- **FeatureTools — Tuning DFS & Computational Performance Guides**  [NEW]  (confidence: verified)
  - Summary: Official guides document `max_depth` control (limits recursive traversal), `ignore_variables` (exclude columns from synthesis), `drop_contains` (filter features by substring), and `where_primitives` (restrict primitives by variable type). Performance guide covers chunking, caching, and parallelization strategies. Cutoff-time handling allows point-in-time correctness for temporal datasets.
  - Why relevant: Gives concrete mitigation strategies against feature space explosion that the draft only mentions as a problem. The cutoff-time mechanism links directly to the "waktu sejak login terakhir" leakage example in ch16_s05 and to point-in-time joins in ch06_s04.
  - Source: https://featuretools.alteryx.com/en/stable/guides/tuning_dfs.html & https://featuretools.alteryx.com/en/stable/guides/performance.html · type: docs · date: v1.31.0

### ch16_s02 — AutoML and Automated Feature Pipelines

- **AutoGluon Tabular — AutoMLPipelineFeatureGenerator Architecture (v1.5.0)**  [NEW]  (confidence: verified)
  - Summary: AutoGluon's FE pipeline processes data in 5 generator stages: (1) AsType → (2) FillNa → (3) Identity/Category/Datetime/TextSpecial/TextNgram generators → (4) DropUnique → (5) DropDuplicates. Datetime columns are auto-expanded into year/month/day/dayofweek. Text columns get n-gram (count-vectorizer), character/word count features plus special stats. Categoricals are monotonic-integer encoded. Columns with single value or duplicates are dropped. The pipeline is fully configurable via `PipelineFeatureGenerator` and can be extended with custom generators.
  - Why relevant: The draft discusses AutoML abstractly as "pipeline search"; this shows a concrete production AutoML system's actual FE architecture. The multi-stage design with type-aware generators is a teachable pattern. The modularity demonstrates that even fully automated FE pipelines are composable and inspectable — directly supporting the ch16_s04 HITL argument.
  - Source: https://auto.gluon.ai/stable/tutorials/tabular/tabular-feature-engineering.html · type: docs · date: v1.5.0 (2025)

- **AutoGluon v1.5.0 — Tabular Foundation Models & TabArena Integration**  [NEW]  (confidence: verified)
  - Summary: AutoGluon v1.5 introduced a new `presets='extreme'` quality tier using Tabular Foundation Models (TFMs) meta-learned on the TabArena benchmark: TabPFNv2, TabICL, Mitra, TabDPT, and TabM. These TFMs effectively learn feature representations during pretraining on synthetic tabular data, blurring the line between "feature engineering" and "model architecture." The standard AutoML still ships with ~20 model families including LightGBM, CatBoost, XGBoost, neural nets, and weighted ensembles.
  - Why relevant: This is the most significant post-2024 development in AutoML-over-tabular-data. TFMs represent a third path for tabular FE beyond handcrafted and classical AutoML — learned tabular representations that are zero-shot or few-shot. Directly enriches the "where AutoML helps vs. burns compute" tradeoff discussion.
  - Source: https://auto.gluon.ai/stable/tutorials/tabular/tabular-essentials.html & https://tabarena.ai · type: docs & benchmark · date: v1.5.0 (Dec 2025)

- **H2O AutoML — Model-Focused Automation vs. FE Pipeline**  [NEW]  (confidence: verified)
  - Summary: H2O's AutoML (v3.20+) focuses on automated model search (GLM, GBM, DRF, XRT, DeepLearning + Stacked Ensembles) with little explicit FE pipeline — it relies on H2O's internal handling of numeric/categorical types. The system searches over hyperparameter grids for each algorithm family within a time/model budget. Feature engineering is largely left to the user as a pre-step, making H2O a useful contrast case for "AutoML that does minimal FE" vs. AutoGluon's type-aware pipeline.
  - Why relevant: Provides a useful contrast for the "where AutoML helps" discussion — not all AutoML systems are equal in their FE capabilities. H2O represents the model-search-centric end of the spectrum, AutoGluon represents the FE-pipeline-centric end. Helps the book draw a sharper distinction.
  - Source: https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html · type: docs · date: v3.20+

### ch16_s03 — GenAI for Feature Proposals; the Meaningless-Feature Risk

- **CAAFE (Hollmann et al., 2024) — Context-Aware Automated Feature Engineering**  [REFRESH]  (confidence: verified)
  - Summary: The seminal paper that introduced LLM-based automated FE for tabular data. CAAFE feeds dataset metadata (column names, types, brief descriptions) to an LLM, which generates Python feature-transformation code. The LLM never sees raw data values — it operates purely on schema semantics. Generated features are then validated through iterative cross-validation against a baseline, with only empirically-beneficial features retained. Published at NeurIPS 2023; code at github.com/automl/CAAFE. Multiple follow-up papers (see below) have extended or benchmarked against CAAFE.
  - Why relevant: The draft mentions CAAFE by name but at a surface level. This provides the paper's full methodology (metadata-only, code generation, empirical validation loop), the published venue, and the open-source implementation. Establishes CAAFE as the academic-primary reference the brief asks for.
  - Source: Hollmann et al., "Context-Aware Automated Feature Engineering" (NeurIPS 2023) · github.com/automl/CAAFE · type: paper + code · date: 2024

- **LLM-FE (Abhyankar, Shojaee & Reddy, 2025) — LLMs as Evolutionary Optimizers**  [NEW]  (confidence: verified)
  - Summary: Frames automated FE as a **program search** problem. LLMs iteratively propose feature transformation programs; data-driven feedback (validation performance) guides the evolutionary search. Unlike CAAFE's simpler iteration loop, LLM-FE uses LLMs both to generate and to reason about prior experiments, maintaining an accumulated history of what worked. Accepted at TMLR. Code: github.com/nikhilsab/LLMFE. Outperforms CAAFE and other baselines on diverse classification/regression benchmarks.
  - Why relevant: The draft's CAAFE pipeline is "propose → cross-validate → keep/reject." LLM-FE adds a fundamentally different search paradigm: evolutionary optimization where the LLM learns from prior rounds. This provides a concrete example of how the field has advanced beyond simple CAAFE-style validation.
  - Source: https://arxiv.org/abs/2503.14434 · type: paper (TMLR accepted) · date: Mar 2025 (revised May 2026)

- **Human-LLM Collaborative Feature Engineering (Li et al., 2026) — ICLR 2026**  [NEW]  (confidence: verified)
  - Summary: Decouples feature proposal (LLM) from feature selection (explicit utility/uncertainty model). Introduces a mechanism for selective human preference elicitation — in early rounds, when utility estimation is unreliable, humans compare pairs of proposed operations to guide the search. The framework reduces cognitive load and outperforms both fully-automated (CAAFE, OCTree) and naive LLM selection. Uses GPT-4o. Published at ICLR 2026.
  - Why relevant: Directly bridges s03 (GenAI risk) and s04 (HITL). Shows that even with LLM-proposed features, the selection step benefits from structured human input — not just "review the top 10." The decoupling of proposal from selection is a design pattern the book can teach.
  - Source: https://arxiv.org/abs/2601.21060 · type: paper (ICLR 2026) · date: Jan 2026

- **PromptFE (Zou, Utke, Klabjan & Liu, 2026) — EACL 2026**  [NEW]  (confidence: verified)
  - Summary: An LLM-based AutoFE algorithm that uses semantic dataset information for automated feature engineering. Key innovation: provides top-performing features from prior rounds as in-context examples in the prompt, enabling the LLM to recognize patterns of promising feature transformations. More compact prompt format than CAAFE, reducing LLM token cost. Published at EACL 2026.
  - Why relevant: Shows maturation of the LLM-FE paradigm — efficiency improvements (shorter prompts) and learning from prior successes via in-context examples. Addresses a practical limitation of CAAFE (high API cost from verbose prompts).
  - Source: https://aclanthology.org/2026.eacl-long.28.pdf · type: paper (EACL 2026) · date: 2026

- **FeRG-LLM (Ko et al., 2025) — Feature Engineering by Reason Generation**  [NEW]  (confidence: verified)
  - Summary: Trains a specialized LLM (fine-tuned on feature engineering dialogues) that generates features along with explicit reasoning chains explaining *why* each proposed feature is expected to help. Uses Direct Preference Optimization (DPO) alignment. The reasoning makes the proposals auditable — addressing the "black-box LLM proposer" concern. Published at NAACL 2025 Findings.
  - Why relevant: Addresses a critical gap in the draft: the draft treats LLM proposals as opaque; FeRG-LLM shows that reasoning traces can make proposals auditable. Directly enriches the "plausible-but-spurious" discussion by showing *how* to detect implausibility through generated rationale.
  - Source: https://aclanthology.org/2025.findings-naacl.237.pdf · type: paper (NAACL 2025 Findings) · date: 2025

- **Fine-tuning LLMs for Automated Feature Engineering (Hirose, Uchida & Shirakawa, 2024)**  [NEW]  (confidence: verified)
  - Summary: Demonstrates that fine-tuning LLMs specifically for feature engineering tasks reduces instability in code generation compared to CAAFE's zero-shot approach. Fine-tuned models produce more syntactically valid, executable code and require fewer regeneration attempts. Presented at AutoML Conference 2024.
  - Why relevant: Shows that the base CAAFE approach has a practical limitation — LLMs sometimes generate un-executable code. Fine-tuning mitigates this. Useful as a brief "how the field evolved" note.
  - Source: https://openreview.net/forum?id=FqbkgaMf8O · type: paper (AutoML Conf 2024) · date: 2025

- **LLM2Features (Tsymbalov & Savchenko, 2024)**  [NEW]  (confidence: verified)
  - Summary: Studies LLM-based automated feature generation with focus on interpretability. Compares against CAAFE and shows that LLMs can generate features with human-readable formulas, while CAAFE's code-based approach can produce opaque transformations. Demonstrates on AutoML with tabular data benchmarks.
  - Why relevant: Add the interpretability dimension to the LLM-FE discussion — important for the book's emphasis on *dirancang manusia* and HITL workflows (ch16_s04). If humans must review features, interpretable format matters.
  - Source: https://openreview.net/forum?id=qbSoiHLEK0 · type: paper · date: 2024

- **AFE-Master (Liang et al., 2026) — Domain-Specific Language Parsing + Guided Local Search**  [NEW]  (confidence: verified)
  - Summary: A post-2025 advance that uses Domain-Specific Language (DSL) parsing to structurally constrain LLM feature proposals and guided local search to efficiently navigate the feature space. Overcomes limitations of purely free-text LLM proposals that can wander into nonsensical transformations. Presented at WWW 2026.
  - Why relevant: Represents the latest maturation where LLM-FE systems add structural constraints (DSLs) to prevent the spurious-feature problem. A good "road ahead" note for the chapter.
  - Source: https://dl.acm.org/doi/10.1145/3774904.3792816 · type: paper (WWW 2026) · date: 2026

### ch16_s04 — Human-in-the-Loop: Validating and Curating Machine-Proposed Features

- **Human-LLM Collaborative FE (Li et al., 2026) — Structured HITL Selection**  [NEW]  (confidence: verified)
  - Summary: (See full entry under s03.) The framework's HITL mechanism — selective preference elicitation guided by uncertainty quantification — is a concrete, evaluated alternative to the draft's conceptual "review top-10 features" workflow. Demonstrated across both synthetic studies and real user studies, with measured reduction in cognitive load.
  - Why relevant: The draft describes HITL conceptually; this paper provides an empirically validated, published-at-ICLR HITL framework with both algorithmic design and human-subject results. Exactly the kind of evidence that turns a design opinion into a teachable principle.
  - Source: https://arxiv.org/abs/2601.21060 · type: paper (ICLR 2026) · date: Jan 2026

- **AutoGluon's Modular Feature Generator Pipeline as HITL Enabler**  [NEW]  (confidence: verified)
  - Summary: AutoGluon's `PipelineFeatureGenerator` and individual generators (`DatetimeFeatureGenerator`, `CategoryFeatureGenerator`, `TextNgramFeatureGenerator`, etc.) are individually composable and configurable. Users can insert, remove, or customize generators. The `feature_metadata_in` parameter allows users to manually specify feature types, overriding automatic inference. This architecture naturally supports HITL — the human defines the generator composition; the machine executes.
  - Why relevant: Demonstrates that industrial AutoML systems already implement the HITL philosophy architecturally. The pipeline is automated but configurable — the human sets guardrails (generator selection, feature type overrides) and the machine fills in the details. A concrete pattern the book can reference.
  - Source: https://auto.gluon.ai/stable/tutorials/tabular/tabular-feature-engineering.html · type: docs · date: v1.5.0 (2025)

- **FeRG-LLM Reason Traces as Audit Trail**  [REFRESH]  (confidence: verified)
  - Summary: (See full entry under s03.) The explicit reasoning chains generated alongside each feature proposal create an audit trail that makes HITL review more efficient — a human can read the LLM's rationale and judge whether the reasoning is domain-appropriate without needing to reverse-engineer the transformation logic.
  - Why relevant: Provides a concrete mechanism for *how* humans validate LLM proposals efficiently. The draft's HITL workflow is correct in principle but vague on method; FeRG-LLM shows one validated approach.

- **LLM-Augmented Feature Engineering for ML Pipelines (Rancea, Anghel & Cioara, 2026)**  [NEW]  (confidence: verified)
  - Summary: An integrated LLM-based automated FE pipeline that addresses the full workflow from raw schema to validated features. Positions the LLM as a feature proposer within a larger AutoML pipeline, with explicit filtering and validation stages. Published at IEEE Conference 2026.
  - Why relevant: Shows the integration of LLM-FE into full AutoML — the convergence of s02 (AutoML pipelines) and s03 (GenAI proposals). Useful as a "state of convergence" example.
  - Source: IEEE Xplore https://ieeexplore.ieee.org/abstract/document/11536587/ · type: paper (IEEE conf) · date: 2026

### ch16_s05 — Case Study: Automated + Human-Curated Features on a Relational Dataset

- **FeatureTools `load_mock_customer()` — Canonical Demo Dataset**  [NEW]  (confidence: verified)
  - Summary: FeatureTools ships with a built-in mock customer dataset (customers→sessions→transactions) that is the standard demo for DFS. The dataset includes timestamped transactions, session attributes, and customer demographics — structurally identical to the draft's retail churn scenario. Running DFS on 5 customers produces 75 features; on sessions, 44 features. The library also provides `graph_feature()` for lineage visualization and `describe_feature()` for natural-language feature descriptions.
  - Why relevant: If the book includes a companion notebook for this case study, this is the canonical dataset to use. Also provides the real DFS output scale (75 features from 5 entities) that readers would see, making the draft's "800 features from retail data" claim verifiable.
  - Source: https://featuretools.alteryx.com/en/stable/ · type: docs/demo · date: v1.31.0 (May 2024)

- **FeatureTools Feature Selection Guide — Post-DFS Pruning**  [NEW]  (confidence: verified)
  - Summary: FeatureTools includes a dedicated feature selection guide covering `ft.selection.remove_highly_correlated_features()`, `ft.selection.remove_highly_null_features()`, `ft.selection.remove_single_value_features()`, and integration with `feature_importances_` from sklearn models. This is the exact statistical filtering step (variance-zero, high-correlation) that the draft case study describes.
  - Why relevant: If the book shows a companion notebook, these are the exact function calls that implement the "750 removed by statistical filters" step. Makes the case study reproducible.
  - Source: https://featuretools.alteryx.com/en/stable/guides/feature_selection.html · type: docs · date: v1.31.0 (May 2024)

- **FeatureTools Cutoff-Time Mechanism for Temporal Leakage Prevention**  [REFRESH]  (confidence: verified)
  - Summary: FeatureTools' cutoff-time system allows DFS to compute features using only data available *before* a specified timestamp for each entity. This prevents the exact temporal leakage that the draft's case study discovers ("waktu sejak login terakhir" being updated post-churn). The `Handling Time` guide provides detailed examples with and without cutoff times, showing how feature values differ when temporal constraints are enforced.
  - Why relevant: The draft's case study finds temporal leakage through human review. This source shows that the leakage *can be prevented programmatically* via cutoff-time configuration — making it a teachable lesson about designing the automation correctly rather than relying entirely on post-hoc human detection.
  - Source: https://featuretools.alteryx.com/en/stable/getting_started/handling_time.html · type: docs · date: v1.31.0 (May 2024)

---

## Cross-cutting / chapter-level new developments

- **Tabular Foundation Models (TFMs): TabPFNv2, TabICL, Mitra, TabDPT, TabM**  [NEW]  (confidence: verified)
  - Summary: A new class of models pretrained on synthetic tabular data at scale (TabArena benchmark). These models learn feature representations during pretraining and apply zero-shot or few-shot to new tabular datasets, effectively internalizing what used to be manual feature engineering. TabPFNv2 (Hollmann et al., 2025), TabICL (in-context learning for tables), and Mitra/TabDPT (transformer-based) represent the frontier where FE is absorbed into model architecture.
  - Why relevant: These models challenge the very premise that automated FE (DFS, AutoML pipelines, LLM-FE) is the ceiling — if TFMs can outperform engineered features on many benchmarks, the book must address this as the emerging alternative to all of Ch 16's content. Positions Ch 16 within a rapidly moving landscape. Relates to Ch 15 (deep learning on tabular data) and the book's *dirancang manusia → dipelajari mesin* spectrum.
  - Source: TabArena benchmark https://tabarena.ai · type: benchmark · date: 2025

- **LLM-FE Landscape Maturation (2024–2026): From Simple Propose+Validate to Structured Search**  [NEW]  (confidence: verified)
  - Summary: The sub-field of LLM-based automated FE has progressed rapidly: CAAFE (2024, zero-shot propose+validate) → fine-tuned LLMs (2024, reduced instability) → FeRG-LLM (2025, reasoning traces) → LLM-FE (2025, evolutionary search with feedback) → PromptFE (2026, in-context learning from prior successes) → AFE-Master (2026, DSL-constrained search) → Human-LLM Collaborative (ICLR 2026, structured HITL). This trajectory maps onto increasing sophistication of search, decreasing token cost, and tighter integration with human judgment.
  - Why relevant: The chapter can frame CAAFE not as "the" solution but as the opening move in an active research arc. This narrative makes the chapter future-proof and positions readers to evaluate new LLM-FE systems against a taxonomy of design patterns.

- **The Leakage-Awareness of FeatureTools Primitives**  [NEW]  (confidence: verified)
  - Summary: FeatureTools maintainers have actively removed primitives that caused data leakage: `Correlation` and `AutoCorrelation` removed in v1.25 (Apr 2023), `Rolling*` gap default changed from 0→1 in v1.15 (Oct 2022) to prevent lookahead. These are real-world examples of *automated* FE systems that encode pipeline-discipline awareness.
  - Why relevant: Ties Ch 16 back to the book's recurring “*praktik pipeline yang benar*" callout (from Ch 2). Shows that even fully automated systems can and should implement leakage safeguards — the human still sets the parameters, but the system provides safe defaults.
  - Source: https://featuretools.alteryx.com/en/stable/release_notes.html · type: docs · date: v1.31.0

- **Neurosymbolic FE & Symbolic Regression for Feature Construction**  [NEW]  (confidence: uncertain)
  - Summary: The Google Scholar search returned limited results for "neurosymbolic feature engineering" as a named subfield. However, symbolic regression systems (e.g., PySR, gplearn) can be viewed as a lightweight neurosymbolic approach — using genetic programming (symbolic) guided by model performance (neural proxy). The LLM-FE approaches with DSL constraints (AFE-Master) also represent a form of neurosymbolic: LLM (neural) + structural grammar (symbolic).
  - Why relevant: If the book wants to include a brief "beyond current tools" section, the convergence of LLM-FE toward structured search (DSLs, grammars) points toward a neurosymbolic interpretation. The evidence is pattern-based rather than paper-backed for the label.
  - Source: Inference from multiple papers reviewed · type: research direction · date: 2024–2026

---

## Candidate new terms (for Living Glossary / Appendix D)

| Term | Definition | Section |
|---|---|---|
| Deep Feature Synthesis (DFS) | Algorithm that automatically generates features from relational datasets by recursively applying mathematical primitives along table relationships | ch16_s01 |
| Feature primitives | Basic building-block operations (SUM, MEAN, MODE, WEEKDAY, etc.) used to construct complex features | ch16_s01 |
| Feature space explosion | Combinatorial explosion of generated features when automation stacks operations deeply, creating massive dimensionality | ch16_s01 |
| EntitySet | FeatureTools' abstraction for describing a relational schema: DataFrames + index columns + temporal indices + inter-table relationships | ch16_s01 |
| Cutoff time | The timestamp before which all training data must be observed; prevents temporal leakage in automated FE | ch16_s01 |
| AutoML | Automated Machine Learning; systems that automate preprocessing, feature engineering, model selection, and hyperparameter tuning | ch16_s02 |
| Pipeline search space | The combinatorial set of all possible sequences of data transformations, FE steps, and model algorithms evaluated by an AutoML system | ch16_s02 |
| CAAFE | Context-Aware Automated Feature Engineering; LLM-based approach that uses column metadata/descriptions to generate domain-informed feature transformations | ch16_s03 |
| Plausible-but-spurious feature | A generated feature that makes semantic sense in human language but provides no actual predictive value or introduces noise | ch16_s03 |
| Human-in-the-loop (HITL) | System architecture where automated processes pause at designated points to require human validation, judgment, or steering | ch16_s04 |
| Tabular Foundation Model (TFM) | Neural network pretrained on synthetic tabular data to learn generalizable feature representations, applicable to new tables zero-shot | ch16_s02 |
| Feature lineage graph | Visual representation tracing the primitive operations and intermediate features that produced a final generated feature | ch16_s01 |
| Evolutionary FE search | Program-search approach where LLMs iteratively propose feature transformations, with data-driven feedback guiding subsequent rounds (as in LLM-FE) | ch16_s03 |
| Feature selection wrapper (in AutoFE context) | Post-generation pruning step using statistical heuristics: zero-variance, high-correlation, null-above-threshold removal | ch16_s05 |

---

## Source list

- [1] FeatureTools Documentation v1.31.0 — https://featuretools.alteryx.com/en/stable/ (docs, May 2024)
- [2] FeatureTools Release Notes — https://featuretools.alteryx.com/en/stable/release_notes.html (docs/changelog, v1.31.0 May 2024)
- [3] FeatureTools Tuning DFS Guide — https://featuretools.alteryx.com/en/stable/guides/tuning_dfs.html (docs, v1.31.0)
- [4] FeatureTools Performance Guide — https://featuretools.alteryx.com/en/stable/guides/performance.html (docs, v1.31.0)
- [5] FeatureTools Feature Selection Guide — https://featuretools.alteryx.com/en/stable/guides/feature_selection.html (docs, v1.31.0)
- [6] FeatureTools Handling Time (Cutoff) Guide — https://featuretools.alteryx.com/en/stable/getting_started/handling_time.html (docs, v1.31.0)
- [7] AutoGluon Tabular Feature Engineering — https://auto.gluon.ai/stable/tutorials/tabular/tabular-feature-engineering.html (docs, v1.5.0, Dec 2025)
- [8] AutoGluon Tabular Essentials (TFMs) — https://auto.gluon.ai/stable/tutorials/tabular/tabular-essentials.html (docs, v1.5.0, Dec 2025)
- [9] TabArena Benchmark — https://tabarena.ai (benchmark, 2025)
- [10] H2O AutoML Documentation — https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html (docs, v3.20+)
- [11] Hollmann et al., "Context-Aware Automated Feature Engineering" (CAAFE), NeurIPS 2023 — github.com/automl/CAAFE (paper + code, 2024)
- [12] Abhyankar, Shojaee & Reddy, "LLM-FE: Automated Feature Engineering for Tabular Data with LLMs as Evolutionary Optimizers" — https://arxiv.org/abs/2503.14434 (paper, TMLR accepted, Mar 2025 / rev. May 2026)
- [13] Li et al., "Human-LLM Collaborative Feature Engineering for Tabular Data" — https://arxiv.org/abs/2601.21060 (paper, ICLR 2026, Jan 2026)
- [14] Zou, Utke, Klabjan & Liu, "PromptFE: Automated Feature Engineering by Prompting" — https://aclanthology.org/2026.eacl-long.28.pdf (paper, EACL 2026)
- [15] Ko et al., "FeRG-LLM: Feature Engineering by Reason Generation Large Language Models" — https://aclanthology.org/2025.findings-naacl.237.pdf (paper, NAACL 2025 Findings)
- [16] Hirose, Uchida & Shirakawa, "Fine-tuning LLMs for Automated Feature Engineering" — https://openreview.net/forum?id=FqbkgaMf8O (paper, AutoML Conf 2024)
- [17] Tsymbalov & Savchenko, "LLM2Features: Large Language Models in Interpretable Feature Generation for AutoML with Tabular Data" — https://openreview.net/forum?id=qbSoiHLEK0 (paper, 2024)
- [18] Liang et al., "AFE-Master: Enhancing LLM-Driven Autonomous Feature Engineering with Domain-Specific Language Parsing and Guided Local Search" — https://dl.acm.org/doi/10.1145/3774904.3792816 (paper, WWW 2026)
- [19] Rancea, Anghel & Cioara, "LLM-Augmented Feature Engineering for Machine Learning Pipelines" — IEEE (paper, 2026)
