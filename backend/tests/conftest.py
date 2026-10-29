import os
import tempfile

# Must be set before app modules import settings. CI overrides DATABASE_URL with a real Postgres.
_tmp = tempfile.mkdtemp()
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_tmp}/test.db")
os.environ["UPLOAD_DIR"] = f"{_tmp}/uploads"
os.environ["CELERY_EAGER"] = "true"
os.environ["JWT_SECRET"] = "test-secret-at-least-32-bytes-long!!"

import pytest  # noqa: E402

from app import extraction  # noqa: E402
from app.db import Base, engine  # noqa: E402
from eval.pdfgen import make_pdf  # noqa: E402

INVOICE_LINES = [
    "ACME Supplies Ltd",
    "INVOICE",
    "Supplier: ACME Supplies Ltd",
    "Invoice No: INV-1042",
    "Invoice Date: 2024-03-05",
    "Due Date: 2024-04-04",
    "Bill To: Globex Corp",
    "Description   Qty   Unit Price   Amount",
    "Widget A   10   $25.00   $250.00",
    "Gadget B   2   $100.00   $200.00",
    "Subtotal: $450.00",
    "Tax (10%): $45.00",
    "Total: $495.00",
]

GOOD_LLM = {
    "document_type": "invoice", "supplier_name": "ACME Supplies Ltd", "customer_name": "Globex Corp",
    "document_number": "INV-1042", "po_number": None, "document_date": "2024-03-05", "due_date": "2024-04-04",
    "currency": "USD", "subtotal": 450, "tax": 45, "total": 495,
    "line_items": [{"description": "Widget A", "quantity": 10, "unit_price": 25, "amount": 250},
                   {"description": "Gadget B", "quantity": 2, "unit_price": 100, "amount": 200}],
}


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def invoice_pdf() -> bytes:
    return make_pdf([INVOICE_LINES])


@pytest.fixture
def llm(monkeypatch):
    """Replace the network call; set .reply to a dict or an exception instance."""
    class Fake:
        reply = GOOD_LLM
        calls = 0

        def __call__(self, text):
            Fake.calls += 1
            if isinstance(self.reply, Exception):
                raise self.reply
            return dict(self.reply)

    fake = Fake()
    monkeypatch.setattr(extraction, "call_llm", fake)
    return fake
