# Eval: llm:qwen2.5:1.5b

- Run: 2026-10-29 12:45 UTC on macOS-27.0.1-arm64-arm-64bit
- Dataset: `eval/dataset/synthetic` (30 PDFs)
- Model: qwen2.5:1.5b @ http://localhost:11434/v1
- Latency per document: median 10.10s, max 29.75s
- Docs where the model output was unusable for ≥1 chunk (regex fallback): 0
- Docs with no result because the LLM call failed (timeout 300.0s): 0
- **Overall field accuracy: 96.9%** (378/390 field checks)

| Field | Accuracy |
|---|---|
| document_type | 100.0% |
| supplier_name | 96.7% |
| customer_name | 96.7% |
| document_number | 100.0% |
| po_number | 100.0% |
| document_date | 100.0% |
| due_date | 100.0% |
| currency | 100.0% |
| subtotal | 93.3% |
| tax | 100.0% |
| total | 100.0% |
| line_items_count | 96.7% |
| line_items_exact | 76.7% |

| Template | Mean field accuracy | Docs |
|---|---|---|
| classic | 98.5% | 5 |
| day_first | 96.9% | 5 |
| label_variants | 93.8% | 5 |
| multipage | 96.9% | 5 |
| purchase_order | 98.5% | 5 |
| unlabelled_supplier | 96.9% | 5 |

## Misses

| File | Field | Detail |
|---|---|---|
| 001_label_variants.pdf | subtotal | got 28506.84 want 46865.11 |
| 001_label_variants.pdf | line_items_exact | got 5 items want 5 |
| 005_day_first.pdf | line_items_exact | got 5 items want 5 |
| 006_classic.pdf | line_items_exact | got 5 items want 5 |
| 015_unlabelled_supplier.pdf | supplier_name | got Hooli Labs want ORBITAL PRINT & DESIGN |
| 015_unlabelled_supplier.pdf | customer_name | got ORBITAL PRINT & DESIGN want Hooli Labs |
| 020_purchase_order.pdf | line_items_exact | got 4 items want 4 |
| 025_label_variants.pdf | subtotal | got 11372.58 want 24157.59 |
| 025_label_variants.pdf | line_items_exact | got 4 items want 4 |
| 028_multipage.pdf | line_items_count | got 16 items want 19 |
| 028_multipage.pdf | line_items_exact | got 16 items want 19 |
| 029_day_first.pdf | line_items_exact | got 2 items want 2 |
