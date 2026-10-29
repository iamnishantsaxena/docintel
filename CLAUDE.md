# CLAUDE.md

Guidance for Claude Code in this repo. `Legacy/` holds the original Streamlit prototype (V1), kept for reference
while deciding whether to delete it — don't edit it, and ignore it unless asked.

## What this is

Document intelligence platform: upload invoice/PO PDFs → LLM extraction → deterministic validation → human
review in a React UI → CSV/XLSX export. FastAPI + PostgreSQL + Celery/Redis backend in `backend/`, Vite React
TS frontend in `frontend/`. Human-facing docs live in `README.md` and `docs/`; keep them in sync.

## Commands

```bash
cd backend
.venv/bin/pytest -q                      # fast, no network; LLM faked via the `llm` fixture
.venv/bin/ruff check app tests eval      # line length 120 (ruff.toml)
.venv/bin/python -m eval.run_eval --no-llm   # needs JWT_SECRET env (≥32 chars) like any app import
cd ../frontend && npm run build          # tsc --noEmit + vite build
```

Dev servers: `.claude/launch.json` at the repo root (`api-dev` = SQLite + `CELERY_EAGER` + `LLM_ENABLED=false`,
`web-dev` = Vite on 5173 proxying `/api`).

## Architecture (see docs/ARCHITECTURE.md)

- `app/extraction.py` — the only place that calls the model (`call_llm`, OpenAI-compatible HTTP via httpx, no
  LangChain). Raises `LLMUnavailable` (retryable) vs `LLMBadOutput` (fall back). `extract()` returns
  `(fields_json, issues, meta)`.
- `app/fields.py` — `Fields`/`LineItem` schema + `coerce()`: untrusted dict → typed fields, bad values become
  null + `unparseable_value` issue. Money is `Decimal`, stored in JSON as strings.
- `app/rules.py` — pure validation rules; `error` blocks approval, `warning` doesn't. Add new rules here with a
  test in `tests/test_rules.py`, and add the code to the table in `docs/API.md`.
- `app/worker.py` — Celery task; idempotency via atomic `claim()` UPDATE, not the queue. `validate_document()`
  = rules + DB duplicate check, used by worker and the PUT/approve routes.
- `app/main.py` — all routes; every per-document route depends on `owned_document` (404 for others' docs).
- Schema changes: there's no Alembic yet (`init_db` = `create_all`); add migrations before changing columns on
  real data.

## Rules of thumb

- Keep it a fixed pipeline: one model call per chunk, everything else deterministic. Don't add agent loops.
- Never report accuracy/perf numbers that weren't produced by `eval/run_eval.py`; state model, hardware, date.
- Tests must not need a model or network — fake `extraction.call_llm` (see `tests/conftest.py`).
