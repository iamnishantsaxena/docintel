# Eval: llm:qwen2.5:1.5b

- Run: 2026-11-07 12:24 UTC on macOS-27.0.1-arm64-arm-64bit
- Dataset: `eval/dataset/company` (100 PDFs)
- Model: qwen2.5:1.5b @ http://localhost:11434/v1
- Latency per document: median 7.83s, max 46.06s
- Docs where the model output was unusable for ≥1 chunk (regex fallback): 0
- Docs with no result because the LLM call failed (timeout 300.0s): 0
- **Overall field accuracy: 83.8%** (1089/1300 field checks)
- Accuracy on printed fields (truth has a value; incl. line items): 84.9% (594/700)
- Not-printed fields correctly left empty (1 − invented-value rate): 82.5% (495/600)

| Field | Accuracy |
|---|---|
| document_type | 100.0% |
| supplier_name | 97.0% |
| customer_name | 72.0% |
| document_number | 94.0% |
| po_number | 92.0% |
| document_date | 100.0% |
| due_date | 100.0% |
| currency | 50.0% |
| subtotal | 50.0% |
| tax | 98.0% |
| total | 100.0% |
| line_items_count | 86.0% |
| line_items_exact | 50.0% |

| Template | Mean field accuracy | Docs |
|---|---|---|
| invoice | 76.8% | 50 |
| purchase_order | 90.8% | 50 |

## Misses

| File | Field | Detail |
|---|---|---|
| 10286_invoice.pdf | customer_name | got QUICK want Horst Kloss |
| 10286_invoice.pdf | currency | got EUR want None |
| 10286_invoice.pdf | subtotal | got 3016.00 want None |
| 10295_invoice.pdf | customer_name | got VINET want Paul Henriot |
| 10295_invoice.pdf | currency | got EUR want None |
| 10295_invoice.pdf | subtotal | got 121.60 want None |
| 10297_invoice.pdf | currency | got EUR want None |
| 10297_invoice.pdf | subtotal | got 1420.00 want None |
| 10298_invoice.pdf | customer_name | got HUNGO want Patricia McKenna |
| 10298_invoice.pdf | currency | got EUR want None |
| 10298_invoice.pdf | subtotal | got 3127.00 want None |
| 10298_purchase_order.pdf | document_number | got None want 10298 |
| 10298_purchase_order.pdf | line_items_exact | got 4 items want 4 |
| 10307_invoice.pdf | customer_name | got LONEP want Fran Wilson |
| 10307_invoice.pdf | currency | got USD want None |
| 10307_invoice.pdf | subtotal | got 424.00 want None |
| 10308_invoice.pdf | currency | got EUR want None |
| 10308_invoice.pdf | subtotal | got 88.80 want None |
| 10308_purchase_order.pdf | po_number | got None want 10308 |
| 10308_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10308_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10311_invoice.pdf | currency | got USD want None |
| 10311_invoice.pdf | subtotal | got 268.80 want None |
| 10319_invoice.pdf | customer_name | got TORTU want Miguel Angel Paolino |
| 10319_invoice.pdf | currency | got USD want None |
| 10319_invoice.pdf | subtotal | got 1191.20 want None |
| 10319_invoice.pdf | line_items_exact | got 3 items want 3 |
| 10319_purchase_order.pdf | line_items_exact | got 3 items want 3 |
| 10322_invoice.pdf | customer_name | got PERIC want Guillermo Fernández |
| 10322_invoice.pdf | currency | got USD want None |
| 10322_invoice.pdf | subtotal | got 112.00 want None |
| 10322_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10322_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10336_invoice.pdf | currency | got EUR want None |
| 10336_invoice.pdf | subtotal | got 316.80 want None |
| 10336_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10336_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10340_invoice.pdf | currency | got EUR want None |
| 10340_invoice.pdf | subtotal | got 2564.40 want None |
| 10344_invoice.pdf | customer_name | got WHITC want Karl Jablonski |
| 10344_invoice.pdf | currency | got USD want None |
| 10344_invoice.pdf | subtotal | got 2856.00 want None |
| 10344_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10353_invoice.pdf | customer_name | got PICCO want Georg Pipps |
| 10353_invoice.pdf | currency | got EUR want None |
| 10353_invoice.pdf | subtotal | got 10741.60 want None |
| 10368_invoice.pdf | customer_name | got ERNSH want Roland Mendel |
| 10368_invoice.pdf | currency | got EUR want None |
| 10368_invoice.pdf | subtotal | got 1834.20 want None |
| 10368_invoice.pdf | line_items_exact | got 4 items want 4 |
| 10368_purchase_order.pdf | po_number | got None want 10368 |
| 10374_invoice.pdf | currency | got PLN want None |
| 10374_invoice.pdf | subtotal | got 459.00 want None |
| 10374_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10374_purchase_order.pdf | line_items_exact | got 2 items want 2 |
| 10384_invoice.pdf | customer_name | got BERGS want Christina Berglund |
| 10384_invoice.pdf | currency | got SEK want None |
| 10384_invoice.pdf | subtotal | got 2222.40 want None |
| 10384_invoice.pdf | tax | got 0.00 want None |
| 10384_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10384_purchase_order.pdf | line_items_exact | got 2 items want 2 |
| 10395_invoice.pdf | currency | got USD want None |
| 10395_invoice.pdf | subtotal | got 2333.20 want None |
| 10395_invoice.pdf | line_items_exact | got 3 items want 3 |
| 10395_purchase_order.pdf | line_items_exact | got 3 items want 3 |
| 10402_invoice.pdf | customer_name | got ERNSH want Roland Mendel |
| 10402_invoice.pdf | currency | got EUR want None |
| 10402_invoice.pdf | subtotal | got 2713.50 want None |
| 10402_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10402_purchase_order.pdf | document_number | got None want 10402 |
| 10402_purchase_order.pdf | line_items_exact | got 2 items want 2 |
| 10433_invoice.pdf | currency | got EUR want None |
| 10433_invoice.pdf | subtotal | got 851.20 want None |
| 10433_invoice.pdf | tax | got 0.00 want None |
| 10467_invoice.pdf | currency | got EUR want None |
| 10467_invoice.pdf | subtotal | got 235.20 want None |
| 10467_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10467_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10467_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10474_invoice.pdf | customer_name | got PERIC want Guillermo Fernández |
| 10474_invoice.pdf | currency | got USD want None |
| 10474_invoice.pdf | subtotal | got 1249.10 want None |
| 10474_purchase_order.pdf | document_number | got None want 10474 |
| 10474_purchase_order.pdf | line_items_exact | got 4 items want 4 |
| 10476_invoice.pdf | currency | got USD want None |
| 10476_invoice.pdf | subtotal | got 182.40 want None |
| 10476_purchase_order.pdf | document_number | got None want 10476 |
| 10494_invoice.pdf | customer_name | got COMMI want Pedro Afonso |
| 10494_invoice.pdf | currency | got EUR want None |
| 10494_invoice.pdf | subtotal | got 912.00 want None |
| 10494_purchase_order.pdf | supplier_name | got Pedro Afonso want None |
| 10544_invoice.pdf | customer_name | got LONEP want Fran Wilson |
| 10544_invoice.pdf | currency | got USD want None |
| 10544_invoice.pdf | subtotal | got 417.20 want None |
| 10544_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10544_purchase_order.pdf | line_items_exact | got 2 items want 2 |
| 10563_invoice.pdf | customer_name | got RICAR want Janete Limeira |
| 10563_invoice.pdf | currency | got BRL want None |
| 10563_invoice.pdf | subtotal | got 965.00 want None |
| 10563_purchase_order.pdf | po_number | got None want 10563 |
| 10563_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10563_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10579_invoice.pdf | currency | got USD want None |
| 10579_invoice.pdf | subtotal | got 317.75 want None |
| 10579_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10579_purchase_order.pdf | line_items_exact | got 2 items want 2 |
| 10622_invoice.pdf | customer_name | got RICAR want Janete Limeira |
| 10622_invoice.pdf | currency | got BRL want None |
| 10622_invoice.pdf | subtotal | got 605.00 want None |
| 10622_purchase_order.pdf | po_number | got None want 10622 |
| 10622_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10622_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10652_invoice.pdf | currency | got BRL want None |
| 10652_invoice.pdf | subtotal | got 331.78 want None |
| 10654_invoice.pdf | customer_name | got BERGS want Christina Berglund |
| 10654_invoice.pdf | currency | got SEK want None |
| 10654_invoice.pdf | subtotal | got 668.70 want None |
| 10676_invoice.pdf | customer_name | got TORTU want Miguel Angel Paolino |
| 10676_invoice.pdf | currency | got USD want None |
| 10676_invoice.pdf | subtotal | got 534.85 want None |
| 10676_invoice.pdf | line_items_exact | got 3 items want 3 |
| 10676_purchase_order.pdf | supplier_name | got Miguel Angel Paolino want None |
| 10676_purchase_order.pdf | line_items_exact | got 3 items want 3 |
| 10677_invoice.pdf | customer_name | got ANTON want Antonio Moreno |
| 10677_invoice.pdf | currency | got MXN want None |
| 10677_invoice.pdf | subtotal | got 956.90 want None |
| 10677_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10677_purchase_order.pdf | line_items_exact | got 2 items want 2 |
| 10682_invoice.pdf | customer_name | got ANTON want Antonio Moreno |
| 10682_invoice.pdf | currency | got USD want None |
| 10682_invoice.pdf | subtotal | got 375.50 want None |
| 10692_invoice.pdf | customer_name | got ALFKI want Maria Anders |
| 10692_invoice.pdf | currency | got EUR want None |
| 10692_invoice.pdf | subtotal | got 878.00 want None |
| 10692_invoice.pdf | line_items_exact | got 1 items want 1 |
| 10692_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10692_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10767_invoice.pdf | currency | got EUR want None |
| 10767_invoice.pdf | subtotal | got 28.00 want None |
| 10767_invoice.pdf | line_items_exact | got 1 items want 1 |
| 10767_purchase_order.pdf | supplier_name | got Pascale Cartrain want None |
| 10796_invoice.pdf | currency | got USD want None |
| 10796_invoice.pdf | subtotal | got 2878.08 want None |
| 10796_invoice.pdf | line_items_exact | got 4 items want 4 |
| 10796_purchase_order.pdf | document_number | got None want 10796 |
| 10796_purchase_order.pdf | line_items_exact | got 4 items want 4 |
| 10801_invoice.pdf | currency | got EUR want None |
| 10801_invoice.pdf | subtotal | got 4035.80 want None |
| 10801_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10801_purchase_order.pdf | line_items_exact | got 2 items want 2 |
| 10812_invoice.pdf | currency | got EUR want None |
| 10812_invoice.pdf | subtotal | got 1852.00 want None |
| 10812_invoice.pdf | line_items_exact | got 3 items want 3 |
| 10812_purchase_order.pdf | line_items_exact | got 3 items want 3 |
| 10818_invoice.pdf | currency | got EUR want None |
| 10818_invoice.pdf | subtotal | got 833.00 want None |
| 10821_invoice.pdf | currency | got USD want None |
| 10821_invoice.pdf | subtotal | got 678.00 want None |
| 10821_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10821_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10827_invoice.pdf | currency | got EUR want None |
| 10827_invoice.pdf | subtotal | got 843.00 want None |
| 10827_purchase_order.pdf | po_number | got None want 10827 |
| 10827_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10827_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10832_invoice.pdf | customer_name | got LAMAI want Annette Roulet |
| 10832_invoice.pdf | currency | got EUR want None |
| 10832_invoice.pdf | subtotal | got 568.95 want None |
| 10832_purchase_order.pdf | document_number | got None want 10832 |
| 10832_purchase_order.pdf | line_items_exact | got 4 items want 4 |
| 10838_invoice.pdf | customer_name | got LINOD want Felipe Izquierdo |
| 10838_invoice.pdf | currency | got USD want None |
| 10838_invoice.pdf | subtotal | got 2584.50 want None |
| 10843_invoice.pdf | customer_name | got VICTE want Mary Saveley |
| 10843_invoice.pdf | currency | got EUR want None |
| 10843_invoice.pdf | subtotal | got 212.00 want None |
| 10844_invoice.pdf | customer_name | got PICCO want Georg Pipps |
| 10844_invoice.pdf | currency | got SEK want None |
| 10844_invoice.pdf | subtotal | got 735.00 want None |
| 10844_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10844_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10847_invoice.pdf | customer_name | got SAVEA want Jose Pavarotti |
| 10847_invoice.pdf | currency | got USD want None |
| 10847_invoice.pdf | subtotal | got 6164.90 want None |
| 10847_invoice.pdf | line_items_exact | got 6 items want 6 |
| 10847_purchase_order.pdf | po_number | got None want 10847 |
| 10847_purchase_order.pdf | line_items_exact | got 6 items want 6 |
| 10890_invoice.pdf | currency | got EUR want None |
| 10890_invoice.pdf | subtotal | got 860.10 want None |
| 10890_purchase_order.pdf | po_number | got None want 10890 |
| 10890_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10890_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10893_invoice.pdf | currency | got EUR want None |
| 10893_invoice.pdf | subtotal | got 5502.11 want None |
| 10893_invoice.pdf | line_items_exact | got 5 items want 5 |
| 10893_purchase_order.pdf | po_number | got None want 10893 |
| 10893_purchase_order.pdf | line_items_exact | got 5 items want 5 |
| 10914_invoice.pdf | customer_name | got QUEEN want Lúcia Carvalho |
| 10914_invoice.pdf | currency | got BRL want None |
| 10914_invoice.pdf | subtotal | got 537.50 want None |
| 10914_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10914_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10946_invoice.pdf | currency | got DKK want None |
| 10946_invoice.pdf | subtotal | got 1407.50 want None |
| 11077_invoice.pdf | customer_name | got RATTC want Paula Wilson |
| 11077_invoice.pdf | currency | got USD want None |
| 11077_invoice.pdf | subtotal | got 1374.60 want None |
| 11077_invoice.pdf | line_items_count | got 26 items want 25 |
| 11077_invoice.pdf | line_items_exact | got 26 items want 25 |
| 11077_purchase_order.pdf | line_items_count | got 23 items want 25 |
| 11077_purchase_order.pdf | line_items_exact | got 23 items want 25 |
