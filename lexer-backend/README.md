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

For comprehensive technical documentation, see the `docs/` folder:

### Core Documentation

- **[LEXER_EXPLAINED.md](docs/LEXER_EXPLAINED.md)** - Complete technical reference explaining **EVERYTHING** about how the lexer works
  - Every function with parameters, return types, and line numbers
  - Intermediate vs final state concepts
  - The 'ANY' pseudo-character mechanism
  - Complete workflow examples with character-by-character traces
  - All 374 states explained with categories

- **[LEXER_ARCHITECTURE.md](docs/LEXER_ARCHITECTURE.md)** - Visual architecture and flow diagrams
  - High-level system architecture
  - Data flow diagrams
  - FSA state organization
  - Processing and error handling flows
  - Token recognition examples with step-by-step state transitions

### Additional References

- **[DELIMITER_REFERENCE.md](docs/DELIMITER_REFERENCE.md)** - Complete reference for all delimiter types and their usage
- **[FRONTEND_INTEGRATION.md](docs/FRONTEND_INTEGRATION.md)** - Guide on how data flows from the lexer backend to the React frontend, including API calls, field mapping, and visual rendering



## Status

Complete, tested, and production-ready with frontend integration.
