---
chapter: ch13
title: Spatial & Graph Data
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 13 Resources — Spatial & Graph Data

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence). "verified" = a source was fetched and the claim checked against its text; "uncertain" = taken from a search-result snippet only, not the full source.

## Coverage baseline (what the drafts already have)
- **Spatial half (s01–s03).** s01: lat/lon as weak raw features, CRS (WGS84 → UTM), Haversine vs Euclidean, distance + proximity features. s02: Tobler's First Law, spatial autocorrelation, spatial lag (weighted neighbor average), KNN/radius/postcode neighbor definitions. s03: spatial target leakage from autocorrelation, why random k-fold inflates scores, spatial **block** cross-validation, deforestation pixel example.
- **Graph half (s04–s08).** s04: degree/in-/out-degree, centrality (PageRank, betweenness), clustering coefficient; "designed" graph features. s05: neighborhood aggregation (mean/sum/max), path-based features (shortest path, common neighbors), recommender example; explicitly framed as the manual precursor to GNN message passing. s06: Node2Vec — biased random walk with p/q (BFS↔DFS), Word2Vec/skip-gram objective, two LaTeX equations, citation-network example. s07: GNN message passing, one mean-aggregation update equation, multi-layer receptive field, molecule-toxicity example. s08: graph leakage via edges crossing the split, transductive vs inductive, temporal splits, fraud-network example.
- **Case study (s09).** House-price (raw coords → distance/spatial-lag + spatial block CV) and citation-network node classification (degree baseline → Node2Vec → GNN).
- **Notable gaps the drafts do NOT cover:** attention-based GNNs (GAT/GATv2); over-smoothing/over-squashing (why "deeper GNN" is not free); heterogeneous/relational GNNs (R-GCN, HGT); knowledge-graph embeddings (TransE/RotatE/ComplEx/DistMult); equivariant GNNs for 3D/molecules; spatio-temporal/dynamic GNNs; GraphSAGE inductive sampling as the named bridge between s05 aggregation and s07; concrete tooling (PyTorch Geometric, NetworkX, PySAL/esda, spacv, H3); LISA/local Moran's I and Getis-Ord as engineered spatial features; the inductive-split leakage subtleties (duplicate nodes, negative-sampling leakage in link prediction).

## Resources by subsection

### ch13_s01 — Spatial: coordinates, reference systems, distance & proximity
- **Uber H3 — hexagonal hierarchical spatial indexing as a feature/aggregation primitive**  [NEW]  (confidence: verified)
  - Summary: H3 tiles the globe with hexagons across 16 resolution levels; every cell has a single centerpoint-to-neighbor distance (vs two for squares, three for triangles), so adjacency and movement are cleaner. `latLngToCell` maps a lat/lon to a 64-bit cell id; coarser ancestors are obtained by truncation; `gridDisk`/kRing gives ring neighborhoods. Open source (C core; Python/JS/Go/Java bindings).
  - Why relevant: a modern, very common way to turn raw coordinates into categorical/aggregation features (counts, densities, target means per cell) — a concrete upgrade to the draft's "raw lat/lon is weak" point, and a clean unit for spatial joins. Pairs naturally with the proximity-feature idea.
  - Source: https://www.uber.com/us/en/blog/h3/ · type: blog/docs · date: (system in active use; bindings current 2024–2025)
- **CRS / projection discipline: WGS84 (EPSG:4326) → projected UTM for metric distance**  [REFRESH]  (confidence: verified)
  - Summary: confirms the draft's CRS framing; standard practice is geopandas/pyproj `to_crs` to a projected CRS before computing Euclidean distances, else use Haversine/geodesic on the sphere. Mixing degrees with Euclidean math is a classic silent bug.
  - Why relevant: reinforces s01's CRS section with the current tool names (GeoPandas, pyproj) the notebook will use.
  - Source: (corroborated across GeoPandas/PySAL ecosystem docs surfaced in searches) · type: docs · date: 2024–2025
- **Note:** distance-to-landmark and proximity-count features (draft's core) are canonical and well-supported; no contradicting evidence found.

### ch13_s02 — Neighborhood features and spatial autocorrelation
- **PySAL / esda: Moran's I and LISA (Local Moran's I) as engineered features**  [NEW]  (confidence: verified)
  - Summary: `esda.Moran` gives the global statistic; `esda.Moran_Local` (LISA) returns a per-observation local statistic, a pseudo p-value (`p_sim`), and a quadrant label `q` (1=HH hot spot, 2=LH doughnut/outlier, 3=LL cold spot, 4=HL diamond/outlier). Spatial weights come from `libpysal` (Queen/Rook contiguity, KNN, distance-band). Getis-Ord `G_i`/`G_i*` give hot/cold concentration.
  - Why relevant: extends s02 beyond the single "spatial lag" feature — LISA cluster type, significance flag, and local-I value are directly usable columns that encode local structure for a non-spatial model. Gives the chapter named, current tooling.
  - Source: https://geographicdata.science/book/notebooks/07_local_autocorrelation.html · type: book/docs (Rey, Arribas-Bel, Wolf — *Geographic Data Science with Python*) · date: 2023–2025 online edition
- **Spatial lag = the simplest neighborhood feature; weights matrix is the design choice**  [REFRESH]  (confidence: verified)
  - Summary: corroborates the draft's spatial-lag definition and adds that the *weights matrix* (contiguity vs KNN vs distance band, row-standardized or not) is the real modeling lever; the same `W` is reused for autocorrelation tests and lag features.
  - Why relevant: tightens s02's "definition of neighbor can be adjusted" sentence into concrete, reproducible choices.
  - Source: http://darribas.org/gds19/content/labs/lab_06.html · type: course/docs · date: 2019 (canonical, still standard)

### ch13_s03 — Spatial leakage and spatial cross-validation
- **`spacv` — spatial cross-validation in Python (sklearn-compatible)**  [NEW]  (confidence: verified)
  - Summary: provides SKCV (spatial K-fold with spatially explicit blocks) and a configurable **buffer / "dead zone"** that removes training points within a radius of the test fold, preventing near-neighbor bleed. sklearn-style `split()` integrates with `cross_val_score`. Depends on geopandas/shapely + numpy/pandas/scipy/sklearn.
  - Why relevant: gives s03 (and the s09 `[KODE]` placeholder) a real, citable implementation of "block + buffer" beyond the conceptual figure. Directly supports the spatial-block CV the draft describes.
  - Source: https://github.com/SamComber/spacv · type: docs/repo · date: current package
- **Tooling landscape + the buffer rationale (scikit-learn how-to)**  [NEW]  (confidence: verified)
  - Summary: a practical walk-through showing why random CV leaks under spatial autocorrelation and how to build geographic folds with sklearn; names the broader ecosystem — `mlr3spatiotempcv`, `blockCV`, `sperrorest`, `spatialsample` (R) and `spacv` (Python). Spatial leave-one-out adds a buffer so points in the dead zone are excluded from training.
  - Why relevant: lets the chapter mention that this is standard, tool-supported practice (not a bespoke trick), and points readers to language-appropriate tools.
  - Source: https://towardsdatascience.com/spatial-cross-validation-using-scikit-learn-74cb8ffe0ab9/ · type: blog · date: 2023 (current)
- **Real-domain spatial-leakage evidence (soil mapping, marine RS)**  [NEW]  (confidence: uncertain)
  - Summary: recent applied papers document inflated CV scores from spatial leakage and argue for blocked/leave-profile-out CV: a 3D digital-soil-mapping study (leave-profile-out CV) and a 2025 marine remote-sensing study on *choosing block size* for spatial CV.
  - Why relevant: backs s03's claim with 2024–2025 domain evidence beyond the deforestation toy example; the "how big should a block be" question is a good nuance.
  - Source: https://www.sciencedirect.com/science/article/pii/S0016706125000618 ; https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2025.1531097/full · type: paper · date: 2025

### ch13_s04 — Graph: degree, centrality, clustering features
- **NetworkX as the canonical handcrafted-feature toolkit**  [NEW]  (confidence: verified)
  - Summary: degree/in-/out-degree, `pagerank`, `betweenness_centrality`, `closeness_centrality`, `clustering` (local clustering coefficient) are all one-call functions; these are exactly the s04 features and the implementation the notebook should use. (Canonical, stable API.)
  - Why relevant: grounds s04's "designed graph features" in the standard tool; nothing in the draft needs correction, just a named library.
  - Source: NetworkX algorithms docs (centrality, clustering) · type: docs · date: current (NetworkX 3.x, 2024–2025)
- **Centrality framing is sound; note degree-vs-position distinction is standard**  [REFRESH]  (confidence: verified)
  - Summary: the draft's contrast (degree = local activity; betweenness = bridge/flow control; PageRank = recursive authority) matches textbook treatments; clustering coefficient = fraction of a node's neighbor-pairs that are themselves connected.
  - Why relevant: confirms accuracy of s04 definitions.
  - Source: https://epichka.com/blog/2023/gat-paper-explained/ (background) and standard graph-ML references · type: blog/docs · date: 2023

### ch13_s05 — Neighborhood aggregation and path-based features
- **GraphSAGE: the named bridge from manual aggregation (s05) to learned message passing (s07)**  [NEW]  (confidence: verified)
  - Summary: GraphSAGE learns an *aggregation function* (mean / pooling / LSTM aggregators) over a **fixed-size sampled neighborhood** rather than a per-node embedding, so it generalizes to unseen nodes (inductive). It is literally "neighborhood aggregation, but learned and sampled."
  - Why relevant: s05's whole arc is "manual neighbor aggregation → automatic message passing." GraphSAGE is the canonical intermediate concept that makes the transition explicit and motivates *sampling* (why you can't aggregate all neighbors at scale). Strengthens the s05→s07 hand-off.
  - Source: https://arxiv.org/abs/1706.02216 (Hamilton, Ying, Leskovec) · type: paper · date: NeurIPS 2017
- **Path/structure link-prediction features (common neighbors, Adamic–Adar, shortest path)**  [REFRESH]  (confidence: verified)
  - Summary: the draft's "common neighbors / shortest path" features are the classic link-prediction heuristics; NetworkX exposes `common_neighbors`, `jaccard_coefficient`, `adamic_adar_index`, `shortest_path_length`. Worth naming Adamic–Adar as the weighted refinement of common-neighbor counts.
  - Why relevant: adds one concrete, named feature (Adamic–Adar) to s05's path-based discussion without new theory.
  - Source: NetworkX link-prediction docs · type: docs · date: current

### ch13_s06 — Node embeddings (Node2Vec) 🔢
- **Node2Vec lineage and the p/q intuition (DeepWalk → Node2Vec)**  [REFRESH]  (confidence: verified)
  - Summary: DeepWalk = uniform random walks + skip-gram; Node2Vec adds the **biased** walk with return parameter `p` and in-out parameter `q`, interpolating BFS (homophily / community) ↔ DFS (structural equivalence / roles). The draft already has both equations; the key added nuance is the homophily-vs-structural-equivalence framing of what the embedding captures.
  - Why relevant: sharpens s06's interpretation of *why* p/q matter (what kind of similarity the vectors encode), which the current draft states only implicitly.
  - Source: https://arxiv.org/abs/1607.00653 (Grover & Leskovec, node2vec, KDD 2016); DeepWalk (Perozzi et al., 2014) · type: paper · date: 2014–2016 (canonical)
- **Limitation that motivates s07: random-walk embeddings ignore node attributes and are transductive**  [NEW]  (confidence: verified)
  - Summary: Node2Vec/DeepWalk learn a lookup table of vectors purely from topology — they cannot use node features and cannot embed a node unseen at training time. This is exactly the gap GraphSAGE/GNNs fill.
  - Why relevant: the draft's s07 opens with "random walks ignore node attributes"; this item documents the second, equally important limitation (transductive only / no new nodes), reinforcing the pivot to learned, inductive methods.
  - Source: https://arxiv.org/abs/1706.02216 (motivation section) · type: paper · date: 2017

### ch13_s07 — GNNs as representation learners 🔢
- **Graph Attention Networks (GAT) and GATv2: learned, query-dependent neighbor weights**  [NEW]  (confidence: verified)
  - Summary: GAT replaces GCN's fixed degree-based normalization with a learned attention coefficient per edge: `e_ij = LeakyReLU(aᵀ[W h_i ‖ W h_j])`, softmax-normalized over neighbors, with multi-head attention. **GATv2** fixes GAT's "static attention" (every node ranks neighbors the same way) by reordering the nonlinearity to give **dynamic, query-conditioned** attention — a near-free drop-in (same asymptotic cost) that helps especially on heterophilic graphs.
  - Why relevant: the single biggest modern omission in s07. The draft shows only mean aggregation; GAT/GATv2 is the natural "weighted aggregation, learned" extension and is standard in current practice/PyG.
  - Source: GAT — Veličković et al., arXiv:1710.10903 (ICLR 2018); GATv2 — Brody, Alon, Yahav, arXiv:2105.14491; summary verified at https://www.emergentmind.com/topics/graph-attention-network-v2-gatv2 and https://epichka.com/blog/2023/gat-paper-explained/ · type: paper/blog · date: 2018 / 2021 (variants 2024–2025: DeepGAT, GATE)
- **Over-smoothing and over-squashing: why "just stack more GNN layers" fails (2024 survey)**  [NEW]  (confidence: verified)
  - Summary: **Over-smoothing** — node representations collapse toward each other as depth grows (tied to the graph Laplacian's small spectral gap). **Over-squashing** — long-range information gets crushed through bottleneck edges/low-curvature "narrow passages." Fixes: graph **rewiring** (SDRF, BORF, FoSR), **normalization** (PairNorm), **DropEdge**, residual / Jumping-Knowledge connections, and graph transformers (global attention). There is a fundamental trade-off — easing one tends to worsen the other.
  - Why relevant: critical caveat for s07's "deeper network = wider context" sentence, which currently reads as unambiguously good. This is the modern, honest counterweight and a great "why/trade-off" discussion.
  - Source: https://arxiv.org/pdf/2411.17429 (Attali, Buscaldi, Pernelle, Malliaros — rewiring survey); also over-squashing survey arXiv:2308.15568; trade-off arXiv:2212.02374 · type: paper · date: 2024
- **Heterogeneous & relational GNNs: R-GCN and HGT (Heterogeneous Graph Transformer)**  [NEW]  (confidence: verified)
  - Summary: real graphs have multiple node/edge types. **R-GCN** keeps a separate weight matrix per relation type; **HGT** uses node-/edge-type-specific Transformer attention and scales via neighbor sampling; HAN/GTN use meta-paths. Recent scalable variants (SeHGNN, NARS, H2SGNN) separate propagation from transformation for million-node graphs.
  - Why relevant: most applied graphs (citation, e-commerce, knowledge graphs) are heterogeneous; mentioning R-GCN/HGT keeps s07 from implying all graphs are single-type. Ties to the s09 citation case (papers, authors, venues = different node types).
  - Source: https://www.emergentmind.com/topics/heterogeneous-graph-neural-networks-gnns ; HGT — Hu et al., arXiv:2003.01332 ; R-GCN — Schlichtkrull et al. 2017 · type: docs/paper · date: 2017–2024
- **E(n)-equivariant GNNs (EGNN) for 3D / molecular / spatial geometry**  [NEW]  (confidence: verified)
  - Summary: EGNN updates node features *and* coordinates so outputs are equivariant to rotation/translation/reflection/permutation, without expensive spherical-harmonic layers. Strong on molecular property prediction and dynamical systems — and it is the natural meeting point of the chapter's two halves (geometry + graphs).
  - Why relevant: optional but high-value bridge between the spatial and graph halves; the molecule-toxicity example in s07 is exactly a geometric-graph problem where equivariance matters.
  - Source: https://arxiv.org/abs/2102.09844 (Satorras, Hoogeboom, Welling) · type: paper · date: 2021
- **PyTorch Geometric — the implementation substrate**  [NEW]  (confidence: verified)
  - Summary: PyG's `Data` object holds `x` (node features), `edge_index` (COO connectivity), `edge_attr`, `y`; layers like `GCNConv`, `SAGEConv`, `GATConv`, `GATv2Conv` are drop-in; built-in `Planetoid` datasets (Cora/Citeseer/Pubmed); `DataLoader` mini-batches graphs as block-diagonal adjacency. A 2-layer GCN reaches ~81.5% on Cora. DGL is the analogous alternative with first-class heterograph support (`multi_update_all`).
  - Why relevant: gives s07 and the s09 notebook a current, named API (GATv2Conv/SAGEConv) and a verified benchmark number for the case study.
  - Source: https://pytorch-geometric.readthedocs.io/en/2.6.1/get_started/introduction.html ; DGL: https://www.dgl.ai/dgl_docs/guide/message-heterograph.html · type: docs · date: PyG 2.6.x (2024–2025)
- **Bronstein — "Beyond Message Passing" (limits of MPNNs)**  [NEW]  (confidence: verified)
  - Summary: message passing is the GNN workhorse but is bounded by the Weisfeiler–Lehman test (can't even count triangles/rings reliably) and suffers over-squashing; physics-inspired "continuous" GNNs (diffusion/gradient-flow PDEs) are an alternative research direction.
  - Why relevant: optional depth for s07's framing of GNNs as automated aggregation — names the theoretical ceiling (WL test) in plain terms.
  - Source: https://thegradient.pub/graph-neural-networks-beyond-message-passing-and-weisfeiler-lehman/ · type: blog · date: 2022 (Michael Bronstein)

### ch13_s08 — Leakage on graphs
- **Transductive vs inductive splits made precise + concrete pitfalls**  [REFRESH]  (confidence: verified)
  - Summary: tabular splits assume row independence; graph splits break it because edges cross the boundary, so a test node's features/label flow into a training node via aggregation/message passing. Transductive = whole topology visible, only test *labels* masked; inductive = train on a subgraph, evaluate on a physically disconnected subgraph. Pitfall: even "inductive" benchmarks have been found to contain ~5% duplicated nodes/edges/labels across splits, silently violating the assumption.
  - Why relevant: corroborates s08 and adds the duplicate-node finding plus the canonical evaluation-pitfalls reference (Shchur et al., "Pitfalls of GNN Evaluation," 2018).
  - Source: Shchur et al. 2018 (arXiv:1811.05868); fully-inductive node classification arXiv:2405.20445 (2024) · type: paper · date: 2018 / 2024
- **PyTorch Geometric `RandomLinkSplit` / `RandomNodeSplit`: leakage-aware splitting in code**  [NEW]  (confidence: verified)
  - Summary: `RandomLinkSplit` does an edge-level train/val/test split where train excludes val/test edges and val excludes test edges; `disjoint_train_ratio` separates message-passing edges from supervision edges; `is_undirected=True` prevents reverse-edge leakage; `add_negative_train_samples`/`neg_sampling_ratio` handle negatives. (Negative-sampling leakage — reusing the same negatives, or sampling them after the split — is a real link-prediction footgun.)
  - Why relevant: turns s08's abstract "cut the edges before aggregation" into the exact, current tooling and surfaces link-prediction-specific leakage (negative sampling), which the draft omits.
  - Source: https://pytorch-geometric.readthedocs.io/en/latest/_modules/torch_geometric/transforms/random_link_split.html · type: docs · date: PyG 2.5–2.6 (2024–2025)
- **Temporal splits for growing graphs (corroboration)**  [REFRESH]  (confidence: verified)
  - Summary: matches the draft's temporal-split recommendation; in dynamic-graph benchmarks the standard is "train on edges/nodes up to time T, evaluate after T," which is also the only way to respect feature-availability for streaming graphs.
  - Why relevant: backs s08's temporal-split paragraph with the dynamic-GNN literature (see cross-cutting).
  - Source: https://arxiv.org/abs/2405.00476 · type: paper · date: 2024

### ch13_s09 — Case study: location-based prediction & node classification
- **Cora citation network as the canonical node-classification case (with PyG)**  [REFRESH]  (confidence: verified)
  - Summary: Cora = 2,708 papers, 1,433 bag-of-words features, 7 classes, with standard train/val/test masks built into PyG `Planetoid`. A 2-layer GCN gets ~81.5% — a clean, reproducible target for the s09 graph half (degree baseline → Node2Vec → GCN/GAT).
  - Why relevant: gives the case study a concrete, well-known dataset and an honest benchmark number; matches the draft's "citation network" framing exactly.
  - Source: https://pytorch-geometric.readthedocs.io/en/2.6.1/get_started/introduction.html · type: docs · date: PyG 2.6.x
- **Spatial half: `spacv` block+buffer CV for the house-price example**  [REFRESH]  (confidence: verified)
  - Summary: implements the `[KODE: spatial block cross-validation]` placeholder directly; SKCV + buffer is the precise mechanism behind the draft's "train north, test south" narrative.
  - Why relevant: the case study's code callout has a ready library; also supports comparing random-CV vs spatial-CV scores to *show* the leakage gap.
  - Source: https://github.com/SamComber/spacv · type: docs/repo · date: current

## Cross-cutting / chapter-level new developments
- **Knowledge-graph embeddings (TransE, DistMult, ComplEx, RotatE)**  [NEW]  (confidence: verified)
  - A whole family adjacent to s06's node embeddings but for *typed* (entity, relation, entity) triples. **TransE**: relation as translation `h + r ≈ t` (fails on symmetric/1-to-many). **DistMult**: bilinear, only symmetric relations. **ComplEx**: complex embeddings, handles asymmetry. **RotatE** (Sun et al., ICLR 2019): relation = rotation in complex space, models symmetry/antisymmetry + inversion + composition, trained with self-adversarial negative sampling. Good optional sidebar showing the "designed scoring function vs learned embedding" spectrum on relational data.
  - Source: https://arxiv.org/abs/1902.10197 (RotatE) · type: paper · date: 2019
- **Spatio-temporal / dynamic GNNs**  [NEW]  (confidence: verified)
  - For graphs that evolve in time: discrete-time (snapshot) vs continuous-time models, typically GNN ⊗ (RNN / temporal attention). Benchmarks: traffic forecasting, dynamic link prediction. Directly connects Ch 13 to Ch 10 (time series) and reframes s08's temporal split as a first-class modeling regime.
  - Source: https://arxiv.org/abs/2405.00476 (Feng et al., 2024 survey of 81 models) · type: paper · date: 2024
- **Graph foundation models (GFMs)**  [NEW]  (confidence: verified)
  - 2025 push to bring LLM-style pretraining/transfer to graphs: backbone + self-supervised pretraining + adaptation (fine-tune/prompt), plus LLM+GNN hybrids on text-attributed graphs. Forward-link to Ch 15 (learned/transferred representations). Still early; evaluation/standardization is an open problem.
  - Source: https://arxiv.org/abs/2505.15116 (Wang et al., 2025 survey) · type: paper · date: 2025
- **E(n)-equivariant GNNs as the spatial∩graph meeting point** (see s07) — geometric symmetry baked into the architecture; the clearest example that the two halves of the chapter are not unrelated.

## Candidate new terms (for Living Glossary / Appendix D)
- **Graph Attention Network (GAT) / GATv2** — neighbor aggregation with learned, (GATv2: query-dependent) attention weights. (keep English)
- **Static vs dynamic attention** — GAT ranks neighbors identically for every node (static); GATv2 conditions the ranking on the query node (dynamic).
- **Over-smoothing** (*over-smoothing*) — node embeddings collapse toward indistinguishability as GNN depth grows.
- **Over-squashing** (*over-squashing*) — long-range signal crushed through bottleneck edges; tied to graph curvature.
- **Graph rewiring** — editing edges (SDRF/BORF/FoSR) to relieve over-squashing/over-smoothing.
- **Message passing / MPNN** — already implied in s07; worth a formal glossary entry.
- **GraphSAGE** — inductive embeddings via sampled-neighborhood learned aggregation.
- **Inductive vs transductive learning** — already in s08 brief; promote to glossary.
- **Heterogeneous graph / R-GCN / HGT** — multi-type nodes/edges; relation-specific or typed-attention aggregation.
- **Knowledge-graph embedding (TransE/RotatE/ComplEx/DistMult)** — embeddings of (entity, relation, entity) triples.
- **Equivariant GNN / EGNN** — architecture respecting rotation/translation/reflection symmetry.
- **Spatial autocorrelation; Moran's I; LISA (Local Moran's I); Getis-Ord G** — global vs local measures; LISA quadrants HH/LL/HL/LH.
- **Spatial lag** — already in s02 brief.
- **Spatial (block) cross-validation; buffer / dead zone** — leakage-safe geographic splitting.
- **H3 / hexagonal spatial indexing** — hierarchical hex cells as spatial feature units.
- **Coordinate Reference System (CRS); WGS84; UTM; Haversine** — already in s01 brief.
- **Tobler's First Law** — already in s02.

## Source list
- [1] GATv2 (How Attentive are Graph Attention Networks?) — Brody, Alon, Yahav, arXiv:2105.14491; topic summary https://www.emergentmind.com/topics/graph-attention-network-v2-gatv2 (paper/blog, 2021)
- [2] Graph Attention Networks (original GAT) — Veličković et al., arXiv:1710.10903; explainer https://epichka.com/blog/2023/gat-paper-explained/ (paper/blog, 2018/2023)
- [3] Graph Rewiring to Mitigate Over-Squashing and Over-Smoothing: A Survey — Attali et al., https://arxiv.org/pdf/2411.17429 (paper, 2024)
- [4] Over-Squashing in GNNs: A Comprehensive Survey — arXiv:2308.15568 (paper, 2023/2024)
- [5] Trade-off between Over-smoothing and Over-squashing — arXiv:2212.02374 (paper, 2022, CIKM 2023)
- [6] Heterogeneous Graph Neural Networks (topic) — https://www.emergentmind.com/topics/heterogeneous-graph-neural-networks-gnns ; HGT arXiv:2003.01332 (docs/paper, 2020–2024)
- [7] RotatE: Knowledge Graph Embedding by Relational Rotation — Sun et al., https://arxiv.org/abs/1902.10197 (paper, 2019)
- [8] E(n) Equivariant Graph Neural Networks — Satorras, Hoogeboom, Welling, https://arxiv.org/abs/2102.09844 (paper, 2021)
- [9] GraphSAGE: Inductive Representation Learning on Large Graphs — Hamilton, Ying, Leskovec, https://arxiv.org/abs/1706.02216 (paper, 2017)
- [10] node2vec — Grover & Leskovec, arXiv:1607.00653 (paper, KDD 2016)
- [11] PyTorch Geometric — Introduction by Example — https://pytorch-geometric.readthedocs.io/en/2.6.1/get_started/introduction.html (docs, PyG 2.6.x)
- [12] PyG RandomLinkSplit (source/docs) — https://pytorch-geometric.readthedocs.io/en/latest/_modules/torch_geometric/transforms/random_link_split.html (docs, 2024–2025)
- [13] DGL — Message Passing on Heterogeneous Graphs — https://www.dgl.ai/dgl_docs/guide/message-heterograph.html (docs, current)
- [14] Beyond Message Passing (physics-inspired GNNs) — Michael Bronstein, https://thegradient.pub/graph-neural-networks-beyond-message-passing-and-weisfeiler-lehman/ (blog, 2022)
- [15] Pitfalls of Graph Neural Network Evaluation — Shchur et al., arXiv:1811.05868 (paper, 2018)
- [16] Fully-inductive Node Classification on Arbitrary Graphs — arXiv:2405.20445 (paper, 2024)
- [17] A Comprehensive Survey of Dynamic Graph Neural Networks — Feng et al., https://arxiv.org/abs/2405.00476 (paper, 2024)
- [18] Graph Foundation Models: A Comprehensive Survey — Wang et al., https://arxiv.org/abs/2505.15116 (paper, 2025)
- [19] spacv — Spatial Cross-Validation in Python — https://github.com/SamComber/spacv (docs/repo, current)
- [20] Spatial Cross-Validation using scikit-learn — https://towardsdatascience.com/spatial-cross-validation-using-scikit-learn-74cb8ffe0ab9/ (blog, 2023)
- [21] Local Spatial Autocorrelation (LISA, PySAL/esda) — *Geographic Data Science with Python* (Rey, Arribas-Bel, Wolf), https://geographicdata.science/book/notebooks/07_local_autocorrelation.html (book/docs, 2023–2025)
- [22] PySAL/esda spatial autocorrelation lab — http://darribas.org/gds19/content/labs/lab_06.html (course/docs, 2019)
- [23] Uber H3 — Hexagonal Hierarchical Spatial Index — https://www.uber.com/us/en/blog/h3/ (blog/docs, current)
- [24] Leave-profile-out CV / spatial data leakage in digital soil mapping — https://www.sciencedirect.com/science/article/pii/S0016706125000618 (paper, 2025)
- [25] Choosing blocks for spatial cross-validation (marine RS) — https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2025.1531097/full (paper, 2025)
