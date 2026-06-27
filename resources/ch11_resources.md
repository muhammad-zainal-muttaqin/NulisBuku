---
chapter: ch11
title: Text & Documents
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 11 Resources — Text & Documents

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence).

## Coverage baseline (what the drafts already have)
- s01: Tokenization, BoW, n-grams — classic text-to-vector pipeline (no BPE/subword, no Unicode-aware tokenization)
- s02: TF-IDF — TF, IDF, balancing common vs. rare words
- s03: Word embeddings — sparse→dense shift, distributional hypothesis, Word2Vec/GloVe mentioned in concept only
- s04: Contextual/sentence/document embeddings — polysemy, dynamic vs. static vectors, mean-pooling, sentence transformers
- s05: Pretrained LMs as frozen feature extractors — BERT→SVM pipeline, freezing weights
- s06: Fine-tuning vs. feature extraction — data size, compute, overfitting trade-offs
- s07: Case study — TF-IDF vs. SBERT on doc classification, leakage warnings (vectorizer fit before split, duplicate docs)

**What is absent from ALL drafts:** modern embedding landscape (2024–2026), multilingual models, LLMs as feature extraction engines, sparse-dense hybrid, MTEB benchmark, efficient/distilled models for scale, text features for tabular data, domain-adaptive pretraining, Matryoshka embeddings.

---

## Resources by subsection

### ch11_s01 — Classic Text Representations
- **[REFRESH] BPE and subword tokenization (Gage 1994 / Sennrich+ 2016)** (confidence: verified)
  - Summary: Byte-Pair Encoding (BPE) and subword tokenizers (WordPiece, Unigram) split rare words into subword units to handle OOV tokens naturally. The draft uses word-level tokenization only; BPE is the backbone of modern tokenizers (BERT, GPT, T5) and directly relevant when transitioning to LM-based representations.
  - Why relevant: Bridges s01 tokenization to pretrained models in s05. A natural place to mention that tokenizers in BERT/GPT use subword splitting, not simple space-delimited words.
  - Source: https://huggingface.co/docs/transformers/tokenizer_summary · type: docs · date: updated 2024

- **[REFRESH] CountVectorizer vs. HashingVectorizer trade-offs** (confidence: verified)
  - Summary: scikit-learn offers both vocabulary-based (CountVectorizer) and hashing-based (HashingVectorizer) approaches. HashingVectorizer avoids storing vocabulary in memory and handles streaming data but introduces hash collisions. The draft mentions sparse matrices but not this practical production consideration.
  - Why relevant: Production/deployment concern for s01 — when vocabularies become too large.
  - Source: https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction · type: docs · date: 2024

### ch11_s02 — TF-IDF
- **[REFRESH] BM25 as a modernized TF-IDF successor** (confidence: verified)
  - Summary: Okapi BM25 is a refined TF-IDF-like scoring function that incorporates document length normalization and saturating TF (non-linear dampening of repeated terms). It remains the dominant "classic" IR baseline against which neural retrievers are benchmarked (appears in virtually all BGE/M3, E5, MTEB evaluations).
  - Why relevant: The draft presents TF-IDF as the canonical weighting method but does not mention that BM25 is its widely-used, length-aware successor. Important context for the s07 case-study baseline and for understanding retrieval benchmarks.
  - Source: https://arxiv.org/abs/2104.08663 (BEIR benchmark) · type: paper · date: 2021 (updated benchmark 2023+)

**[REFRESH] Sublinear TF scaling and SMART notation** (confidence: uncertain)
  - Summary: Multiple TF-IDF variants exist (ltc, lnc, etc. via SMART notation) — sublinear TF (log TF), boolean TF, augmented TF. scikit-learn defaults differ from classic IR defaults.
  - Why relevant: Practical precision for educators/readers who will use TfidfVectorizer and wonder about sublinear_tf=True.
  - Source: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html · type: docs · date: 2024

### ch11_s03 — The Shift to Learned: Word Embeddings
- **[REFRESH] Word2Vec → fastText evolution (Bojanowski+ 2016)** (confidence: verified)
  - Summary: fastText extends Word2Vec by treating each word as a bag of character n-grams, enabling embeddings for OOV words and morphologically rich languages. Still widely used (especially for languages like Indonesian where morphology matters).
  - Why relevant: Indonesian is a morphologically rich language (affixes: me-, ber-, -kan, etc.); fastText is far more practical for Indonesian text than vanilla Word2Vec. Strong fit for the book's target language.
  - Source: https://fasttext.cc/docs/en/english-vectors.html · type: docs · date: updated 2024

- **[NEW] Matryoshka Representation Learning for embeddings** (confidence: verified)
  - Summary: Matryoshka embeddings (Kusupati+ 2022, integrated into OpenAI text-embedding-3 and Sentence Transformers v3+) allow a single embedding vector to be truncated to multiple smaller dimensions while retaining most of the quality. A 1024d embedding truncated to 256d still performs well — crucial for storage-cost trade-offs at scale.
  - Why relevant: Directly connects how modern embeddings address the dimensionality/efficiency concerns introduced in s03. The book's "dimensions" discussion (s03: 100-300d) can be refreshed with this technique.
  - Source: https://arxiv.org/abs/2205.13147 · type: paper · date: 2022 (used in OpenAI embed v3, Jan 2024)

### ch11_s04 — Contextual, Sentence, and Document Embeddings
- **[REFRESH] Sentence Transformers v3+ (2024): Matryoshka, Adaptive Layers, ONNX export** (confidence: verified)
  - Summary: Sentence Transformers v3.x (2024) added native support for Matryoshka loss, adaptive layer pruning, ONNX/OpenVINO export, and prompt-based encoding. The library now directly supports training Matryoshka embeddings and selecting depth at inference time.
  - Why relevant: The draft discusses sentence embeddings from SBERT (the 2019 paper). The library has evolved significantly. Important for s04's practical guidance.
  - Source: https://www.sbert.net/docs/pretrained_models.html · type: docs · date: 2024–2025

- **[REFRESH] Instructor-style instruct-tuned embedding models** (confidence: verified)
  - Summary: INSTRUCTOR (Su+ 2023) and similar models add task-specific instructions ("Represent the sentence for retrieving relevant passages") before encoding. E5-mistral-7b-instruct and GRIT (Muennighoff+ 2024) generalize this approach. Instruction-aware embeddings outperform task-agnostic ones on diverse benchmarks.
  - Why relevant: The draft treats embedding as a uniform operation. Modern embeddings are instruction-conditioned — a key concept for s04/s05.
  - Source: https://huggingface.co/hkunlp/instructor-large · type: model card · date: 2023

- **[NEW] Jina Embeddings v5-text (2025): LoRA task adapters for embeddings** (confidence: verified)
  - Summary: jina-embeddings-v5-text (677M params, 32K context, Matryoshka dimensions) introduces task-specific LoRA adapters — a single base model that is parameter-efficiently adapted to retrieval, classification, STS, and clustering tasks. Sets new SOTA in small-model category on MMTEB.
  - Why relevant: Represents the cutting edge of practical embedding models (2025). Demonstrates how a single model can produce domain-adapted embeddings without full fine-tuning.
  - Source: https://jina.ai/embeddings/ · type: docs/blog · date: 2025

### ch11_s05 — Pretrained Language Models as Feature Extractors
- **[NEW] LLMs as feature extractors: using GPT-4, Claude, Llama 3 for structured FE from unstructured text** (confidence: uncertain)
  - Summary: A growing 2024 paradigm uses LLMs (GPT-4, Claude, Llama 3, Mistral) not for classification but to extract structured features from raw text — e.g., pulling entity mentions, topic labels, sentiment scores, factual attributes — which then feed downstream tabular models. This is feature engineering, not classification; the LLM acts as an interpretable feature extractor, replacing regex/rule-based NLP pipelines.
  - Why relevant: This is the most important [NEW] topic for s05. The draft only covers BERT-as-vectorizer; the modern landscape includes LLM-based structured feature extraction (tab-augmentation from text columns). Connects text FE to tabular FE (Ch 3–6).
  - Source: https://platform.openai.com/docs/guides/embeddings ("Embedding as a text feature encoder for ML algorithms"); also https://arxiv.org/abs/2401.00368 (E5-mistral) · type: docs/paper · date: 2024

- **[NEW] Decoder-only LLMs as embedding generators: E5-Mistral, SFR-Embedding-Mistral, NV-Embed** (confidence: verified)
  - Summary: 2024 saw a shift from encoder-only (BERT) to decoder-only (Mistral, Llama) foundation models for embedding generation. Models like e5-mistral-7b-instruct (7B params, 4096d embeddings) and Salesforce SFR-Embedding-Mistral achieve SOTA on MTEB using LLM backbones rather than BERT. They use last-token pooling and task instructions.
  - Why relevant: The draft's feature extractor discussion centers on BERT. The modern answer is often Llama/Mistral-based embedding models, which are 2024 developments.
  - Source: https://huggingface.co/intfloat/e5-mistral-7b-instruct · https://huggingface.co/Salesforce/SFR-Embedding-Mistral · type: model cards · date: 2024

### ch11_s06 — Fine-tuning vs. Feature Extraction
- **[NEW] Parameter-Efficient Fine-Tuning (PEFT): LoRA, QLoRA, Adapters for embedding models** (confidence: verified)
  - Summary: LoRA (Hu+ 2021) and QLoRA (Dettmers+ 2023) enable fine-tuning embedding models by updating only a small fraction of parameters (adapters). Sentence Transformers now supports PEFT training natively. Jina v5 uses task-specific LoRA adapters for retrieval/classification/STS. This expands the fine-tuning vs. extraction trade-off with a middle ground.
  - Why relevant: The draft's binary "freeze vs. full fine-tuning" choice is outdated. The real 2024 practitioner menu includes LoRA/QLoRA fine-tuning that captures domain specificity with minimal compute. A valuable addition or sidebar.
  - Source: https://www.sbert.net/examples/sentence_transformer/training/peft/README.html · type: docs · date: 2024–2025

- **[REFRESH] SetFit: few-shot fine-tuning of sentence transformers** (confidence: verified)
  - Summary: SetFit (Tunstall+ 2022) fine-tunes Sentence Transformer embeddings with contrastive learning on as few as 8 labeled examples per class, then trains a lightweight classification head. Bridges the gap between frozen extraction and full fine-tuning.
  - Why relevant: A practical, low-resource alternative to the freeze-vs-fine-tune binary in the draft. Indonesian-language tasks often have limited labeled data.
  - Source: https://arxiv.org/abs/2209.11055 · type: paper · date: 2022

### ch11_s07 — Case Study: Document Classification, TF-IDF vs. Contextual Embedding
- **[NEW] The MTEB leaderboard as an empirical decision tool** (confidence: verified)
  - Summary: MTEB (Muennighoff+ 2022) provides standardized benchmarks across ~58 datasets in 8 task categories (classification, clustering, pair classification, reranking, retrieval, STS, summarization, bitext mining). In 2024–2025, the leaderboard is dominated by LLM-based and multilingual models. OpenAI text-embedding-3-large scores 64.6%, while BGE-M3 (open-source, multilingual, hybrid) and E5-Mistral (7B) top retrieval tasks. The MMTEB extension adds multilingual evaluation.
  - Why relevant: Gives the case study concrete models to benchmark against. SBERT is no longer the only sensible baseline; BGE-M3 and E5-mistral are the 2024-2025 standards.
  - Source: https://huggingface.co/spaces/mteb/leaderboard · https://github.com/embeddings-benchmark/mteb · type: benchmark/paper · date: 2022–2026 (updated)

- **[NEW] Domain-specific embedding models: code, law, finance, medical (Voyage AI, SPECTER2)** (confidence: verified)
  - Summary: Voyage AI released domain-specific models in 2024: voyage-code-2, voyage-law-2, voyage-finance-2 — outperforming general models within their domains by significant margins. SPECTER2 (2023) provides science-specific embeddings. This demonstrates that domain-adaptive pretraining and fine-tuning matters for feature quality.
  - Why relevant: Enriches the case study with a real finding: the best embedding for document classification may depend heavily on domain. A TF-IDF baseline might beat an off-the-shelf embedding in niche domains unless the embedding is domain-adapted.
  - Source: https://blog.voyageai.com/2024/09/18/voyage-3/ · type: blog · date: Sep 2024

---

## Cross-cutting / chapter-level new developments

### The 2024–2026 Multilingual Embedding Landscape
- **BGE-M3 (BAAI, Feb 2024):** 100+ languages, dense + sparse + colbert retrieval in one model, 8192-token context. Trained via self-knowledge distillation. Dominates multilingual benchmarks. 31M+ monthly downloads on HF.
  - Source: https://arxiv.org/abs/2402.03216 · type: paper · date: Feb 2024
- **Multilingual E5 (Microsoft, Feb 2024):** Based on XLM-RoBERTa large, trained on 4B+ multilingual text pairs, supports 100 languages. Mr. TyDi benchmark leader (2024). 8.2M monthly downloads.
  - Source: https://arxiv.org/abs/2402.05672 · https://huggingface.co/intfloat/multilingual-e5-large · type: paper/model card · date: Feb 2024
- **LaBSE (Google, 2020):** Still heavily used (109 languages, 768d). Basis for many multilingual production deployments.
  - Source: https://arxiv.org/abs/2007.01852 · type: paper · date: 2020

### The Commercial / Proprietary Embedding API Landscape (2024–2025)
- **OpenAI text-embedding-3-small (62.3% MTEB, $0.02/1M tokens) and text-embedding-3-large (64.6% MTEB, $0.13/1M tokens):** Native Matryoshka dimension reduction, 8192-token context. The 2024 default for many API-based pipelines.
  - Source: https://platform.openai.com/docs/guides/embeddings · type: docs · date: 2024
- **Cohere Embed v4.0 (2025):** Multimodal (text + images), 256-1536 variable dimensions, 128K-token context. Represents the convergence of text and vision embeddings.
  - Source: https://docs.cohere.com/v2/docs/cohere-embed · type: docs · date: 2025
- **Voyage AI voyage-3 (Sep 2024):** 1024d, 32K context, $0.06/1M tokens. Outperforms OpenAI v3 large by 7.55% across 8 domains (tech, code, law, finance, multilingual, web, long-context, conversation). voyage-3-lite (512d) at $0.02/1M tokens still beats OpenAI v3 large.
  - Source: https://blog.voyageai.com/2024/09/18/voyage-3/ · type: blog · date: Sep 2024
- **Jina Embeddings v5 (2025):** Open-weight models — v5-text (677M/239M, LoRA task adapters, 32K context) and v5-omni (multimodal: text + image + audio + video). Byte-compatible with previous versions for no-reindex upgrades.
  - Source: https://jina.ai/embeddings/ · type: docs/blog · date: 2025

### Sparse, Dense, and Hybrid Retrieval as Feature Paradigms
- **SPLADE (NAVER, 2021–2024):** Sparse neural retrieval that learns token-level importance weights (30522-dim vocabulary space). Produces interpretable, BM25-style sparse vectors with deep-learning quality. Now integrated into sentence-transformers as SparseEncoder.
  - Source: https://huggingface.co/naver/splade-cocondenser-ensembledistil · https://arxiv.org/abs/2107.05720 · type: model card/paper · date: 2021 (updated 2024)
- **BGE-M3 hybrid retrieval (2024):** Single model produces dense, sparse (lexical weights), and ColBERT-style multi-vector representations simultaneously. Hybrid scoring combines all three. Represents the state of the art in representation flexibility.
  - Source: https://huggingface.co/BAAI/bge-m3 · type: model card · date: Feb 2024

### Efficient and Distilled Models for FE at Scale
- **all-MiniLM-L6-v2 (SBERT, 2021):** 22.7M params, 384d embeddings, 245M+ downloads/month. The most popular lightweight general-purpose embedding model. Trained on 1B sentence pairs with contrastive learning.
  - Source: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 · type: model card · date: 2021 (updated)
- **DistilBERT (Sanh+ 2019):** 66M params (40% smaller than BERT-base), retains 97% of performance, 60% faster. Ubiquitous as a base for distilled sentence transformers.
  - Source: https://huggingface.co/distilbert/distilbert-base-uncased · type: model card · date: 2019
- **MiniLM series (Microsoft, 2020–2021):** Deep self-attention distillation. Models from Multi-Head (12-layer, 384d) to L6 (6-layer, 384d). Foundation for the all-MiniLM family.
  - Source: https://arxiv.org/abs/2002.10957 · type: paper · date: 2020

### Text Features for Tabular Augmentation
- **OpenAI embeddings cookbook: "Embedding as a text feature encoder for ML algorithms"** (2024): Official OpenAI guidance shows embeddings used as features for RandomForest regression/classification on tabular data. SVD/PCA on embeddings is discouraged (loses information density).
  - Source: https://platform.openai.com/docs/guides/embeddings#embedding-as-a-text-feature-encoder-for-ml-algorithms · type: docs · date: 2024
- **Text2Feature paradigm (LLM-based):** Emerging 2024 pattern: use LLM structured output (JSON mode, function calling) to extract numeric/categorical features from text columns in tabular data. E.g., ask GPT-4 to extract "product_category", "sentiment_score", "key_entities" from product reviews → features for XGBoost.
  - This is a cross-cutting topic relevant to ch06_s05 (domain-driven features), ch11_s05 (feature extractors), ch16_s03 (GenAI for feature proposals).
  - Source: Not a single canonical paper. See OpenAI structured-outputs: https://platform.openai.com/docs/guides/structured-outputs · type: docs · date: 2024

### Domain-Adaptive Pretraining for Better Text Features
- **Adaptive pretraining (Gururangan+ 2020 / sentence-transformers domain adaptation):** Continued pretraining (MLM) on domain-specific corpora before feature extraction significantly improves downstream task performance. SBERT docs provide domain-adaptation recipes.
  - Source: https://www.sbert.net/examples/sentence_transformer/domain_adaptation/README.html · https://arxiv.org/abs/2004.10964 · type: docs/paper · date: 2020 (updated 2024)
- **Voyage domain-specific models (2024):** Voyage proved domain-adapted embeddings (law, finance, code) consistently beat general ones in their respective domains, providing empirical evidence for the domain-adaptation thesis.
  - Source: https://blog.voyageai.com/2024/09/18/voyage-3/ · type: blog · date: Sep 2024

---

## Candidate new terms (for Living Glossary / Appendix D)
- **Matryoshka embedding** — an embedding vector designed so truncating it to a lower dimension preserves quality; enables cost-adaptive deployment.
- **SPLADE (Sparse Lexical and Expansion Model)** — neural model producing sparse, interpretable token-weight vectors combining the strengths of BM25 and dense retrieval.
- **Multi-functionality embedding** — model (e.g., BGE-M3) producing dense, sparse, and multi-vector representations from a single forward pass.
- **Task instruction / prompt-based embedding** — embedding model conditioned on a natural-language task description (e.g., "Retrieve relevant documents for the query").
- **BPE (Byte-Pair Encoding)** — subword tokenization algorithm merging frequent character pairs; foundation of modern tokenizers.
- **PEFT (Parameter-Efficient Fine-Tuning)** — techniques like LoRA/Adapters that update only a tiny fraction of parameters for domain adaptation.
- **MTEB (Massive Text Embedding Benchmark)** — standardized benchmark covering 58 datasets across 8 task categories for evaluating text embeddings.
- **Cross-lingual embedding** — embedding model that maps text from multiple languages into a shared semantic space, enabling zero-shot transfer.

---

## Source list
- [1] MTEB Leaderboard — https://huggingface.co/spaces/mteb/leaderboard (benchmark, updated 2024–2026)
- [2] MTEB paper (Muennighoff+ 2022) — https://arxiv.org/abs/2210.07316 (paper, 2022)
- [3] OpenAI Embeddings Guide — https://platform.openai.com/docs/guides/embeddings (docs, 2024)
- [4] BGE-M3 paper (Chen+ 2024) — https://arxiv.org/abs/2402.03216 (paper, Feb 2024)
- [5] C-Pack / BGE paper (Xiao+ 2023) — https://arxiv.org/abs/2309.07597 (paper, Sep 2023; SIGIR 2024)
- [6] Cohere Embed v3/v4 docs — https://docs.cohere.com/v2/docs/cohere-embed (docs, 2024–2025)
- [7] Voyage AI voyage-3 blog — https://blog.voyageai.com/2024/09/18/voyage-3/ (blog, Sep 2024)
- [8] Jina Embeddings — https://jina.ai/embeddings/ (docs/blog, 2025)
- [9] Improving Text Embeddings with LLMs (Wang+ 2024) — https://arxiv.org/abs/2401.00368 (paper, Dec 2023; ACL 2024)
- [10] E5-mistral-7b-instruct — https://huggingface.co/intfloat/e5-mistral-7b-instruct (model card, 2024)
- [11] SFR-Embedding-Mistral — https://huggingface.co/Salesforce/SFR-Embedding-Mistral (model card, 2024)
- [12] Multilingual E5 (Wang+ 2024) — https://arxiv.org/abs/2402.05672 (paper, Feb 2024) · https://huggingface.co/intfloat/multilingual-e5-large (model card, 2024)
- [13] Sentence Transformers pretrained models — https://www.sbert.net/docs/pretrained_models.html (docs, 2024–2025)
- [14] Sentence Transformers domain adaptation — https://www.sbert.net/examples/sentence_transformer/domain_adaptation/README.html (docs, 2024)
- [15] Sentence Transformers PEFT training — https://www.sbert.net/examples/sentence_transformer/training/peft/README.html (docs, 2024)
- [16] all-MiniLM-L6-v2 — https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 (model card, 2021)
- [17] SPLADE model — https://huggingface.co/naver/splade-cocondenser-ensembledistil (model card, 2022)
- [18] SPLADE paper (Formal+ 2022) — https://arxiv.org/abs/2107.05720 (paper, 2021; updated 2022)
- [19] Matryoshka Representation Learning (Kusupati+ 2022) — https://arxiv.org/abs/2205.13147 (paper, 2022)
- [20] BEIR benchmark (Thakur+ 2021) — https://arxiv.org/abs/2104.08663 (paper, 2021)
- [21] SetFit paper (Tunstall+ 2022) — https://arxiv.org/abs/2209.11055 (paper, 2022)
- [22] INSTRUCTOR model — https://huggingface.co/hkunlp/instructor-large (model card, 2023)
- [23] BAAI/bge-m3 — https://huggingface.co/BAAI/bge-m3 (model card, Feb 2024)
- [24] HuggingFace tokenizer summary — https://huggingface.co/docs/transformers/tokenizer_summary (docs, updated 2024)
- [25] fastText — https://fasttext.cc/docs/en/english-vectors.html (docs, updated)
- [26] OpenAI structured outputs — https://platform.openai.com/docs/guides/structured-outputs (docs, 2024)
- [27] DistilBERT (Sanh+ 2019) — https://arxiv.org/abs/1910.01108 · https://huggingface.co/distilbert/distilbert-base-uncased (paper/model card, 2019)
- [28] MiniLM paper (Wang+ 2020) — https://arxiv.org/abs/2002.10957 (paper, 2020)
- [29] LaBSE paper (Feng+ 2020) — https://arxiv.org/abs/2007.01852 (paper, 2020)
