# docdb-mcp

An MCP server that resolves patent publication numbers to their canonical
[DOCDB](https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/docdb)
identifiers.

## What it does

Given a country code and publication number, `resolve_docdb_id` returns candidate
records with canonical DOCDB ID (including kind code), first inventor, publication
date, and family ID. This is useful for asserting that DOCDB identifiers are
correct, or for recovering properly normalized DOCDB identifiers from 
citations that appear in different formats across documents:

- `US 8,000,000 (Greenberg)` → `US8000000B2`

## Installation

### Option 1 — Hosted endpoint (no install)

A public MCP server is available at `https://docdb.sarl-graip.fr/mcp` using the
streamable HTTP transport. Configure your MCP client to point at it directly:

```json
{
  "mcpServers": {
    "docdb": {
      "type": "streamable-http",
      "url": "https://docdb.sarl-graip.fr/mcp"
    }
  }
}
```

No API key or credentials required.

### Option 2 — Local install via uvx

Add this to your MCP client configuration (Claude Desktop, Continue, Cursor, etc.):

```json
{
  "mcpServers": {
    "docdb": {
      "command": "uvx",
      "args": ["docdb-mcp"],
      "env": {
        "DOCDB_API_URL": "https://docdb.sarl-graip.fr"
      }
    }
  }
}
```

`uvx` installs and runs the package in one step — no virtualenv needed.

## Tool reference

### `resolve_docdb_id(cc, number)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `cc` | `str` | Two-letter DOCDB country code, e.g. `"US"`, `"EP"`, `"WO"` |
| `number` | `str` | Publication number **without** kind code, e.g. `"8000000"` |

**Strip the kind code before calling.** The kind code is the trailing
letter+digit suffix (B2, A1, A2, U1). Passing it returns an empty list,
not an error.

```
"US8000000B2"  → cc="US",  number="8000000"
"EP1234567A1"  → cc="EP",  number="1234567"
"US 8,000,000" → cc="US",  number="8000000"
```

**Returns** a list of records (empty list = no match):

```json
[
  {
    "docdb_id":  "US8000000B2",
    "inventor":  "ROBERT J. GREENBERG",
    "date_publ": "20110816",
    "family_id": "39183031"
  }
]
```

Multiple records mean the same publication number has several document
variants (e.g. an A1 and a B2 of the same application).

## License

MIT
