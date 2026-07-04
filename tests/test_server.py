"""Tests for the MCP server — runs against the live API."""

import os
import pytest
from docdb_mcp.server import resolve_docdb_id

pytestmark = pytest.mark.skipif(
    not os.environ.get("DOCDB_API_URL"),
    reason="DOCDB_API_URL not set",
)


def test_known_record():
    results = resolve_docdb_id("US", "8000000")
    assert len(results) >= 1
    r = results[0]
    assert r["docdb_id"].startswith("US8000000")
    assert "inventor" in r
    assert "date_publ" in r
    assert "family_id" in r


def test_kind_code_stripped_returns_empty():
    # Kind code included in number — should return empty, not error
    results = resolve_docdb_id("US", "8000000B2")
    assert results == []


def test_unknown_number_returns_empty():
    results = resolve_docdb_id("US", "0")
    assert results == []


def test_invalid_cc_raises():
    with pytest.raises(Exception):
        resolve_docdb_id("XX", "8000000")
