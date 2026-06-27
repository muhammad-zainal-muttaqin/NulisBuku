# ch07 — Feature Selection
## Research Resources (Gathering Agent)

**Date:** 2026-06-27  
**Scope:** ch07_s01 – ch07_s06 (Relevance & redundancy; Filter; Wrapper; Embedded; Stability & nested validation; Case study)  
**Tags:** [NEW] = not in baseline book materials; [REFRESH] = update/verify existing coverage

---

## ch07_s01 — Relevance vs. Redundancy; The Curse of Dimensionality

### [REFRESH] scikit-learn: Feature Selection — User Guide §1.13
- **URL:** https://scikit-learn.org/stable/modules/feature_selection.html
- **What:** Canonical classification of filter/wrapper/embedded methods. Documents `VarianceThreshold`, `SelectKBest`, `SelectFromModel`, `RFE`/`RFECV`, `SequentialFeatureSelector`, and pipeline integration.
- **Relevance:** Foundational taxonomy and API patterns. The `Pipeline(clf)` example shows the correct way to embed selection inside a model pipeline to avoid leakage.

### [REFRESH] CrossValidated: "Feature Selection and Cross-Validation" (113 votes)
- **URL:** https://stats.stackexchange.com/questions/27750/feature-selection-and-cross-validation
- **What:** Seminal Q&A on why feature selection must happen *inside* the CV loop. Covers the "selection bias / overfitting" problem when selection precedes splitting.
- **Relevance:** Key conceptual underpinning for ch07_s05 (nested validation). Frequently cited in ML textbooks.

### [REFRESH] CrossValidated: "Variable selection for predictive modeling really needed in 2016?" (84 votes)
- **URL:** https://stats.stackexchange.com/questions/215154/
- **What:** Debate on whether modern compute + regularization makes explicit feature selection obsolete. Community answer: still needed for interpretability, cost, and production latency.
- **Relevance:** Motivates *why* Ch 7 exists in the era of deep learning and large compute.

### [REFRESH] CrossValidated: "Why is variable selection necessary?" (36 votes)
- **URL:** https://stats.stackexchange.com/questions/18214/
- **What:** Discusses theoretical pitfalls (bias, overfitting) of selection and why one might still do it.
- **Relevance:** Direct input for the "why select at all" argument in s01.

### [REFRESH] CrossValidated: "Feature selection for 'final' model when performing cross-validation" (95 votes)
- **URL:** https://stats.stackexchange.com/questions/2306/
- **What:** Practitioners wrestling with the tension between selection for final model vs. selection for evaluation. Emphasizes nested CV.
- **Relevance:** Bridge between s01 (why) and s05 (nested validation).

---

## ch07_s02 — Filter Methods

### [REFRESH] scikit-learn: Univariate Feature Selection (§1.13.2)
- **URL:** https://scikit-learn.org/stable/modules/feature_selection.html#univariate-feature-selection
- **What:** `SelectKBest`, `SelectPercentile`, `SelectFpr/Fdr/Fwe`; scoring functions: `f_classif`, `f_regression`, `chi2`, `mutual_info_classif`, `mutual_info_regression`. Notes on sparse data support.
- **Relevance:** Core reference for correlation-based, MI-based, and chi-square filters. Covers the F-test-vs-MI trade-off (linear dependency vs. any statistical dependency).

### [REFRESH] scikit-learn: Comparison of F-test and Mutual Information (example notebook)
- **URL:** https://scikit-learn.org/stable/auto_examples/feature_selection/plot_f_test_vs_mi.html
- **What:** Side-by-side comparison showing F-test captures only linear relationships while MI captures arbitrary dependencies.
- **Relevance:** Direct material for the filter-methods subsection. Visual example of the trade-off.

### [NEW] LightGBM: Features (conceptual overview)
- **URL:** https://lightgbm.readthedocs.io/en/latest/Features.html
- **What:** Histogram-based algorithm, leaf-wise tree growth, categorical feature handling. Describes gain-based split finding and the O(#bins) complexity advantage.
- **Relevance:** Provides context for why tree-based feature importance (used in embedded methods, s04) is fast and reliable — the histogram approach makes computing gain efficient.

### [REFRESH] CrossValidated: "How exactly does Chi-square feature selection work?" (23 votes)
- **URL:** https://stats.stackexchange.com/questions/24179/
- **What:** Clarifies that chi-square is computed per feature-class pair and then aggregated.
- **Relevance:** Pedagogical reference for explaining chi-square to readers.

---

## ch07_s03 — Wrapper Methods

### [REFRESH] scikit-learn: Recursive Feature Elimination (§1.13.3)
- **URL:** https://scikit-learn.org/stable/modules/feature_selection.html#recursive-feature-elimination
- **What:** `RFE` and `RFECV` (with cross-validation to auto-tune feature count). Uses `coef_` or `feature_importances_` from an external estimator. Recursively prunes least-important features.
- **Relevance:** Core wrapper method. `RFECV` example shows the auto-tuning pattern essential for s05.

### [REFRESH] scikit-learn: Sequential Feature Selection (§1.13.5)
- **URL:** https://scikit-learn.org/stable/modules/feature_selection.html#sequential-feature-selection
- **What:** Forward-SFS and Backward-SFS as model-agnostic wrappers (no `coef_`/`feature_importances_` required). Greedy, uses cross-validated scoring. Notes computational cost: backward selection from m→m−1 features requires m×k model fits.
- **Relevance:** Complements RFE; SFS is more general but slower. Direct material for s03.

### [REFRESH] MachineLearningMastery: "Feature Selection in Python with Scikit-Learn"
- **URL:** https://machinelearningmastery.com/feature-selection-in-python-with-scikit-learn/
- **What:** Practical tutorial covering RFE, ExtraTrees feature importance, and the difference between univariate stats (chi2) vs. wrapper approaches.
- **Relevance:** Classroom-friendly reference; clear distinction between filter and wrapper paradigms.

---

## ch07_s04 — Embedded Methods

### [REFRESH] scikit-learn: L1-based Feature Selection (§1.13.4.1)
- **URL:** https://scikit-learn.org/stable/modules/feature_selection.html#l1-based-feature-selection
- **What:** `SelectFromModel` + `Lasso`, `LogisticRegression`(penalty='l1'), `LinearSVC`(penalty='l1'). C parameter controls sparsity. Notes on L1 recovery theory (compressive sensing, BIC).
- **Relevance:** Core LASSO-based embedded method. The note on `LassoCV` potentially under-penalizing vs. `LassoLarsIC` being conservative is a teaching point.

### [REFRESH] scikit-learn: Tree-based Feature Selection (§1.13.4.2)
- **URL:** https://scikit-learn.org/stable/modules/feature_selection.html#tree-based-feature-selection
- **What:** `SelectFromModel` + `ExtraTreesClassifier`/`RandomForestClassifier`. Impurity-based importance (MDI). Warning: impurity importance is biased toward high-cardinality features.
- **Relevance:** Core tree-based embedded method. Direct link to caveat about MDI vs. permutation importance.

### [REFRESH] BorutaPy (scikit-learn-contrib)
- **URL:** https://github.com/scikit-learn-contrib/boruta_py
- **What:** Python implementation of Boruta "all-relevant" feature selection (Kursa & Rudnicki, 2010). Uses shadow features + Random Forest importance + statistical testing (Benjamini-Hochberg FDR + Bonferroni). Key distinction: finds *all* features carrying information, not a minimal-optimal subset. Supports perc (percentile threshold relaxation) and two-step correction. v0.4.3 (Aug 2024).
- **Relevance:** Primary embedded method beyond simple tree importance. The "all-relevant" vs. "minimal-optimal" distinction is a key pedagogical point for s04.

### [NEW] Featurewiz (AutoViML): MRMR-based Selection
- **URL:** https://github.com/AutoViML/featurewiz
- **What:** Uses Minimum Redundancy Maximum Relevance (MRMR) via SULOV (Searching for Uncorrelated List of Variables) + Recursive XGBoost. Two-stage: (1) SULOV removes mutually correlated features using Mutual Information Score; (2) Recursive XGBoost selects best features from remainder. v0.6+ (Jan 2025). Also integrates auto-encoders (VAE, DAE) for deep feature extraction.
- **Relevance:** Modern hybrid filter+embedded approach. MRMR is explicitly positioned vs. Boruta (featurewiz claims MRMR outperforms Boruta; provides smaller non-redundant set). The comparison between "all-relevant" (Boruta) and "minimal-redundancy" (MRMR) philosophies is valuable case-study material.

### [NEW] CatBoost: Feature Importance Types
- **URL:** https://catboost.ai/en/docs/concepts/fstr
- **What:** Four importance types: `PredictionValuesChange` (default, how much predictions change on average when feature changes), `LossFunctionChange` (difference in loss with/without feature, dataset-dependent), `InternalFeatureImportance` (raw internal calculation), `PredictionDiff` (impact on prediction differences for object pairs). Also handles feature combinations.
- **Relevance:** Shows how modern GBDT libraries go beyond single importance type. The `LossFunctionChange` variant (approximate retraining without feature) is a more principled alternative to simple gain importance.

### [REFRESH] CrossValidated: "Why does the Lasso provide Variable Selection?" (128 votes)
- **URL:** https://stats.stackexchange.com/questions/74542/
- **What:** Geometric explanation of LASSO's L1 penalty producing zero coefficients compared to ridge's L2.
- **Relevance:** Foundational intuition for embedded selection via regularized linear models.

### [REFRESH] CrossValidated: "What are disadvantages of using the lasso for variable selection for regression?" (101 votes)
- **URL:** https://stats.stackexchange.com/questions/7935/
- **What:** LASSO issues: correlated predictors pick one arbitrarily, p>n limitation (selects at most n variables), post-selection inference bias.
- **Relevance:** Critical caveats for the embedded-methods discussion.

### [REFRESH] CrossValidated: "Best approach for model selection: Bayesian or cross-validation?" (27 votes)
- **URL:** https://stats.stackexchange.com/questions/20729/
- **What:** Compares Bayesian model selection (marginal likelihood) vs. cross-validation for feature/model selection.
- **Relevance:** Alternative perspective on model-based selection.

---

## ch07_s05 — Selection Stability and Nested Validation

### [REFRESH] CrossValidated: "Should feature selection be performed only on training data (or all data)?" (28 votes)
- **URL:** https://stats.stackexchange.com/questions/64825/
- **What:** Core pipeline discipline: selection must be fit on training data only, then applied to test. References Guyon (2003) and Singhi & Liu (2006).
- **Relevance:** Directly addresses the selection-leakage concern. Essential for ch07_s05.

### [REFRESH] CrossValidated: "Model stability when dealing with large p, small n problem" (23 votes)
- **URL:** https://stats.stackexchange.com/questions/29580/
- **What:** Practical experience with model/selection instability when n=150, p=400. Elastic net preferred over LASSO alone.
- **Relevance:** Real-world example of selection instability — ties stability concerns directly to high-dimensional settings.

### [REFRESH] CrossValidated: "Variability in cv.glmnet results" (21 votes)
- **URL:** https://stats.stackexchange.com/questions/97777/
- **What:** cv.glmnet gives different selected features on different runs. Documents that LASSO selection can be highly unstable with correlated features and small samples.
- **Relevance:** Direct motivation for stability analysis and nested validation.

### [REFRESH] CrossValidated: "How should Feature Selection and Hyperparameter optimization be ordered?" (43 votes)
- **URL:** https://stats.stackexchange.com/questions/264533/
- **What:** Practical ordering of selection vs. hyperparameter tuning in a pipeline.
- **Relevance:** Addresses the pipeline architecture question that arises when combining selection with model tuning.

---

## ch07_s06 — Case Study: Comparing Selection Methods

### [REFRESH] scikit-learn: Model-based and Sequential Feature Selection (diabetes dataset example)
- **URL:** https://scikit-learn.org/stable/auto_examples/feature_selection/plot_select_from_model_diabetes.html
- **What:** Compares `SelectFromModel` (Lasso) vs. `SequentialFeatureSelector` on diabetes regression data. Shows which features each method selects.
- **Relevance:** Pre-built case-study template comparing embedded vs. wrapper approaches on a single dataset.

### [REFRESH] scikit-learn: Feature importances with a forest of trees
- **URL:** https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
- **What:** Synthetic data example showing recovery of meaningful features via impurity importance.
- **Relevance:** Demonstrates that tree-based importance can recover true signal features.

### [REFRESH] scikit-learn: Permutation Importance vs Random Forest Feature Importance (MDI)
- **URL:** https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance.html
- **What:** Compares impurity-based importance (MDI) with permutation importance. Shows MDI's bias toward high-cardinality features and how permutation importance corrects it.
- **Relevance:** Critical caveat for any case study that relies on tree-based embedded importance. Shows that "importance" is method-dependent.

### [NEW] Featurewiz vs. Boruta comparison (from Featurewiz docs)
- **URL:** https://github.com/AutoViML/featurewiz (see "Comparing featurewiz to Boruta" section)
- **What:** Explicit comparison: Boruta uses an "All-Relevant" approach (may include redundant correlated features); Featurewiz/MRMR uses a "Minimal Optimal" approach (removes redundancy via SULOV + MI). Featurewiz claims smaller, less redundant feature sets.
- **Relevance:** Direct head-to-head comparison useful for the case study narrative. The "all-relevant vs. minimal-optimal" trade-off is a core conceptual axis.

---

## Cross-Cutting Modern Topics (2024-2026)

### SHAP-Based Feature Selection

- **[NEW] SHAP Official Documentation**
  - **URL:** https://shap.readthedocs.io/en/latest/
  - **What:** SHAP (SHapley Additive exPlanations) computes game-theoretic feature attributions. Key for feature selection via `mean(|SHAP|)` as a filter criterion. TreeSHAP is optimized for tree models (XGBoost, LightGBM, CatBoost). Includes tabular, text, image, genomic examples. Also covers explainer types: Tree, Kernel, Deep, Gradient, Linear.
  - **Relevance:** SHAP is the modern bridge between embedded methods (feature importance) and model-agnostic attribution. `ShapRFECV` (third-party) combines SHAP with recursive elimination. This is the primary modern recency hook for Ch 7.
  - **Note for writer:** The SHAP docs include a cautionary note — "Be careful when interpreting predictive models in search of causal insights" — which is relevant to the ch09_s06 callout on importance ≠ causality, but also touches the Ch 7 discussion of what "relevance" really means.

### CatBoost SHAP Integration

- **[NEW] CatBoost ShapValues**
  - **URL:** https://catboost.ai/en/docs/concepts/shap-values
  - **What:** CatBoost natively computes `ShapValues` as part of its model analysis package. Can output SHAP values per object or aggregated.
  - **Relevance:** Shows that modern GBDT libraries now treat SHAP as a first-class output alongside traditional importance. This supports the pattern: train once → get both feature importance and SHAP for selection.

### Modern GBDT Importance Ecosystem

- **[NEW] XGBoost Python API (feature_importances_)**
  - **URL:** https://xgboost.readthedocs.io/en/stable/python/python_api.html
  - **What:** XGBoost provides `feature_importances_`, `get_score()` with `importance_type` parameter supporting: `weight` (number of times a feature is used in splits), `gain` (average gain of splits using the feature), `cover` (average coverage of splits), `total_gain`, `total_cover`.
  - **Relevance:** Multiple importance types from one model — each tells a different story. `gain` ≈ `feature_importances_` in sklearn. `weight` can be misleading (counts splits, not impact). The existence of multiple types is itself a pedagogical point: "importance" is not a single number.

### Causal Feature Selection (Forward-Looking)

- **[NEW] Concept reference: Markov Blanket Feature Selection**
  - **Source:** Established literature (Aliferis et al., Koller & Friedman). Not a single web resource, but well-documented in the causal ML community.
  - **What:** The Markov blanket of the target variable is the minimal set of features that renders all other features conditionally independent of the target. Causal discovery algorithms (PC, FCI, LiNGAM) can identify this set under assumptions.
  - **Relevance:** Advanced forward-looking note. Causal feature selection is theoretically motivated: if you select the Markov blanket, no other feature adds predictive information. This connects to the relevance-vs-redundancy framing in s01 and the "importance ≠ causality" callout in ch09_s06.
  - **Note for writer:** Brief mention only — this is an advanced topic that can be a forward-pointer to further reading. Not a core subsection.

### Stability Selection (Subsampling-Based Consensus)

- **[NEW] Concept reference: Stability Selection (Meinshausen & Buhlmann, 2010)**
  - **Source:** Established statistical literature. Frequently reimplemented in scikit-learn-contrib and modern AutoML libraries.
  - **What:** Run LASSO (or other selection) on many bootstrap subsamples; keep features selected consistently across subsamples above a threshold. Also: Randomized LASSO, stability paths.
  - **Relevance:** Directly addresses the stability concerns in s05. Modern implementations (stability-selection package on PyPI) provide sklearn-compatible estimators. This connects subsampling, ensemble thinking, and selection stability.

### AutoML-Integrated Selection

- **[NEW] Concept reference: AutoML Feature Selection (AutoGluon, FLAML, Optuna)**
  - **Source:** AutoGluon docs (https://auto.gluon.ai), FLAML docs (https://microsoft.github.io/FLAML/), Optuna docs (https://optuna.org).
  - **What:** AutoGluon's `TabularPredictor` performs automatic feature preprocessing and selection as part of its model ensemble. FLAML performs feature selection via `tune_feature` space in its search. Optuna can optimize which features to include as a hyperparameter.
  - **Relevance:** Modern AutoML systems embed feature selection as a component of their search. This shifts the practitioner question from "which method?" to "how do I configure the search?" Mention as a forward-pointer to Ch 16 (Automated Feature Engineering).

---

## Taxonomy and Terminology References

### [REFRESH] Wikipedia: Feature Selection
- **URL:** https://en.wikipedia.org/wiki/Feature_selection
- **What:** Canonical definitions: filter, wrapper, embedded, hybrid methods. Covers relevance, redundancy, subset search strategies.
- **Relevance:** Reference for terminology consistency.

### [REFRESH] Wikipedia: Minimum Redundancy Feature Selection (MRMR)
- **URL:** https://en.wikipedia.org/wiki/Minimum_redundancy_feature_selection
- **What:** MRMR algorithm (Peng et al., 2005). Selects features that are maximally relevant to the target and minimally redundant with each other. Wikipedia cites MRMR as "more powerful than other feature selection algorithms such as Boruta."
- **Relevance:** Direct coverage of the relevance-vs-redundancy trade-off that gives Chapter 7 its opening theme.

---

## Summary Table: Method ↔ Source Mapping

| Method Family | Primary Source | Alternative/Modern |
|---|---|---|
| Variance threshold | `sklearn.VarianceThreshold` | — |
| Univariate filter (corr, chi2) | `sklearn.SelectKBest` + `f_classif`/`chi2` | — |
| Mutual information filter | `sklearn.mutual_info_classif`/`_regression` | MRMR (featurewiz) |
| RFE | `sklearn.RFE`/`RFECV` | ShapRFECV (SHAP-based) |
| Sequential (forward/backward) | `sklearn.SequentialFeatureSelector` | — |
| LASSO (L1) | `sklearn.Lasso` + `SelectFromModel` | Elastic Net |
| Tree-based importance | `sklearn.RandomForestClassifier.feature_importances_` | XGBoost `gain`/`weight`/`cover` |
| Boruta (all-relevant) | `boruta.BorutaPy` | CatBoost `LossFunctionChange` |
| MRMR (minimal-redundancy) | `featurewiz` (SULOV + Recursive XGBoost) | — |
| SHAP-based selection | `shap.Explainer` → `mean(|SHAP|)` filter | ShapRFECV |
| Causal (Markov blanket) | PC algorithm, LiNGAM, FCI | Advanced/future reading |

---

## Notes for the Compiler/Writer

1. **The SHAP recency hook is strong.** Consider mentioning `mean(|SHAP|)` as a modern filter criterion in ch07_s02 and linking to ShapRFECV in ch07_s03. The BorutaPy library itself can be wrapped around any sklearn ensemble; combined with SHAP this creates BorutaShap (a popular community pattern).
2. **The "all-relevant" vs. "minimal-optimal" distinction** (Boruta vs. MRMR) is a rich conceptual axis for the case study (s06) and could anchor the opening motivation (s01).
3. **GBDT importance types** (XGBoost: weight/gain/cover; CatBoost: PredictionValuesChange/LossFunctionChange; LightGBM: gain) — a comparative table would help readers understand why the same model can give different "importance" rankings depending on which metric is queried.
4. **Selection stability** has direct empirical backing from the CrossValidated Q&As (cv.glmnet variability, large-p-small-n instability). These are concrete examples to use in s05.
5. **Nested validation** is already well-covered in scikit-learn docs and CrossValidated (questions 27750, 2306, 64825). The pipeline-in-CV pattern from scikit-learn §1.13.6 is the canonical implementation reference.
6. **No drafts or briefs existed** for any ch07_s* subsection at research time — this file serves as the primary external-source foundation.
