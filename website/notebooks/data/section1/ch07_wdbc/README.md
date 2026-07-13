# Chapter 7 WDBC Snapshot

Local snapshot for UCI Breast Cancer Wisconsin Diagnostic, sourced from `sklearn.datasets.load_breast_cancer`.

Files:

- `wdbc.parquet` - 569 rows, 30 real numeric features, `diagnosis`, and binary `malignant`.
- `wdbc.csv` - portable CSV version of the same table.
- `top_correlated_feature_pairs.csv` - top absolute feature correlations for the redundancy demo.
- `verified_stats.json` - reproducible counts, redundancy stats, selector scores, and selected-feature summaries.

The notebook adds 20 clearly labeled synthetic `probe_noise_*` columns at runtime to demonstrate feature selection against irrelevant controls. Those probe columns are not part of the dataset identity.
