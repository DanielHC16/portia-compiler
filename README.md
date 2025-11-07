# PORTIA Programming Language  
### Written by: BSCS 3‑3 A.Y. 2025‑2026 | LoomVI  

PORTIA takes its name from the Portia spider — renowned for patience, precision, and calculated strategy. Just as the spider weaves its web with intent, PORTIA weaves rules and logic into a unified and purposeful structure.

PORTIA is a **high‑level, procedural, statically typed programming language** built around clarity and discipline. Programs are written as tightly defined statements, with explicit scoping and language features that emphasize order, readability, and precision.

- **From C** → procedural structure, explicit scoping, disciplined statement design  
- **From Python** → readability, consistency, avoidance of ambiguity  
- **From Lua** → intuitive string handling  

Like a web, PORTIA programs form deliberate, interconnected patterns of intent.

---

## Documentation

- **[Quick Reference](QUICK_REFERENCE.md)** - Common commands and workflows
- **[Language Specification](docs/language-spec/README.md)** - Complete PORTIA language reference
- **[Installation Guide](docs/INSTALLATION.md)** - Complete setup instructions
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute to the project
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

---

## Tech Stack

- **Backend**: Python 3.12+ · FastAPI · Uvicorn  
- **Frontend**: React · Vite · TypeScript  

---

## Prerequisites

- **Python 3.12 or higher** (required for `match` statements and modern features)
- **Node.js 18+** (for frontend)
- **Git** (for version control)

---

## Setup

### 1. Clone the Repository
```powershell
git clone https://github.com/DanielHC16/portia-compiler.git
cd portia-compiler
```

### 2. Backend Setup

Create Python 3.12 virtual environments for each backend:

```powershell
# Lexer Backend
cd lexer-backend
py -3.12 -m venv .venv-py312
.\.venv-py312\Scripts\Activate.ps1
pip install --upgrade pip fastapi uvicorn pytest
deactivate
cd ..

# Parser Backend
cd parser-backend
py -3.12 -m venv .venv-py312
.\.venv-py312\Scripts\Activate.ps1
pip install --upgrade pip fastapi uvicorn pytest
deactivate
cd ..

# Semantic Backend
cd semantic-backend
py -3.12 -m venv .venv-py312
.\.venv-py312\Scripts\Activate.ps1
pip install --upgrade pip fastapi uvicorn pytest
deactivate
cd ..
```

### 3. Frontend Setup
```powershell
cd app-frontend
npm install
cd ..
```

### 4. Running the Application

**Important**: Run all startup scripts from the **project root directory** (`portia-compiler/`)

Start each service in a separate terminal:

```powershell
# Terminal 1 - Lexer (port 8000)
# From: portia-compiler/
.\scripts\start-lexer.ps1

# Terminal 2 - Parser (port 8001)
# From: portia-compiler/
.\scripts\start-parser.ps1

# Terminal 3 - Semantic (port 8002)
# From: portia-compiler/
.\scripts\start-semantic.ps1

# Terminal 4 - Frontend (port 5173)
# From: portia-compiler/
cd app-frontend
npm run dev
```

Access the application at `http://localhost:5173`

**Note**: The startup scripts automatically navigate to their respective backend folders and use the correct Python interpreter from `.venv-py312`.

---

## VS Code Setup

After creating virtual environments, configure VS Code to use Python 3.12:

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Select `.venv-py312/Scripts/python.exe` for each backend folder

---

## Project Structure
```
portia-compiler/
├── app-frontend/              # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── api.ts            # Backend API client + type definitions
│   │   ├── index.css         # Global styles and CSS variables
│   │   ├── main.tsx          # Application entry point
│   │   └── components/
│   │       ├── Layout.css         # Component-specific styles
│   │       ├── ViewSwitcher.tsx   # Main app with tab navigation
│   │       ├── LexerPanel.tsx     # Lexical analysis interface
│   │       ├── TokenList.tsx      # Token display component
│   │       ├── ParserTBA.tsx      # Syntax parser (TBA)
│   │       └── SemanticTBA.tsx    # Semantic analyzer (TBA)
│   └── package.json
├── lexer-backend/             # Lexical analyzer (FastAPI)
│   ├── app/
│   │   ├── main.py           # FastAPI server entry point
│   │   └── lexer/
│   │       ├── lexer.py           # Character-by-character lexer
│   │       ├── tokens.py          # Token class definition
│   │       ├── errors.py          # Lexical error handling
│   │       ├── keywords.py        # PORTIA keyword definitions
│   │       ├── character_classes.py
│   │       └── utils.py
│   └── .venv-py312/          # Python 3.12 virtual environment
├── parser-backend/            # Syntax analyzer (TBA)
│   ├── parser/
│   │   ├── api.py
│   │   └── syntax_analyzer.py
│   └── main.py
├── semantic-backend/          # Semantic analyzer (TBA)
│   ├── semantic/
│   │   ├── api.py
│   │   └── semantic_analyzer.py
│   └── main.py
├── docs/                      # Documentation
│   ├── language-spec/        # PORTIA language specification
│   ├── INSTALLATION.md
│   ├── CONTRIBUTING.md
│   └── TROUBLESHOOTING.md
└── scripts/                   # Startup scripts
    ├── start-lexer.ps1
    ├── start-parser.ps1
    └── start-semantic.ps1
```

---

## Features

### Lexical Analysis
- **Instant tokenization**: Real-time token generation with zero delay
- **Character-by-character scanning**: Ladderized keyword matching
- **38 PORTIA keywords**: All reserved words with boundary checking
- **Token types**: Keywords, operators, delimiters, literals, identifiers, comments
- **Error handling**: Strict validation - errors prevent token generation
- **Error highlighting**: Visual feedback with line/column position
- **Line numbers**: Synchronized scrolling between editor and display
- **Comment toggle**: Hide/show comment tokens

### Syntax Analysis (TBA)
- Parse tree generation
- AST visualization

### Semantic Analysis (TBA)
- Type checking and validation
- Symbol table management
- Scope analysis

### Frontend Features
- **Theme Toggle**: Switch between light and dark modes  
- **Persistent State**: Code persists across tab switches
- **Three-panel view**: Lexical, Syntax, and Semantic analyzers
- **Token display**: Filterable token list with type, lexeme, line, and column

---

## TODO List

### Backend
- [ ] Verify lexer correctness against full PORTIA spec
- [ ] Double‑check token classification
- [ ] Add robust error handling and edge‑case coverage
- [ ] Implement parser (syntax analyzer)
- [ ] Implement semantic analyzer

### Frontend
- [ ] Add syntax tree visualization
- [ ] Enhanced error messages with suggestions
- [ ] Code completion support
- [ ] Export/import code functionality

### General
- [ ] Complete CFG (Context-Free Grammar) definition
- [ ] Add comprehensive test suite
- [ ] Create language specification document
- [ ] Add example PORTIA programs

---

## License

This project is part of an academic requirement for BSCS 3-3 A.Y. 2025-2026.

---

## Team LoomVI

**BSCS 3-3 | A.Y. 2025-2026**

For questions or contributions, please see our [Contributing Guide](docs/CONTRIBUTING.md) or open an issue.

---

<div align="center">

**[⬆ Back to Top](#portia-programming-language)**

Made by Team LoomVI

</div>
