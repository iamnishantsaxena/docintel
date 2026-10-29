"""
Deterministic validation. Pure functions over Fields (+ source text), no model calls, no I/O.
Severity 'error' blocks approval; 'warning' is shown to the reviewer but doesn't block.
"""

import re
from datetime import date, timedelta
from decimal import Decimal

from .fields import Fields

TOLERANCE = Decimal("0.02")  # rounding slack per comparison
REQUIRED = ("supplier_name", "document_number", "document_date", "total")
ISO_CURRENCIES = {"USD", "EUR", "GBP", "INR", "CAD", "AUD", "JPY", "CHF", "CNY", "SGD", "NZD", "SEK", "NOK",
                  "DKK", "ZAR", "AED", "MXN", "BRL", "HKD"}


def _issue(field, code, severity, message):
    return {"field": field, "code": code, "severity": severity, "message": message}


def _close(a: Decimal, b: Decimal) -> bool:
    return abs(a - b) <= TOLERANCE


def _in_text(value: str, text: str) -> bool:
    norm = lambda s: re.sub(r"[\s,]", "", s).lower()  # noqa: E731
    return norm(value) in norm(text)


def validate(f: Fields, text: str | None = None, today: date | None = None) -> list[dict]:
    today = today or date.today()
    issues = []

    for name in REQUIRED:
        if getattr(f, name) in (None, ""):
            issues.append(_issue(name, "missing_required", "error", f"{name.replace('_', ' ').capitalize()} is required"))

    for name in ("subtotal", "tax", "total"):
        v = getattr(f, name)
        if v is not None and v < 0:
            issues.append(_issue(name, "negative_amount", "error", f"{name.capitalize()} is negative ({v})"))

    if f.subtotal is not None and f.tax is not None and f.total is not None:
        expected = f.subtotal + f.tax
        if not _close(expected, f.total):
            issues.append(_issue("total", "total_mismatch", "error",
                                 f"Subtotal {f.subtotal} + tax {f.tax} = {expected}, but total is {f.total}"))

    if f.subtotal and f.tax is not None and f.subtotal > 0:
        rate = f.tax / f.subtotal
        if rate > Decimal("0.30"):
            issues.append(_issue("tax", "tax_rate_implausible", "warning", f"Tax is {rate:.0%} of subtotal"))

    amounts = [li.amount for li in f.line_items]
    if f.line_items and all(a is not None for a in amounts):
        line_sum = sum(amounts, Decimal(0))
        target_name, target = ("subtotal", f.subtotal) if f.subtotal is not None else ("total", f.total)
        # Only compare against total when there's no tax to account for.
        if target is not None and (target_name == "subtotal" or not f.tax) and not _close(line_sum, target):
            issues.append(_issue(target_name, "line_items_sum_mismatch", "error",
                                 f"Line items sum to {line_sum}, but {target_name} is {target}"))

    for i, li in enumerate(f.line_items):
        if li.quantity is not None and li.unit_price is not None and li.amount is not None:
            if not _close(li.quantity * li.unit_price, li.amount):
                issues.append(_issue(f"line_items[{i}].amount", "line_amount_mismatch", "error",
                                     f"{li.quantity} x {li.unit_price} = {li.quantity * li.unit_price}, but amount is {li.amount}"))
        if li.quantity is not None and li.quantity <= 0:
            issues.append(_issue(f"line_items[{i}].quantity", "non_positive_quantity", "warning",
                                 f"Quantity is {li.quantity}"))

    if f.document_date and f.document_date > today + timedelta(days=1):
        issues.append(_issue("document_date", "date_in_future", "error", f"Document date {f.document_date} is in the future"))
    if f.document_date and f.document_date.year < 2000:
        issues.append(_issue("document_date", "date_implausible", "warning", f"Document date {f.document_date} is before 2000"))
    if f.document_date and f.due_date and f.due_date < f.document_date:
        issues.append(_issue("due_date", "due_before_issue", "error",
                             f"Due date {f.due_date} is before document date {f.document_date}"))

    if f.currency and f.currency not in ISO_CURRENCIES:
        issues.append(_issue("currency", "unknown_currency", "warning", f"Unrecognised currency code {f.currency}"))

    # Hallucination guard: identifiers the model returns must actually be printed in the document.
    if text:
        for name in ("document_number", "po_number"):
            v = getattr(f, name)
            if v and not _in_text(v, text):
                issues.append(_issue(name, "not_in_source", "warning", f"{v!r} does not appear in the document text"))

    return issues


def has_errors(issues: list[dict]) -> bool:
    return any(i["severity"] == "error" for i in issues)
