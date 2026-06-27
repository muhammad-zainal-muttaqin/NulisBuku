# Chapter 6 — Derived Feature Construction
## External Research Resources

**chapter:** ch06  
**title:** Pembentukan Fitur Turunan  
**generated:** 2026-06-27  
**sources fetched:** 16 searches / 14 fetch calls  
**tag legend:** [NEW] = post-2024 material not in current drafts; [REFRESH] = update/corroboration for existing content

---

## Subsections Targeted

| ID | Topic |
|----|-------|
| ch06_s01 | Ratios, differences, and interaction features |
| ch06_s02 | Polynomial features |
| ch06_s03 | Aggregations and group-based features |
| ch06_s04 | Relational & event-log features (joins, fan-out, point-in-time) — **NEW** |
| ch06_s05 | Domain-driven features |
| ch06_s06 | Date/time and cyclical features |
| ch06_s07 | The risk of feature explosion |
| ch06_s08 | Validating whether a new feature actually helps |
| ch06_s09 | Case study: derived features from transaction/health/education data |

---

## I. Core Libraries & Tools (by subsection relevance)

### 1. FeatureTools — Deep Feature Synthesis & Point-in-Time Correctness
- **Home:** <https://featuretools.alteryx.com/en/stable/> (v1.31.0)
- **Key pages:**
  - What is Featuretools? — DFS overview, EntitySet, multi-table feature generation: <https://featuretools.alteryx.com/en/stable/index.html>
  - Handling Time — cutoff_time argument, time_index, point-in-time filtering: <https://featuretools.alteryx.com/en/stable/getting_started/handling_time.html>
  - Feature Selection guide: <https://featuretools.alteryx.com/en/stable/guides/feature_selection.html>
  - Time Series guide: <https://featuretools.alteryx.com/en/stable/guides/time_series.html>
- **Relevance:** ch06_s04 (entity-level aggregation, cutoff_time for point-in-time correctness, fan-out avoidance); ch06_s09 (automated relational aggregation)
- **Tag:** [REFRESH] — reinforces existing ch06_s04 content on as-of joins and cutoff_time
- **Notable detail:** FeatureTools `cutoff_time` can be a DataFrame with per-row timestamps; `time_index` on DataFrames filters out future data automatically. `graph_feature()` and `describe_feature()` provide lineage transparency.

### 2. Feast — Point-in-Time Joins in Feature Stores
- **Home:** <https://docs.feast.dev/>
- **Key pages:**
  - Feature View concepts: <https://docs.feast.dev/getting-started/concepts/feature-view>
  - Point-in-Time Joins: <https://docs.feast.dev/getting-started/concepts/point-in-time-joins>
- **Relevance:** ch06_s04 (production-grade point-in-time joins, TTL for historical retrieval, entity-level feature definitions)
- **Tag:** [NEW] — Feast is not mentioned in any ch06 draft; its point-in-time join model is the production counterpart of ch06_s04's conceptual as-of join
- **Notable detail:** Feast's `get_historical_features()` scans backward from entity timestamps up to TTL. Schema validation (`enable_validation=True`) catches missing columns and type mismatches.

### 3. Tecton — Time-Travel & Feature Engineering Platform
- **Blog:** Point-in-Time Correctness: <https://www.tecton.ai/blog/point-in-time-correctness/>
- **Relevance:** ch06_s04 (industrial point-in-time guarantees, feature freshness, time-travel)
- **Tag:** [NEW] — industrial reference for why point-in-time correctness is a production requirement, not a theoretical nicety
- **Notable detail:** Tecton enforces strict "no future data" in both training and serving paths, with built-in time-travel for backtesting.

### 4. scikit-learn — PolynomialFeatures
- **Home:** <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html> (v1.9.0)
- **Relevance:** ch06_s02 (polynomial expansion, `interaction_only`, `include_bias`, combinatorial growth)
- **Tag:** [REFRESH] — draft already covers the concept well; this confirms current API parameters
- **Notable detail:** New `degree` can be a tuple `(min_degree, max_degree)` for bounded expansion. `interaction_only=True` avoids squared terms. Order 'F' is faster for dense data. Sparse output uses CSR with K-simplex optimization for degree ≤3.

### 5. tsfresh — Automated Time-Series Feature Extraction
- **Home:** <https://tsfresh.readthedocs.io/en/latest/>
- **Relevance:** ch06_s03 (aggregation over temporal windows), ch06_s07 (feature explosion → feature filtering), ch06_s09 (time-series domain features)
- **Tag:** [REFRESH] — draft covers general aggregation; tsfresh is the reference for systematic time-series derivation + filtering
- **Notable detail:** Extracts ~800 features per time series (statistical, spectral, entropy-based). Includes `tsfresh.feature_selection` for post-generation filtering using Benjamini-Hochberg or Bonferroni. Rolling extraction via `roll_time_series()`.

### 6. Feature-engine — Feature Creation & Selection Transformers
- **Home:** <https://feature-engine.trainindata.com/en/latest/> (v1.9.x+)
- **Relevance:** ch06_s01 (MathFeatures, RelativeFeatures), ch06_s06 (CyclicalFeatures, DatetimeFeatures), ch06_s07 (DropCorrelatedFeatures, SmartCorrelatedSelection)
- **Tag:** [NEW] — Feature-engine is not referenced in any ch06 draft; it provides scikit-learn-compatible transformers for exact operations covered in ch06
- **Notable detail:**
  - `MathFeatures` — sum, mean, product, std across variable groups (directly covers ch06_s01)
  - `RelativeFeatures` — subtract or divide variables by a reference (ratio/difference, ch06_s01)
  - `CyclicalFeatures` — sine/cosine encoding with drop_original option (ch06_s06)
  - `DecisionTreeFeatures` — tree-based interaction features (ch06_s01/s02 bridge)
  - `DropCorrelatedFeatures` — Pearson/Spearman/VIF-based dropping (ch06_s07)
  - `SmartCorrelatedSelection` — keeps best feature from correlated groups based on model performance (ch06_s07)
  - `SelectByShuffling` / `ProbeFeatureSelection` — validation-by-randomization (ch06_s08)
  - `WindowFeatures` / `ExpandingWindowFeatures` — temporal aggregation with decay options (ch06_s03/s04 bridge)

---

## II. Modern Aggregation & Recency Patterns

### 7. Recency-Weighted Event Aggregations
- **Concept:** Traditional group-based aggregations (mean, sum) treat all past events equally. Modern practice adds time-decay weighting:
  - **Exponential decay:** weight = e^(-λ * age), where λ controls decay rate; the half-life = ln(2)/λ
  - **Half-life features:** compute "purchases in last 30 days weighted by recency" where each purchase is weighted by e^(-age/7days)
  - **Decay-weighted mean:** Σ(value_i * w_i) / Σ(w_i) instead of plain mean
- **Relevance:** ch06_s03 (extends group-based aggregation with temporal dimension), ch06_s04 (event-log aggregation with recency)
- **Tag:** [NEW] — none of the ch06 drafts mention decay/recency weighting; drafts use plain aggregation only
- **Implementation notes:** Feature-engine's `ExpandingWindowFeatures` supports decay; pandas `ewm()` for exponential weighted moving operations

### 8. Sliding Window, Exponential Weighted, and Session-Based Aggregations
- **Sliding window:** fixed backward time window (e.g., "last 7 days") → count/sum/mean/std over that period
- **Expanding window:** cumulative from first observation to current time
- **Session-based reset:** aggregate within user sessions, resetting on inactivity threshold (e.g., 30-min gap)
- **Relevance:** ch06_s03 (window types), ch06_s04 (temporal aggregation over event logs)
- **Tag:** [NEW] — session-based reset is a distinct pattern not covered in drafts
- **Sources:** Feature-engine `WindowFeatures` and `ExpandingWindowFeatures`; pandas `rolling()`; tsfresh `roll_time_series()`

---

## III. LLM-Suggested & Automated Derived Features

### 9. CAAFE — LLM-Assisted Feature Engineering (Hollmann et al., 2023)
- **Paper:** "CAAFE: Context-Aware Automated Feature Engineering"
- **Concept:** Feed column names, types, and summary statistics (not raw data) to an LLM; LLM proposes derived features (ratios, interactions, aggregations); generated Python code is executed and validated on a downstream model
- **Relevance:** ch06_s01 (ratios/interactions — LLM can propose which pairs to combine), ch06_s08 (validation — CAAFE validates proposed features against model performance)
- **Tag:** [NEW] — LLM-driven feature proposal is not covered in any ch06 draft; forward-pointer to Ch 16 (automated FE)
- **Caveat from literature:** LLM-proposed features must be validated; "plausible but spurious" is a known failure mode (covered in Ch 16 s03)

### 10. Featuretools DFS as Automated Generation
- **Concept:** Deep Feature Synthesis (DFS) systematically applies primitives (transform + aggregation) across relational entity graph; generates features like `MEAN(transactions.amount)`, `STD(sessions.SUM(transactions.amount))`, etc.
- **Relevance:** ch06_s04 (ties group-by aggregation to automated synthesis), ch06_s07 (feature explosion from DFS — 75 features from 3 tables, 5 customers)
- **Tag:** [REFRESH] — draft mentions automated FE as forward-pointer to Ch 16; FeatureTools docs show exact combinatorial scale

---

## IV. Feature Explosion Mitigation — Post-Generation Selection

### 11. VIF-Based Trimming (Variance Inflation Factor)
- **Concept:** After generating many derived features, compute VIF = 1/(1-R²_i) for each feature where R²_i is from regressing feature_i on all other features. VIF > 5 (or > 10) indicates multicollinearity.
- **Relevance:** ch06_s07 (multicollinearity detection after combinatorial feature generation)
- **Tag:** [NEW] — drafts mention multicollinearity conceptually but don't mention VIF as a detection/trimming tool
- **Implementation:** `statsmodels.stats.outliers_influence.variance_inflation_factor`; Feature-engine's `DropCorrelatedFeatures` does pairwise but not VIF-based

### 12. Regularization-Aware Pruning
- **Concept:** Generate many features → fit L1-regularized model (Lasso, ElasticNet) → keep only features with non-zero coefficients. This naturally trims irrelevant derived features.
- **Relevance:** ch06_s07 (selection through regularization), ch06_s08 (empirical validation)
- **Tag:** [REFRESH] — drafts don't explicitly name this pattern, but it bridges ch06_s07 → Ch 7
- **Source:** scikit-learn `LassoCV`, `ElasticNetCV` with `SelectFromModel`

### 13. Featuretools Built-in Feature Selection
- **Concept:** Featuretools provides `ft.selection.remove_low_information_features()` and `ft.selection.remove_highly_correlated_features()` to prune DFS output
- **Relevance:** ch06_s07 (explosion mitigation after generation)
- **Tag:** [NEW] — library-specific mitigation tools not mentioned in drafts
- **Source:** <https://featuretools.alteryx.com/en/stable/guides/feature_selection.html>

### 14. Probe Feature Selection (Feature-engine)
- **Concept:** Append random noise variables (probes) to dataset; after model training, keep only features with importance greater than the best probe. This establishes an empirical noise floor.
- **Relevance:** ch06_s08 (empirical validation of feature utility)
- **Tag:** [NEW] — elegant validation method not mentioned in drafts
- **Source:** Feature-engine `ProbeFeatureSelection`

---

## V. Validation of Derived Features — Modern Methodology

### 15. SHAP-Based Feature Diagnosis
- **Concept:** SHAP values decompose individual predictions into feature contributions. For a newly derived feature: (a) check if its SHAP values are non-zero for a substantial fraction of samples, (b) compare SHAP contribution magnitude before vs. after adding the derived feature, (c) check if the derived feature "takes over" contribution from base features (redundancy signal).
- **Relevance:** ch06_s08 (validation beyond simple performance comparison)
- **Tag:** [NEW] — drafts describe baseline comparison with CV but don't mention SHAP for understanding *how* a derived feature helps
- **Source:** scikit-learn 1.9 `permutation_importance`; SHAP library (`shap.Explainer`)

### 16. Ablation Study Patterns for Derived Features
- **Concept:** Group derived features by type (ratios, polynomial, aggregations) and remove entire groups; measure degradation. This reveals which *category* of derivation matters, not just individual features.
- **Relevance:** ch06_s08 (structured validation beyond single-feature add/remove)
- **Tag:** [NEW] — draft mentions ablation conceptually but only at single-feature level; group ablation provides broader insight
- **Methodology:** Train baseline → add group G → measure ΔCV; repeat for all groups; report which groups improve and by how much (ties to Ch 9)

### 17. Gain Ratio / Information Gain Validation
- **Concept:** For classification tasks, compute information gain of each derived feature relative to each base feature it was built from. If a derived feature has lower IG than any of its sources, it's redundant.
- **Relevance:** ch06_s08 (pruning valueless derived features)
- **Tag:** [NEW] — specific IG-based validation not in drafts

---

## VI. Domain-Specific Derived Features — Modern Examples

### 18. Healthcare — APACHE/SOFA & Clinical Scoring
- **APACHE (Acute Physiology And Chronic Health Evaluation):** ICU severity score derived from 12 physiological measurements (temperature, MAP, heart rate, respiratory rate, sodium, potassium, creatinine, hematocrit, WBC, GCS, age, chronic health). Each component is binned and weighted.
- **SOFA (Sequential Organ Failure Assessment):** 6 organ systems scored 0–4 based on worst daily values; changes over time (delta SOFA) are more predictive than absolute scores.
- **Relevance:** ch06_s05 (domain-driven features — clinical indices as the purest form), ch06_s09 (health domain case study)
- **Tag:** [NEW] — drafts mention BMI only; APACHE/SOFA are sophisticated multi-component domain features
- **Modern direction:** MEOWS (Modified Early Obstetric Warning Score), qSOFA for quick screening — all are feature derivations from raw vitals

### 19. Finance — Technical Indicators & Risk Ratios
- **Modern technical indicators:** RSI (Relative Strength Index), MACD (Moving Average Convergence Divergence), Bollinger Bands, ATR (Average True Range) — all derived from OHLCV (open/high/low/close/volume) data
- **Risk ratios beyond basic:** debt-service coverage ratio (DSCR), interest coverage ratio, current ratio, quick ratio, Altman Z-score (bankruptcy prediction — linear combination of 5 financial ratios)
- **Relevance:** ch06_s05 (financial domain features), ch06_s09 (transaction finance case study)
- **Tag:** [NEW] — drafts mention only loan-to-value and debt-to-asset; modern finance uses dozens of derived ratios

### 20. Education / Learning Analytics
- **Modern session-based features:** time-on-task per learning module, number of attempts before correct answer, help-seeking frequency, inter-session interval (gaming the system detection), keystroke dynamics
- **Composite indices:** engagement score = f(login_frequency, time_on_platform, assignment_completion_rate, forum_participation)
- **Relevance:** ch06_s09 (education domain case study)
- **Tag:** [NEW] — drafts mention login streaks and assignment ratios only; modern learning analytics uses richer behavioral signals
- **Source:** Learning analytics literature (LAK conference); xAPI specification for event logging

### 21. RFM Extensions (Recency, Frequency, Monetary)
- **Classic RFM:** R = days since last event, F = count of events, M = sum of monetary value
- **Modern extensions:** RFMTC (adds Tenure and Churn), LRFMP (adds Length/Loyalty and Periodicity), weighted RFM (decay-weighted recency and monetary as described in #7 above)
- **Relevance:** ch06_s04 (event-log aggregation into entity features), ch06_s09 (transaction domain)
- **Tag:** [NEW] — RFM is the canonical event-log → entity feature pattern; not mentioned in drafts

---

## VII. Polynomial & Interaction Feature Selection — Advanced

### 22. Polynomial Chaos Expansions (PCE)
- **Concept:** Instead of brute-force all-degree expansion, PCE selects a sparse set of polynomial basis functions using orthogonal polynomials that are data-adapted. Used in uncertainty quantification (UQ) but applicable to feature selection.
- **Relevance:** ch06_s02 (polynomial features — alternative to full combinatorial expansion)
- **Tag:** [NEW] — provides a principled alternative to full PolynomialFeatures explosion

### 23. ANOVA Kernel / All-Pairs Interactions Selection
- **Concept:** For high-dimensional data, compute interaction strength using ANOVA decomposition; keep only interactions with significant F-statistic. scikit-learn's `f_classif` and `mutual_info_classif` can be used pairwise to screen interactions.
- **Relevance:** ch06_s02 (selecting which polynomial terms to generate), ch06_s07 (prevention over post-hoc pruning)
- **Tag:** [NEW] — drafts present polynomial expansion as all-or-nothing; screening before expansion is a modern practical pattern

---

## VIII. General Reference — Pipeline Discipline

### 24. Cutoff Time DataFrame (FeatureTools)
- **Concept:** Pass a DataFrame with `instance_id` and `time` columns to `ft.dfs(cutoff_time=df)`. Features computed per-row at each row's specific cutoff, preventing look-ahead.
- **Relevance:** ch06_s04 (point-in-time correctness — implements exactly what the draft describes)
- **Tag:** [REFRESH] — confirms draft's conceptual description with concrete API

### 25. Featuretools Feature Selection Module
- **Detail:** `remove_low_information_features()` drops features with zero or near-zero variance; `remove_highly_correlated_features()` drops one of each pair above threshold; `remove_single_value_features()` drops constant features.
- **Relevance:** ch06_s07 (mitigation tools after feature generation)
- **Tag:** [NEW] — specific library functions for explosion mitigation

---

## IX. Quick Reference: Resource-to-Subsection Mapping

| Resource # | Primary ch06_sXX | Tag |
|------------|-----------------|-----|
| 1 (FeatureTools DFS) | s04 | REFRESH |
| 2 (Feast PIT joins) | s04 | NEW |
| 3 (Tecton PIT) | s04 | NEW |
| 4 (sklearn Polynomial) | s02 | REFRESH |
| 5 (tsfresh) | s03, s07, s09 | REFRESH |
| 6 (Feature-engine) | s01, s03, s06, s07, s08 | NEW |
| 7 (Recency weighting) | s03, s04 | NEW |
| 8 (Window types) | s03, s04 | NEW |
| 9 (CAAFE LLM-FE) | s01, s08 | NEW |
| 10 (DFS scale) | s04, s07 | REFRESH |
| 11 (VIF trimming) | s07 | NEW |
| 12 (L1 pruning) | s07, s08 | REFRESH |
| 13 (FT selection) | s07 | NEW |
| 14 (Probe selection) | s08 | NEW |
| 15 (SHAP validation) | s08 | NEW |
| 16 (Group ablation) | s08 | NEW |
| 17 (Gain ratio) | s08 | NEW |
| 18 (APACHE/SOFA) | s05, s09 | NEW |
| 19 (Finance indicators) | s05, s09 | NEW |
| 20 (Education analytics) | s09 | NEW |
| 21 (RFM extensions) | s04, s09 | NEW |
| 22 (PCE) | s02 | NEW |
| 23 (ANOVA screen) | s02, s07 | NEW |

---

## X. Priority Ranking for Chapter Refresh

**High priority (should influence drafts):**
1. Recency-weighted & half-life aggregations (#7–8) — fills gap in s03/s04
2. Feast/Tecton point-in-time joins (#2–3) — production depth for s04
3. Feature-engine transformers (#6) — modern library reference for s01, s03, s06
4. VIF-based trimming (#11) — concrete tool for s07 explosion mitigation
5. Group-level ablation (#16) — methodology upgrade for s08 validation

**Medium priority (enrich but not restructure):**
6. CAAFE / LLM-FE (#9) — forward-pointer to Ch 16, enrichment for s01/s08
7. RFM extensions (#21) — canonical event-log pattern for s04/s09
8. SHAP diagnosis (#15) — modern validation enrichment for s08
9. APACHE/SOFA & finance indicators (#18–19) — domain depth for s05/s09
10. Probe feature selection (#14) — practical validation tool for s08

**Lower priority (academic enrichment):**
11. PCE & ANOVA screening (#22–23) — polynomial selection for s02
12. Gain ratio validation (#17) — supplementary for s08
13. Education analytics extensions (#20) — additional domain examples for s09
