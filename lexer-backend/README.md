# PORTIA Lexer Backend

FastAPI-based lexical analyzer for PORTIA language using a Finite State Automaton (FSA) implementation.

## What is This?

The PORTIA lexer converts source code into tokens using a pure FSA-based state machine. It processes code character-by-character, tracking state transitions to recognize keywords, operators, literals, identifiers, and delimiters.

### Basic Usage

```python
from app.lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()
result = lexer.transition("int x = 5;")

print(result['tokens'])  # List of recognized tokens
print(result['errors'])   # List of lexical errors
```

### API Endpoint

```bash
POST /lex
Body: {"code": "int x = 5;"}
Response: {"tokens": [...], "errors": [...]}
```

## How It Works

The lexer uses a transition-based FSA approach:

1. **`transition(code)`** - Main entry point that processes source code
2. **`lex_transition(state, char)`** - Core FSA state machine that handles all state transitions
3. **Character classes** - Used for pattern matching (numbers, letters, etc.)
4. **Delimiters** - Used for validation to ensure tokens are properly separated

Every character is processed through the FSA state machine defined in `lex_transition()`, making it a pure transition-based lexer.

## Documentation

For detailed explanations, see the `docs/` folder:

- **[LEXER_EXPLAINED.md](docs/LEXER_EXPLAINED.md)** - Complete technical explanation of how the lexer works, including function descriptions, architecture, and examples
- **[LEXER_FLOW_DIAGRAM.md](docs/LEXER_FLOW_DIAGRAM.md)** - Visual diagrams showing the internal flow, state transitions, and data flow
- **[DELIMITER_REFERENCE.md](docs/DELIMITER_REFERENCE.md)** - Complete reference for all delimiter types and their usage
- **[FRONTEND_INTEGRATION.md](docs/FRONTEND_INTEGRATION.md)** - Complete guide on how data flows from the lexer backend to the React frontend, including API calls, field mapping, and visual rendering



## Status

Complete, tested, and production-ready with frontend integration.
