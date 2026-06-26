# Living Glossary — Seed (→ Lampiran D)

Single source of truth for term decisions. Loaded into book-level context for **every** generation (plan §5–6); the pipeline maintains the live `glossary.json` from it and review only **extends** it. This seed records decisions already made.

Guiding rule (from the terminology policy): use **what the Indonesian IT/CS community actually uses**. Default to a natural Indonesian word where one exists and is common; otherwise keep the English term, italicized. Never invent/revive purist Indonesian.

---

## 1. Core conceptual pair (the spine — verbatim, book-wide)

| Indonesian (use) | English | Note |
|---|---|---|
| representasi yang **dirancang manusia** | designed (by human) representation | explicit agent *manusia* is load-bearing |
| representasi yang **dipelajari mesin** | learned (by machine) representation | explicit agent *mesin*; never the bare *dipelajari* (misreads as "learned by us") |

## 1b. Coined phrase for a concept (rendered, not a single loanword)

| Indonesian (use) | English | Note |
|---|---|---|
| **praktik pipeline yang benar** | pipeline discipline | keep *pipeline* English; **not** "disiplin pipeline" (awkward calque). Anchored in **Bab 2**; mentioned rarely elsewhere, only at a real leakage / training–inference risk. |

## 2. Indonesian terms — use as-is (do not force to English, do not localize to purist forms)

Common, natural Indonesian; English source shown for reference.

| Indonesian (use) | English source |
|---|---|
| **fitur** | feature |
| **distribusi** | distribution |
| model | model |
| data | data |
| algoritma | algorithm |
| citra | image |
| jaringan | network |
| pelatihan / latih | training |
| representasi | representation |
| atribut | attribute |
| dimensi | dimension |
| skala | scale |

> **Note on *fitur*:** this is the **house term** (cf. the book title *Rekayasa Fitur*). Standalone "feature" → *fitur*. Keep English only inside established compounds where the community does (*feature store*, *feature extractor*); the activity "feature engineering" → *rekayasa fitur*.

## 3. English terms — keep as-is, *italicized* (community lingua-franca; no commonly-used Indonesian form)

*machine learning, deep learning, embedding, pipeline, leakage, target encoding, one-hot, encoding, autoencoder, pretrained, fine-tuning, feature store, feature extractor, dataset, batch, epoch, gradient, overfitting, baseline.*

*(Not exhaustive — review adds more, with the reviewer's decision recorded here.)*

## 4. Avoid (purist localizations — use the English/common form instead)

| Avoid | Use instead |
|---|---|
| derau | *noise* |
| mangkus | *efficient* / efisien |
| sangkil | *effective* / efektif |
| larik | *array* |
| dwimatra | dua dimensi / 2D |
| peladen | *server* |

---

> **How to extend:** when a reviewer decides a rendering for a new term during Editorial Review, add a row to the right section here (and the live `glossary.json`). This file *is* Lampiran D, built as a by-product of review.
