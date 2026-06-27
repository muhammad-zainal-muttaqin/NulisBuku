# Ch 12 Research Resources — Images & Audio

**Generated:** 2026-06-27
**Status:** Gathered (not yet vetted by Compiler)
**Instructions:** Flags `[NEW]` = material not in current drafts; may warrant subsection addition/expansion. Flags `[REFRESH]` = validates or deepens existing draft coverage; compiler may incorporate selectively.

---

## 1. ViT vs CNN for Feature Extraction (Relevance: ch12_s03, ch12_s04)

### [NEW] Empirical Landscape 2024–2026

- **ViTs now dominate as feature extractors** for most downstream tasks, but the gap depends on dataset size and task type.
- On **small datasets (<5k samples)**, CNNs (ConvNeXt, ResNet-50) often still surpass ViTs when the pretrained weights are from supervised ImageNet — the convolutional inductive bias helps when data is scarce.
- On **medium-to-large transfer tasks (>10k)**, ViT-based extractors (ViT-B/16, ViT-L/14) consistently outperform comparable CNNs on linear probing and fine-tuning benchmarks.
- **ConvNeXt v2** (2023) and **ConvNeXt-XXL** (2024) represent the best of both worlds: CNN-style hierarchical structure with modern training recipes, competitive with ViT-L on dense tasks.
- **Best practice (2024–2025):** For unknown tasks, try both a ViT (e.g. ViT-B/16 from timm or DINOv2-B) and ConvNeXt-Base. If data is limited, favor the CNN; if data is moderate+, use ViT.

**Source:** HuggingFace timm documentation (models updated through Jan 2025), timm benchmark leaderboards.

### [REFRESH] CNN Hierarchical Feature Extraction (ch12_s03)

- Existing draft correctly describes the CNN hierarchical pipeline (edges → textures → object parts → semantics). Confirmed as still the canonical mental model.

---

## 2. CLIP/SigLIP as Image Feature Extractors (Relevance: ch12_s04, ch14)

### [NEW] Modern CLIP Variants as Drop-in Replacements for ImageNet-CNNs

| Model | Architecture | Training Data Scale | Key Property |
|---|---|---|---|
| **OpenAI CLIP** (ViT-B/32, ViT-L/14) | ViT | 400M image-text pairs | Original, widely available |
| **OpenCLIP** (ViT-G/14, ViT-H/14) | ViT | LAION-2B | Open-source, larger, better zero-shot |
| **SigLIP** (ViT-B/16, ViT-L/16, SO400M) | ViT | WebLI (multi-billion) | Sigmoid loss instead of softmax; much stronger features, especially SigLIP-SO |
| **EVA-CLIP** (EVA-02 series) | ViT | Merged-2B + LAION-2B | Best-in-class ImageNet linear probe at release; BAAI |
| **DFN (Data Filtering Network)** | ViT | Filtered LAION | Better quality at same scale by filtering training data |

**Recommended default (mid-2025):** `google/siglip-so400m-patch14-384` for general-purpose frozen feature extraction. SigLIP-SO provides stronger embeddings than the original CLIP, especially for dense vision tasks.

**Source:** HuggingFace model hub, OpenCLIP GitHub (`mlfoundations/open_clip`, v2.30+).

### [NEW] Using CLIP Vision Encoder as Feature Extractor

- `CLIPVisionModel.from_pretrained("openai/clip-vit-base-patch32")` → `outputs.pooler_output` = image embedding
- The vision encoder can be used standalone without the text branch via `get_image_features()` or `CLIPVisionModel`

**Source:** HuggingFace `transformers` docs for CLIP (v5.12.0, June 2025).

---

## 3. DINOv2 — Self-Supervised Vision Features (Relevance: ch12_s04)

### [NEW] Key Properties

- **Paper:** Oquab et al., "DINOv2: Learning Robust Visual Features without Supervision" (arXiv:2304.07193, 2023; updated 2024).
- **Architecture:** ViT-based, patch size 14, available in small/base/large/giant sizes.
- **Key advantage over supervised features:** DINOv2 features excel on **dense prediction tasks** (segmentation, depth estimation, correspondence) — this is where supervised ImageNet models typically fall short.
- **Two output modes:**
  - **CLS token** (`last_hidden_states[:, 0, :]`) — global image embedding, good for classification/retrieval
  - **Patch features** (`last_hidden_states[:, 1:, :]`) — spatial-local features at 14x14 patch resolution, excellent for dense tasks
- **Code (from HF docs):** `AutoModel.from_pretrained("facebook/dinov2-base")` with `BitImageProcessor` for preprocessing.
- **When to use:** DINOv2 is the current go-to for self-supervised vision features where you need spatial fidelity — outperforms CLIP on segmentation, depth estimation.

**Source:** HuggingFace `transformers` docs for Dinov2 (v5.12.0, June 2025); DINOv2 paper (arXiv:2304.07193).

---

## 4. Image Embeddings & Patch Best Practices (Relevance: ch12_s04)

### [REFRESH] ViT Patch Processing

- Existing draft correctly describes patch splitting and attention mechanism. The 16×16 grid example aligns with standard ViT-B/16.
- DINOv2 uses patch_size=14 → for a 224×224 input: 16×16 = 256 patches plus 1 CLS token.

### [NEW] Multi-Scale Feature Extraction

- **Modern best practice:** For tasks requiring multi-scale features (object detection, segmentation), extract features from intermediate ViT layers, not just the final layer.
- **timm feature extraction API:** `model.forward_features(x)` returns intermediate features; timm models can be configured to output features from multiple stages.
- **Hierarchical ViTs** (Swin, ConvNeXt) naturally produce multi-scale feature pyramids like CNNs, making them preferable for dense tasks vs. plain ViTs.

**Source:** `timm` (pytorch-image-models) library, v1.x (2025).

---

## 5. Whisper Encoder as Audio Feature Extractor (Relevance: ch12_s06)

### [NEW] Using Whisper Encoder Hidden States

- **Whisper** is an encoder-decoder transformer (680k hours of labeled audio). Its encoder processes mel-spectrogram input and produces rich speech representations.
- **Key insight (not in drafts):** The Whisper encoder's last hidden state can be used as a general-purpose audio feature extractor — a drop-in replacement for wav2vec2/HuBERT for non-ASR downstream tasks when you want larger-scale pretraining.
- **Whisper large-v3** has 1.55B parameters; its encoder alone is ~600M parameters — substantially larger than most dedicated audio encoders.
- **Code approach:** `WhisperModel.from_pretrained(...).get_encoder()` or use `output_hidden_states=True` on the full model to extract encoder features.
- **Caveat:** Whisper uses log-mel spectrogram input (80 mel bins), NOT raw waveform — so it sits between the spectrogram-based and raw-waveform paradigms.
- **Whisper large-v3-turbo** (2024) provides faster inference with minimal accuracy loss; useful as a feature extractor at scale.

**Source:** HuggingFace `transformers` docs for Whisper (v5.12.0); OpenAI Whisper paper (arXiv:2212.04356).

---

## 6. Audio Foundation Models Beyond wav2vec/HuBERT (Relevance: ch12_s06, ch12_s07)

### [NEW] WavLM (Microsoft, 2022–2025)

- **Architecture:** Built on HuBERT framework. Adds gated relative position bias in the transformer and utterance mixing during pretraining.
- **Training data:** 94k hours (WavLM Large).
- **Key strength:** State-of-the-art on **SUPERB benchmark** across diverse tasks (ASR, speaker ID, emotion recognition, keyword spotting) — it handles both content and speaker tasks well.
- **Speaker focus:** WavLM preserves speaker identity better than wav2vec2/HuBERT, making it preferable for speaker verification and diarization.
- **HuggingFace:** `microsoft/wavlm-base`, `microsoft/wavlm-large`; uses `Wav2Vec2Processor` for preprocessing (raw waveform input).
- **WavLM ForXVector:** Has a dedicated head for speaker embedding extraction (x-vector style).

**Source:** HuggingFace docs for WavLM (v5.12.0); WavLM paper (arXiv:2110.13900).

### [NEW] Other Notable Audio Foundation Models

| Model | Input | Pretraining | Key Use Case |
|---|---|---|---|
| **AudioMAE** (2022) | Spectrogram patches | Masked autoencoding (like MAE for vision) | General audio classification, sound event detection |
| **BEATs** (Microsoft, 2023) | Spectrogram | Iterative SSL with acoustic tokenizer | Audio classification; strong on AudioSet |
| **CLAP** (LAION, 2023) | Raw audio + text | Contrastive audio-text (like CLIP for audio) | Zero-shot audio classification, text-to-audio retrieval |
| **MERT** (2023) | Raw waveform | Music-specific SSL with teacher models | Music understanding, genre/tag classification |
| **Wav2Vec2-BERT 2.0** (Meta, 2024) | Raw waveform | 4.5M hours pretraining (!) | ASR, speech translation at scale |

**Source:** HuggingFace model hub and respective arXiv papers.

### [REFRESH] wav2vec 2.0 & HuBERT (ch12_s06)

- Existing draft coverage is correct and current. The HuggingFace docs confirm raw waveform input (16kHz mono), SSL via masking, and feature extraction via `Wav2Vec2Model` / `HubertModel`.
- **Update note:** Meta released **Wav2Vec2-BERT 2.0** (4.5M hours pretraining) — recommended for fine-tuning tasks per HF docs. This may warrant a brief mention in the draft.

---

## 7. Edge / Efficient Encoders (Relevance: ch12_s03, ch12_s01)

### [NEW] Deploying Feature Extractors on Edge Devices

- **MobileNetV4** (2024): Introduces Universal Inverted Bottleneck (UIB) that unifies several efficient block designs. State-of-the-art for mobile-class models; available in timm.
- **FastViT** (Apple, 2023): Hybrid CNN-ViT architecture with structural reparameterization for 2× inference speedup vs. comparable models on mobile.
- **EfficientViT** (2023–2024): Designed for real-time dense prediction on edge devices; cascade group attention for efficiency.
- **Key takeaway for FE:** When deploying feature extraction on edge devices, MobileNetV4-S (small) provides the best accuracy-latency trade-off as of mid-2025. For ViT-based, FastViT-SA12 provides competitive quality at much lower FLOPs.

**Source:** MobileNetV4 paper (arXiv:2404.10518), timm model zoo.

---

## 8. Modern Image Augmentation (Relevance: ch12_s01)

### [NEW] The Designed Feature Engineering That Survives in DL

| Augmentation | What It Does | When to Use |
|---|---|---|
| **RandAugment** (Cubuk et al., 2019) | Random magnitude of 14 operations (rotate, shear, etc.) | Default choice; replaces hand-tuned augmentation policies |
| **MixUp** (Zhang et al., 2018) | Linearly interpolates two images AND their labels | Strong regularizer; improves calibration and robustness |
| **CutMix** (Yun et al., 2019) | Pastes a patch from one image onto another; labels mixed proportionally | Better localization than MixUp; widely used in ViT training |
| **AugMix** (Hendrycks et al., 2019) | Mixes several augmented versions of the same image | Improves robustness to corruptions/domain shift |
| **TrivialAugment** (2021) | Single augmentation with random magnitude — simpler than RandAugment | Surprisingly competitive with RandAugment at zero tuning cost |

**Modern default recipe (2024–2025 for timm/ViT training):** RandAugment (magnitude=9) + MixUp (alpha=0.8) + CutMix (alpha=1.0) + RandomErasing. This is baked into timm's training recipes.

**Augmentation as FE:** These augmentations are a form of **designed feature engineering that survives inside deep learning** — they're human-designed transformations that teach invariance and improve feature quality, but are applied programmatically in the pipeline.

**Source:** timm training recipes; torchvision `transforms` documentation (v2 API).

---

## 9. Audio Feature Extraction: Spectrogram vs MFCC vs Learned (Relevance: ch12_s05, ch12_s06)

### [NEW] When to Use Which (2024 Guidance)

| Representation | When to Use | When NOT to Use |
|---|---|---|
| **Raw Waveform** | With wav2vec2/HuBERT/WavLM/Whisper encoders | Classical ML (SVM, random forest) — too high-dimensional |
| **Mel-spectrogram** | CNN-based audio classifiers, Whisper input, YAMNet-style models | Tasks needing compact features; very small datasets |
| **MFCC** | Small datasets (<1k samples) with classical ML; ASR with HMM/GMM; resource-constrained edge deployment | Deep learning on large datasets; emotion/music tasks (MFCC loses nuance) |
| **Learned (wav2vec2 embeddings)** | Best accuracy in 2024 for speech/non-speech audio classification with moderate+ data | Extremely low-resource scenarios where fine-tuning is impossible |

**Trend:** MFCC is increasingly legacy for DL pipelines. The 2024 default is: if you have < 100 labeled samples, use MFCC + SVM; otherwise, use a pretrained audio encoder (wav2vec2 or WavLM).

**Source:** HuggingFace audio course; SUPERB benchmark results.

---

## 10. Multimodal Audio-Vision (Relevance: ch12_s04, ch12_s07, ch14)

### [NEW] Joint Embedding Spaces for Audio + Image

- **ImageBind** (Meta, 2023): Learns a single joint embedding space across 6 modalities: images, text, audio, depth, thermal, and IMU data. Images serve as the "anchor" modality — the image encoder is frozen and other modalities are aligned to it.
  - Enables **cross-modal retrieval**: audio → image, image → audio, etc.
  - Available on HuggingFace: `facebook/imagebind-huge`
  - **Relevance for Ch 12:** ImageBind demonstrates that audio embeddings and image embeddings can live in a unified space — useful for downstream multimodal feature engineering without paired data across all modalities.
- **AudioCLIP** (2021): Extends CLIP with an audio encoder (ESResNeXt) for audio-image-text triplets.
- **CLAP** (LAION, 2023): Like CLIP but trained on audio-text pairs. Enables text-to-audio and audio-to-text retrieval.

**Source:** ImageBind paper (arXiv:2305.05665), HuggingFace model hub.

---

## 11. Pipeline Discipline Resources (Relevance: ch12_s01, ch12_s08)

### [REFRESH] Augmentation & Normalization Best Practices

- **Normalization:** Compute mean/std from training set only; apply identical values to validation/test. `torchvision.transforms.Normalize(mean, std)` — the standard three-channel values are ImageNet defaults `([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])`.
- **Augmentation during training only:** Standard in all frameworks (PyTorch `transforms.Compose`, HuggingFace `torchvision.transforms.v2`). The draft covers this correctly.
- **SpecAugment** for audio: Applied inside wav2vec2/HuBERT/WavLM models automatically during training (controlled via `mask_time_prob`, `mask_feature_prob` in config). Whisper also supports SpecAugment but it's disabled by default for inference.

### [REFRESH] Modality-Specific Leakage (ch12_s08)

- Existing draft coverage of source-recording-level split for audio/video is correct and comprehensive. The GroupKFold / source-recording principle is standard best practice for continuous modalities.

---

## 12. Handcrafted Features — HOG & Modern Usage (Relevance: ch12_s02)

### [REFRESH] HOG

- Existing draft correctly describes HOG as gradient orientation histograms capturing silhouettes. The pedestrian detection example is the canonical HOG use case (Dalal & Triggs, 2005).
- **Modern relevance (2024):** HOG is still used in embedded/real-time systems with extreme latency constraints where running a CNN is infeasible. Some edge applications combine HOG with lightweight classifiers for rapid person/vehicle detection.

---

## Summary Table: Chapter 12 Subsections × Resource Flags

| Subsection | NEW Flags Count | REFRESH Flags Count | Priority Action |
|---|---|---|---|
| ch12_s01 | Augmentation survey (RandAugment etc.), Edge encoders | Normalization pipeline notes | Medium |
| ch12_s02 | — | HOG modern relevance | Low |
| ch12_s03 | ViT vs CNN landscape 2024–2026, ConvNeXt v2 | CNN hierarchy confirmation | Medium |
| ch12_s04 | DINOv2, CLIP/SigLIP variants, multi-scale features | ViT patch processing | High (DINOv2) |
| ch12_s05 | MFCC vs learned features decision guide | Spectrogram/MFCC confirmation | Medium |
| ch12_s06 | WavLM, Whisper-as-extractor, AudioMAE/CLAP/BEATs/MERT, Wav2Vec2-BERT 2.0 | wav2vec2/HuBERT core | High (WavLM, Whisper) |
| ch12_s07 | ImageBind/AudioCLIP for multimodal audio-vision | Pooling strategy confirmation | Medium |
| ch12_s08 | — | Leakage discipline, source-recording split | Low |

**Top Recommendations for Compiler:**
1. **[ch12_s04]** Add DINOv2 as a major modern image embedding model — the draft only covers ViT generically; DINOv2's CLS token + patch features are important for the "modern representations" narrative.
2. **[ch12_s06]** Add WavLM and Whisper-as-extractor as modern audio encoder alternatives beyond wav2vec2/HuBERT. The draft currently only mentions wav2vec2 and HuBERT.
3. **[ch12_s04]** Reference CLIP/SigLIP as modern ImageNet-CNN replacements for image feature extraction.