# PORTIA Compiler

PORTIA is a compiler project for the PORTIA programming language. This
repository contains the full pipeline, from lexical analysis up to runtime
execution, along with a web-based IDE for testing and demonstration.

## Components

- `lexer-backend/` - lexical analyzer
- `parser-backend/` - recursive descent parser
- `semantic-backend/` - semantic analyzer
- `icg-backend/` - intermediate code generation and runtime execution
- `app-frontend/` - React-based IDE
- `test-scripts/` - test and regression scripts
- `revised-documents/` - grammar and language reference files

## Language Support

PORTIA currently includes support for:

- lexical analysis
- parsing into AST form
- semantic validation
- ICG and runtime execution
- built-in functions: `len`, `abs`, `sqrt`, and `pow`

## Requirements

- Python 3.12
- Node.js 18+
- npm
- PowerShell (for the provided scripts on Windows)

## Setup

### Backend Environments

```powershell
cd lexer-backend
python -m venv .venv-py312
.venv-py312\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic watchfiles
cd ..

cd parser-backend
python -m venv .venv-py312
.venv-py312\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic watchfiles
cd ..

cd semantic-backend
python -m venv .venv-py312
.venv-py312\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic watchfiles
cd ..
```

### Frontend

```powershell
cd app-frontend
npm install
cd ..
```

## Running

Start everything:

```powershell
.\scripts\start-portia.ps1
```

Stop everything:

```powershell
.\scripts\stop-all.ps1
```

Start individual services:

```powershell
.\scripts\start-lexer.ps1
.\scripts\start-parser.ps1
.\scripts\start-semantic.ps1
.\scripts\start-icg.ps1
```

## Ports

- Lexer: `8000`
- Parser: `8001`
- Semantic: `8002`
- ICG: `8003`
- Frontend: `5173`

## Project Structure

```text
portia-compiler/
|-- app-frontend/
|-- icg-backend/
|-- lexer-backend/
|-- parser-backend/
|-- semantic-backend/
|-- revised-documents/
|-- scripts/
|-- test-scripts/
`-- README.md
```

## Documentation

- [lexer-backend/README.md](lexer-backend/README.md)
- [parser-backend/README.md](parser-backend/README.md)
- [semantic-backend/README.md](semantic-backend/README.md)
- [icg-backend/README.md](icg-backend/README.md)
- [app-frontend/README.md](app-frontend/README.md)

## Team

LoomVI | BSCS 3-3 | 2025-2026

- Jonalene Ryza B. Abundo
- Daniel Hardy C. Camacho
- Mariel Kim R. Vaflor
- Carla R. Mabutas
- Hershey Anne P. Dalangin
- Sydney Angeleve M. Pena
