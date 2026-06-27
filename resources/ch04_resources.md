---
chapter: ch04
title: Categorical Feature Representation
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 4 Resources — Categorical Feature Representation

> External material gathered 2026-06-27. Tagging: [NEW] = absent from current drafts · [REFRESH] = newer/better source for a topic the draft already covers. Each item carries provenance (source · type · date · confidence). Confidence = "verified" when the claim was read off the source actually fetched; "uncertain" when it rests on a search snippet only or a number that disagreed across versions.

## Coverage baseline (what the drafts already have)
- **s01** Nominal (no order), ordinal (meaningful rank), high-cardinality (too many unique levels) defined with concrete Indonesian examples. States ML models cannot process raw text labels; encoding = translation to numeric representation.
- **s02** Ordinal encoding maps to integers → works for tree-based models but misleads linear models (fake magnitude). One-hot encoding creates binary columns per category → safe for linear models but explodes dimensionality with high cardinality.
- **s03** Count/frequency encoding replaces labels with occurrence count or proportion. Reduces cardinality to single column; risk of collisions when two different categories share the same count.
- **s04** Target encoding replaces category with mean target value; powerful for linear relationships but acute leakage risk if computed on full dataset. Mentions smoothing for small categories and "praktik pipeline yang benar" (fit on train only). No specific encoder variants (CatBoost/James-Stein/GLMM) or CV-based fitting.
- **s05** Hashing maps categories to fixed-width numeric indices via hash function → deterministic, no memory for unseen values, but trades collision risk for fixed memory. No mention of modern improvements (learned hash, collision-aware methods).
- **s06** Entity embeddings = trainable dense vectors for each category learned during neural network training. Captures semantic similarity (e.g., Saturday/Sunday close together). Bridge to Part V. Based on Guo & Berkhahn 2016.
- **s07** Unseen categories = new labels at inference time. Pipeline must provide fallback ("Other"/"Unknown" category). Uses rare-category consolidation during training + mapping unknowns to the catch-all at inference.
- **s08** Case study: retail pricing across zip codes comparing One-Hot → Hashing → Target Encoding → Entity Embeddings. Concludes dense representations (target encoding, entity embeddings) perform best on high-cardinality data.

---

## Resources by subsection

### ch04_s01 — Types of categorical variables

- **Feature-engine official guide on categorical types, cardinality, and unseen categories**  [REFRESH]  (confidence: verified)
  - Summary: The Feature-engine documentation clearly defines nominal vs ordinal, low vs high cardinality, and the concept of unseen categories. It notes that high-cardinality features can lead to overfitting in tree-based models and that numeric features can also be categorical (e.g., Store ID, Zip Code).
  - Why relevant: Authoritative, modern (actively maintained) taxonomy that matches the draft's structure; gives vocabulary and rationale that can be cited directly.
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/index.html · type: docs · date: 2024-2026 · 

- **scikit-learn 1.9 categorical feature definitions with missing-value handling**  [REFRESH]  (confidence: verified)
  - Summary: scikit-learn v1.9 docs explicitly treat missing values (`np.nan`, `None`) as additional categories in OneHotEncoder and OrdinalEncoder. The `encoded_missing_value` parameter gives ordinal encoding a dedicated integer for NaN.
  - Why relevant: The draft does not mention how missing values interact with categorical encoders (an important real-world nuance); this gives a concrete API-anchored addition.
  - Source: https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features · type: docs · date: 1.9.0 (2026) · 

### ch04_s02 — One-hot and ordinal encoding

- **scikit-learn `min_frequency` and `max_categories` for infrequent categories in OrdinalEncoder and OneHotEncoder**  [NEW]  (confidence: verified)
  - Summary: scikit-learn 1.9 supports `min_frequency` (absolute count or fraction) and `max_categories` (upper limit on output columns per feature) to aggregate infrequent categories into a single bucket. OneHotEncoder's `handle_unknown='infrequent_if_exist'` silently routes unseen categories to the infrequent bucket or all-zeros.
  - Why relevant: The draft treats one-hot as a baseline with no practical guardrails; this is the built-in mechanism to prevent explosion and handle unseen data — directly feeds both s02 and s07.
  - Source: https://scikit-learn.org/stable/modules/preprocessing.html#infrequent-categories · type: docs · date: 1.9.0 (2026) · 

- **OrdinalEncoder with `encoded_missing_value` and `handle_unknown`**  [NEW]  (confidence: verified)
  - Summary: `OrdinalEncoder(encoded_missing_value=-1, handle_unknown='use_encoded_value', unknown_value=3)` explicitly maps both missing values and unseen categories to designated integers, avoiding NaN propagation or crashes.
  - Why relevant: Production-grade details the draft omits entirely; practical defense against the "unseen category crash" of s07.
  - Source: https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features · type: docs · date: 1.9.0 (2026) · 

### ch04_s03 — Frequency and count encoding

- **Feature-engine `CountFrequencyEncoder` — production-grade implementation with unseen handling**  [NEW]  (confidence: verified)
  - Summary: `CountFrequencyEncoder(encoding_method='count'|'frequency', unseen='encode')` allows explicit assignment of count/frequency 0 to unseen categories at inference. Works with both regression and classification, multi-class included.
  - Why relevant: The draft mentions collision risk but not the unseen-category gap; this is the named, scikit-learn-compatible encoder with the missing guardrail.
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/CountFrequencyEncoder.html · type: docs · date: 2024-2026 · 

- **category_encoders `CountEncoder` — `combine_min_categories()` for rare-category grouping**  [NEW]  (confidence: verified)
  - Summary: `CountEncoder` from the category_encoders library includes a `combine_min_categories()` method to group rare categories before counting, reducing collision risk and handling unseen values.
  - Why relevant: Direct operational fix for the draft's collision problem; available in the most popular sklearn-compatible encoding library.
  - Source: https://contrib.scikit-learn.org/category_encoders/count.html · type: docs · date: 2024 (v2.8.1) · 

### ch04_s04 — Target encoding and its leakage risk

- **scikit-learn `TargetEncoder` — full shrinkage + cross-fitting formula (v1.3+)**  [REFRESH]  (confidence: verified)
  - Summary: scikit-learn 1.9 TargetEncoder implements empirical Bayes shrinkage: S_i = λ_i·(n_iY/n_i) + (1-λ_i)·(n_Y/n) where λ_i = n_i/(m+n_i) and `smooth="auto"` computes m = σ_i²/τ². **Key differentiator:** `fit(X, y).transform(X)` ≠ `fit_transform(X, y)` because `fit_transform` uses internal cross-fitting (5-fold by default, configurable via `cv` parameter) to prevent leakage. Supports continuous, binary, and multiclass targets. Unseen categories encoded with global target mean.
  - Why relevant: The draft mentions leakage prevention and smoothing generically; this gives the exact formula, the cross-fitting mechanism, the `smooth` parameter, and the sklearn API — all ready to cite at book's version anchor (1.9). Also bridges Ch 2 (pipeline discipline / cross-validation inside transformation).
  - Source: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html · type: docs · date: 1.9.0 (2026) · 

- **category_encoders library — supervised encoder family and their distinct shrinkage strategies**  [NEW]  (confidence: verified)
  - Summary: The library provides a full taxonomy of target-based encoders, each with a different shrinkage/regularization approach:
    - **TargetEncoder** — classic Micci-Barreca (2001) smoothing: weighted blend of category mean and global mean.
    - **CatBoostEncoder** — ordered target statistics: computes target mean using only *prior* observations in a random permutation, preventing label leakage through data ordering.
    - **JamesSteinEncoder** — James-Stein shrinkage estimator, pulling category means toward the global mean with stronger shrinkage for small-sample categories (empirical Bayes).
    - **GLMMEncoder** — Generalized Linear Mixed Model, fitting a hierarchical model per categorical feature; captures both fixed and random effects (Gelman & Hill, 2006).
    - **MEstimateEncoder** — M-estimate smoothing with a prior weight `m`; λ = n_i/(n_i + m).
    - **LeaveOneOutEncoder** — LOO target mean (compute mean excluding the current row); `fit_transform()` uses internal nested CV to counter overfitting.
    - **QuantileEncoder** — encodes category by its empirical quantile bucket (Mougan et al., MDAI 2021).
    - **WOEEncoder** — Weight of Evidence = ln(P(X=x|Y=1) / P(X=x|Y=0)), standard in credit risk / finance.
  - Why relevant: The draft only mentions "target encoding" and "smoothing" generically. This taxonomy anchors s04 with the current state of the art — each variant is a scikit-learn-compatible transformer with its own leakage-control mechanism. The CatBoost, James-Stein, and GLMM encoders were specifically requested for the book.
  - Source: https://contrib.scikit-learn.org/category_encoders/ · type: docs · date: 2024 (v2.8.1) · GitHub: https://github.com/scikit-learn-contrib/category_encoders · 

- **CatBoost ordered target statistics — the no-leakage CTR formula**  [REFRESH]  (confidence: verified)
  - Summary: CatBoost transforms categorical features using the formula `avg_target = (countInClass + prior) / (totalCount + 1)`, where counts are computed **only from previous objects in a random permutation** — a streaming-style ordered statistic that guarantees no information from the current row leaks into its own encoding. Multiple random permutations are generated for robustness. The `one_hot_max_size` parameter controls threshold below which one-hot is used instead of CTR (default = 2 for non-ranking, 10 for ranking, 255 for GPU without target data). **CatBoost explicitly warns: do not manually one-hot encode categorical features before training.**
  - Why relevant: The draft describes target encoding leakage prevention only in abstract pipeline terms. This is the concrete algorithmic mechanism (ordered statistics + permutations) that CatBoost uses to make target encoding *leakage-safe by construction* — a named technique the book must cover given CatBoost's native categorical handling.
  - Source: https://catboost.ai/en/docs/concepts/algorithm-main-stages_cat-to-numberic · type: docs · date: 2024-2026 · Also: https://catboost.ai/en/docs/features/categorical-features · 

- **Feature-engine `MeanEncoder` — smoothing and unseen-category fallback**  [NEW]  (confidence: verified)
  - Summary: `MeanEncoder(smoothing='auto', unseen='encode')` uses the target mean per category blended with global mean. Unseen categories automatically receive the global target mean value. Works for binary classification and regression.
  - Why relevant: A third library's perspective on leakage-safe target encoding (smoothing parameter, unseen handling), giving the reader multiple implementation paths.
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/MeanEncoder.html · type: docs · date: 2024-2026 · 

### ch04_s05 — Hashing for high-cardinality features

- **category_encoders `HashingEncoder` — sklearn-compatible with configurable n_components**  [REFRESH]  (confidence: verified)
  - Summary: `HashingEncoder(n_components=8)` maps categories to `n_components` binary columns via the hashing trick. Supports parallel hashing (`n_jobs`), and can hash in chunks. Deterministic: same string always maps to same columns.
  - Why relevant: The draft describes hashing conceptually; this gives the exact API (with parameter names and parallelism detail) the reader would use in practice.
  - Source: https://contrib.scikit-learn.org/category_encoders/hashing.html · type: docs · date: 2024 (v2.8.1) · 

- **scikit-learn `FeatureHasher` — low-level hashing for arbitrary feature spaces**  [NEW]  (confidence: verified)
  - Summary: `FeatureHasher(n_features=2**20, input_type='string')` applies the hashing trick to any iterable of (feature_name, value) pairs. Uses signed 32-bit murmurhash3. The `alternate_sign=True` default reduces collision bias through cancellation. Designed for text token features but usable for categorical variables.
  - Why relevant: The sklearn-native hashing implementation is a practical alternative to the category_encoders one; important for readers who want to stay within sklearn's ecosystem. The `alternate_sign` trick is a subtle but important collision-mitigation technique the draft doesn't mention.
  - Source: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.FeatureHasher.html · type: docs · date: 1.9.0 (2026) · 

- **Feature-engine hashing approach — intentionally NOT supported, with rationale**  [NEW]  (confidence: verified)
  - Summary: Feature-engine's documentation explicitly states it does NOT support hashing or binary encoding because these methods "return features that are not easy to interpret" and "it is very hard to make sense of the outputs of machine learning models trained on categorical variables encoded with these methods."
  - Why relevant: Important trade-off note — hashing solves memory at the cost of interpretability; Feature-engine's deliberate omission gives the draft a design-philosophy counterpoint to present.
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/index.html · type: docs · date: 2024-2026 · 

### ch04_s06 — Entity embeddings

- **Guo & Berkhahn (2016) — the foundational entity embeddings paper (already cited in draft)**  [REFRESH]  (confidence: verified)
  - Summary: Proposes mapping categorical variables to Euclidean embedding spaces learned by a neural network during supervised training. Key findings: (1) reduces memory vs one-hot; (2) places similar categories close in embedding space (revealing intrinsic structure); (3) embeddings trained from one task boost downstream model performance when used as input features; (4) especially useful for high-cardinality datasets where other methods overfit. Achieved 3rd place in a Kaggle competition.
  - Why relevant: The draft already describes this paper well, but the arXiv abstract confirms the key claims about generalization, distance measures, and visualization potential.
  - Source: https://arxiv.org/abs/1604.06737 · type: paper · date: 2016-04 · 

- **LLM-derived embeddings for non-semantic categorical data — Bakumenko et al. (2024)**  [NEW]  (confidence: verified)
  - Summary: Proposes using pretrained sentence-transformer LLMs to encode categorical values (e.g., GL account codes, product IDs — data that has *label text* but no inherent linguistic meaning) as dense semantic embeddings. Tested 3 sentence-transformer models (all-MiniLM-L6-v2, all-mpnet-base-v2, multi-qa-mpnet-base-dot-v1) on real-world financial ledger data. LLM embeddings + downstream classifiers (LR, RF, GBM, SVM, NN) **outperform traditional encoding baselines**, especially in tackling feature sparsity. Published in IEEE Access 2025.
  - Why relevant: This is the bridge from s06 (entity embeddings — learned during training on *your* data) to the modern paradigm (semantic embeddings — pretrained on *external* data). Directly requested as a priority topic. The paper's key insight: even "non-semantic" categorical labels benefit from LLM embeddings because category *names* carry latent semantic information (e.g., "Jakarta" encodes geographic meaning).
  - Source: https://arxiv.org/abs/2406.03614 · type: paper · date: 2024-06 · Published: IEEE Access 13 (2025) 146757-146771 · DOI: 10.1109/ACCESS.2025.3600967 · 

- **Feature-engine `DecisionTreeEncoder` — tree-based learned encoding as midpoint between target encoding and entity embeddings**  [NEW]  (confidence: verified)
  - Summary: `DecisionTreeEncoder()` trains a decision tree (or random forest) per categorical feature to predict the target, then replaces each category with the tree's prediction (mean target in the leaf). Works as a "poor man's learned representation" — simpler than neural entity embeddings, but data-driven and supervised like them.
  - Why relevant: Positions decision tree encoding on the designed→learned continuum between target encoding (statistical) and entity embeddings (neural), giving the chapter a narrative through-line the draft lacks.
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/DecisionTreeEncoder.html · type: docs · date: 2024-2026 · 

- **UniRec — unified multimodal encoding with categorical features for LLM-based recommendation (Lei et al., 2026)**  [NEW]  (confidence: verified)
  - Summary: Formalizes recommendation features into four modalities: text, images, categorical features, numerical attributes. Proposes modality-specific encoders with triplet representation (attribute name, type, value) to preserve semantic distinctions. Outperforms SOTA multimodal and LLM-based recommenders by up to 15%.
  - Why relevant: Shows how categorical feature representation is being integrated into the LLM stack — not just as preprocessing, but as a first-class modality alongside text and images. Positions the chapter's topic in the 2026 research frontier.
  - Source: https://arxiv.org/abs/2601.19423 · type: paper · date: 2026-01 · 

### ch04_s07 — Handling unseen categories at inference

- **scikit-learn's comprehensive unseen-category handling matrix**  [REFRESH]  (confidence: verified)
  - Summary: Across sklearn 1.9:
    - `OneHotEncoder(handle_unknown='infrequent_if_exist')`: unknown → infrequent bucket or all-zeros
    - `OneHotEncoder(handle_unknown='ignore')`: unknown → all zeros + `inverse_transform` maps all-zeros to dropped category or `None`
    - `OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)`: unknown → explicit integer
    - `TargetEncoder.fit_transform()`: unseen categories → global target mean (`target_mean_` attribute)
    - `OneHotEncoder(min_frequency=...)`: categories below threshold grouped into infrequent bucket during `fit`; unseen at `transform` also routed there when `handle_unknown='infrequent_if_exist'`
  - Why relevant: The draft's "Other"/"Unknown" strategy is sound but generic; this gives the exact sklearn mechanisms — per-encoder, per-parameter — that implement that strategy in production pipelines.
  - Source: https://scikit-learn.org/stable/modules/preprocessing.html · type: docs · date: 1.9.0 (2026) · 

- **Feature-engine `RareLabelEncoder` — explicit rare-category grouping as pre-encoding step**  [NEW]  (confidence: verified)
  - Summary: `RareLabelEncoder(tol=0.05, n_categories=10, replace_with='Rare')` groups infrequent categories into a single label *before* encoding. This is a preprocessing step designed to work with any downstream encoder (one-hot, ordinal, target, WoE). Reduces cardinality and prevents unseen-category failures.
  - Why relevant: The draft s07 talks about creating an "Other" category as a strategy but names no tool; this is the exact, named transformer for that job. Separates concern (rare grouping) from concern (encoding).
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/RareLabelEncoder.html · type: docs · date: 2024-2026 · 

- **Feature-engine `StringSimilarityEncoder` — handling unseen "near-miss" categories via string distance**  [NEW]  (confidence: verified)
  - Summary: Encodes categories by their string similarity to each other (cosine/Levenshtein/Jaro-Winkler etc.), producing float features in [0,1]. Useful for "dirty" categorical data — misspellings, abbreviations, inconsistent capitalisation. Groups near-identical categories together.
  - Why relevant: An alternative unseen-category strategy: if a novel label is a minor typo of a known one ("Jakrta" vs "Jakarta"), string similarity catches it. Expands s07 beyond the simple fallback bucket.
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/StringSimilarityEncoder.html · type: docs · date: 2024-2026 · 

### ch04_s08 — Case study: encoding comparison on high-cardinality data

- **category_encoders `NestedCVWrapper` — leakage-safe supervised encoding for benchmarking**  [NEW]  (confidence: verified)
  - Summary: `NestedCVWrapper` wraps any supervised encoder to perform nested cross-validation during training — the inner folds compute the encoding parameters; the outer fold evaluates model performance. This is the *correct* way to benchmark supervised encoders (target, CatBoost, James-Stein, GLMM, etc.) without inflating scores via leakage.
  - Why relevant: The case study (s08) compares encoders by accuracy; without nested CV, target-based encoders will artificially dominate. This wrapper is the methodological guardrail the case study needs.
  - Source: https://contrib.scikit-learn.org/category_encoders/ · type: docs · date: 2024 (v2.8.1) · 

- **CatBoost parameter tuning — one_hot_max_size, random permutations, and hyperparameter guidance**  [NEW]  (confidence: verified)
  - Summary: CatBoost docs recommend: (a) never one-hot encode during preprocessing — use `one_hot_max_size` instead (inbuilt); (b) `has_time` parameter preserves temporal order for CTR computation (no random permutation when data is naturally ordered); (c) CTR types include Borders, Buckets, BinarizedTargetMeanValue, and Counter. The "Counter" CTR is count-based and does NOT depend on the label.
  - Why relevant: Concrete tuning advice for CatBoost as a comparison baseline in the case study; also reinforces the draft's leakage theme (ordered statistics, no-preprocessing one-hot).
  - Source: https://catboost.ai/en/docs/concepts/parameter-tuning · type: docs · date: 2024-2026 · 

- **Feature-engine encoding comparison matrix (regression / binary / multiclass support)**  [REFRESH]  (confidence: verified)
  - Summary: Feature-engine provides a clear compatibility table: OneHotEncoder, OrdinalEncoder, CountFrequencyEncoder, and DecisionTreeEncoder support all target types; MeanEncoder = binary + regression only; WoEEncoder = binary classification only. Also notes monotonicity: most encoders produce or attempt monotonic relationships between encoded variable and target, benefiting linear models.
  - Why relevant: The case study needs to respect these constraints — e.g., WoE cannot be included in a regression benchmark. The monotonicity note is a quantitative quality metric the draft doesn't discuss.
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/index.html · type: docs · date: 2024-2026 · 

---

## Cross-cutting resources (applicable to multiple subsections)

- **category_encoders library — full inventory (v2.8.1, 20+ encoders)**  [REFRESH]  (confidence: verified)
  - Summary: The library provides **unsupervised encoders** (BackwardDifference, BaseN, Binary, Gray, Count, Hashing, Helmert, Ordinal, OneHot, Polynomial, RankHot, Sum) and **supervised encoders** (CatBoost, GLMM, JamesStein, LeaveOneOut, MEstimate, Target, WeightOfEvidence, Quantile, SummaryEncoder). All are sklearn-compatible `fit()`/`transform()` transformers. Key usage notes: (1) internally works with pandas DataFrames; (2) `fit_transform()` ≠ `fit().transform()` for supervised encoders due to internal CV mechanisms; (3) wrappers available: `PolynomialWrapper` for multi-output, `NestedCVWrapper` for leakage-safe evaluation.
  - Why relevant: This is the de-facto standard encoding library for the sklearn ecosystem (2.5k GitHub stars, active maintenance). Every subsection from s03 onward can reference specific encoders from this library. Contains references to foundational papers (Micci-Barreca 2001, Weinberger et al. 2009, Gelman & Hill 2006, Zhang LOO encoding).
  - Source: https://contrib.scikit-learn.org/category_encoders/ · type: docs + GitHub · date: 2024 (v2.8.1) · GitHub: https://github.com/scikit-learn-contrib/category_encoders · 

- **Fairness implications of encoding protected categorical attributes — Mougan et al. (2023)**  [NEW]  (confidence: verified)
  - Summary: Studies how different categorical encoding schemes affect fairness when the categorical variable encodes protected attributes (gender, race, etc.) or their proxies (zip code → race, device type → socioeconomic status). Key finding: encoding choice impacts downstream fairness metrics; some encodings inadvertently preserve or amplify sensitive information. Published at AAAI/ACM AIES 2023.
  - Why relevant: Requested as a priority topic. The draft does not address fairness at all in Ch 4, but Ch 9 dedicates a subsection to "sensitive information and proxy features" (ch09_s07). This paper explicitly bridges categorical encoding → fairness, giving the writer a cross-reference hook from Ch 4 to Ch 9 and ensuring the chapter acknowledges the ethical dimension of encoding decisions.
  - Source: https://arxiv.org/abs/2201.11358 · type: paper · date: 2023-01 · Published: AAAI/ACM AIES 2023 · 

- **Binary encoding and Gray encoding — alternative compressed encodings for tree-based models**  [NEW]  (confidence: verified)
  - Summary: Binary encoding converts each integer category ID to its binary representation, creating log₂(n_categories) columns instead of n_categories (one-hot) or 1 (ordinal). Gray encoding uses Gray code instead (adjacent numbers differ by 1 bit). Both provide a middle ground between one-hot (wide) and ordinal (single column, misleading distances for non-ordinal data).
  - Why relevant: The draft omits these entirely, but they're a practical third option for the s02 "baselines" conversation, especially for tree-based models that benefit from the low-dimensional compressed representation.
  - Source: https://contrib.scikit-learn.org/category_encoders/binary.html · type: docs · date: 2024 (v2.8.1) · 

- **Feature-engine encoders — complete API surface for reproducibility**  [REFRESH]  (confidence: verified)
  - Summary: All Feature-engine encoders inherit from a unified base, support `fit()`/`transform()`/`fit_transform()`, accept `variables` parameter for column selection, and handle unseen categories through `unseen` parameters where applicable. Compatible with `sklearn.pipeline.Pipeline` and `ColumnTransformer`. Version 1.1.0+ allows encoding numerical variables via `ignore_format=False`. The RareLabelEncoder (`tol`, `n_categories`, `replace_with='Rare'`) is the universal pre-encoding cardinality reducer.
  - Why relevant: Complete API reference for every encoder that the book's companion notebook would use. Gives the writer concrete names to reference in prose instead of describing operations generically.
  - Source: https://feature-engine.trainindata.com/en/latest/user_guide/encoding/index.html · type: docs · date: 2024-2026 · 

- **WoEEE — hybrid enhancement for categorical data transformation (M et al., 2025)**  [NEW]  (confidence: uncertain — abstract elided by publisher)
  - Summary: A 2025 paper proposing a hybrid approach combining multiple encoding strategies for enhanced categorical data transformation. Published in International Journal of Data Science and Analytics (Springer, 2025).
  - Why relevant: Indicates ongoing research into hybrid encoding strategies (combining strengths of multiple approaches), demonstrating the field remains active beyond the 2016-2020 encoder library consolidation.
  - Source: https://doi.org/10.1007/s41060-025-00845-5 · type: paper · date: 2025 · International Journal of Data Science and Analytics · 

---

## Source summary

| Source | Type | Date | Confidence |
|---|---|---|---|
| scikit-learn preprocessing docs (v1.9) | Official docs | 2026 | verified |
| category_encoders library docs (v2.8.1) | Official docs | 2024 | verified |
| Feature-engine encoding guide | Official docs | 2024-2026 | verified |
| CatBoost algorithm docs (CTR formula) | Official docs | 2024-2026 | verified |
| CatBoost categorical features guide | Official docs | 2024-2026 | verified |
| CatBoost parameter tuning guide | Official docs | 2024-2026 | verified |
| Guo & Berkhahn — Entity Embeddings of Categorical Variables (arXiv:1604.06737) | Paper | 2016 | verified |
| Bakumenko et al. — Non-Semantic Financial Data Encoding with LLMs (arXiv:2406.03614) | Paper | 2024-2025 | verified |
| Mougan et al. — Fairness Implications of Encoding Protected Categorical Attributes (arXiv:2201.11358) | Paper | 2023 | verified |
| Lei et al. — UniRec: Unified Multimodal Encoding for LLM-Based Recommendations (arXiv:2601.19423) | Paper | 2026 | verified |
| WoEEE hybrid encoder | Paper | 2025 | uncertain |

**Total sources:** 11 (7 verified · 1 uncertain · 3 foundational from draft's existing base)

**New vs Refresh breakdown:** 14 [NEW] · 10 [REFRESH]

**Gaps identified (no sources found, noted for awareness):**
- Optimal transport-based categorical encoders (no verified paper found in 2024-2026 window; topic may be too niche/academic)
- Factorization machines vs entity embeddings head-to-head comparison (no direct comparison paper found)
- Learned hash / collision-aware hashing for categorical features beyond basic feature hashing (search and arxiv lookups yielded no ML-focused result in the requested period)
- Beta target encoding as distinct from standard target encoding (appears to be subsumed into the MEstimateEncoder and GLMMEncoder frameworks, not an independent named method)
