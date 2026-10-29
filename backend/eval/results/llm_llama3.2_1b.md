# Eval: llm:llama3.2:1b

- Run: 2026-10-29 12:39 UTC on macOS-27.0.1-arm64-arm-64bit
- Dataset: `eval/dataset/synthetic` (30 PDFs)
- Model: llama3.2:1b @ http://localhost:11434/v1
- Latency per document: median 5.30s, max 21.39s
- Docs where the model output was unusable for ≥1 chunk (regex fallback): 0
- Docs with no result because the LLM call failed (timeout 300.0s): 0
- **Overall field accuracy: 85.1%** (332/390 field checks)

| Field | Accuracy |
|---|---|
| document_type | 83.3% |
| supplier_name | 86.7% |
| customer_name | 100.0% |
| document_number | 100.0% |
| po_number | 100.0% |
| document_date | 90.0% |
| due_date | 100.0% |
| currency | 100.0% |
| subtotal | 63.3% |
| tax | 90.0% |
| total | 53.3% |
| line_items_count | 93.3% |
| line_items_exact | 46.7% |

| Template | Mean field accuracy | Docs |
|---|---|---|
| classic | 95.4% | 5 |
| day_first | 81.5% | 5 |
| label_variants | 72.3% | 5 |
| multipage | 96.9% | 5 |
| purchase_order | 80.0% | 5 |
| unlabelled_supplier | 84.6% | 5 |

## Misses

| File | Field | Detail |
|---|---|---|
| 001_label_variants.pdf | subtotal | got 28660.84 want 46865.11 |
| 001_label_variants.pdf | total | got 42608.10 want 49208.37 |
| 001_label_variants.pdf | line_items_count | got 8 items want 5 |
| 001_label_variants.pdf | line_items_exact | got 8 items want 5 |
| 002_purchase_order.pdf | document_type | got invoice want purchase_order |
| 002_purchase_order.pdf | total | got 33002.40 want 33902.40 |
| 002_purchase_order.pdf | line_items_exact | got 2 items want 2 |
| 003_unlabelled_supplier.pdf | subtotal | got 6926.92 want 6296.92 |
| 003_unlabelled_supplier.pdf | total | got 7400.67 want 6800.67 |
| 003_unlabelled_supplier.pdf | line_items_exact | got 2 items want 2 |
| 004_multipage.pdf | tax | got 11806.93 want 11860.93 |
| 005_day_first.pdf | supplier_name | got None want Kestrel Industrial Parts |
| 005_day_first.pdf | document_date | got 2025-11-06 want 2025-06-11 |
| 005_day_first.pdf | subtotal | got 287772.93 want 28772.93 |
| 005_day_first.pdf | total | got 287772.93 want 28772.93 |
| 007_label_variants.pdf | subtotal | got 0.00 want 8521.80 |
| 007_label_variants.pdf | tax | got 0.00 want 681.74 |
| 007_label_variants.pdf | total | got 0.00 want 9203.54 |
| 007_label_variants.pdf | line_items_exact | got 2 items want 2 |
| 008_purchase_order.pdf | document_type | got invoice want purchase_order |
| 009_unlabelled_supplier.pdf | line_items_exact | got 3 items want 3 |
| 011_day_first.pdf | supplier_name | got None want Orbital Print & Design |
| 012_classic.pdf | subtotal | got 29105.49 want 29015.49 |
| 013_label_variants.pdf | subtotal | got 0.00 want 21108.61 |
| 013_label_variants.pdf | total | got 21581.61 want 21108.61 |
| 013_label_variants.pdf | line_items_count | got 2 items want 3 |
| 013_label_variants.pdf | line_items_exact | got 2 items want 3 |
| 014_purchase_order.pdf | document_type | got invoice want purchase_order |
| 014_purchase_order.pdf | total | got 29470.57 want 29570.57 |
| 014_purchase_order.pdf | line_items_exact | got 3 items want 3 |
| 015_unlabelled_supplier.pdf | subtotal | got 23163.26 want 23316.26 |
| 015_unlabelled_supplier.pdf | total | got 27899.51 want 27979.51 |
| 017_day_first.pdf | supplier_name | got None want Blue Harbor Logistics GmbH |
| 017_day_first.pdf | line_items_exact | got 3 items want 3 |
| 018_classic.pdf | total | got 30494.90 want 30394.90 |
| 019_label_variants.pdf | subtotal | got 7333.20 want 35357.17 |
| 019_label_variants.pdf | total | got 10171.77 want 38185.74 |
| 019_label_variants.pdf | line_items_exact | got 5 items want 5 |
| 020_purchase_order.pdf | document_type | got invoice want purchase_order |
| 020_purchase_order.pdf | subtotal | got 18063.32 want 18006.32 |
| 020_purchase_order.pdf | total | got 18063.32 want 18006.32 |
| 021_unlabelled_supplier.pdf | line_items_exact | got 5 items want 5 |
| 022_multipage.pdf | line_items_exact | got 16 items want 16 |
| 023_day_first.pdf | document_date | got 2024-02-10 want 2024-10-02 |
| 023_day_first.pdf | line_items_exact | got 4 items want 4 |
| 024_classic.pdf | subtotal | got 35655.36 want 36555.36 |
| 025_label_variants.pdf | subtotal | got 11371.58 want 24157.59 |
| 025_label_variants.pdf | total | got 16298.11 want 28989.11 |
| 025_label_variants.pdf | line_items_exact | got 4 items want 4 |
| 026_purchase_order.pdf | document_type | got invoice want purchase_order |
| 026_purchase_order.pdf | total | got 22231.69 want 22831.69 |
| 026_purchase_order.pdf | line_items_exact | got 3 items want 3 |
| 027_unlabelled_supplier.pdf | tax | got 2673.07 want 2693.07 |
| 027_unlabelled_supplier.pdf | total | got 36366.46 want 36356.46 |
| 027_unlabelled_supplier.pdf | line_items_exact | got 4 items want 4 |
| 029_day_first.pdf | supplier_name | got None want Orbital Print & Design |
| 029_day_first.pdf | document_date | got 2025-01-04 want 2025-04-01 |
| 029_day_first.pdf | line_items_exact | got 2 items want 2 |
