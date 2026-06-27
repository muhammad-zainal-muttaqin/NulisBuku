---
chapter: ch17
title: Synthesis — Designing Pipelines & Lasting Principles
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 17 Resources — Synthesis: Designing Pipelines & Lasting Principles

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence).

## Coverage baseline (what the drafts already have)

- **ch17_s01 (Design Framework):** Goal → unit → target → split → sources → transform → select → baseline → evaluate. Credit scoring example. No mention of concrete design frameworks, checklists, or industry templates.
- **ch17_s02 (Training–Inference Consistency):** Fit/transform contract, median imputation skew example, silent failure risk. No mention of feature stores as a solution, no concrete industry post-mortems.
- **ch17_s03 (Schema Validation, Versioning, Drift):** Abstract coverage of schema validation, versioning, and data drift. Kept ringkas (3 short paragraphs each). No mention of specific tools or frameworks.
- **ch17_s04 (Decision Framework):** High-level routing: tabular → designed, time/spatial → windowing+no leakage, text/image/audio → learned. Mentions interpretability requirements. No concrete decision tree or checklist formalism.
- **ch17_s05 (Principles I):** Problem-driven, availability-at-inference (churn/24h-sync example), transform-follows-split, privacy/proxy callout. Solid but lacks external anchoring.
- **ch17_s06 (Principles II):** Validation over count, designed+learned complement, road ahead (human-AI collaboration). Hybrid medical diagnosis example. Spectrum closing.
- **ch17_s07 (Case Studies):** Two scenarios: retail demand forecasting (tabular/temporal) and multimodal medical diagnosis. Side-by-side architecture diagram. Code placeholder for sklearn pipeline + FeatureUnion.

---

## Resources by subsection

### ch17_s01 — The Design Framework: From Prediction Goal to Final Pipeline

- **Eugene Yan — How to Write Design Docs for ML Systems (2021, evergreen)**  [NEW]  (confidence: high)
  - Summary: Structured framework using Why/What/How. Covers: problem statement framing (surrogate problems), data description, technique selection, validation/experimentation (time-based splits), human-in-the-loop, high-level design diagrams (system-context, data-flow), infra/scalability, performance (throughput/latency), security, data privacy, monitoring+alarms, cost, integration points, risks/uncertainties. Includes minimalist template at github.com/eugeneyan/ml-design-docs. Recommends two-stage review (pre-review + formal review).
  - Why relevant: The most comprehensive industry-standard design doc framework for ML. Directly maps to the draft's "Goal → unit → target → split → sources → transform → select → baseline → evaluate" chain. Adds concrete methodology (surrogate problem, data description, baseline comparison, validation strategy) and implementation (high-level design, serving, monitoring). The two-stage review pattern complements the book's emphasis on pipeline discipline.
  - Source: https://eugeneyan.com/writing/ml-design-docs/ · type: blog · date: Mar 2021 (evergreen)

- **Eugene Yan — The Why, What, How Framework**  [NEW]  (confidence: high)
  - Summary: Writing framework that forces structured thinking: Why (motivation, success criteria, constraints, scope, assumptions), What (the proposal), How (methodology + implementation). Designed to make design docs clear enough for asynchronous review.
  - Why relevant: Provides the underlying reasoning structure that the draft's design framework implicitly follows. Can be referenced as a lightweight mental model for designing FE pipelines.
  - Source: https://eugeneyan.com/writing/writing-docs-why-what-how/ · type: blog · date: Mar 2021

- **Google Cloud — Rules of ML (Martin Zinkevich, 2016, evergreen)**  [REFRESH]  (confidence: high)
  - Summary: 43 rules of thumb for production ML. Rule #4: "Keep the first model simple and get the infrastructure right." Rule #32: "Reorder training examples and use progressive sampling." Rule #37: "Don't use a feature unless it has proven useful." Classic reference for production ML design.
  - Why relevant: The "Rules of ML" is the de facto industry reference for production ML design principles. Multiple rules (especially #4, #28, #32, #36, #37, #40, #43) directly reinforce ch17_s01 and ch17_s05 principles. Widely cited as a foundational design framework.
  - Source: https://developers.google.com/machine-learning/guides/rules-of-ml · type: docs · date: 2016 (evergreen)

### ch17_s02 — Training–Inference Consistency and Training-Serving Skew

- **Feast — Open Source Feature Store (v0.64.0, June 2026)**  [NEW]  (confidence: verified)
  - Summary: Feast (7.1k GitHub stars) is the open-source feature store originally from GoJek, now under the LF AI & Data Foundation. Core architecture: (1) offline store for historical feature extraction (training), (2) online store for low-latency serving (inference), (3) Python SDK for defining features, entities, sources, and transformations. Key features: point-in-time correct feature retrieval, push-based online serving, schema validation (enable_validation parameter), feature versioning (alpha), entity aliasing, on-demand feature views, stream feature views. Supports multiple offline stores (BigQuery, Snowflake, Redshift, DuckDB) and online stores (Redis, DynamoDB, Datastore, Postgres, and many more). Explicitly NOT an ETL system, data orchestrator, or data warehouse.
  - Why relevant: Feast directly addresses the training-serving skew problem the draft describes — it ensures features are computed identically in training and inference through a unified API. The point-in-time correctness mechanism prevents temporal leakage. The offline/online store architecture is the canonical pattern for maintaining training-inference consistency. Provides a concrete tooling answer to the draft's abstract "use the same pipeline object" advice.
  - Source: https://docs.feast.dev · https://github.com/feast-dev/feast · type: docs + repo · date: v0.64.0 (Jun 2026)

- **Tecton/Databricks — What is a Feature Store (May 2025, updated post-acquisition)**  [NEW]  (confidence: verified)
  - Summary: Tecton (acquired by Databricks Aug 2025) defines the five components of a feature store: Transformation, Storage, Serving, Monitoring, and Feature Registry. Explains three feature types: Batch Transform (data at rest), Streaming Transform (Kafka/Kinesis), On-Demand Transform (request-time data). Describes entity-based data model with timestamps. Emphasizes that feature stores "run data pipelines that transform raw data into feature values, store and manage the feature data, and serve it consistently for training and inference." Covers backfill jobs, automatic feature recomputation, and enterprise capabilities.
  - Why relevant: Authoritative definition of feature store architecture from the company that created Feast (Willem Pienaar) and later built Tecton. The five-component model gives the draft a concrete reference for how production systems solve training-serving skew. The three feature types (batch, streaming, on-demand) map to different latency/freshness requirements useful for ch17_s04's decision framework.
  - Source: https://www.databricks.com/blog/what-is-a-feature-store · type: blog/docs · date: May 2025

- **Eugene Yan — Feature Stores: A Hierarchy of Needs (Feb 2021)**  [NEW]  (confidence: high)
  - Summary: Organizes feature store capabilities into five levels: (1) Access — reducing duplication, encouraging reusability; (2) Serving — using features in real-time at high throughput/low latency; (3) Integrity — minimizing train-serve skew, point-in-time correctness (time travel); (4) Convenience — simple APIs, unified SDKs (GoJek's Feast), interactive development; (5) Autopilot — automated backfilling, monitoring, anomaly detection. Extensive case studies: GoJek (Feast), Uber (Palette), Netflix (distributed time-travel, shared feature encoders), DoorDash (Gigascale with Redis, 10M+ QPS), Airbnb (Zipline backfill), Alibaba (real-time recommendations).
  - Why relevant: The "integrity" level directly addresses ch17_s02 and ch17_s03. Uber's dual-store sync (Hive ↔ Cassandra), Netflix's shared feature encoders, and GoJek's unified API are concrete industry patterns for maintaining training-inference consistency. The hierarchy provides a framework to explain to readers *what level of feature store sophistication they actually need* — not everyone needs DoorDash-level gigascale.
  - Source: https://eugeneyan.com/writing/feature-stores/ · type: blog · date: Feb 2021

- **DoorDash — Building a Gigascale ML Feature Store with Redis (Nov 2020)**  [REFRESH]  (confidence: high)
  - Summary: DoorDash's feature store handles billions of feature-value pairs across millions of entities, serves 10+ million QPS, and refreshes daily via fast batch writes. They benchmarked Redis, Cassandra, CockroachDB, ScyllaDB, and YugabyteDB before choosing Redis. Real-time features (e.g., 20-min moving average delivery time) update uniformly throughout the day.
  - Why relevant: The extreme end of the feature store spectrum — provides concrete scale numbers that ground the draft's abstract discussions. Shows that training-serving consistency at gigascale requires careful architecture choices (Redis binary serialization + compression).
  - Source: https://doordash.engineering/2020/11/19/building-a-gigascale-ml-feature-store-with-redis/ · type: eng blog · date: Nov 2020

- **Netflix — Distributed Time Travel for Feature Generation (Jun 2019)**  [REFRESH]  (confidence: high)
  - Summary: Netflix's solution for point-in-time correct feature generation. Takes snapshots of offline and online data with stratified sampling on attributes (viewing patterns, device, time, region). Parallel Spark jobs call microservices via Prana to capture online state. Snapshots stored in S3/Parquet. Provides simple APIs for data scientists to create time-travel features.
  - Why relevant: Concrete example of point-in-time correctness at scale. The stratified sampling approach to snapshot creation is a practical pattern for resource-constrained settings. The "same encoders" pattern (offline Spark vs. online microservices using identical feature encoders) is a direct mitigation for training-serving skew.
  - Source: https://netflixtechblog.com/distributed-time-travel-for-feature-generation-389cccdd3907 · type: eng blog · date: Jun 2019

- **Feast — Feature View Concept & Schema Validation**  [NEW]  (confidence: verified)
  - Summary: Feast's FeatureView is an object representing a logical group of time-series feature data. Contains: data source, zero or more entities, name, optional schema (fields with types), TTL, optional enable_validation for schema checks during materialization. Schema validation verifies: all declared feature columns present, column types match expected Feast types. Entity aliasing allows join_key_map overrides for multi-role entities. Feature views support automatic version tracking with @v<N> syntax for version-qualified reads.
  - Why relevant: The FeatureView abstraction is a production-grade implementation of the "feature definition" concept the draft alludes to. The enable_validation parameter and version tracking directly address ch17_s03's schema validation and versioning needs. Shows how a real system codifies the "train with the same feature definitions as serve" principle.
  - Source: https://docs.feast.dev/getting-started/concepts/feature-view · type: docs · date: v0.64.0 (2026)

### ch17_s03 — Schema Validation, Transformation Versioning, and Drift

- **Evidently AI — Open-Source ML/LLM Observability (v0.7.21, Mar 2026)**  [NEW]  (confidence: verified)
  - Summary: Evidently (7.6k GitHub stars, 40M+ downloads) is an open-source framework for evaluating, testing, and monitoring data and AI systems. 100+ built-in metrics covering: text descriptors (sentiment, toxicity, etc.), data quality (missing values, duplicates, min-max ranges), data drift (20+ statistical tests and distance metrics), classification metrics, regression metrics, ranking metrics, recommendation metrics. Features: Reports (interactive HTML), Test Suites (with pass/fail conditions), Monitoring Dashboard (self-hosted or Cloud). Supports tabular and text data, predictive and generative tasks.
  - Why relevant: The primary open-source tool for the data quality, schema validation, and drift detection topics in ch17_s03. 20+ statistical tests for distribution shift gives concrete methods beyond the draft's generic "detect drift" discussion. Test Suites with auto-generated conditions from reference data provide a practical schema validation pattern.
  - Source: https://docs.evidentlyai.com · https://github.com/evidentlyai/evidently · type: docs + repo · date: v0.7.21 (Mar 2026)

- **Evidently AI — "My Data Drifted, What's Next?" (Nov 2021, updated Jul 2025)**  [NEW]  (confidence: high)
  - Summary: Actionable response framework when drift is detected: (1) Check data quality first — bugs and logging errors masquerade as drift; (2) Investigate the drift — plot distributions, check correlations, involve domain experts; (3) Do nothing — false alert, acceptable performance, wait for labels; (4) Retrain if labels available; (5) Calibrate or rebuild model — reweight samples, create segment-specific models, change prediction target, consider online learning; (6) Pause model and use fallback — human expert, heuristics, classic models; (7) Find low-performing segments and route predictions accordingly; (8) Apply business logic on top. Emphasizes "design drift monitoring backwards from possible actions."
  - Why relevant: The draft describes drift detection but not *what to do about it*. This framework provides a complete decision tree linking drift signals to concrete actions — exactly what the synthesis chapter should offer. The "data quality first" priority reinforces the schema validation discussion. The segment-routing pattern connects to ch17_s04's decision framework.
  - Source: https://www.evidentlyai.com/blog/ml-monitoring-data-drift-how-to-handle · type: blog · date: Nov 2021 (updated Jul 2025)

- **NannyML — Post-Deployment Data Science (v0.13.1, Jul 2025)**  [NEW]  (confidence: verified)
  - Summary: NannyML (2.1k GitHub stars) focuses on post-deployment model monitoring without access to targets. Key capabilities: (1) CBPE (Confidence-Based Performance Estimation) for classification — estimates ROC AUC, accuracy, etc. without ground truth; (2) DLE (Direct Loss Estimation) for regression; (3) Multivariate drift detection using PCA-based data reconstruction; (4) Univariate drift detection with multiple statistical tests (Jensen-Shannon, L-Infinity, etc.); (5) Intelligent alerting that links drift alerts to estimated performance drops, reducing alert fatigue.
  - Why relevant: Addresses a gap in the draft — the draft assumes labels are available, but in many production systems they arrive with delay or not at all. CBPE/DLE are novel algorithms (researched by NannyML team) for estimating performance degradation from drift. The PCA-based multivariate approach complements Evidently's univariate focus.
  - Source: https://github.com/NannyML/nannyml · https://nannyml.com · type: repo + docs · date: v0.13.1 (Jul 2025)

- **Pandera — DataFrame Validation (v0.32.0, 2026)**  [NEW]  (confidence: verified)
  - Summary: Open-source schema validation library for dataframes. Supports pandas, polars, pyspark, dask, modin, ibis, geopandas via a Narwhals-powered unified backend. Features: DataFrameSchema with column type checks, custom Check objects (range, isin, str_matches, etc.), DataFrameModel (class-based schema definition), Hypothesis testing integration, lazy validation (collect all errors), decorators for pipeline integration (@check_input, @check_output, @check_io), schema inference from data, YAML/JSON serialization. Also supports xarray DataArrays and Datasets.
  - Why relevant: The most mature open-source schema validation library for Python dataframes. Pandera's @check_input/@check_output decorators provide a direct, minimal-integration pattern for adding validation to FE pipelines without a full MLOps platform. The DataFrameModel pattern (class-based schemas) provides a maintainable way to version schema definitions.
  - Source: https://pandera.readthedocs.io · type: docs · date: v0.32.0 (2026)

- **DVC — Data and Model Versioning (v3.x, 2026)**  [NEW]  (confidence: verified)
  - Summary: DVC (Data Version Control) is an open-source Git extension that versions data, models, and pipelines alongside code. Key features: metafiles (.dvc) tracked in Git point to data/model files stored in cloud/on-premise storage; pipelines defined in dvc.yaml; experiment tracking with metrics/params/plots; data registry for sharing; CI/CD integration. Enables Git-like workflows (checkout, diff, push/pull) for datasets and model artifacts. Explicitly designed to address "what version of data produced what version of model."
  - Why relevant: Directly addresses the transformation versioning discussion in ch17_s03. DVC bridges the gap between Git (code) and feature pipeline artifacts (data, models). The dvc.yaml pipeline definition allows versioning entire FE pipeline graphs — exactly what the draft calls for when discussing rollback coordination between model versions and feature pipeline versions.
  - Source: https://dvc.org/doc · type: docs · date: v3.x (2026)

### ch17_s04 — A Decision Framework Across Data Types

- **Google Cloud — ML Problem Framing Guide (evergreen)**  [NEW]  (confidence: high)
  - Summary: Google's official guide on how to frame ML problems: classification vs. regression, label prediction, output class structure, proxy labels, offline/online inference considerations. Covers the decision of batch vs. online inference based on latency requirements and output usage patterns.
  - Why relevant: Provides a structured approach to the "what type of ML problem" decision that underlies the draft's data-type routing. Helps readers choose between classification/regression/ranking before choosing between tabular/time-series/image features.
  - Source: https://developers.google.com/machine-learning/problem-framing · type: docs · date: evergreen

### ch17_s05 — Principles I: Problem-First, Availability at Inference, Transform Follows Split

- **Chip Huyen — Building A Generative AI Platform (Jul 2024)**  [NEW]  (confidence: high)
  - Summary: Defines context construction as "feature engineering for foundation models" — the same purpose of giving models necessary information. Covers RAG (term-based + embedding-based retrieval, hybrid search), query rewriting, guardrails (input/output, PII masking, jailbreaking), model routing, caching (prompt cache, exact cache, semantic cache), complex logic + write actions. Observability section covers model and system metrics, logs, traces. Observes that "context construction for foundation models is equivalent to feature engineering for classical ML models. They serve the same purpose."
  - Why relevant: Reframes traditional feature engineering for the GenAI era. The "context construction = FE for LLMs" equivalence is a powerful framing for students who think FE is obsolete. The observability architecture (metrics, logs, traces) provides a concrete blueprint for what a production monitoring system for features should look like. The guardrails discussion also reinforces the privacy/proxy callout in ch17_s05.
  - Source: https://huyenchip.com/2024/07/25/genai-platform.html · type: blog · date: Jul 2024

### ch17_s06 — Principles II: Validation Over Count, Designed + Learned Complement, Road Ahead

- **Feast — Feature Monitoring & Data Quality**  [NEW]  (confidence: verified)
  - Summary: Feast includes built-in feature monitoring capabilities: feature quality metrics, drift detection on served features, serving log monitoring, and a UI dashboard for visualization. The feature quality management RFC outlines data profiling, validation (deprecated Great Expectations integration), and automated quality checks.
  - Why relevant: Shows that even feature stores are incorporating monitoring — validation and monitoring are not separate concerns from feature design. Supports ch17_s06's argument that validation rigor should be built into the feature pipeline, not added as an afterthought.
  - Source: https://docs.feast.dev/how-to-guides/feature-monitoring · type: docs · date: v0.64.0 (2026)

### ch17_s07 — Case Study: Designing Pipelines from Scratch

- **Feast Quickstart — End-to-End Feature Store Workflow**  [NEW]  (confidence: verified)
  - Summary: Feast quickstart demonstrates the complete workflow: (1) Install `pip install feast`, (2) `feast init` create repo, (3) `feast apply` register definitions, (4) `feast ui` explore, (5) `store.get_historical_features(entity_df, features)` build training dataset with point-in-time correctness, (6) `feast materialize-incremental` load features to online store, (7) `store.get_online_features(features, entity_rows)` serve at low latency. Python SDK code examples for each step.
  - Why relevant: Provides a ready-made code example for the draft's case study. The seven-step workflow is a concrete instantiation of the "design framework → production" journey the draft describes. The `get_historical_features` + `get_online_features` pairing demonstrates training-inference consistency in practice.
  - Source: https://docs.feast.dev/getting-started/quickstart · https://github.com/feast-dev/feast · type: docs + quickstart · date: v0.64.0 (2026)

---

## Cross-cutting / chapter-level new developments

- **Feature Store Industry Consolidation (2025)**  [NEW]  (confidence: verified)
  - Summary: Major acquisitions in the feature-store/ML-platform space: (1) Tecton acquired by Databricks (Aug 2025) — bringing managed feature-store-as-a-service into the Databricks ecosystem; (2) neptune.ai acquired by OpenAI (Dec 2025) — bringing experiment tracking and ML monitoring into frontier model training. Databricks Feature Store now offers Declarative Feature APIs for automated batch/streaming feature pipelines.
  - Why relevant: Signals the maturation of feature stores from startup offering to integrated infrastructure. Means readers in 2026+ will likely encounter feature stores embedded within their data platform (Databricks, AWS SageMaker) rather than as standalone tools. Useful context for the "road ahead" discussion.

- **The Convergence of Monitoring Tools and Feature Stores**  [NEW]  (confidence: high)
  - Summary: Modern tooling is converging monitoring (Evidently, NannyML) with feature serving (Feast, Tecton/Databricks). Feast now includes built-in feature monitoring and drift detection. Evidently and NannyML can integrate with feature stores as data sources. The implication: the line between "feature engineering" and "ML monitoring" is disappearing — features designed with validation, monitoring, and drift detection in mind from the start are more production-robust.
  - Why relevant: Directly supports ch17_s06's closing thesis that the road ahead is about integration, not separation. Readers should expect to design features that are self-monitoring, not features that are handed off to a separate monitoring team.

- **Data Drift Response Decision Tree**  [NEW]  (confidence: high)
  - Summary: Synthesized from Evidently AI blog, NannyML docs, and industry practice, a practical decision framework for drift response: (1) Is it data quality or real drift? → data quality: fix the pipeline; (2) Is there performance degradation? → if no: monitor, if yes: continue; (3) Are labels available? → if yes: retrain/rebuild, if no: continue; (4) Is the model critical? → if no: live with it, if yes: use fallback strategy; (5) Can you identify low-performing segments? → if yes: route/limit model, if no: pause entirely and use heuristics.
  - Why relevant: Provides a teachable decision tree that ties together all of ch17_s03 (drift), ch17_s05 (availability), and ch17_s04 (decision framework). Can be rendered as a visual figure.

- **Feature Engineering Canvases and Checklists (2024–2025)**  [NEW]  (confidence: moderate)
  - Summary: Emerging documentation pattern in the ML community: lightweight "feature engineering canvases" (like business model canvases) that guide practitioners through: prediction goal → entities → target → features by source → availability at inference → leakage risk → baseline. No single dominant standard exists yet, but the pattern is visible in Google's Rules of ML, Eugene Yan's design docs template, and various company-internal frameworks. The book's Appendix B (leakage checklist) and Appendix C (feature documentation template) are part of this trend.
  - Why relevant: Situates the book's appendices within a broader industry movement toward structured feature design documentation. Can be mentioned as a brief "this is emerging" note in ch17_s04 or ch17_s01 without requiring deep treatment.

---

## Candidate new terms (for Living Glossary / Appendix D)

| Term | Definition | Section |
|---|---|---|
| Feature Store | Centralized system for storing, versioning, and serving ML features with metadata and access controls, enabling reuse and consistency across training and inference | ch17_s02 |
| Offline Store | Feature store component storing historical features for batch model training, typically backed by data warehouses/lakes (BigQuery, Snowflake, S3) | ch17_s02 |
| Online Store | Feature store component storing latest feature values for low-latency inference serving, typically backed by key-value stores (Redis, DynamoDB) | ch17_s02 |
| Point-in-Time Correctness | Guarantee that historical features used during training reflect only information available before each example's timestamp, preventing temporal data leakage | ch17_s02 |
| Training-Serving Skew | Degradation in model performance caused by discrepancies between how features are computed in training vs. production serving environments | ch17_s02 |
| Data Drift | Change in the statistical properties (distribution) of input features over time, potentially degrading model accuracy | ch17_s03 |
| Concept Drift | Change in the relationship between input features and target variable, making previously learned patterns invalid | ch17_s03 |
| Feature View | Feast's abstraction for a logical group of time-series feature data, defining entities, schema, data source, and TTL for consistent training/serving access | ch17_s02 |
| Entity | In feature stores, the object (user, product, transaction) that features are associated with, identified by join keys | ch17_s02 |
| Schema Validation | Runtime verification that incoming data conforms to expected column names, data types, and value constraints before entering the feature pipeline | ch17_s03 |
| Feature Versioning | Practice of tracking and managing changes to feature definitions and transformation logic, enabling reproducible model rollbacks | ch17_s03 |
| CBPE (Confidence-Based Performance Estimation) | NannyML's algorithm for estimating classification model performance without access to ground truth labels, using model confidence scores | ch17_s03 |
| DLE (Direct Loss Estimation) | NannyML's algorithm for estimating regression model performance without access to ground truth, using a separate estimator for the loss function | ch17_s03 |
| Model Gateway | Intermediate layer providing unified, secure access to multiple models (both internal and third-party APIs) with access control, cost management, and fallback policies | ch17_s02 |
| Context Construction | In GenAI platforms, the process of gathering relevant information (documents, SQL results, web search) to augment a user query — analogous to feature engineering for classical ML | ch17_s05 |
| Hybrid Search | Retrieval strategy combining term-based (BM25, keyword) and embedding-based (vector search) retrieval, using the cheaper method for candidate generation and the more precise method for reranking | ch17_s04 |
| Entity Aliasing | Feature store capability to map different join key column names to the same logical entity, useful when the same entity type appears in multiple roles (e.g., origin/destination as aliases of "location") | ch17_s02 |
| Time Travel | Feature store capability to retrieve feature values as they existed at a specific point in time, used for creating historically accurate training datasets | ch17_s02 |

---

## Source list

- [1] Feast Documentation v0.64.0 — https://docs.feast.dev (docs, Jun 2026)
- [2] Feast GitHub Repository — https://github.com/feast-dev/feast (repo, 7.1k stars, v0.64.0 Jun 2026)
- [3] Feast Feature View Concepts — https://docs.feast.dev/getting-started/concepts/feature-view (docs, v0.64.0)
- [4] Feast Quickstart — https://docs.feast.dev/getting-started/quickstart (docs, v0.64.0)
- [5] Feast Feature Monitoring — https://docs.feast.dev/how-to-guides/feature-monitoring (docs, v0.64.0)
- [6] Tecton/Databricks — "What is a Feature Store" — https://www.databricks.com/blog/what-is-a-feature-store (blog, May 2025)
- [7] Evidently AI Documentation — https://docs.evidentlyai.com (docs, v0.7.21 Mar 2026)
- [8] Evidently AI GitHub — https://github.com/evidentlyai/evidently (repo, 7.6k stars, v0.7.21)
- [9] Evidently AI — "My Data Drifted, What's Next?" — https://www.evidentlyai.com/blog/ml-monitoring-data-drift-how-to-handle (blog, Nov 2021/Jul 2025)
- [10] NannyML GitHub — https://github.com/NannyML/nannyml (repo, 2.1k stars, v0.13.1 Jul 2025)
- [11] NannyML Website — https://nannyml.com (product, 2025)
- [12] Pandera Documentation v0.32.0 — https://pandera.readthedocs.io (docs, v0.32.0, 2026)
- [13] DVC Documentation v3.x — https://dvc.org/doc (docs, v3.x, 2026)
- [14] Eugene Yan — "Feature Stores: A Hierarchy of Needs" — https://eugeneyan.com/writing/feature-stores/ (blog, Feb 2021)
- [15] Eugene Yan — "How to Write Design Docs for ML Systems" — https://eugeneyan.com/writing/ml-design-docs/ (blog, Mar 2021)
- [16] Eugene Yan — "The Why, What, How Framework" — https://eugeneyan.com/writing/writing-docs-why-what-how/ (blog, Mar 2021)
- [17] Chip Huyen — "Building A Generative AI Platform" — https://huyenchip.com/2024/07/25/genai-platform.html (blog, Jul 2024)
- [18] DoorDash Engineering — "Building a Gigascale ML Feature Store with Redis" — https://doordash.engineering/2020/11/19/building-a-gigascale-ml-feature-store-with-redis/ (blog, Nov 2020)
- [19] Netflix Tech Blog — "Distributed Time Travel for Feature Generation" — https://netflixtechblog.com/distributed-time-travel-for-feature-generation-389cccdd3907 (blog, Jun 2019)
- [20] Google Cloud — "Rules of ML" — https://developers.google.com/machine-learning/guides/rules-of-ml (docs, 2016, evergreen)
- [21] Google Cloud — "ML Problem Framing" — https://developers.google.com/machine-learning/problem-framing (docs, evergreen)
