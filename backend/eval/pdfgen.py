"""Minimal text-only PDF writer (stdlib). Good enough to produce realistic text-layer invoices for tests/eval."""


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_pdf(pages: list[list[str]]) -> bytes:
    """One list of text lines per page, Helvetica 10pt, top-left aligned."""
    page_ids = [4 + 2 * i for i in range(len(pages))]
    objs = {
        1: "<< /Type /Catalog /Pages 2 0 R >>",
        2: f"<< /Type /Pages /Kids [{' '.join(f'{p} 0 R' for p in page_ids)}] /Count {len(pages)} >>",
        3: "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    }
    for pid, lines in zip(page_ids, pages):
        stream = "BT /F1 10 Tf 14 TL 50 800 Td " + " ".join(f"({_esc(line)}) Tj T*" for line in lines) + " ET"
        objs[pid] = (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /CropBox [0 0 595 842] "
                     f"/Resources << /Font << /F1 3 0 R >> >> /Contents {pid + 1} 0 R >>")
        objs[pid + 1] = f"<< /Length {len(stream.encode('cp1252'))} >>\nstream\n{stream}\nendstream"

    out, offsets = b"%PDF-1.4\n", []
    for k in sorted(objs):
        offsets.append(len(out))
        out += f"{k} 0 obj\n{objs[k]}\nendobj\n".encode("cp1252")
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{o:010d} 00000 n \n".encode() for o in offsets)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out
