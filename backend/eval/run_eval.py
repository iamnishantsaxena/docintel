"""
Field-level extraction accuracy against ground-truth JSON.

    python -m eval.run_eval                 # LLM + regex (needs the configured LLM endpoint)
    python -m eval.run_eval --no-llm        # regex-only baseline
    python -m eval.run_eval --dataset eval/dataset/real

Exact-match scoring after normalisation (case/whitespace for text, Decimal for money, ISO for dates).
A field missing from the truth file (null) counts as correct only if the extraction is also null.
"""

import argparse
import json
import platform
import statistics
import time
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from app.config import settings
from app.extraction import LLMUnavailable, PDFError, extract, pdf_to_pages
from app.fields import Fields

SCALARS = ["document_type", "supplier_name", "customer_name", "document_number", "po_number", "document_date",
           "due_date", "currency", "subtotal", "tax", "total"]
HERE = Path(__file__).parent


def norm(v):
    if v is None or v == "":
        return None
    if isinstance(v, Decimal):
        return v.normalize()
    return " ".join(str(v).split()).lower()


def score(pred: Fields, truth: Fields) -> dict[str, bool]:
    out = {f: norm(getattr(pred, f)) == norm(getattr(truth, f)) for f in SCALARS}
    key = lambda li: (norm(li.quantity), norm(li.unit_price), norm(li.amount))  # noqa: E731
    out["line_items_count"] = len(pred.line_items) == len(truth.line_items)
    out["line_items_exact"] = sorted(map(key, pred.line_items)) == sorted(map(key, truth.line_items))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=str(HERE / "dataset" / "synthetic"))
    ap.add_argument("--no-llm", action="store_true")
    args = ap.parse_args()
    use_llm = not args.no_llm
    mode = f"llm:{settings.llm_model}" if use_llm else "regex-only"

    per_field = defaultdict(list)
    per_template = defaultdict(list)
    failures, latencies, fallbacks, llm_errors = [], [], [], []
    files = sorted(Path(args.dataset).glob("*.pdf"))
    for pdf in files:
        truth = Fields(**json.loads(pdf.with_suffix(".json").read_text()))
        t0 = time.monotonic()
        try:
            fields, issues, _ = extract(pdf_to_pages(pdf.read_bytes()), use_llm=use_llm)
            pred = Fields(**fields)
        except PDFError as e:
            failures.append((pdf.name, "PDF", str(e)))
            continue
        except LLMUnavailable as e:  # e.g. timeout; the worker would retry, the eval just records it
            failures.append((pdf.name, "LLM", str(e)))
            llm_errors.append(pdf.name)
            continue
        latencies.append(time.monotonic() - t0)
        print(f"{pdf.name}: {latencies[-1]:.1f}s", flush=True)
        if any(i["code"] == "llm_bad_output" for i in issues):
            fallbacks.append(pdf.name)  # at least one chunk scored on regex, not the model
        s = score(pred, truth)
        template = pdf.stem.split("_", 1)[-1]
        for f, ok in s.items():
            per_field[f].append(ok)
            if not ok:
                failures.append((pdf.name, f, f"got {getattr(pred, f, None)!s} want {getattr(truth, f, None)!s}"
                                 if f in SCALARS else f"got {len(pred.line_items)} items want {len(truth.line_items)}"))
        per_template[template].append(sum(s.values()) / len(s))

    pct = lambda xs: f"{100 * sum(xs) / len(xs):.1f}%" if xs else "n/a"  # noqa: E731
    all_scores = [ok for xs in per_field.values() for ok in xs]
    lines = [
        f"# Eval: {mode}",
        "",
        f"- Run: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} on {platform.platform()}",
        f"- Dataset: `{Path(args.dataset).relative_to(HERE.parent) if Path(args.dataset).is_relative_to(HERE.parent) else args.dataset}` ({len(files)} PDFs)",
        f"- Model: {settings.llm_model if use_llm else 'none'} @ {settings.llm_base_url if use_llm else '-'}",
        f"- Latency per document: median {statistics.median(latencies):.2f}s, max {max(latencies):.2f}s"
        if latencies else "- Latency: n/a",
        f"- Docs where the model output was unusable for ≥1 chunk (regex fallback): {len(fallbacks)}"
        + (f" ({', '.join(fallbacks)})" if fallbacks else "") if use_llm else "- LLM: not used",
        f"- Docs with no result because the LLM call failed (timeout {settings.llm_timeout_s}s): {len(llm_errors)}"
        + (f" ({', '.join(llm_errors)})" if llm_errors else "") if use_llm else "",
        f"- **Overall field accuracy: {pct(all_scores)}** ({sum(all_scores)}/{len(all_scores)} field checks)",
        "",
        "| Field | Accuracy |", "|---|---|",
        *[f"| {f} | {pct(per_field[f])} |" for f in [*SCALARS, "line_items_count", "line_items_exact"]],
        "", "| Template | Mean field accuracy | Docs |", "|---|---|---|",
        *[f"| {t} | {100 * statistics.mean(v):.1f}% | {len(v)} |" for t, v in sorted(per_template.items())],
        "", "## Misses", "", "| File | Field | Detail |", "|---|---|---|",
        *[f"| {a} | {b} | {c.replace('|', '/')} |" for a, b, c in failures],
    ]
    report = "\n".join(lines) + "\n"
    out = HERE / "results" / f"{mode.replace(':', '_').replace('/', '_')}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(report)
    print(report[:1500])
    print(f"... full report: {out}")


if __name__ == "__main__":
    main()
