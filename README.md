# PORTIA Compiler

PORTIA is a compiler project for the PORTIA programming language. This
repository contains the full pipeline, from lexical analysis up to runtime
execution, along with a web-based IDE for testing and demonstration.

## Quick Links

| Component | Documentation |
|-----------|---------------|
| Lexer Backend | [lexer-backend/README.md](lexer-backend/README.md) |
| Parser Backend | [parser-backend/README.md](parser-backend/README.md) |
| Semantic Backend | [semantic-backend/README.md](semantic-backend/README.md) |
| ICG Backend | [icg-backend/README.md](icg-backend/README.md) |
| Frontend | [app-frontend/README.md](app-frontend/README.md) |

## Pipeline

```text
              +----------------------+
              |  Frontend Web IDE    |
              |      :5173           |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |   Lexer Backend      |
              |      :8000           |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |   Parser Backend     |
              |      :8001           |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |  Semantic Backend    |
              |      :8002           |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |    ICG Backend       |
              |      :8003           |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |   Runtime Output     |
              +----------------------+
```

## How It Fits Together

The frontend IDE is the main entry point for the project. A PORTIA program is
written in the browser, sent to the lexer, then passed stage by stage through
the parser, semantic analyzer, and ICG/runtime layers.

- Lexer turns source code into tokens
- Parser turns tokens into an AST
- Semantic validates the AST and builds symbol information
- ICG lowers the validated program into TAC and executes it

Each stage depends on the previous one succeeding, which keeps errors clearer
and prevents misleading cascaded failures.

## Components

- `lexer-backend/` - lexical analyzer
- `parser-backend/` - recursive descent parser
- `semantic-backend/` - semantic analyzer
- `icg-backend/` - intermediate code generation and runtime execution
- `app-frontend/` - React-based IDE
- `test-scripts/` - test and regression scripts
- `revised-documents/` - grammar and language reference files


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
|-- scripts/
`-- README.md
```

## Team

### LoomVI | BSCS 3-3 | 2025-2026

PORTIA Programming Language Development Team

| Role | Team Member |
|------|-------------|
| Team Leader | Jonalene Ryza B. Abundo |
| Core Developer | Daniel Hardy C. Camacho |
| Documentation Team Lead | Mariel Kim R. Vaflor |
| Finance Team Lead | Carla R. Mabutas |
| Q/A Team | Hershey Anne P. Dalangin |
| Q/A Team | Sydney Angeleve M. Pena |

### Collaborative Development

While each team member has a designated role, LoomVI works collaboratively
across language design, implementation, testing, and documentation. PORTIA is a
shared project effort, not a set of isolated contributions.
