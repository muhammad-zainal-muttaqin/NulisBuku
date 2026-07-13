# Chapter 8 Optical Digits Snapshot

Local snapshot for the sklearn copy of UCI Optical Recognition of Handwritten Digits.

Files:

- `digits.parquet` - 1,797 rows, 64 `pixel_*` features, and target `digit`.
- `digits.csv` - portable CSV version of the same table.
- `digits_images.npy` - 8x8 image tensor aligned with `digits.parquet`.
- `digits_preview_500.csv` - small preview.
- `pca_probe_accuracy.csv` - fixed linear-probe accuracy for selected PCA component counts.
- `verified_stats.json` - reproducible counts, pixel ranges, PCA variance thresholds, and NMF reconstruction stats.

Note: the current UCI page lists the full Optical Digits archive as 5,620 instances. This snapshot intentionally uses the smaller sklearn copy for fast, offline notebook execution.
