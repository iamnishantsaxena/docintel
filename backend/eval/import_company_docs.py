"""
Build a third-party eval set from the "Company Documents" PDFs (Northwind-based, one template per type).

    python -m eval.import_company_docs --src ../dataset/CompanyDocuments --n 50

Samples N order IDs (seeded) and writes each order's invoice and purchase order with ground-truth JSON to
eval/dataset/company/. Truth is parsed from the PDF text with template regexes and cross-checked (invoice
items == PO items for the same order, Σ qty × price == printed total), so it is exact for this template but
**not manually verified** until someone ticks the files in VERIFY.md against the PDFs.

Fields these documents don't print (supplier, tax, currency, due date, subtotal; PO number on invoices) are null in the
truth: a model that fills them in is wrong. Line amount = qty × unit price (implied, never printed).
"""

import argparse
import json
import random
import re
import shutil
from decimal import Decimal
from pathlib import Path

from app.extraction import pdf_to_pages
from app.fields import Fields

OUT = Path(__file__).parent / "dataset" / "company"
ITEM = re.compile(r"^\d+ (.+) (\d+) (\d+(?:\.\d+)?)\s*$", re.M)  # "11 Queso Cabrales 12 14.0"


def text(pdf: Path) -> str:
    return "\n".join(pdf_to_pages(pdf.read_bytes()))


def items(t: str) -> list[dict]:
    return [{"description": d.strip(), "quantity": q, "unit_price": p, "amount": str(Decimal(q) * Decimal(p))}
            for d, q, p in ITEM.findall(t)]


def parse_invoice(t: str) -> dict:
    g = lambda label: re.search(rf"^{label}: (.+?)\s*$", t, re.M).group(1)  # noqa: E731
    return {"document_type": "invoice", "document_number": g("Order ID"), "customer_name": g("Contact Name"),
            # Some PDFs print float artefacts ("TotalPrice 268.79999999999995"); truth is the amount in cents.
            "document_date": g("Order Date"),
            "total": str(Decimal(re.search(r"^TotalPrice ([\d.]+)", t, re.M).group(1)).quantize(Decimal("0.01"))),
            "line_items": items(t)}


def parse_po(t: str) -> dict:
    num, day, name = re.search(r"^(\d+) (\d{4}-\d{2}-\d{2}) (.+?)\s*$", t, re.M).groups()
    # A PO's own number is also its po_number — same convention as the synthetic set and the prompt.
    return {"document_type": "purchase_order", "document_number": num, "po_number": num, "customer_name": name,
            "document_date": day, "line_items": items(t)}


def key(f: Fields) -> list:
    return [(li.description, li.quantity, li.unit_price) for li in f.line_items]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../dataset/CompanyDocuments")
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    src = Path(args.src)

    ids = sorted(re.search(r"\d+", p.name).group() for p in (src / "invoices").glob("invoice_*.pdf"))
    picked = sorted({"11077", *random.Random(args.seed).sample(ids, args.n - 1)})  # 11077: the 2-page one
    OUT.mkdir(parents=True, exist_ok=True)
    for oid in picked:
        inv_pdf, po_pdf = src / "invoices" / f"invoice_{oid}.pdf", src / "PurchaseOrders" / f"purchase_orders_{oid}.pdf"
        inv, po = Fields(**parse_invoice(text(inv_pdf))), Fields(**parse_po(text(po_pdf)))
        # Two independent layouts of the same order must agree, and the lines must add up to the printed total.
        assert inv.line_items and key(inv) == key(po), f"{oid}: invoice and PO line items differ"
        assert sum(li.amount for li in inv.line_items) == inv.total, f"{oid}: lines don't sum to TotalPrice"
        assert (inv.document_number, inv.document_date) == (po.document_number, po.document_date), oid
        for f, pdf, kind in ((inv, inv_pdf, "invoice"), (po, po_pdf, "purchase_order")):
            shutil.copyfile(pdf, OUT / f"{oid}_{kind}.pdf")
            (OUT / f"{oid}_{kind}.json").write_text(
                json.dumps(f.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n")

    files = sorted(p.stem for p in OUT.glob("*.pdf"))
    (OUT / "VERIFY.md").write_text(
        "# Manual verification\n\nOpen each PDF next to its JSON and tick it only if every non-null value matches"
        " what is printed and every null field is genuinely absent.\n\n"
        + "".join(f"- [ ] {s}\n" for s in files[:30]))
    print(f"{len(picked)} orders → {len(files)} documents in {OUT} (cross-checks passed)")


if __name__ == "__main__":
    main()
