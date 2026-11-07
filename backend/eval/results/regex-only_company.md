# Eval: regex-only

- Run: 2026-11-07 12:10 UTC on macOS-27.0.1-arm64-arm-64bit
- Dataset: `eval/dataset/company` (100 PDFs)
- Model: none @ -
- Latency per document: median 0.01s, max 0.03s
- LLM: not used
- LLM errors: n/a
- **Overall field accuracy: 57.8%** (751/1300 field checks)
- Accuracy on printed fields (truth has a value; incl. line items): 21.6% (151/700)
- Not-printed fields correctly left empty (1 − invented-value rate): 100.0% (600/600)

| Field | Accuracy |
|---|---|
| document_type | 100.0% |
| supplier_name | 100.0% |
| customer_name | 0.0% |
| document_number | 0.0% |
| po_number | 50.0% |
| document_date | 50.0% |
| due_date | 100.0% |
| currency | 100.0% |
| subtotal | 100.0% |
| tax | 100.0% |
| total | 50.0% |
| line_items_count | 1.0% |
| line_items_exact | 0.0% |

| Template | Mean field accuracy | Docs |
|---|---|---|
| invoice | 61.7% | 50 |
| purchase_order | 53.8% | 50 |

## Misses

| File | Field | Detail |
|---|---|---|
| 10286_invoice.pdf | customer_name | got None want Horst Kloss |
| 10286_invoice.pdf | document_number | got None want 10286 |
| 10286_invoice.pdf | total | got None want 3016.00 |
| 10286_invoice.pdf | line_items_count | got 0 items want 2 |
| 10286_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10286_purchase_order.pdf | customer_name | got None want Horst Kloss |
| 10286_purchase_order.pdf | document_number | got None want 10286 |
| 10286_purchase_order.pdf | po_number | got None want 10286 |
| 10286_purchase_order.pdf | document_date | got None want 2016-08-21 |
| 10286_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10286_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10295_invoice.pdf | customer_name | got None want Paul Henriot |
| 10295_invoice.pdf | document_number | got None want 10295 |
| 10295_invoice.pdf | total | got None want 121.60 |
| 10295_invoice.pdf | line_items_count | got 0 items want 1 |
| 10295_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10295_purchase_order.pdf | customer_name | got None want Paul Henriot |
| 10295_purchase_order.pdf | document_number | got None want 10295 |
| 10295_purchase_order.pdf | po_number | got None want 10295 |
| 10295_purchase_order.pdf | document_date | got None want 2016-09-02 |
| 10295_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10295_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10297_invoice.pdf | customer_name | got None want Frédérique Citeaux |
| 10297_invoice.pdf | document_number | got None want 10297 |
| 10297_invoice.pdf | total | got None want 1420.00 |
| 10297_invoice.pdf | line_items_count | got 0 items want 2 |
| 10297_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10297_purchase_order.pdf | customer_name | got None want Frédérique Citeaux |
| 10297_purchase_order.pdf | document_number | got None want 10297 |
| 10297_purchase_order.pdf | po_number | got None want 10297 |
| 10297_purchase_order.pdf | document_date | got None want 2016-09-04 |
| 10297_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10297_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10298_invoice.pdf | customer_name | got None want Patricia McKenna |
| 10298_invoice.pdf | document_number | got None want 10298 |
| 10298_invoice.pdf | total | got None want 3127.00 |
| 10298_invoice.pdf | line_items_count | got 0 items want 4 |
| 10298_invoice.pdf | line_items_exact | got 0 items want 4 |
| 10298_purchase_order.pdf | customer_name | got None want Patricia McKenna |
| 10298_purchase_order.pdf | document_number | got None want 10298 |
| 10298_purchase_order.pdf | po_number | got None want 10298 |
| 10298_purchase_order.pdf | document_date | got None want 2016-09-05 |
| 10298_purchase_order.pdf | line_items_count | got 0 items want 4 |
| 10298_purchase_order.pdf | line_items_exact | got 0 items want 4 |
| 10307_invoice.pdf | customer_name | got None want Fran Wilson |
| 10307_invoice.pdf | document_number | got None want 10307 |
| 10307_invoice.pdf | total | got None want 424.00 |
| 10307_invoice.pdf | line_items_count | got 0 items want 2 |
| 10307_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10307_purchase_order.pdf | customer_name | got None want Fran Wilson |
| 10307_purchase_order.pdf | document_number | got None want 10307 |
| 10307_purchase_order.pdf | po_number | got None want 10307 |
| 10307_purchase_order.pdf | document_date | got None want 2016-09-17 |
| 10307_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10307_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10308_invoice.pdf | customer_name | got None want Ana Trujillo |
| 10308_invoice.pdf | document_number | got None want 10308 |
| 10308_invoice.pdf | total | got None want 88.80 |
| 10308_invoice.pdf | line_items_count | got 0 items want 2 |
| 10308_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10308_purchase_order.pdf | customer_name | got None want Ana Trujillo |
| 10308_purchase_order.pdf | document_number | got None want 10308 |
| 10308_purchase_order.pdf | po_number | got None want 10308 |
| 10308_purchase_order.pdf | document_date | got None want 2016-09-18 |
| 10308_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10308_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10311_invoice.pdf | customer_name | got None want Janine Labrune |
| 10311_invoice.pdf | document_number | got None want 10311 |
| 10311_invoice.pdf | total | got None want 268.80 |
| 10311_invoice.pdf | line_items_count | got 0 items want 2 |
| 10311_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10311_purchase_order.pdf | customer_name | got None want Janine Labrune |
| 10311_purchase_order.pdf | document_number | got None want 10311 |
| 10311_purchase_order.pdf | po_number | got None want 10311 |
| 10311_purchase_order.pdf | document_date | got None want 2016-09-20 |
| 10311_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10311_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10319_invoice.pdf | customer_name | got None want Miguel Angel Paolino |
| 10319_invoice.pdf | document_number | got None want 10319 |
| 10319_invoice.pdf | total | got None want 1191.20 |
| 10319_invoice.pdf | line_items_count | got 0 items want 3 |
| 10319_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10319_purchase_order.pdf | customer_name | got None want Miguel Angel Paolino |
| 10319_purchase_order.pdf | document_number | got None want 10319 |
| 10319_purchase_order.pdf | po_number | got None want 10319 |
| 10319_purchase_order.pdf | document_date | got None want 2016-10-02 |
| 10319_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10319_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10322_invoice.pdf | customer_name | got None want Guillermo Fernández |
| 10322_invoice.pdf | document_number | got None want 10322 |
| 10322_invoice.pdf | total | got None want 112.00 |
| 10322_invoice.pdf | line_items_count | got 0 items want 1 |
| 10322_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10322_purchase_order.pdf | customer_name | got None want Guillermo Fernández |
| 10322_purchase_order.pdf | document_number | got None want 10322 |
| 10322_purchase_order.pdf | po_number | got None want 10322 |
| 10322_purchase_order.pdf | document_date | got None want 2016-10-04 |
| 10322_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10322_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10336_invoice.pdf | customer_name | got None want Isabel de Castro |
| 10336_invoice.pdf | document_number | got None want 10336 |
| 10336_invoice.pdf | total | got None want 316.80 |
| 10336_invoice.pdf | line_items_count | got 0 items want 1 |
| 10336_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10336_purchase_order.pdf | customer_name | got None want Isabel de Castro |
| 10336_purchase_order.pdf | document_number | got None want 10336 |
| 10336_purchase_order.pdf | po_number | got None want 10336 |
| 10336_purchase_order.pdf | document_date | got None want 2016-10-23 |
| 10336_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10336_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10340_invoice.pdf | customer_name | got None want Laurence Lebihan |
| 10340_invoice.pdf | document_number | got None want 10340 |
| 10340_invoice.pdf | total | got None want 2564.40 |
| 10340_invoice.pdf | line_items_count | got 0 items want 3 |
| 10340_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10340_purchase_order.pdf | customer_name | got None want Laurence Lebihan |
| 10340_purchase_order.pdf | document_number | got None want 10340 |
| 10340_purchase_order.pdf | po_number | got None want 10340 |
| 10340_purchase_order.pdf | document_date | got None want 2016-10-29 |
| 10340_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10340_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10344_invoice.pdf | customer_name | got None want Karl Jablonski |
| 10344_invoice.pdf | document_number | got None want 10344 |
| 10344_invoice.pdf | total | got None want 2856.00 |
| 10344_invoice.pdf | line_items_count | got 0 items want 2 |
| 10344_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10344_purchase_order.pdf | customer_name | got None want Karl Jablonski |
| 10344_purchase_order.pdf | document_number | got None want 10344 |
| 10344_purchase_order.pdf | po_number | got None want 10344 |
| 10344_purchase_order.pdf | document_date | got None want 2016-11-01 |
| 10344_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10344_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10353_invoice.pdf | customer_name | got None want Georg Pipps |
| 10353_invoice.pdf | document_number | got None want 10353 |
| 10353_invoice.pdf | total | got None want 10741.60 |
| 10353_invoice.pdf | line_items_count | got 0 items want 2 |
| 10353_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10353_purchase_order.pdf | customer_name | got None want Georg Pipps |
| 10353_purchase_order.pdf | document_number | got None want 10353 |
| 10353_purchase_order.pdf | po_number | got None want 10353 |
| 10353_purchase_order.pdf | document_date | got None want 2016-11-13 |
| 10353_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10353_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10368_invoice.pdf | customer_name | got None want Roland Mendel |
| 10368_invoice.pdf | document_number | got None want 10368 |
| 10368_invoice.pdf | total | got None want 1834.20 |
| 10368_invoice.pdf | line_items_count | got 0 items want 4 |
| 10368_invoice.pdf | line_items_exact | got 0 items want 4 |
| 10368_purchase_order.pdf | customer_name | got None want Roland Mendel |
| 10368_purchase_order.pdf | document_number | got None want 10368 |
| 10368_purchase_order.pdf | po_number | got None want 10368 |
| 10368_purchase_order.pdf | document_date | got None want 2016-11-29 |
| 10368_purchase_order.pdf | line_items_count | got 0 items want 4 |
| 10368_purchase_order.pdf | line_items_exact | got 0 items want 4 |
| 10374_invoice.pdf | customer_name | got None want Zbyszek Piestrzeniewicz |
| 10374_invoice.pdf | document_number | got None want 10374 |
| 10374_invoice.pdf | total | got None want 459.00 |
| 10374_invoice.pdf | line_items_count | got 0 items want 2 |
| 10374_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10374_purchase_order.pdf | customer_name | got None want Zbyszek Piestrzeniewicz |
| 10374_purchase_order.pdf | document_number | got None want 10374 |
| 10374_purchase_order.pdf | po_number | got None want 10374 |
| 10374_purchase_order.pdf | document_date | got None want 2016-12-05 |
| 10374_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10374_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10384_invoice.pdf | customer_name | got None want Christina Berglund |
| 10384_invoice.pdf | document_number | got None want 10384 |
| 10384_invoice.pdf | total | got None want 2222.40 |
| 10384_invoice.pdf | line_items_count | got 0 items want 2 |
| 10384_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10384_purchase_order.pdf | customer_name | got None want Christina Berglund |
| 10384_purchase_order.pdf | document_number | got None want 10384 |
| 10384_purchase_order.pdf | po_number | got None want 10384 |
| 10384_purchase_order.pdf | document_date | got None want 2016-12-16 |
| 10384_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10384_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10395_invoice.pdf | customer_name | got None want Carlos Hernández |
| 10395_invoice.pdf | document_number | got None want 10395 |
| 10395_invoice.pdf | total | got None want 2333.20 |
| 10395_invoice.pdf | line_items_count | got 0 items want 3 |
| 10395_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10395_purchase_order.pdf | customer_name | got None want Carlos Hernández |
| 10395_purchase_order.pdf | document_number | got None want 10395 |
| 10395_purchase_order.pdf | po_number | got None want 10395 |
| 10395_purchase_order.pdf | document_date | got None want 2016-12-26 |
| 10395_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10395_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10402_invoice.pdf | customer_name | got None want Roland Mendel |
| 10402_invoice.pdf | document_number | got None want 10402 |
| 10402_invoice.pdf | total | got None want 2713.50 |
| 10402_invoice.pdf | line_items_count | got 0 items want 2 |
| 10402_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10402_purchase_order.pdf | customer_name | got None want Roland Mendel |
| 10402_purchase_order.pdf | document_number | got None want 10402 |
| 10402_purchase_order.pdf | po_number | got None want 10402 |
| 10402_purchase_order.pdf | document_date | got None want 2017-01-02 |
| 10402_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10402_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10433_invoice.pdf | customer_name | got None want Isabel de Castro |
| 10433_invoice.pdf | document_number | got None want 10433 |
| 10433_invoice.pdf | total | got None want 851.20 |
| 10433_invoice.pdf | line_items_count | got 0 items want 1 |
| 10433_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10433_purchase_order.pdf | customer_name | got None want Isabel de Castro |
| 10433_purchase_order.pdf | document_number | got None want 10433 |
| 10433_purchase_order.pdf | po_number | got None want 10433 |
| 10433_purchase_order.pdf | document_date | got None want 2017-02-03 |
| 10433_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10433_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10467_invoice.pdf | customer_name | got None want Giovanni Rovelli |
| 10467_invoice.pdf | document_number | got None want 10467 |
| 10467_invoice.pdf | total | got None want 235.20 |
| 10467_invoice.pdf | line_items_count | got 0 items want 2 |
| 10467_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10467_purchase_order.pdf | customer_name | got None want Giovanni Rovelli |
| 10467_purchase_order.pdf | document_number | got None want 10467 |
| 10467_purchase_order.pdf | po_number | got None want 10467 |
| 10467_purchase_order.pdf | document_date | got None want 2017-03-06 |
| 10467_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10467_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10474_invoice.pdf | customer_name | got None want Guillermo Fernández |
| 10474_invoice.pdf | document_number | got None want 10474 |
| 10474_invoice.pdf | total | got None want 1249.10 |
| 10474_invoice.pdf | line_items_count | got 0 items want 4 |
| 10474_invoice.pdf | line_items_exact | got 0 items want 4 |
| 10474_purchase_order.pdf | customer_name | got None want Guillermo Fernández |
| 10474_purchase_order.pdf | document_number | got None want 10474 |
| 10474_purchase_order.pdf | po_number | got None want 10474 |
| 10474_purchase_order.pdf | document_date | got None want 2017-03-13 |
| 10474_purchase_order.pdf | line_items_count | got 0 items want 4 |
| 10474_purchase_order.pdf | line_items_exact | got 0 items want 4 |
| 10476_invoice.pdf | customer_name | got None want Carlos Hernández |
| 10476_invoice.pdf | document_number | got None want 10476 |
| 10476_invoice.pdf | total | got None want 182.40 |
| 10476_invoice.pdf | line_items_count | got 0 items want 2 |
| 10476_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10476_purchase_order.pdf | customer_name | got None want Carlos Hernández |
| 10476_purchase_order.pdf | document_number | got None want 10476 |
| 10476_purchase_order.pdf | po_number | got None want 10476 |
| 10476_purchase_order.pdf | document_date | got None want 2017-03-17 |
| 10476_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10476_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10494_invoice.pdf | customer_name | got None want Pedro Afonso |
| 10494_invoice.pdf | document_number | got None want 10494 |
| 10494_invoice.pdf | total | got None want 912.00 |
| 10494_invoice.pdf | line_items_count | got 0 items want 1 |
| 10494_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10494_purchase_order.pdf | customer_name | got None want Pedro Afonso |
| 10494_purchase_order.pdf | document_number | got None want 10494 |
| 10494_purchase_order.pdf | po_number | got None want 10494 |
| 10494_purchase_order.pdf | document_date | got None want 2017-04-02 |
| 10494_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10494_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10544_invoice.pdf | customer_name | got None want Fran Wilson |
| 10544_invoice.pdf | document_number | got None want 10544 |
| 10544_invoice.pdf | total | got None want 417.20 |
| 10544_invoice.pdf | line_items_count | got 0 items want 2 |
| 10544_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10544_purchase_order.pdf | customer_name | got None want Fran Wilson |
| 10544_purchase_order.pdf | document_number | got None want 10544 |
| 10544_purchase_order.pdf | po_number | got None want 10544 |
| 10544_purchase_order.pdf | document_date | got None want 2017-05-21 |
| 10544_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10544_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10563_invoice.pdf | customer_name | got None want Janete Limeira |
| 10563_invoice.pdf | document_number | got None want 10563 |
| 10563_invoice.pdf | total | got None want 965.00 |
| 10563_invoice.pdf | line_items_count | got 0 items want 2 |
| 10563_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10563_purchase_order.pdf | customer_name | got None want Janete Limeira |
| 10563_purchase_order.pdf | document_number | got None want 10563 |
| 10563_purchase_order.pdf | po_number | got None want 10563 |
| 10563_purchase_order.pdf | document_date | got None want 2017-06-10 |
| 10563_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10563_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10579_invoice.pdf | customer_name | got None want Jaime Yorres |
| 10579_invoice.pdf | document_number | got None want 10579 |
| 10579_invoice.pdf | total | got None want 317.75 |
| 10579_invoice.pdf | line_items_count | got 0 items want 2 |
| 10579_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10579_purchase_order.pdf | customer_name | got None want Jaime Yorres |
| 10579_purchase_order.pdf | document_number | got None want 10579 |
| 10579_purchase_order.pdf | po_number | got None want 10579 |
| 10579_purchase_order.pdf | document_date | got None want 2017-06-25 |
| 10579_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10579_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10622_invoice.pdf | customer_name | got None want Janete Limeira |
| 10622_invoice.pdf | document_number | got None want 10622 |
| 10622_invoice.pdf | total | got None want 605.00 |
| 10622_invoice.pdf | line_items_count | got 0 items want 2 |
| 10622_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10622_purchase_order.pdf | customer_name | got None want Janete Limeira |
| 10622_purchase_order.pdf | document_number | got None want 10622 |
| 10622_purchase_order.pdf | po_number | got None want 10622 |
| 10622_purchase_order.pdf | document_date | got None want 2017-08-06 |
| 10622_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10622_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10652_invoice.pdf | customer_name | got None want André Fonseca |
| 10652_invoice.pdf | document_number | got None want 10652 |
| 10652_invoice.pdf | total | got None want 331.78 |
| 10652_invoice.pdf | line_items_count | got 0 items want 2 |
| 10652_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10652_purchase_order.pdf | customer_name | got None want André Fonseca |
| 10652_purchase_order.pdf | document_number | got None want 10652 |
| 10652_purchase_order.pdf | po_number | got None want 10652 |
| 10652_purchase_order.pdf | document_date | got None want 2017-09-01 |
| 10652_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10652_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10654_invoice.pdf | customer_name | got None want Christina Berglund |
| 10654_invoice.pdf | document_number | got None want 10654 |
| 10654_invoice.pdf | total | got None want 668.70 |
| 10654_invoice.pdf | line_items_count | got 0 items want 3 |
| 10654_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10654_purchase_order.pdf | customer_name | got None want Christina Berglund |
| 10654_purchase_order.pdf | document_number | got None want 10654 |
| 10654_purchase_order.pdf | po_number | got None want 10654 |
| 10654_purchase_order.pdf | document_date | got None want 2017-09-02 |
| 10654_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10654_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10676_invoice.pdf | customer_name | got None want Miguel Angel Paolino |
| 10676_invoice.pdf | document_number | got None want 10676 |
| 10676_invoice.pdf | total | got None want 534.85 |
| 10676_invoice.pdf | line_items_count | got 0 items want 3 |
| 10676_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10676_purchase_order.pdf | customer_name | got None want Miguel Angel Paolino |
| 10676_purchase_order.pdf | document_number | got None want 10676 |
| 10676_purchase_order.pdf | po_number | got None want 10676 |
| 10676_purchase_order.pdf | document_date | got None want 2017-09-22 |
| 10676_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10676_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10677_invoice.pdf | customer_name | got None want Antonio Moreno |
| 10677_invoice.pdf | document_number | got None want 10677 |
| 10677_invoice.pdf | total | got None want 956.90 |
| 10677_invoice.pdf | line_items_count | got 0 items want 2 |
| 10677_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10677_purchase_order.pdf | customer_name | got None want Antonio Moreno |
| 10677_purchase_order.pdf | document_number | got None want 10677 |
| 10677_purchase_order.pdf | po_number | got None want 10677 |
| 10677_purchase_order.pdf | document_date | got None want 2017-09-22 |
| 10677_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10677_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10682_invoice.pdf | customer_name | got None want Antonio Moreno |
| 10682_invoice.pdf | document_number | got None want 10682 |
| 10682_invoice.pdf | total | got None want 375.50 |
| 10682_invoice.pdf | line_items_count | got 0 items want 3 |
| 10682_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10682_purchase_order.pdf | customer_name | got None want Antonio Moreno |
| 10682_purchase_order.pdf | document_number | got None want 10682 |
| 10682_purchase_order.pdf | po_number | got None want 10682 |
| 10682_purchase_order.pdf | document_date | got None want 2017-09-25 |
| 10682_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10682_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10692_invoice.pdf | customer_name | got None want Maria Anders |
| 10692_invoice.pdf | document_number | got None want 10692 |
| 10692_invoice.pdf | total | got None want 878.00 |
| 10692_invoice.pdf | line_items_count | got 0 items want 1 |
| 10692_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10692_purchase_order.pdf | customer_name | got None want Maria Anders |
| 10692_purchase_order.pdf | document_number | got None want 10692 |
| 10692_purchase_order.pdf | po_number | got None want 10692 |
| 10692_purchase_order.pdf | document_date | got None want 2017-10-03 |
| 10692_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10692_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10767_invoice.pdf | customer_name | got None want Pascale Cartrain |
| 10767_invoice.pdf | document_number | got None want 10767 |
| 10767_invoice.pdf | total | got None want 28.00 |
| 10767_invoice.pdf | line_items_count | got 2 items want 1 |
| 10767_invoice.pdf | line_items_exact | got 2 items want 1 |
| 10767_purchase_order.pdf | customer_name | got None want Pascale Cartrain |
| 10767_purchase_order.pdf | document_number | got None want 10767 |
| 10767_purchase_order.pdf | po_number | got None want 10767 |
| 10767_purchase_order.pdf | document_date | got None want 2017-12-05 |
| 10767_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10767_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10796_invoice.pdf | customer_name | got None want Carlos Hernández |
| 10796_invoice.pdf | document_number | got None want 10796 |
| 10796_invoice.pdf | total | got None want 2878.08 |
| 10796_invoice.pdf | line_items_count | got 0 items want 4 |
| 10796_invoice.pdf | line_items_exact | got 0 items want 4 |
| 10796_purchase_order.pdf | customer_name | got None want Carlos Hernández |
| 10796_purchase_order.pdf | document_number | got None want 10796 |
| 10796_purchase_order.pdf | po_number | got None want 10796 |
| 10796_purchase_order.pdf | document_date | got None want 2017-12-25 |
| 10796_purchase_order.pdf | line_items_count | got 0 items want 4 |
| 10796_purchase_order.pdf | line_items_exact | got 0 items want 4 |
| 10801_invoice.pdf | customer_name | got None want Martín Sommer |
| 10801_invoice.pdf | document_number | got None want 10801 |
| 10801_invoice.pdf | total | got None want 4035.80 |
| 10801_invoice.pdf | line_items_exact | got 2 items want 2 |
| 10801_purchase_order.pdf | customer_name | got None want Martín Sommer |
| 10801_purchase_order.pdf | document_number | got None want 10801 |
| 10801_purchase_order.pdf | po_number | got None want 10801 |
| 10801_purchase_order.pdf | document_date | got None want 2017-12-29 |
| 10801_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10801_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10812_invoice.pdf | customer_name | got None want Maurizio Moroni |
| 10812_invoice.pdf | document_number | got None want 10812 |
| 10812_invoice.pdf | total | got None want 1852.00 |
| 10812_invoice.pdf | line_items_count | got 0 items want 3 |
| 10812_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10812_purchase_order.pdf | customer_name | got None want Maurizio Moroni |
| 10812_purchase_order.pdf | document_number | got None want 10812 |
| 10812_purchase_order.pdf | po_number | got None want 10812 |
| 10812_purchase_order.pdf | document_date | got None want 2018-01-02 |
| 10812_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10812_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10818_invoice.pdf | customer_name | got None want Giovanni Rovelli |
| 10818_invoice.pdf | document_number | got None want 10818 |
| 10818_invoice.pdf | total | got None want 833.00 |
| 10818_invoice.pdf | line_items_count | got 0 items want 2 |
| 10818_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10818_purchase_order.pdf | customer_name | got None want Giovanni Rovelli |
| 10818_purchase_order.pdf | document_number | got None want 10818 |
| 10818_purchase_order.pdf | po_number | got None want 10818 |
| 10818_purchase_order.pdf | document_date | got None want 2018-01-07 |
| 10818_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10818_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10821_invoice.pdf | customer_name | got None want Art Braunschweiger |
| 10821_invoice.pdf | document_number | got None want 10821 |
| 10821_invoice.pdf | total | got None want 678.00 |
| 10821_invoice.pdf | line_items_count | got 0 items want 2 |
| 10821_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10821_purchase_order.pdf | customer_name | got None want Art Braunschweiger |
| 10821_purchase_order.pdf | document_number | got None want 10821 |
| 10821_purchase_order.pdf | po_number | got None want 10821 |
| 10821_purchase_order.pdf | document_date | got None want 2018-01-08 |
| 10821_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10821_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10827_invoice.pdf | customer_name | got None want Laurence Lebihan |
| 10827_invoice.pdf | document_number | got None want 10827 |
| 10827_invoice.pdf | total | got None want 843.00 |
| 10827_invoice.pdf | line_items_count | got 0 items want 2 |
| 10827_invoice.pdf | line_items_exact | got 0 items want 2 |
| 10827_purchase_order.pdf | customer_name | got None want Laurence Lebihan |
| 10827_purchase_order.pdf | document_number | got None want 10827 |
| 10827_purchase_order.pdf | po_number | got None want 10827 |
| 10827_purchase_order.pdf | document_date | got None want 2018-01-12 |
| 10827_purchase_order.pdf | line_items_count | got 0 items want 2 |
| 10827_purchase_order.pdf | line_items_exact | got 0 items want 2 |
| 10832_invoice.pdf | customer_name | got None want Annette Roulet |
| 10832_invoice.pdf | document_number | got None want 10832 |
| 10832_invoice.pdf | total | got None want 568.95 |
| 10832_invoice.pdf | line_items_count | got 0 items want 4 |
| 10832_invoice.pdf | line_items_exact | got 0 items want 4 |
| 10832_purchase_order.pdf | customer_name | got None want Annette Roulet |
| 10832_purchase_order.pdf | document_number | got None want 10832 |
| 10832_purchase_order.pdf | po_number | got None want 10832 |
| 10832_purchase_order.pdf | document_date | got None want 2018-01-14 |
| 10832_purchase_order.pdf | line_items_count | got 0 items want 4 |
| 10832_purchase_order.pdf | line_items_exact | got 0 items want 4 |
| 10838_invoice.pdf | customer_name | got None want Felipe Izquierdo |
| 10838_invoice.pdf | document_number | got None want 10838 |
| 10838_invoice.pdf | total | got None want 2584.50 |
| 10838_invoice.pdf | line_items_count | got 0 items want 3 |
| 10838_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10838_purchase_order.pdf | customer_name | got None want Felipe Izquierdo |
| 10838_purchase_order.pdf | document_number | got None want 10838 |
| 10838_purchase_order.pdf | po_number | got None want 10838 |
| 10838_purchase_order.pdf | document_date | got None want 2018-01-19 |
| 10838_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10838_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10843_invoice.pdf | customer_name | got None want Mary Saveley |
| 10843_invoice.pdf | document_number | got None want 10843 |
| 10843_invoice.pdf | total | got None want 212.00 |
| 10843_invoice.pdf | line_items_count | got 0 items want 1 |
| 10843_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10843_purchase_order.pdf | customer_name | got None want Mary Saveley |
| 10843_purchase_order.pdf | document_number | got None want 10843 |
| 10843_purchase_order.pdf | po_number | got None want 10843 |
| 10843_purchase_order.pdf | document_date | got None want 2018-01-21 |
| 10843_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10843_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10844_invoice.pdf | customer_name | got None want Georg Pipps |
| 10844_invoice.pdf | document_number | got None want 10844 |
| 10844_invoice.pdf | total | got None want 735.00 |
| 10844_invoice.pdf | line_items_count | got 0 items want 1 |
| 10844_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10844_purchase_order.pdf | customer_name | got None want Georg Pipps |
| 10844_purchase_order.pdf | document_number | got None want 10844 |
| 10844_purchase_order.pdf | po_number | got None want 10844 |
| 10844_purchase_order.pdf | document_date | got None want 2018-01-21 |
| 10844_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10844_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10847_invoice.pdf | customer_name | got None want Jose Pavarotti |
| 10847_invoice.pdf | document_number | got None want 10847 |
| 10847_invoice.pdf | total | got None want 6164.90 |
| 10847_invoice.pdf | line_items_count | got 0 items want 6 |
| 10847_invoice.pdf | line_items_exact | got 0 items want 6 |
| 10847_purchase_order.pdf | customer_name | got None want Jose Pavarotti |
| 10847_purchase_order.pdf | document_number | got None want 10847 |
| 10847_purchase_order.pdf | po_number | got None want 10847 |
| 10847_purchase_order.pdf | document_date | got None want 2018-01-22 |
| 10847_purchase_order.pdf | line_items_count | got 0 items want 6 |
| 10847_purchase_order.pdf | line_items_exact | got 0 items want 6 |
| 10890_invoice.pdf | customer_name | got None want Janine Labrune |
| 10890_invoice.pdf | document_number | got None want 10890 |
| 10890_invoice.pdf | total | got None want 860.10 |
| 10890_invoice.pdf | line_items_count | got 0 items want 3 |
| 10890_invoice.pdf | line_items_exact | got 0 items want 3 |
| 10890_purchase_order.pdf | customer_name | got None want Janine Labrune |
| 10890_purchase_order.pdf | document_number | got None want 10890 |
| 10890_purchase_order.pdf | po_number | got None want 10890 |
| 10890_purchase_order.pdf | document_date | got None want 2018-02-16 |
| 10890_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10890_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 10893_invoice.pdf | customer_name | got None want Philip Cramer |
| 10893_invoice.pdf | document_number | got None want 10893 |
| 10893_invoice.pdf | total | got None want 5502.11 |
| 10893_invoice.pdf | line_items_count | got 0 items want 5 |
| 10893_invoice.pdf | line_items_exact | got 0 items want 5 |
| 10893_purchase_order.pdf | customer_name | got None want Philip Cramer |
| 10893_purchase_order.pdf | document_number | got None want 10893 |
| 10893_purchase_order.pdf | po_number | got None want 10893 |
| 10893_purchase_order.pdf | document_date | got None want 2018-02-18 |
| 10893_purchase_order.pdf | line_items_count | got 0 items want 5 |
| 10893_purchase_order.pdf | line_items_exact | got 0 items want 5 |
| 10914_invoice.pdf | customer_name | got None want Lúcia Carvalho |
| 10914_invoice.pdf | document_number | got None want 10914 |
| 10914_invoice.pdf | total | got None want 537.50 |
| 10914_invoice.pdf | line_items_count | got 0 items want 1 |
| 10914_invoice.pdf | line_items_exact | got 0 items want 1 |
| 10914_purchase_order.pdf | customer_name | got None want Lúcia Carvalho |
| 10914_purchase_order.pdf | document_number | got None want 10914 |
| 10914_purchase_order.pdf | po_number | got None want 10914 |
| 10914_purchase_order.pdf | document_date | got None want 2018-02-27 |
| 10914_purchase_order.pdf | line_items_count | got 0 items want 1 |
| 10914_purchase_order.pdf | line_items_exact | got 0 items want 1 |
| 10946_invoice.pdf | customer_name | got None want Palle Ibsen |
| 10946_invoice.pdf | document_number | got None want 10946 |
| 10946_invoice.pdf | total | got None want 1407.50 |
| 10946_invoice.pdf | line_items_count | got 2 items want 3 |
| 10946_invoice.pdf | line_items_exact | got 2 items want 3 |
| 10946_purchase_order.pdf | customer_name | got None want Palle Ibsen |
| 10946_purchase_order.pdf | document_number | got None want 10946 |
| 10946_purchase_order.pdf | po_number | got None want 10946 |
| 10946_purchase_order.pdf | document_date | got None want 2018-03-12 |
| 10946_purchase_order.pdf | line_items_count | got 0 items want 3 |
| 10946_purchase_order.pdf | line_items_exact | got 0 items want 3 |
| 11077_invoice.pdf | customer_name | got None want Paula Wilson |
| 11077_invoice.pdf | document_number | got None want 11077 |
| 11077_invoice.pdf | total | got None want 1374.60 |
| 11077_invoice.pdf | line_items_count | got 0 items want 25 |
| 11077_invoice.pdf | line_items_exact | got 0 items want 25 |
| 11077_purchase_order.pdf | customer_name | got None want Paula Wilson |
| 11077_purchase_order.pdf | document_number | got None want 11077 |
| 11077_purchase_order.pdf | po_number | got None want 11077 |
| 11077_purchase_order.pdf | document_date | got None want 2018-05-06 |
| 11077_purchase_order.pdf | line_items_count | got 0 items want 25 |
| 11077_purchase_order.pdf | line_items_exact | got 0 items want 25 |
