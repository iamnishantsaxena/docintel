from datetime import datetime, timezone
from enum import StrEnum

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

JSONType = JSON().with_variant(JSONB(), "postgresql")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Status(StrEnum):
    queued = "queued"
    processing = "processing"
    needs_review = "needs_review"
    validated = "validated"
    failed = "failed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Document(Base):
    __tablename__ = "documents"
    # Same bytes uploaded twice by the same user = same document; enforced by the DB, not app code.
    __table_args__ = (UniqueConstraint("owner_id", "sha256", name="uq_document_owner_sha256"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    filename: Mapped[str] = mapped_column(String(255))  # display only; never used as a path
    sha256: Mapped[str] = mapped_column(String(64))
    size_bytes: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default=Status.queued, index=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text)
    page_count: Mapped[int | None] = mapped_column(Integer)
    text: Mapped[str | None] = mapped_column(Text)  # extracted PDF text, kept for review + re-validation
    extracted: Mapped[dict | None] = mapped_column(JSONType)  # pipeline output, never edited
    fields: Mapped[dict | None] = mapped_column(JSONType)  # current values incl. reviewer corrections
    issues: Mapped[list | None] = mapped_column(JSONType)
    meta: Mapped[dict | None] = mapped_column(JSONType)  # model, llm_used, timings
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


def init_db() -> None:
    # ponytail: create_all instead of Alembic; add migrations once the schema changes under real data
    Base.metadata.create_all(engine)
