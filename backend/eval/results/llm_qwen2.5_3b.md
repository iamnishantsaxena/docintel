# Eval: llm:qwen2.5:3b

- Run: 2026-10-29 12:28 UTC on macOS-27.0.1-arm64-arm-64bit
- Dataset: `eval/dataset/synthetic` (30 PDFs)
- Model: qwen2.5:3b @ http://localhost:11434/v1
- Latency per document: median 15.03s, max 48.88s
- Docs where the model output was unusable for ≥1 chunk (regex fallback): 0
- Docs with no result because the LLM call failed (timeout 300.0s): 1 (016_multipage.pdf)
- **Overall field accuracy: 96.3%** (363/377 field checks)

| Field | Accuracy |
|---|---|
| document_type | 100.0% |
| supplier_name | 100.0% |
| customer_name | 100.0% |
| document_number | 96.6% |
| po_number | 100.0% |
| document_date | 96.6% |
| due_date | 100.0% |
| currency | 100.0% |
| subtotal | 100.0% |
| tax | 100.0% |
| total | 100.0% |
| line_items_count | 86.2% |
| line_items_exact | 72.4% |

| Template | Mean field accuracy | Docs |
|---|---|---|
| classic | 100.0% | 5 |
| day_first | 96.9% | 5 |
| label_variants | 95.4% | 5 |
| multipage | 86.5% | 4 |
| purchase_order | 98.5% | 5 |
| unlabelled_supplier | 98.5% | 5 |

## Misses

| File | Field | Detail |
|---|---|---|
| 001_label_variants.pdf | line_items_exact | got 5 items want 5 |
| 008_purchase_order.pdf | line_items_exact | got 5 items want 5 |
| 010_multipage.pdf | document_number | got INVOICE BL-99322 want BL-99322 |
| 010_multipage.pdf | line_items_count | got 14 items want 17 |
| 010_multipage.pdf | line_items_exact | got 14 items want 17 |
| 016_multipage.pdf | LLM | LLM request failed: ReadTimeout |
| 019_label_variants.pdf | line_items_count | got 4 items want 5 |
| 019_label_variants.pdf | line_items_exact | got 4 items want 5 |
| 021_unlabelled_supplier.pdf | line_items_exact | got 5 items want 5 |
| 022_multipage.pdf | line_items_count | got 8 items want 16 |
| 022_multipage.pdf | line_items_exact | got 8 items want 16 |
| 023_day_first.pdf | line_items_exact | got 4 items want 4 |
| 028_multipage.pdf | line_items_count | got 17 items want 19 |
| 028_multipage.pdf | line_items_exact | got 17 items want 19 |
| 029_day_first.pdf | document_date | got 2025-01-04 want 2025-04-01 |
