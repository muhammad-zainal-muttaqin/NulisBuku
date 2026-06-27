---
chapter: ch14
title: Multimodal Data
generated: 2026-06-27
stage: gather-only (external resources; not book prose)
language: English (working notes)
---

# Chapter 14 Resources — Multimodal Data

> External material gathered 2026-06-27. Tagging: [NEW] = absent from drafts · [REFRESH] = newer/better source for an existing topic. Each item carries provenance (source · type · date · confidence).

## Coverage baseline (what the drafts already have)
- ch14_s01: multimodal definition, alignment, time sync, sampling-rate mismatch, windowing
- ch14_s02: early/mid/late fusion, feature-level vs decision-level, trade-offs
- ch14_s03: concatenation, dimensionality imbalance (2048 vs 10 dims), SVD reduction, bottleneck projection, scaling
- ch14_s04: missing entire modality, indicator variables, late fusion resilience, shared subspace
- ch14_s05: joint embedding space, dual encoders, contrastive loss, cosine similarity, cross-modal retrieval
- ch14_s06: CLIP as feature extractor, 512-dim vectors, zero-shot classification
- ch14_s07: house-price case study, TF-IDF + PCA + ResNet/CLIP, entity-level splitting, StandardScaler fit on train only

## Resources by subsection

### ch14_s01 — What is multimodal data? Alignment and time synchronization
- **Video-LM alignment & dynamic FPS** [NEW] (confidence: verified)
  - Summary: Qwen2.5-VL uses extended multimodal RoPE (MRoPE) to understand absolute time positions of frames across dynamic FPS rates, preserving real-world speed perception. Gemma 3 interleaves timestamps with video frames in the prompt (e.g., "Frame 00.00: <image>..").
  - Why relevant: Updates the classical fixed-sampling-rate alignment discussion with modern VLM-native temporal understanding — no external resampling needed.
  - Source: https://huggingface.co/blog/vlms-2025 · type: blog (HF official) · date: 2025-05-12

- **Any-to-any multimodal inputs — GPT-4V** [NEW] (confidence: verified)
  - Summary: GPT-4V demonstrated unprecedented ability to process arbitrarily interleaved multimodal inputs (text + image in same prompt), with unique "visual referring prompting" (drawing markers on input images). This shifts alignment from a preprocessing step to a prompt-design concern.
  - Why relevant: Broadens the definition of alignment beyond tabular-join style to include in-context, vision-referring alignment.
  - Source: https://arxiv.org/abs/2309.17421 · type: paper (arXiv) · date: 2023-09-29

### ch14_s02 — Fusion strategies: early, intermediate, late — feature- vs. decision-level
- **Perceiver IO / attention bottleneck for multimodal fusion** [NEW] (confidence: verified)
  - Summary: DeepMind's Perceiver IO (Jaegle et al., 2021) uses a fixed-size latent bottleneck to cross-attend to arbitrary modality inputs (text, image, audio, point clouds) regardless of input dimensionality. This decouples input size from model depth — a fundamentally different approach from simple concatenation.
  - Why relevant: The draft covers "intermediate fusion" conceptually but doesn't mention the Perceiver/attention-bottleneck architecture that dominates modern practice. This bridges s02 and s06.
  - Source: https://arxiv.org/abs/2107.14795 · type: paper · date: 2021 (still current in 2025 VLMs)

- **Mixture-of-Experts (MoE) decoder fusion** [NEW] (confidence: verified)
  - Summary: MoE-LLaVA (2024), DeepSeek-VL2, and Kimi-VL use MoE decoders where only a subset of experts is activated per modality input. This is a new fusion paradigm: modalities aren't merged into a single dense pathway but routed dynamically through modality-specialized sub-networks.
  - Why relevant: Expands the fusion taxonomy beyond early/mid/late to include dynamic routing. Relevant for the VLM era.
  - Source: https://arxiv.org/abs/2401.15947 (MoE-LLaVA) · type: paper · date: 2024-01-29

### ch14_s03 — Feature concatenation and dimensionality balancing
- **BLIP-2 Q-Former: learned bridging vs. raw concatenation** [REFRESH] (confidence: verified)
  - Summary: BLIP-2 uses a lightweight Querying Transformer (Q-Former) to bridge frozen image encoders and frozen LLMs without concatenation. The Q-Former learns to extract visual features relevant to text — essentially a learned dimensionality balancing mechanism rather than post-hoc SVD.
  - Why relevant: The draft covers SVD and bottleneck layers as balancing methods. Q-Former is a more principled, learnable alternative that the draft doesn't mention. Replaces "Truncated SVD on extracted features" with "learned bridging."
  - Source: https://arxiv.org/abs/2301.12597 · type: paper · date: 2023-01-30

- **SigLIP: scaling-friendly contrastive pretraining** [REFRESH] (confidence: verified)
  - Summary: SigLIP replaces CLIP's softmax-normalized contrastive loss with a simple pairwise sigmoid loss. This disentangles batch size from loss normalization, enabling training with up to 1M batch size and better performance at small batch sizes. SigLIP-SO 400M achieves 84.5% ImageNet zero-shot.
  - Why relevant: Draft covers CLIP as the main model. SigLIP is a direct upgrade with better scaling properties for feature extraction. SigLIP-SO 400M is now a standard backbone in Kimi-VL and other 2025 VLMs.
  - Source: https://arxiv.org/abs/2303.15343 · type: paper (ICCV'23 Oral) · date: 2023-03-27; https://huggingface.co/docs/transformers/en/model_doc/siglip · type: docs · date: 2025

### ch14_s04 — Handling missing modalities
- **Cross-modal autoencoders with modality dropout (SMIL-style)** [REFRESH] (confidence: uncertain)
  - Summary: Modern approaches train with deliberate modality dropout during pretraining (randomly zeroing out a modality), forcing the model to learn robust cross-modal inference. The approach generalizes the "indicator variable" method from the draft to a learned robustness paradigm. Multimodal autoencoders can reconstruct missing modality from available ones.
  - Why relevant: Draft covers indicator variables and shared subspace projection at a conceptual level. The modality-dropout training strategy is a practical, proven technique not mentioned.
  - Source: (inference from known architecture patterns; no single canonical paper found in this batch) · type: design note · date: 2024-2025

- **Late fusion for missing-modality robustness (Molmo)** [REFRESH] (confidence: verified)
  - Summary: Allen AI's Molmo (2024) exemplifies a modular VLM design where visual and text branches operate independently until answer generation. This inherent architecture makes it naturally robust to missing image inputs — the text-only LLM backbone can still respond.
  - Why relevant: Concrete modern example reinforcing the draft's late-fusion resilience argument with a 2024 model.
  - Source: https://huggingface.co/blog/vlms-2025 · type: blog · date: 2025-05-12

### ch14_s05 — Cross-modal and joint embeddings
- **InstructBLIP: instruction-aware query transformer for cross-modal alignment** [REFRESH] (confidence: verified)
  - Summary: InstructBLIP extends BLIP-2 with an instruction-aware Q-Former that extracts visual features conditioned on the specific instruction. This makes the joint embedding space task-dependent — the same image maps to different features depending on whether the task is captioning vs. VQA.
  - Why relevant: The draft's joint embedding description is task-agnostic ("dog image = dog text"). InstructBLIP shows that modern systems condition alignment on the downstream task. Nuances the "one shared space" narrative.
  - Source: https://arxiv.org/abs/2305.06500 · type: paper · date: 2023-05-11

- **Multimodal embedding evaluation: recall@k, nDCG for cross-modal retrieval** [NEW] (confidence: verified)
  - Summary: Standard evaluation metrics for joint embedding spaces are recall@k (e.g., recall@1 for image→text and text→image retrieval on MS-COCO/Flickr30k tests), image/text retrieval accuracy, and nDCG benchmarks. The ViDoRe benchmark (2024) extends this to visual document retrieval evaluation.
  - Why relevant: The draft covers how joint embeddings work but not how to evaluate their quality. Essential for the book's emphasis on evaluation (Ch 9).
  - Source: https://arxiv.org/abs/2407.01449 · type: paper (ViDoRe/ColPali, ICLR 2025) · date: 2024-06-27

### ch14_s06 — Multimodal pretrained models
- **VLM landscape 2024–2025: LLaVA, DeepSeek-VL, Qwen-VL, PaliGemma 2, SmolVLM2** [REFRESH] (confidence: verified)
  - Summary: The VLM field has massively diversified since CLIP. LLaVA (NeurIPS 2023 Oral) first connected vision encoder + LLM via a projection layer. As of 2025: Qwen2.5-VL (3B–72B, agentic capabilities), Kimi-VL-Thinking (MoE with reasoning, 16B total/3B active), SmolVLM2 (256M–2.2B, runs on-device), PaliGemma 2 (detection + segmentation), and any-to-any models like Qwen2.5-Omni. All usable as feature extractors.
  - Why relevant: The draft only covers CLIP as a frozen feature extractor. The field has moved to full VLMs with richer extraction capabilities (structured outputs, OCR, localization). The 2025 update is essential.
  - Source: https://huggingface.co/blog/vlms · type: blog · date: 2024-04-11; https://huggingface.co/blog/vlms-2025 · type: blog · date: 2025-05-12

- **BLIP-2 as a feature extractor (frozen encoders + learnable Q-Former)** [REFRESH] (confidence: verified)
  - Summary: BLIP-2 pioneered the "frozen image encoder + frozen LLM + small trainable bridge" paradigm with only ~3% trainable parameters. Achieves SOTA with 54× fewer trainable parameters than Flamingo-80B. This is the blueprint for modern VLM-as-feature-extractor workflows.
  - Why relevant: CLIP is one frozen-extractor approach; BLIP-2 is another with richer capabilities (VQA, captioning). Gives writers a second concrete model family.
  - Source: https://arxiv.org/abs/2301.12597 · type: paper · date: 2023-01-30

### ch14_s07 — Case study: combining tabular + image/text/sensor in one pipeline
- **Multimodal RAG: ColPali & DSE for document retrieval as feature extraction pipeline** [NEW] (confidence: verified)
  - Summary: ColPali (ICLR 2025) and Document Screenshot Embedding (DSE, EMNLP 2024) bypass traditional OCR+parsing pipelines by embedding entire document page screenshots directly with VLMs. ColPali uses late-interaction MaxSim over multi-vector embeddings; DSE uses single-vector dense retrieval. Both demonstrate that VLM-based feature extraction can replace brittle multi-stage pipelines.
  - Why relevant: A concrete modern example of multimodal feature extraction in a real-world pipeline (RAG for documents). Extends the case study beyond house-price prediction or could serve as an alternative case.
  - Source: https://arxiv.org/abs/2407.01449 · type: paper (ICLR 2025) · date: 2024-06-27; https://arxiv.org/abs/2406.11251 · type: paper (EMNLP 2024) · date: 2024-06-17

- **Direct Preference Optimization (DPO) for VLM alignment** [NEW] (confidence: verified)
  - Summary: trl library added DPO support for VLMs in 2024, enabling preference-based fine-tuning where the model learns to prefer chosen over rejected multimodal responses. Uses datasets like RLAIF-V (83k image-question pairs with preferred/rejected answers).
  - Why relevant: Shows how extracted multimodal features are used downstream — not just frozen extraction but preference-aligned fine-tuning for specific tasks. Practical pipeline detail.
  - Source: https://huggingface.co/blog/dpo_vlm · type: blog (HF official) · date: 2025

## Cross-cutting / chapter-level new developments

- **Contrastive vs. generative multimodal representation learning** [NEW] (confidence: verified)
  - Summary: CLIP/SigLIP represent the contrastive paradigm (discriminative, alignment-focused). Generative approaches like Chameleon (Meta, 2024) and Janus-Pro (DeepSeek, 2025) learn through image→text and text→image generation. The contrastive path produces better retrieval/distance features; the generative path produces richer, more transferable representations for complex reasoning.
  - Why relevant: This is a chapter-level axis the draft doesn't address. The book could position the contrastive-vs-generative choice as a fundamental design decision in multimodal FE.
  - Source: https://arxiv.org/abs/2405.09818 (Chameleon); https://huggingface.co/blog/vlms-2025 · type: blog + paper · date: 2024-2025

- **Vision-Language-Action (VLA) models as multimodal feature extractors** [NEW] (confidence: verified)
  - Summary: VLAs (π0, GR00T N1, 2025) extend VLMs to robotics by adding action/state tokens. They demonstrate that multimodal representations can encode not just semantic alignment but also physical affordances — a new dimension of multimodal FE.
  - Why relevant: Broadens the chapter's scope beyond traditional modalities to embodied/action data. Shows where the field is heading.
  - Source: https://huggingface.co/blog/vlms-2025 · type: blog · date: 2025-05-12

- **Multimodal safety & guard models** [NEW] (confidence: verified)
  - Summary: ShieldGemma 2 (Google, 2025) and Llama Guard 4 (Meta, 2025) are multimodal safety classifiers that filter VLM inputs/outputs. These are themselves multimodal feature extraction pipelines for a specific downstream purpose.
  - Why relevant: Relevant for Ch 9's privacy/proxy callout and the book's emphasis on production-readiness. Multimodal systems need multimodal safety.
  - Source: https://huggingface.co/blog/llama-guard-4 · type: blog · date: 2025

## Candidate new terms (for Living Glossary / Appendix D)
- **Multimodal RAG** — retrieval across modalities using VLM-based embedding of document images, bypassing traditional OCR+parsing pipelines
- **Q-Former (Querying Transformer)** — lightweight transformer bridge between frozen image encoder and LLM in BLIP-2; learns to extract task-relevant visual features
- **SigLIP** — Sigmoid loss variant of CLIP; pairwise sigmoid loss eliminates batch-size dependency in contrastive pretraining
- **Any-to-any model** — single model accepting and generating multiple modalities (text, image, audio) via shared representation space
- **Mixture-of-Experts (MoE) decoder** — dynamic routing architecture where only a subset of expert sub-networks activates per input, used in modern VLMs for efficiency
- **Late interaction / MaxSim** — ColPali-style retrieval where similarity is computed between all token-patch embedding pairs, not a single pooled vector
- **Visual document retrieval** — embedding entire document page images with VLMs for retrieval without parsing (ColPali, DSE)
- **Modality dropout** — deliberate removal of a modality during training to build robustness to missing data at inference
- **Vision-Language-Action (VLA) model** — VLM extended with action/state tokens for robotics; multimodal FE for embodied tasks
- **Preference optimization (DPO) for VLMs** — fine-tuning VLMs by ranking preferred vs rejected multimodal responses

## Source list
- [1] Hugging Face — "Vision Language Models Explained" — https://huggingface.co/blog/vlms (blog, 2024-04-11)
- [2] Hugging Face — "Vision Language Models (Better, faster, stronger)" — https://huggingface.co/blog/vlms-2025 (blog, 2025-05-12)
- [3] Zhai et al. — "Sigmoid Loss for Language Image Pre-Training (SigLIP)" — https://arxiv.org/abs/2303.15343 (paper, ICCV 2023 Oral)
- [4] Hugging Face — SigLIP documentation — https://huggingface.co/docs/transformers/en/model_doc/siglip (docs, 2025)
- [5] Li et al. — "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models" — https://arxiv.org/abs/2301.12597 (paper, 2023-01-30)
- [6] Liu et al. — "Visual Instruction Tuning (LLaVA)" — https://arxiv.org/abs/2304.08485 (paper, NeurIPS 2023 Oral)
- [7] Yang et al. — "The Dawn of LMMs: Preliminary Explorations with GPT-4V(ision)" — https://arxiv.org/abs/2309.17421 (paper, 2023-09-29)
- [8] Dai et al. — "InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning" — https://arxiv.org/abs/2305.06500 (paper, 2023-05-11)
- [9] Lin et al. — "MoE-LLaVA: Mixture of Experts for Large Vision-Language Models" — https://arxiv.org/abs/2401.15947 (paper, 2024-01-29)
- [10] Faysse et al. — "ColPali: Efficient Document Retrieval with Vision Language Models" — https://arxiv.org/abs/2407.01449 (paper, ICLR 2025)
- [11] Ma et al. — "Unifying Multimodal Retrieval via Document Screenshot Embedding (DSE)" — https://arxiv.org/abs/2406.11251 (paper, EMNLP 2024)
- [12] Ying et al. — "MMT-Bench: A Comprehensive Multimodal Benchmark for Evaluating Large Vision-Language Models Towards Multitask AGI" — https://arxiv.org/abs/2404.16006 (paper, 2024-04-24)
- [13] Yue et al. — "MMMU-Pro: A More Robust Multi-discipline Multimodal Understanding Benchmark" — https://arxiv.org/abs/2409.02813 (paper, ACL 2025)
- [14] Chameleon (Meta) — https://huggingface.co/collections/facebook/chameleon-668da9663f80d483b4c61f58 (model collection, 2024)
- [15] Janus-Pro (DeepSeek) — https://huggingface.co/deepseek-ai/Janus-Pro-7B (model, 2025)
- [16] Hugging Face — "Preference Optimization for Vision Language Models with TRL" — https://huggingface.co/blog/dpo_vlm (blog, 2025)
- [17] Hugging Face — "Llama Guard 4" — https://huggingface.co/blog/llama-guard-4 (blog, 2025)
- [18] MMMU Benchmark — https://huggingface.co/datasets/MMMU/MMMU (dataset, 2024)
- [19] MMBench — https://huggingface.co/datasets/lmms-lab/MMBench (dataset/benchmark, 2024)
- [20] Open VLM Leaderboard — https://huggingface.co/spaces/opencompass/open_vlm_leaderboard (leaderboard, 2025)
- [21] Jaegle et al. — "Perceiver IO: A General Architecture for Structured Inputs & Outputs" — https://arxiv.org/abs/2107.14795 (paper, 2021)
