# Chapter 10 — Time Series & Sensor Data
## Externally-Sourced Research Resources

> **Chapter:** ch10  
> **Title:** Deret Waktu & Data Sensor (Time Series & Sensor Data)  
> **Generated:** 2026-06-27  
> **Agent:** Research Gathering  
> **Source priority:** official docs > trusted blogs > arXiv  
> **Tags:** [NEW] = published/updated 2024–2026 and not yet referenced in drafts; [REFRESH] = older foundational sources worth re-checking against current library versions.

---

## ch10_s01 — Temporal Sample Construction: Lookback, Stride, Horizon, Alignment

### 1. [NEW] sktime Forecasting Documentation — Window Reduction & Data Structures
- **Type:** Official documentation  
- **URL:** https://www.sktime.net/en/stable/api_reference/forecasting.html  
- **Relevance:** sktime's `make_reduction`, `DirectReductionForecaster`, and `RecursiveReductionForecaster` provide a programmatic API for all temporal sample construction concepts in this subsection. The `ForecastingHorizon` object cleanly separates lookback, prediction horizon, and relative/absolute definitions. Also demonstrates how sktime's splitters interface (expanding/sliding window) automates sample construction during backtesting.
- **Provenance:** sktime official docs, v0.30+ (2024–2025).

### 2. [REFRESH] sktime — Data Types & IO (Time Series Container Conventions)
- **Type:** Official documentation  
- **URL:** https://www.sktime.net/en/stable/examples/01_data_container.html  
- **Relevance:** Documents sktime's `pd.DataFrame`-based time-series container conventions (`MultiIndex` for panels), which is the foundation for understanding how lookback windows, strides, and horizon alignment map to the data structures that sktime and scikit-learn-compatible transformers expect. Essential for the "constructing the learning sample" framing of s01.
- **Provenance:** sktime official docs, 2024.

### 3. [NEW] aeon — Unequal Length Transformers (Padder, Resizer, Truncator)
- **Type:** Official documentation  
- **URL:** https://www.aeon-toolkit.org/en/stable/api_reference/transformations.html#unequal-length  
- **Relevance:** The draft mentions irregular sampling/resampling briefly. aeon's `Padder`, `Resizer`, and `Truncator` transformers are the programmatic realization of "resampling must create equal-length windows before windowing." Directly relevant for practitioners who face irregular time series in the wild.
- **Provenance:** aeon official docs, 2024–2025.

---

## ch10_s02 — Lag and Rolling-Statistics Features

### 1. [REFRESH] sktime — `make_reduction` with Custom Window Lengths
- **Type:** Official documentation  
- **URL:** https://www.sktime.net/en/stable/api_reference/forecasting.html#reduction  
- **Relevance:** sktime's reduction forecasters (`make_reduction`) auto-generate lag features from specified window lengths and provide built-in strategies (direct, recursive, multioutput). This is the canonical Python API for what ch10_s02 teaches conceptually. The `SkforecastAutoreg` adapter further demonstrates how to bridge sktime with popular auto-regressive libraries.
- **Provenance:** sktime official docs, 2025.

### 2. [NEW] tsfresh v0.20+ — Feature Extraction from Rolling Windows
- **Type:** Official documentation  
- **URL:** https://tsfresh.readthedocs.io/en/latest/text/list_of_features.html  
- **Relevance:** tsfresh computes 63+ feature categories per rolling window, including `absolute_sum_of_changes`, `mean_abs_change`, `agg_autocorrelation`, `agg_linear_trend`, `quantile`, etc. This is the practical instantiation of "extracting lag and rolling features from a lookback window" — the exact bridge from s01 (construct the window) to s02 (compute features within it).
- **Provenance:** tsfresh official docs, v0.20+ (2024).

### 3. [NEW] aeon — `TSFresh` and `Catch22` Wrappers for Feature Extraction
- **Type:** Official documentation  
- **URL:** https://www.aeon-toolkit.org/en/stable/api_reference/transformations.html#feature-based  
- **Relevance:** aeon wraps both `TSFresh` and `Catch22` as scikit-learn-compatible collection transformers. This means aeon users can extract hundreds of rolling/lag features from a collection of time series in a single fit/transform call — directly relevant to the "flattening temporal structure into tabular features" theme of s02.
- **Provenance:** aeon official docs, 2025.

---

## ch10_s03 — Differencing, Trend, and Seasonality

### 1. [NEW] aeon — `DifferenceTransformer`, `BKFilter`, `BoxCoxTransformer`, `SlopeTransformer`
- **Type:** Official documentation  
- **URL:** https://www.aeon-toolkit.org/en/stable/api_reference/transformations.html#series-transforms  
- **Relevance:** aeon provides a full pipeline-compatible suite for stationarity-oriented transformations: `DifferenceTransformer` (n-th order differencing), `BKFilter` (Baxter-King band-pass filter for trend-cycle decomposition), `BoxCoxTransformer` (variance stabilization), `SlopeTransformer` (piecewise trend slope). Each is a `BaseSeriesTransformer` — fits in a pipeline, no manual data editing.
- **Provenance:** aeon official docs, 2025.

### 2. [REFRESH] sktime — `STLForecaster` and `PolynomialTrendForecaster`
- **Type:** Official documentation  
- **URL:** https://www.sktime.net/en/stable/api_reference/forecasting.html#trend-forecasters  
- **Relevance:** sktime's STL decomposition-based forecaster extracts trend and seasonal components directly. Also `CurveFitForecaster` and `SplineTrendForecaster` provide programmable trend feature extraction. These operationalize the trend-decomposition concepts taught in ch10_s03 into actual Python estimators.
- **Provenance:** sktime official docs, 2024.

---

## ch10_s04 — Frequency-Domain Features (FFT)

### 1. [NEW] aeon — `PeriodogramTransformer` and `DWTTransformer`
- **Type:** Official documentation  
- **URL:** https://www.aeon-toolkit.org/en/stable/api_reference/transformations.html#collection-transformers  
- **Relevance:** `PeriodogramTransformer` extracts the power spectral density of time series — a direct frequency-domain feature extractor. `DWTTransformer` (Discrete Wavelet Transform) provides multi-scale spectral decomposition. Both are scikit-learn compatible transformers, making spectral-based feature extraction a pipeline step rather than an ad-hoc script.
- **Provenance:** aeon official docs, 2025.

### 2. [NEW] tsfresh — `fft_coefficient`, `fft_aggregated`, `fourier_entropy`, `spkt_welch_density`, `cwt_coefficients`
- **Type:** Official documentation  
- **URL:** https://tsfresh.readthedocs.io/en/latest/text/list_of_features.html  
- **Relevance:** tsfresh provides a rich set of frequency-domain feature calculators: FFT coefficients, spectral centroid/variance/skew/kurtosis, Fourier entropy via Welch's method, continuous wavelet transform coefficients. This shows readers that spectral features aren't just "compute FFT manually" — there's an established library ecosystem.
- **Provenance:** tsfresh official docs, 2024.

### 3. [REFRESH] Catch22 — Frequency-Domain Features in the Canonical Set
- **Type:** Academic paper (arXiv)  
- **URL:** https://arxiv.org/abs/1901.10200  
- **Relevance:** The Catch22 paper (Lubba et al., 2019) distilled 4,791 hctsa features into 22 maximally discriminative characteristics. Several of the 22 (e.g., `SP_Summaries_welch_rect_area_5_1`, `SP_Summaries_welch_rect_centroid`) are frequency-domain features, making this a canonical reference for which spectral features are most useful in practice.
- **Provenance:** arXiv:1901.10200, published 2019; implementation available in aeon, sktime, and the catch22 Python package via pycatch22.

---

## ch10_s05 — Temporal Validation: Avoiding Look-Ahead Leakage

### 1. [NEW] sktime — Temporal Splitters (`ExpandingWindowSplitter`, `SlidingWindowSplitter`, `CutoffSplitter`)
- **Type:** Official documentation  
- **URL:** https://www.sktime.net/en/stable/api_reference/split.html  
- **Relevance:** This is the authoritative implementation of temporal cross-validation. sktime provides `ExpandingWindowSplitter` (growing training window), `SlidingWindowSplitter` (fixed-size rolling window), `CutoffSplitter` (manual cutoffs), and `temporal_train_test_split`. These enforce the strict "train precedes test" temporal ordering that ch10_s05 teaches. The purging/embargo concept ("purge gap" in the draft) maps to how these splitters handle overlapping windows.
- **Provenance:** sktime official docs, 2025.

### 2. [REFRESH] sktime — `evaluate` Backtesting Function for Forecasting
- **Type:** Official documentation  
- **URL:** https://www.sktime.net/en/stable/api_reference/forecasting.html  
- **Relevance:** sktime's `evaluate` function runs backtesting (rolling origin evaluation) with proper temporal split handling. This is the practical implementation of the temporal validation strategy taught in s05 — users should use `evaluate(splitter=temporal_cv)` rather than manual loops, because the library handles the purge-gap logic and temporal ordering automatically.
- **Provenance:** sktime official docs, 2024.

---

## ch10_s06 — Features for Classic Models vs. Sequential Inputs

### 1. [NEW] PatchTST — Time Series Patching as a Bridge Between Tabular and Sequential Representations
- **Type:** Academic paper (arXiv, ICLR 2023)  
- **URL:** https://arxiv.org/abs/2211.14730  
- **Relevance:** PatchTST (Nie et al., ICLR 2023) reframes time-series forecasting by segmenting series into subseries-level patches used as Transformer tokens. This is directly relevant to s06's spectrum discussion: patches are a "halfway point" — they're neither fully handcrafted lags (tabular) nor raw timesteps (sequential). The paper also demonstrates masked pre-training for time series, where the model learns representations by reconstructing masked patches — representing the shift toward *dipelajari mesin* representations. Channel-independence design (each variable treated as separate univariate series sharing weights) also demonstrates a modern FE decision.
- **Provenance:** arXiv:2211.14730v2, ICLR 2023; code at github.com/yuqinie98/PatchTST.

### 2. [NEW] Chronos — Pretrained Forecasting Models as Feature Extractors
- **Type:** Academic paper (arXiv, 2024)  
- **URL:** https://arxiv.org/abs/2403.07815  
- **Relevance:** Chronos (Ansari et al., Amazon, 2024) tokenizes time-series values via scaling and quantization into a fixed vocabulary, then trains T5-family models on tokenized series via cross-entropy. This is a paradigm shift for s06: a single pretrained model can serve as a *feature extractor* (by extracting embeddings or forecast outputs) for downstream models. Demonstrates zero-shot forecasting on unseen datasets — a capability beyond handcrafted features. Available on Hugging Face (amazon/chronos-t5-*).
- **Provenance:** arXiv:2403.07815, Mar 2024; model checkpoints on Hugging Face.

### 3. [NEW] Lag-Llama — Lags as Covariates in a Foundation Model
- **Type:** Academic paper (arXiv, 2023)  
- **URL:** https://arxiv.org/abs/2310.08278  
- **Relevance:** Lag-Llama (Rasul et al., 2023) is a decoder-only transformer that uses *lags as covariates* — the model itself learns how to consume lag features. This inverts the s06 framing: instead of "you must flatten lags for tabular models and pass raw sequences for DL models," Lag-Llama shows that even modern transformer architectures can be designed to explicitly accept handcrafted lag features alongside the raw sequence. Available on Hugging Face (time-series-foundation-models/Lag-Llama).
- **Provenance:** arXiv:2310.08278, Oct 2023; GitHub: github.com/time-series-foundation-models/lag-llama.

### 4. [NEW] MOMENT — General-Purpose Time-Series Foundation Model for Feature Extraction
- **Type:** Academic paper (arXiv, ICML 2024)  
- **URL:** https://arxiv.org/abs/2402.03885  
- **Relevance:** MOMENT (Goswami et al., ICML 2024) is an open-source family of pretrained models for general-purpose time-series analysis. Key to s06: MOMENT can serve as a frozen feature extractor for classification, regression, anomaly detection, and forecasting with minimal fine-tuning. This is the **forecasting-as-FE** paradigm — use a pretrained model to produce embeddings that downstream models use as features. Available on Hugging Face (AutonLab/MOMENT-1-large).
- **Provenance:** arXiv:2402.03885v3, ICML 2024; Hugging Face model page.

### 5. [REFRESH] TS2Vec — Universal Self-Supervised TS Representation
- **Type:** Academic paper (arXiv, AAAI 2022)  
- **URL:** https://arxiv.org/abs/2106.10466  
- **Relevance:** TS2Vec (Yue et al., AAAI 2022) proposed hierarchical contrastive learning for time series, achieving SOTA on 125 UCR and 29 UEA datasets. A linear regressor on top of TS2Vec features outperforms previous forecasting SOTAs. Directly relevant to s06: TS2Vec learned representations can replace handcrafted lag/rolling features entirely for many tasks.
- **Provenance:** arXiv:2106.10466, AAAI 2022; code at github.com/yuezhihan/ts2vec.

### 6. [REFRESH] TS-TCC and CoST — Contrastive Time-Series Representation Learning
- **Type:** Academic papers (arXiv)  
- **URLs:** https://arxiv.org/abs/2106.14112 (TS-TCC, IJCAI 2021); https://arxiv.org/abs/2202.01575 (CoST, 2022)  
- **Relevance:** TS-TCC uses weak/strong augmentations plus temporal+contextual contrastive learning — a linear classifier on top matches supervised performance. CoST disentangles seasonal and trend representations via time-domain + frequency-domain contrastive losses, achieving 21.3% MSE improvement on multivariate benchmarks. Both are canonical examples of self-supervised TS representation learning, moving from *dirancang manusia* (manual lag/rolling features) toward *dipelajari mesin*.
- **Provenance:** arXiv:2106.14112 (IJCAI-21); arXiv:2202.01575.

---

## ch10_s07 — Case Study: Multivariate Time-Series Prediction

### 1. [NEW] TimesNet — Temporal 2D-Variation Modeling for Multivariate Time Series
- **Type:** Academic paper (arXiv, ICLR 2023)  
- **URL:** https://arxiv.org/abs/2210.02186  
- **Relevance:** TimesNet (Wu et al., ICLR 2023) converts 1D time series into 2D tensors by discovering multiple periods, enabling 2D CNNs to capture both intra-period and inter-period variations. SOTA on five tasks (forecasting, imputation, classification, anomaly detection). Directly relevant to the multivariate prediction case study — demonstrates that modern approaches can learn periodic structures that handcrafted cyclical encoding approximates. Available in sktime as `LTSFTransformerForecaster`.
- **Provenance:** arXiv:2210.02186v3, ICLR 2023; code at github.com/thuml/Time-Series-Library.

### 2. [REFRESH] aeon — Benchmarking API for Fair Model Comparison
- **Type:** Official documentation  
- **URL:** https://www.aeon-toolkit.org/en/stable/api_reference/benchmarking.html  
- **Relevance:** aeon provides a reproducible benchmarking framework for comparing multiple time-series models with proper cross-validation. In a case study that emphasizes "temporal split done right," aeon's benchmarking tools ensure the comparison is honest — same splits, same metrics, reproducible seeds. This complements sktime's `evaluate` with a different ecosystem.
- **Provenance:** aeon official docs, 2024–2025.

### 3. [NEW] sktime LTSF Forecasters — PatchTST and TimesNet as sktime Estimators
- **Type:** Official documentation  
- **URL:** https://www.sktime.net/en/stable/api_reference/forecasting.html#deep-learning-based-forecasters  
- **Relevance:** sktime now integrates modern deep-learning forecasters including `LTSFLinearForecaster`, `LTSFDLinearForecaster`, `LTSFNLinearForecaster`, and `LTSFTransformerForecaster` (including TimesNet-based), as well as `SCINetForecaster`, `ConvTimeNetForecaster`, `XLSTMForecaster`, and `CINNForecaster`. These provide the "modern model" baseline that the case study in s07 could compare against the random forest baseline described in the draft.
- **Provenance:** sktime official docs, 2025.

---

## Cross-Cutting Resources (Useful for Multiple Subsections)

### A. [NEW] tsfresh — Official Introduction & Feature Overview
- **Type:** Official documentation  
- **URL:** https://tsfresh.readthedocs.io/en/latest/text/introduction.html  
- **Relevance:** The reference documentation for automated time-series feature extraction in Python. Covers 63+ feature calculators across categories: statistical moments, autocorrelation, spectral/Fourier, entropy, complexity, wavelet, and more. Provides the feature relevance filtering pipeline (Fresh algorithm) that selects statistically significant features. Relevant to s02–s04 and s06.
- **Provenance:** tsfresh v0.20+, 2024.

### B. [REFRESH] hctsa — Highly Comparative Time-Series Analysis (MATLAB/Python)
- **Type:** GitHub repository + Academic paper  
- **URLs:** https://github.com/benfulcher/hctsa | Cell Systems (2017), J. Roy. Soc. Interface (2013)  
- **Relevance:** The original massive feature extraction library (7,700+ features). Catch22 is derived from this. The repository's `FeatureSets` directory documents the full taxonomy of time-series features (distribution, autocorrelation, entropy, stationarity, scaling, model-based, etc.), which provides a conceptual reference map for time-series feature engineering. Last release v1.10 (Nov 2024).  
- **Provenance:** GitHub benfulcher/hctsa, papers cited in README.

### C. [NEW] aeon — `Catch22` Transformer + ROCKET Family
- **Type:** Official documentation  
- **URL:** https://www.aeon-toolkit.org/en/stable/api_reference/transformations.html  
- **Relevance:** aeon's `Catch22` transformer (with `catch24` option for mean+variance) and the ROCKET/MiniRocket/MultiRocket family are state-of-the-art convolution-based feature extractors for time series. ROCKET (random convolutional kernels) provides GPU-accelerated options via `ROCKETGPU`. These are "handcrafted" feature extractors (designed by humans) that achieve near-SOTA accuracy for time-series classification, showing that even at the *dirancang manusia* pole, modern automated methods exist.
- **Provenance:** aeon official docs, 2025.

### D. [NEW] aeon — Self-Supervised Transformers (TRILITE, TimeMCL)
- **Type:** Official documentation  
- **URL:** https://www.aeon-toolkit.org/en/stable/api_reference/transformations.html#self-supervised  
- **Relevance:** aeon now includes self-supervised representation learning transformers (`TRILITE` — triplet loss in time, `TimeMCL` — time mixup contrastive learning) directly as `CollectionTransformer` objects. This enables the book's *dipelajari mesin* narrative to point at actual library implementations, not just research papers.
- **Provenance:** aeon official docs, 2025.

---

## Resource Summary Table

| Subsection | [NEW] Items | [REFRESH] Items | Total |
|---|---|---|---|
| ch10_s01 | 2 (sktime forecasting API, aeon unequal-length) | 1 (sktime data containers) | 3 |
| ch10_s02 | 2 (tsfresh feature list, aeon feature wrappers) | 1 (sktime make_reduction) | 3 |
| ch10_s03 | 1 (aeon diff/BKFilter/BoxCox/Slope) | 1 (sktime STL/trend forecasters) | 2 |
| ch10_s04 | 2 (aeon Periodogram/DWT, tsfresh FFT features) | 1 (Catch22 frequency features) | 3 |
| ch10_s05 | 1 (sktime temporal splitters) | 1 (sktime evaluate backtesting) | 2 |
| ch10_s06 | 4 (PatchTST, Chronos, Lag-Llama, MOMENT) | 2 (TS2Vec, TS-TCC/CoST) | 6 |
| ch10_s07 | 2 (TimesNet, sktime LTSF forecasters) | 1 (aeon benchmarking) | 3 |
| Cross-cutting | 3 (tsfresh intro, aeon Catch22/ROCKET, aeon self-supervised) | 1 (hctsa) | 4 |
| **Total** | **17** | **9** | **26** |

---

## Provenance & Quality Notes
- All arXiv papers accessed 2026-06-27 via direct abstract-page fetches, confirmed to match title and content.
- Library documentation accessed during the same research session; version numbers reflect the current stable docs as of mid-2025 (sktime v0.30+, tsfresh v0.20+, aeon v0.11+).
- Hugging Face model references (Chronos, MOMENT, Lag-Llama) confirmed via arXiv paper metadata.
- No synthetic/nonexistent URLs; all are real, functional, and directly relevant.
- No prose written — these are research pointers only. The compiler/writer must decide what to incorporate.
