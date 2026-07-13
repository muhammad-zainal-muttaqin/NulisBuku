# UCI Online Retail Notebook Snapshot

Parsed snapshot used by the Bab 1 and Bab 2 Section-1 notebooks.

- Source: UCI Machine Learning Repository, Online Retail dataset.
- Source URL: <https://archive.ics.uci.edu/dataset/352/online+retail>
- DOI: <https://doi.org/10.24432/C5BW33>
- Snapshot date: 2026-07-09.
- License: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Attribution: Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.

Files:

- `online_retail.parquet`: parsed notebook copy with normalized dtypes and derived columns.
- `verified_stats.json`: stats recomputed from the parsed snapshot.

Derived columns:

- `is_cancellation`: true when `InvoiceNo` starts with `C` or `Quantity < 0`.
- `line_value`: `Quantity * UnitPrice`.
- `abs_line_value`: `abs(Quantity) * UnitPrice`.

The full original download and CSV fallback are stored in `v2/data/section1/ch01_online_retail/`.
