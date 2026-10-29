# Architecture

## Components

```mermaid
flowchart LR
    U[Reviewer<br/>browser] -->|HTTPS| W[web<br/>nginx + React SPA]
    W -->|/api/*| A[api<br/>FastAPI]
    A -->|SQL| P[(PostgreSQL<br/>users, documents,<br/>fields, issues, status)]
    A -->|write PDF| F[(uploads volume<br/>content-addressed by SHA-256)]
    A -->|enqueue doc id| R[(Redis<br/>Celery broker)]
    R --> K[worker<br/>Celery]
    K -->|atomic claim / results| P
    K -->|read PDF| F
    K -->|chat/completions<br/>JSON mode| L[LLM endpoint<br/>Ollama / any OpenAI-compatible]
```

Five containers (`docker-compose.yml`): `db`, `redis`, `api`, `worker`, `web`. `api` and `worker` are the same
image with different commands. The LLM is deliberately outside the stack: it's an HTTP dependency selected by
`LLM_BASE_URL`, so the same code runs against local Ollama or a hosted endpoint.

## Processing pipeline (one Celery task per document)

```mermaid
flowchart TD
    S[claim row:<br/>UPDATE ... SET status='processing'<br/>WHERE status='queued' OR stale] -->|0 rows| X[exit: already handled]
    S -->|1 row| T[pdfplumber: PDF -> page texts]
    T -->|PDFError: not a PDF / corrupt /<br/>too many pages / no text layer| FAIL[status = failed]
    T --> C[group pages into chunks<br/>≤ LLM_MAX_CHARS]
    C --> M[LLM per chunk<br/>temperature 0, JSON mode]
    M -->|timeout / 429 / 5xx| RQ[status = queued<br/>Celery retry, exponential backoff]
    RQ -->|last attempt| RX[regex-only draft<br/>+ llm_unavailable warning]
    M -->|bad JSON / wrong shape| BO[drop chunk<br/>+ llm_bad_output warning]
    M --> G[merge chunks:<br/>first non-null scalar wins,<br/>line items concatenated]
    BO --> G
    G --> CO[coerce field-by-field<br/>into typed Fields<br/>unparseable -> null + warning]
    RX --> CO
    CO --> RG[regex gap-fill<br/>+ disagreement check]
    RG --> V[deterministic rules<br/>+ duplicate lookup in DB]
    V --> NR[status = needs_review]
```

Only one step calls a model. Everything after it is plain, unit-tested Python, so a given model output always
produces the same fields and the same issues.

## Document lifecycle

```mermaid
stateDiagram-v2
    [*] --> queued: upload (new SHA-256 for this user)
    queued --> processing: worker claims row
    processing --> queued: LLM unavailable (retry)
    processing --> needs_review: extracted
    processing --> failed: unreadable PDF / internal error
    failed --> queued: reprocess
    needs_review --> queued: reprocess (discards edits)
    needs_review --> needs_review: reviewer edits (re-validated)
    needs_review --> validated: approve (server re-checks: no errors)
    validated --> needs_review: reviewer edits again
    validated --> [*]: export CSV / XLSX
```

## Key design decisions

| Decision | Why | Trade-off / upgrade path |
|---|---|---|
| Fixed pipeline, no agent framework | Extraction is one well-defined transform. An agent loop adds latency, cost and non-determinism without adding capability here. | If a document type genuinely needs tool use (e.g. looking up a supplier master), add that one call explicitly. |
| LLM via raw OpenAI-compatible HTTP (`httpx`), not LangChain | The legacy prototype (`Legacy/`) pulled ~40 transitive packages to make one call. Direct HTTP gives explicit timeout and error classification (retryable vs not). | — |
| Idempotency via a conditional `UPDATE` on the row | Works across retries, redelivery after a worker crash, and double-clicked "Reprocess". The queue can deliver twice; the database decides once. | Stale `processing` rows (crashed worker) are reclaimable after `STALE_PROCESSING_S`. |
| Duplicate uploads blocked by `UNIQUE(owner_id, sha256)` | Database constraint, so concurrent uploads of the same file can't both win. | Per-user, so users can't probe whether someone else uploaded a file. |
| Separate `extracted` (immutable) and `fields` (current) JSON | Keeps the model's original output for auditing and lets you measure how much reviewers correct. | — |
| Money as `Decimal`, serialised as strings | Floats make `subtotal + tax == total` checks flaky. | — |
| Regex as gap-filler *and* cross-check | Fills fields the model leaves empty and flags when model and labelled text disagree on total / number. | Regex patterns are English, label-driven. |
| `create_all` instead of Alembic | One schema version so far. | Add Alembic before the first schema change on real data. |
| PDFs on a shared volume, not in Postgres | Keeps the DB small; files are content-addressed so the path is never user-controlled. | Swap `store_file`/`file_path` for S3 when there's more than one host. |

## Code map

```
backend/app/
  config.py      env-driven settings (pydantic-settings); JWT_SECRET is required
  db.py          SQLAlchemy models: User, Document; Status enum
  auth.py        scrypt password hashing, JWT issue/verify, current_user dependency
  fields.py      Fields/LineItem schema + lenient coercion of untrusted model output
  extraction.py  PDF -> text, chunking, LLM call, JSON parsing, regex fallback, merge
  rules.py       deterministic validation rules (pure functions)
  worker.py      Celery app, atomic claim, retry policy, file storage, DB-backed duplicate check
  main.py        FastAPI routes: auth, upload, list/detail, review, approve, reprocess, export
backend/tests/   pytest: unit (fields, rules, extraction) + API integration
backend/eval/    synthetic dataset generator, accuracy harness, results
frontend/src/    React + TypeScript: api.ts (typed client), App.tsx (login, list, review)
```
