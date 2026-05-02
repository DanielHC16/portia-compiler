# PORTIA Frontend

The PORTIA frontend is the browser interface for the PORTIA compiler pipeline.
It is a React + TypeScript + Vite single-page app with a CodeMirror 6 editor,
phase-specific compiler panels, inline diagnostics, terminal-style runtime
output, and shared source state across all views.

The current frontend covers four compiler phases:

- Lexical analysis
- Syntax analysis
- Semantic analysis
- Intermediate Code Generation and execution

## Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Main Files](#main-files)
- [Application Shell](#application-shell)
- [Compiler Panels](#compiler-panels)
- [Code Editor](#code-editor)
- [API Client](#api-client)
- [Diagnostics](#diagnostics)
- [Shared State](#shared-state)
- [Environment Variables](#environment-variables)
- [Running Locally](#running-locally)
- [File Structure](#file-structure)

## Overview

The app lets users write PORTIA source code and run it through the compiler
without leaving the browser. Each panel focuses on one layer of the compiler,
but all panels share the same editor contents.

Main capabilities:

- CodeMirror 6 editor with PORTIA syntax highlighting.
- Four views: Lexical, Syntax, Semantics, and ICG.
- Inline error highlighting inside the editor.
- Error cards for lexer, parser, semantic, and runtime/ICG errors.
- Token table for lexer/parser/semantic pipeline visibility.
- ICG terminal output for `thread`, `threadln`, and `trap` input.
- Dark/light theme toggle persisted in `localStorage`.
- Save current source as a `.portia` file.
- Load `.portia` or `.txt` source files into the editor.
- Smart quote and line-ending normalization before backend calls.

## Architecture

```text
Browser
  |
  v
React App
  |
  +-- ViewSwitcher.tsx
      |
      +-- sharedCode
      +-- sharedTokens
      +-- sharedLexErrors
      +-- theme
      |
      +-- LexerPanel.tsx
      |     -> api.lexCode()
      |     -> lexer backend :8000 /lex
      |
      +-- ParserPanel.tsx
      |     -> api.lexCode()
      |     -> api.parseTokens()
      |     -> parser backend :8001 /parse
      |
      +-- SemanticPanel.tsx
      |     -> api.lexCode()
      |     -> api.parseTokens()
      |     -> api.analyzeAst()
      |     -> semantic backend :8002 /analyze/ast
      |
      +-- ICGPanel.tsx
            -> api.lexCode()
            -> api.parseTokens()
            -> api.analyzeAst()
            -> api.runProgram()
            -> ICG backend :8003 /run
```

The frontend does not compile PORTIA by itself. It coordinates requests to the
backend services and renders their results in a consistent UI.

## Main Files

| File | Responsibility |
| --- | --- |
| `src/main.tsx` | React entry point. Renders `ViewSwitcher`. |
| `src/api.ts` | Shared fetch wrappers for lexer, parser, semantic, and ICG backends. |
| `src/index.css` | Global layout, theme variables, panels, buttons, and editor/error styling. |
| `src/components/ViewSwitcher.tsx` | App shell, phase switcher, theme toggle, save/load buttons, shared state. |
| `src/components/LexerPanel.tsx` | Lexical analysis panel. |
| `src/components/ParserPanel.tsx` | Syntax analysis panel. |
| `src/components/SemanticPanel.tsx` | Semantic analysis panel. |
| `src/components/ICGPanel.tsx` | Intermediate code generation and execution panel. |
| `src/components/ErrorDisplay.tsx` | Shared error-card renderer. |
| `src/components/TokenList.tsx` | Scrollable token table. |
| `src/codemirror/PortiaEditor.tsx` | CodeMirror editor wrapper. |
| `src/codemirror/portiaLanguage.ts` | PORTIA syntax highlighting stream parser. |
| `src/codemirror/themes.ts` | Dark and light CodeMirror themes. |

## Application Shell

`ViewSwitcher.tsx` is the root UI component for the frontend. It owns:

- The active panel: `lexical`, `syntax`, `semantics`, or `icg`.
- The shared editor source: `sharedCode`.
- Latest lexer output: `sharedTokens` and `sharedLexErrors`.
- The current theme: `dark` or `light`.
- Save/load actions for local source files.

All four panels stay mounted and are hidden with CSS when inactive. This means
switching tabs does not destroy each panel's local result state.

The header contains:

```text
PORTIA   [ Lexical | Syntax | Semantics | ICG ]   [ Save ] [ Load ] [ Theme ]
```

## Compiler Panels

Each compiler panel has the same basic idea: an editor on the left and results
on the right. Later phases run earlier phases first so the compiler pipeline
stays honest.

### Lexical Panel

File: `src/components/LexerPanel.tsx`

The Lexical panel sends the current source to the lexer backend.

Flow:

```text
source code -> POST /lex -> tokens + lexer errors
```

It displays:

- Token list returned by the lexer.
- Lexical errors as red error cards.
- Red editor squiggles for lexer errors.

Important behavior:

- Updates `sharedTokens` and `sharedLexErrors` after a run.
- Can hide comment tokens from the displayed token list.
- Keeps old tokens/errors visible while editing until the next run.

### Syntax Panel

File: `src/components/ParserPanel.tsx`

The Syntax panel runs lexing first, then parsing if lexing succeeds.

Flow:

```text
source code
  -> POST /lex
  -> filter whitespace/comment tokens
  -> POST /parse
  -> AST or parser errors
```

It displays:

- Token list used by the parser.
- Lexer errors if lexing fails.
- Parser errors if parsing fails.
- Red editor squiggles for lexer errors.
- Orange editor squiggles for parser errors.

On successful parsing, the AST is logged to the browser console for inspection.

### Semantics Panel

File: `src/components/SemanticPanel.tsx`

The Semantics panel runs the full static-analysis pipeline.

Flow:

```text
source code
  -> POST /lex
  -> POST /parse
  -> POST /analyze/ast
  -> semantic result + symbol table
```

Each phase gates the next one:

- Lexer errors stop parsing.
- Parser errors stop semantic analysis.
- Semantic errors are displayed after a valid AST is produced.

It displays:

- Token list.
- Lexer, parser, and semantic errors.
- Color-coded editor squiggles.
- Success status when all static phases pass.

The semantic response also includes the symbol table used later by ICG/runtime.

### ICG Panel

File: `src/components/ICGPanel.tsx`

The ICG panel runs the complete compiler path and executes the generated
intermediate code.

Flow:

```text
source code
  -> POST /lex
  -> POST /parse
  -> POST /analyze/ast
  -> POST /run
  -> generated TAC + runtime output
```

The panel sends the AST and semantic symbol table to the ICG backend. The backend
generates indirect triples, executes them, and returns terminal output,
runtime errors, return value information, and input-wait state.

It displays:

- Source editor.
- A terminal-style output panel.
- Compiler errors from earlier phases when the pipeline cannot continue.
- Runtime/ICG errors when execution fails.
- Interactive input prompts for `trap`.

Runtime behavior:

- `thread` appends output to the current terminal line.
- `threadln` commits a terminal line.
- `trap` pauses execution when input is needed.
- User input is validated in the frontend and then sent back to the backend.
- The panel reruns with the accumulated input buffer so execution can continue.

Generated TAC is logged in browser developer tools for debugging.

## Code Editor

File: `src/codemirror/PortiaEditor.tsx`

The editor uses CodeMirror 6. It provides:

- Line numbers.
- Active-line highlighting.
- Bracket matching.
- Auto-closing brackets and quotes.
- Indentation support.
- Code folding.
- Undo/redo history.
- Diagnostics through CodeMirror lint extensions.
- Dark/light editor themes.

The editor receives an `errors` prop from each panel. Those errors are converted
to CodeMirror diagnostics using their line, column, and optional `token_length`.

### Syntax Highlighting

File: `src/codemirror/portiaLanguage.ts`

PORTIA highlighting is implemented with a CodeMirror `StreamParser`.

Highlighted groups include:

| PORTIA source | Highlight role |
| --- | --- |
| Data types such as `int`, `double`, `string`, `bool`, `char`, `long` | Keyword |
| Declarations such as `var`, `const`, `global`, `func`, `main`, `weave`, `using` | Keyword |
| Control flow such as `if`, `else`, `switch`, `case`, `for`, `while`, `break`, `return` | Keyword |
| IO words such as `trap`, `thread`, `threadln` | Keyword |
| `true`, `false` | Atom |
| String and character literals | String |
| Numeric literals | Integer/float |
| Operators and punctuation | Operator/punctuation |
| Comments | Line/block comment |

## API Client

File: `src/api.ts`

All backend calls go through this file. The panels should not call `fetch`
directly.

| Function | Dev endpoint | Purpose |
| --- | --- | --- |
| `lexCode(code, opts?)` | `POST http://localhost:8000/lex` | Tokenize source. |
| `parseTokens(tokens, source?, lexerErrors?, opts?)` | `POST http://localhost:8001/parse` | Parse lexer tokens into an AST. |
| `parseSource(source, opts?)` | `POST http://localhost:8001/parse/source` | Convenience lex+parse endpoint. |
| `analyzeAst(ast, opts?)` | `POST http://localhost:8002/analyze/ast` | Run semantic analysis. |
| `generateTAC(ast, symbolTable?, opts?)` | `POST http://localhost:8003/generate` | Generate TAC without executing. |
| `executeTAC(tac, inputs?, symbolTable?, opts?)` | `POST http://localhost:8003/execute` | Execute serialized TAC. |
| `runProgram(ast, inputs?, symbolTable?, opts?)` | `POST http://localhost:8003/run` | Generate TAC and execute in one call. |

Every request helper accepts an optional `AbortSignal`. Panels use this to cancel
older requests when a new run starts.

In production builds, API calls use same-origin serverless routes:

```text
/api/lex
/api/parse
/api/parse_source
/api/analyze_ast
/api/icg_generate
/api/icg_execute
/api/icg_run
```

## Diagnostics

Errors are shown in two places:

- Inline editor diagnostics.
- Error cards in the panel result area.

`ErrorDisplay.tsx` renders the error cards. It supports four categories:

| Category | Used for |
| --- | --- |
| `lexical` | Lexer errors. |
| `syntax` | Parser errors. |
| `semantic` | Semantic analyzer errors. |
| `runtime` | ICG/runtime execution errors. |

The editor currently uses lexer, parser, and semantic diagnostic styles for
inline squiggles. Runtime errors are shown in the ICG terminal error area.

## Shared State

`ViewSwitcher` owns the main cross-panel state:

| State | Type | Written by | Read by |
| --- | --- | --- | --- |
| `sharedCode` | `string` | All editors, load/reset actions | All panels |
| `sharedTokens` | `Token[]` | Lexer panel | Parser/Semantic/ICG panels |
| `sharedLexErrors` | `LexError[]` | Lexer panel | Parser/Semantic/ICG panels |
| `theme` | `"dark" | "light"` | Theme button | App shell and editor |

The panels also keep their own local result state. For example, ICG keeps
terminal lines, pending inputs, current AST, and runtime errors locally because
those are specific to execution.

## Environment Variables

For local development, no `.env` file is required if each backend runs on its
default port.

Optional overrides:

```env
VITE_LEXER_BACKEND_URL=http://localhost:8000
VITE_PARSER_BACKEND_URL=http://localhost:8001
VITE_SEMANTIC_BACKEND_URL=http://localhost:8002
VITE_ICG_BACKEND_URL=http://localhost:8003
```

These values are read by `src/api.ts`.

## Running Locally

Install frontend dependencies:

```powershell
cd app-frontend
npm install
```

Start only the frontend:

```powershell
npm run dev
```

The Vite dev server runs at:

```text
http://localhost:5173
```

Build for production:

```powershell
npm run build
```

Preview the production build:

```powershell
npm run preview
```

Start the full PORTIA stack from the project root:

```powershell
.\scripts\start-portia.ps1
```

Stop backend/frontend helper processes from the project root:

```powershell
.\scripts\stop-all.ps1
```

## File Structure

```text
app-frontend/
|-- index.html
|-- package.json
|-- vite.config.ts
|-- tsconfig.json
|-- tsconfig.app.json
|-- tsconfig.node.json
|-- postcss.config.js
|-- eslint.config.js
|-- public/
|   `-- assets/
`-- src/
    |-- main.tsx
    |-- api.ts
    |-- index.css
    |-- codemirror/
    |   |-- index.ts
    |   |-- PortiaEditor.tsx
    |   |-- portiaLanguage.ts
    |   `-- themes.ts
    `-- components/
        |-- ViewSwitcher.tsx
        |-- LexerPanel.tsx
        |-- ParserPanel.tsx
        |-- SemanticPanel.tsx
        |-- ICGPanel.tsx
        |-- ErrorDisplay.tsx
        `-- TokenList.tsx
```

## Development Notes

- Keep backend URL changes in `src/api.ts` and `.env` only.
- Keep compiler panels responsible for phase orchestration, not raw fetch calls.
- Keep shared editor state in `ViewSwitcher`.
- Keep display-only components such as `ErrorDisplay` and `TokenList` reusable
  across panels.
- When adding a new compiler phase, update the view switcher, API client, and
  this README together.
