# API

Interactive docs (Swagger UI) are served by the running API at **`/api/docs`**; the full OpenAPI 3 spec is
checked in at [`openapi.json`](openapi.json) (regenerate with the command at the bottom).

All endpoints except `register`, `login` and `health` require `Authorization: Bearer <token>`. A document that
belongs to another user returns **404**, not 403, so ids can't be probed.

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/auth/register` | `{email, password}` (password ≥ 8 chars) → `{access_token}` |
| `POST` | `/api/auth/login` | OAuth2 form (`username`, `password`) → `{access_token}` |
| `GET` | `/api/auth/me` | Current user |
| `POST` | `/api/documents` | Multipart `files` (1–20 PDFs, ≤ 10 MB each) → per-file result; **202** |
| `GET` | `/api/documents?status=&limit=&offset=` | List own documents, newest first |
| `GET` | `/api/documents/{id}` | Detail: `fields`, `extracted`, `issues`, `meta`, status |
| `GET` | `/api/documents/{id}/file` | The original PDF |
| `PUT` | `/api/documents/{id}/fields` | Replace fields with reviewer corrections; re-runs validation |
| `POST` | `/api/documents/{id}/approve` | → `validated`. **422** with `issues` if any error-severity issue remains |
| `POST` | `/api/documents/{id}/reprocess` | Re-queue a `failed`/`queued`/`needs_review` document |
| `DELETE` | `/api/documents/{id}` | Delete the record |
| `GET` | `/api/export?format=csv\|xlsx` | Validated documents. XLSX has `documents` and `line_items` sheets |
| `GET` | `/api/health` | Liveness |

## Examples

```bash
TOKEN=$(curl -s -X POST localhost:8080/api/auth/register -H 'Content-Type: application/json' \
  -d '{"email":"me@example.com","password":"a-long-password"}' | jq -r .access_token)

curl -s -X POST localhost:8080/api/documents -H "Authorization: Bearer $TOKEN" \
  -F files=@invoice1.pdf -F files=@invoice2.pdf
# [{"id":1,"filename":"invoice1.pdf","status":"queued","duplicate":false,"error":null}, ...]
# Uploading the same bytes again returns the existing id with "duplicate": true.
# Rejected files come back with "id": null and an "error" ("Only PDF files are accepted", ...).

curl -s localhost:8080/api/documents/1 -H "Authorization: Bearer $TOKEN"
```

`GET /api/documents/{id}` (abridged, illustrative values — not a measured run):

```json
{
  "id": 1, "filename": "invoice1.pdf", "status": "needs_review", "page_count": 1, "attempts": 1,
  "fields": {
    "document_type": "invoice", "supplier_name": "ACME Supplies Ltd", "customer_name": "Globex Corp",
    "document_number": "INV-1042", "po_number": null, "document_date": "2024-03-05", "due_date": "2024-04-04",
    "currency": "USD", "subtotal": "450.00", "tax": "45.00", "total": "500.00",
    "line_items": [{"description": "Widget A", "quantity": "10", "unit_price": "25.00", "amount": "250.00"}]
  },
  "issues": [
    {"field": "total", "code": "total_mismatch", "severity": "error",
     "message": "Subtotal 450.00 + tax 45.00 = 495.00, but total is 500.00"}
  ],
  "meta": {"model": "qwen2.5:1.5b", "llm_used": true, "chunks": 1, "processing_ms": 4210,
           "sources": {"total": "llm", "supplier_name": "regex"}}
}
```

Money values are decimal **strings** to avoid float rounding. Dates are ISO `YYYY-MM-DD`.

## Issue codes

| Code | Severity | Meaning |
|---|---|---|
| `missing_required` | error | supplier, number, date or total is empty |
| `total_mismatch` | error | subtotal + tax ≠ total (±0.02) |
| `line_items_sum_mismatch` | error | Σ line amounts ≠ subtotal (or total when no subtotal/tax) |
| `line_amount_mismatch` | error | quantity × unit price ≠ line amount |
| `negative_amount` | error | subtotal/tax/total < 0 |
| `date_in_future` | error | document date after tomorrow |
| `due_before_issue` | error | due date before document date |
| `tax_rate_implausible` | warning | tax > 30 % of subtotal |
| `date_implausible` | warning | document date before 2000 |
| `unknown_currency` | warning | not in the supported ISO list |
| `non_positive_quantity` | warning | line quantity ≤ 0 |
| `not_in_source` | warning | document/PO number not found in the PDF text (hallucination guard) |
| `possible_duplicate` | warning | another of your documents has the same supplier + number |
| `llm_regex_disagree` | warning | model and labelled text give different total / number |
| `llm_bad_output` | warning | model reply wasn't usable JSON; pattern matching used for that chunk |
| `llm_unavailable` | warning | model unreachable after all retries; regex-only draft |
| `unparseable_value` | warning | a model value couldn't be parsed (e.g. `"about 500"`) and was dropped |

## Status codes

`401` bad/expired token · `404` not found or not yours · `409` wrong state for the action (e.g. editing a
document still processing) · `413` too many files · `422` validation failure (bad input, or approve with
errors) · `503` queue unavailable on reprocess.

Regenerate the spec:

```bash
cd backend && JWT_SECRET=$(openssl rand -hex 32) DATABASE_URL=sqlite:// \
  .venv/bin/python -c "import json; from app.main import app; json.dump(app.openapi(), open('../docs/openapi.json','w'), indent=1)"
```
