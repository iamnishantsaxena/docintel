"""The extracted-record shape, shared by the pipeline, the rules, the API and the export."""

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Literal

from dateutil import parser as dateparser
from pydantic import BaseModel, ConfigDict, Field, field_validator

DocType = Literal["invoice", "purchase_order", "other"]

MONEY_FIELDS = ("subtotal", "tax", "total")
DATE_FIELDS = ("document_date", "due_date")
TEXT_FIELDS = ("supplier_name", "customer_name", "document_number", "po_number", "currency")


class LineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str | None = Field(None, max_length=500)
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    amount: Decimal | None = None


class Fields(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_type: DocType | None = None
    supplier_name: str | None = Field(None, max_length=255)
    customer_name: str | None = Field(None, max_length=255)
    document_number: str | None = Field(None, max_length=100)
    po_number: str | None = Field(None, max_length=100)
    document_date: date | None = None
    due_date: date | None = None
    currency: str | None = Field(None, max_length=3)
    subtotal: Decimal | None = None
    tax: Decimal | None = None
    total: Decimal | None = None
    line_items: list[LineItem] = Field(default_factory=list, max_length=500)

    @field_validator("currency")
    @classmethod
    def _upper(cls, v: str | None) -> str | None:
        return v.upper() if v else v


def parse_money(value) -> Decimal | None:
    """'$1,234.50' / '1.234,50 EUR' / '(12.00)' / 7 -> Decimal. Raises ValueError on garbage."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError(f"not an amount: {value!r}")
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value)).quantize(Decimal("0.01"))
    s = str(value).strip()
    negative = s.startswith("(") and s.endswith(")") or s.startswith("-")
    s = re.sub(r"[^\d.,]", "", s)
    if not s:
        raise ValueError(f"not an amount: {value!r}")
    if "," in s and "." in s:
        # whichever separator comes last is the decimal point
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".") if re.search(r",\d{1,2}$", s) else s.replace(",", "")
    try:
        d = Decimal(s).quantize(Decimal("0.01"))
    except InvalidOperation:
        raise ValueError(f"not an amount: {value!r}") from None
    return -d if negative else d


def parse_date(value) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    # ponytail: dateutil's default month-first parsing; 03/04/2024 is ambiguous for non-US documents
    return dateparser.parse(str(value)).date()


def parse_quantity(value) -> Decimal | None:
    if value is None or value == "":
        return None
    d = Decimal(str(value).replace(",", "").strip())
    if not d.is_finite():
        raise ValueError(f"not a quantity: {value!r}")
    return d


def coerce(raw: dict) -> tuple[Fields, list[dict]]:
    """
    Turn untrusted model/regex output into Fields, field by field. A value that won't parse becomes None
    plus an issue, instead of failing the whole document.
    """
    out: dict = {}
    issues: list[dict] = []

    def bad(field: str, value) -> None:
        issues.append({"field": field, "code": "unparseable_value", "severity": "warning",
                       "message": f"Extracted value {str(value)[:60]!r} could not be parsed and was dropped"})

    for f in TEXT_FIELDS:
        v = raw.get(f)
        if isinstance(v, (str, int, float)) and str(v).strip() and str(v).strip().lower() not in ("null", "none", "n/a"):
            out[f] = str(v).strip()[:255]
    if out.get("currency") and not re.fullmatch(r"[A-Za-z]{3}", out["currency"]):
        bad("currency", out.pop("currency"))

    doc_type = str(raw.get("document_type") or "").lower().replace(" ", "_")
    if doc_type in ("invoice", "purchase_order", "other"):
        out["document_type"] = doc_type

    for f, parse in [(f, parse_money) for f in MONEY_FIELDS] + [(f, parse_date) for f in DATE_FIELDS]:
        try:
            out[f] = parse(raw.get(f))
        except (ValueError, TypeError, OverflowError):
            bad(f, raw.get(f))

    items = raw.get("line_items") if isinstance(raw.get("line_items"), list) else []
    out["line_items"] = []
    for i, item in enumerate(items[:500]):
        if not isinstance(item, dict):
            continue
        li = {"description": str(item["description"])[:500] if item.get("description") else None}
        for f, parse in (("quantity", parse_quantity), ("unit_price", parse_money), ("amount", parse_money)):
            try:
                li[f] = parse(item.get(f))
            except (ValueError, TypeError, ArithmeticError):
                bad(f"line_items[{i}].{f}", item.get(f))
        if any(v is not None for v in li.values()):
            out["line_items"].append(li)

    return Fields(**out), issues
