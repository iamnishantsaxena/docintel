# Document Intelligence Platform — technical write-up

## Problem

Accounts-payable teams receive invoices and purchase orders as PDFs in many layouts. Someone has to retype
supplier, number, dates, tax, total and line items into a system, and check that the numbers add up. The goal
is to do the typing automatically, do the arithmetic checking deterministically, and leave a human to confirm.

## Approach

**One model call, then deterministic Python.** Each document goes through a fixed pipeline: PDF text →
LLM extraction (JSON mode, temperature 0) → field-by-field coercion into a typed schema → regex gap-fill and
cross-check → rule-based validation → human review. The model is used only for the step that actually needs
language understanding (reading an arbitrary layout). Everything that can be checked — arithmetic, date logic,
whether an invoice number is really printed in the document, duplicates — is checked by code that is unit
tested and always gives the same answer.

No agent framework: extraction is a single transformation with a known output schema, so a tool-calling loop
would only add latency and non-determinism. The legacy prototype used LangChain for one `invoke()`; this version replaces it with a direct
HTTP call to any OpenAI-compatible endpoint, which also made timeouts and error classification explicit.

**Human in the loop by design.** Every extraction lands in `needs_review`. Issues are shown next to the fields
they concern, values show whether they came from the model, the regex fallback, or a reviewer edit, and
approval is refused server-side while any error-severity issue remains. Only approved records are exported.

## Reliability

| Concern | Handling |
|---|---|
| Slow LLM calls | Celery worker (Redis broker); API returns 202 immediately; UI polls only while something is in flight |
| Duplicate uploads | `UNIQUE(owner_id, sha256)`; re-upload returns the existing document |
| Duplicate task execution | Atomic `UPDATE … WHERE status='queued'` claim; second delivery is a no-op |
| Worker crash mid-task | `acks_late` + `reject_on_worker_lost`; stale `processing` rows become claimable again |
| LLM timeout / 429 / 5xx | Row goes back to `queued`; Celery retries with exponential backoff (10 s → 300 s cap) |
| LLM down for good | Last attempt produces a regex-only draft with an `llm_unavailable` warning instead of failing |
| LLM 4xx (bad model name, etc.) | Not retried; regex fallback + `llm_bad_output` warning |
| Garbage model output | Bad JSON → that chunk falls back; bad values → nulled individually with a warning |
| Malformed PDFs | Magic-byte check, page limit, parser exceptions mapped to a clear `failed` status |
| Runaway tasks | Celery soft (300 s) / hard time limits |
| Broker down at upload | Document stays `queued` with a message; "Re-run extraction" re-enqueues |

## Security

- **AuthN:** email + password (scrypt, per-user salt, constant-time compare — stdlib, no extra dependency),
  HS256 JWT with expiry. `JWT_SECRET` has no default and must be ≥ 32 chars or the app won't start.
- **AuthZ:** every document route goes through one `owned_document` dependency; other users' documents return
  404. Duplicate detection is per user, so it can't be used to probe other accounts.
- **Uploads:** content checked by magic bytes, not filename or Content-Type; size capped while reading and at
  nginx; files stored under their SHA-256 (the user's filename is display-only, never a path); page limit
  guards against decompression-style abuse; PDF served back with `nosniff`.
- **Input validation:** Pydantic models with `extra="forbid"`, length limits, typed decimals/dates on every
  write endpoint.
- **Output:** CSV/XLSX cells starting with `= + - @` are prefixed with `'` (spreadsheet formula injection);
  nginx sets CSP, `X-Frame-Options`, `nosniff`.
- **LLM:** the prompt treats the document as data; the model's output can't trigger actions — it is coerced to
  a fixed schema and re-validated.

Not done: rate limiting on login, refresh tokens / revocation, roles beyond "owner", malware scanning,
encryption at rest beyond what the volume provides.

## Testing

`pytest` — 78 tests, ~2 s, no network or model needed (the LLM call is faked at the function boundary):

- **Unit:** money/date parsing, coercion of wrong-typed model output, every validation rule, JSON extraction
  from chatty/fenced/truncated replies, HTTP error classification (timeouts, 429, 5xx, 4xx, wrong shape).
- **Malformed documents:** empty, non-PDF bytes, corrupt and truncated PDFs, text-less PDFs, page limit.
- **Integration (FastAPI TestClient + DB + eager Celery):** register/login, cross-user isolation on every
  route, upload validation and path-traversal filenames, full upload → review → approve → export flow,
  approval blocked by errors, duplicate upload, duplicate-invoice warning, task idempotency, LLM outage →
  requeue → regex-only degrade, Celery retry then success, reprocess.

The CI workflow (`.github/workflows/ci.yml`) is set up to run the same suite against **PostgreSQL 16** (SQLite locally), lints with ruff, type-checks and builds the
frontend, runs the regex-only eval, then builds the Docker images and boots the full compose stack. (It hasn't run on GitHub yet; the suite has only been run locally against SQLite.)

## Measured results

See [EVALUATION.md](EVALUATION.md). On 30 synthetic PDFs, MacBook Air M2 8 GB, local Ollama (2026-10-29):

| | Field accuracy | Median s/doc |
|---|---|---|
| regex only | 86.7 % | 0.01 |
| qwen2.5:1.5b | 96.9 % | 10.1 |
| qwen2.5:3b | 96.3 % (1 timeout) | 15.0 |
| llama3.2:3b | 95.1 % | 11.6 |
| llama3.2:1b | 85.1 % | 5.3 |

The model's value is mostly in fields regex can't find (supplier name: 33 % → 97–100 %). The top three are
separated by a handful of field checks from one run each, so they aren't meaningfully ranked. Line items are
the weakest field for every model (47–77 % exactly right). The synthetic set is a regression benchmark; a
hand-verified real sample is the next step before quoting accuracy.

## Known limitations

No OCR (scanned PDFs fail clearly). Month-first date parsing silently swaps UK dates. Regex fallback is
English, label-driven. Export is CSV/XLSX only; no ERP integration.
Single-host file storage. No database migrations yet (`create_all`).

## What I'd do next

1. Hand-label 30–50 real invoices and measure the LLM configuration on them (and on the synthetic set).
2. Locale-aware date parsing driven by currency/country, with a warning when a date is ambiguous.
3. OCR path (Tesseract/`ocrmypdf`) for image-only PDFs, gated behind the same pipeline.
4. Track reviewer corrections (`extracted` vs `fields`) as a live accuracy metric.
5. Alembic migrations; S3-compatible storage for multi-host deploys.
