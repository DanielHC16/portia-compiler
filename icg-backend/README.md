# PORTIA ICG Backend

**Intermediate Code Generator** for the PORTIA compiler.

## Overview

The ICG backend is Phase 4 of the PORTIA compiler pipeline. It transforms
semantically-validated AST into three-address code (TAC) using **Indirect Triples**
and executes the code via **RuntimeExecutor**.

## Architecture

```
icg-backend/
├── main.py              # FastAPI entry point (port 8003)
├── icg/
│   ├── __init__.py      # Package exports
│   ├── api.py           # FastAPI routes
│   ├── triple.py        # Triple, IndirectTripleTable
│   ├── managers.py      # TempManager, LabelManager
│   ├── icg_visitor.py   # AST→TAC transformation
│   └── runtime_executor.py  # TAC interpreter
└── test_*.py            # Test files
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate` | POST | Generate TAC from AST |
| `/execute` | POST | Execute TAC with inputs |
| `/run` | POST | Generate + Execute in one call |
| `/health` | GET | Health check |

### POST /run (Main Endpoint)

**Request:**
```json
{
  "ast": { ... },
  "inputs": ["42", "hello"],  // Pre-defined inputs for trap()
  "symbol_table": { ... }     // Optional
}
```

**Response:**
```json
{
  "success": true,
  "tac": { "triples": [...], "pointers": [...] },
  "tac_text": "(0) func_begin main ...",
  "tac_html": "<table>...</table>",
  "output": ["Hello", "42"],
  "return_value": null,
  "errors": []
}
```

## Running

```powershell
# Start ICG backend
.\scripts\start-icg.ps1

# Or start all services
.\scripts\start-portia.ps1
```

The backend runs on **port 8003** by default.

## TAC Operations

| Category | Operations |
|----------|------------|
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| Relational | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Logical | `&&`, `\|\|`, `not` |
| Assignment | `=` |
| Control Flow | `jump`, `jumpf`, `jumpt`, `label` |
| I/O | `trap`, `thread`, `threadln` |
| Functions | `func_begin`, `func_end`, `return` |

## Example

**PORTIA Source:**
```
func main() -> void {
    int x = 5;
    int y = 3;
    threadln(x + y);
}
```

**Generated TAC:**
```
(0)    func_begin main     -
(1)    =          x        5
(2)    =          y        3
(3)    +          x        y
(4)    threadln   (3)      -
(5)    func_end   main     -
```

**Output:** `8`

## Pipeline Integration

ICG runs **only if** all previous phases succeed:
- Lexer: `success = true`
- Parser: `success = true`
- Semantic: `success = true`

## Testing

```powershell
cd icg-backend
python test_runtime_executor.py  # Unit tests
python test_api.py               # API tests
```
