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

- **[Language Specification](docs/language-spec/README.md)** - Complete PORTIA language reference
- **[Installation Guide](docs/INSTALLATION.md)** - Complete setup instructions
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute to the project
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

---

## Tech Stack

- **Backend**: Python · FastAPI · Uvicorn  
- **Frontend**: React · Vite · TypeScript · Monaco Editor  

---

## Project Structure
```
portia-compiler/
├── app-frontend/          # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── api.ts        # Backend API calls
│   │   └── main.tsx      # Entry point
│   └── package.json
├── lexer-backend/         # Lexical analyzer
│   ├── app/
│   │   ├── lexer/        # Lexer implementation
│   │   └── main.py       # FastAPI server
│   └── package.json
├── parser-backend/        # Syntax analyzer
│   ├── parser/
│   │   └── syntax_analyzer.py
│   └── main.py
├── semantic-backend/      # Semantic analyzer
│   ├── semantic/
│   │   └── semantic_analyzer.py
│   └── main.py
└── scripts/              # Startup scripts
    ├── start-lexer.ps1
    ├── start-parser.ps1
    └── start-semantic.ps1
```

---

## Features

- **Lexical Analysis**: Real-time tokenization with syntax highlighting
- **Syntax Analysis**: Parse tree generation (TBA)
- **Semantic Analysis**: Type checking and validation (TBA)
- **Theme Toggle**: Switch between light and dark modes  
- **Persistent State**: Code persists across tab switches
- **Error Highlighting**: Visual feedback for lexical errors with pulsing animation
- **Line Numbers**: Synchronized line numbering with code editor
- **Fast Updates**: 20ms debounce for near-instant syntax highlighting

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
