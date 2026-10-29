# Eval: regex-only

- Run: 2026-10-29 13:08 UTC on macOS-27.0.1-arm64-arm-64bit
- Dataset: `eval/dataset/synthetic` (30 PDFs)
- Model: none @ -
- Latency per document: median 0.01s, max 0.03s
- LLM: not used

- **Overall field accuracy: 86.7%** (338/390 field checks)

| Field | Accuracy |
|---|---|
| document_type | 100.0% |
| supplier_name | 33.3% |
| customer_name | 83.3% |
| document_number | 83.3% |
| po_number | 90.0% |
| document_date | 73.3% |
| due_date | 80.0% |
| currency | 100.0% |
| subtotal | 83.3% |
| tax | 100.0% |
| total | 100.0% |
| line_items_count | 100.0% |
| line_items_exact | 100.0% |

| Template | Mean field accuracy | Docs |
|---|---|---|
| classic | 92.3% | 5 |
| day_first | 86.2% | 5 |
| label_variants | 87.7% | 5 |
| multipage | 92.3% | 5 |
| purchase_order | 100.0% | 5 |
| unlabelled_supplier | 61.5% | 5 |

## Misses

| File | Field | Detail |
|---|---|---|
| 000_classic.pdf | supplier_name | got None want Blue Harbor Logistics GmbH |
| 001_label_variants.pdf | po_number | got None want PO-2929 |
| 001_label_variants.pdf | subtotal | got None want 46865.11 |
| 003_unlabelled_supplier.pdf | supplier_name | got None want NORTHWIND TRADERS |
| 003_unlabelled_supplier.pdf | customer_name | got None want Globex Corp |
| 003_unlabelled_supplier.pdf | document_number | got None want INV-45833 |
| 003_unlabelled_supplier.pdf | document_date | got None want 2025-06-08 |
| 003_unlabelled_supplier.pdf | due_date | got None want 2025-08-07 |
| 004_multipage.pdf | supplier_name | got None want Kestrel Industrial Parts |
| 005_day_first.pdf | supplier_name | got None want Kestrel Industrial Parts |
| 005_day_first.pdf | document_date | got 2025-11-06 want 2025-06-11 |
| 006_classic.pdf | supplier_name | got None want Blue Harbor Logistics GmbH |
| 007_label_variants.pdf | subtotal | got None want 8521.80 |
| 009_unlabelled_supplier.pdf | supplier_name | got None want SUNRISE PACKAGING CO. |
| 009_unlabelled_supplier.pdf | customer_name | got None want Umbrella Retail |
| 009_unlabelled_supplier.pdf | document_number | got None want BL-46812 |
| 009_unlabelled_supplier.pdf | document_date | got None want 2024-12-18 |
| 009_unlabelled_supplier.pdf | due_date | got None want 2025-02-16 |
| 010_multipage.pdf | supplier_name | got None want Kestrel Industrial Parts |
| 011_day_first.pdf | supplier_name | got None want Orbital Print & Design |
| 011_day_first.pdf | due_date | got 2024-12-06 want 2024-06-12 |
| 012_classic.pdf | supplier_name | got None want Blue Harbor Logistics GmbH |
| 013_label_variants.pdf | subtotal | got None want 21108.61 |
| 015_unlabelled_supplier.pdf | supplier_name | got None want ORBITAL PRINT & DESIGN |
| 015_unlabelled_supplier.pdf | customer_name | got None want Hooli Labs |
| 015_unlabelled_supplier.pdf | document_number | got None want IN-26656 |
| 015_unlabelled_supplier.pdf | document_date | got None want 2025-02-17 |
| 015_unlabelled_supplier.pdf | due_date | got None want 2025-04-03 |
| 016_multipage.pdf | supplier_name | got None want Sunrise Packaging Co. |
| 017_day_first.pdf | supplier_name | got None want Blue Harbor Logistics GmbH |
| 018_classic.pdf | supplier_name | got None want Initech Office Solutions |
| 019_label_variants.pdf | po_number | got None want PO-7240 |
| 019_label_variants.pdf | subtotal | got None want 35357.17 |
| 021_unlabelled_supplier.pdf | supplier_name | got None want ACME SUPPLIES LTD |
| 021_unlabelled_supplier.pdf | customer_name | got None want Stark Manufacturing |
| 021_unlabelled_supplier.pdf | document_number | got None want INV-77753 |
| 021_unlabelled_supplier.pdf | document_date | got None want 2024-11-07 |
| 021_unlabelled_supplier.pdf | due_date | got None want 2024-12-07 |
| 022_multipage.pdf | supplier_name | got None want ACME Supplies Ltd |
| 023_day_first.pdf | supplier_name | got None want ACME Supplies Ltd |
| 023_day_first.pdf | document_date | got 2024-02-10 want 2024-10-02 |
| 024_classic.pdf | supplier_name | got None want Maple Leaf Hardware Inc. |
| 025_label_variants.pdf | po_number | got None want PO-9055 |
| 025_label_variants.pdf | subtotal | got None want 24157.59 |
| 027_unlabelled_supplier.pdf | supplier_name | got None want SUNRISE PACKAGING CO. |
| 027_unlabelled_supplier.pdf | customer_name | got None want Wayne Hospitality Group |
| 027_unlabelled_supplier.pdf | document_number | got None want INV-49935 |
| 027_unlabelled_supplier.pdf | document_date | got None want 2025-06-07 |
| 027_unlabelled_supplier.pdf | due_date | got None want 2025-07-22 |
| 028_multipage.pdf | supplier_name | got None want ACME Supplies Ltd |
| 029_day_first.pdf | supplier_name | got None want Orbital Print & Design |
| 029_day_first.pdf | document_date | got 2025-01-04 want 2025-04-01 |
