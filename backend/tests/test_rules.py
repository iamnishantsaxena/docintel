from datetime import date
from decimal import Decimal as D

from app.fields import Fields, LineItem
from app.rules import has_errors, validate

TODAY = date(2024, 6, 1)


def good(**overrides) -> Fields:
    base = dict(supplier_name="ACME", document_number="INV-1", document_date=date(2024, 3, 5),
                due_date=date(2024, 4, 4), currency="USD", subtotal=D("450"), tax=D("45"), total=D("495"),
                line_items=[LineItem(description="A", quantity=D(10), unit_price=D(25), amount=D(250)),
                            LineItem(description="B", quantity=D(2), unit_price=D(100), amount=D(200))])
    return Fields(**{**base, **overrides})


def codes(f, text=None):
    return {i["code"] for i in validate(f, text, TODAY)}


def test_clean_invoice_has_no_issues():
    assert validate(good(), "INV-1", TODAY) == []


def test_missing_required():
    issues = validate(Fields(), None, TODAY)
    assert {i["field"] for i in issues} == {"supplier_name", "document_number", "document_date", "total"}
    assert has_errors(issues)


def test_total_mismatch():
    assert "total_mismatch" in codes(good(total=D("500")))


def test_rounding_tolerance():
    assert "total_mismatch" not in codes(good(total=D("495.01")))


def test_line_items_sum_mismatch():
    assert "line_items_sum_mismatch" in codes(good(subtotal=D("460"), total=D("505")))


def test_line_sum_compared_to_total_when_no_subtotal_and_no_tax():
    assert "line_items_sum_mismatch" in codes(good(subtotal=None, tax=None, total=D("999")))
    assert "line_items_sum_mismatch" not in codes(good(subtotal=None, tax=None, total=D("450")))


def test_line_amount_mismatch():
    f = good(line_items=[LineItem(description="A", quantity=D(3), unit_price=D(10), amount=D(31))],
             subtotal=D(31), tax=D(0), total=D(31))
    assert codes(f) == {"line_amount_mismatch"}


def test_dates():
    assert "date_in_future" in codes(good(document_date=date(2030, 1, 1), due_date=None))
    assert "due_before_issue" in codes(good(due_date=date(2024, 1, 1)))


def test_negative_and_implausible_tax():
    assert "negative_amount" in codes(good(tax=D("-1"), total=D("449")))
    assert "tax_rate_implausible" in codes(good(tax=D("200"), total=D("650")))


def test_unknown_currency_is_warning():
    issues = validate(good(currency="XYZ"), None, TODAY)
    assert [i["severity"] for i in issues] == ["warning"]


def test_hallucinated_identifier_flagged():
    assert "not_in_source" in codes(good(document_number="INV-9999"), "Invoice No: INV-1")
    assert "not_in_source" not in codes(good(document_number="INV 1"), "Invoice No: INV-1".replace("-", " "))
