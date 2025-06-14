## 📁 Data Files Notice

To keep the repository lightweight and within GitHub's file size limits, **large cleaned data files are not included** in the repo.

### ❌ Not Included
- `segmentation/data/cleaned_customer_events.csv` (≈118 MB)

This file is intentionally excluded and listed in `.gitignore` to prevent Git LFS requirements and push errors.

### ✅ How to Use
If you need the cleaned data file for running the pipeline:

1. **Generate it locally** using the data processing scripts:
   ```bash
   python -m data_ingestion.load_example_module
