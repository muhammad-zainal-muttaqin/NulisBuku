# Chapter 9 WDBC Evaluation Snapshot

Chapter-specific reuse of the WDBC snapshot prepared for Chapter 7.

Files:

- `wdbc.parquet` - 569 rows, 30 real numeric WDBC features, `diagnosis`, and binary `malignant`.
- `wdbc.csv` - portable CSV version of the same table.
- `top_correlated_feature_pairs.csv` - copied redundancy summary from Chapter 7.
- `group_ablation_scores.csv` - retrain-and-score results after removing `mean`, `error`, or `worst` feature families.
- `permutation_importance.csv` - validation-set permutation importance for the fixed random forest.
- `model_importance.csv` - model-based feature importance for the same fixed random forest.
- `verified_stats.json` - reproducible grouping, split protocol, baseline, ablation, and importance stats.

The fixed ruler uses WDBC's natural feature families: 10 `mean`, 10 `error`, and 10 `worst` measurements.
