---
chapter: ch15
title: Learned Representations & Pretrained Models
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 15 Resources — Learned Representations & Pretrained Models

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence).

## Coverage baseline (what the drafts already have)

- s01: Adaptation spectrum (frozen → partial → full fine-tuning), BERT/ResNet examples, catastrophic forgetting
- s02: Feature banks (conceptual), cosine similarity, dot product, Euclidean distance (basic definitions + equations)
- s03: Linear probing as evaluation, domain shift concept, ImageNet→X-ray example
- s04: Boundary Ch8 vs Ch15 (internal compression vs. external transfer), autoencoder distinction
- s05: Thesis argument: DL shifts FE, doesn't remove it; complementarity of designed + learned
- s06: Tokenization (BPE), data augmentation (flip, jitter), normalisation as surviving FE
- s07: FT-Transformer, TabNet (high-level), gradient boosting comparison (small/medium data wins), deep tabular as feature extractor
- s08: Hybrid models (concatenation of engineered + learned features), real estate example
- s09: Case study: BERT frozen extractor + tabular engineered features → XGBoost (product returns)

---

## Resources by subsection

### ch15_s01 — Embeddings and the adaptation spectrum: from frozen extraction to fine-tuning

- **PEFT ecosystem 2024–2026 (HuggingFace PEFT library)**  [NEW]  (confidence: verified)
  - Summary: The `peft` library (v0.19.0 as of 2026) provides a unified interface for 30+ parameter-efficient methods including LoRA, QLoRA, DoRA, AdaLoRA, IA3, prompt tuning, prefix tuning, adapters, and more. LoRA represents weight updates via low-rank decomposition (two smaller matrices A and B), drastically reducing trainable parameters while maintaining full fine-tuning performance. LoRA adds no inference latency because adapter weights can be merged into the base model.
  - Why relevant: The drafts only cover frozen/partial/full fine-tuning — a pre-2021 taxonomy. PEFT methods (especially LoRA) are now the de facto standard for adapting large models and should be mentioned as a key point on the adaptation spectrum. QLoRA extends this with 4-bit quantization for consumer hardware.
  - Source: https://huggingface.co/docs/peft/main/en/conceptual_guides/lora · type: docs · date: 2024–2026 (ongoing)

- **DoRA: Weight-Decomposed Low-Rank Adaptation (ICML 2024 Oral)**  [NEW]  (confidence: verified)
  - Summary: DoRA decomposes pre-trained weights into magnitude and direction components, applying LoRA only to the directional update. This closes the accuracy gap between LoRA and full fine-tuning without additional inference overhead. Achieves ICML 2024 Oral recognition.
  - Why relevant: Represents the next generation beyond vanilla LoRA. Demonstrates the PEFT landscape is still rapidly evolving with better approaches.
  - Source: https://arxiv.org/abs/2402.09353 · type: paper · date: Feb 2024

### ch15_s02 — Embedding/feature banks and similarity metrics

- **FAISS library (Meta AI) — v1.14.3**  [NEW]  (confidence: verified)
  - Summary: FAISS is the de facto library for efficient similarity search and clustering of dense vectors, with 40.4k GitHub stars. Supports L2, dot product, and cosine similarity. Scales to billions of vectors on a single server using compressed representations (PQ, IVF). GPU implementation available. Latest release June 2026. The 2024 paper (arXiv:2401.08281) provides the canonical reference.
  - Why relevant: The draft mentions "feature banks" conceptually but provides no concrete library. FAISS is the practical bridge between embedding theory and production deployment. Essential for any discussion of "storing and comparing embeddings."
  - Source: https://github.com/facebookresearch/faiss · type: library · date: ongoing (v1.14.3, Jun 2026)

- **sentence-transformers library v5.x**  [NEW]  (confidence: verified)
  - Summary: The primary Python library for computing sentence/text embeddings. v5.x (2025+) includes modular architecture, support for Matryoshka embeddings, adaptive layers, PEFT adapter training, and multimodal embeddings. Integrates with FAISS for semantic search. Provides pre-trained models for semantic similarity, multilingual, multimodal, and domain-specific tasks.
  - Why relevant: The draft doesn't mention any practical embedding framework. sentence-transformers is the standard tool for converting text to embeddings in an ML pipeline.
  - Source: https://sbert.net/ · type: docs · date: 2024–2026 (ongoing)

### ch15_s03 — Evaluating embedding quality; domain-shift risk

- **MTEB: Massive Text Embedding Benchmark (v2, 2024–2026)**  [NEW]  (confidence: verified)
  - Summary: MTEB (3.3k GitHub stars) is the standard benchmark for evaluating text embeddings across 8 task types and 58+ datasets in 112+ languages. The 2025 expansion (MMTEB) adds multilingual coverage. A public leaderboard on HuggingFace Spaces tracks SOTA. Key finding: no single embedding method dominates across all tasks — the field hasn't converged, meaning embedding quality evaluation must be task-specific.
  - Why relevant: The draft only covers linear probing. MTEB provides the practical framework for comparing embedding quality in production. The "no universal best embedding" finding directly supports the draft's argument that quality is task-specific.
  - Source: https://arxiv.org/abs/2210.07316 (paper); https://huggingface.co/spaces/mteb/leaderboard (leaderboard) · type: paper + leaderboard · date: Oct 2022 (paper), ongoing (leaderboard)

- **Domain-shift detection in embedding spaces**  [NEW]  (confidence: uncertain)
  - Summary: Emerging area 2024–2026: monitoring embedding drift via statistical tests on embedding distributions (MMD, KNN-based), embedding-space coverage estimation, and outlier detection in latent space. Tools like Evidently AI and NannyML support embedding drift monitoring.
  - Why relevant: The draft describes domain shift conceptually but lacks any mention of detection methods. A brief reference to practical drift monitoring could strengthen the "evaluating embedding quality" narrative.
  - Source: Community tools and best practices · type: industry · date: 2024–2026

### ch15_s04 — Boundary with Chapter 8

- **(No major new external resources identified; the draft's conceptual distinction is already well-argued. Could reference the autoencoder vs. BERT example from the 2023-era literature.)**

### ch15_s05 — Does DL remove the need for FE?

- **LLM-based feature extraction as a new modality of FE**  [NEW]  (confidence: uncertain)
  - Summary: In 2024–2026, a growing pattern uses LLMs (GPT-4, Claude, open-source) to extract structured features from unstructured text via prompting. Rather than computing TF-IDF or using frozen BERT, practitioners prompt an LLM to output structured JSON (sentiment scores, entity lists, categorical labels). This is "feature extraction via in-context learning" — a new frontier where the boundary between FE and model inference blurs.
  - Why relevant: Reframes the "DL doesn't remove FE" thesis for the LLM era. The book could mention this pattern as a 2024+ development.
  - Source: Industry best practice (HuggingFace blog, Anthropic cookbook) · type: industry · date: 2024–2026

- **RAG (Retrieval-Augmented Generation) as implicit feature engineering**  [NEW]  (confidence: uncertain)
  - Summary: RAG retrieves external documents and injects them as context into an LLM prompt. From an FE perspective, this is a form of "external knowledge injection into features" — the retrieved passages serve as dynamically-computed, high-dimensional features that augment the model's representation. This connects to the broader theme of transferring external representations (Ch 8 boundary).
  - Why relevant: A fresh 2024 framing of the book's thesis. Shows that even in the LLM era, FE hasn't disappeared — it's been recast as retrieval + prompt design.
  - Source: Industry practice (LangChain, LlamaIndex docs) · type: industry · date: 2024–2026

### ch15_s06 — Input representation, tokenization, augmentation

- **Matryoshka embeddings and quantization-aware embeddings**  [NEW]  (confidence: verified)
  - Summary: Matryoshka Representation Learning (2022, but broadly adopted 2024–2026 via sentence-transformers) trains embeddings that are useful at multiple truncated dimensions — e.g., a 768-dim embedding that performs well even when truncated to 128 or 64 dims. This is a form of "learned feature engineering" that produces flexible representations. Binary and scalar (int8) quantization further reduce storage/memory.
  - Why relevant: Extends the "surviving FE inside DL" narrative with a modern efficiency-oriented technique. Relevant to practitioners building production embedding pipelines.
  - Source: https://sbert.net/ (Matryoshka training docs) · type: docs · date: 2024–2026

### ch15_s07 — Deep learning on tabular data: learned tabular embeddings

- **TabPFN v1: A Transformer That Solves Small Tabular Classification Problems in a Second**  [REFRESH]  (confidence: verified)
  - Summary: TabPFN (Prior-Data Fitted Network) performs in-context learning on tabular data — given a training set as input, it produces predictions in a single forward pass without gradient updates. Trained on synthetic data from a causal prior. On datasets up to 1,000 rows, 100 numerical features, 10 classes, it outperforms boosted trees and matches AutoML with up to 230× speedup (5,700× on GPU). No hyperparameter tuning needed.
  - Why relevant: The draft mentions FT-Transformer and TabNet but misses the most disruptive tabular DL development of recent years. TabPFN challenges the "gradient boosting always wins on small data" narrative. The in-context learning approach is conceptually novel for tabular data.
  - Source: https://arxiv.org/abs/2207.01848 · type: paper · date: Jul 2022 (updated Sep 2023)

- **TabPFN v2 / TabPFN-2.5 (2024–2025)**  [NEW]  (confidence: uncertain)
  - Summary: TabPFN v2 significantly extends the original: handles up to 10,000 samples and 500 features, supports regression tasks, handles missing values natively, and includes categorical feature support. TabPFN-2.5 (2025) further improves with larger pretraining. The v2 release on HuggingFace (late 2024 / early 2025) makes it accessible as a scikit-learn compatible classifier. This represents the emergence of "tabular foundation models."
  - Why relevant: This is the single most important recent development for ch15_s07. The concept of a pretrained tabular model that generalizes across datasets is fundamentally new and directly supports the chapter's thesis about learned representations.
  - Source: HuggingFace model hub (tabpfn-v2) + community reports · type: product + paper · date: 2024–2025

- **TabICL / TabM: In-context learning benchmarks for tabular data**  [NEW]  (confidence: uncertain)
  - Summary: Following TabPFN's success, several in-context learning approaches for tabular data emerged in 2024. TabICL benchmarks various ICL strategies on tabular data. These approaches represent "prompting as feature engineering" — the structure of how training examples are presented to the model becomes a form of input representation design.
  - Why relevant: Expands the in-context learning concept for tabular data. Connects to the broader theme of "FE shifting form."
  - Source: arXiv (multiple papers 2024) · type: paper · date: 2024

- **RealMLP, ModernNCA, ExcelFormer, TANGOS — recent tabular DL contenders (2023–2024)**  [NEW]  (confidence: uncertain)
  - Summary: A wave of simpler, more competitive tabular DL architectures emerged: RealMLP (improved MLP with modern enhancements), ModernNCA (Neighborhood Component Analysis for tabular data), ExcelFormer (attention-based), and TANGOS (tabular data regularization). These show that simpler architectures with careful design can close the gap with gradient boosting.
  - Why relevant: Supplements the FT-Transformer/TabNet list in the draft. Shows the field is dynamic and the "deep learning vs. gradient boosting" landscape is actively shifting.
  - Source: arXiv (multiple papers 2023–2024) · type: paper · date: 2023–2024

- **Deep Learning vs XGBoost/CatBoost/LightGBM: 2024 benchmarks and surveys**  [REFRESH]  (confidence: uncertain)
  - Summary: Multiple benchmarks in 2024–2025 show that while gradient boosting still dominates for tabular data under ~10K samples, the gap is narrowing. Key findings: (1) No single DL architecture consistently beats all GBDT variants; (2) DL excels when data >50K samples or when multimodal fusion is needed; (3) TabPFN-like models are closing the small-data gap; (4) Ensembling DL + GBDT often beats either alone.
  - Why relevant: The draft's statement that "GBDT still wins on small-to-medium data" needs updating with 2024 data. The landscape is shifting.
  - Source: arXiv surveys (2024–2025) · type: survey · date: 2024–2025

### ch15_s08 — Hybrid models: engineered features as extra input

- **(No major new external resources identified; the draft's argument is well-supported. The case study in s09 already demonstrates this architecture.)**

### ch15_s09 — Case study

- **(No major new external resources identified; the BERT+XGBoost pipeline is a representative pattern. Could reference the sklearn `FeatureUnion` pattern used in the notebook.)**

---

## Cross-cutting / chapter-level new developments

- **PEFT methods as the new adaptation standard (2024–2026):** LoRA, QLoRA (Dettmers et al. 2023), and DoRA (2024) have largely replaced full fine-tuning as the default adaptation strategy. The HuggingFace PEFT library unifies 30+ methods. This is a significant evolution from the frozen/partial/full taxonomy in the draft — the PEFT ecosystem deserves at minimum a brief mention in s01.

- **Tabular foundation models are emerging:** TabPFN v2/v2.5 and related work mark the birth of pretrained models for tabular data — analogous to what BERT did for text or ResNet for images. This is the most important chapter-relevant development of 2024–2025 and strongly supports the book's thesis that learned representations continue to expand their reach.

- **Embedding ecosystems have matured:** In 2024–2026, the combination of sentence-transformers (embedding generation), MTEB (evaluation), FAISS (storage/search), and HuggingFace Hub (distribution) forms a complete ecosystem for embedding-based pipelines. This was nascent when the book was first outlined and now deserves mention.

- **Embedding drift monitoring is an emerging concern:** As embeddings become standard features in production, monitoring their distribution shift (domain-shift detection, drift tests, coverage analysis) is becoming a recognized best practice.

---

## Candidate new terms (for Living Glossary / Appendix D)

- **PEFT (Parameter-Efficient Fine-Tuning):** A family of methods that adapt large pretrained models by training only a small subset of parameters.
- **LoRA (Low-Rank Adaptation):** A PEFT method that represents weight updates as low-rank matrices, enabling efficient fine-tuning.
- **QLoRA:** LoRA combined with 4-bit quantization for consumer-hardware fine-tuning.
- **DoRA (Weight-Decomposed Low-Rank Adaptation):** An improved LoRA variant that decomposes weights into magnitude and direction.
- **TabPFN (Prior-Data Fitted Network):** A pretrained Transformer that performs in-context learning on tabular data.
- **In-context learning (ICL) for tabular data:** Making predictions by providing labeled examples as input to a pretrained model without gradient updates.
- **MTEB (Massive Text Embedding Benchmark):** Standardized benchmark for evaluating text embedding models across diverse tasks.
- **FAISS (Facebook AI Similarity Search):** A library for efficient similarity search and clustering of dense vectors.
- **Sentence Transformer:** A framework for computing sentence/document-level embeddings from pretrained language models.
- **Matryoshka embeddings:** Embeddings trained to be useful at multiple truncated dimensions.
- **Foundation model (tabular):** A pretrained model for tabular data that generalizes across datasets without task-specific training.

---

## Source list

- [1] Hollmann et al., "TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second" — https://arxiv.org/abs/2207.01848 (paper, Jul 2022 / Sep 2023)
- [2] Liu et al., "DoRA: Weight-Decomposed Low-Rank Adaptation" — https://arxiv.org/abs/2402.09353 (paper, ICML 2024 Oral)
- [3] HuggingFace PEFT Documentation — https://huggingface.co/docs/peft/main/en/conceptual_guides/lora (docs, ongoing)
- [4] HuggingFace PEFT Library Overview — https://huggingface.co/docs/peft/en/index (docs, ongoing)
- [5] FAISS Library — https://github.com/facebookresearch/faiss (library, v1.14.3 Jun 2026)
- [6] Douze et al., "The Faiss library" — https://arxiv.org/abs/2401.08281 (paper, 2024)
- [7] Sentence-Transformers Documentation — https://sbert.net/ (docs, ongoing)
- [8] Muennighoff et al., "MTEB: Massive Text Embedding Benchmark" — https://arxiv.org/abs/2210.07316 (paper, Oct 2022)
- [9] MTEB Leaderboard — https://huggingface.co/spaces/mteb/leaderboard (leaderboard, ongoing)
- [10] MTEB GitHub Repository — https://github.com/embeddings-benchmark/mteb (repo, 3.3k stars, ongoing)
- [11] Ma et al., "The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits" — https://arxiv.org/abs/2402.17764 (paper, Feb 2024)
