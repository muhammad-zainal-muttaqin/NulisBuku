---
chapter: ch03
title: Numeric Feature Representation
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 3 Resources — Numeric Feature Representation

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence).

## Coverage baseline (what the drafts already have)
- ch03_s01 draft: Scale and distribution problems — large-range features dominate distance math, skewed distributions violate model assumptions
- ch03_s02 draft: Standardization (zero-mean, unit-variance) and min-max scaling (compress to [0,1]); when each fits (linear/regularized models → standardization; NNs/pixels → min-max); outlier sensitivity of min-max
- ch03_s03 draft: Robust scaling via median + IQR replacement; CEO salary example demonstrating mean/σ breakdown from outliers; median/IQR bypasses extremes
- ch03_s04 draft: Power transforms (log, Box-Cox, Yeo-Johnson) for skew; quantile transforms (rank-based, forces distribution shape) for extreme outliers; distortion vs. stabilization trade-off
- ch03_s05 draft: Clipping (capping extreme values at fixed bounds) and binning/discretization (converting continuous to categorical buckets); binning introduces non-linearity for linear models at cost of detail
- ch03_s06 draft: Distance-based and gradient-based models (k-NN, SVM, NNs, linear) are scale-sensitive; tree-based models (Decision Trees, Random Forest, GBM) are scale-insensitive (split on thresholds only)
- ch03_s07 draft: Case study — k-NN/SVM accuracy plummets on raw unscaled data, jumps after standardization; Random Forest accuracy identical either way
- Briefs: all briefs align; no [NEW] callouts flagged for recency layer

---

## Resources by subsection

### ch03_s01 — Scale and distribution: why numeric features need transforming
- **scikit-learn 1.9: "If a feature has a variance that is orders of magnitude larger than others, it might dominate the objective function"** [REFRESH] (confidence: verified)
  - Summary: The official preprocessing guide states the canonical justification: features with large variance dominate learning objectives, making estimators unable to learn from other features. Also covers the "Gaussian with zero mean and unit variance" assumption common to many estimators.
  - Why relevant: This is the definitive statement of the problem ch03_s01 describes — it directly supports the draft's argument about salary (10M) vs. age (50) scale dominance.
  - Source: https://scikit-learn.org/stable/modules/preprocessing.html · type: docs (official) · date: v1.9.0 (June 2026)

- **scikit-learn 1.9 example: "Many estimators are designed with the assumption that each feature takes values close to zero or more importantly that all features vary on comparable scales"** [REFRESH] (confidence: verified)
  - Summary: The scaling comparison example's opening text articulates the two-fold problem: metric-based and gradient-based estimators assume comparable feature scales; unscaled data can "slow down or even prevent convergence."
  - Why relevant: Reinforces the draft's dual framing (scale problem + distribution problem) with authority from the official example gallery.
  - Source: https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html · type: docs (official example) · date: v1.9.0 (June 2026)

### ch03_s02 — Standardization and min-max scaling
- **scikit-learn 1.9: StandardScaler and MinMaxScaler API — no breaking API changes; sparse handling notes** [REFRESH] (confidence: verified)
  - Summary: StandardScaler centers to zero mean and unit variance; MinMaxScaler compresses to [0,1] via (X - min)/(max - min); MaxAbsScaler for [-1,1] range. Important pipeline note: all scalers must be fit on training data only, then used via transform on test data. Sparse data recommendations: MaxAbsScaler preferred; StandardScaler acceptable only with with_mean=False.
  - Why relevant: Confirms the 1.9 API is stable for these workhorses; the sparse-handling notes and pipeline contract are valuable reinforcement for ch03_s02's positioning of these as the "two workhorses."
  - Source: https://scikit-learn.org/stable/modules/preprocessing.html#standardization-or-mean-removal-and-variance-scaling · type: docs (official) · date: v1.9.0 (June 2026)

### ch03_s03 — Robust scaling
- **scikit-learn 1.9: RobustScaler confirmed as a drop-in replacement when outliers are present; centering/scaling based on percentiles** [REFRESH] (confidence: verified)
  - Summary: The official docs state RobustScaler uses "more robust estimates for the center and range" via percentiles. The scaling comparison example demonstrates that unlike StandardScaler/MinMaxScaler, RobustScaler produces "approximately similar" ranges across features even with outliers, with most transformed values in [-2, 3]. Crucially, "the outliers themselves are still present in the transformed data" — they are not collapsed, only the scale is robust.
  - Why relevant: Direct documentation confirmation of ch03_s03's core argument (median/IQR replace mean/σ). Adds a nuanced point the draft could incorporate: RobustScaler preserves outlier positions rather than eliminating them, unlike QuantileTransformer which collapses outliers.
  - Source: https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html · type: docs (official example) · date: v1.9.0 (June 2026)

- **Feature-engine Winsorizer: Four capping methods beyond IQR — Gaussian, IQR, MAD, and Percentile** [NEW] (confidence: verified)
  - Summary: Feature-engine's Winsorizer offers `capping_method` options: 'gaussian' (mean ± fold×std), 'iqr' (Q75 + fold×IQR, Q25 − fold×IQR), 'mad' (median ± fold×MAD, recommended fold=3.29), and 'quantiles' (percentile-based caps). MAD-based method uses median absolute deviation — more robust than IQR for heavily contaminated distributions. Each method provides optional indicator variables for flagged outliers. The `fold` parameter controls sensitivity (auto: 3.0 gaussian, 1.5 IQR, 3.29 MAD).
  - Why relevant: Goes well beyond what the ch03 draft covers (it only discusses median/IQR robust scaling). MAD-based capping is a modern robust technique with strong statistical grounding (Rousseeuw & Croux, 1993; Leys et al., 2013). The Winsorizer's multi-method API and the indicator-flagging feature are practical extensions the book should reference.
  - Source: https://feature-engine.trainindata.com/en/latest/api_doc/outliers/Winsorizer.html · type: docs (open-source library) · date: feature-engine v1.9+ (2025–2026)

### ch03_s04 — Power and quantile transforms
- **scikit-learn 1.9 PowerTransformer: Yeo-Johnson and Box-Cox with λ via maximum likelihood; 1.9 change to use scipy.stats.yeojohnson** [REFRESH] (confidence: verified)
  - Summary: PowerTransformer supports Box-Cox (strictly positive data) and Yeo-Johnson (positive or negative). The optimal λ is estimated per feature via MLE. By default, applies zero-mean, unit-variance normalization after transformation. The map-to-normal example shows effectiveness: Yeo-Johnson works on lognormal, chi-squared, and Weibull; Box-Cox slightly better on positive-only distributions; QuantileTransformer (non-parametric) forces any distribution to normal given enough samples but is harder to interpret and can overfit on small datasets ("less than a few hundred points"). Important 1.9 change: PowerTransformer with method="yeo-johnson" now uses scipy.stats.yeojohnson for numerical stability (#33272).
  - Why relevant: Updates the book's Yeo-Johnson and Box-Cox coverage with the 1.9 stability improvement. The small-dataset warning for QuantileTransformer vs. PowerTransformer is a practical decision rule the draft could incorporate.
  - Source: https://scikit-learn.org/stable/auto_examples/preprocessing/plot_map_data_to_normal.html · type: docs (official example) · date: v1.9.0 (June 2026)

- **Feature-engine YeoJohnsonTransformer: Wrapper around scipy.stats.yeojohnson with per-variable λ dictionary** [REFRESH] (confidence: verified)
  - Summary: Feature-engine's YeoJohnsonTransformer provides a DataFrame-friendly wrapper with automatic numerical variable detection, per-variable λ storage (`lambda_dict_`), and inverse_transform support. Unlike scikit-learn's PowerTransformer which is array-based, this returns DataFrames and allows variable selection within the transformer.
  - Why relevant: Offers a more user-friendly alternative path for readers using DataFrames. The inverse_transform feature is useful for interpretability.
  - Source: https://feature-engine.trainindata.com/en/latest/api_doc/transformation/YeoJohnsonTransformer.html · type: docs (open-source library) · date: feature-engine v1.9+ (2025–2026)

- **scikit-learn 1.9 QuantileTransformer: subsample parameter, sparse support via ignore_implicit_zeros** [REFRESH] (confidence: verified)
  - Summary: QuantileTransformer maps features to uniform or normal distributions via rank transformation G⁻¹(F(X)). Key parameters: n_quantiles (default 1000), subsample (default 10k, None to disable since v1.5), ignore_implicit_zeros for sparse matrices. Non-linear transformation — "may distort linear correlations between variables measured at the same scale but renders variables measured at different scales more directly comparable."
  - Why relevant: The subsample parameter (added v1.5) and the explicit documentation of the correlation-distortion trade-off are newer practical details beyond what the draft covers.
  - Source: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html · type: docs (official) · date: v1.9.0 (June 2026)

### ch03_s05 — Clipping and binning
- **scikit-learn 1.9 KBinsDiscretizer: Three strategies (uniform, quantile, kmeans) with onehot/ordinal encoding** [REFRESH] (confidence: verified)
  - Summary: KBinsDiscretizer bins continuous features into k bins. Three strategies: 'uniform' (constant-width), 'quantile' (equal-frequency via quantiles), 'kmeans' (clustering-based). Output encoding: 'onehot' (sparse default), 'ordinal', or 'onehot-dense'. The discretization example demonstrates a key insight: after discretization, linear regression and decision tree make "exactly the same prediction" because "features are constant within each bin." Discretization makes linear models more flexible but adds no benefit for tree-based models.
  - Why relevant: The three-strategy taxonomy (uniform/quantile/kmeans) goes beyond the draft's simple binning discussion. The "linear model becomes more flexible, tree becomes less flexible" insight is a powerful trade-off illustration the draft could incorporate.
  - Source: https://scikit-learn.org/stable/auto_examples/preprocessing/plot_discretization.html · type: docs (official example) · date: v1.9.0 (June 2026)

- **Feature-engine DecisionTreeDiscretiser: Supervised discretization using decision trees (KDD 2009 competition approach)** [NEW] (confidence: verified)
  - Summary: Trains a decision tree per variable, then replaces values with tree predictions, bin number, or bin boundaries. Uses cross-validated grid search to tune tree depth (param_grid defaults to max_depth ∈ [1,2,3,4]). Scoring metric is configurable (e.g., 'neg_mean_squared_error' for regression, 'f1' for classification). Inspired by the KDD Cup 2009 winners (Niculescu-Mizil et al.). More sophisticated than unsupervised equal-width/frequency binning — bins are data-driven and supervised.
  - Why relevant: Supervised discretization is a modern binning approach absent from the draft. Tree-based binning produces non-uniform splits optimized for predictive power, representing a significant upgrade over the equal-width/equal-frequency methods covered in ch03_s05.
  - Source: https://feature-engine.trainindata.com/en/latest/api_doc/discretisation/DecisionTreeDiscretiser.html · type: docs (open-source library) · date: feature-engine v1.9+ (2025–2026)

- **scikit-learn 1.9 SplineTransformer: Piecewise polynomial alternative to binning** [NEW] (confidence: verified)
  - Summary: SplineTransformer generates B-spline basis functions — piecewise polynomials of fixed low degree (default cubic) that offer advantages over pure polynomial features: robust at boundaries (no Runge's phenomenon), good extrapolation, and a banded feature matrix with low condition number. Unlike KBinsDiscretizer (hard bin edges), splines are smooth and continuous.
  - Why relevant: A modern alternative to binning that preserves continuity while introducing non-linearity — addresses the "binning destroys fine-grained information" trade-off discussed in ch03_s05.
  - Source: https://scikit-learn.org/stable/modules/preprocessing.html#spline-transformer · type: docs (official) · date: v1.9.0 (June 2026)

### ch03_s06 — Which models are sensitive vs. insensitive to scale
- **scikit-learn 1.9 example: Official taxonomy — "metric-based and gradient-based estimators assume standardized data; decision tree-based estimators are robust to arbitrary scaling"** [REFRESH] (confidence: verified)
  - Summary: The scaling comparison example explicitly classifies models into scale-sensitive (metric-based: k-NN, SVM with RBF kernel; gradient-based: linear models, neural networks) vs. scale-insensitive (tree-based: Decision Trees, Random Forests, Gradient Boosting). Reinforces that unscaled data can degrade performance and prevent convergence for gradient-based estimators.
  - Why relevant: This is the authoritative, canonical taxonomy from the library maintainers — perfectly aligns with ch03_s06's scope and provides the exact language for the model-family decision lens.
  - Source: https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html · type: docs (official example) · date: v1.9.0 (June 2026)

- **LightGBM 4.x: Histogram-based binning confirms scale insensitivity — continuous features bucketed into discrete bins** [REFRESH] (confidence: verified)
  - Summary: LightGBM uses histogram-based algorithms that "bucket continuous feature values into discrete bins." Since the algorithm operates on binned values (#bins, not raw feature magnitudes), it is inherently scale-invariant. Leaf-wise tree growth further confirms the split-on-ordinal-threshold property that makes tree-based methods immune to scaling.
  - Why relevant: Provides a technical explanation for *why* modern gradient boosting is scale-insensitive (histogram binning), beyond just "trees split on thresholds." Useful for ch03_s06's deeper explanation.
  - Source: https://lightgbm.readthedocs.io/en/latest/Features.html · type: docs (official) · date: LightGBM 4.x (2024–2025)

- **CatBoost 1.x: No special feature preprocessing required — quantizes numerical features internally** [REFRESH] (confidence: verified)
  - Summary: CatBoost performs its own "preliminary calculation of splits" and internal quantization of numerical features as part of the training algorithm. It handles categorical and text features natively, requiring no external scaling, encoding, or discretization. This confirms that all modern GBDT libraries (XGBoost 2.x, LightGBM 4.x, CatBoost 1.x) remain fully scale-insensitive.
  - Why relevant: Closes the loop on tree-based model families — confirms that the scale-insensitivity property holds across all three major GBDT implementations, not just a theoretical property of decision trees.
  - Source: https://catboost.ai/en/docs/concepts/algorithm-main-stages · type: docs (official) · date: CatBoost 1.x (2025–2026)

### ch03_s07 — Case study: transformation effects on k-NN, SVM, tree-based
- **scikit-learn 1.9 example: California Housing — StandardScaler vs. MinMaxScaler vs. RobustScaler vs. PowerTransformer vs. QuantileTransformer on data with outliers** [NEW] (confidence: verified)
  - Summary: This example provides a complete comparative visualization of all major scalers on the California Housing dataset's MedInc and AveOccup features. Key empirical observations: (1) StandardScaler "cannot guarantee balanced feature scales in the presence of outliers" — data on one feature squeezed into [-0.2, 0.2] while another spans [-2, 4]; (2) MinMaxScaler "compresses all inliers into the narrow range [0, 0.005]" when outliers exist; (3) RobustScaler produces "approximately similar" ranges across features (both in [-2, 3]); (4) QuantileTransformer (uniform) maps everything including outliers to [0, 1], collapsing outliers and inliers together.
  - Why relevant: Provides a richer, more nuanced empirical comparison than ch03_s07's current k-NN vs. SVM vs. RF framing. Could be referenced as a more complete experiment showing *which* scaling method works best when outliers are present, not just "scale vs. don't scale."
  - Source: https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html · type: docs (official example) · date: v1.9.0 (June 2026)

- **scikit-learn 1.9: PowerTransformer (Box-Cox vs. Yeo-Johnson) vs. QuantileTransformer — distribution-level comparison across six distributions** [NEW] (confidence: verified)
  - Summary: The map-to-normal example compares Box-Cox, Yeo-Johnson, and QuantileTransformer on six distributions: Lognormal, Chi-squared, Weibull, Gaussian, Uniform, and Bimodal. Results: (1) Box-Cox slightly outperforms Yeo-Johnson on positive-only distributions; (2) QuantileTransformer is "harder to interpret" but "can force any arbitrary distribution into a Gaussian" with enough samples (thousands); (3) on small datasets (< few hundred points), "the quantile transformer is prone to overfitting" and power transforms are recommended.
  - Why relevant: Extends ch03_s07's model-sensitivity case study into a distribution-shape case study — showing that the choice between PowerTransformer and QuantileTransformer depends on dataset size and interpretability requirements, not just model family.
  - Source: https://scikit-learn.org/stable/auto_examples/preprocessing/plot_map_data_to_normal.html · type: docs (official example) · date: v1.9.0 (June 2026)

---

## Recency hooks not yet in drafts (topics for potential new subsections or enrichment)

> These are topics surfaced by the 2024–2026 landscape that are absent from the current draft/brief structure. The compiler may choose to weave them in or flag them for a future recency layer.

| Topic | Relevance | Source |
|---|---|---|
| **MAD-based robust scaling** (median absolute deviation) | More robust than IQR for heavy contamination; featured in Feature-engine Winsorizer as `capping_method='mad'` with fold=3.29 (MAD * 3.29 ≈ 3σ for Gaussian). Leys et al. (2013) recommend MAD over SD for outlier detection. | Feature-engine Winsorizer docs + Rousseeuw & Croux (1993) |
| **Supervised discretization via decision trees** | Feature-engine DecisionTreeDiscretiser trains a tree per variable, uses predictions as bin values. Produces data-optimal splits unlike equal-width/frequency. KDD Cup 2009 winning approach. | Feature-engine DecisionTreeDiscretiser docs |
| **SplineTransformer as smooth alternative to binning** | B-splines preserve continuity while introducing non-linearity — avoids the "hard bin edge" problem of KBinsDiscretizer. scikit-learn 1.9 includes this as a preprocessing option. | scikit-learn 1.9 preprocessing page |
| **GBDT internal quantization (LightGBM/CatBoost)** | LightGBM histogram-bins features internally; CatBoost quantizes during training. Both confirm scale invariance through internal discretization, not just split logic. | LightGBM Features page; CatBoost docs |
| **PowerTransformer 1.9 stability improvement** | scikit-learn 1.9 switched Yeo-Johnson to `scipy.stats.yeojohnson` for numerical stability (#33272). Relevant if the book ships code examples. | scikit-learn 1.9 release notes |
| **QuantileTransformer subsample parameter** | Added in scikit-learn 1.5, the `subsample` parameter (default 10k) controls the number of samples used for quantile estimation, enabling use on datasets too large for the full quantile computation. | scikit-learn QuantileTransformer docs |
| **Feature-engine DataFrame-native API** | Unlike scikit-learn's array-based approach, Feature-engine transformers work on DataFrames with in-transformer variable selection, preserving column names and returning DataFrames — no ColumnTransformer needed. | Feature-engine homepage |

---

## Source index

| # | URL | Type | Date |
|---|---|---|---|
| 1 | https://scikit-learn.org/stable/modules/preprocessing.html | official docs | v1.9.0 (Jun 2026) |
| 2 | https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html | official example | v1.9.0 (Jun 2026) |
| 3 | https://scikit-learn.org/stable/auto_examples/preprocessing/plot_map_data_to_normal.html | official example | v1.9.0 (Jun 2026) |
| 4 | https://scikit-learn.org/stable/auto_examples/preprocessing/plot_discretization.html | official example | v1.9.0 (Jun 2026) |
| 5 | https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PowerTransformer.html | official API ref | v1.9.0 (Jun 2026) |
| 6 | https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html | official API ref | v1.9.0 (Jun 2026) |
| 7 | https://scikit-learn.org/stable/whats_new/v1.9.html | official release notes | v1.9.0 (Jun 2026) |
| 8 | https://feature-engine.trainindata.com/en/latest/ | library docs | v1.9+ (2025–2026) |
| 9 | https://feature-engine.trainindata.com/en/latest/api_doc/outliers/Winsorizer.html | library API docs | v1.9+ (2025–2026) |
| 10 | https://feature-engine.trainindata.com/en/latest/api_doc/transformation/YeoJohnsonTransformer.html | library API docs | v1.9+ (2025–2026) |
| 11 | https://feature-engine.trainindata.com/en/latest/api_doc/discretisation/DecisionTreeDiscretiser.html | library API docs | v1.9+ (2025–2026) |
| 12 | https://lightgbm.readthedocs.io/en/latest/Features.html | official docs | LightGBM 4.x (2024–2025) |
| 13 | https://catboost.ai/en/docs/concepts/algorithm-main-stages | official docs | CatBoost 1.x (2025–2026) |
