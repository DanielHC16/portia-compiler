# PORTIA Frontend

The frontend is the **visual interface** of the PORTIA compiler. It is a single-page web application built with React, TypeScript, and Vite, featuring a CodeMirror-based code editor with full PORTIA syntax highlighting. Users can write PORTIA source code and run it through the full compiler pipeline — lexer, parser, and semantic analyzer — directly in the browser, with real-time error highlighting inline in the editor.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Application Shell](#application-shell)
- [The Three Panels](#the-three-panels)
  - [Lexical Panel](#lexical-panel)
  - [Syntax Panel](#syntax-panel)
  - [Semantics Panel](#semantics-panel)
- [The Code Editor (CodeMirror)](#the-code-editor-codemirror)
- [API Client](#api-client)
- [Error Display](#error-display)
- [Token List](#token-list)
- [Themes](#themes)
- [Shared State](#shared-state)
- [Environment Configuration](#environment-configuration)
- [Running the Frontend](#running-the-frontend)
- [File Structure](#file-structure)

---

## Overview

The PORTIA frontend provides:

- A **CodeMirror 6** powered editor with PORTIA syntax highlighting using a custom language definition.
- **Three compiler views**: Lexical, Syntax, and Semantics — switchable via a tab bar.
- **Inline error highlighting** — lex errors, parse errors, and semantic errors are all underlined directly in the editor with color-coded squiggles (red for lexer, orange for parser, blue for semantic).
- **Error cards** below the editor showing human-readable error messages with monospace chips for identifier names mentioned in messages.
- A token list panel showing all recognized tokens with their types, lexemes, and line/column positions.
- **Dark / Light theme toggle** with user preference persistence in `localStorage`.
- **Shared code state** across all three panels — typing in one panel keeps the code synchronized with the others.
- Smart quote normalization — Unicode curly quotes are converted to ASCII before sending to the backend.

---

## Architecture

```
Browser
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│  App  (main.tsx → ViewSwitcher)                                  │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ LexerPanel   │  │ ParserPanel  │  │ SemanticPanel        │   │
│  │  (Lexical)   │  │  (Syntax)    │  │  (Semantics)         │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│         ▲                  ▲                    ▲                 │
│         └──────────────────┴────────────────────┘                │
│                    Shared State                                   │
│         (sharedCode, sharedTokens, sharedLexErrors)              │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  PortiaEditor (CodeMirror 6)                             │     │
│  │  portiaLanguage + error linting + theme                  │     │
│  └─────────────────────────────────────────────────────────┘     │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  api.ts  (fetch wrappers for 3 backends)                 │     │
│  └─────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
        │               │               │
        ▼               ▼               ▼
  Lexer :8000    Parser :8001   Semantic :8002
```

**Key source files:**

| File | Responsibility |
|------|---------------|
| `src/main.tsx` | React entry point, renders `<ViewSwitcher />` |
| `src/api.ts` | Typed `fetch` wrappers for all 3 backends |
| `src/index.css` | Global styles, CSS variables for themes |
| `src/components/ViewSwitcher.tsx` | App shell: header, tab bar, theme toggle, shared state |
| `src/components/LexerPanel.tsx` | Lexical analysis view |
| `src/components/ParserPanel.tsx` | Syntax analysis view |
| `src/components/SemanticPanel.tsx` | Semantic analysis view |
| `src/components/ErrorDisplay.tsx` | Error card renderer |
| `src/components/TokenList.tsx` | Token table renderer |
| `src/codemirror/PortiaEditor.tsx` | CodeMirror 6 editor component |
| `src/codemirror/portiaLanguage.ts` | PORTIA syntax highlighting rules |
| `src/codemirror/themes.ts` | Dark and light editor themes |
| `src/codemirror/index.ts` | Re-exports from the `codemirror/` folder |

---

## Application Shell

`ViewSwitcher.tsx` is the root component. It:

1. **Holds all shared state** — `sharedCode`, `sharedTokens`, `sharedLexErrors`.
2. **Renders the header** with the PORTIA brand, tab switcher, and theme toggle.
3. **Mounts all three panels** simultaneously (`display: none` when not active) so that switching tabs does not reset panel state or re-run analyses.
4. **Loads/saves the theme** to `localStorage` under the key `portia-theme`.
5. Applies the `data-theme` attribute to `document.documentElement` so CSS variables respond globally.

### Header Layout

```
[ PORTIA ]    [ Lexical | Syntax | Semantics ]    [ 🌙 / ☀️ ]
```

---

## The Three Panels

All panels share the same **two-column layout**: a CodeMirror editor on the left and an output pane (tokens + errors) on the right. Each panel is fully self-contained; it reads from and writes back to shared state.

### Lexical Panel

**File:** `src/components/LexerPanel.tsx`

**What it does:**
- Sends the current code to `POST /lex` on the lexer backend (port 8000).
- Displays the returned **token list** in a table.
- Displays **lex errors** as error cards.
- Highlights errors inline in the editor (red squiggles via CodeMirror linting).
- Updates `sharedTokens` and `sharedLexErrors` so the other panels can use the tokens.

**User flow:**
1. Write PORTIA code in the editor.
2. Click **Run Lexer**.
3. See tokens on the right and any errors highlighted inline.

**Special behavior:**
- Smart quote normalization converts `"`, `"`, `'`, `'` to ASCII `"` and `'` before sending to the backend.
- Line ending normalization: `\r\n` / `\r` → `\n`.
- A **"Hide Comments"** toggle is available to filter comment tokens from the display.
- Tokens and errors remain visible after typing new code until **Run Lexer** is clicked again, so you can reference results while editing.
- A **Reset** button restores the default example and clears all output.

---

### Syntax Panel

**File:** `src/components/ParserPanel.tsx`

**What it does:**
- Re-runs the lexer on the current code (does not consume shared tokens), then sends the token list to `POST /parse` on the parser backend (port 8001).
- If lex errors are present, shows lex errors only and skips parsing.
- Displays the final **token list** and any **parse errors** as error cards.
- Displays **both lex errors (red) and parse errors (orange)** as inline squiggles.
- Logs the full AST to the browser console on success.

**User flow:**
1. Write PORTIA code in the editor.
2. Click **Run Parser**.
3. If the code lexes cleanly, see the AST in the browser console and token list on the right.
4. If there are errors, see them as cards and inline highlights.

**Important detail:** The panel filters out `space`, `newline`, `single_comment`, and `multi_comment` tokens before sending to the parser (the parser backend also skips these, but this reduces payload size).

---

### Semantics Panel

**File:** `src/components/SemanticPanel.tsx`

**What it does:**
- Runs the **full pipeline**: lexer → parser → semantic analyzer.
- Each stage gates the next: if lex errors are found, parsing is skipped; if parse errors are found, semantic analysis is skipped.
- Sends the AST to `POST /analyze/ast` on the semantic backend (port 8002).
- Displays the token list, lex errors, parse errors, and semantic errors.
- Shows three colors of squiggles: red (lexer), orange (parser), blue (semantic).
- Shows a **"Analysis Complete"** badge when no errors are found at any stage.

**User flow:**
1. Write PORTIA code in the editor.
2. Click **Run Semantics**.
3. See a full pipeline result: tokens, any errors from any stage, and inline highlights.

**Error pipeline gating:**
```
Run Semantics button clicked
  │
  ├─ Lex code
  │    ├─ Lex errors? → Show lex errors, STOP
  │    └─ No lex errors → continue
  │
  ├─ Parse tokens (filter whitespace/comments first)
  │    ├─ Parse errors? → Show parse errors, STOP
  │    └─ AST produced → continue
  │
  └─ Analyze AST
       ├─ Semantic errors? → Show semantic errors
       └─ No errors → "Analysis complete ✓"
```

---

## The Code Editor (CodeMirror)

**File:** `src/codemirror/PortiaEditor.tsx`

The editor is built on **CodeMirror 6** with the following extensions active:

| Extension | Purpose |
|-----------|---------|
| `portiaLanguage` | Custom PORTIA syntax highlighting stream parser |
| `lineNumbers` | Line number gutter |
| `highlightActiveLine` | Highlight the current cursor line |
| `highlightActiveLineGutter` | Highlight the gutter of the current line |
| `bracketMatching` | Auto-highlight matching `()`, `[]`, `{}` |
| `closeBrackets` | Auto-close `(`, `[`, `{`, `"`, `'` |
| `indentOnInput` | Auto-indent on newline |
| `foldGutter` + `foldKeymap` | Code folding (fold/unfold blocks) |
| `history` + `historyKeymap` | Undo/redo |
| `defaultKeymap` | Standard editing shortcuts |
| `closeBracketsKeymap` | Jump-out shortcut for closing brackets |
| `linter` | Error diagnostics rendering (squiggles) |
| `lintGutter` | Error indicator dots in the gutter |

### Dynamic Reconfiguration

Three `Compartment` objects allow changing extensions without recreating the editor or losing cursor position:

| Compartment | Controls |
|------------|---------|
| `themeCompartment` | Editor theme (dark ↔ light) |
| `lintCompartment` | Error diagnostics (updates on every backend response) |
| `readOnlyCompartment` | Read-only mode toggle |

### Error Highlight Types

Errors passed as `EditorError[]` props are converted to CodeMirror `Diagnostic` objects. Each error type gets a distinct CSS class:

| `errorType` | CSS class | Squiggle color |
|-------------|-----------|---------------|
| `"lexer"` | `cm-error-lexer` | Red |
| `"parser"` | `cm-error-parser` | Orange / amber |
| `"semantic"` | `cm-error-semantic` | Blue/cyan |

The highlight range is calculated from the 1-based `line` + `column` in the error object. If `token_length` is provided (from parser errors), it highlights exactly that many characters. Otherwise it extends to the end of the current word.

---

### PORTIA Syntax Highlighting

**File:** `src/codemirror/portiaLanguage.ts`

Implemented as a **CodeMirror StreamParser** that reads the source character by character. Token categories and their highlight roles:

| PORTIA tokens | CodeMirror role |
|--------------|----------------|
| `int`, `long`, `float`, `double`, `char`, `string`, `bool`, `void` | `keyword` |
| `if`, `else`, `switch`, `case`, `default`, `for`, `while`, `do`, `break`, `return` | `keyword` |
| `var`, `const`, `global`, `func`, `main`, `weave`, `using` | `keyword` |
| `trap`, `thread`, `threadln` | `keyword` |
| `true`, `false` | `atom` |
| `// ...` single-line comments | `lineComment` |
| `/* ... */` multi-line comments | `blockComment` |
| `"..."` string literals | `string` |
| `'.'` character literals | `string` |
| Integer / long literals | `integer` |
| Float / double literals | `float` |
| Identifiers | `variableName` |
| Operators (`+`, `-`, `*`, `/`, `=`, `==`, etc.) | `operator` |
| Delimiters / punctuation | `punctuation` |

---

## API Client

**File:** `src/api.ts`

All backend communication is abstracted into typed async functions:

| Function | Endpoint | Description |
|----------|----------|-------------|
| `lexCode(code, opts?)` | `POST /lex` | Tokenize source code |
| `parseTokens(tokens, source?, lexer_errors?, opts?)` | `POST /parse` | Parse a token list |
| `parseSource(source, opts?)` | `POST /parse/source` | Lex + parse in one call |
| `analyzeTokens(tokens, opts?)` | `POST /analyze` | Legacy token analysis |
| `analyzeAst(ast, opts?)` | `POST /analyze/ast` | Analyze a parsed AST |

All functions accept an optional `{ signal: AbortSignal }` option for request cancellation. Running a new analysis while a previous one is in-flight automatically cancels the old request via `AbortController`.

### Backend URLs

By default the client assumes all backends run on localhost:

| Service | Default URL | Override env var |
|---------|------------|-----------------|
| Lexer | `http://localhost:8000` | `VITE_LEXER_BACKEND_URL` |
| Parser | `http://localhost:8001` | `VITE_PARSER_BACKEND_URL` |
| Semantic | `http://localhost:8002` | `VITE_SEMANTIC_BACKEND_URL` |

---

## Error Display

**File:** `src/components/ErrorDisplay.tsx`

A shared error card renderer used by all three panels. Features:

- Renders each error as a card with a color-coded left border (matching the squiggle color for that error type).
- Shows the line and column number.
- **Monospace chips for identifiers**: any quoted identifier in an error message like `'varName'` is rendered as an inline `<code>` chip with a subtle background.
- Clean, minimal design matching the overall dark/light theme.

**Example rendering:**
```
Error at line 5, col 3
  undeclared identifier 'score'  ← 'score' renders as a code chip
```

---

## Token List

**File:** `src/components/TokenList.tsx`

A scrollable table listing all tokens returned by the lexer:

| Column | Content |
|--------|---------|
| # | Token index |
| Type | Token type (e.g., `int`, `ID`, `INTLIT`) |
| Lexeme | The actual source text |
| Line | 1-based line number |
| Col | 1-based column number |

A "Hide Comments" toggle is available in the Lexer panel to filter out `COMMENT` and `NEWLINE` tokens from the list.

---

## Themes

**File:** `src/codemirror/themes.ts`

Two hand-crafted CodeMirror themes:

| Theme | Background | Foreground |
|-------|-----------|-----------|
| Dark | Dark navy / charcoal | Off-white / cyan accents |
| Light | White / light gray | Dark text / blue accents |

The `getCodeMirrorTheme(theme: "dark" | "light")` function returns the appropriate extensions to pass into the `themeCompartment`. Themes are also applied via CSS variables on `document.documentElement[data-theme]` for everything outside the editor (buttons, panels, text).

---

## Shared State

All three panels share a single source of truth managed by `ViewSwitcher`:

| State | Type | Direction |
|-------|------|-----------|
| `sharedCode` | `string` | Written by every panel editor; read by all |
| `sharedTokens` | `Token[]` | Written by LexerPanel; read by Parser/Semantic |
| `sharedLexErrors` | `LexError[]` | Written by LexerPanel; read by Parser/Semantic |

Because all panels are always mounted (just hidden with CSS), they receive prop updates instantly when switching tabs. This means:
- Running the lexer in the Lexical panel and switching to the Syntax panel shows those same tokens already loaded.
- All panels use the same editor contents, so there is no drift between views.

---

## Environment Configuration

Create a `.env` file in `app-frontend/` to override backend URLs (useful when deploying to a server or using different ports):

```env
VITE_LEXER_BACKEND_URL=http://your-server:8000
VITE_PARSER_BACKEND_URL=http://your-server:8001
VITE_SEMANTIC_BACKEND_URL=http://your-server:8002
```

For local development the defaults (`localhost:8000/8001/8002`) require no configuration.

---

## Running the Frontend

### Development server (hot module replacement)

```powershell
cd app-frontend
npm install      # first time only
npm run dev
```

The app will be available at **http://localhost:5173**.

### Production build

```powershell
cd app-frontend
npm run build
```

Output is written to `app-frontend/dist/`. Serve it with any static file server.

### Preview production build locally

```powershell
cd app-frontend
npm run preview
```

### Via the project-root script

```powershell
# From the project root (starts all services including frontend)
.\scripts\start-portia.ps1
```

### Dependencies

All managed by npm. Install with `npm install`.

**Runtime:**

| Package | Version | Purpose |
|---------|---------|---------|
| `react` | ^19 | UI framework |
| `react-dom` | ^19 | DOM rendering |
| `@codemirror/state` | ^6 | CodeMirror editor state |
| `@codemirror/view` | ^6 | CodeMirror editor view |
| `@codemirror/commands` | ^6 | Keyboard shortcuts |
| `@codemirror/language` | ^6 | Language support base |
| `@codemirror/lint` | ^6 | Error diagnostics/squiggles |
| `@codemirror/autocomplete` | ^6 | Bracket closing |

**Dev:**

| Package | Purpose |
|---------|---------|
| `vite` + `@vitejs/plugin-react` | Build tool + React fast refresh |
| `typescript` | Type checking |
| `eslint` | Linting |
| `tailwindcss` | Utility CSS (partially used) |

---

## File Structure

```
app-frontend/
├── index.html                    # Entry HTML (Vite root)
├── package.json                  # npm manifest + scripts
├── vite.config.ts                # Vite + React plugin config
├── tsconfig.json                 # TypeScript project references
├── tsconfig.app.json             # App-level TypeScript config
├── tsconfig.node.json            # Node tools TypeScript config
├── postcss.config.js             # PostCSS (Tailwind)
├── eslint.config.js              # ESLint flat config
├── public/
│   └── assets/                   # Static public assets
└── src/
    ├── main.tsx                  # React entry, renders <ViewSwitcher />
    ├── api.ts                    # Typed fetch wrappers for all 3 backends
    ├── index.css                 # Global styles + CSS theme variables
    ├── codemirror/
    │   ├── index.ts              # Re-exports
    │   ├── PortiaEditor.tsx      # CodeMirror 6 editor component
    │   ├── portiaLanguage.ts     # PORTIA StreamParser (syntax highlighting)
    │   └── themes.ts             # Dark / light editor themes
    └── components/
        ├── ViewSwitcher.tsx      # App shell, shared state, tab bar
        ├── LexerPanel.tsx        # Lexical analysis view
        ├── ParserPanel.tsx       # Syntax analysis view
        ├── SemanticPanel.tsx     # Semantic analysis view
        ├── ErrorDisplay.tsx      # Error card renderer
        └── TokenList.tsx         # Token table renderer
```
