# Chapter → Subsection Breakdown

**Purpose:** the iteration unit for the pipeline. Each subsection = one Compilation + Writer unit. This is the list the orchestrator walks (§6) and the granularity the Compilation Agent works at (§4).

**Language:** English (working artifact for English-reasoning agents). Indonesian headings are produced downstream at writer/editorial stage, kept consistent via the Living Glossary. (Indonesian chapter subtitles below are provisional and need a native-speaker check.)

**Conventions:**
- ID = `chNN_sNN` (matches the `briefs/`, `drafts/` file scheme).
- Each subsection has a working title + one-line scope (what it must cover). This is *not* the brief — the brief is the compiler's structured output; this is the input that scopes it.
- **Recurring callouts** are invoked only where they genuinely apply (never separate units, and **not in every subsection**): (1) the *dirancang manusia → dipelajari mesin* spectrum — **rarely; default off.** Defined in Ch 1, resolved in the synthesis (Ch 17), carried by the book's structure in between; flagged in a brief only at a true turning point, never as per-subsection boilerplate; (2) pipeline discipline / leakage (book term: *praktik pipeline yang benar*) — home is Ch 2; elsewhere rarely, only at a real specific risk; (3) **interaction with the model family** — where the decision depends on it; (4) **modality-specific leakage** — once, in the relevant data-type chapter. A callout is a clause woven into prose, not a labeled box.
- 🔢 = notation-bearing chapter (compiler supplies LaTeX per §5).
- Per-subsection word budget = ~45k English ÷ **129 units ≈ ~350 English / ~405 Indonesian words** per subsection (average; case studies and dense concept units run longer, list-style units shorter).

---

## BAGIAN I — FONDASI

### Ch 1 — From Raw Data to Model Representation
*(Dari Data Mentah ke Representasi Model)*

| ID | Subsection | Scope |
|---|---|---|
| ch01_s01 | Data, attributes, features, representation | Core vocabulary; what "a feature" actually is vs. raw data. |
| ch01_s02 | The role of features in ML | Why representation sets the ceiling on what a model can learn. |
| ch01_s03 | Designed vs. learned representations | **Introduces the book's central spectrum** (*dirancang manusia → dipelajari mesin*) — defined here, then invoked **only at pivots**, not repeated every chapter. |
| ch01_s04 | The myth "feature engineering is dead in deep learning" | Reframe: FE shifts form, doesn't disappear. |
| ch01_s05 | From prediction question to the learning table: unit, target, and feature-availability cutoff | **NEW.** What is *one sample* (entity / event / timestamp); the target and prediction horizon; prediction (index) time; the cutoff for information allowed to be a feature. Many apparent "FE errors" are really sample-construction errors. Forward-points to Ch 2 (leakage) and Ch 17 (design framework). |
| ch01_s06 | A map of representation structures | **NEW (short).** Vector / feature matrix, sequence, grid/tensor, set, graph, multimodal — so readers don't assume every representation is $X\in\mathbb{R}^{n\times d}$. The destination Parts IV–V build toward. |
| ch01_s07 | The feature engineering pipeline at a glance | Roadmap of the book; how the parts connect. |
| ch01_s08 | Case study: transaction data → feature matrix | Concrete walk from raw rows to a usable matrix — applies s05 (define the unit/target) then builds the features. |

*Notes: ch01_s03 is where the spectrum is defined, not just called out. ch01_s05 introduces the learning-table backbone early, per review. 8 units.*

### Ch 2 — Pipelines, Validation, and Data Leakage
*(Pipeline, Validasi, dan Data Leakage)* — the home of *praktik pipeline yang benar*; referenced sparingly elsewhere.

| ID | Subsection | Scope |
|---|---|---|
| ch02_s01 | Fit/transform: the pipeline as a training–inference contract | The mental model everything else hangs on. |
| ch02_s02 | Reusable transformers, serialization, reproducible random state | How a transformation stays identical train→inference. |
| ch02_s03 | A taxonomy of leakage | Target, train–test contamination, temporal, between-group. |
| ch02_s04 | Why leakage is born at the feature engineering stage | The book's reason for making this a recurring callout. |
| ch02_s05 | Correct splitting strategies | Random, group, temporal — when each applies; ties to the cutoff from ch01_s05. |
| ch02_s06 | Pipelines inside cross-validation | Where transformation must live to stay honest. |
| ch02_s07 | Common student mistakes | Concrete anti-patterns to recognize. |
| ch02_s08 | Case study: a valid pipeline vs. a leaking one | Side-by-side; the leak made visible. |

*Notes: this chapter IS the pipeline-discipline callout's home; denser, so 8 units.*

---

---

## BAGIAN II — TABULAR DATA TRANSFORMATION

### Ch 3 — Numeric Feature Representation
*(Representasi Fitur Numerik)*

| ID | Subsection | Scope |
|---|---|---|
| ch03_s01 | Scale and distribution: why numeric features need transforming | The problem before the techniques. |
| ch03_s02 | Standardization and min-max scaling | The two workhorses; when each fits. |
| ch03_s03 | Robust scaling | Scaling when outliers are present. |
| ch03_s04 | Power and quantile transforms | Reshaping skewed distributions. |
| ch03_s05 | Clipping and binning | Discretization and its trade-offs. |
| ch03_s06 | Which models are sensitive vs. insensitive to scale | The model-family decision lens: k-NN/SVM vs. trees (first home of the recurring model-family callout). |
| ch03_s07 | Case study: transformation effects on k-NN, SVM, tree-based | Same data, three model families. |

### Ch 4 — Categorical Feature Representation
*(Representasi Fitur Kategorikal)*

| ID | Subsection | Scope |
|---|---|---|
| ch04_s01 | Types of categorical variables | Nominal, ordinal, high-cardinality. |
| ch04_s02 | One-hot and ordinal encoding | The baselines; where each breaks. |
| ch04_s03 | Frequency and count encoding | Cheap encodings for cardinality. |
| ch04_s04 | Target encoding and its leakage risk | Powerful but dangerous; the leakage callout lives here. |
| ch04_s05 | Hashing for high-cardinality features | Trading collisions for memory. |
| ch04_s06 | Entity embeddings | Bridge to learned representations (describe plainly; no spectrum callout needed). |
| ch04_s07 | Handling unseen categories at inference | The production failure mode. |
| ch04_s08 | Case study: encoding comparison on high-cardinality data | Which encoding wins, and why. |

### Ch 5 — Missing Values & Outliers (Reproducible, Pipeline-Based)
*(Missing Values & Outlier — Reproducible, Berbasis Pipeline)*

> Reframed per review: the lesson is **reproducible and pipeline-based**, not "automatic." Automation means *not edited row by row*, never *applied without inspection, diagnostics, and judgment*.

| ID | Subsection | Scope |
|---|---|---|
| ch05_s01 | Missingness mechanisms (MCAR/MAR/MNAR) | Just enough theory to choose a strategy — inspection precedes automation. |
| ch05_s02 | Imputation as a pipeline component | Why it's a *fitted, reproducible transformer*, not a one-off manual edit. |
| ch05_s03 | Simple vs. model-based imputation | Mean/median → iterative/KNN → modern (MIWAE/diffusion) *(recency hook)*. |
| ch05_s04 | The missing-indicator feature | Missingness as signal. |
| ch05_s05 | Outliers: detection vs. handling | Two separate decisions; diagnostics first. |
| ch05_s06 | Robust transformations for outliers | Reducing influence without deleting. |
| ch05_s07 | The boundary between data cleaning and feature engineering | Where this book stops. |
| ch05_s08 | Case study: a reproducible imputation & robust-handling pipeline | Inspected, leakage-safe, fitted on train only — not "hands-off." |

### Ch 6 — Derived Feature Construction
*(Pembentukan Fitur Turunan)*

| ID | Subsection | Scope |
|---|---|---|
| ch06_s01 | Ratios, differences, and interaction features | The most common derivations. |
| ch06_s02 | Polynomial features | Expressiveness vs. explosion. |
| ch06_s03 | Aggregations and group-based features | Features computed over groups. |
| ch06_s04 | Relational & event-log features: joins, aggregations, and point-in-time correctness | **NEW.** One-to-one/one-to-many/many-to-many; aggregating event histories to entity-level features; fan-out duplication from careless joins; as-of / point-in-time joins; features computed only from events available before prediction. Bridges SQL-style FE to automated relational synthesis (Ch 16). |
| ch06_s05 | Domain-driven features | Encoding subject-matter knowledge. |
| ch06_s06 | Date/time and cyclical features | Calendar features; sine/cosine encoding. |
| ch06_s07 | The risk of feature explosion | When more features hurt. |
| ch06_s08 | Validating whether a new feature actually helps | Tie-in to Ch 9. |
| ch06_s09 | Case study: derived features from transaction/health/education data | Domain features in practice. |

---

## BAGIAN III — SELECTION & DIMENSIONALITY REDUCTION

### Ch 7 — Feature Selection
*(Seleksi Fitur)* — combined basics + methods.

| ID | Subsection | Scope |
|---|---|---|
| ch07_s01 | Relevance vs. redundancy; the curse of dimensionality | Why select at all. |
| ch07_s02 | Filter methods | Correlation, mutual information, chi-square. |
| ch07_s03 | Wrapper methods | RFE, sequential selection. |
| ch07_s04 | Embedded methods | LASSO, tree-based importance, Boruta. |
| ch07_s05 | Selection stability and nested validation | Avoiding selection leakage. |
| ch07_s06 | Case study: comparing selection methods on one dataset | Trade-offs made concrete. |

### Ch 8 🔢 — Dimensionality Reduction & Latent Representations
*(Reduksi Dimensi & Representasi Laten)*

| ID | Subsection | Scope |
|---|---|---|
| ch08_s01 | Why reduce dimensionality? Compression vs. visualization | The two distinct goals. |
| ch08_s02 | PCA and SVD / truncated SVD 🔢 | The linear workhorses. |
| ch08_s03 | NMF 🔢 | Non-negative, parts-based factorization. |
| ch08_s04 | Manifold learning: t-SNE and UMAP 🔢 | Nonlinear visualization (UMAP = academic primary). |
| ch08_s05 | Autoencoders as learned compression | Neural, but still *your own data*. |
| ch08_s06 | Using reduced representations well: visualization vs. preprocessing, misuse, and the boundary with Ch 15 | **Merged (old s06+s07).** Common misuse errors; compressing *your own* data vs. *transferred* representations (two-way cross-ref with Ch 15). |
| ch08_s07 | Case study: PCA & autoencoder on high-dimensional data | Linear vs. learned compression. |

### Ch 9 — Feature Quality Evaluation
*(Evaluasi Kualitas Fitur)* — universal prerequisite (with Ch 2).

| ID | Subsection | Scope |
|---|---|---|
| ch09_s01 | What makes a feature good? Predictive utility, stability, availability, and cost | **NEW (opening frame).** Quality is broader than importance: availability at inference, stability over time/populations, sensitivity to measurement error, compute/storage/latency, interpretability, maintainability, robustness under shift. Ablation/SHAP become tools *within* this frame, not its definition. |
| ch09_s02 | Establishing a baseline | You can't judge features without one. |
| ch09_s03 | Ablation studies | Add/remove feature groups, measure impact. |
| ch09_s04 | Permutation and model-based importance | Two importance families. |
| ch09_s05 | SHAP for feature diagnosis | Modern attribution; recency hook. |
| ch09_s06 | Stability across folds; importance ≠ causality | Two critical caveats. |
| ch09_s07 | Sensitive information and proxy features: privacy, fairness, data minimization | **NEW.** Direct sensitive attributes; proxies (postcode, device type); embeddings that retain private information; removing vs. retaining protected attributes and the fairness effect; data minimization; "improves accuracy" ≠ "legitimate." (Recurring as a callout again in Ch 17; this is the concise home, not an ethics chapter.) |
| ch09_s08 | Documenting feature decisions | Feeds Appendix C (feature documentation template). |
| ch09_s09 | Case study: ablation across feature groups | Honest reporting of what helped. |

---

## BAGIAN IV — FEATURE ENGINEERING BY DATA TYPE

### Ch 10 — Time Series & Sensor Data
*(Deret Waktu & Data Sensor)*

| ID | Subsection | Scope |
|---|---|---|
| ch10_s01 | Temporal sample construction: lookback, stride, horizon, and alignment | **NEW (split from old s01).** Windowing *constructs the learning sample*: input-window (lookback) length, stride, prediction horizon, target-window length, input↔target alignment, causal vs. centered windows, overlapping-window dependence, irregular sampling/resampling. |
| ch10_s02 | Lag and rolling-statistics features | **Split from old s01.** Features computed *within or from* the constructed window. |
| ch10_s03 | Differencing, trend, and seasonality | Stationarity-oriented features. |
| ch10_s04 | Frequency-domain features (FFT), briefly | When spectral features matter. |
| ch10_s05 | Temporal validation: avoiding look-ahead leakage | The dominant leakage risk here (modality-specific leakage callout: overlapping windows crossing split boundaries). |
| ch10_s06 | Features for classic models vs. sequential inputs | Engineered vs. RNN/LSTM/Transformer input. |
| ch10_s07 | Case study: multivariate time-series prediction | Temporal split done right. |

### Ch 11 — Text & Documents
*(Teks & Dokumen)*

| ID | Subsection | Scope |
|---|---|---|
| ch11_s01 | Classic text representations | Tokenization, bag-of-words, n-grams. |
| ch11_s02 | TF-IDF | The classic weighting scheme. |
| ch11_s03 | The shift to learned: word embeddings | The shift to learned representations for text (describe plainly; spine label not required). |
| ch11_s04 | Contextual, sentence, and document embeddings | From word to longer spans. |
| ch11_s05 | Pretrained language models as feature extractors | LMs as frozen extractors. |
| ch11_s06 | Fine-tuning vs. feature extraction | The key decision and its trade-offs. |
| ch11_s07 | Case study: document classification — TF-IDF vs. contextual embedding | Designed vs. learned, head to head (modality-specific leakage: vectorizer fit before split, duplicate/same-author docs across folds). |

### Ch 12 — Images & Audio
*(Citra & Audio)* — combined; shared pretrained-encoder pattern, each representation handled separately.

| ID | Subsection | Scope |
|---|---|---|
| ch12_s01 | Images: normalization and augmentation | Preparing pixels. |
| ch12_s02 | Handcrafted image features (HOG) and their limits | The designed end for vision. |
| ch12_s03 | CNN feature extractors and pretrained vision models | The learned end. |
| ch12_s04 | Image embeddings and patches | Modern representations. |
| ch12_s05 | Audio: waveform, spectrogram, MFCC, chroma | **The designed end** of the audio mini-spectrum. |
| ch12_s06 | Pretrained audio encoders: raw-waveform models | wav2vec 2.0, HuBERT — **the learned end** (modern SOTA, not spectrogram-as-image). |
| ch12_s07 | Audio embeddings and aggregation over time | Pooling across frames. |
| ch12_s08 | Case study: handcrafted vs. deep features (image & audio) | Both modalities compared (modality-specific leakage: frames/clips from one source recording across splits). |

### Ch 13 🔢 — Spatial & Graph Data
*(Data Spasial & Graf)* — two distinct halves; academic primary chapter.

| ID | Subsection | Scope |
|---|---|---|
| ch13_s01 | Spatial: coordinates, reference systems, distance & proximity | Location as features. |
| ch13_s02 | Neighborhood features and spatial autocorrelation | Spatial structure as signal. |
| ch13_s03 | Spatial leakage and spatial cross-validation | The spatial-specific leakage callout. |
| ch13_s04 | Graph: degree, centrality, clustering features | Handcrafted graph features. |
| ch13_s05 | Neighborhood aggregation and path-based features | Structure-derived features. |
| ch13_s06 | Node embeddings (Node2Vec) 🔢 | Learned graph representations (academic primary). |
| ch13_s07 | GNNs as representation learners 🔢 | The learned end for graphs. |
| ch13_s08 | Leakage on graphs | Why graph splits are subtle (connected nodes split naively across train/test). |
| ch13_s09 | Case study: location-based prediction & node classification | One case per half. |

### Ch 14 🔢 — Multimodal Data
*(Data Multimodal)* — standalone chapter; academic primary.

| ID | Subsection | Scope |
|---|---|---|
| ch14_s01 | What is multimodal data? Alignment and time synchronization | The setup problem. |
| ch14_s02 | Fusion strategies: early, intermediate, late — and feature- vs. decision-level | **Merged (old s02+s07).** The core design axis (where fusion happens) plus where to combine. |
| ch14_s03 | Feature concatenation and dimensionality balancing | Making modalities combinable. |
| ch14_s04 | Handling missing modalities | A common real-world failure. |
| ch14_s05 | Cross-modal and joint embeddings 🔢 | Shared representation spaces. |
| ch14_s06 | Multimodal pretrained models | CLIP and kin (academic primary). |
| ch14_s07 | Case study: combining tabular + image/text/sensor in one pipeline | Fusion end to end (modality-specific leakage: modalities from one entity split separately). |

---

## BAGIAN V — FEATURE ENGINEERING IN MODERN ML

### Ch 15 🔢 — Learned Representations & Pretrained Models
*(Representasi yang Dipelajari Mesin & Pretrained Model)* — the *dipelajari mesin* end of the spectrum, made practical.

| ID | Subsection | Scope |
|---|---|---|
| ch15_s01 | Embeddings and the adaptation spectrum: from frozen extraction to fine-tuning | **Merged (old s01+s02+s03).** Brief recap of static vs. contextual (defined in Ch 11), then the adaptation continuum: frozen extractor → partial → full fine-tuning, with trade-offs. |
| ch15_s02 | Embedding/feature banks and similarity metrics 🔢 | Storing and comparing embeddings. |
| ch15_s03 | Evaluating embedding quality; domain-shift risk | When transfer fails. |
| ch15_s04 | Boundary with Ch 8 | **Transferred representations vs. compressing your own data** (two-way cross-ref). |
| ch15_s05 | Does DL remove the need for FE? Learned vs. handcrafted | The chapter's thesis question. |
| ch15_s06 | Input representation, tokenization, augmentation | FE that survives inside DL. |
| ch15_s07 | Deep learning on tabular data: learned tabular embeddings | Tabular transformers (e.g. FT-Transformer, TabNet), deep tabular nets as feature extractors; when they beat vs. lose to gradient boosting; relation to entity embeddings (Ch 4). *(recency hook)* |
| ch15_s08 | Hybrid models: engineered features as extra input | Designed + learned together. |
| ch15_s09 | Case study: pretrained extractor + hybrid model (learned + engineered) | The learned-representations synthesis case. |

### Ch 16 — Automated Feature Engineering & Human–AI Collaboration
*(Rekayasa Fitur Otomatis & Kolaborasi Manusia–AI)* — automation is still *dirancang manusia* (human-directed), not *dipelajari mesin*.

| ID | Subsection | Scope |
|---|---|---|
| ch16_s01 | Automated feature generation: Deep Feature Synthesis and the search space | DFS over relational/event data (ties to Ch 6 s04); what the search space is and why it explodes (academic primary: DFS). |
| ch16_s02 | AutoML and automated feature pipelines | Automated search/selection within a pipeline; where it helps and where it just burns compute. |
| ch16_s03 | GenAI for feature proposals; the meaningless-feature risk | LLM-proposed features (academic primary: CAAFE); plausible-but-spurious features; why automation needs a validator. |
| ch16_s04 | Human-in-the-loop: validating and curating machine-proposed features | The collaboration workflow; designer judgment stays essential; automated FE is automated yet still *dirancang manusia*. |
| ch16_s05 | Case study: automated + human-curated features on a relational dataset | DFS/AutoFE proposals filtered by human validation, measured against a baseline. |

---

## BAGIAN VI — CLOSING

### Ch 17 — Synthesis: Designing Pipelines & Lasting Principles
*(Sintesis: Merancang Pipeline & Prinsip yang Bertahan Lama)* — two clear halves (A: design framework, B: principles).

| ID | Subsection | Scope |
|---|---|---|
| ch17_s01 | The design framework: from prediction goal to final pipeline | Goal → **unit → target → split** (the backbone, set up in Ch 1 s05) → sources → transform → select → baseline → evaluate. |
| ch17_s02 | Training–inference consistency and training-serving skew | The production contract. |
| ch17_s03 | Schema validation, transformation versioning, and drift (briefly) | Kept ringkas — this is FE, not MLOps. |
| ch17_s04 | A decision framework across data types | Routing the reader (ties to Appendix A). |
| ch17_s05 | Principles I: start from the problem; features must be available at inference; transformations follow the split | **Merged (old s05+s06+s07).** Plus a brief privacy/proxy callout (recap of Ch 9 s07). |
| ch17_s06 | Principles II: validation over feature count; designed and learned complement each other; the road ahead | **Merged (old s08+s09).** Closes the spectrum thesis. |
| ch17_s07 | Case study: designing pipelines from scratch for several scenarios | Applies the whole book. |

---

## Tally

| Part | Chapters | Subsections |
|---|---|---|
| I — Foundations | 1–2 | 16 |
| II — Tabular | 3–6 | 32 |
| III — Selection & Reduction | 7–9 | 22 |
| IV — By Data Type | 10–14 | 38 |
| V — Modern ML | 15–16 | 14 |
| VI — Closing | 17 | 7 |
| **Total** | **17 chapters** | **129 subsections** |

*Appendices A–F are not prose subsections — in the printed book they are pointers (~1 page each), built as by-products: Appendix D from the Living Glossary, Appendix E from the Dataset × Chapter Matrix (see plan §5–6).*

*Change log vs. the 16-chapter / 127-unit version (colleague review, applied): split old Ch 15 → Ch 15 (Learned Representations) + Ch 16 (Automated FE); old Ch 16 → Ch 17. Added: ch01_s05 (learning-table construction), ch01_s06 (representation-structures map), ch06_s04 (relational/point-in-time), ch09_s01 (broader feature quality), ch09_s07 (privacy/proxy), ch10 windowing split. Merged: ch08 s06+s07, ch14 s02+s07, old ch15 s01-s03, old ch16 five principles → two. Net +2 subsections; book word budget unchanged (per-subsection budget absorbs it).*

*Provisional: the compiler's recency layer may add a subsection where a current technique warrants its own unit (§4).*
