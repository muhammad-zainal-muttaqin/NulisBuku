# Ch14 Open Food Facts Curated Snapshot

Source: https://world.openfoodfacts.org/data
Static export streamed from: https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz
License: Open Food Facts database under ODbL; contents under DbCL; product images under CC BY-SA.
Snapshot date: 2026-07-09.

The full export is not vendored. This folder stores only a curated paired subset
with product text, tabular nutrition fields, Nutri-Score labels, source image URLs,
cached thumbnails, derived image-color features, and fixed evaluation metrics.
The best fixed classification AP is the train-only late tabular+image score
fusion recorded in `off_late_fusion_weights.json`.
