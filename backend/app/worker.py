"""
Background processing. Idempotency comes from an atomic status claim in Postgres, not from the queue:
a task that is delivered twice (retry, redelivery after a worker crash, double-click on Reprocess)
finds the row already claimed and exits.
"""

import logging
import time
from datetime import timedelta
from pathlib import Path

from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.orm import Session

from . import rules
from .config import settings
from .db import Document, SessionLocal, Status, utcnow
from .extraction import LLMUnavailable, PDFError, extract, pdf_to_pages
from .fields import Fields

log = logging.getLogger(__name__)

celery = Celery("docintel", broker=settings.redis_url)
celery.conf.update(
    task_always_eager=settings.celery_eager,
    task_acks_late=True,  # a worker that dies mid-task doesn't lose the message
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,  # LLM calls are slow; don't hoard tasks
    task_soft_time_limit=settings.task_soft_time_limit_s,
    task_time_limit=settings.task_soft_time_limit_s + 30,
)


class Retryable(Exception):
    pass


def file_path(sha256: str) -> Path:
    # Content-addressed: the path is derived from the hash, never from the user's filename.
    return Path(settings.upload_dir) / sha256[:2] / sha256


def store_file(sha256: str, data: bytes) -> None:
    path = file_path(sha256)
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def claim(db: Session, doc_id: int) -> Document | None:
    stale = utcnow() - timedelta(seconds=settings.stale_processing_s)
    res = db.execute(
        update(Document)
        .where(Document.id == doc_id,
               or_(Document.status == Status.queued,
                   and_(Document.status == Status.processing, Document.updated_at < stale)))
        .values(status=Status.processing, attempts=Document.attempts + 1, updated_at=utcnow())
    )
    db.commit()
    return db.get(Document, doc_id) if res.rowcount else None


def validate_document(db: Session, doc: Document, fields: Fields) -> list[dict]:
    """Pure rules + the one rule that needs the database: same supplier+number already on file."""
    issues = rules.validate(fields, doc.text)
    if fields.supplier_name and fields.document_number:
        dup = db.scalar(select(Document.id).where(
            Document.owner_id == doc.owner_id, Document.id != doc.id,
            func.lower(Document.fields["supplier_name"].as_string()) == fields.supplier_name.lower(),
            Document.fields["document_number"].as_string() == fields.document_number,
        ).limit(1))
        if dup:
            issues.append({"field": "document_number", "code": "possible_duplicate", "severity": "warning",
                           "message": f"Document #{dup} has the same supplier and number"})
    return issues


def run(doc_id: int, final_attempt: bool = False) -> str:
    with SessionLocal() as db:
        doc = claim(db, doc_id)
        if doc is None:
            return "skipped"
        started = time.monotonic()
        try:
            pages = pdf_to_pages(file_path(doc.sha256).read_bytes())
            doc.text = "\n\n".join(pages)
            doc.page_count = len(pages)
            # On the last attempt, stop waiting for the model and give the reviewer a regex-only draft.
            fields_json, issues, meta = extract(pages, use_llm=False if final_attempt else None)
            if final_attempt and settings.llm_enabled:
                issues.append({"field": None, "code": "llm_unavailable", "severity": "warning",
                               "message": "Model unavailable after retries; fields come from pattern matching only"})
        except PDFError as e:
            doc.status, doc.error = Status.failed, str(e)
            db.commit()
            return "failed"
        except (LLMUnavailable, SoftTimeLimitExceeded) as e:
            doc.status, doc.error = Status.queued, f"Retrying: {e}"
            db.commit()
            raise Retryable(str(e)) from e
        except Exception:
            log.exception("unexpected failure processing document %s", doc_id)
            doc.status, doc.error = Status.failed, "Internal error during processing"
            db.commit()
            return "failed"

        fields = Fields(**fields_json)
        doc.extracted = fields_json
        doc.fields = fields_json
        doc.issues = issues + validate_document(db, doc, fields)
        doc.meta = {**meta, "processing_ms": round((time.monotonic() - started) * 1000)}
        doc.status, doc.error = Status.needs_review, None
        db.commit()
        return "done"


@celery.task(bind=True, max_retries=settings.task_max_retries, name="process_document")
def process_document(self, doc_id: int) -> str:
    try:
        return run(doc_id, final_attempt=self.request.retries >= self.max_retries)
    except Retryable as e:
        raise self.retry(exc=e, countdown=min(10 * 2 ** self.request.retries, 300)) from e


def enqueue(doc_id: int) -> bool:
    try:
        process_document.delay(doc_id)
        return True
    except Exception:  # broker down: the row stays 'queued' and can be re-enqueued via /reprocess
        log.exception("could not enqueue document %s", doc_id)
        return False
