"""
Generate the synthetic eval set: PDFs + ground-truth JSON, deterministic (seeded).

Ground truth is exact by construction because the generator writes both the PDF and the JSON from the same
values. That makes it a *synthetic* benchmark, not a manually verified real-world one; see eval/README.md.
"""

import json
import random
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from eval.pdfgen import make_pdf

OUT = Path(__file__).parent / "dataset" / "synthetic"
SUPPLIERS = ["ACME Supplies Ltd", "Northwind Traders", "Blue Harbor Logistics GmbH", "Initech Office Solutions",
             "Sunrise Packaging Co.", "Kestrel Industrial Parts", "Orbital Print & Design", "Maple Leaf Hardware Inc."]
CUSTOMERS = ["Globex Corp", "Umbrella Retail", "Stark Manufacturing", "Wayne Hospitality Group", "Hooli Labs"]
PRODUCTS = ["Ergonomic Office Chair", "Standing Desk", "Monitor Arm", "LED Desk Lamp", "Cable Kit", "Toner Cartridge",
            "Printer Paper A4 (box)", "Steel Bracket M8", "Shipping Pallet", "Label Roll 100mm", "Safety Gloves L"]
SYMBOL = {"USD": "$", "EUR": "€", "GBP": "£"}


def money(d: Decimal, cur: str) -> str:
    return f"{SYMBOL[cur]}{d:,.2f}"


def make_case(i: int, rng: random.Random) -> tuple[list[list[str]], dict, str]:
    template = ["classic", "label_variants", "purchase_order", "unlabelled_supplier", "multipage", "day_first"][i % 6]
    cur = {"label_variants": "EUR", "day_first": "GBP"}.get(template, rng.choice(["USD", "USD", "EUR"]))
    supplier, customer = rng.choice(SUPPLIERS), rng.choice(CUSTOMERS)
    issued = date(2024, 1, 1) + timedelta(days=rng.randrange(600))
    due = issued + timedelta(days=rng.choice([15, 30, 45, 60]))
    number = f"{rng.choice(['INV', 'IN', 'BL'])}-{rng.randrange(1000, 99999)}"
    prints_po = template in ("classic", "label_variants", "purchase_order")
    po = f"PO-{rng.randrange(1000, 9999)}" if prints_po and (rng.random() < 0.5 or template == "purchase_order") else None

    n_items = rng.randrange(14, 22) if template == "multipage" else rng.randrange(1, 6)
    items = []
    for name in rng.sample(PRODUCTS * 2, n_items):
        qty = rng.randrange(1, 40)
        price = Decimal(rng.randrange(150, 90000)) / 100
        items.append({"description": name, "quantity": str(qty), "unit_price": f"{price:.2f}", "amount": f"{qty * price:.2f}"})
    subtotal = sum(Decimal(it["amount"]) for it in items)
    rate = rng.choice([Decimal("0"), Decimal("0.05"), Decimal("0.08"), Decimal("0.2")])
    tax = (subtotal * rate).quantize(Decimal("0.01"))
    total = subtotal + tax

    doc_type = "purchase_order" if template == "purchase_order" else "invoice"
    truth = {"document_type": doc_type, "supplier_name": supplier, "customer_name": customer,
             "document_number": po if doc_type == "purchase_order" else number,
             "po_number": po, "document_date": issued.isoformat(),
             "due_date": None if doc_type == "purchase_order" else due.isoformat(), "currency": cur,
             "subtotal": f"{subtotal:.2f}", "tax": f"{tax:.2f}", "total": f"{total:.2f}", "line_items": items}

    rows = [f"{it['description']}   {it['quantity']}   {money(Decimal(it['unit_price']), cur)}   "
            f"{money(Decimal(it['amount']), cur)}" for it in items]
    table_head = "Description   Qty   Unit Price   Amount"
    totals = [f"Subtotal: {money(subtotal, cur)}", f"Tax ({rate * 100:.0f}%): {money(tax, cur)}", f"Total: {money(total, cur)}"]

    if template == "classic":
        head = [supplier, "123 Commerce Way, Springfield", "INVOICE", f"Invoice No: {number}",
                f"Invoice Date: {issued.isoformat()}", f"Due Date: {due.isoformat()}",
                *([f"PO Number: {po}"] if po else []), f"Bill To: {customer}", ""]
        pages = [head + [table_head] + rows + [""] + totals]
    elif template == "label_variants":
        head = ["TAX INVOICE", f"Vendor: {supplier}", f"Invoice # {number}", f"Date: {issued:%B %d, %Y}",
                f"Payment due: {due:%B %d, %Y}", f"Customer: {customer}", *([f"Your ref (PO): {po}"] if po else []), ""]
        vat = f"VAT {rate * 100:.0f}%: {money(tax, cur)}"
        pages = [head + ["Item   Qty   Price   Line Total"] + rows + ["", f"Net amount: {money(subtotal, cur)}", vat,
                                                                   f"Amount Due: {money(total, cur)}"]]
        truth["subtotal"] = f"{subtotal:.2f}"  # labelled "Net amount": regex won't catch it, the model should
    elif template == "purchase_order":
        head = ["PURCHASE ORDER", f"PO Number: {po}", f"Order Date: {issued.isoformat()}", f"Vendor: {supplier}",
                f"Buyer: {customer}", "Ship To: 1 Dock Road, Port City", ""]
        pages = [head + [table_head] + rows + [""] + totals]
    elif template == "unlabelled_supplier":
        head = [supplier.upper(), "Registered office: 9 Market St", "", f"Invoice {number}",
                f"Issued {issued:%d %b %Y}", f"Terms: Net {(due - issued).days}", f"Due {due:%d %b %Y}",
                f"Billed to {customer}", ""]
        pages = [head + [table_head] + rows + ["", f"Sub total {money(subtotal, cur)}",
                                               f"Tax {money(tax, cur)}", f"TOTAL DUE {money(total, cur)}"]]
        truth["supplier_name"] = supplier.upper()
    elif template == "multipage":
        head = [supplier, "INVOICE", f"Invoice No: {number}", f"Invoice Date: {issued.isoformat()}",
                f"Due Date: {due.isoformat()}", f"Bill To: {customer}", ""]
        half = len(rows) // 2
        pages = [head + [table_head] + rows[:half] + ["continued on next page"],
                 [f"Invoice {number} - page 2", table_head] + rows[half:] + [""] + totals]
    else:  # day_first: UK-style dd/mm/yyyy, the documented ambiguity case
        head = [supplier, "INVOICE", f"Invoice No: {number}", f"Invoice Date: {issued:%d/%m/%Y}",
                f"Due Date: {due:%d/%m/%Y}", f"Bill To: {customer}", ""]
        pages = [head + [table_head] + rows + [""] + totals]
    return pages, truth, template


def main(n: int = 30, seed: int = 7) -> None:
    rng = random.Random(seed)
    OUT.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        pages, truth, template = make_case(i, rng)
        stem = f"{i:03d}_{template}"
        (OUT / f"{stem}.pdf").write_bytes(make_pdf(pages))
        (OUT / f"{stem}.json").write_text(json.dumps(truth, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {n} documents to {OUT}")


if __name__ == "__main__":
    main()
