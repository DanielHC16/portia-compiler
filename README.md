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

- Python 3.10+ (for match-case syntax)
- Node.js 18+ and npm
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd portia-compiler

# Setup lexer backend
cd lexer-backend
python -m venv .venv-py312
.\.venv-py312\Scripts\Activate.ps1   # Windows
pip install fastapi uvicorn
cd ..

# Setup frontend
cd app-frontend
npm install
cd ..
```

### Running the Compiler

**Using Scripts (Recommended):**
```powershell
# Terminal 1 - Start lexer backend
.\scripts\start-lexer.ps1

# Terminal 2 - Start frontend
cd app-frontend
npm run dev
```

**Manual Start:**
```bash
# Terminal 1 - Backend
cd lexer-backend
.\.venv-py312\Scripts\uvicorn app.main:app --reload

# Terminal 2 - Frontend
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
│   │       └── portia_lexer.py    # FSA lexer
│   ├── test_lexer.py
│   ├── README.md
│   └── LEXER_EXPLAINED.md
│
├── parser-backend/            # Syntax parser (in development)
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
- FSA-based tokenization with 130+ states
- 38 keywords
- Comprehensive operators and delimiters
- Multiple literal types (integer, long, float, double, string, character, boolean)
- Character-level error detection
- Comment support (single-line and multi-line)

### Frontend Interface
- Real-time syntax highlighting
- Token visualization
- Error highlighting with line/column display
- Auto-closing pairs
- Theme support (dark/light)

## Technology Stack

**Backend:** Python 3.10+ | FastAPI | Uvicorn

**Frontend:** React 19 | TypeScript | Vite 7

## Testing

```bash
cd lexer-backend
.\.venv-py312\Scripts\python.exe test_lexer.py
```

## Documentation

- [Lexer Backend Documentation](lexer-backend/README.md)
- [Lexer Technical Deep-Dive](lexer-backend/LEXER_EXPLAINED.md)
- [Frontend Documentation](app-frontend/README.md)

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

**Lexer:** Complete | **Parser:** In Development | **Semantic:** In Development

**Version:** 1.0.0

**Last Updated:** November 2025
