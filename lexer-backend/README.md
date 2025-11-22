# PORTIA Lexer Backend

FastAPI lexical analysis service for the PORTIA language. Implements a strict Finite State Automaton (FSA) with category‑specific delimiter enforcement, numeric overflow detection, primitive casting delimiter rules, and detailed positional error reporting.

## Overview
The lexer converts source code to a stream of tokens plus structured lexical errors. Every character is consumed exactly once by `lex_transition()` (no backtracking). Intermediate states finalize via an `'ANY'` sentinel allowing delimiter validation **without** consuming the delimiter character prematurely.

Core concepts:
- Deterministic FSA: keywords, operators, delimiters, identifiers, comments, strings, numerics, escapes, character literals each occupy explicit state ranges.
- Delimiter Enforcement: `check_delimiter()` maps token types to category sets (see `docs/DELIMITER_REFERENCE.md`) preventing ambiguous splits (e.g., `intx` becomes identifier not `int` + `x`).
- Primitive Casting: Castable types (`bool, char, double, float, int, long, string`) allow immediate `)` via `dtype_delim`. Non‑castable keywords (`void`, `weave`) require whitespace before `)`.
- Numeric Limits: Int (≤10 digits), Long (≤19), Float (≤7 fractional), Double (≤16 fractional). Overflow triggers a targeted error and consumes remaining contiguous digits.
- Error Surfaces: unexpected character, invalid delimiter, unterminated comment/string, lone decimal point, numeric overflow, identifier too long, trailing operator at EOF.

## Quick Start (Library Use)
```python
from app.lexer.portia_lexer import LexicalAnalyzer

code = "(int)x + 42.000001"  # sample
lexer = LexicalAnalyzer()
result = lexer.transition(code)

for t in result['tokens']:
    print(f"{t['tokenType']:12} {t['tokenName']}")

for e in result['errors']:
    print(f"ERROR: {e['message']} @ line {e['line']} col {e['column']}")
```

## HTTP API
`POST /lex`
Request body:
```json
{ "code": "int x = 5;" }
```
Response structure:
```json
{
  "tokens": [
    { "tokenName": "int", "tokenType": "int", "tokenLine": 1, "tokenCol": 1 },
    { "tokenName": "x", "tokenType": "identifier", "tokenLine": 1, "tokenCol": 5 }
  ],
  "errors": [
    { "message": "Lexical Error: ...", "line": 1, "column": 10, "start_index": 9, "end_index": 10 }
  ]
}
```

## Architecture Summary
| Component | File | Responsibility |
|-----------|------|---------------|
| API layer | `app/main.py` | Receives code, instantiates lexer, returns JSON |
| FSA engine | `app/lexer/portia_lexer.py` | State transitions, token assembly, error capture |
| Character sets | `app/lexer/character_classes.py` | Alphabetics, digits, whitespace, operator classes |
| Delimiters | `app/lexer/delimiters.py` | Category delimiter sets + `dtype_delim` |
| Docs | `docs/` | Canonical specs & integration guides |

## Key Guarantees
- Linear time: one pass, no backtracking.
- Deterministic token boundaries via delimiter sets.
- Primitive casting direct closure `(int)` without whitespace; `void`/`weave` require whitespace.
- Numeric overflow produces immediate clear error (does not misclassify token).
- All errors carry absolute indices (`start_index`, `end_index`) plus line/column for UI mapping.
- Identifier length enforcement (≤25 chars) with explicit error token type when exceeded.

## Selected Error Examples
| Source | Error Message |
|--------|---------------|
| `"abc` | Unterminated string literal (EOF) |
| `/* x` | Unterminated multi-line comment (EOF) |
| `123456789012` | Long literal reached maximum of 19 digits (if >19) |
| `intx` | Token 'int' not properly delimited (continues as identifier) |
| `-.` | Decimal point must be followed by at least one digit |
| `identifier_with_excessive_length_over_25_chars` | Identifier exceeds maximum length |

## Documentation Index
- `docs/PORTIA_FSA_SPEC.md` — Canonical state range & casting delimiter spec.
- `docs/LEXER_EXPLAINED.md` — Function‑level deep dive, updated numeric & casting details.
- `docs/DELIMITER_REFERENCE.md` — Full delimiter catalog with category semantics.
- `docs/LEXER_ARCHITECTURE.md` — Flow & diagrams (processing, error, state organization).
- `docs/FRONTEND_INTEGRATION.md` — End‑to‑end request/response + UI mapping.

## Testing
Run unit tests (17 currently):
```powershell
cd lexer-backend
.venv-py312\Scripts\python.exe -m pytest -q
```

## Contributing
1. Update or add states → reflect changes simultaneously in `PORTIA_FSA_SPEC.md`.
2. Add new token type → include delimiter set entry and extend `get_token_type()` mapping.
3. Preserve hash comment style (`#`) inside Python sources (project convention).
4. Run tests and add coverage for any new lexical edge cases.

## Status
Stable; passes test suite; integrated with frontend highlighting & metrics.
