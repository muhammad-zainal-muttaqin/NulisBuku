# Chapter 11 SMS Spam Snapshot

Local snapshot for UCI SMS Spam Collection.

Files:

- `sms_spam_collection.zip` - original UCI archive.
- `SMSSpamCollection` - original labeled text file.
- `readme` - original archive readme.
- `sms_spam.parquet` - parsed table with `label`, `text`, `is_spam`, and normalized text helper.
- `sms_spam.csv` - portable parsed fallback.
- `sms_spam_preview_1000.csv` - small preview.
- `verified_stats.json` - reproducible label counts, sparsity, duplicate, and fixed-ruler metrics.

Parse rule: split each raw line on the first tab. Generic CSV parsing can merge lines because SMS text contains quote characters.
