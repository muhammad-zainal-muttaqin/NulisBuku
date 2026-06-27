---
chapter: ch05
title: Missing Values & Outliers (Reproducible, Pipeline-Based)
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 5 Resources — Missing Values & Outliers

> External material gathered 2026-06-27. Tagging: [NEW] = absent from current drafts · [REFRESH] = newer/better source for a topic the draft already covers. Each item carries provenance (source · type · date · confidence). Confidence = "verified" when the claim was read off the source actually fetched; "uncertain" when it rests on a search snippet only or a number that disagreed across versions.

## Coverage baseline (what the drafts already have)
- **s01** MCAR/MAR/MNAR defined conceptually with examples (sensor glitch / weight-by-gender / income self-censoring); inspection precedes automation. Deliberately excludes Little's test and Rubin's theory (per brief).
- **s02** Imputation = a fitted transformer; fit on train only; fit/transform contract; leakage from computing statistics before split. No tool/API names, no CV-fold subtlety.
- **s03** Simple (mean/median/mode) → model-based (KNN, iterative/MICE round-robin) → one paragraph naming MIWAE and "diffusion models" generically as modern/expensive. No specific modern method, numbers, or library.
- **s04** Missing-indicator as binary signal feature; strongest under MNAR; don't indicate purely-random columns. No API names (sklearn `MissingIndicator` / Feature-engine `AddMissingIndicator`).
- **s05** Outlier detection vs handling as two decisions; names IQR, std-dev threshold, isolation forest; domain judgment (age=150 error vs whale/fraud transaction). Brief explicitly keeps LOF etc. out.
- **s06** Robust handling: capping/winsorizing (1st/99th pct), robust scaling (median + IQR), log/power transform. No MAD/modified-z, no Feature-engine `Winsorizer` capping methods.
- **s07** Cleaning (fact correction, static/global) vs FE (representation, fit-on-train, leakage-bound). Positioning/scoping subsection.
- **s08** Case study: indicator → model-based imputer → capping(95th) → robust scaler in one Pipeline, fit on train only. Placeholder for signature snippet.

---

## Resources by subsection

### ch05_s01 — Missingness mechanisms (MCAR/MAR/MNAR)

- **MissMecha — Python package for studying/generating/diagnosing missingness mechanisms**  [NEW]  (confidence: verified)
  - Summary: All-in-one package (Aug 2025) to *generate* MCAR/MAR/MNAR for experiments and *diagnose* mechanism in real data. Its visual module extends `missingno` with type-aware plots and a "nullity correlation" analysis — pairwise correlation between binary missingness masks — to surface candidate MAR/MNAR structure.
  - Why relevant: the draft asserts "inspection precedes automation" but names no concrete tooling; this gives a modern, citeable instrument for the inspection step (and a teaching tool for the three mechanisms).
  - Source: https://arxiv.org/abs/2508.04740 · type: paper · date: 2025-08 · 
- **`missingno` + Little's MCAR test (`missdat` / `pyampute`)**  [NEW]  (confidence: uncertain)
  - Summary: `missingno` gives nullity matrix / heatmap / dendrogram to *see* missingness structure; Little's MCAR test (chi-square over deviations of group means) gives a statistical check of the MCAR assumption, exposed in Python via the `missdat` package's `mcar_test`.
  - Why relevant: concrete diagnostics named for s01 without violating the "no Rubin proofs / keep intuitive" exclusion — a test you *run*, not derive. Mention as optional sanity check, with the honest caveat that failing-to-reject MCAR is weak evidence.
  - Source: https://github.com/ResidentMario/missingno · type: docs/blog · date: 2018 (lib); test guides 2024 · 
- **MNAR is the case where the missingness *location itself* is the model target (forward hook to not-MIWAE / missing-indicator)**  [REFRESH]  (confidence: verified)
  - Summary: Modern deep imputers (not-MIWAE) make the s01 point operational — when missingness depends on the unobserved value (self-censoring), you must *model the missingness process*, not just impute around it.
  - Why relevant: strengthens the s01→s04 bridge (MNAR ⇒ indicator carries signal) with a current reference.
  - Source: https://arxiv.org/abs/2006.12871 · type: paper · date: 2021-03 (ICLR 2021) · 

### ch05_s02 — Imputation as a pipeline component

- **scikit-learn imputation API as it actually stands in 1.9 (the leakage-safe primitives)**  [REFRESH]  (confidence: verified)
  - Summary: `SimpleImputer`, `KNNImputer`, `MissingIndicator` are stable; **`IterativeImputer` is still flagged EXPERIMENTAL** and needs `from sklearn.experimental import enable_iterative_imputer`. Both `SimpleImputer` and `IterativeImputer` take `add_indicator=True` to stack a missing-mask; `keep_empty_features=True` stops imputers silently dropping all-NaN columns. All of these are `fit`/`transform` objects → they belong inside a `Pipeline`, which is exactly the draft's thesis.
  - Why relevant: gives the draft current, version-anchored API facts (the "experimental" flag is the kind of detail readers hit in practice).
  - Source: https://scikit-learn.org/stable/modules/impute.html · type: docs · date: 1.9.0 (2026) · 
- **"When to Impute? Imputation before vs during cross-validation" — a principled nuance to the strict rule**  [NEW]  (confidence: verified)
  - Summary: Jaeger, Tierney & Simon find that imputing *before* CV does introduce an optimistic bias, **but** its lower variance can yield lower overall RMSE; they conclude *unsupervised* imputation before CV "appears valid in certain settings," and that models tuned with impute-before vs impute-within differ minimally.
  - Why relevant: the draft (correctly) preaches fit-on-train-only; this is the honest footnote — the bias/variance trade-off is real, and *unsupervised* (e.g. median) imputation is the safer-to-relax case vs supervised/target-aware imputation. Good "common nuance" sidebar without undermining the rule.
  - Source: https://arxiv.org/abs/2010.00718 · type: paper · date: 2020-10 · 
- **Split-before-preprocessing as the consolidated best practice**  [REFRESH]  (confidence: verified)
  - Summary: 2024 practitioner consensus (sklearn `Pipeline`, fit on train only, transformations inside each CV fold; for resampling use `imblearn.Pipeline`). Pre-deployment checklist: never call `.fit()` on the unsplit data.
  - Why relevant: backs s02/s08 with a current, concrete leakage checklist (also feeds Ch 2).
  - Source: https://machinelearningmastery.com/data-preparation-without-data-leakage/ · type: blog · date: 2024 · 

### ch05_s03 — Simple vs. model-based imputation (the recency-hook subsection)

- **DiffPuter — diffusion + EM for imputation (current tabular SOTA reference)**  [REFRESH]  (confidence: verified; numbers from v2 abstract)
  - Summary: Combines a diffusion model with Expectation-Maximization — training step = M-step (density MLE), sampling step = E-step (a-posteriori estimate of the missing entries). Reports **6.94% average MAE and 4.78% RMSE improvement** over the strongest prior method across **10 datasets vs 17 baselines**. ICLR 2025 **Spotlight**.
  - Why relevant: the draft only says "diffusion models" generically — this is the named, dated, benchmarked anchor that turns the hand-wave into a citation. (Note: an earlier v1 abstract quoted 8.10%/5.64%; v2 reads 6.94%/4.78% — use v2.)
  - Source: https://arxiv.org/abs/2405.20690 · type: paper · date: 2024-05 → ICLR 2025 · 
- **ReMasker — masked-autoencoder imputation (the "BERT-for-tables" angle)**  [NEW]  (confidence: verified)
  - Summary: Extends masked autoencoding to tabular imputation by treating natural missingness as masks and additionally *re-masking* observed entries to train reconstruction; learns "missingness-invariant representations," and its advantage *grows as the missing ratio rises*. On par with / beats SOTA. ICLR 2024.
  - Why relevant: a second, conceptually distinct modern family (self-supervised reconstruction) to set beside diffusion and VAEs — keeps the "modern" paragraph from collapsing to one method.
  - Source: https://arxiv.org/abs/2309.13793 · type: paper · date: 2023-09 → ICLR 2024 · 
- **TabImpute — zero-shot imputation on a tabular foundation model (TabPFN)**  [NEW]  (confidence: verified)
  - Summary: A pre-trained transformer (built on TabPFN) that imputes **with no fitting or hyperparameter tuning at inference**, via entry-wise featurization, reporting ~**100× speedup** over prior deep approaches.
  - Why relevant: the freshest twist (Oct 2025) — connects this chapter to the "foundation models / learned representations" arc (Ch 15) and to the book's designed→learned spine; a vivid "where is this going" note.
  - Source: https://arxiv.org/abs/2510.02625 · type: paper · date: 2025-10 · 
- **not-MIWAE — MNAR-aware deep generative imputation (the missing piece next to MIWAE)**  [NEW]  (confidence: verified)
  - Summary: MIWAE (the method the draft names) assumes MAR; **not-MIWAE explicitly models the missingness mechanism** (e.g. self-censoring), so it stays unbiased under MNAR where MIWAE/mean-impute would not.
  - Why relevant: directly upgrades the draft's lone "MIWAE" mention and closes the s01 MNAR loop — modern method whose whole point is the mechanism taxonomy this chapter teaches.
  - Source: https://arxiv.org/abs/2006.12871 · type: paper · date: 2021 (ICLR 2021) · 
- **HyperImpute — AutoML imputation framework / one-stop benchmark library**  [NEW]  (confidence: verified)
  - Summary: van der Schaar lab framework that *iteratively selects and configures* column-wise models (AutoML for imputation). Ships a single API for MICE, MissForest, GAIN, MIRACLE, MIWAE, Sinkhorn, SoftImpute — i.e. the library to *demonstrate* the simple→model-based→deep ladder in the companion notebook.
  - Why relevant: gives the chapter a concrete, modern library that contains every tier the draft discusses (good for the repo/case study; reduces dependency sprawl).
  - Source: https://github.com/vanderschaarlab/hyperimpute · type: docs/paper · date: 2022 (ICML); maintained 2024-25 · 
- **Skeptical counterweight: simple stochastic imputers often match deep ones**  [NEW]  (confidence: verified)
  - Summary: "A Practical Guide to Modern Imputation" (Näf, Univ. Geneva, Jan 2026) argues good imputers must be (1) **distributional/stochastic** (draw, don't point-predict), (2) flexible/nonparametric, (3) sound under MAR; deterministic predictors like `missForest`/KNN can do *worse than ignoring* missingness on some distributions, while `mice-cart`/`mice-rf`/`mice-drf` excel. Companion benchmark "Do we Need Dozens of Methods…?" (Grzesiak, Muller, Josse, Näf, Nov 2025) reaches the same "complexity isn't automatically worth it" conclusion across classical → deep methods.
  - Why relevant: essential balance for the recency hook — keeps the book honest ("modern ≠ automatically better"; single-value model imputation shrinks variance). Pairs perfectly with the book's "inspection and judgment, not hands-off automation" framing.
  - Source: https://arxiv.org/abs/2601.14796 · type: paper · date: 2026-01 · 
- **sklearn `IterativeImputer` ≈ MICE but returns a *single* imputation**  [REFRESH]  (confidence: verified)
  - Summary: Docs state it was inspired by R's MICE but **returns one imputation, not multiple**; multiple imputation needs repeated runs with different seeds and `sample_posterior=True`. `KNNImputer` uses `nan_euclidean_distances`. Docs explicitly call single-vs-multiple imputation for prediction "an open problem."
  - Why relevant: precise correction to a common student misconception ("sklearn does MICE") and a clean hook to the uncertainty point below.
  - Source: https://scikit-learn.org/stable/modules/impute.html · type: docs · date: 1.9.0 · 

### ch05_s04 — The missing-indicator feature

- **`MissingIndicator` / `add_indicator` and its sharp edge**  [REFRESH]  (confidence: verified)
  - Summary: sklearn `MissingIndicator(features='missing-only')` (default) only emits masks for columns that had missing values **at fit time** — a column first seen missing at transform/inference gets *no* indicator. `add_indicator=True` on `SimpleImputer`/`IterativeImputer` stacks the mask automatically. Feature-engine's `AddMissingIndicator` is the equivalent and is meant to be *combined* with an imputer, never used alone.
  - Why relevant: the draft argues the concept well but names no API; this adds the leakage/availability gotcha (train-fitted indicator set is frozen) that fits the chapter's pipeline-discipline theme.
  - Source: https://scikit-learn.org/stable/modules/impute.html · type: docs · date: 1.9.0 · 
- **Caveat: indicators inflate dimensionality and can be mutually collinear**  [REFRESH]  (confidence: verified)
  - Summary: Practitioner guidance: indicators "capture the importance of missing values" but add columns and are often highly correlated with each other (co-missing patterns) — reinforces the draft's "don't indicate purely-random columns."
  - Why relevant: supports the draft's selectivity advice with a citeable source.
  - Source: https://www.blog.trainindata.com/your-guide-to-missing-values-imputation/ · type: blog · date: 2024-07 · 

### ch05_s05 — Outliers: detection vs. handling

- **PyOD 3.x — the canonical outlier-detection library (the missing tool in this chapter)**  [NEW]  (confidence: verified)
  - Summary: PyOD 3.6.1, ~**61 detectors**, 46M+ downloads, unified `fit`/`decision_function`/`predict` API spanning probabilistic (ECOD, COPOD, MAD), proximity (LOF, kNN, HBOS), ensembles (Isolation Forest, SUOD), and neural (AutoEncoder, VAE, **DeepSVDD**). "New in V3": agentic workflow + `EmbeddingOD` (text/image/audio via foundation-model encoders, 2025). Companion benchmark **ADBench** = 30 algorithms × 57 tabular datasets.
  - Why relevant: the draft mentions isolation forest in passing; PyOD is the obvious named home for "detection" and lets the case study/notebook scale beyond IQR without writing detectors by hand.
  - Source: https://github.com/yzhao062/pyod · type: docs · date: v3.6.1, 2017→2025 · 
- **ECOD — parameter-free, interpretable modern default detector**  [NEW]  (confidence: verified)
  - Summary: Empirical-CDF-based Outlier Detection — estimates a per-dimension empirical CDF, converts each point's coordinates to tail probabilities, aggregates into a score. **Parameter-free**, interpretable (shows which dims drove the score), fast/scalable; beat **11 SOTA baselines on 30 datasets**. IEEE TKDE 2022; in PyOD.
  - Why relevant: an excellent "if you must pick one multivariate detector, start here" recommendation — no contamination/threshold tuning, which suits the book's reproducible-and-inspectable ethos.
  - Source: https://arxiv.org/abs/2201.00382 · type: paper · date: 2022 (TKDE) · 
- **COPOD — copula-based detector (companion baseline to ECOD)**  [NEW]  (confidence: uncertain)
  - Summary: Copula-Based Outlier Detection; also parameter-free; reported ~**82.47% mean ROC-AUC over 30 datasets** (~1.5% over next best). ICDM 2020; in PyOD.
  - Why relevant: natural second-name alongside ECOD; both are the "modern, no-knob" probabilistic detectors the chapter currently omits.
  - Source: https://pyod.readthedocs.io/ · type: docs/paper · date: 2020 (ICDM) · 
- **scikit-learn outlier vs novelty detection (the API the draft would actually use)**  [REFRESH]  (confidence: verified)
  - Summary: `IsolationForest`, `LocalOutlierFactor`, `EllipticEnvelope`, `OneClassSVM`, `SGDOneClassSVM`. Key teaching distinction: **outlier detection** = training data is polluted (`fit_predict`); **novelty detection** = train on clean data, flag new points (`LOF(novelty=True)`, predict on unseen only). `contamination` sets the score threshold; LOF/IForest handle multimodal data, `EllipticEnvelope` assumes a single Gaussian.
  - Why relevant: gives s05 a precise vocabulary (detection≠novelty; the `contamination` knob is a *modeling assumption*) that reinforces "detection is observation, handling is a separate decision."
  - Source: https://scikit-learn.org/stable/modules/outlier_detection.html · type: docs · date: 1.9.0 · 
- **DeepOD + Deep SVDD for tabular/time-series anomaly detection**  [NEW]  (confidence: uncertain)
  - Summary: `DeepOD` packages ~25 deep detectors (reconstruction / representation / self-supervised); Deep SVDD trains a network so normal data falls in a tight hypersphere and works on tabular as well as images.
  - Why relevant: the "deep end" of the detection spectrum — one sentence is enough; mirrors the book's designed→learned spine without ballooning the chapter.
  - Source: https://pypi.org/project/deepod/ · type: docs · date: 2024 · 

### ch05_s06 — Robust transformations for outliers

- **MAD / modified z-score — the robust replacement for mean±kσ thresholds**  [NEW]  (confidence: verified)
  - Summary: Standard z-scores self-sabotage: an extreme value inflates the mean *and* σ, masking itself. The **modified z-score** `0.6745·(x − median)/MAD` (MAD = median |x − median|) uses median + median-absolute-deviation; common flag is `|mz| > 3.5`. Proposed by Hampel (1974).
  - Why relevant: the draft covers robust *scaling* but not robust *thresholding* for detection/capping; MAD is the natural bridge (and the 'mad' option in Feature-engine's `Winsorizer`).
  - Source: https://en.wikipedia.org/wiki/Median_absolute_deviation · type: docs/blog · date: classic (1974), guides 2024 · 
- **Feature-engine `Winsorizer` — capping as a fitted transformer with selectable rules**  [REFRESH]  (confidence: verified)
  - Summary: Caps min/max at limits found by one of four rules — `'gaussian'` (mean±kσ), `'iqr'` (Tukey fences), `'mad'` (robust, median+MAD), `'quantiles'` (percentiles) — and can add capping indicators. A `fit`/`transform` object, so the cap limits are learned on train only.
  - Why relevant: makes the draft's winsorizing concrete and *leakage-safe by construction*; the four-rule menu is a clean teaching table; ties s06 capping to the s02 pipeline thesis.
  - Source: https://feature-engine.trainindata.com/en/latest/api_doc/outliers/Winsorizer.html · type: docs · date: v1.9.x, 2024-25 · 
- **`sklearn.preprocessing.RobustScaler` (median + IQR) as the named primitive**  [REFRESH]  (confidence: verified)
  - Summary: The draft describes robust scaling in words; the concrete object is `RobustScaler` (centers on median, scales by IQR 25–75), already cross-referenced from Ch 3.
  - Why relevant: anchor the prose to the actual class for the notebook hand-off.
  - Source: https://scikit-learn.org/stable/modules/outlier_detection.html (cross-ref impute/preprocessing docs) · type: docs · date: 1.9.0 · 

### ch05_s07 — The boundary between data cleaning and feature engineering

- **Cleaning = static/global, FE = fit-on-train — the leakage line is the operational boundary**  [REFRESH]  (confidence: verified)
  - Summary: The 2024 leakage literature frames exactly the draft's distinction operationally: factual cleaning (parse "1,200.50", drop biologically-impossible age=150, dedupe) can be one-shot and global; representation changes (impute, scale, indicator) must be fit on train inside the pipeline. The test "does this depend on the train/test split?" is a crisp boundary criterion.
  - Why relevant: gives the philosophical subsection a single, citeable operational criterion instead of pure assertion.
  - Source: https://www.ibm.com/think/topics/data-leakage-machine-learning · type: blog/docs · date: 2024 · 
- *Honest note:* this is a positioning/scoping subsection; little genuinely-new external material exists and little is needed. One operational-criterion citation is the right ceiling — do not over-source it.

### ch05_s08 — Case study: a reproducible imputation & robust-handling pipeline

- **`ColumnTransformer` + `Pipeline` as the leakage-safe assembly (the signature-snippet target)**  [REFRESH]  (confidence: verified)
  - Summary: The book's `[KODE: ...]` placeholder maps to: `ColumnTransformer` routing columns → `AddMissingIndicator`/`add_indicator` + (`IterativeImputer`/`KNNImputer`) + `Winsorizer` + `RobustScaler`, all inside one `Pipeline.fit(X_train)`. Cap limits, imputation models, and indicator column-set are all frozen at fit and replayed at `transform`.
  - Why relevant: turns the conceptual case study into a concrete, current, copy-from-notebook skeleton.
  - Source: https://scikit-learn.org/stable/modules/impute.html · type: docs · date: 1.9.0 · 
- **The "impute inside CV" nuance applies to the case study's validation**  [NEW]  (confidence: verified)
  - Summary: When the case study reports CV scores, the "When to Impute?" result is the caveat to state — unsupervised imputation before CV is often fine, but supervised/iterative imputation belongs inside the fold to avoid optimistic bias.
  - Why relevant: lets the case study model honest, nuanced reporting rather than a slogan.
  - Source: https://arxiv.org/abs/2010.00718 · type: paper · date: 2020 · 

---

## Cross-cutting / chapter-level new developments

- **Diffusion & Flow-Matching for tabular data — a 2025–26 survey + curated list**  [NEW]  (confidence: verified). Splits the landscape into *generation* vs *imputation*; imputation roster: **TabCSDI** (NeurIPS-W 2022), **MissDiff**, **DiffPuter** (ICLR 2025), **SimpDM** (CIKM 2024), **NewImp** (NeurIPS 2024, gradient-flow view), **TabSyn**. One paragraph here future-proofs the s03 recency hook. Source: https://github.com/Diffusion-Model-Leiden/awesome-diffusion-models-for-tabular-data (survey arXiv:2502.17119) · survey · 2025-26.
- **"Modern ≠ automatically better" is now a documented stance**  [NEW]  (confidence: verified). Two 2025–26 papers (Näf 2026; Grzesiak et al. 2025) argue stochastic/distributional classical imputers (MICE-CART/RF/DRF) frequently match or beat deep methods, and that deterministic single-value imputation understates variance. This is the chapter's honest backbone against over-hyping — reuse in s03 and in the Ch 17 principles. Sources above.
- **Imputation uncertainty / single-vs-multiple imputation** [NEW] (confidence: verified). Single imputation underestimates variance (90% CIs can fall below 80% coverage at ~30% missingness); proper multiple imputation propagates uncertainty (Rubin's rules), though those rules can themselves under-cover for non-Bayesian imputers. Good "caveat" sidebar for s02/s03. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC4638176/ · paper · 2015 (canonical) + https://arxiv.org/abs/2601.14796 · 2026.
- **PyOD 3 / ADBench / DeepOD** as the consolidated outlier-detection ecosystem [NEW] (confidence: verified) — the chapter currently has *no* named detection library; PyOD is the single best citation for s05 and the case-study repo.
- **Missing *modality* (multimodal) — deep survey** [NEW] (confidence: verified). "Deep Multimodal Learning with Missing Modality: A Survey" (arXiv 2409.07825, v4 Aug 2025) taxonomizes handling into *modality imputation* (zero/random/retrieval composition, or generation via AE/GAN/diffusion) vs *architecture/representation* strategies (attention, distillation, graph, MLLM), and separates missing-at-train vs missing-at-test. **Mostly feeds Ch 14 (Multimodal), not Ch 5** — note as a forward pointer: "missing values" at the *modality* level is a structurally different problem from tabular cell-level missingness. Include only as a one-line cross-reference if at all. Source: https://arxiv.org/html/2409.07825v4 · survey · 2025-08.

## Candidate new terms (for Living Glossary / Appendix D)
- missingness mechanism (mekanisme *missingness*) — already partly in book
- multiple imputation vs single imputation (imputasi ganda vs imputasi tunggal) → note: book/sklearn `IterativeImputer` does *single*
- imputation uncertainty / proper imputation (ketidakpastian imputasi)
- iterative imputation / MICE / chained equations (imputasi iteratif) — in book; add "chained equations" gloss
- diffusion-based imputation (imputasi berbasis *diffusion*) — DiffPuter, TabCSDI
- masked-autoencoder imputation (imputasi *masked autoencoder*) — ReMasker
- zero-shot / foundation-model imputation (imputasi *zero-shot*) — TabImpute / TabPFN
- missingness-invariant representation
- winsorizing / capping (penanganan dengan *capping*) — in book (s06)
- median absolute deviation (MAD) / modified z-score (deviasi absolut median)
- empirical-CDF outlier detection — ECOD
- copula-based outlier detection — COPOD
- isolation forest / local outlier factor (LOF)
- novelty detection vs outlier detection (deteksi *novelty* vs deteksi *outlier*)
- contamination parameter (parameter *contamination*)
- Deep SVDD / deep anomaly detection
- nullity matrix / nullity correlation (`missingno` / MissMecha)

## Source list
- [1] Diffusion models for missing value imputation in tabular data (TabCSDI) — https://arxiv.org/abs/2210.17128 (paper, 2022)
- [2] DiffPuter: Empowering Diffusion Models for Missing Data Imputation — https://arxiv.org/abs/2405.20690 (paper, ICLR 2025 Spotlight)
- [3] ReMasker: Imputing Tabular Data with Masked Autoencoding — https://arxiv.org/abs/2309.13793 (paper, ICLR 2024)
- [4] TabImpute: Universal Zero-Shot Imputation for Tabular Data — https://arxiv.org/abs/2510.02625 (paper, 2025)
- [5] not-MIWAE: Deep Generative Modelling with Missing not at Random Data — https://arxiv.org/abs/2006.12871 (paper, ICLR 2021)
- [6] MIWAE: Deep Generative Modelling and Imputation of Incomplete Data — https://arxiv.org/abs/1812.02633 (paper, ICML 2019)
- [7] HyperImpute (AutoML imputation framework) — https://github.com/vanderschaarlab/hyperimpute (docs/paper, 2022→)
- [8] A Practical Guide to Modern Imputation (Näf) — https://arxiv.org/abs/2601.14796 (paper, 2026-01)
- [9] Do we Need Dozens of Methods for Real World Missing Value Imputation? — https://arxiv.org/abs/2511.04833 (paper, 2025-11)
- [10] Diffusion and Flow Matching Models for Tabular Data: A Survey (+ curated list) — https://github.com/Diffusion-Model-Leiden/awesome-diffusion-models-for-tabular-data / arXiv:2502.17119 (survey, 2025-26)
- [11] When to Impute? Imputation before and during cross-validation — https://arxiv.org/abs/2010.00718 (paper, 2020)
- [12] scikit-learn: Imputation of missing values (8.4) — https://scikit-learn.org/stable/modules/impute.html (docs, 1.9.0)
- [13] scikit-learn: Novelty and Outlier Detection (2.7) — https://scikit-learn.org/stable/modules/outlier_detection.html (docs, 1.9.0)
- [14] PyOD (GitHub) — https://github.com/yzhao062/pyod (docs, v3.6.1, 2025)
- [15] PyOD documentation — https://pyod.readthedocs.io/ (docs, 2025)
- [16] ECOD: Unsupervised Outlier Detection Using Empirical CDFs — https://arxiv.org/abs/2201.00382 (paper, IEEE TKDE 2022)
- [17] DeepOD (deep outlier detection library) — https://pypi.org/project/deepod/ (docs, 2024)
- [18] Feature-engine: Missing Data Imputation API — https://feature-engine.trainindata.com/en/latest/api_doc/imputation/index.html (docs, v1.9.x)
- [19] Feature-engine: Winsorizer — https://feature-engine.trainindata.com/en/latest/api_doc/outliers/Winsorizer.html (docs, v1.9.x)
- [20] Train in Data — Your Guide to Missing Values Imputation — https://www.blog.trainindata.com/your-guide-to-missing-values-imputation/ (blog, 2024-07)
- [21] Train in Data — MICE explained — https://www.blog.trainindata.com/multiple-imputation-with-chained-equations-mice-what-is-it/ (blog)
- [22] MissMecha: studying missing-data mechanisms — https://arxiv.org/abs/2508.04740 (paper, 2025-08)
- [23] missingno (missing-data visualization) — https://github.com/ResidentMario/missingno (docs, 2018)
- [24] Median absolute deviation — https://en.wikipedia.org/wiki/Median_absolute_deviation (reference; Hampel 1974)
- [25] Multiple Imputation: A Flexible Tool for Handling Missing Data — https://pmc.ncbi.nlm.nih.gov/articles/PMC4638176/ (paper, 2015 canonical)
- [26] Deep Multimodal Learning with Missing Modality: A Survey — https://arxiv.org/html/2409.07825v4 (survey, 2025-08) [mostly Ch 14]
- [27] How to Avoid Data Leakage When Performing Data Preparation — https://machinelearningmastery.com/data-preparation-without-data-leakage/ (blog, 2024)
- [28] What is Data Leakage in Machine Learning? (IBM) — https://www.ibm.com/think/topics/data-leakage-machine-learning (blog/docs, 2024)
