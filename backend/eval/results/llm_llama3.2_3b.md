# Eval: llm:llama3.2:3b

- Run: 2026-10-29 12:36 UTC on macOS-27.0.1-arm64-arm-64bit
- Dataset: `eval/dataset/synthetic` (30 PDFs)
- Model: llama3.2:3b @ http://localhost:11434/v1
- Latency per document: median 11.59s, max 43.54s
- Docs where the model output was unusable for ≥1 chunk (regex fallback): 0
- Docs with no result because the LLM call failed (timeout 300.0s): 0
- **Overall field accuracy: 95.1%** (371/390 field checks)

| Field | Accuracy |
|---|---|
| document_type | 100.0% |
| supplier_name | 100.0% |
| customer_name | 100.0% |
| document_number | 100.0% |
| po_number | 100.0% |
| document_date | 90.0% |
| due_date | 100.0% |
| currency | 100.0% |
| subtotal | 83.3% |
| tax | 100.0% |
| total | 96.7% |
| line_items_count | 96.7% |
| line_items_exact | 70.0% |

| Template | Mean field accuracy | Docs |
|---|---|---|
| classic | 98.5% | 5 |
| day_first | 93.8% | 5 |
| label_variants | 87.7% | 5 |
| multipage | 95.4% | 5 |
| purchase_order | 100.0% | 5 |
| unlabelled_supplier | 95.4% | 5 |

## Misses

| File | Field | Detail |
|---|---|---|
| 001_label_variants.pdf | subtotal | got 46685.11 want 46865.11 |
| 001_label_variants.pdf | line_items_exact | got 5 items want 5 |
| 005_day_first.pdf | document_date | got 2025-11-06 want 2025-06-11 |
| 007_label_variants.pdf | subtotal | got 7821.80 want 8521.80 |
| 010_multipage.pdf | line_items_exact | got 17 items want 17 |
| 013_label_variants.pdf | subtotal | got 21208.61 want 21108.61 |
| 013_label_variants.pdf | total | got 21208.61 want 21108.61 |
| 015_unlabelled_supplier.pdf | line_items_exact | got 3 items want 3 |
| 018_classic.pdf | line_items_exact | got 4 items want 4 |
| 019_label_variants.pdf | subtotal | got 33571.17 want 35357.17 |
| 021_unlabelled_supplier.pdf | line_items_count | got 4 items want 5 |
| 021_unlabelled_supplier.pdf | line_items_exact | got 4 items want 5 |
| 022_multipage.pdf | line_items_exact | got 16 items want 16 |
| 023_day_first.pdf | document_date | got 2024-02-10 want 2024-10-02 |
| 023_day_first.pdf | line_items_exact | got 4 items want 4 |
| 025_label_variants.pdf | subtotal | got 24357.59 want 24157.59 |
| 025_label_variants.pdf | line_items_exact | got 4 items want 4 |
| 028_multipage.pdf | line_items_exact | got 19 items want 19 |
| 029_day_first.pdf | document_date | got 2025-01-04 want 2025-04-01 |
