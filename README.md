# PORTIA by LoomVI

PORTIA takes its name from the Portia spider — renowned for patience, precision, and calculated strategy. Just as the spider weaves its web with intent, PORTIA weaves rules and logic into a unified and purposeful structure.

PORTIA is a **high‑level, procedural, statically typed programming language** built around clarity and discipline. Programs are written as tightly defined statements, with explicit scoping and language features that emphasize order, readability, and precision.

- **From C** → procedural structure, explicit scoping, disciplined statement design  
- **From Python** → readability, consistency, avoidance of ambiguity  
- **From Lua** → intuitive string handling  

Like a web, PORTIA programs form deliberate, interconnected patterns of intent.

## Overview

PORTIA is a statically-typed, imperative programming language with a complete compiler toolchain consisting of:

- **Lexical Analyzer** - FSA-based tokenization with strict delimiter validation
- **Syntax Parser** - Context-free grammar parsing (in development)
- **Semantic Analyzer** - Type checking and semantic validation (in development)
- **Web Interface** - React-based IDE with real-time analysis and syntax highlighting

## Quick Start

### Prerequisites

- Python 3.10+ 
- Node.js 18+ and npm
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd portia-compiler

# Setup Python virtual environment
cd lexer-backend
python -m venv .venv-py312
.\.venv-py312\Scripts\Activate.ps1   # Windows PowerShell
# OR: source .venv-py312/bin/activate  # Linux/Mac
pip install fastapi uvicorn
cd ..

# Setup frontend
cd app-frontend
npm install
cd ..
```

### Running the Compiler

**Quick Start (All Services):**
```powershell
# Single command - starts all backends + frontend
.\scripts\start-portia.ps1
```

This launches:
- Lexer backend on `http://localhost:8000`
- Parser backend on `http://localhost:8001`
- Frontend on `http://localhost:5173`

Open `http://localhost:5173` in your browser.

**Individual Services:**
```powershell
# Lexer only
.\scripts\start-lexer.ps1

# Parser only
.\scripts\start-parser.ps1

# Frontend only
cd app-frontend
npm run dev
```

**Manual Start:**
```bash
# Terminal 1 - Lexer backend
cd lexer-backend
.\.venv-py312\Scripts\uvicorn app.main:app --reload --port 8000

# Terminal 2 - Parser backend
cd parser-backend
python -m venv .venv-py312  # First time only
.\.venv-py312\Scripts\Activate.ps1
pip install fastapi uvicorn  # First time only
uvicorn main:app --reload --port 8001

# Terminal 3 - Frontend
cd app-frontend
npm run dev
```

Open `http://localhost:5173` in your browser.

## Project Structure

```
portia-compiler/
├── app-frontend/              # React + TypeScript frontend
│   ├── src/
│   │   ├── api.ts            # Backend API client
│   │   ├── main.tsx          # App entry point
│   │   ├── index.css         # Global styles
│   │   └── components/       # React components
│   ├── public/
│   │   └── portia-logo.svg
│   ├── package.json
│   └── README.md
│
├── lexer-backend/             # Lexical analyzer backend
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   └── lexer/
│   │       ├── portia_lexer.py       # FSA lexer
│   │       ├── character_classes.py  # Character set definitions
│   │       └── delimiters.py         # Delimiter definitions
│   ├── docs/                 # Comprehensive documentation
│   ├── README.md
│   └── LEXER_EXPLAINED.md
│
├── parser-backend/            # Syntax parser backend
│   ├── main.py               # FastAPI application
│   ├── parser/
│   │   ├── syntax_analyzer.py    # Recursive descent parser
│   │   └── api.py                # Parser API endpoints
│   ├── PARSER_REFERENCE.md   # Complete parser documentation
│   └── README.md
│
├── semantic-backend/          # Semantic analyzer (in development)
├── scripts/                   # Utility scripts
│   ├── start-lexer.ps1
│   ├── start-parser.ps1
│   └── start-semantic.ps1
│
└── README.md                  # This file
```

## Features

### Lexical Analyzer
- **353-state FSA** (s0 initial + s1-s353 operational)
- **27 keywords** (int, bool, if, while, void, weave, etc.)
- **20 operators** (arithmetic, logical, relational, assignment)
- **11 delimiters** (parentheses, braces, brackets, semicolons, etc.)
- **6 literal types** (int, long, float, double, string, char)
- **2 comment types** (single-line `//`, multi-line `/* */`)
- **Strict delimiter validation** preventing ambiguous splits
- **Numeric overflow detection** (Int ≤10 digits, Long ≤19, Float ≤7 fractional, Double ≤16)
- **Character-level error reporting** with precise start/end indices
- **Primitive casting delimiter rules** (`(int)x` valid, `(void)x` invalid)
- **Whitespace and newline tokens** for syntax formatting

### Syntax Parser
- **Recursive descent parser** implementing LL(1) context-free grammar
- **36 AST node types** representing all language constructs
- **Panic mode error recovery** with intelligent synchronization
- **400+ production rules** covering complete PORTIA grammar
- **100+ predict sets** for optimized parsing decisions
- **Full expression parsing** with operator precedence (logical, relational, arithmetic)
- **Weave support** for user-defined struct types with field access
- **Array handling** for 1D and 2D arrays with initialization
- **Function declarations** with parameters, return types, and nested scopes
- **Control flow parsing** (if/else, switch/case, for, while, do-while)
- **Context-aware error messages** with line and column information

### Frontend Interface
- **Real-time syntax highlighting** with One Dark theme
- **Token-based coloring** (keywords, literals, operators, delimiters)
- **Interactive AST tree viewer** with collapsible nodes and hierarchical display
- **Three view modes** (Tokens, Tree, Raw JSON) for comprehensive analysis
- **Virtual scrolling** for efficient rendering of large token lists (10,000+ tokens)
- **Error highlighting** with precise character-level positioning
- **Dual panel layout** for lexical and syntax analysis
- **Auto-lex with debouncing** (350ms delay, disables at ≥80 lines)
- **Request cancellation** (AbortController prevents race conditions)
- **Line numbers** with synchronized scrolling
- **Performance optimizations** (O(1) token rendering, non-blocking highlighting)

## Technology Stack

**Backend:** Python 3.10+ | FastAPI | Uvicorn

**Frontend:** React 19 | TypeScript | Vite 7

## Testing

```bash
cd lexer-backend
.\.venv-py312\Scripts\python.exe test_lexer.py
```

## Documentation

### Core Documentation
- **[Complete Lexer Technical Reference](lexer-backend/docs/COMPLETE_LEXER_REFERENCE.md)** — Comprehensive 6000+ line reference with all functions, parameters, algorithms, state machine design, token types, error handling, performance analysis, testing, and troubleshooting.
- **[Complete Parser Technical Reference](parser-backend/PARSER_REFERENCE.md)** — Full parser documentation covering recursive descent parsing, LL(1) grammar, AST node types, error recovery, predict sets, expression parsing, and testing guide.
- **[Complete Frontend Technical Reference](app-frontend/docs/COMPLETE_FRONTEND_REFERENCE.md)** — Full React component documentation, state management, API integration, syntax highlighting algorithm, virtual scrolling, performance optimizations, and UI architecture.

### Quick References
- [Lexer Backend README](lexer-backend/README.md) — Quick start and API overview
- [Parser Backend README](parser-backend/README.md) — Parser quick start and usage
- [Frontend Overview](app-frontend/FRONTEND_OVERVIEW.md) — Quick start with architecture diagrams and configuration guide

### Specialized Documentation
- [FSA Specification](lexer-backend/docs/PORTIA_FSA_SPEC.md) — State range & casting delimiter specification
- [Lexer Deep Dive](lexer-backend/docs/LEXER_EXPLAINED.md) — Function-level technical details
- [Delimiter Reference](lexer-backend/docs/DELIMITER_REFERENCE.md) — Complete delimiter catalog
- [Lexer Architecture](lexer-backend/docs/LEXER_ARCHITECTURE.md) — Flow diagrams and architecture patterns
- [Frontend Integration Guide](lexer-backend/docs/FRONTEND_INTEGRATION.md) — End-to-end request/response flow with UI mapping

## Team

**LoomVI | BSCS 3-3 2025-2026**

PORTIA Programming Language Development Team

| Role | Team Member |
|------|-------------|
| Team Leader | Jonalene Ryza B. Abundo |
| Core Developer | Daniel Hardy C. Camacho |
| Documentation Team Lead | Mariel Kim R. Vaflor |
| Finance Team Lead | Carla R. Mabutas |
| Q/A Team | Hershey Anne P. Dalangin |
| Q/A Team | Sydney Angeleve M. Peña |

### Collaborative Development

While each team member has a designated role, LoomVI operates as a fully collaborative unit. All team members actively contribute across different aspects of the PORTIA compiler project, including:

- Grammar design and refinement
- Parser implementation and testing
- Documentation and technical writing
- Quality assurance and validation
- Project planning and coordination

This cross-functional approach ensures that every team member has a comprehensive understanding of the PORTIA language and contributes to all phases of development.

## Status

**Lexer:** Complete | **Parser:** Complete | **Semantic:** In Development

**Version:** 1.0.0

**Last Updated:** January 2026
