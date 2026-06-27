---
chapter: ch08
title: Dimensionality Reduction & Latent Representations
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 8 Resources — Dimensionality Reduction & Latent Representations

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence). Chapter 8 is 🔢 notation-bearing and academic-primary on UMAP. The explicit Ch 8 ↔ Ch 15 boundary holds throughout: **Ch 8 = unsupervised compression of YOUR OWN data matrix (PCA/SVD/NMF/autoencoder); Ch 15 = transferred pretrained representations from external corpora.**

## Coverage baseline (what the drafts already have)
- **s01** — Curse of dimensionality; reduction creates a dense *latent representation* (vs. selection which drops columns); two goals: compression (preprocessing) vs. visualization (2D/3D). Sensor example.
- **s02** — PCA (orthogonal variance-maximizing components, $X_{reduced}=XW_k$); SVD ($X=U\Sigma V^T$); Truncated SVD for sparse matrices where mean-centering destroys sparsity (TF-IDF → Ch 11).
- **s03** — NMF ($X\approx WH$, $W,H\ge 0$), additive parts-based representation, interpretability vs. PCA; topic modeling and audio spectrogram examples.
- **s04** — Manifold learning; Swiss roll; t-SNE (local structure, KL divergence, slow, distorts global); UMAP as modern academic primary (Riemannian geometry, faster, better global); single-cell RNA example; both for visualization not preprocessing.
- **s05** — Autoencoder as learned compression (encoder/decoder, bottleneck, reconstruction loss); "dipelajari mesin" spectrum note; still your-own-data, no external semantics.
- **s06** — Misuse 1 (t-SNE/UMAP coords as features); Misuse 2 (PCA leakage — fit on whole dataset before split); boundary with Ch 15.
- **s07** — Case study: PCA (95% variance) vs. autoencoder on high-dim (image) data; pipeline with StandardScaler; claims autoencoder beats PCA on downstream accuracy.
- **Gaps the drafts do not touch:** PaCMAP / TriMap / PHATE / densMAP / DREAMS / PCC (newer manifold methods); the *initialization* critique of the "UMAP preserves global structure" claim; parametric UMAP (inductive transform for inference); VAE / β-VAE / disentanglement and other autoencoder variants (denoising/sparse/contractive); spectral methods (Laplacian eigenmaps, diffusion maps); TDA / persistent homology; IncrementalPCA / randomized SVD / MiniBatchNMF / β-divergence; applying PCA to high-dim pretrained transformer embeddings (whitening, anisotropy); intrinsic-dimensionality estimation for choosing $k$; privacy/fairness risks of DR (reversibility, bias propagation).

## Resources by subsection

### ch08_s01 — Why reduce dimensionality? Compression vs. visualization

- **Comprehensive review: a four-way taxonomy + eight persistent challenges**  [NEW]  (confidence: verified)
  - Summary: Organizes DR into linear (PCA/LDA/ICA/NMF), nonlinear (manifold: t-SNE, UMAP, Isomap, LLE; neural: AE, VAE, transformer embeddings), hybrid (PCA→UMAP), and ensemble (Procrustes/consensus). Names eight challenges: dimensionality selection, interpretability–accuracy trade-off, stability/reproducibility, overfitting in HDLSS, **bias propagation**, **privacy (PCA/AE are reversible)**, noise sensitivity, scalability ($O(n^2)$).
  - Why relevant: gives s01 a cleaner "why and what to watch for" frame than just compression-vs-visualization; the privacy/bias points forward-link to Ch 9 (sensitive/proxy features). The hybrid PCA→UMAP idea reframes "two goals" as composable steps.
  - Source: https://peerj.com/articles/cs-3025/ (PMC mirror https://pmc.ncbi.nlm.nih.gov/articles/PMC12453773/) · type: paper (review) · date: PeerJ Computer Science, 2025 (Aasim Ayaz Wani)

- **How many components? Intrinsic-dimensionality estimation vs. the 95%-variance heuristic**  [NEW]  (confidence: verified)
  - Summary: The "keep 90–95% variance" rule the drafts use (s07) "lacks theoretical grounding." Modern alternatives: intrinsic-dimensionality estimators (TwoNN, DANCo), parallel analysis (compare observed eigenvalues to random), and task-aligned cross-validation.
  - Why relevant: gives s01/s02/s07 an honest answer to the recurring student question "how many dimensions do I keep?" beyond an arbitrary variance threshold.
  - Source: https://peerj.com/articles/cs-3025/ · type: paper (review) · date: 2025

### ch08_s02 — PCA and SVD / truncated SVD 🔢

- **scikit-learn `decomposition`: the full PCA family beyond plain PCA**  [REFRESH]  (confidence: verified)
  - Summary: PCA centers but does **not** scale (so StandardScaler first); `whiten=True` rescales components to unit variance for downstream models assuming isotropy (RBF-SVM, K-Means); `svd_solver='randomized'` for $k\ll d$; **IncrementalPCA** (`partial_fit`, memmap) for out-of-core/streaming data that doesn't fit in memory; TruncatedSVD = PCA-without-centering for sparse text (LSA), recommended with `TfidfVectorizer(sublinear_tf=True, use_idf=True)`.
  - Why relevant: drafts cover PCA/SVD/TruncatedSVD intuition but omit the practical menu (randomized solver, IncrementalPCA for big/streaming data, the whiten option). Directly extends s02 with current API caveats.
  - Source: https://scikit-learn.org/stable/modules/decomposition.html · type: docs · date: scikit-learn 1.x (current, 2025/2026)

- **Applying PCA to high-dimensional pretrained transformer/sentence embeddings**  [NEW]  (confidence: verified)
  - Summary: On pretrained sentence embeddings, plain **PCA cuts dimensionality ~50% with no significant downstream loss**, and sometimes *improves* STS/retrieval (e.g. all-mpnet-base-v2). A 2025 retrieval study finds standard PCA and Kernel-PCA retain performance under heavy reduction while **autoencoders and especially UMAP degrade drastically**; PCA is also far cheaper (≈2 s train, ≈5 ms inference).
  - Why relevant: This is the Ch 8 side of the Ch 8↔Ch 15 boundary — compressing *your own copy* of (possibly pretrained) embeddings is a PCA job, not a UMAP/AE job. Strong, current evidence to counter the instinct to reach for fancy nonlinear methods.
  - Source: https://arxiv.org/abs/2403.14001 (Zhang, Zhou, Bollegala — "Evaluating Unsupervised Dimensionality Reduction Methods for Pretrained Sentence Embeddings", LREC-COLING 2024) · type: paper · date: 2024

- **Whitening / anisotropy of transformer embeddings — task-dependent**  [NEW]  (confidence: uncertain — fetch failed; conclusion corroborated across two search summaries)
  - Summary: LLM embeddings are anisotropic; PCA-whitening makes them isotropic. Whitening **helps semantic-similarity / retrieval** (cosine becomes geometrically faithful) but **consistently hurts classification** (it strips discriminative anisotropies classifiers exploit), worse at higher dimension.
  - Why relevant: nuances the `whiten=True` option for s02/s06 — "isotropy is good" is not universally true. Good "kapan/mengapa/trade-off" material.
  - Source: https://arxiv.org/pdf/2407.12886 ("Whitening Not Recommended for Classification Tasks in LLMs", 2024) · type: paper · date: 2024

### ch08_s03 — NMF 🔢

- **scikit-learn NMF: β-divergence, MiniBatchNMF, initialization, regularization**  [NEW]  (confidence: verified)
  - Summary: The loss is a **β-divergence**: β=2 Frobenius (default), β=1 **Kullback–Leibler** (natural for counts/text), β=0 **Itakura–Saito** (natural for audio power spectrograms) — so the drafts' two examples (topics, spectrograms) map to *different divergences*. Solvers: `'cd'` (Frobenius only) vs `'mu'` (any β). Init matters (`nndsvda`/`nndsvdar` for dense, `nndsvd` for sparse). `MiniBatchNMF` (Lefèvre/Bach/Févotte 2011) scales NMF to large data via mini-batches + forgetting factor; L1/L2 regularization (`alpha_W`, `alpha_H`, `l1_ratio`) tunes sparsity.
  - Why relevant: upgrades s03 from "NMF is additive/interpretable" to the modern, large-scale, divergence-aware version — and the β=1 (text) / β=0 (audio) detail makes the draft's two examples technically precise. "Modern NMF variants" is an explicit priority topic.
  - Source: https://scikit-learn.org/stable/modules/decomposition.html and https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.MiniBatchNMF.html · type: docs · date: scikit-learn 1.x (current)

### ch08_s04 — Manifold learning: t-SNE and UMAP 🔢

- **UMAP — canonical paper (academic primary)**  [REFRESH]  (confidence: verified)
  - Summary: McInnes, Healy, Melville. Riemannian geometry + algebraic topology; competitive with t-SNE on quality, "arguably preserves more global structure," superior runtime, no embedding-dimension cap (viable as general-purpose DR, not just 2D viz).
  - Why relevant: the citation behind s04's UMAP claims; cite the arXiv id and JOSS package paper.
  - Source: https://arxiv.org/abs/1802.03426 (paper) · https://joss.theoj.org/papers/10.21105/joss.00861 (software) · type: paper · date: 2018; umap-learn current docs at v0.5.8

- **The initialization critique — UMAP's global-structure edge is mostly from PCA init**  [NEW]  (confidence: verified)
  - Summary: A widely-cited counter-result: UMAP does **not** preserve global structure better than t-SNE *when both use the same (informative) initialization*. UMAP-with-random-init is as poor globally as t-SNE-with-random-init; t-SNE-with-PCA-init matches UMAP. The "captured global structure is just the result of an informative initialization." sklearn's t-SNE now supports `init='pca'`.
  - Why relevant: This is the single most important *correction* to the drafts. s04 states UMAP intrinsically "menjaga penempatan struktur global" — the honest, current framing is "with good initialization." High-value "kesalahan umum / nuance" material.
  - Source: https://www.biorxiv.org/content/10.1101/2019.12.19.877522v1 (Kobak & Linderman) · echoed in https://pmc.ncbi.nlm.nih.gov/articles/PMC12453773/ · type: paper · date: 2019/2021

- **PaCMAP — near / mid-near / further pairs (balances local AND global)**  [NEW]  (confidence: verified)
  - Summary: Wang, Huang, Rudin, Shaposhnik. Categorizes point pairs into **near** (local), **mid-near** (global skeleton), and **further** (anti-collapse) and weights them over training; this is the design principle that lets one method preserve both scales where t-SNE/UMAP/TriMap trade one for the other. The companion analysis distills DR into attraction/repulsion + initialization principles.
  - Why relevant: the strongest "newer manifold method" to add to s04 as the modern successor framing; directly fits the academic-primary brief. PaCMAP slightly improves global structure over UMAP in benchmarks.
  - Source: https://arxiv.org/abs/2012.04456 (JMLR vol. 22, 2021) · type: paper · date: 2021

- **TriMap — triplet-based, global-structure-first**  [NEW]  (confidence: verified)
  - Summary: Amid & Warmuth. Uses **triplets** $(i,j,k)$ ("i closer to j than k") instead of pairwise similarities to capture higher-order/global structure (relative cluster distances, multiple scales, outliers); scales to millions of points, faster than t-SNE/UMAP.
  - Why relevant: a second modern manifold method for s04's comparison table; the triplet idea contrasts cleanly with t-SNE/UMAP pairwise probabilities.
  - Source: https://arxiv.org/abs/1910.00204 · type: paper · date: 2019

- **PHATE — diffusion/heat-potential embedding for trajectories**  [NEW]  (confidence: verified)
  - Summary: Moon, van Dijk, et al. Heat-diffusion affinities → denoised 2D/3D embedding that preserves **continuous progression/branching trajectory** structure (not just clusters); strong in single-cell biology. Preserves both local and global distances but (per comparisons) can blur local cluster structure.
  - Why relevant: rounds out the s04 family with the "trajectory/continuum" use-case that clustering-oriented t-SNE/UMAP miss; connects DR to the spectral/diffusion-maps family below.
  - Source: https://www.nature.com/articles/s41587-019-0336-3 (Nature Biotechnology 2019) · https://github.com/KrishnaswamyLab/PHATE · type: paper/docs · date: 2019

- **densMAP — density-preserving UMAP**  [NEW]  (confidence: verified)
  - Summary: Narayan, Berger, Cho. Augments UMAP's objective with a local-density distortion term so visual spacing reflects true local density (standard UMAP/t-SNE give dense subsets *too much* visual space). Shipped inside umap-learn: `UMAP(densmap=True, dens_lambda=2.0)`; ~30–50% slower; supervised variant exists.
  - Why relevant: concrete, in-package modern UMAP variant for s04; teaches that "cluster area on a UMAP plot is not density" — a reading caveat that also feeds s06.
  - Source: https://umap-learn.readthedocs.io/en/latest/densmap_demo.html · paper https://www.nature.com/articles/s41587-020-00801-7 (Nature Biotechnology 2021) · type: docs/paper · date: 2021

- **DREAMS and PCC — 2025–2026 "preserve both scales" methods**  [NEW]  (confidence: verified)
  - Summary: **DREAMS** (Kury, Kobak, Damrich, TMLR 2026): combines t-SNE local preservation with PCA global preservation via a simple regularizer, producing a *spectrum* of embeddings across scales; beats prior methods on 11 datasets. **PCC** (Gildenblat & Pahnke, 2025): optimizes Pearson/Spearman distance-correlation (global) + cluster separability (local); its correlation objective can be bolted onto UMAP to improve global structure with minimal local loss.
  - Why relevant: shows s04 readers the field is actively converging on "local+global" objectives in 2025–2026; cite as "the frontier," not as a teaching default.
  - Source: https://arxiv.org/abs/2508.13747 (DREAMS) · https://arxiv.org/abs/2503.07609 (PCC) · type: paper · date: 2025–2026

- **Spectral methods: Laplacian eigenmaps / diffusion maps (scikit-learn `SpectralEmbedding`)**  [NEW]  (confidence: verified)
  - Summary: sklearn's manifold module includes Isomap (geodesic), LLE/MLLE/HLLE/LTSA, and **SpectralEmbedding = Laplacian eigenmaps** (eigendecomposition of the graph Laplacian; minimizes a graph-based cost so manifold-near points stay near). Diffusion maps extend this via random-walk/heat-diffusion on the graph. Caveats it flags: scale features first (NN-based), noise can "short-circuit" the manifold, results are non-deterministic.
  - Why relevant: the drafts jump straight to t-SNE/UMAP; the spectral family is the conceptual bridge (and the ancestor of UMAP's graph view, and of Node2Vec/GNN spectral intuition in Ch 13). Explicit priority topic.
  - Source: https://scikit-learn.org/stable/modules/manifold.html · survey https://arxiv.org/abs/2106.02154 · type: docs/paper · date: current / 2021

- **"How to Use t-SNE Effectively" (distill.pub) — canonical reading guide**  [REFRESH]  (confidence: verified)
  - Summary: Wattenberg, Viégas, Johnson. Five pitfalls: perplexity changes everything; **cluster sizes are meaningless** (t-SNE equalizes density); **inter-cluster distances often meaningless**; random noise can look clustered at low perplexity; topology needs multiple perplexities.
  - Why relevant: the visual, intuition-first reference for s04 and s06's "don't over-read the plot" message.
  - Source: https://distill.pub/2016/misread-tsne/ · type: blog (peer-reviewed) · date: 2016

### ch08_s05 — Autoencoders as learned compression

- **From Autoencoder to β-VAE (Lil'Log) — the full autoencoder family**  [NEW]  (confidence: verified)
  - Summary: Lilian Weng's reference progression: vanilla AE → **denoising AE** (corrupt input, learn robust features) → **sparse AE** (KL sparsity penalty, ~interpretable units) → **contractive AE** (Jacobian-Frobenius penalty for stability) → **VAE** (encode a *distribution* $q(z|x)$, ELBO = reconstruction + KL, reparameterization trick) → **β-VAE** (weight the KL by β>1 to encourage *disentangled* latent factors at some reconstruction cost).
  - Why relevant: the draft only has the vanilla AE. This gives s05 the variant menu and the bridge to "what makes a latent representation good" (robustness, sparsity, disentanglement) — all still *your-own-data*, preserving the Ch 8↔Ch 15 line.
  - Source: https://lilianweng.github.io/posts/2018-08-12-vae/ · type: blog · date: 2018 (canonical, still current)

- **VAE / β-VAE / disentanglement — current research (2024–2025)**  [NEW]  (confidence: verified)
  - Summary: Active line refining the β disentanglement–reconstruction trade-off: **L-VAE** (learns the loss-term weights instead of fixing β; arXiv 2507.02619), **Denoising Multi-β VAE** (one VAE across a range of β; 2507.06613), and β-VAE + diffusion-feedback distillation (2402.02346). Theme: disentangled latents aid both discrimination and generation.
  - Why relevant: lets s05 gesture at the modern frontier of *learned, structured* latent spaces (recency hook) without leaving the compress-your-own-data scope.
  - Source: https://arxiv.org/abs/2507.02619 · https://arxiv.org/abs/2507.06613 · https://arxiv.org/abs/2402.02346 · type: paper · date: 2024–2025

- **Parametric UMAP — a UMAP/autoencoder hybrid with inductive transform**  [NEW]  (confidence: verified)
  - Summary: Replaces UMAP's direct embedding optimization with a **neural network encoder** trained on the UMAP objective. Benefits: fast embedding of *new* data (true inductive `transform`), optional decoder for inverse/reconstruction, an **autoencoder variant** (joint UMAP + reconstruction loss), and semi-supervised support. Keras/TensorFlow backend; default 3×100 MLP.
  - Why relevant: bridges s04↔s05↔s06. It directly answers s04's correct caveat that t-SNE/UMAP are transductive and "sulit dipakai untuk inference" — parametric UMAP is the parametric escape hatch. Also a clean example that the AE↔manifold boundary is porous.
  - Source: https://umap-learn.readthedocs.io/en/latest/parametric_umap.html · paper (Sainburg, McInnes, Gentner) https://direct.mit.edu/neco/article/33/11/2881/107068 · type: docs/paper · date: umap-learn v0.5.8 / Neural Computation 2021

### ch08_s06 — Using reduced representations well + boundary with Ch 15

- **"Stop Misusing t-SNE and UMAP for Visual Analytics" — hard evidence for the misuse subsection**  [NEW]  (confidence: verified)
  - Summary: Jeon, Park, Shin, Seo. Reviewed **136 papers**: practitioners routinely read inter-cluster relationships off t-SNE/UMAP even though those projections "do not faithfully reflect the original distances between clusters." Root cause = low DR literacy; prior fixes failed; they argue for auto-selecting/validating projections.
  - Why relevant: a citable, recent, quantitative backbone for s06's Misuse #1 — exactly the "kesalahan umum" the subsection is built around. Strongest single new source for this subsection.
  - Source: https://arxiv.org/abs/2506.08725 · type: paper · date: 2025

- **Compress-your-own-(pretrained)-embeddings with PCA, not UMAP/AE**  [NEW]  (confidence: verified)
  - Summary: For *downstream-preserving* compression of high-dim embeddings, PCA/KPCA retain performance under heavy reduction while UMAP and autoencoders degrade it badly (retrieval study); PCA can halve dims with no loss. Whitening helps similarity but hurts classification (see s02).
  - Why relevant: sharpens s06's boundary discussion with a concrete rule — "to *use* a reduced representation downstream, pick a distance-faithful linear method; reserve UMAP/t-SNE for the eye." Also the practical RAG angle (storage/quantization).
  - Source: https://arxiv.org/abs/2403.14001 · RAG context https://arxiv.org/pdf/2505.00105 · type: paper · date: 2024–2025

- **Leakage-safe DR = a fitted transformer inside the CV/pipeline**  [REFRESH]  (confidence: verified)
  - Summary: Reinforces the draft's Misuse #2: DR is a fitted estimator (`fit` on train only, `transform` test) and belongs *inside* the sklearn Pipeline/cross-validation, exactly like a scaler. Parametric models (PCA, parametric UMAP) make the train→inference contract explicit; transductive t-SNE/UMAP do not, which is itself a reason they're poor preprocessors.
  - Why relevant: ties s06 back to Ch 2 (pipeline discipline) with the modern parametric-vs-transductive framing.
  - Source: https://scikit-learn.org/stable/modules/decomposition.html · https://umap-learn.readthedocs.io/en/latest/transform.html · type: docs · date: current

### ch08_s07 — Case study: PCA & autoencoder on high-dimensional data

- **Caveat the draft's conclusion: autoencoder does NOT always beat PCA**  [NEW]  (confidence: verified)
  - Summary: AE wins when structure is genuinely nonlinear/curved *and* data is plentiful; **PCA wins (or ties) on small datasets, near-linear data, when interpretability/compute matter, and is far cheaper** — AEs overfit and need much more data when randomly initialized. Hybrid: **PCA-boosted autoencoders** initialize/seed the AE with PCA to win in low-data regimes.
  - Why relevant: s07 currently asserts the AE wins on downstream accuracy. The honest case-study framing is "it depends on nonlinearity + sample size"; this gives the comparison its trade-off backbone and an extra hybrid variant to mention.
  - Source: https://arxiv.org/pdf/2205.11673 (PCA-Boosted Autoencoders, low-data regimes) · practitioner overview https://medium.com/@hassaanidrees7/autoencoders-vs-pca-dimensionality-reduction-for-complex-data-e07d4612b711 · type: paper/blog · date: 2022 / current
  - Cross-ref: the sentence-embedding result (s02/s06) is a concrete case where PCA > AE > UMAP for downstream retention.

## Cross-cutting / chapter-level new developments

- **Reproducibility & stochasticity** [NEW, verified] — t-SNE/UMAP/PaCMAP are stochastic; fixed seeds, PCA initialization, and ensemble+Procrustes alignment are the current reproducibility levers. (Wani 2025, PeerJ CS.)
- **Privacy & fairness of DR** [NEW, verified] — PCA and autoencoders are (approximately) **reversible**, so a "compressed" matrix can leak; DR can **propagate bias** from inputs. Differential-privacy variants exist (DP-PCA, DP-UMAP). Forward-links cleanly to Ch 9 (sensitive/proxy features) and Ch 17. (Wani 2025.)
- **Topological Data Analysis (TDA) / persistent homology** [NEW, verified] — `giotto-tda` (Tauzin et al., JMLR 2021) is a scikit-learn-compatible toolkit that turns raw data → persistence diagrams → ML feature vectors (persistence landscapes/images/statistics). A *different philosophy* of "latent structure" (shape/holes/connected components) than variance-based DR; an optional advanced sidebar, and a candidate Appendix-D term. Source: https://www.jmlr.org/papers/volume22/20-325/20-325.pdf · 2024 review: https://pmc.ncbi.nlm.nih.gov/articles/PMC12931839/
- **The "local vs. global" axis as the chapter's organizing tension** [framing] — PCA/MDS = global/metric-faithful; t-SNE/UMAP = local; PaCMAP/TriMap/DREAMS/PCC = both. A single comparison table (method × local? × global? × parametric/inductive? × deterministic?) would serve s04 and s06 well.

## Candidate new terms (for Living Glossary / Appendix D)
- **PaCMAP** (Pairwise Controlled Manifold Approximation Projection) — near/mid-near/further pairs.
- **TriMap** — triplet-based, global-structure-preserving DR.
- **PHATE** — diffusion/heat-potential embedding for trajectories.
- **densMAP** — density-preserving UMAP.
- **DREAMS / PCC** — 2025–2026 local+global methods.
- **Parametric UMAP** — neural-network UMAP with inductive `transform`.
- **Laplacian eigenmaps / Spectral embedding**, **diffusion maps** — spectral DR family.
- **Variational autoencoder (VAE)**, **β-VAE**, **disentangled representation** — structured learned latents.
- **Denoising / sparse / contractive autoencoder** — autoencoder regularization variants.
- **β-divergence** (Frobenius / Kullback–Leibler / Itakura–Saito) — NMF objective family.
- **MiniBatchNMF**, **IncrementalPCA**, **randomized SVD** — scalable/streaming variants.
- **Whitening / anisotropy / isotropy** — embedding-geometry post-processing.
- **Intrinsic dimensionality** (TwoNN, DANCo); **parallel analysis** — choosing $k$.
- **Persistent homology / Topological Data Analysis (TDA)** — shape-based features.
- **Robust PCA** (low-rank + sparse decomposition); **DP-PCA / DP-UMAP** (differentially private DR).
- **Transductive vs. inductive (parametric) embedding** — can it transform new samples at inference?

## Source list
- [1] Stop Misusing t-SNE and UMAP for Visual Analytics — https://arxiv.org/abs/2506.08725 (paper, 2025)
- [2] Comprehensive review of dimensionality reduction algorithms (Wani) — https://peerj.com/articles/cs-3025/ · https://pmc.ncbi.nlm.nih.gov/articles/PMC12453773/ (review, PeerJ CS 2025)
- [3] PaCMAP — Understanding how DR tools work — https://arxiv.org/abs/2012.04456 (paper, JMLR 2021)
- [4] TriMap: Large-scale DR Using Triplets — https://arxiv.org/abs/1910.00204 (paper, 2019)
- [5] PHATE (Nature Biotechnology) — https://www.nature.com/articles/s41587-019-0336-3 · https://github.com/KrishnaswamyLab/PHATE (paper/docs, 2019)
- [6] densMAP (umap-learn docs) — https://umap-learn.readthedocs.io/en/latest/densmap_demo.html · paper https://www.nature.com/articles/s41587-020-00801-7 (docs/paper, 2021)
- [7] DREAMS — https://arxiv.org/abs/2508.13747 (paper, TMLR 2026)
- [8] PCC: Preserving Clusters and Correlations — https://arxiv.org/abs/2503.07609 (paper, 2025)
- [9] UMAP — https://arxiv.org/abs/1802.03426 · https://joss.theoj.org/papers/10.21105/joss.00861 (paper/software, 2018)
- [10] UMAP does not preserve global structure better than t-SNE (init critique) — https://www.biorxiv.org/content/10.1101/2019.12.19.877522v1 (paper, 2019)
- [11] How to Use t-SNE Effectively (Distill) — https://distill.pub/2016/misread-tsne/ (blog, 2016)
- [12] scikit-learn manifold learning — https://scikit-learn.org/stable/modules/manifold.html (docs, current)
- [13] scikit-learn decomposition (PCA/IncrementalPCA/TruncatedSVD/NMF) — https://scikit-learn.org/stable/modules/decomposition.html (docs, current)
- [14] scikit-learn MiniBatchNMF — https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.MiniBatchNMF.html (docs, current)
- [15] Parametric UMAP (umap-learn docs) — https://umap-learn.readthedocs.io/en/latest/parametric_umap.html · paper https://direct.mit.edu/neco/article/33/11/2881/107068 (docs/paper, v0.5.8 / 2021)
- [16] From Autoencoder to Beta-VAE (Lil'Log) — https://lilianweng.github.io/posts/2018-08-12-vae/ (blog, 2018)
- [17] L-VAE / Multi-β VAE / β-VAE distillation — https://arxiv.org/abs/2507.02619 · https://arxiv.org/abs/2507.06613 · https://arxiv.org/abs/2402.02346 (papers, 2024–2025)
- [18] Evaluating Unsupervised DR for Pretrained Sentence Embeddings — https://arxiv.org/abs/2403.14001 (paper, LREC-COLING 2024)
- [19] Whitening Not Recommended for Classification in LLMs — https://arxiv.org/pdf/2407.12886 (paper, 2024)
- [20] RAG embedding storage: quantization + DR — https://arxiv.org/pdf/2505.00105 (paper, 2025)
- [21] PCA-Boosted Autoencoders (low-data regimes) — https://arxiv.org/pdf/2205.11673 (paper, 2022)
- [22] giotto-tda — https://www.jmlr.org/papers/volume22/20-325/20-325.pdf (paper, JMLR 2021) · TDA review https://pmc.ncbi.nlm.nih.gov/articles/PMC12931839/ (2024)
- [23] Laplacian-based DR / spectral & diffusion maps (tutorial-survey) — https://arxiv.org/abs/2106.02154 (paper, 2021)
- [24] Comprehensive evaluation of DR for transcriptomic data — https://www.nature.com/articles/s42003-022-03628-x (paper, Comm Biology 2022)
- [25] Autoencoders vs PCA (practitioner overview) — https://medium.com/@hassaanidrees7/autoencoders-vs-pca-dimensionality-reduction-for-complex-data-e07d4612b711 (blog, current)
