# Chapter 10 Bike Sharing Snapshot

Local snapshot for UCI Bike Sharing.

Files:

- `bike_sharing_dataset.zip` - original UCI archive.
- `hour.csv` - original hourly records.
- `day.csv` - original daily records.
- `Readme.txt` - original UCI archive readme.
- `hour.parquet` - parsed hourly table with added `datetime`.
- `day.parquet` - parsed daily table.
- `hour_lag_features.parquet` - causal lag/rolling feature table for the notebook.
- `hour_preview_1000.csv` - small preview.
- `verified_stats.json` - reproducible row counts, regularity, autocorrelation, and fixed-ruler metrics.

The notebook predicts hourly `cnt` with features that are available before each timestamp. The fixed holdout trains before 2012-10-01 and tests from 2012-10-01 onward.
