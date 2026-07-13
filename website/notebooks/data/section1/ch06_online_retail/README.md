# Chapter 6 Online Retail Relational Snapshot

Derived from the shared UCI Online Retail snapshot in `data/section1/ch01_online_retail/`.

Files:

- `line_items.parquet` - known-customer invoice-line rows with derived monetary fields.
- `invoices.parquet` - one row per `InvoiceNo` and `CustomerID`.
- `customers.parquet` - one row per customer with whole-history summary fields.
- `customer_cutoff_features.parquet` - customer/index-time learning table for the chapter demo.
- `customer_cutoff_features_preview_1000.csv` - small preview of the learning table.
- `verified_stats.json` - reproducible row counts, cutoffs, feature lists, and fixed-ruler scores.

The chapter demo uses `customer_cutoff_features.parquet`. Features are computed from invoice history before each `index_time`; the target is whether the customer has any positive invoice in the following 60 days. The evaluation split trains on April-August 2011 cutoffs and tests on September-October 2011 cutoffs.
