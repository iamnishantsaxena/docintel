from datetime import date
from decimal import Decimal

import pytest

from app.fields import coerce, parse_money


@pytest.mark.parametrize("raw, expected", [
    ("$1,234.50", "1234.50"), ("1.234,50 EUR", "1234.50"), ("€12,5", "12.50"), ("(12.00)", "-12.00"),
    ("-3", "-3.00"), (7, "7.00"), (19.999, "20.00"), ("1,000", "1000.00"), (None, None), ("", None),
])
def test_parse_money(raw, expected):
    assert parse_money(raw) == (Decimal(expected) if expected else None)


@pytest.mark.parametrize("raw", ["abc", "N/A", True, "..."])
def test_parse_money_rejects_garbage(raw):
    with pytest.raises(ValueError):
        parse_money(raw)


def test_coerce_keeps_good_fields_and_flags_bad_ones():
    # The kinds of wrong output small models actually produce.
    fields, issues = coerce({
        "supplier_name": "  ACME  ", "document_number": 1042, "document_date": "March 5, 2024",
        "due_date": "next tuesday-ish", "total": "about five hundred", "subtotal": "$450.00",
        "currency": "dollars", "document_type": "Purchase Order", "customer_name": "null",
        "line_items": [{"description": "Widget", "quantity": "ten", "amount": "250"}, "garbage", {}],
        "unexpected_key": {"nested": True},
    })
    assert fields.supplier_name == "ACME"
    assert fields.document_number == "1042"
    assert fields.document_date == date(2024, 3, 5)
    assert fields.document_type == "purchase_order"
    assert fields.subtotal == Decimal("450.00")
    assert fields.due_date is None and fields.total is None and fields.currency is None
    assert fields.customer_name is None
    assert len(fields.line_items) == 1 and fields.line_items[0].quantity is None
    assert {i["field"] for i in issues} == {"due_date", "total", "currency", "line_items[0].quantity"}


@pytest.mark.parametrize("raw", [{}, {"line_items": "not a list"}, {"total": [1, 2]}, {"supplier_name": {"a": 1}}])
def test_coerce_never_raises_on_wrong_types(raw):
    fields, _ = coerce(raw)
    assert fields.line_items == [] or isinstance(fields.line_items, list)
