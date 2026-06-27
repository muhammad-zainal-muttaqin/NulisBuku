---
chapter: ch09
title: Feature Quality Evaluation
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 9 Resources — Feature Quality Evaluation

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence). "verified" = the cited source was fetched and the claim checked against it; "uncertain" = sourced from search-result summaries / abstracts only (full text not fetched, often paywalled).

## Coverage baseline (what the drafts already have)
- **s01** (NEW frame): feature quality = predictive utility + inference availability + stability/drift + sensitivity to measurement error + compute/storage/latency/maintenance cost. Ablation/SHAP positioned as tools *within* the frame. Single cited source so far is one 2023 trainindata blog — thin, the weakest-cited NEW subsection.
- **s02**: baseline via simple model + basic features; scikit-learn dummy estimators; every new feature must beat baseline net of cost.
- **s03**: ablation by feature *group* (not single feature) because of correlation + retrain cost; fraud example (drop transaction history → AUC −5%).
- **s04**: model-based (impurity/Gini) importance vs permutation importance; high-cardinality / ID-column overfitting; permutation is model-agnostic and run on validation.
- **s05**: SHAP as cooperative-game attribution; local→global aggregation; directional effect; medical-risk example. Brief explicitly excludes TreeSHAP-vs-KernelSHAP detail and the Shapley formula. Cited source: Molnar IML book (2023). **This is the labeled recency-hook subsection but currently cites nothing post-2023.**
- **s06**: importance stability across CV folds; importance ≠ causality (umbrella–rain confounder); forward-points to Ch 17 (intervention vs prediction).
- **s07** (NEW): drop-sensitive-attribute insufficient; proxies (postcode, device type); embeddings leak private info; remove-vs-retain protected attributes for auditing; data minimization; "improves accuracy ≠ legitimate." Cited: Fairlearn docs.
- **s08**: feature documentation as anti-liability (business logic, transform, source, baseline impact); feeds Appendix C template; Hopsworks feature-store blog (2022).
- **s09**: synthetic credit-default case; baseline → ablate demographics / transactions / interaction-logs → keep what pays for its cost; CV to confirm.

---

## Resources by subsection

### ch09_s01 — What makes a feature good? (utility, stability, availability, cost)
- **Feature-store quality dimensions formalize "availability + latency + cost" as first-class.**  [NEW]  (confidence: verified)
  - Summary: Production feature platforms split storage into an **online store** (low-latency, high-availability, latest value per key, sub-second / single-digit-ms p99 lookups for inference) and an **offline store** (high-throughput batch for training). Monitored operational metrics include feature **availability, capacity, staleness/freshness, serving throughput, latency, and error rates** — exactly the non-accuracy dimensions s01 argues for.
  - Why relevant: gives concrete, current vocabulary and an industry-standard framing for "availability at inference" and "cost/latency," replacing the lone 2023 blog. Lets the chapter say *where* availability is enforced (online store) and *what* gets monitored.
  - Source: https://www.databricks.com/blog/what-feature-store-complete-guide-ml-feature-engineering · type: blog/docs · date: 2024
- **Feature drift / Population Stability Index (PSI) makes "stability over time" measurable.**  [NEW]  (confidence: verified)
  - Summary: PSI is a univariate drift metric quantifying how much a feature's (or score's) distribution shifted between a baseline/training population and a recent production population; applied per-feature and to model outputs. Common rules of thumb: PSI < 0.1 stable, 0.1–0.25 moderate shift, > 0.25 significant shift. Tooling (Evidently) also offers Jensen–Shannon distance and Wasserstein distance, auto-selecting a method by column type and sample size (Wasserstein default for numeric > 1000 rows, JS for categoricals, default threshold 0.1; "dataset drift" flagged when ≥ 50% of columns drift).
  - Why relevant: turns the abstract "stability/robustness under shift" bullet into a named, computable diagnostic the reader can cite without turning the chapter into MLOps. Pairs with the s01 "drift" definition.
  - Source: https://docs.evidentlyai.com/metrics/preset_data_drift · type: docs · date: 2025  ·  also https://arize.com/blog-course/population-stability-index-psi/ (PSI explainer, 2024)
- **NannyML: estimating performance (silent failure) without labels.**  [NEW]  (confidence: uncertain — docs page timed out; claims from NannyML search summary + GitHub README)
  - Summary: Open-source library that estimates a deployed model's performance *before* labels arrive, via **CBPE** (Confidence-Based Performance Estimation, classification) and **DLE** (Direct Loss Estimation, regression); **PAPE** (mid-2024) is reported ~10–30% more accurate than CBPE. Tied directly to per-feature data-drift signals to explain *why* performance changed.
  - Why relevant: motivates s01's claim that a "good" feature is one whose stability you can actually watch in production; gives a concrete tool for "robustness under shift" without deep MLOps.
  - Source: https://github.com/NannyML/nannyml · type: docs/repo · date: 2024  ·  https://nannyml.readthedocs.io/en/v0.13.1/how_it_works/performance_estimation.html

### ch09_s02 — Establishing a baseline
- **scikit-learn `DummyClassifier`/`DummyRegressor` as the canonical naive baseline.**  [REFRESH]  (confidence: verified — same family of source already in brief)
  - Summary: Dummy estimators (strategies: most_frequent, stratified, prior, uniform, mean/median) give a "no real learning" reference so a metric like 0.85 accuracy can be judged against, e.g., a 0.80 majority-class floor. The brief already cites this; keep as the baseline anchor.
  - Why relevant: confirms the draft's "dummy estimator" claim with a current docs pointer.
  - Source: https://scikit-learn.org/stable/modules/model_evaluation.html#dummy-estimators · type: docs · date: 2024–2026
- *(Thin subsection externally — baselines are stable, well-settled methodology; little 2024–2026 novelty. The draft's content is sound; no strong new source needed beyond docs.)*

### ch09_s03 — Ablation studies
- **Ablation-study methodology reference (existing brief source holds up).**  [REFRESH]  (confidence: uncertain)
  - Summary: The brief cites arXiv:1905.09275 (ablation studies in ML / "ablation programming"). Still the most-cited dedicated treatment; the feature-group ablation the draft describes is an application of it.
  - Why relevant: keeps a citable definition for "ablation study" as a term.
  - Source: https://arxiv.org/abs/1905.09275 · type: paper · date: 2019
- *(Honest note: there is little fresh 2024–2026 literature on *feature-group* ablation specifically — it is a stable technique. The recency value for this subsection lives in s04/s05 instead.)*

### ch09_s04 — Permutation and model-based importance
- **scikit-learn permutation-importance docs: correlated-feature caution + train-vs-test + MDI bias.**  [REFRESH]  (confidence: verified)
  - Summary: Three load-bearing cautions, verified verbatim: (1) **Correlated features** — "When two features are correlated and one of the features is permuted, the model still has access to the latter through its correlated feature. This results in a lower reported importance value for both features, though they might actually be important." Recommended fix: cluster correlated features, keep one per cluster. (2) **Train vs held-out** — features important on train but not on a held-out set signal overfitting; compute on validation/CV. (3) **MDI (impurity) bias** — tree built-in importance "strongly biased and favor[s] high cardinality features," which is exactly the draft's ID-column failure; permutation importance avoids this.
  - Why relevant: the draft asserts the cardinality bias and the validation-set fix; this is the primary, current source backing both, plus it adds the correlated-feature dilution caveat the draft does not yet mention.
  - Source: https://scikit-learn.org/stable/modules/permutation_importance.html · type: docs · date: 2024–2026 (sklearn 1.9)
- **Conditional Permutation Importance (CPI) — statistically valid importance under correlation.**  [NEW]  (confidence: verified)
  - Summary: Chamma, Engemann & Thirion. Standard permutation importance "can misidentify unimportant variables as important in the presence of correlations among covariates." CPI resamples the feature of interest from its *conditional* distribution (preserving the joint structure) instead of marginal shuffling, giving **accurate type-I error control** while remaining model-agnostic and acting as a "drop-in replacement." Key interpretive distinction: marginal PFI measures loss from losing a feature's information; conditional importance measures loss from losing the information *unique* to that feature.
  - Why relevant: directly upgrades s04 (and s06's stability theme) with the modern, defensible fix for the correlated-feature pitfall the draft currently omits.
  - Source: https://arxiv.org/abs/2309.07593 · type: paper · date: 2023 (rev. 2023; NeurIPS 2023 line of work)
- **Disentangled Feature Importance (DFI) — attributing *shared* signal across correlated features.**  [NEW]  (confidence: verified)
  - Summary: Du, Roeder & Wasserman (2025). Argues conditional/incremental methods treat shared predictive information as redundancy — fine for selection, wrong for *attribution*. DFI maps covariates to an independent latent space via entropic optimal transport, computes importance there, then attributes back through barycentric sensitivities; recovers the classical R² decomposition in Gaussian linear settings, with uncertainty quantification.
  - Why relevant: a frontier (2025) framing of "importance under dependence," useful as a forward-pointer / advanced caveat; reinforces that "which importance?" depends on the question (selection vs attribution).
  - Source: https://arxiv.org/abs/2507.00260 · type: paper · date: 2025
- **"Stop Permuting Features" — the extrapolation intuition.**  [NEW]  (confidence: uncertain — blog)
  - Summary: Permuting a feature forces the model to predict on out-of-distribution combinations it never saw; because models extrapolate badly, those off-manifold points distort the importance score. A clean, teachable intuition for *why* the correlated-feature problem exists.
  - Why relevant: an accessible companion explanation for s04's caveat; good for a footnote/"common mistake."
  - Source: https://medium.com/data-science/stop-permuting-features-c1412e31b63f · type: blog · date: 2021

### ch09_s05 — SHAP for feature diagnosis (recency hook)
- **`shap` library current state (v0.52.0, May 2026): explainer families + GPU.**  [REFRESH]  (confidence: verified)
  - Summary: Latest release 0.52.0 (2026-05-28), Python ≥ 3.12. Explainer families: **TreeExplainer** (fast exact for tree ensembles), **PartitionExplainer**, **KernelExplainer** (model-agnostic), **LinearExplainer**, **DeepExplainer**/**GradientExplainer** (NN), plus **GPUTree**. GPU path enabled via `SHAP_ENABLE_CUDA=1`. Supports XGBoost/LightGBM/CatBoost/sklearn/PySpark/Transformers/TF/PyTorch.
  - Why relevant: the recency-hook subsection currently cites only a 2023 book; this anchors SHAP to the *current* library and explicitly names the fast/GPU paths the chapter mandate asks for — without needing the Shapley formula.
  - Source: https://pypi.org/project/shap/ · type: docs · date: 2026  ·  https://shap.readthedocs.io/en/latest/release_notes.html
- **Fast TreeSHAP (v1/v2) — algorithmic speedup of exact tree SHAP.**  [NEW]  (confidence: verified)
  - Summary: Yang (LinkedIn), 2021. v1 ≈ 1.5× faster than original TreeSHAP at equal memory; v2 ≈ 2.5–3× faster (medium/large models) at higher memory, ideal when interpreting many samples repeatedly. Complementary to GPUTreeShap (algorithmic vs parallel speedup; combinable).
  - Why relevant: concrete "modern fast SHAP variant" for the recency hook; lets the prose say SHAP at scale is solved without diving into math.
  - Source: https://arxiv.org/abs/2109.09847 · type: paper · date: 2021
- **GPUTreeShap — massively parallel exact SHAP for tree ensembles.**  [NEW]  (confidence: verified)
  - Summary: Mitchell, Frank & Holmes (2022, arXiv:2010.13972). CUDA implementation; benchmarked **13–19× faster** than a 40-core CPU TreeSHAP on medium/large models (e.g., 18.3× on covtype-large: 50.9s vs 930.2s). Shipped as **`shap.explainers.GPUTree`**, integrated into **XGBoost since 1.3** and into **RAPIDS cuML**.
  - Why relevant: the strongest single "modern SHAP" datapoint — turns "SHAP is too slow on big ensembles" into a solved, citable engineering fact.
  - Source: https://github.com/rapidsai/gputreeshap · type: docs/repo · date: 2022  ·  paper: https://arxiv.org/abs/2010.13972
- **PartitionExplainer / Owen values: SHAP that respects correlated feature groups.**  [NEW]  (confidence: verified)
  - Summary: PartitionExplainer computes Shapley values recursively over a feature hierarchy (Owen values), with quadratic — not exponential — exact runtime on a balanced partition tree, and "always assigns to groups of correlated features the credit that set of features would have had if treated as a group."
  - Why relevant: bridges s05 to the correlated-feature theme of s04/s06; the modern answer to "SHAP double-counts correlated features."
  - Source: https://shap.readthedocs.io/en/latest/generated/shap.PartitionExplainer.html · type: docs · date: 2026
- **Caveat: SHAP attributions are sensitive to feature representation.**  [NEW]  (confidence: verified)
  - Summary: Hwang, Bell, Fonseca, Pliatsika, Stoyanovich, Whang (2025). Routine engineering choices — histogram-binning age, choice of race encoding, scaling — measurably change SHAP importance *without changing the model*, and the effect can be exploited to hide discrimination. Conclusion: SHAP rankings are not an objective measure of true feature quality.
  - Why relevant: essential skeptical counterweight for the recency hook; ties s05 to s07 (fairness) and to the book's "importance ≠ ground truth" stance.
  - Source: https://arxiv.org/abs/2505.08345 · type: paper · date: 2025
- **Caveat: formal "failings of Shapley values for explainability."**  [NEW]  (confidence: uncertain — search summary + abstract)
  - Summary: Line of work (Marques-Silva et al.) proves existing SHAP-score definitions can assign undue high/low importance, and even give non-zero scores to provably irrelevant features. Reinforces "use SHAP to *generate hypotheses*, not to certify importance."
  - Why relevant: gives the chapter a rigorous citation for the limits of SHAP, balancing its dominance in the draft.
  - Source: https://www.sciencedirect.com/science/article/abs/pii/S0888613X23002438 · type: paper · date: 2023  ·  also https://arxiv.org/abs/2501.11429 (2025)

### ch09_s06 — Stability across folds; importance ≠ causality
- **Double/Debiased Machine Learning (DML): the principled bridge from prediction to causation.**  [NEW]  (confidence: verified via search summary of DoubleML docs + EconML)
  - Summary: DML (Chernozhukov et al.) separates the prediction task from causal-effect estimation using Neyman-orthogonal moments, sample-splitting, and cross-fitting — residualize outcome and treatment with flexible ML, then estimate the effect. Implementations: **DoubleML** (Python/R) and **EconML** (Microsoft); **DoWhy** integrates EconML estimators (e.g., `backdoor.econml.dml.LinearDML`). Literature shows explosive 2016–2024 growth.
  - Why relevant: the concrete, modern toolset behind s06's "importance ≠ causality" — names *what you would do instead* if the goal is intervention (forward-points to Ch 17).
  - Source: https://docs.doubleml.org/stable/literature/literature.html · type: docs · date: 2024  ·  https://www.pywhy.org/EconML/  ·  https://www.pywhy.org/dowhy/
- **Variable importance for causal forests — importance for *treatment-effect heterogeneity*.**  [NEW]  (confidence: verified)
  - Summary: Bénard & Josse (2023). Causal/Generalized Random Forests estimate heterogeneous treatment effects but are black boxes; this defines a "drop-and-relearn" variable importance measuring each input's impact on the *heterogeneity of treatment effects* (not prediction accuracy), with a corrective term for confounders. Implemented in the `grf` ecosystem; EconML exposes `CausalForestDML`/forest learners.
  - Why relevant: sharpens the draft's umbrella example — shows there exists a *different* importance notion when the question is causal, making "importance ≠ causality" actionable, not just cautionary.
  - Source: https://arxiv.org/abs/2308.03369 · type: paper · date: 2023  ·  related (with CIs): https://arxiv.org/abs/2408.13002 (2024)
- **Selection-stability tooling: Boruta-SHAP, shapicant, powershap.**  [NEW]  (confidence: uncertain — search summary)
  - Summary: A 2024 comparison evaluates Boruta/PIMP/Lasso vs Shapley-based Boruta-SHAP, shapicant, powershap. Findings: SHAP+Boruta reduces variance in the selection process and shows slightly better stability than plain importance-based selection; powershap/shapicant use shadow features + label permutation to derive p-value-style stop criteria.
  - Why relevant: connects s06's "stability across folds" to concrete modern selection methods (and back to Ch 7); gives the reader named tools for *stable* importance.
  - Source: https://github.com/Ekeany/Boruta-Shap · type: docs/repo · date: 2024  ·  powershap: https://link.springer.com/chapter/10.1007/978-3-031-26387-3_5

### ch09_s07 — Sensitive information and proxy features (privacy, fairness, data minimization)
- **Fairlearn assessment / MetricFrame — disaggregated fairness diagnostics.**  [REFRESH]  (confidence: verified)
  - Summary: Fairlearn (docs v0.15.dev, copyright 2018–2026) centers on **MetricFrame** for disaggregated metrics across sensitive groups, plus demographic parity, equalized odds, equal opportunity, and the **Four-Fifths (80%) rule**; supports intersecting groups and confidence intervals. (Note: the assessment page itself does not deep-dive "proxies" — that framing comes from the user-guide narrative the brief cited.)
  - Why relevant: the concrete, current tool for the "retain protected attributes to *audit*" argument in the draft; MetricFrame is exactly how you'd measure whether a proxy is discriminating.
  - Source: https://fairlearn.org/main/user_guide/assessment/index.html · type: docs · date: 2026
- **AIF360 (AI Fairness 360, Trusted-AI) — metrics + bias-mitigation across the pipeline.**  [NEW]  (confidence: verified)
  - Summary: Open-source toolkit with group + individual fairness metrics, bias scanning, and mitigation at **three stages**: pre-processing (modify training data), in-processing (constrain training), post-processing (adjust predictions). Offers a scikit-learn-compatible API.
  - Why relevant: the second named fairness toolkit the chapter mandate asks for; lets s07 mention that fairness can be addressed at the *feature/data* stage (pre-processing), aligning with the chapter's feature-engineering lens.
  - Source: https://aif360.readthedocs.io/en/stable/ · type: docs · date: 2024–2026
- **The Data Minimization Principle in Machine Learning.**  [NEW]  (confidence: verified)
  - Summary: Ganesh, Tran, Shokri & Fioretto (FAccT 2025; arXiv May 2024). Formalizes data minimization (legal roots: collect/process/retain only what's necessary) as an optimization problem over features — and finds a **significant mismatch between expected and actual privacy gains**: dropping features does *not* automatically protect privacy, because residual proxies remain. Directly supports the draft's "improves accuracy ≠ legitimate."
  - Why relevant: gives s07 a rigorous, citable backbone for "data minimization" beyond the intuition, and a sober caveat that minimization alone is not a privacy guarantee.
  - Source: https://arxiv.org/abs/2405.19471 · type: paper · date: 2024 (FAccT 2025)
- **Proxy discrimination: "fairness through unawareness" is insufficient; proxies can be detected/labeled.**  [NEW]  (confidence: uncertain — abstracts/search)
  - Summary: Multiple 2022–2026 works show sensitive attributes correlate with proxies (neighborhood/ZIP, device), so simply dropping the protected column fails ("fairness through unawareness ineffective"). Methods exist to *generate proxy sensitive-attribute labels* for auditing when the true attribute is missing; "weak proxies" can suffice (and may be preferable) for fairness assessment under missing sensitive data.
  - Why relevant: backs the draft's central claim about ZIP/device proxies with current literature, and supports the "retain for audit" recommendation.
  - Source: https://arxiv.org/html/2312.15994v1 (Proxy Sensitive Attribute Label Generation) · type: paper · date: 2023  ·  https://arxiv.org/pdf/2210.03175 (Weak Proxies, 2022)
- **The Statistical Fairness–Accuracy Frontier (Pareto trade-off).**  [NEW]  (confidence: verified)
  - Summary: Fallah, Jordan & Ulichney (2025). Formalizes the fairness–accuracy **Pareto frontier** and extends it to finite samples; provides worst-case-optimal estimators and **uniform finite-sample confidence bands** for the whole frontier, plus the insight that finite-sample effects hit each group's welfare asymmetrically (motivating deliberate sample allocation).
  - Why relevant: gives s07 a precise, modern way to discuss "removing vs retaining a sensitive/proxy feature has a fairness *cost/benefit*" as a trade-off curve, not a binary.
  - Source: https://arxiv.org/abs/2508.17622 · type: paper · date: 2025  ·  theory companion: https://arxiv.org/abs/2310.12785

### ch09_s08 — Documenting feature decisions
- **Model Cards for Model Reporting.**  [NEW]  (confidence: verified via documentation-standards survey)
  - Summary: Mitchell et al. (2019). Structured model documentation: intended use & users, contextual/conditioning factors, **disaggregated metrics across demographic groups**, ethical considerations, limitations. The de facto standard the chapter's "document feature decisions" should name-check.
  - Why relevant: elevates s08 from ad-hoc tables to a recognized standard; the disaggregated-metrics field ties documentation back to s07 fairness.
  - Source: https://arxiv.org/abs/1810.03993 · type: paper · date: 2019
- **Datasheets for Datasets.**  [NEW]  (confidence: verified)
  - Summary: Gebru et al. Documents motivation, composition (labels/errors), collection process, preprocessing/cleaning, recommended/contraindicated uses, distribution, and maintenance — the data-side analogue feeding feature provenance.
  - Why relevant: gives Appendix C lineage; "collection + preprocessing + intended use" maps cleanly onto the draft's source/transform/assumptions fields.
  - Source: https://arxiv.org/abs/1803.09010 · type: paper · date: 2018 (CACM 2021)
- **Data Cards (Google).**  [NEW]  (confidence: verified)
  - Summary: Pushkarna, Zaldivar & Kjartansson (2022). Modular, user-centric dataset documentation with **layered detail (telescopic / periscopic / microscopic)** capturing rationale, evolution, and operational impact. 2024–2026 trend: machine-readable schemas (JSON/OWL2), LLM-assisted generation (CardGen), and audits showing most cards still omit ethics/environment sections.
  - Why relevant: a more recent, structured model for the documentation template; the "layered detail" idea is a nice design cue for Appendix C.
  - Source: https://dl.acm.org/doi/fullHtml/10.1145/3531146.3533231 · type: paper · date: 2022
- **Feature store / feature catalog documentation (existing source refresh).**  [REFRESH]  (confidence: uncertain)
  - Summary: Feature stores double as feature *catalogs* — centralizing definitions, owners, lineage, and freshness so features are documented-by-construction and reusable, the production realization of the draft's anti-liability argument.
  - Why relevant: links s08's "documentation" to where it actually lives in modern stacks; updates the brief's 2022 Hopsworks pointer.
  - Source: https://www.databricks.com/blog/what-feature-store-complete-guide-ml-feature-engineering · type: blog/docs · date: 2024

### ch09_s09 — Case study: ablation across feature groups
- **(Reuse s03 + s04/s06 sources.)**  [REFRESH]  (confidence: verified)
  - Summary: The case study is synthetic/internal (per brief) and synthesizes baseline → group ablation → CV-stability → cost/latency decision. No new external source is strictly needed; strengthen "honest reporting" by referencing the permutation-importance validation discipline (sklearn docs) and CV-stability framing already gathered.
  - Why relevant: keeps the case grounded in cited methodology rather than introducing a new dataset claim.
  - Source: https://scikit-learn.org/stable/modules/permutation_importance.html · type: docs · date: 2024–2026
- *(Honest note: thinnest subsection for *external* sourcing — it is an applied synthesis by design. Recency value is borrowed from s01/s04/s05, not native.)*

---

## Cross-cutting / chapter-level new developments
- **The "importance ≠ ground truth" through-line is now empirically sharp.** Three independent 2023–2025 results converge: permutation importance fails under correlation (CPI fix), SHAP is manipulable by feature representation (Hwang 2025) and provably misleading in cases (Marques-Silva), and "real" importance for action requires causal estimands (causal-forest VI, DML). The chapter can frame all of Ch 9's tools as *hypothesis generators*, not certifiers.
- **Production monitoring is the natural home of "stability/availability/cost."** PSI + Evidently/NannyML give the chapter a concrete, current, non-MLOps-heavy vocabulary for s01 — and a clean forward link to Ch 17 drift/skew.
- **Documentation has standardized.** Model Cards / Datasheets / Data Cards (plus 2024–2026 machine-readable + LLM-generated variants) turn s08/Appendix C from "good habit" into "named artifact," with disaggregated-metrics fields that re-link to s07 fairness.
- **Fast SHAP is a solved engineering story.** Fast TreeSHAP (algorithmic) + GPUTreeShap (13–19× on GPU, shipped in XGBoost ≥1.3 and `shap.GPUTree`) + PartitionExplainer (correlated groups) collectively retire "SHAP is too slow / double-counts" — strong material for the s05 recency hook.
- **Fairness is a trade-off curve, not a switch.** The fairness–accuracy Pareto frontier (with finite-sample confidence bands) lets s07 discuss retain-vs-drop decisions quantitatively and honestly.

## Candidate new terms (for Living Glossary / Appendix D)
- **Population Stability Index (PSI)** — univariate distribution-shift metric (bands ~0.1 / 0.25).
- **Conditional Permutation Importance (CPI)** — permute conditional on other features; type-I error control under correlation.
- **Disentangled Feature Importance (DFI)** — latent-space (optimal-transport) attribution of shared signal.
- **Marginal vs conditional importance** — losing a feature's info vs losing only its *unique* info.
- **Owen values / PartitionExplainer** — SHAP over a feature hierarchy; credits correlated groups jointly.
- **TreeSHAP / Fast TreeSHAP / GPUTreeShap** — exact tree SHAP and its algorithmic/GPU accelerations.
- **CBPE / DLE / PAPE** — performance estimation without labels (classification / regression / 2024 successor).
- **Data minimization** — collect/process/retain only necessary features (legal + ML-optimization framing).
- **Proxy feature / proxy discrimination** — neutral-looking feature correlated with a protected attribute.
- **Fairness through unawareness** — (insufficient) strategy of dropping protected attributes.
- **MetricFrame** — disaggregated metric across sensitive groups (Fairlearn).
- **Four-Fifths (80%) rule** — disparate-impact threshold.
- **Fairness–accuracy Pareto frontier** — set of non-dominated fairness/accuracy trade-offs.
- **Double/Debiased Machine Learning (DML)** — orthogonalization + cross-fitting for causal effects (DoubleML/EconML/DoWhy).
- **Causal-forest variable importance** — importance for treatment-effect heterogeneity, not prediction.
- **Model card / Datasheet / Data card** — structured model/dataset documentation standards.

## Source list
- [1] What is a Feature Store? Complete Guide (Databricks) — https://www.databricks.com/blog/what-feature-store-complete-guide-ml-feature-engineering (blog/docs, 2024)
- [2] Evidently — Data Drift preset (PSI/JS/Wasserstein) — https://docs.evidentlyai.com/metrics/preset_data_drift (docs, 2025)
- [3] Arize — Population Stability Index (PSI) — https://arize.com/blog-course/population-stability-index-psi/ (blog, 2024)
- [4] NannyML — GitHub & performance-estimation docs (CBPE/DLE/PAPE) — https://github.com/NannyML/nannyml · https://nannyml.readthedocs.io/en/v0.13.1/how_it_works/performance_estimation.html (docs, 2024)
- [5] scikit-learn — Dummy estimators / model evaluation — https://scikit-learn.org/stable/modules/model_evaluation.html#dummy-estimators (docs, 2024–2026)
- [6] Ablation studies in ML (arXiv:1905.09275) — https://arxiv.org/abs/1905.09275 (paper, 2019)
- [7] scikit-learn — Permutation feature importance — https://scikit-learn.org/stable/modules/permutation_importance.html (docs, 2024–2026)
- [8] Chamma, Engemann, Thirion — Statistically Valid Variable Importance via Conditional Permutations (arXiv:2309.07593) — https://arxiv.org/abs/2309.07593 (paper, 2023)
- [9] Du, Roeder, Wasserman — Disentangled Feature Importance (arXiv:2507.00260) — https://arxiv.org/abs/2507.00260 (paper, 2025)
- [10] Vorotyntsev — Stop Permuting Features — https://medium.com/data-science/stop-permuting-features-c1412e31b63f (blog, 2021)
- [11] SHAP — PyPI (v0.52.0) — https://pypi.org/project/shap/ (docs, 2026)
- [12] SHAP — PartitionExplainer docs — https://shap.readthedocs.io/en/latest/generated/shap.PartitionExplainer.html (docs, 2026)
- [13] Yang — Fast TreeSHAP (arXiv:2109.09847) — https://arxiv.org/abs/2109.09847 (paper, 2021)
- [14] Mitchell, Frank, Holmes — GPUTreeShap (repo + arXiv:2010.13972) — https://github.com/rapidsai/gputreeshap · https://arxiv.org/abs/2010.13972 (docs/paper, 2022)
- [15] Hwang et al. — SHAP-based Explanations are Sensitive to Feature Representation (arXiv:2505.08345) — https://arxiv.org/abs/2505.08345 (paper, 2025)
- [16] Marques-Silva et al. — On the failings of Shapley values for explainability — https://www.sciencedirect.com/science/article/abs/pii/S0888613X23002438 · https://arxiv.org/abs/2501.11429 (paper, 2023/2025)
- [17] DoubleML — literature & docs — https://docs.doubleml.org/stable/literature/literature.html (docs, 2024)
- [18] EconML (PyWhy) — https://www.pywhy.org/EconML/ · DoWhy — https://www.pywhy.org/dowhy/ (docs, 2024–2026)
- [19] Bénard & Josse — Variable importance for causal forests (arXiv:2308.03369) — https://arxiv.org/abs/2308.03369 (paper, 2023)
- [20] Hines et al. — Variable importance in heterogeneous treatment effects with confidence (arXiv:2408.13002) — https://arxiv.org/abs/2408.13002 (paper, 2024)
- [21] Boruta-SHAP (repo) — https://github.com/Ekeany/Boruta-Shap · Powershap — https://link.springer.com/chapter/10.1007/978-3-031-26387-3_5 (docs/paper, 2023–2024)
- [22] Fairlearn — assessment / MetricFrame — https://fairlearn.org/main/user_guide/assessment/index.html (docs, 2026)
- [23] AIF360 (Trusted-AI) — https://aif360.readthedocs.io/en/stable/ (docs, 2024–2026)
- [24] Ganesh, Tran, Shokri, Fioretto — The Data Minimization Principle in ML (arXiv:2405.19471, FAccT 2025) — https://arxiv.org/abs/2405.19471 (paper, 2024)
- [25] Proxy Sensitive Attribute Label Generation (arXiv:2312.15994) — https://arxiv.org/html/2312.15994v1 (paper, 2023)
- [26] Weak Proxies are Sufficient and Preferable for Fairness with Missing Sensitive Attributes (arXiv:2210.03175) — https://arxiv.org/pdf/2210.03175 (paper, 2022)
- [27] Fallah, Jordan, Ulichney — The Statistical Fairness-Accuracy Frontier (arXiv:2508.17622) — https://arxiv.org/abs/2508.17622 (paper, 2025)
- [28] Theoretical Characterization of Accuracy-Fairness Pareto Frontier (arXiv:2310.12785) — https://arxiv.org/abs/2310.12785 (paper, 2023)
- [29] Mitchell et al. — Model Cards for Model Reporting (arXiv:1810.03993) — https://arxiv.org/abs/1810.03993 (paper, 2019)
- [30] Gebru et al. — Datasheets for Datasets (arXiv:1803.09010) — https://arxiv.org/abs/1803.09010 (paper, 2018)
- [31] Pushkarna et al. — Data Cards (ACM FAccT 2022) — https://dl.acm.org/doi/fullHtml/10.1145/3531146.3533231 (paper, 2022)
- [32] SHAP vs importance-based feature selection: comparative analysis (J. Big Data, 2024) — https://link.springer.com/article/10.1186/s40537-024-00905-w (paper, 2024; full text not fetched — search summary: importance-based slightly outperformed SHAP-based on selection)
