# Project: Rekayasa Fitur Modern - Agent System Instructions

This file is the **master instruction manual** for any AI Agent working on this repository.

## The Absolute Mandate
You MUST read and strictly obey the instructions contained in the `pipeline/` directory before taking any action. These files are the single source of truth for the book's content, structure, style, and vocabulary.

**MANDATORY READING LIST:**
Before writing or modifying any content, you MUST execute `read` commands for the following files:
1. `pipeline/book-pipeline-plan.md` - For architecture and workflow.
2. `pipeline/chapter-subsection-breakdown.md` - For the specific scope of the subsection you are working on.
3. `pipeline/outline-rekayasa-fitur.md` - For global book structure and constraints.
4. `pipeline/writer-system-prompt.md` - For the exact voice, tone, style, and paragraph guidelines.
5. `pipeline/glossary-seed.md` - For the mandatory terminology policy.
6. `pipeline/RULE.md` - For project boundaries.

Do NOT rely on summary instructions. Read the actual pipeline files. The instructions there are hard rules, not suggestions.
### Aturan Penomoran Heading (Format Markdown)
- **Dilarang Menulis Nomor Bab/Sub-bab Secara Manual:** Pada saat menulis draf, jangan menaruh angka hierarki pada judul *heading* (Contoh SALAH: ## 14.1 Judul Sub-Bab). Quarto akan memberikan penomoran secara otomatis. Tulislah hanya teks judulnya saja (Contoh BENAR: ## Judul Sub-Bab).
- **Hierarki *Heading* Tidak Boleh Melompat:** Gunakan level # untuk judul Bab utama, ## untuk sub-bab level 1, ### untuk sub-bab level 2, dst. Jangan menggunakan #### secara langsung jika belum ada ## dan ### di atasnya, karena mesin *renderer* (Quarto) akan bingung dan menghasilkan penomoran seperti 14.0.0.1.
