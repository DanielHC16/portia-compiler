# PORTIA Compiler

A multi-stage compiler for the PORTIA programming language, featuring a complete lexer, parser, and semantic analyzer (in progress).

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           PORTIA Compiler                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│    Source Code                                                          │
│         │                                                               │
│         ▼                                                               │
│    ┌─────────────────┐                                                  │
│    │  Lexer Backend  │  Port 8000                                       │
│    │  (Python/FastAPI)│                                                 │
│    └────────┬────────┘                                                  │
│             │ Tokens                                                    │
│             ▼                                                           │
│    ┌─────────────────┐                                                  │
│    │ Parser Backend  │  Port 8001                                       │
│    │ (Lark/Earley)   │                                                  │
│    └────────┬────────┘                                                  │
│             │ AST                                                       │
│             ▼                                                           │
│    ┌─────────────────┐                                                  │
│    │Semantic Backend │  Port 8002 (TBA)                                 │
│    │  (Python/FastAPI)│                                                 │
│    └────────┬────────┘                                                  │
│             │                                                           │
│             ▼                                                           │
│    ┌─────────────────┐                                                  │
│    │    Frontend     │  Port 5173                                       │
│    │ (React/TypeScript/Vite)                                            │
│    └─────────────────┘                                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Components

### Lexer Backend (`lexer-backend/`)

Finite State Automaton (FSA) based lexical analyzer that tokenizes PORTIA source code.

- **Technology**: Python, FastAPI
- **Port**: 8000
- **Endpoint**: `POST /lex` - Accepts `{ "code": "..." }` and returns tokens and errors
- **Features**:
  - Character class-based FSA transitions
  - Delimiter recognition
  - Line and column tracking for error reporting
  - Support for comments, strings, and all PORTIA literals

### Parser Backend (`parser-backend/`)

Parser using the Lark parsing library with the Earley algorithm.

- **Technology**: Python, FastAPI, Lark
- **Port**: 8001
- **Endpoints**:
  - `POST /parse` - Accepts `{ "tokens": [...] }` and returns AST
  - `POST /parse/source` - Accepts `{ "source": "..." }`, calls lexer, then parses
- **Features**:
  - Earley parser with explicit ambiguity handling
  - Grammar defined in `portia.lark`
  - Error reporting with expected tokens
  - Accurate line/column positions from original lexer tokens

### Semantic Backend (`semantic-backend/`)

Semantic analyzer for type checking and symbol table management. **Status: In Progress (TBA)**

- **Technology**: Python, FastAPI
- **Port**: 8002
- **Endpoints**:
  - `POST /analyze` - Accepts tokens
  - `POST /analyze/ast` - Accepts AST for semantic analysis

### Frontend (`app-frontend/`)

Web-based IDE for writing, compiling, and debugging PORTIA programs.

- **Technology**: React, TypeScript, Vite
- **Port**: 5173
- **Features**:
  - Code editor with syntax highlighting
  - Lexer panel showing tokenization results
  - Parser panel with AST tree visualization
  - Real-time error highlighting with line/column markers
  - View switcher between compiler phases

## Setup and Installation

### Prerequisites

- Python 3.12+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd portia-compiler
   ```

2. **Set up Lexer Backend**
   ```bash
   cd lexer-backend
   python -m venv .venv-py312
   .venv-py312\Scripts\activate  # Windows
   # source .venv-py312/bin/activate  # Linux/Mac
   pip install fastapi uvicorn
   ```

3. **Set up Parser Backend**
   ```bash
   cd parser-backend
   python -m venv .venv-py312
   .venv-py312\Scripts\activate  # Windows
   pip install fastapi uvicorn lark
   ```

4. **Set up Semantic Backend**
   ```bash
   cd semantic-backend
   python -m venv .venv-py312
   .venv-py312\Scripts\activate  # Windows
   pip install fastapi uvicorn
   ```

5. **Set up Frontend**
   ```bash
   cd app-frontend
   npm install
   ```

## Running the Compiler

### Quick Start (Windows)

Use the provided PowerShell scripts:

```powershell
# Start all services (opens separate terminal windows)
./scripts/start-portia.ps1

# Stop all services
./scripts/stop-all.ps1
```

### Manual Start

Start each service in a separate terminal:

```bash
# Terminal 1: Lexer (Port 8000)
cd lexer-backend
.venv-py312\Scripts\python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Parser (Port 8001)
cd parser-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8001

# Terminal 3: Semantic (Port 8002)
cd semantic-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8002

# Terminal 4: Frontend (Port 5173)
cd app-frontend
npm run dev
```

### Access the Application

Open your browser to: **http://localhost:5173**

## API Usage

### Lexical Analysis

```bash
curl -X POST http://localhost:8000/lex \
  -H "Content-Type: application/json" \
  -d '{"code": "int main() { return 0; }"}'
```

### Parsing (with tokens)

```bash
curl -X POST http://localhost:8001/parse \
  -H "Content-Type: application/json" \
  -d '{"tokens": [...]}'
```

### Parsing (with source)

```bash
curl -X POST http://localhost:8001/parse/source \
  -H "Content-Type: application/json" \
  -d '{"source": "int main() { return 0; }"}'
```

## Project Structure

```
portia-compiler/
├── lexer-backend/          # Lexical analyzer
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   └── lexer/
│   │       ├── portia_lexer.py      # FSA-based lexer
│   │       ├── character_classes.py # Character classification
│   │       └── delimiters.py        # Delimiter recognition
│   └── docs/               # Lexer documentation
│
├── parser-backend/         # Syntax analyzer
│   ├── main.py             # FastAPI application
│   └── parser/
│       ├── api.py          # Parser API routes
│       ├── portia_parser.py # Lark-based parser
│       └── portia.lark     # Grammar definition
│
├── semantic-backend/       # Semantic analyzer (TBA)
│   ├── main.py             # FastAPI application
│   └── semantic/
│       ├── api.py          # Semantic API routes
│       └── semantic_analyzer.py
│
├── app-frontend/           # Web IDE
│   ├── src/
│   │   ├── main.tsx        # React entry point
│   │   ├── api.ts          # Backend API client
│   │   └── components/     # UI components
│   └── docs/               # Frontend documentation
│
└── scripts/                # Utility scripts
    ├── start-portia.ps1    # Start all services
    └── stop-all.ps1        # Stop all services
```

## PORTIA Language Features

- **Data Types**: `int`, `long`, `float`, `double`, `char`, `string`, `bool`
- **Variables**: Global (`global var/const`) and local (`local var/const`)
- **Arrays**: 1D and 2D arrays with optional initialization
- **Weave Types**: User-defined struct-like types
- **Functions**: User-defined functions with parameters and return types
- **Control Flow**: `if`/`else`, `switch`/`case`, `for`, `while`, `do-while`
- **I/O**: `trap` (input), `thread`/`threadln` (output)
- **Operators**: Arithmetic, relational, logical, assignment, increment/decrement

## Documentation

- `lexer-backend/docs/` - Lexer architecture and FSA specification
- `app-frontend/docs/` - Frontend component reference

## Authors

- Abundo, J.R.B.
- Camacho, D.H.C.
- Dalangin, H.A.P.
- Mabutas, C.R.
- Peña, S.A.M.
- Vaflor, M.K.R.

## License

This project is developed for educational purposes.
