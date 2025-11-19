# Portia Frontend Overview

This document explains how the `app-frontend` works: structure, data flow, performance optimizations, and development tips.

## 1. Tech Stack
- React + TypeScript (Vite build)
- Lightweight manual syntax highlighting from lexer tokens (no heavy editor dependency)
- REST calls to separate backend services (lexer, parser, semantic)

## 2. Directory Structure
```
app-frontend/
  src/
    main.tsx              # App bootstrap (React root)
    index.css             # Global theme + styles + token classes
    api.ts                # Backend API wrappers (lexer, parser, semantic)
    components/
      ViewSwitcher.tsx    # Switch between Lexical / Syntax / Semantics views
      LexerPanel.tsx      # Code input, lexical analysis, highlighting, token/error display
      TokenList.tsx       # Virtualized token table
      ParserTBA.tsx       # Parser preview panel (source + AST JSON)
      SemanticTBA.tsx     # Semantic analysis preview panel (lex + analysis result)
      Layout.css          # (Optional styling hook)
```

## 3. Data Flow (Lexical)
1. User edits code in `LexerPanel` textarea.
2. Debounced (350ms) auto-lex triggers unless disabled.
3. `lexCode` POSTs source to lexer backend; returns tokens + errors.
4. Tokens + errors converted into HTML highlight segments.
5. Results displayed:
   - Syntax-highlight overlay
   - Token table (virtualized)
   - Error list panel

## 4. Auto-Lex Behavior
- Auto lex is enabled by default.
- If line count reaches **≥ 80 lines**, auto lex is disabled to prevent UI lockups.
- Banner appears with manual instructions; user can click "Run Lexer" or re-enable auto.
- AbortController cancels in-flight lex requests when new edits occur.

## 5. Performance Optimizations
| Area | Technique |
|------|-----------|
| Frequent edits | Debounce (350ms) + request cancellation |
| Large inputs | Auto lex disable (≥ 80 lines) |
| Highlighting | Batched via `requestIdleCallback` / `requestAnimationFrame` |
| Token rendering | Manual virtualization in `TokenList` (row height math) |
| Scroll stability | `useLayoutEffect` restores scroll position pre-paint |
| Metrics | Lex + highlight times displayed (ms) |

### Token Table Virtualization
- Only a slice of rows near current scroll position is rendered.
- Container height emulates full size; table positioned with absolute offset.
- Row height constant: `ROW_HEIGHT = 21`. Adjust with caution (keep in sync with CSS).

### Highlight Building
- Tokens carry line + column. Lines are converted to character offsets.
- Overlapping prevention ensures clean non-overlapping spans.
- Errors produce highlight segments with `.hl-error` class.

## 6. API Layer (`api.ts`)
Functions accept optional `AbortSignal`:
- `lexCode(code, { signal })`
- `parseSource(source, { signal })`
- `parseTokens(tokens, source?, { signal })`
- `analyzeTokens(tokens, { signal })`
- `analyzeAst(ast, { signal })`

Mapping adapts backend field names:
```
backend: tokenType, tokenName, tokenLine, tokenCol
frontend: type      , lexeme    , line     , column
```

## 7. Theming
- Two themes (dark default, light) switched via `data-theme` attribute on `<html>`.
- Token classes: `.hl-keyword`, `.hl-number`, `.hl-string`, etc. Defined separately for dark/light.
- Errors have pulsing background for visibility.

## 8. Extending the Frontend
Recommended steps to add a new analyzer panel:
1. Create `NewAnalyzerPanel.tsx` in `components/`.
2. Add state + execution button similar to `ParserTBA`.
3. Wire backend call in `api.ts` (add wrapper if needed).
4. Insert into `ViewSwitcher.tsx` (tab + slider transform adjustment).

## 9. Common Tweaks
| Goal | Change |
|------|--------|
| Adjust auto-lex threshold | Edit `LINE_DISABLE_THRESHOLD` in `LexerPanel.tsx` |
| Change debounce delay | Modify `350` ms in `handleCodeChange` debounce |
| Add token class style | Update `.hl-*` rules in `index.css` |
| Make token table denser | Lower `ROW_HEIGHT` & adjust padding in CSS |

## 10. Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Highlight flashing | Extremely rapid edits | Increase debounce or disable auto lex temporarily |
| Slow large paste | Auto lex still enabled | Confirm banner; re-enable only when ready |
| Scroll jumps | Row height mismatch | Keep `ROW_HEIGHT` consistent with CSS row styling |
| Missing highlight color | Token type not mapped | Extend `tokenClass` in `LexerPanel.tsx` |

## 11. Code Style Principles
- Keep components focused (one responsibility per panel).
- Prefer explicit naming (`runLexWithCode`, not `doLex`).
- Abort previous async work before starting new.
- Avoid large external editor dependencies; current approach is deliberate minimalism.

## 12. Future Improvements (Optional)
- Web Worker offload for highlight + token mapping.
- Persist code in `localStorage` to restore session.
- User-configurable thresholds (debounce, line disable).
- Diff-based incremental highlighting.

## 13. Quick Start
```
# From repository root
cd app-frontend
npm install
npm run dev
# Open http://localhost:5173 (default Vite port)
```

## 14. Contributing Guidelines
- Keep performance instrumentation lightweight; remove heavy profilers before merging.
- Document new token types or analyzer endpoints.
- Update this file when adding major UX or data flow changes.

---
Last updated: 2025-11-19
