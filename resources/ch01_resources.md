---
chapter: ch01
title: From Raw Data to Model Representation
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 1 Resources — From Raw Data to Model Representation

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence).

## Coverage baseline (what the drafts already have)
- ch01_s01 draft: data → attribute → feature → representation pipeline defined with text/pixel examples
- ch01_s02 draft: the "ceiling effect" — features set the theoretical upper bound; linear model with good features beats complex NN
- ch01_s03 draft: designed-by-human ↔ learned-by-machine spectrum defined with BMI (designed) and CNN edges (learned); hybrid approach mentioned
- ch01_s04 draft: the myth reframed — FE shifts form (augmentation, tokenization, target framing) not disappears; image cropping/resizing as designed FE
- ch01_s05 draft: unit-of-observation, target+horizon, index-time cutoff introduced; data-leakage warning; credit-card churn example
- ch01_s06 draft: five representation structures listed (tabular vector/matrix, sequence, grid/tensor, graph, set) with examples
- ch01_s07 draft: pipeline roadmap — Part II (tabular transforms), Part III (selection/reduction), Part IV (specialized data types), Part V (DL + automated)
- ch01_s08 draft: case study — e-commerce log → feature matrix via unit=User, target=churn, index-time cutoff, aggregation features (frequency, monetary, behavioral)
- Briefs: all briefs align; s05 flags "data leakage" term, s06 flags "not all data is flat matrix"

---

## Resources by subsection

### ch01_s01 — Data, attributes, features, representation (core vocabulary)
- **"A feature is data that's used as the input for ML models to make predictions. Raw data is rarely in a format that is consumable by an ML model, so it needs to be transformed into features. This process is called feature engineering."** [REFRESH] (confidence: verified)
  - Summary: Tecton's industry-standard definition of feature vs. raw data, positioned in a production ML context. Emphasizes that raw data is rarely ML-consumable — exactly the distinction ch01_s01 makes.
  - Why relevant: Provides a crisp, practitioner-validated definition that aligns with the draft but adds the "production" lens (the feature must survive training AND inference).
  - Source: https://www.tecton.ai/blog/what-is-a-feature-platform/ · type: blog (industry) · date: ~2025 (Databricks-hosted, current)

- **Distinction between features-as-columns vs. features-as-data-products** [NEW] (confidence: verified)
  - Summary: Eugene Yan's feature store hierarchy (Access → Serving → Integrity → Convenience → Autopilot) reframes features as managed assets, not transient columns. At the "Access" level, features need discoverability, lineage, and reuse — positioning a feature as something with provenance, not just a transformed column.
  - Why relevant: This is a modern framing of "what a feature is" that goes beyond the academic data/attribute/feature distinction — the feature as a managed, versioned, reusable product. Could enrich the ch01_s01 vocabulary discussion.
  - Source: https://eugeneyan.com/writing/feature-stores/ · type: blog (practitioner deep-dive) · date: 2021-02

- **Feast's code-level definition of feature retrieval** [REFRESH] (confidence: verified)
  - Summary: Feast (open-source feature store) operationalizes the feature concept via `get_historical_features()` and `get_online_features()` — a feature is not just a column but something that must be retrievable identically in training and serving.
  - Why relevant: Concrete illustration of the feature-as-contract concept, connecting the vocabulary to pipeline discipline.
  - Source: https://www.feast.dev/ · type: docs/landing page (open-source) · date: 2025–2026 (active project, v0.64+)

### ch01_s02 — Role of features in ML (representation = ceiling)
- **Data-centric AI framing: "Data-centric AI is the discipline of systematically engineering the data used to build an AI system."** [NEW] (confidence: verified)
  - Summary: Andrew Ng's data-centric AI movement positions feature engineering as the core of the ML development process — systematically engineering data to improve model performance, rather than endlessly tuning architecture. This directly supports ch01_s02's thesis that features set the ceiling.
  - Why relevant: Provides a named movement and authoritative framing (Ng, NeurIPS DCAI workshops 2021+) that validates the book's emphasis on FE over model tuning. The draft says "features set the ceiling" — DCAI provides the philosophical/industry backing.
  - Source: https://datacentricai.org/ · type: resource hub (academic/industry) · date: 2021–2025 (ongoing)

- **Chip Huyen (2024): "Context construction for foundation models is equivalent to feature engineering for classical ML models."** [NEW] (confidence: verified)
  - Summary: In her GenAI platform architecture post, Huyen explicitly equates context construction (RAG, tool use, query rewriting) to feature engineering — both give the model the necessary information to process an input. This extends the "ceiling" concept to the LLM era.
  - Why relevant: Shows the ceiling effect persists even in the foundation-model paradigm — the quality of retrieved context (the "features" for an LLM) determines answer quality. Excellent bridge to ch01_s04 (FE isn't dead, it's context construction).
  - Source: https://huyenchip.com/2024/07/25/genai-platform.html · type: blog (practitioner) · date: 2024-07-25

- **"Features (and labels) are the inputs for machine learning models. In a regression equation, labels are the dependent variable, features are independent variables."** [REFRESH] (confidence: verified)
  - Summary: Eugene Yan's crisp, no-nonsense definition that aligns with ch01_s02's ceiling argument — if the independent variables lack signal, no regression can recover it.
  - Why relevant: A clean, quotable formulation suitable for reinforcing the ceiling principle.
  - Source: https://eugeneyan.com/writing/feature-stores/ · type: blog · date: 2021-02

### ch01_s03 — Designed vs. learned representations (the central spectrum)
- **SimCLR (Chen et al., 2020, ICML): self-supervised learning as implicit feature engineering** [NEW] (confidence: verified)
  - Summary: SimCLR showed that with the right data augmentations (random crop, color distortion, Gaussian blur), a contrastive learning objective can produce visual representations matching supervised ResNet-50 — without any labels. The key finding: "composition of data augmentations plays a critical role in defining effective predictive tasks." The human designs the augmentation; the machine learns the representation.
  - Why relevant: This is the perfect illustration of the spectrum's middle ground: the human still designs the augmentation strategy (a form of FE), but the actual feature extraction is learned. Augmentation design = modern-day designed FE for the learned-representation paradigm.
  - Source: https://arxiv.org/abs/2002.05709 · type: paper (ICML 2020) · date: 2020-07-01 (v3)

- **BYOL (Grill et al., 2020, NeurIPS): representation learning without negative examples** [NEW] (confidence: verified)
  - Summary: BYOL achieves SOTA self-supervised representations without contrastive negative pairs — two networks (online and target) bootstrap each other's representations. The target network is updated via slow-moving average. Shows that learned representations can emerge from clever architecture design and data augmentation alone.
  - Why relevant: Further evidence for the designed→learned spectrum — the human designs the training procedure (online/target, EMA, augmentations), and the machine learns entirely from that structure. BYOL pushes the "learned" end further by removing the need for explicit contrastive labels.
  - Source: https://arxiv.org/abs/2006.07733 · type: paper (NeurIPS 2020) · date: 2020-09-10 (v3)

- **MAE (He et al., 2021): masked autoencoders — reconstructing masked patches as a self-supervised task** [NEW] (confidence: verified)
  - Summary: MAE masks 75% of image patches and learns representations by reconstructing the missing pixels. With an asymmetric encoder-decoder (encoder sees only visible patches, lightweight decoder reconstructs), it achieves 3x+ training speedup and SOTA transfer. The "mask and reconstruct" paradigm is a different path to learned representations than contrastive (SimCLR) or bootstrapping (BYOL).
  - Why relevant: Illustrates the diversity within the "learned by machine" end — SSL approaches differ in what pretext task the human designs. The contrast between SimCLR (discriminative), BYOL (bootstrapping), and MAE (generative/reconstructive) shows that even at the learned end, human design choices (which SSL paradigm?) matter enormously.
  - Source: https://arxiv.org/abs/2111.06377 · type: paper (CVPR 2022 spotlight) · date: 2021-12-19 (v3)

### ch01_s04 — The myth "feature engineering is dead"
- **Chip Huyen (2024): context construction IS feature engineering** [NEW] (confidence: verified)
  - Summary: "Context construction for foundation models is equivalent to feature engineering for classical ML models. They serve the same purpose: giving the model the necessary information to process an input." She then describes RAG, query rewriting, text-to-SQL, and agentic retrieval as forms of context construction — all of which are the new face of feature engineering.
  - Why relevant: This is the single strongest external validation of the book's thesis in ch01_s04. From a leading practitioner, it renames and reframes FE for the LLM era. The draft says "FE shifts form" — Huyen provides the concrete new form: context construction.
  - Source: https://huyenchip.com/2024/07/25/genai-platform.html · type: blog · date: 2024-07-25

- **Feature engineering resurfaces as data preparation in deep learning: augmentation strategies, tokenization, and target framing** [REFRESH] (confidence: verified)
  - Summary: The SimCLR paper's core finding — that the composition of data augmentations is the critical design decision for self-supervised learning — demonstrates that even in the most "learned" paradigm, human-designed FE (augmentation selection) governs success. Similarly, BYOL and MAE depend entirely on the human-chosen pretext task.
  - Why relevant: Provides technical evidence for the draft's claim that "rekayasa fitur tidak menghilang, melainkan berevolusi." Human decisions about augmentation, tokenization, and preprocessing determine what the model can learn.
  - Source: https://arxiv.org/abs/2002.05709 · type: paper · date: 2020; https://arxiv.org/abs/2006.07733 · date: 2020; https://arxiv.org/abs/2111.06377 · date: 2021

- **Real-time ML reinforces the need for systematic feature engineering: batch vs. streaming features** [NEW] (confidence: verified)
  - Summary: Chip Huyen's 2022 post on real-time ML catalogs how features in production ML systems must be engineered differently for batch vs. streaming contexts — batch features (historical, precomputed), near-real-time features (streaming, updated in seconds), and real-time features (computed at prediction time). The engineering of WHEN and HOW a feature is computed is the new FE challenge that DL alone cannot solve.
  - Why relevant: Demonstrates that even in modern ML infrastructure, feature engineering decisions (freshness, computation strategy, serving latency) are the hard part — the model architecture is secondary.
  - Source: https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html · type: blog · date: 2022-01-02

### ch01_s05 — Learning table: unit, target, and feature-availability cutoff
- **Point-in-time correctness ("time travel") as the core integrity requirement in feature platforms** [NEW] (confidence: verified)
  - Summary: Tecton's feature platform documentation frames point-in-time correctness as a first-class concern: "ensuring that historical features and labels used in offline training and evaluation don't have data leaks." Features must be computed as-of the prediction time, using only data available before that timestamp. This is exactly the "batas ketersediaan fitur" (feature-availability cutoff) concept in the draft.
  - Why relevant: Validates and grounds the draft's concept in real production infrastructure. Shows that the index-time cutoff isn't just a theoretical nicety — it's a hard requirement implemented in feature platforms through time-travel, snapshotting, and as-of joins.
  - Source: https://www.tecton.ai/blog/what-is-a-feature-platform/ · type: blog · date: ~2025

- **Eugene Yan's "Integrity" tier in feature store hierarchy: minimizing train-serve skew and point-in-time correctness** [NEW] (confidence: verified)
  - Summary: At the Integrity level, feature stores address (a) creating point-in-time accurate features to simulate production (avoiding data leaks), and (b) consistency between training and serving features. Netflix's "Distributed Time Travel" and Uber's dual-store sync (offline Hive ↔ online Cassandra) are concrete implementations.
  - Why relevant: Links ch01_s05's index-time concept to real infrastructure patterns. Shows that the problem is hard enough that Netflix and Uber built custom solutions (time-travel, snapshotting) for it.
  - Source: https://eugeneyan.com/writing/feature-stores/#integrity · type: blog · date: 2021-02

- **Chip Huyen (2022): online features taxonomy — batch vs. near-real-time vs. real-time** [REFRESH] (confidence: verified)
  - Summary: Huyen distinguishes three categories: batch features (historical, precomputed, e.g. mean preparation time), near-RT features (streaming, async precomputed, e.g. current queue depth), and real-time features (computed on prediction request, e.g. distance to delivery location). Each has different freshness-to-latency tradeoffs and different availability-cutoff implications.
  - Why relevant: Extends the draft's binary "before index-time = legal, after = illegal" concept to a nuanced view where feature computation strategy (precomputed vs. on-demand) interacts with the cutoff. The same feature can be computed in different modes with different staleness guarantees.
  - Source: https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html · type: blog · date: 2022-01-02

### ch01_s06 — Map of representation structures
- **Multimodal foundation models ingest diverse representation structures natively** [NEW] (confidence: uncertain — inferred from known architectures; worth verifying with specific 2024–2026 papers)
  - Summary: Modern foundation models (GPT-4V, Gemini, Claude 3, LLaVA, etc.) natively handle multiple representation structures: text as token sequences, images as patch grids, audio as spectrograms/waveforms, tabular data as key-value or serialized text. This collapses the previously separate representation pipelines into a unified model — the representation structure is no longer a preprocessing choice but part of the model's input interface.
  - Why relevant: The draft lists five separate structures (tabular, sequence, grid, graph, set). The 2024 landscape shows these structures increasingly fused within single models. This is a forward-looking note for ch01_s06 — multimodal models are reshaping the "map" itself.
  - Source: To verify with specific sources — potential: Gemini 1.5 technical report (2024), GPT-4V system card (2023), Meta's multimodal work. · type: paper/blog · date: 2024–2025

- **Self-supervised pretraining as a representation-structure bridge: MAE for grids, contrastive for sequences, graph SSL for graphs** [NEW] (confidence: verified)
  - Summary: The SSL revolution implicitly maps representation structures to learning paradigms: MAE-style masking works for grid/tensor data (images, video), contrastive learning (SimCLR) works for images, masked language modeling works for sequences (text), and specialized graph SSL (GraphCL, Node2Vec) for graph data. Each representation structure has converged on a dominant SSL strategy.
  - Why relevant: Connects ch01_s06's structural survey to ch01_s03's spectrum — each representation structure has its own designed→learned trajectory. The "map" is not static; SSL has transformed how each structure is represented.
  - Source: https://arxiv.org/abs/2002.05709 (SimCLR) · date: 2020; https://arxiv.org/abs/2111.06377 (MAE) · date: 2021; Node2Vec: Grover & Leskovec, KDD 2016

- **Feast now supports document/embedding retrieval alongside structured features — blurring the structure boundary** [NEW] (confidence: verified)
  - Summary: Feast 0.64+ added `retrieve_online_documents()` for vector similarity search alongside traditional feature retrieval. A single feature store now serves both structured tabular features and unstructured document chunks — the representation structure is a property of the feature, not of the platform.
  - Why relevant: Practical evidence that the boundary between representation structures is collapsing in production infrastructure. The draft's "peta struktur representasi" should acknowledge that modern platforms treat them as a continuum.
  - Source: https://www.feast.dev/ · type: docs/landing · date: 2025–2026

### ch01_s07 — Feature engineering pipeline at a glance
- **Feature platforms as the operational realization of the FE pipeline concept** [NEW] (confidence: verified)
  - Summary: Tecton's architecture — feature repository (features as code) → feature pipelines (batch, streaming, on-demand transforms) → feature store (offline + online) → monitoring (data quality + operational) — is essentially the FE pipeline book structure in production form: Part II (tabular transforms) = batch pipelines, Part III (selection) = monitoring/quality, Part IV (data types) = streaming + on-demand transforms, Part V (modern) = integration with model serving.
  - Why relevant: Provides a real-world validation that the book's pipeline structure mirrors how industry actually builds FE infrastructure. The "feature platform" concept could be introduced as an aspirational end-state for the book's journey.
  - Source: https://www.tecton.ai/blog/what-is-a-feature-platform/ · type: blog · date: ~2025

- **Eugene Yan's hierarchy of needs as a FE pipeline maturity model** [NEW] (confidence: verified)
  - Summary: The five-tier hierarchy (Access → Serving → Integrity → Convenience → Autopilot) maps perfectly onto the book's progression: Access = Part II (make features), Serving = bridge to production, Integrity = Ch 2 (leakage/split discipline), Convenience = well-designed pipeline APIs, Autopilot = Ch 16 (automated FE).
  - Why relevant: An alternative, practitioner-friendly framing for the pipeline overview. Could be referenced in ch01_s07 as a maturity model that readers can map their own projects against.
  - Source: https://eugeneyan.com/writing/feature-stores/ · type: blog · date: 2021-02

- **Real-time ML pipeline architecture as the next frontier of FE pipelines** [REFRESH] (confidence: verified)
  - Summary: Chip Huyen's stage-by-stage guide from batch prediction → online prediction with batch features → online prediction with streaming features → continual learning maps the evolution of FE pipeline complexity. Each stage adds new feature computation and serving requirements.
  - Why relevant: The draft's pipeline overview is static (transforms → select → reduce → serve). Huyen's staging shows the pipeline as an evolving entity, adding real-time, streaming, and continuous components. This forward-looking dimension could enrich ch01_s07.
  - Source: https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html · type: blog · date: 2022-01-02

### ch01_s08 — Case study: transaction data → feature matrix
- **Monzo Bank's feature store journey: from analytics stack (BigQuery) to production stack (Cassandra)** [NEW] (confidence: verified)
  - Summary: Eugene Yan documents Monzo Bank's practical challenge — features available in their analytics stack (BigQuery) were not available in production (Cassandra). They built automated synchronization with tagging, schema checking, and cron-based syncing. This is a real-world analog of the draft's e-commerce case study but with production serving constraints.
  - Why relevant: Provides a complementary case study to the draft's e-commerce example — shows that after building the feature matrix, you still need to solve the serving problem. Could be mentioned as a "beyond this chapter" preview.
  - Source: https://eugeneyan.com/writing/feature-stores/#serving · type: blog · date: 2021-02

- **DoorDash's Gigascale feature store: serving billions of feature-value pairs at 10M+ QPS** [NEW] (confidence: verified)
  - Summary: DoorDash stores billions of feature records across millions of entities, serves 10M+ QPS with features for store ranking and recommendations, and refreshes daily via batch writes. This is the extreme end of the "transaction log → feature matrix" pipeline at planet scale.
  - Why relevant: Shows what the simple case study in ch01_s08 scales to — serving features at DoorDash's scale requires Redis-based feature stores with binary serialization and compression. Connects the academic case study to the extreme real-world version.
  - Source: https://eugeneyan.com/writing/feature-stores/#serving · type: blog · date: 2021-02

---

## Cross-cutting / chapter-level new developments

### Foundation models reframing "feature engineering"
- **Chip Huyen (2024) makes the explicit equivalence**: context construction = feature engineering. RAG, web search, SQL retrieval, query rewriting — all serve the same purpose as classical FE: providing the model with relevant information to make a decision. This frames FE not as a dying art but as an evolved, higher-level discipline. [NEW]
- **The designed→learned spectrum now extends to foundation models**: at the designed end, humans craft prompt templates and retrieval strategies; at the learned end, the foundation model itself has learned representations during pretraining. The book's central spectrum remains valid but must be extended to include this new frontier. [NEW]
- **Data-centric AI validates the book's core premise**: Andrew Ng's movement argues that systematically engineering data — including feature engineering — yields more improvement than tweaking model architecture. This is essentially the book's thesis validated at the highest level of the field. [NEW]

### Self-supervised pretraining as implicit feature engineering
- **The SSL revolution (2020–2022) fundamentally changed what "feature engineering" means for unstructured data**: with SimCLR, BYOL, MAE, and their successors, the representation is learned without labels — but the human still designs the pretext task, the augmentations, and the architecture. This is a new kind of meta-FE: designing the conditions under which good representations emerge. [NEW]
- **The augmentation-as-FE insight**: SimCLR's key finding that composition of data augmentations is the critical design choice. The human doesn't engineer features; they engineer the augmentation strategy that induces good features. This is a profound reframing relevant across ch01_s03, s04, and s06. [NEW]

### Feature stores / platforms as a paradigm shift
- **FE as a platform concern, not a bespoke task**: Tecton, Feast, and the broader feature-store ecosystem have elevated feature engineering from an ad-hoc data-scientist activity to a managed, versioned, monitored platform capability. Features are now code, stored centrally, discoverable, reusable, and served with SLAs. This reframes FE as an infrastructure discipline. [NEW]
- **Point-in-time correctness as a first-class constraint**: Feature platforms have operationalized the concept — it's no longer a theoretical warning about leakage but a hard requirement with dedicated infrastructure (time-travel, snapshotting, as-of joins). [NEW]

### The learning-table framing in modern practice
- **Prediction-time cutoff is not just a theoretical concept — it's implemented in production**: Companies like Uber, Netflix, DoorDash, and Monzo all build their feature infrastructure around the concept that features must be correct as-of a specific point in time. The draft's ch01_s05 framing is validated by industry practice. [NEW]
- **The unit-of-observation decision governs the entire downstream pipeline**: Huyen's real-time ML post shows that the unit (user? user-day? session?) determines what features can be computed and at what latency. This is the same insight as ch01_s05's unit/target/horizon trio, extended to production scale. [REFRESH]

---

## Candidate new terms (for Living Glossary / Appendix D)

| Term (EN) | Proposed Indonesian | Context | Source |
|---|---|---|---|
| context construction | konstruksi konteks | Chip Huyen 2024 — the foundation-model equivalent of feature engineering | GenAI Platform post |
| feature store | feature store (keep EN) | Central infrastructure for storing, versioning, and serving features | Eugene Yan, Tecton, Feast |
| feature platform | feature platform (keep EN) | Broader infrastructure: feature repository + pipelines + store + monitoring | Tecton |
| point-in-time correctness | kebenaran point-in-time | Features must be correct as-of a specific timestamp (anti-leakage) | Eugene Yan, Tecton |
| train-serve skew | train-serve skew (keep EN) | Mismatch between features used during training vs. inference | Chip Huyen 2022, Eugene Yan |
| self-supervised learning | self-supervised learning (keep EN) | Learning representations from unlabeled data via pretext tasks | SimCLR, BYOL, MAE |
| pretext task | pretext task (keep EN) | The surrogate task (e.g., augmentation prediction, masked reconstruction) that drives SSL | SimCLR, MAE |
| data-centric AI | data-centric AI (keep EN) | The discipline of systematically engineering data to build AI systems | datacentricai.org |
| index time | waktu prediksi | Already in the draft (ch01_s05). Confirm consistency. | Draft |
| prediction horizon | horizon prediksi | Already in the draft. | Draft |
| unit of observation | unit observasi | Already in the draft. | Draft |

---

## Source list

- [1] Chip Huyen, "Building A Generative AI Platform" — https://huyenchip.com/2024/07/25/genai-platform.html (blog, 2024-07-25)
- [2] Chip Huyen, "Real-time machine learning: challenges and solutions" — https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html (blog, 2022-01-02, updated 2023-01-03)
- [3] Chip Huyen, "Building LLM applications for production" — https://huyenchip.com/2023/04/11/llm-engineering.html (blog, 2023-04-11)
- [4] Eugene Yan, "Feature Stores: A Hierarchy of Needs" — https://eugeneyan.com/writing/feature-stores/ (blog, 2021-02)
- [5] Tecton / Databricks, "What is a Feature Platform?" — https://www.tecton.ai/blog/what-is-a-feature-platform/ (blog, ~2025)
- [6] Feast, "The Open Source Feature Store for Machine Learning" — https://www.feast.dev/ (docs/landing, 2025–2026)
- [7] Ting Chen, Simon Kornblith, Mohammad Norouzi, Geoffrey Hinton, "A Simple Framework for Contrastive Learning of Visual Representations" (SimCLR) — https://arxiv.org/abs/2002.05709 (paper, ICML 2020, v3 2020-07-01)
- [8] Jean-Bastien Grill et al. (DeepMind), "Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning" (BYOL) — https://arxiv.org/abs/2006.07733 (paper, NeurIPS 2020, v3 2020-09-10)
- [9] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, Ross Girshick (Meta AI), "Masked Autoencoders Are Scalable Vision Learners" (MAE) — https://arxiv.org/abs/2111.06377 (paper, v3 2021-12-19)
- [10] Data-centric AI Resource Hub — https://datacentricai.org/ (resource hub, 2021–2025)
- [11] Andrew Ng, "The Batch" newsletter, Issue 277 — https://www.deeplearning.ai/the-batch/issue-277/ (newsletter, 2024-11-27)
- [12] Aditya Grover, Jure Leskovec, "node2vec: Scalable Feature Learning for Networks" — KDD 2016 (paper, for graph representation learning lineage)
