# PORTIA Frontend - Quick Reference Guide

This document provides a high-level overview of the PORTIA frontend architecture. For detailed technical documentation, see [`docs/COMPLETE_FRONTEND_REFERENCE.md`](./docs/COMPLETE_FRONTEND_REFERENCE.md).

## Overview

The PORTIA frontend is a React-based interactive development environment featuring real-time lexical analysis with syntax highlighting, error reporting, and token visualization.

### Technology Stack
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 6
- **Styling**: CSS Variables (no framework dependencies)
- **State Management**: React Hooks (useState, useEffect, useRef)
- **Backend Integration**: REST API (Fetch API)

### Key Features
- **Real-Time Lexical Analysis**: Auto-lex with 350ms debouncing
- **Syntax Highlighting**: Token-based code coloring (One Dark theme)
- **Line Numbers**: Synchronized scrolling with editor
- **Virtual Scrolling**: Efficient rendering of large token lists
- **Error Highlighting**: Precise error locations with visual indicators
- **Performance Optimizations**: Request cancellation, scroll preservation, auto-lex threshold

## Architecture Flow Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                      PORTIA FRONTEND ARCHITECTURE                  │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  User Interaction Layer                                            │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Browser (http://localhost:5173)                             │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  User Types Code                                       │ │ │
│  │  │  "int x = 5;"                                          │ │ │
│  │  └───────────────────────┬────────────────────────────────┘ │ │
│  └──────────────────────────┼──────────────────────────────────┘ │
└──────────────────────────────┼────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────┐
│  Component Layer (React)                                           │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  ViewSwitcher.tsx                                            │ │
│  │  - Tab navigation (Lexer/Parser/Semantic)                    │ │
│  │  - State: activeView                                         │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
│                           │                                        │
│                           ▼                                        │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  LexerPanel.tsx (558 lines)                                  │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  State Management                                      │ │ │
│  │  │  - code: string                                        │ │ │
│  │  │  - tokens: Token[]                                     │ │ │
│  │  │  - errors: LexError[]                                 │ │ │
│  │  │  - loading: boolean                                    │ │ │
│  │  │  - hideComments: boolean                               │ │ │
│  │  │  - autoLexDisabled: boolean                            │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                                                              │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  Event Handlers                                        │ │ │
│  │  │  - handleCodeChange() → Debounce (350ms)              │ │ │
│  │  │  - runLex() / runLexWithCode() → API call             │ │ │
│  │  │  - buildHighlightsFromTokens() → Syntax highlighting  │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                                                              │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  Rendering                                             │ │ │
│  │  │  - Textarea (user input)                               │ │ │
│  │  │  - Pre overlay (syntax highlighting)                   │ │ │
│  │  │  - Line numbers (synchronized scroll)                  │ │ │
│  │  │  - Error panel                                         │ │ │
│  │  │  - TokenList component                                 │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
│                           │                                        │
│                           ▼                                        │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  TokenList.tsx (85 lines)                                    │ │
│  │  - Virtual scrolling (ROW_HEIGHT=21px)                       │ │
│  │  - ResizeObserver for viewport tracking                      │ │
│  │  - Renders only visible rows (~20-30)                        │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│  API Layer (api.ts)                                                │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  lexCode(code, { signal })                                   │ │
│  │  - POST http://localhost:8000/lex                            │ │
│  │  - Body: { "code": "int x = 5;" }                            │ │
│  │  - AbortSignal for request cancellation                      │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
└──────────────────────────┼────────────────────────────────────────┘
                           │
                           │ HTTP Request
                           │
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  Backend Layer (FastAPI)                                           │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Lexer Backend (http://localhost:8000)                       │ │
│  │  - POST /lex endpoint                                        │ │
│  │  - LexicalAnalyzer.transition()                              │ │
│  │  - Returns: { tokens, errors }                               │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
└──────────────────────────┼────────────────────────────────────────┘
                           │
                           │ JSON Response
                           │
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  Data Processing Layer                                             │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Field Mapping (api.ts)                                      │ │
│  │  Backend → Frontend                                          │ │
│  │  - tokenType  → type                                         │ │
│  │  - tokenName  → lexeme                                       │ │
│  │  - tokenLine  → line                                         │ │
│  │  - tokenCol   → column                                       │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
└──────────────────────────┼────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  State Update & Re-render                                          │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  React State Updates                                         │ │
│  │  - setTokens(mappedTokens)                                   │ │
│  │  - setErrors(errors)                                         │ │
│  │  - setLoading(false)                                         │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
└──────────────────────────┼────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  Visual Rendering                                                  │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  1. Syntax Highlighting (buildHighlightsFromTokens)          │ │
│  │     - Calculate line starts for position mapping             │ │
│  │     - Build error ranges (start_index/end_index)             │ │
│  │     - Create token matches with overlap detection            │ │
│  │     - Generate HTML segments with CSS classes                │ │
│  │                                                              │ │
│  │  2. Token Table (TokenList)                                  │ │
│  │     - Calculate visible range (scroll + viewport)            │ │
│  │     - Slice tokens array                                     │ │
│  │     - Render only visible rows                               │ │
│  │                                                              │ │
│  │  3. Error Panel                                              │ │
│  │     - Display error messages                                 │ │
│  │     - Show line/column information                           │ │
│  │     - Apply red highlighting to error ranges                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

## Data Flow Timeline

```
Time →
│
├─ T=0ms: User types "i"
│  └─→ onChange event fires
│      └─→ handleCodeChange("i")
│          ├─→ setCode("i")
│          └─→ Start 350ms debounce timer
│
├─ T=100ms: User types "n"
│  └─→ onChange event fires
│      └─→ handleCodeChange("in")
│          ├─→ setCode("in")
│          ├─→ Cancel previous debounce
│          └─→ Start new 350ms debounce timer
│
├─ T=200ms: User types "t"
│  └─→ onChange event fires
│      └─→ handleCodeChange("int")
│          ├─→ setCode("int")
│          ├─→ Cancel previous debounce
│          └─→ Start new 350ms debounce timer
│
├─ T=300ms: User types " "
│  └─→ onChange event fires
│      └─→ handleCodeChange("int ")
│          ├─→ setCode("int ")
│          ├─→ Cancel previous debounce
│          └─→ Start new 350ms debounce timer
│
├─ T=650ms: Debounce timer expires (no typing for 350ms)
│  └─→ runLexWithCode("int ")
│      ├─→ Abort any in-flight request
│      ├─→ setLoading(true)
│      └─→ lexCode("int ", { signal: abortController.signal })
│          └─→ POST http://localhost:8000/lex
│
├─ T=700ms: Backend processing
│  └─→ LexicalAnalyzer.transition("int ")
│      └─→ FSA state machine processes characters
│
├─ T=750ms: Backend response received
│  └─→ { tokens: [...], errors: [] }
│      └─→ Field mapping (tokenType → type, etc.)
│          └─→ setTokens([{type:"int", lexeme:"int", ...}])
│          └─→ setErrors([])
│          └─→ setLoading(false)
│
├─ T=751ms: React re-render triggered
│  └─→ buildHighlightsFromTokens(code, tokens, errors)
│      └─→ Generate HTML segments with classes
│          └─→ setHighlightedHTML("<span class='hl-keyword'>int</span> ")
│
└─ T=752ms: Browser paint
   └─→ Visual updates:
       ├─→ Syntax highlighting applied (keyword colored violet)
       ├─→ Token table updated (1 row: "int")
       └─→ Error panel shows "No errors"
```

---

## Directory Structure

```
app-frontend/
├── src/
│   ├── main.tsx              # Application entry point
│   ├── index.css             # Global styles and CSS variables
│   ├── api.ts                # Backend API integration
│   └── components/
│       ├── Layout.css        # Component-specific styles
│       ├── ViewSwitcher.tsx  # Tab navigation
│       ├── LexerPanel.tsx    # Main lexer interface (558 lines)
│       ├── TokenList.tsx     # Virtualized token table (85 lines)
│       ├── ParserTBA.tsx     # Parser placeholder
│       └── SemanticTBA.tsx   # Semantic analyzer placeholder
├── docs/
│   └── COMPLETE_FRONTEND_REFERENCE.md  # Detailed technical docs
├── public/                   # Static assets
├── index.html                # HTML entry point
├── vite.config.ts            # Vite configuration
├── tsconfig.json             # TypeScript config
└── package.json              # Dependencies and scripts
```

---

## Data Flow (Lexical Analysis)

1. **User Input**: Code typed in textarea (React controlled component)
2. **Debouncing**: 350ms delay prevents API spam during typing
3. **API Call**: `lexCode()` POSTs source to backend (`http://localhost:8000/lex`)
4. **Backend Processing**: Lexer returns `{ tokens, errors }`
5. **Field Mapping**: Transform backend format to frontend format:
   - `tokenType` → `type`
   - `tokenName` → `lexeme`
   - `tokenLine` → `line`
   - `tokenCol` → `column`
6. **State Update**: React state updates trigger re-render
7. **Visual Rendering**:
   - Syntax highlighting overlay (colored spans)
   - Token table (virtualized)
   - Error panel (with line/column info)

**See**: [`docs/COMPLETE_FRONTEND_REFERENCE.md`](./docs/COMPLETE_FRONTEND_REFERENCE.md) for detailed flow diagrams.

---

## Auto-Lex Behavior

- **Enabled by default**: Lexer runs automatically 350ms after typing stops
- **Threshold**: ≥80 lines disables auto-lex (performance protection)
- **Manual Override**: "Run Lexer" button always available
- **Request Cancellation**: AbortController cancels in-flight requests when user types again

---

## Performance Optimizations

| Optimization | Technique | Impact |
|--------------|-----------|--------|
| **API Calls** | Debouncing (350ms) + AbortController | ~95% reduction in requests |
| **Large Files** | Auto-lex disable (≥80 lines) | Prevents UI lockup |
| **Highlighting** | Instant synchronous rendering | Immediate visual feedback, no delays |
| **Token Table** | Virtual scrolling (ROW_HEIGHT=21px) | O(1) rendering regardless of token count |
| **Scroll Stability** | `useLayoutEffect` scroll restoration | Prevents jarring jumps |
| **Race Conditions** | Request cancellation | Eliminates stale data bugs |

### Virtual Scrolling (TokenList.tsx)
- Renders only visible rows (~20-30) instead of all tokens
- Calculates visible range based on scroll position and viewport height
- Smooth scrolling with 10,000+ tokens
- Row height constant: `ROW_HEIGHT = 21px`

### Syntax Highlighting (LexerPanel.tsx)
- Simplified algorithm (85 lines, down from 120+)
- Token-based segment building with efficient overlap detection
- Fallback column indexing for backend compatibility (1-indexed vs 0-indexed)
- Error prioritization: `start_index`/`end_index` over line/column
- CSS classes: `.hl-keyword`, `.hl-number`, `.hl-string`, `.hl-error`, etc.
- One Dark color scheme (CSS variables)
- Simple error highlighting: 2px solid red underline

---

## Component Reference

### Main Components

| Component | Purpose | Lines | Key Features |
|-----------|---------|-------|--------------|
| **main.tsx** | Application entry point | ~10 | React root, StrictMode |
| **ViewSwitcher.tsx** | Tab navigation | ~50 | Lexer/Parser/Semantic tabs |
| **LexerPanel.tsx** | Main lexer interface | 504 | Editor, highlighting, tokens, errors |
| **TokenList.tsx** | Token table | 85 | Virtual scrolling, comment filtering |
| **api.ts** | Backend integration | 60 | Type-safe API calls, field mapping |

### LexerPanel.tsx Key Functions

| Function | Purpose |
|----------|---------|
| `runLex()` / `runLexWithCode()` | Trigger lexical analysis via API |
| `handleCodeChange(newCode)` | Handle user input with debouncing |
| `buildHighlightsFromTokens()` | Generate syntax highlighting segments |
| `tokenClass(type)` | Map token type to CSS class |
| `escapeHtml(text)` | Sanitize HTML for safe rendering |

---

## API Integration (api.ts)

### Available Endpoints

- `lexCode(code, { signal? })` - Lexical analysis
- `parseSource(source, { signal? })` - Parse source code
- `parseTokens(tokens, source?, { signal? })` - Parse from tokens
- `analyzeTokens(tokens, { signal? })` - Semantic analysis from tokens
- `analyzeAst(ast, { signal? })` - Semantic analysis from AST

### Field Mapping

Backend uses different field names than frontend:

```typescript
// Backend format
{
  tokenType: "int",
  tokenName: "int",
  tokenLine: 1,
  tokenCol: 1
}

// Frontend format (after mapping)
{
  type: "int",
  lexeme: "int",
  line: 1,
  column: 1
}
```

---

## Theming

- **Two themes**: Dark (default), Light
- **Switching**: `data-theme` attribute on `<html>`
- **Token colors**:
  - **Keywords**: Purple (#c678dd)
  - **Numbers**: Orange (#d19a66)
  - **Strings**: Green (#98c379)
  - **Chars**: Cyan (#56b6c2)
  - **Comments**: Gray (#5c6370)
  - **Identifiers**: Red (#e06c75)
  - **Operators/Delimiters**: Light Gray (#abb2bf)
  - **Errors**: Red background with wavy underline

---

## Common Configuration Changes

| Goal | File | Change |
|------|------|--------|
| Adjust auto-lex threshold | `LexerPanel.tsx` | Modify `LINE_DISABLE_THRESHOLD` (currently 80) |
| Change debounce delay | `LexerPanel.tsx` | Modify timeout in `handleCodeChange` (currently 350ms) |
| Add token color | `index.css` | Add `.hl-*` rule |
| Backend URL | `.env` | Set `VITE_LEXER_BACKEND_URL` |
| Row height | `TokenList.tsx` + CSS | Update `ROW_HEIGHT` constant (keep synced) |

---

## Development Workflow

### Quick Start
```bash
cd app-frontend
npm install
npm run dev
# Open http://localhost:5173
```

### Build for Production
```bash
npm run build      # Output to dist/
npm run preview    # Preview production build
```

### Environment Variables
Create `.env` file:
```
VITE_LEXER_BACKEND_URL=http://localhost:8000
VITE_PARSER_BACKEND_URL=http://localhost:8001
VITE_SEMANTIC_BACKEND_URL=http://localhost:8002
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| CORS error | Backend not configured | Add frontend URL to CORS middleware |
| Highlight flashing | Rapid edits | Increase debounce or disable auto-lex |
| Scroll jumps | Row height mismatch | Sync `ROW_HEIGHT` with CSS |
| Missing token color | Unmapped token type | Extend `tokenClass()` function |
| Auto-lex not working | File ≥80 lines | Manually click "Run Lexer" |
| Slow large paste | Auto-lex enabled | Wait for auto-disable or click stop |

---

## Extending the Frontend

### Adding a New Analyzer Panel

1. Create `NewAnalyzerPanel.tsx` in `components/`
2. Add state + execution button similar to `ParserTBA.tsx`
3. Wire backend call in `api.ts`
4. Add tab in `ViewSwitcher.tsx`
5. Update slider transform calculation

### Adding a New Token Type

1. Update token type in `api.ts` type definitions
2. Add CSS class in `index.css` (e.g., `.hl-mynewtype`)
3. Extend `tokenClass()` function in `LexerPanel.tsx`

---

## Best Practices

- **Performance**: Keep virtual scrolling row height synchronized with CSS
- **Async**: Always abort previous requests before starting new ones
- **State**: Use `useLayoutEffect` for scroll-related updates (prevents visual jumps)
- **Naming**: Prefer explicit function names (`runLexWithCode` not `doLex`)
- **Dependencies**: Avoid heavy editor libraries; current approach is deliberately minimal

---

## Future Enhancements (Optional)

- Web Worker offload for highlighting + token mapping
- LocalStorage persistence for code across sessions
- User-configurable thresholds (debounce, line disable)
- Diff-based incremental highlighting
- Code folding for functions/blocks
- Find/Replace functionality
- Multiple file tabs
- Autocomplete suggestions

---

## Additional Documentation

- **Complete Technical Reference**: [`docs/COMPLETE_FRONTEND_REFERENCE.md`](./docs/COMPLETE_FRONTEND_REFERENCE.md)
- **Backend Integration**: [`../lexer-backend/docs/FRONTEND_INTEGRATION.md`](../lexer-backend/docs/FRONTEND_INTEGRATION.md)

---

**Last Updated**: December 2024  
**Version**: PORTIA v1.0 (React 18 + TypeScript)
