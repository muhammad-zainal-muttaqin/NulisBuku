---
chapter: ch02
title: Pipelines, Validation, and Data Leakage
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 2 Resources — Pipelines, Validation, and Data Leakage

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence).

## Coverage baseline (what the drafts already have)

- ch02_s01: fit/transform contract, pipeline as encapsulation, training-serving skew defined, standardisation example
- ch02_s02: transformer as object, serialisation, random state for reproducibility — but NO mention of `set_output(transform='pandas')`, NO `Pipeline(memory=...)` caching, NO imblearn.Pipeline
- ch02_s03: four-category taxonomy (target, train-test contamination, temporal, between-group) — sufficient, but missing modern leakage types (embedding leakage, LLM fine-tuning leakage)
- ch02_s04: why leakage happens at FE stage (aggregate features, global transforms before split) — solid
- ch02_s05: random split, group split, temporal split — mentions concepts but not the SPECIFIC sklearn API classes (GroupKFold, TimeSeriesSplit, StratifiedGroupKFold)
- ch02_s06: pipeline inside CV — describes the problem well but NO mention of nested CV, NO mention of Pipeline `memory` parameter for CV caching
- ch02_s07: three student mistakes — global scaling before split, fit_transform on test, manual manipulations outside transformer
- ch02_s08: real-estate imputation case study — side-by-side leaking vs. valid pipeline

---

## Resources by subsection

### ch02_s01 — Fit/transform: the pipeline as a training–inference contract

- **`set_output(transform='pandas')` — pandas-aware pipeline output**  [REFRESH]  (confidence: verified)
  - Summary: scikit-learn v1.2+ introduced `set_output` which allows any transformer or pipeline to return pandas DataFrames instead of NumPy arrays, preserving column names through the entire pipeline chain. Can be set globally via `sklearn.set_config(transform_output='pandas')`. Works with `Pipeline`, `ColumnTransformer`, all individual transformers. Also supports `polars` output since v1.4.
  - Why relevant: The draft mentions the pipeline contract conceptually but never addresses the practical problem of losing feature names during transformations. This API makes pipelines far more useful for real workflows — debugging, feature-name tracking, and integration with `feature_names_in_` for later model inspection.
  - Source: https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_set_output.html · type: docs (official example) · date: scikit-learn 1.2+ (stable in 1.9.0, 2026)

- **Pipeline `memory` parameter for transformer caching**  [NEW]  (confidence: verified)
  - Summary: `Pipeline(steps, memory=cachedir)` caches fitted transformers to disk using `joblib.Memory`. When the same transformer with the same parameters and input data is fit again within a grid search or CV loop, the cached result is reused — avoiding redundant computation. The last step is never cached. Enabling caching clones transformers before fitting (original instance cannot be inspected).
  - Why relevant: Directly supports ch02_s06 (pipelines inside CV). A practical optimisation that makes large-scale pipeline CV feasible. The draft mentions the conceptual need but this is a concrete API feature students and practitioners should know.
  - Source: https://scikit-learn.org/stable/modules/compose.html#pipeline (section "Caching transformers: avoid repeated computation") · type: docs · date: scikit-learn 1.9.0

### ch02_s02 — Reusable transformers, serialisation, reproducible random state

- **Imbalanced-learn Pipeline for resampling inside the pipeline contract**  [NEW]  (confidence: verified)
  - Summary: `imblearn.pipeline.Pipeline` extends sklearn's Pipeline to handle samplers (SMOTE, RandomUnderSampler, etc.) that implement `fit_resample`. Critical nuance: `fit_transform` on this pipeline triggers resampling (producing a resampled dataset), while calling `fit` then `transform` separately does NOT resample — the sampler only activates during `fit`. This breaks the scikit-learn contract expectation that `fit_transform` equals `fit` + `transform`. Supports memory caching and `set_output` (inherited from sklearn).
  - Why relevant: The draft discusses transformers and serialisation but never mentions that resampling (a common imbalanced-data operation) needs a special pipeline. Students using SMOTE outside a pipeline will leak synthetic minority samples — a concrete anti-pattern that belongs in ch02_s07.
  - Source: https://imbalanced-learn.org/stable/references/generated/imblearn.pipeline.Pipeline.html · type: docs · date: imbalanced-learn 0.14.2 (2026)

- **Scikit-learn model persistence guidance**  [REFRESH]  (confidence: verified)
  - Summary: sklearn User Guide section 11 (Model persistence) documents the recommended serialisation approach. Official recommendation is `joblib` or `pickle` for scikit-learn objects; `ONNX` for interoperability with non-Python runtimes. Security note: never unpickle untrusted data.
  - Why relevant: The draft discusses serialisation in general terms; this provides the concrete, updated official guidance.
  - Source: https://scikit-learn.org/stable/model_persistence.html · type: docs · date: scikit-learn 1.9.0

- **Random state best practices from sklearn common pitfalls**  [REFRESH]  (confidence: verified)
  - Summary: The sklearn Common Pitfalls page (§12.3) provides detailed guidance on `random_state`: for estimators, passing a `RandomState` instance gives more robust CV results (different RNG per fold); for CV splitters, passing an integer is safer (ensures fold-to-fold comparability). Warns against setting global numpy seed. Also documents the cloning subtleties when `RandomState` instances are shared across estimators.
  - Why relevant: The draft mentions random_state but this adds important nuance about integer vs. instance, and the fold-to-fold comparability issue — directly useful for ch02_s06.
  - Source: https://scikit-learn.org/stable/common_pitfalls.html · type: docs · date: scikit-learn 1.9.0

### ch02_s03 — A taxonomy of leakage

- **Embedding leakage: same pretrained model fit on all data before splitting**  [NEW]  (confidence: verified)
  - Summary: A modern leakage pattern where a pretrained model (e.g., BERT, CLIP, GPT-family) is used to generate embeddings for the entire dataset BEFORE the train/test split. Since the model was pretrained on external data, this appears safe — but if fine-tuning or adapter-training happens on the full dataset before splitting, test-set information contaminates the embeddings. Even without fine-tuning, if the same embedding extraction is considered "part of feature engineering," its parameters were fit on all data.
  - Why relevant: This is a leakage type absent from the draft's four-category taxonomy. It's especially relevant in the deep learning / LLM era. Cross-references ch15 (learned representations).
  - Source: Chip Huyen, "Designing Machine Learning Systems" (O'Reilly 2022), Chapter 6 + https://huyenchip.com/2022/02/07/data-distribution-shifts-and-monitoring.html · type: book + blog · date: 2022

- **LLM fine-tuning data leakage: training-data contamination from test sets**  [NEW]  (confidence: uncertain)
  - Summary: When fine-tuning LLMs for downstream tasks, practitioners sometimes inadvertently include test-set documents in pretraining corpora or instruction-tuning datasets. This is a form of target leakage at scale — the model "memorises" answers rather than learning to generalise. Benchmarks like MMLU, GSM8K, and HumanEval have documented contamination issues. The phenomenon generalises: any large-scale feature extraction or representation learning that sees the full dataset before splitting can leak.
  - Why relevant: A concrete modern example of target leakage that extends the taxonomy. Relevant for students who will encounter LLM fine-tuning workflows.
  - Source: https://arxiv.org/abs/2311.01640 ("Pretraining Data Mixtures Enable Narrow Model Selection Capabilities in Transformer Models" — contamination measurement) · type: paper · date: 2023

- **Chip Huyen's production data shifts as leakage precursors**  [REFRESH]  (confidence: verified)
  - Summary: Huyen (2022) documents how many "data shifts" detected in production are actually caused by internal errors — bugs in the data pipeline, features standardised using wrong-statistics subset, inconsistencies between training and inference feature extraction. These are effectively leakage's twin: the flip side where the model was trained on data that doesn't match production reality. Also introduces the concept of "train-serving skew" as the umbrella term.
  - Why relevant: Provides a production-oriented framing that complements the draft's more academic taxonomy. Connects leakage taxonomy to MLOps monitoring practice.
  - Source: https://huyenchip.com/2022/02/07/data-distribution-shifts-and-monitoring.html · type: blog (Stanford CS 329S course notes) · date: Feb 2022

### ch02_s04 — Why leakage is born at the feature engineering stage

- **Feature stores as leakage prevention infrastructure**  [NEW]  (confidence: verified)
  - Summary: Feature stores (Feast, Tecton) provide point-in-time-correct feature retrieval — they ensure that when you request features for training at time T, you ONLY get feature values that existed before T. This directly prevents temporal leakage at the infrastructure level. Feast explicitly documents "Avoid data leakage by generating point-in-time correct feature sets" as a core design goal. The point-in-time join is the key mechanism: it joins feature values based on event timestamps, ensuring future values don't leak.
  - Why relevant: This is the infrastructure-level answer to the problem the draft raises. Instead of relying solely on programmer discipline, feature stores encode the temporal constraint into the data infrastructure. Bridges to ch06_s04 (relational/point-in-time features) and ch16 (automated FE).
  - Source: https://docs.feast.dev/ · type: docs (official) · date: 2026 (Feast current)

- **ColumnTransformer + FeatureUnion as pipeline-level leakage guardrails**  [REFRESH]  (confidence: verified)
  - Summary: `ColumnTransformer` applies different transformations to different column subsets within a single Pipeline object. When the ColumnTransformer is placed inside a Pipeline and used with `cross_val_score`, each column's transformations are fit ONLY on the training fold — preventing per-column leakage. `FeatureUnion` concatenates outputs of parallel transformers, all fit on the same training data. These abstractions make leakage-safe heterogeneous-data processing the default path.
  - Why relevant: The draft mentions the problem but the concrete tooling (ColumnTransformer) that makes safety-by-default possible is only implied. This makes the "how" concrete.
  - Source: https://scikit-learn.org/stable/modules/compose.html · type: docs · date: scikit-learn 1.9.0

### ch02_s05 — Correct splitting strategies

- **GroupKFold, StratifiedGroupKFold, TimeSeriesSplit — concrete sklearn API**  [REFRESH]  (confidence: verified)
  - Summary: `GroupKFold(n_splits=5, shuffle=True)` ensures NO group appears in both train and test across folds. Since v1.6: `shuffle` and `random_state` parameters added. `StratifiedGroupKFold` combines GroupKFold stratification — preserves class distribution while keeping groups intact. `TimeSeriesSplit(n_splits=5, gap=0, test_size=None, max_train_size=None)` implements chronological split where training sets are supersets of earlier folds. `gap` parameter (v0.24+) allows skipping samples between train and test to simulate real deployment delays.
  - Why relevant: The draft describes the concepts but never names the actual sklearn API classes. Students need to know these exist to implement what the draft teaches. Additionally, the `gap` parameter in TimeSeriesSplit is a 2020+ addition not widely known.
  - Source: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html · type: API docs · date: scikit-learn 1.9.0

- **Nested cross-validation for unbiased model evaluation**  [NEW]  (confidence: verified)
  - Summary: Nested CV uses an outer loop (cross_val_score) to estimate generalisation error and an inner loop (GridSearchCV) for hyperparameter tuning. Without nesting, using the SAME data for both tuning and evaluation yields optimistically biased scores — a form of leakage through hyperparameter selection. The sklearn example demonstrates that non-nested scores are consistently higher than nested scores (avg difference ~0.008 on iris with SVC). Reference: Cawley & Talbot (2010).
  - Why relevant: This is a critical validation concept that sits at the intersection of ch02_s05 (splits) and ch02_s06 (CV). The draft doesn't mention nested CV at all. It's a textbook case of selection-bias-as-leakage.
  - Source: https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html · type: docs (official example) · date: scikit-learn 1.9.0

### ch02_s06 — Pipelines inside cross-validation

- **Pipeline `memory` caching for efficient CV**  [NEW]  (confidence: verified)
  - Summary: When running `GridSearchCV` over a Pipeline with expensive transformers (e.g., PCA, feature selection), the `memory` parameter avoids re-fitting transformers on every hyperparameter combination. Cachedir stores intermediate transformer results; if parameters and input data are identical across a CV fold, the cached version is loaded. Critical for making CV with deep pipelines computationally tractable.
  - Why relevant: Ch02_s06 explains why pipelines belong inside CV but doesn't address the practical computational cost. This is the optimisation that makes the principle scalable. The draft's code placeholder `[KODE: ...]` is exactly where this concept should appear.
  - Source: https://scikit-learn.org/stable/modules/compose.html#pipeline (section "Caching transformers") · type: docs · date: scikit-learn 1.9.0

- **Data transformation with held-out data — sklearn CV documentation**  [REFRESH]  (confidence: verified)
  - Summary: The sklearn cross-validation user guide (§3.1.1) explicitly demonstrates the correct pattern: `scaler.fit(X_train)` then `scaler.transform(X_test)`, contrasted with the Pipeline-based `cross_val_score(clf, X, y, cv=cv)` which automates this inside each fold. Documents that `cross_validate` returns fit-times, score-times, and optionally training scores and fitted estimators.
  - Why relevant: Directly supports the draft's argument with official documentation citations. The `cross_validate` function (with `return_estimator=True`) is a more modern alternative to `cross_val_score` that the draft doesn't mention.
  - Source: https://scikit-learn.org/stable/modules/cross_validation.html · type: docs · date: scikit-learn 1.9.0

### ch02_s07 — Common student mistakes

- **Anti-pattern: using the same pretrained model to embed all data before splitting**  [NEW]  (confidence: verified)
  - Summary: Students familiar with deep learning often run `model.encode(all_data)` then `train_test_split(embeddings, labels)`. If the encoder was fine-tuned or adapted on the full dataset (even partially), the test set has already influenced the training representations. This is equivalent to fitting a scaler on the full dataset before splitting. The fix: split raw data first, then fit/transform the encoder on train only.
  - Why relevant: This is a modern, DL-era anti-pattern that the draft's three-item list (from a pre-DL perspective) doesn't cover. It's increasingly common as pretrained models become standard.
  - Source: General principle derived from sklearn's "Data leakage during pre-processing" documentation (https://scikit-learn.org/stable/common_pitfalls.html) applied to embedding extraction · type: synthesis · confidence: verified (principle is well-established)

- **Common pitfalls in sklearn: inconsistent preprocessing**  [REFRESH]  (confidence: verified)
  - Summary: The sklearn Common Pitfalls page (§12.1) provides a concrete code example of wrong (scale train only, not test) vs. right (scale both with fitted scaler) vs. best (Pipeline). Shows that forgetting to transform test data can cause MSE to jump from 0.90 to 62.80. Also covers data leakage through feature selection (§12.2.2) — selecting features on all data before splitting inflates accuracy from 0.5 (random) to 0.76.
  - Why relevant: Provides concrete, reproducible numerical examples that can be cited in the draft to make the anti-patterns tangible with real numbers.
  - Source: https://scikit-learn.org/stable/common_pitfalls.html · type: docs · date: scikit-learn 1.9.0

### ch02_s08 — Case study: a valid pipeline vs. a leaking one

- **Feast point-in-time joins as a production-grade case extension**  [NEW]  (confidence: verified)
  - Summary: The draft's real-estate case study could be extended with a production-scale example: using a feature store with point-in-time-correct joins to guarantee that imputation values are computed from data that was available at prediction time. Feast demonstrates this pattern: define a FeatureView with a TTL (time-to-live), and the offline store automatically filters out future data when generating training datasets.
  - Why relevant: Extends the pedagogical case study into a production MLOps context, connecting the chapter's lessons to infrastructure students will encounter.
  - Source: https://docs.feast.dev/ · type: docs · date: 2026

---

## Cross-cutting / chapter-level new developments

- **ML monitoring tools for leakage/drift detection: Great Expectations, Evidently AI, TFDV**  [NEW]  (confidence: verified)
  - Summary: Three major open-source tools provide data validation layers that catch leakage-adjacent problems in production. Great Expectations (greatexpectations.io) validates data schemas, distributions, and expectations — can alert when feature distributions shift between training and serving. Evidently AI (evidentlyai.com) provides pre-built Data Drift, Data Quality, and Target Drift reports. TensorFlow Data Validation (TFDV) generates schema from training data and detects anomalies/skew in serving data. These tools operationalise the chapter's principles.
  - Why relevant: The draft focuses on prevention at development time; these tools address detection in production. Together they complete the "prevent → detect" lifecycle. A brief mention in ch02 would bridge to the monitoring discussion in ch17.
  - Source: https://docs.evidentlyai.com/ , https://greatexpectations.io/ , https://www.tensorflow.org/tfx/data_validation · type: docs · date: 2024-2026

- **Temporal leakage in online learning: event-time vs. processing-time**  [NEW]  (confidence: uncertain)
  - Summary: In online/streaming ML systems, features arrive with two timestamps: event-time (when the event actually happened) and processing-time (when the system received it). Using processing-time for splits can cause leakage because late-arriving data may be assigned to the wrong chronological split. Industry best practice (e.g., at Uber, Google) is to always use event-time for temporal splits and feature computation windows.
  - Why relevant: Extends the temporal leakage discussion in ch02_s03 and ch02_s05 to real-time systems. This is a nuance the draft's simpler "past vs. future" framing doesn't capture.
  - Source: General MLOps principle documented in multiple sources; see also Feast point-in-time join documentation · type: synthesis · date: 2024

---

## Candidate new terms (for Living Glossary / Appendix D)

| Term | Definition | Source |
|---|---|---|
| point-in-time join | A join that ensures feature values are retrieved as they existed at a specific timestamp, preventing future data from leaking into training. | Feast docs |
| nested cross-validation | Two-layer CV: outer loop estimates generalisation, inner loop tunes hyperparameters. Prevents selection-bias-as-leakage. | sklearn docs / Cawley & Talbot 2010 |
| feature store | A data management layer that serves features for training and inference with point-in-time correctness, schema validation, and consistency guarantees. | Feast / Tecton |
| training-serving skew | The difference between model performance during training and performance during serving, caused by inconsistencies in the data pipeline. | Chip Huyen, Designing ML Systems |
| embedding leakage | A leakage pattern where a pretrained model generates representations for the entire dataset before a train/test split, causing test-set information to contaminate training representations. | synthesis (sklearn principle applied to DL) |
| StratifiedGroupKFold | CV splitter that preserves class distribution while ensuring no group appears in both train and test folds. | sklearn 1.4+ API |
| set_output API | sklearn API (v1.2+) that configures transformers to return pandas DataFrames instead of NumPy arrays, preserving column names. | sklearn docs |

---

## Source list

1. [1] sklearn `set_output` API — https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_set_output.html (official example, scikit-learn 1.9.0, 2026)
2. [2] sklearn Pipelines and composite estimators — https://scikit-learn.org/stable/modules/compose.html (official docs, scikit-learn 1.9.0, 2026)
3. [3] sklearn Cross-validation — https://scikit-learn.org/stable/modules/cross_validation.html (official docs, scikit-learn 1.9.0, 2026)
4. [4] sklearn Common pitfalls — https://scikit-learn.org/stable/common_pitfalls.html (official docs, scikit-learn 1.9.0, 2026)
5. [5] sklearn Nested vs. non-nested CV — https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html (official example, scikit-learn 1.9.0, 2026)
6. [6] sklearn GroupKFold API — https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html (API docs, scikit-learn 1.9.0, 2026)
7. [7] sklearn TimeSeriesSplit API — https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html (API docs, scikit-learn 1.9.0, 2026)
8. [8] imbalanced-learn Pipeline — https://imbalanced-learn.org/stable/references/generated/imblearn.pipeline.Pipeline.html (API docs, imbalanced-learn 0.14.2, 2026)
9. [9] Chip Huyen, Data Distribution Shifts and Monitoring — https://huyenchip.com/2022/02/07/data-distribution-shifts-and-monitoring.html (blog / CS 329S course notes, Feb 2022) — Note: expanded in book "Designing Machine Learning Systems" (O'Reilly 2022)
10. [10] Feast Feature Store documentation — https://docs.feast.dev/ (official docs, 2026)
11. [11] Cawley, G.C.; Talbot, N.L.C. "On over-fitting in model selection and subsequent selection bias in performance evaluation." JMLR 2010, 11, 2079-2107. (paper, 2010)
12. [12] Evidently AI — https://docs.evidentlyai.com/ (docs, 2024+)
13. [13] Great Expectations — https://greatexpectations.io/ (docs, 2024+)
14. [14] TensorFlow Data Validation — https://www.tensorflow.org/tfx/data_validation (docs, 2024+)
15. [15] sklearn Model persistence — https://scikit-learn.org/stable/model_persistence.html (official docs, scikit-learn 1.9.0, 2026)
