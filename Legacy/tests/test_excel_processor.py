"""
Unit tests for Excel processing in src/excel_processor.py and its wiring into
src/agent.py. No Ollama needed: _extract_with_llm is monkeypatched.
"""

import io
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.excel_processor import ExcelProcessor, ExcelValidator
from src.agent import OrderExtractionPipeline


def make_excel_bytes() -> io.BytesIO:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Customer", "Jane Doe"])
    sheet.append(["Ship to", "123 Main St, Springfield, IL 62704"])
    sheet.append([])
    sheet.append(["Item", "Qty", "Price"])
    sheet.append(["Widget", 2, 10.0])
    sheet.append(["Gadget", 1, 5.5])

    buf = io.BytesIO()
    workbook.save(buf)
    buf.seek(0)
    return buf


def test_process_excel_splits_front_matter_from_item_table():
    result = ExcelProcessor(chunk_size=2000).process_excel(make_excel_bytes())

    assert result["success"] is True
    assert result["text"] == "Customer: Jane Doe\nShip to: 123 Main St, Springfield, IL 62704"
    assert result["tables"] == [[
        ["Item", "Qty", "Price"],
        ["Widget", "2", "10"],
        ["Gadget", "1", "5.5"],
    ]]


def test_process_excel_with_no_header_row_treats_everything_as_front_matter():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Customer", "Jane Doe"])
    sheet.append(["Order Date", "2024-01-15"])
    buf = io.BytesIO()
    workbook.save(buf)
    buf.seek(0)

    result = ExcelProcessor().process_excel(buf)

    assert result["tables"] == []
    assert "Customer: Jane Doe" in result["text"]


def test_process_excel_reports_error_on_invalid_file():
    result = ExcelProcessor().process_excel(io.BytesIO(b"not an excel file"))
    assert result["success"] is False
    assert "error" in result


def test_excel_validator_checks_header_and_size():
    valid_bytes = make_excel_bytes()
    assert ExcelValidator.is_valid_excel(valid_bytes) == (True, "")
    assert ExcelValidator.is_valid_excel(io.BytesIO(b"not an excel file"))[0] is False

    is_valid, _ = ExcelValidator.check_file_size(valid_bytes, max_size_mb=0.0001)
    assert is_valid is False


def test_process_excel_streaming_routes_through_shared_pipeline():
    agent = OrderExtractionPipeline()
    agent._extract_with_llm = lambda text: {"customer_name": "Jane Doe", "items": []}

    result = agent.process_excel(make_excel_bytes())

    assert result["order"]["customer_name"] == "Jane Doe"
    assert result["extraction_metadata"]["source_type"] == "excel"
    assert result["extraction_metadata"]["excel_info"]["num_tables"] == 1


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))
