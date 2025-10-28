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
- **Frontend**: React · Vite · TypeScript  

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
│   │   ├── lexer/
│   │   │   ├── lexer.py           # Character-by-character lexer
│   │   │   ├── tokens.py          # Token class definition
│   │   │   ├── errors.py          # Lexical error handling
│   │   │   ├── keywords.py        # PORTIA keyword definitions
│   │   │   ├── character_classes.py
│   │   │   └── utils.py
│   │   └── tests/            # Lexer test suite
│   └── package.json
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
