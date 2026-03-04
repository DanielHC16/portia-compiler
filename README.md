# PORTIA Compiler

A multi-stage compiler for the **PORTIA programming language**, featuring a hand-built FSA-based lexer, a recursive descent parser, an AST-driven semantic analyzer, and a fully interactive React + CodeMirror web IDE.

---

## Quick Links

| Component | Documentation |
|-----------|--------------|
| Lexer Backend | [lexer-backend/README.md](lexer-backend/README.md) |
| Parser Backend | [parser-backend/README.md](parser-backend/README.md) |
| Semantic Backend | [semantic-backend/README.md](semantic-backend/README.md) |
| Frontend (Web IDE) | [app-frontend/README.md](app-frontend/README.md) |

---

## How It All Fits Together

The PORTIA compiler is a classic **pipeline architecture**: each stage consumes the output of the previous one, and each stage runs as an independent backend service. The frontend orchestrates them all.

```
+--------------------------------------------------------------------------+
|                         PORTIA Compiler Pipeline                         |
|                                                                          |
|   Source Code (written in the browser editor)                            |
|          |                                                               |
|          v                                                               |
|   +----------------------------------------------------------------------+
|   | Stage 1 - Lexical Analysis              lexer-backend  port 8000     |
|   |                                                                      |
|   |  Input : raw source code string                                      |
|   |  Output: list of typed tokens  +  lex errors                         |
|   |                                                                      |
|   |  * FSA-based, character-by-character (~350 states)                   |
|   |  * Recognizes keywords, identifiers, all literal types,              |
|   |    operators, and delimiters                                         |
|   |  * Reports multiple errors without stopping early                    |
|   +----------------------------------------------------------------------+
|          | tokens[]
|          v                                                               |
|   +----------------------------------------------------------------------+
|   | Stage 2 - Syntax Analysis              parser-backend  port 8001     |
|   |                                                                      |
|   |  Input : token list                                                  |
|   |  Output: Abstract Syntax Tree (AST)  +  parse error                  |
|   |                                                                      |
|   |  * Recursive descent, 240 CFG productions, 115 non-terminals         |
|   |  * FIRST/FOLLOW/PREDICT sets in grammar.py                           |
|   |  * Blocked if lex errors exist (no cascading errors)                 |
|   |  * AST nodes represent only semantic meaning (no grammar noise)      |
|   +----------------------------------------------------------------------+
|          | AST (JSON)
|          v                                                               |
|   +----------------------------------------------------------------------+
|   | Stage 3 - Semantic Analysis        semantic-backend  port 8002       |
|   |                                                                      |
|   |  Input : AST JSON from parser                                        |
|   |  Output: semantic errors  +  symbol table                            |
|   |                                                                      |
|   |  * Two-pass AST walker (hoist globals/weaves/funcs, then bodies)     |
|   |  * Type checking, scoping, const enforcement, array shape rules      |
|   |  * Full weave (struct-like) type system validation                   |
|   |  * 209 exhaustive tests, all passing                                 |
|   +----------------------------------------------------------------------+
|          | errors[] + symbol_table{}
|          v                                                               |
|   +----------------------------------------------------------------------+
|   | Frontend - Web IDE                      app-frontend  port 5173      |
|   |                                                                      |
|   |  * React + TypeScript + Vite                                         |
|   |  * CodeMirror 6 editor with PORTIA syntax highlighting               |
|   |  * Three panels: Lexical / Syntax / Semantics                        |
|   |  * Inline error squiggles per stage (red / orange / blue)            |
|   |  * Dark / light theme toggle                                         |
|   +----------------------------------------------------------------------+
|                                                                          |
+--------------------------------------------------------------------------+
```

### Data Flow — Step by Step

1. **User types PORTIA source code** in the browser editor.
2. **Lexer** (`POST /lex`) tokenizes the code. Returns tokens + lex errors.
3. If there are lex errors → **stop**. Parser and semantic analyzer are not called.
4. **Parser** (`POST /parse`) receives the token list and produces an AST. Returns AST + parse error.
5. If there is a parse error → **stop**. Semantic analysis is not called.
6. **Semantic analyzer** (`POST /analyze/ast`) receives the AST and validates all types, scopes, and language rules. Returns semantic errors + full symbol table.
7. The **frontend** renders all errors as inline squiggles in the editor and as human-readable error cards below it.

### Error Gating

Each stage only runs if the previous stage succeeded. This is a deliberate design choice — feeding a token list with lex errors into the parser, or an invalid AST into the semantic analyzer, would produce cascading, misleading errors that obscure the real problem.

### Backend Communication

All three backends expose JSON REST APIs. The frontend calls them sequentially. Each backend is fully independent and can be called directly with `curl` or any HTTP client for testing or integration.

---

## Installation

### Prerequisites

| Tool | Minimum version | Used for |
|------|----------------|---------|
| Python | 3.12+ | All three backends |
| Node.js | 18+ | Frontend |
| npm | 9+ | Frontend package management |
| PowerShell | 5.1+ | Scripts (Windows) |

### 1 — Clone the repository

```powershell
git clone <repository-url>
cd portia-compiler
```

> **First-time Windows setup** — allow script execution if not already done:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 2 — Set up the Lexer Backend

```powershell
cd lexer-backend
python -m venv .venv-py312
.venv-py312\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic watchfiles
cd ..
```

### 3 — Set up the Parser Backend

```powershell
cd parser-backend
python -m venv .venv-py312
.venv-py312\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic watchfiles
cd ..
```

### 4 — Set up the Semantic Backend

```powershell
cd semantic-backend
python -m venv .venv-py312
.venv-py312\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic watchfiles
cd ..
```

### 5 — Set up the Frontend

```powershell
cd app-frontend
npm install
cd ..
```

---

## Running the Compiler

### Quick Start — all services at once

```powershell
.\scripts\start-portia.ps1
```

This opens four terminal windows, one per service. Each Python backend uses `uvicorn --reload` so it automatically restarts when `.py` files change. The frontend uses Vite's built-in HMR.

### Stop all services

```powershell
.\scripts\stop-all.ps1
```

### Start individual services

```powershell
.\scripts\start-lexer.ps1      # Lexer only    (port 8000)
.\scripts\start-parser.ps1     # Parser only   (port 8001)
.\scripts\start-semantic.ps1   # Semantic only (port 8002)
```

### Manual start (alternative)

```powershell
# Terminal 1 - Lexer
cd lexer-backend
.venv-py312\Scripts\python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Parser
cd parser-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8001

# Terminal 3 - Semantic
cd semantic-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8002

# Terminal 4 - Frontend
cd app-frontend
npm run dev
```

### Access the IDE

Open your browser: **http://localhost:5173**

---

## Service Summary

| Service | Port | Technology | Hot-reload |
|---------|------|-----------|-----------|
| Lexer Backend | 8000 | Python, FastAPI, uvicorn | `uvicorn --reload` |
| Parser Backend | 8001 | Python, FastAPI, uvicorn | `uvicorn --reload` |
| Semantic Backend | 8002 | Python, FastAPI, uvicorn | `uvicorn --reload` |
| Frontend | 5173 | React, TypeScript, Vite | Vite HMR |

---

## API Quick Reference

### Lexer — `POST http://localhost:8000/lex`
```json
{ "code": "int main() { return 0; }" }
```

### Parser — `POST http://localhost:8001/parse`
```json
{ "tokens": [...], "lexer_errors": [] }
```

### Parser (source shortcut) — `POST http://localhost:8001/parse/source`
```json
{ "source": "int main() { return 0; }" }
```

### Semantic — `POST http://localhost:8002/analyze/ast`
```json
{ "ast": { "node": "Program", ... } }
```

---

## Project Structure

```
portia-compiler/
|
+-- lexer-backend/              <- Stage 1: Lexical Analyzer
|   +-- app/
|   |   +-- main.py             # FastAPI app
|   |   +-- lexer/
|   |       +-- portia_lexer.py # FSA implementation
|   |       +-- character_classes.py
|   |       +-- delimiters.py
|   +-- README.md               <- Detailed lexer documentation
|
+-- parser-backend/             <- Stage 2: Recursive Descent Parser
|   +-- main.py                 # FastAPI app
|   +-- parser/
|   |   +-- portia_parser.py    # Parser (240 productions)
|   |   +-- grammar.py          # FIRST/FOLLOW/PREDICT sets
|   |   +-- ast_nodes.py        # AST node definitions
|   |   +-- api.py
|   +-- README.md               <- Detailed parser documentation
|
+-- semantic-backend/           <- Stage 3: Semantic Analyzer
|   +-- main.py                 # FastAPI app
|   +-- semantic/
|   |   +-- semantic_analyzer.py # Two-pass analyzer (1600+ lines)
|   |   +-- api.py
|   +-- README.md               <- Detailed semantic documentation
|
+-- app-frontend/               <- Web IDE
|   +-- src/
|   |   +-- api.ts              # Backend API client
|   |   +-- components/         # React panels + error display
|   |   +-- codemirror/         # Editor + syntax highlighting
|   +-- README.md               <- Detailed frontend documentation
|
+-- scripts/
|   +-- start-portia.ps1        # Start all 4 services
|   +-- stop-all.ps1            # Stop all services
|   +-- start-lexer.ps1
|   +-- start-parser.ps1
|   +-- start-semantic.ps1
|
+-- test-scripts/
|   +-- semantic/
|       +-- test_semantic_exhaustive.py  # 209-test semantic suite
|
+-- revised-documents/          # CFG and grammar reference documents
    +-- [PARSER REVAMP] CFG.txt
    +-- [PARSER REVAMP] FIRST-SET.txt
    +-- [PARSER REVAMP] FOLLOW-SET.txt
    +-- [PARSER REVAMP] PREDICT-SET.txt
```

---

## Team

### LoomVI | BSCS 3-3 | 2025-2026

**PORTIA Programming Language Development Team**

| Role | Team Member |
|------|-------------|
| **Team Leader** | Jonalene Ryza B. Abundo |
| **Core Developer** | Daniel Hardy C. Camacho |
| **Documentation Team Lead** | Mariel Kim R. Vaflor |
| **Finance Team Lead** | Carla R. Mabutas |
| **Q/A Team** | Hershey Anne P. Dalangin |
| **Q/A Team** | Sydney Angeleve M. Peña |

### Collaborative Development

While each team member has a designated role, **LoomVI operates as a fully collaborative unit**. All team members actively contribute across different aspects of the PORTIA compiler project, including:

- Grammar design and refinement
- Parser implementation and testing
- Semantic rule design and enforcement
- Documentation and technical writing
- Quality assurance and validation
- Project planning and coordination

This cross-functional approach ensures that every team member has a comprehensive understanding of the PORTIA language and contributes meaningfully to all phases of development.
