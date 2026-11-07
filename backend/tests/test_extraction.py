import httpx
import pytest

from app import extraction
from app.extraction import (LLMBadOutput, LLMUnavailable, PDFError, call_llm, chunk_pages, extract,
                            merge_chunks, parse_json_object, pdf_to_pages, regex_extract)
from eval.pdfgen import make_pdf
from tests.conftest import INVOICE_LINES

# ---------- malformed documents ----------


@pytest.mark.parametrize("data, msg", [
    (b"", "Not a PDF"),
    (b"PK\x03\x04 this is a zip", "Not a PDF"),
    (b"%PDF-1.4\n garbage garbage", "Could not parse"),
    (make_pdf([["x"]])[:60], "Could not parse"),  # truncated
    (make_pdf([[]]), "no extractable text"),  # image-only / blank
])
def test_malformed_pdfs_raise_pdf_error(data, msg):
    with pytest.raises(PDFError, match=msg):
        pdf_to_pages(data)


def test_page_limit(monkeypatch):
    monkeypatch.setattr(extraction.settings, "max_pages", 2)
    with pytest.raises(PDFError, match="limit is 2"):
        pdf_to_pages(make_pdf([["a"], ["b"], ["c"]]))


def test_multi_page_text():
    assert pdf_to_pages(make_pdf([["page one"], ["page two"]])) == ["page one", "page two"]


def test_chunk_pages_respects_limit_and_order():
    chunks = chunk_pages(["a" * 30, "b" * 30, "c" * 90], max_chars=64)
    assert all(len(c) <= 64 for c in chunks)
    assert "".join(chunks).replace("\n", "") == "a" * 30 + "b" * 30 + "c" * 90


# ---------- model output parsing ----------

@pytest.mark.parametrize("content", [
    '{"total": 5}', '```json\n{"total": 5}\n```', 'Sure! Here is the JSON:\n{"total": 5}\nHope this helps.',
])
def test_parse_json_object_tolerates_wrapping(content):
    assert parse_json_object(content) == {"total": 5}


@pytest.mark.parametrize("content", ["", "I cannot help with that.", '{"total": 5', "[1, 2, 3]", '{"a": }'])
def test_parse_json_object_rejects_bad_output(content):
    with pytest.raises(LLMBadOutput):
        parse_json_object(content)


def test_merge_chunks_first_value_wins_items_concatenate():
    merged = merge_chunks([{"total": None, "supplier_name": "A", "line_items": [{"d": 1}]},
                           {"total": 5, "supplier_name": "B", "line_items": [{"d": 2}]}])
    assert merged == {"total": 5, "supplier_name": "A", "line_items": [{"d": 1}, {"d": 2}]}


# ---------- LLM API failures ----------

def _respond(monkeypatch, response=None, exc=None):
    def fake_post(*args, **kwargs):
        if exc:
            raise exc
        return response
    monkeypatch.setattr(extraction.httpx, "post", fake_post)


def _chat(content, status=200):
    return httpx.Response(status, json={"choices": [{"message": {"content": content}}]})


@pytest.mark.parametrize("exc", [httpx.ReadTimeout("t"), httpx.ConnectError("refused")])
def test_transport_errors_are_retryable(monkeypatch, exc):
    _respond(monkeypatch, exc=exc)
    with pytest.raises(LLMUnavailable):
        call_llm("text")


@pytest.mark.parametrize("status", [429, 500, 503])
def test_rate_limit_and_server_errors_are_retryable(monkeypatch, status):
    _respond(monkeypatch, httpx.Response(status, text="busy"))
    with pytest.raises(LLMUnavailable):
        call_llm("text")


def test_client_error_is_not_retryable(monkeypatch):
    _respond(monkeypatch, httpx.Response(404, text="model not found"))
    with pytest.raises(LLMBadOutput, match="404"):
        call_llm("text")


def test_unexpected_response_shape(monkeypatch):
    _respond(monkeypatch, httpx.Response(200, json={"error": "nope"}))
    with pytest.raises(LLMBadOutput):
        call_llm("text")


def test_successful_call(monkeypatch):
    _respond(monkeypatch, _chat('{"total": "12.50"}'))
    assert call_llm("text") == ({"total": "12.50"}, extraction.settings.llm_model)


def test_reply_length_is_capped(monkeypatch):
    sent = {}
    monkeypatch.setattr(extraction.httpx, "post", lambda *a, **kw: sent.update(kw["json"]) or _chat("{}"))
    call_llm("text")
    assert sent["max_tokens"] == extraction.settings.llm_max_tokens


# ---------- pipeline ----------

TEXT = "\n".join(INVOICE_LINES)


def test_regex_extract_on_labelled_invoice():
    r = regex_extract(TEXT)
    assert r["document_number"] == "INV-1042"
    assert r["supplier_name"] == "ACME Supplies Ltd"
    assert r["customer_name"] == "Globex Corp"
    assert (r["subtotal"], r["tax"], r["total"]) == ("$450.00", "$45.00", "$495.00")
    assert len(r["line_items"]) == 2


def test_extract_prefers_llm_and_records_sources(llm):
    fields, issues, meta = extract([TEXT])
    assert fields["total"] == "495.00" and meta["sources"]["total"] == "llm"
    assert meta["llm_used"] and issues == []


def test_extract_falls_back_to_regex_on_bad_model_output(llm):
    llm.reply = LLMBadOutput("Invalid JSON from model")
    fields, issues, meta = extract([TEXT])
    assert fields["document_number"] == "INV-1042" and meta["sources"]["document_number"] == "regex"
    assert [i["code"] for i in issues] == ["llm_bad_output"] and not meta["llm_used"]


def test_extract_fills_gaps_and_flags_disagreement(llm):
    llm.reply = {**llm.reply, "supplier_name": None, "total": 594}  # missing + transposed digits
    fields, issues, meta = extract([TEXT])
    assert fields["supplier_name"] == "ACME Supplies Ltd" and meta["sources"]["supplier_name"] == "regex"
    assert any(i["code"] == "llm_regex_disagree" and i["field"] == "total" for i in issues)


def test_extract_propagates_llm_unavailable_for_retry(llm):
    llm.reply = LLMUnavailable("timeout")
    with pytest.raises(LLMUnavailable):
        extract([TEXT])


def test_extract_without_llm(llm):
    fields, _, meta = extract([TEXT], use_llm=False)
    assert llm.calls == 0 and fields["total"] == "495.00" and meta["model"] is None


# ---------- Cloud-first, local fallback ----------

CLOUD = {"cloud_llm_base_url": "https://cloud.example/v1", "cloud_llm_model": "cloud-m", "cloud_llm_api_key": "k"}


def _endpoints(monkeypatch, replies: dict, **cfg):
    """Configure endpoints and answer per base URL: a response, or an exception to raise."""
    for k, v in cfg.items():
        monkeypatch.setattr(extraction.settings, k, v)
    tried = []

    def fake_post(url, **kw):
        tried.append(kw["json"]["model"])
        r = next(v for base, v in replies.items() if url.startswith(base))
        if isinstance(r, Exception):
            raise r
        return r
    monkeypatch.setattr(extraction.httpx, "post", fake_post)
    return tried


def test_no_cloud_key_means_local_only(monkeypatch):
    tried = _endpoints(monkeypatch, {"http://localhost": _chat('{"total": "1"}')},
                       **{**CLOUD, "cloud_llm_api_key": ""})
    assert call_llm("t") == ({"total": "1"}, extraction.settings.llm_model) and tried == [extraction.settings.llm_model]


def test_cloud_key_makes_cloud_first(monkeypatch):
    tried = _endpoints(monkeypatch, {"https://cloud": _chat('{"total": "2"}')}, **CLOUD)
    assert call_llm("t") == ({"total": "2"}, "cloud-m") and tried == ["cloud-m"]  # local never called


@pytest.mark.parametrize("cloud_fails", [httpx.ConnectError("down"), httpx.Response(429, text="slow down"),
                                         httpx.Response(402, text="out of credit"), _chat("not json")])
def test_cloud_failure_falls_back_to_local(monkeypatch, cloud_fails):
    tried = _endpoints(monkeypatch, {"https://cloud": cloud_fails, "http://localhost": _chat('{"total": "3"}')},
                       **CLOUD)
    assert call_llm("t") == ({"total": "3"}, extraction.settings.llm_model)
    assert tried == ["cloud-m", extraction.settings.llm_model]


def test_all_unreachable_is_retryable(monkeypatch):
    _endpoints(monkeypatch, {"https://cloud": httpx.ConnectError("x"), "http://localhost": httpx.ReadTimeout("y")},
               **CLOUD)
    with pytest.raises(LLMUnavailable):
        call_llm("t")


def test_any_bad_output_and_none_usable_falls_back_to_regex(monkeypatch):
    _endpoints(monkeypatch, {"https://cloud": _chat("garbage"), "http://localhost": httpx.ConnectError("x")},
               **CLOUD)
    with pytest.raises(LLMBadOutput):  # not retried: extract() uses pattern matching for this chunk
        call_llm("t")


def test_cloud_only_deployment_skips_local(monkeypatch):
    tried = _endpoints(monkeypatch, {"https://cloud": _chat('{"total": "4"}')}, **CLOUD, llm_base_url="")
    assert call_llm("t")[1] == "cloud-m" and tried == ["cloud-m"]


def test_cloud_key_without_url_or_model_fails_at_startup():
    from app.config import Settings
    with pytest.raises(ValueError, match="CLOUD_LLM"):
        Settings(jwt_secret="x" * 32, cloud_llm_api_key="k")


def test_meta_records_the_model_that_answered(monkeypatch, invoice_pdf):
    _endpoints(monkeypatch, {"https://cloud": _chat('{"total": "495.00"}')}, **CLOUD)
    _, _, meta = extract(pdf_to_pages(invoice_pdf))
    assert meta["model"] == "cloud-m"
