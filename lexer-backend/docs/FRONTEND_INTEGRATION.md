# Frontend-Backend Integration Guide

Complete explanation of how data flows from the PORTIA lexer backend to the React frontend, including request handling, data transformation, and visual rendering.

## Overview

The PORTIA lexer uses a REST API architecture where the React frontend sends source code to the FastAPI backend, receives tokens and errors, and displays them with real-time syntax highlighting.

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND-BACKEND ARCHITECTURE                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React Frontend (Port 5173)                             │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  LexerPanel.tsx                                    │  │  │
│  │  │  - User types code                                 │  │  │
│  │  │  - Calls lexCode()                                │  │  │
│  │  │  - Updates state                                  │  │  │
│  │  │  - Renders tokens & errors                        │  │  │
│  │  └──────────────────┬───────────────────────────────┘  │  │
│  │                     │                                   │  │
│  │  ┌──────────────────▼───────────────────────────────┐  │  │
│  │  │  api.ts                                          │  │  │
│  │  │  - HTTP POST request                             │  │  │
│  │  │  - Field mapping                                 │  │  │
│  │  │  - Error handling                                │  │  │
│  │  └──────────────────┬───────────────────────────────┘  │  │
│  └──────────────────────┼─────────────────────────────────┘  │
│                          │                                     │
│                          │ HTTP POST /lex                       │
│                          │ { "code": "int x = 5;" }            │
│                          │                                     │
│                          ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend (Port 8000)                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  main.py: lex_code()                               │  │  │
│  │  │  - Receives request                                │  │  │
│  │  │  - Creates LexicalAnalyzer                         │  │  │
│  │  │  - Calls lexer.transition()                        │  │  │
│  │  └──────────────────┬───────────────────────────────┘  │  │
│  │                     │                                   │  │
│  │  ┌──────────────────▼───────────────────────────────┐  │  │
│  │  │  portia_lexer.py: LexicalAnalyzer                  │  │  │
│  │  │  - FSA state machine                               │  │  │
│  │  │  - Token recognition                               │  │  │
│  │  │  - Error detection                                 │  │  │
│  │  │  - Returns { tokens, errors }                     │  │  │
│  │  └──────────────────┬───────────────────────────────┘  │  │
│  └──────────────────────┼─────────────────────────────────┘  │
│                          │                                     │
│                          │ JSON Response                        │
│                          │ { tokens: [...], errors: [...] }    │
│                          │                                     │
│                          ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Frontend Processing                                    │  │
│  │  - Field mapping (tokenType → type)                     │  │
│  │  - State update                                        │  │
│  │  - Syntax highlighting                                 │  │
│  │  - Error visualization                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Complete Data Flow

### Step 1: User Input

User types code in the React textarea component:

```typescript
// LexerPanel.tsx
const [code, setCode] = useState<string>("int x = 5;");

function handleCodeChange(newCode: string) {
  setCode(newCode);
  runLexWithCode(newCode);  // Triggers lexical analysis
}
```

**Visual Flow:**

```
User Types: "int x = 5;"
     │
     ▼
┌──────────────┐
│  textarea    │  ← User input captured
│  onChange    │
└──────┬───────┘
       │
       ▼
  setCode(newCode)
       │
       ▼
  runLexWithCode(newCode)
```

### Step 2: API Call

The frontend calls the `lexCode()` function which makes an HTTP POST request:

```typescript
// api.ts
export async function lexCode(code: string): Promise<{ tokens: Token[]; errors: LexError[] }> {
  const response = await postJSON(`${LEXER_URL}/lex`, { code });
  
  // Map backend field names to frontend field names
  const mappedTokens = response.tokens.map((token: any) => ({
    type: token.tokenType,      // Backend: tokenType → Frontend: type
    lexeme: token.tokenName,     // Backend: tokenName → Frontend: lexeme
    line: token.tokenLine,       // Backend: tokenLine → Frontend: line
    column: token.tokenCol       // Backend: tokenCol → Frontend: column
  }));
  
  return {
    tokens: mappedTokens,
    errors: response.errors || []
  };
}
```

**Request Details:**

```
HTTP Method: POST
URL: http://localhost:8000/lex
Headers: {
  "Content-Type": "application/json"
}
Body: {
  "code": "int x = 5;"
}
```

**Visual Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend: api.ts                                           │
│                                                             │
│  lexCode("int x = 5;")                                     │
│       │                                                     │
│       ▼                                                     │
│  postJSON("http://localhost:8000/lex", { code })           │
│       │                                                     │
│       ├─→ fetch()                                           │
│       ├─→ method: "POST"                                    │
│       ├─→ headers: { "Content-Type": "application/json" }   │
│       └─→ body: JSON.stringify({ code: "int x = 5;" })    │
│                                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP Request
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  Network Layer                                             │
│  - TCP connection                                          │
│  - HTTP/1.1 protocol                                       │
│  - JSON payload                                            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
```

### Step 3: Backend Processing

The FastAPI backend receives the request and processes it:

```python
# main.py
@app.post("/lex")
def lex_code(req: CodeRequest):
    # Main lexical analysis endpoint
    # Takes source code and returns tokens and errors
    lexer = LexicalAnalyzer()
    return lexer.transition(req.code)
```

**Backend Processing Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│  Backend: main.py                                           │
│                                                             │
│  POST /lex                                                  │
│       │                                                     │
│       ▼                                                     │
│  FastAPI receives request                                   │
│       │                                                     │
│       ├─→ Validates JSON body                               │
│       ├─→ Creates CodeRequest object                        │
│       └─→ Extracts req.code = "int x = 5;"                 │
│                                                             │
│       ▼                                                     │
│  lex_code(req)                                              │
│       │                                                     │
│       ├─→ Creates LexicalAnalyzer()                        │
│       └─→ Calls lexer.transition(req.code)                 │
│                                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend: portia_lexer.py                                   │
│                                                             │
│  LexicalAnalyzer.transition("int x = 5;")                  │
│       │                                                     │
│       ├─→ Character-by-character processing                │
│       ├─→ FSA state transitions                            │
│       ├─→ Token recognition                                │
│       ├─→ Delimiter validation                             │
│       └─→ Error detection                                  │
│                                                             │
│       ▼                                                     │
│  Returns: {                                                │
│    "tokens": [                                              │
│      { "tokenName": "int", "tokenType": "int", ... },      │
│      { "tokenName": "x", "tokenType": "identifier", ... }, │
│      { "tokenName": "=", "tokenType": "assign", ... },     │
│      { "tokenName": "5", "tokenType": "int_lit", ... },   │
│      { "tokenName": ";", "tokenType": "semicolon", ... }   │
│    ],                                                       │
│    "errors": []                                             │
│  }                                                          │
│                                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ JSON Response
                        │
                        ▼
```

### Step 4: Response Handling

The backend returns a JSON response with tokens and errors:

**Backend Response Format:**

```json
{
  "tokens": [
    {
      "tokenName": "int",
      "tokenType": "int",
      "tokenLine": 1,
      "tokenCol": 1
    },
    {
      "tokenName": "x",
      "tokenType": "identifier",
      "tokenLine": 1,
      "tokenCol": 5
    },
    {
      "tokenName": "=",
      "tokenType": "assign",
      "tokenLine": 1,
      "tokenCol": 7
    },
    {
      "tokenName": "5",
      "tokenType": "int_lit",
      "tokenLine": 1,
      "tokenCol": 9
    },
    {
      "tokenName": ";",
      "tokenType": "semicolon",
      "tokenLine": 1,
      "tokenCol": 10
    }
  ],
  "errors": []
}
```

**Visual Response Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│  Backend Response                                           │
│                                                             │
│  HTTP/1.1 200 OK                                            │
│  Content-Type: application/json                              │
│                                                             │
│  {                                                          │
│    "tokens": [...],                                         │
│    "errors": []                                             │
│  }                                                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Network Transmission
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend: api.ts                                           │
│                                                             │
│  await fetch() resolves                                     │
│       │                                                     │
│       ├─→ res.json() parses JSON                            │
│       └─→ response = { tokens: [...], errors: [...] }      │
│                                                             │
│       ▼                                                     │
│  Field Mapping                                              │
│       │                                                     │
│       ├─→ token.tokenType → type                           │
│       ├─→ token.tokenName → lexeme                         │
│       ├─→ token.tokenLine → line                           │
│       └─→ token.tokenCol → column                         │
│                                                             │
│       ▼                                                     │
│  Return mapped data                                         │
│                                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
```

### Step 5: Frontend State Update

The frontend updates React state with the transformed data:

```typescript
// LexerPanel.tsx
async function runLexWithCode(sourceCode: string) {
  setLoading(true);
  try {
    const resp = await lexCode(sourceCode);
    setTokens(resp.tokens as SimpleToken[]);  // Update tokens state
    setErrors(resp.errors);                    // Update errors state
  } catch (err: any) {
    setErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
    setTokens([]);
  } finally {
    setLoading(false);
  }
}
```

**State Update Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend State Management                                 │
│                                                             │
│  const [tokens, setTokens] = useState<SimpleToken[]>([]);  │
│  const [errors, setErrors] = useState<LexError[]>([]);     │
│                                                             │
│  After API response:                                       │
│       │                                                     │
│       ├─→ setTokens([                                       │
│       │     { type: "int", lexeme: "int", ... },           │
│       │     { type: "identifier", lexeme: "x", ... },      │
│       │     ...                                            │
│       │   ])                                               │
│       │                                                     │
│       └─→ setErrors([])                                    │
│                                                             │
│       ▼                                                     │
│  React re-renders components                                │
│                                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
```

### Step 6: Visual Rendering

The frontend renders tokens and errors in multiple ways:

#### A. Token List Display

```typescript
// TokenList.tsx
<TokenList tokens={tokens} hideComments={hideComments} />
```

**Visual:**

```
┌─────────────────────────────────────────────────────────────┐
│  Token List Table                                           │
├──────┬──────────────┬──────┬────────┬────────┐              │
│ Type │ Lexeme       │ Line │ Column │        │              │
├──────┼──────────────┼──────┼────────┼────────┤              │
│ int  │ int          │ 1    │ 1      │        │              │
│ id   │ x            │ 1    │ 5      │        │              │
│ =    │ =            │ 1    │ 7      │        │              │
│ int  │ 5            │ 1    │ 9      │        │              │
│ ;    │ ;            │ 1    │ 10     │        │              │
└──────┴──────────────┴──────┴────────┴────────┘              │
│ Total: 5 tokens                                              │
└─────────────────────────────────────────────────────────────┘
```

#### B. Syntax Highlighting

The frontend applies color-coded syntax highlighting based on token types:

```typescript
// LexerPanel.tsx
function buildHighlightsFromTokens(src: string, toks: SimpleToken[], errs: LexError[]) {
  // Build colored spans for each token
  // Keywords: violet (#cba6f7)
  // Identifiers: white (#cdd6f4)
  // Numbers: amber (#fab387)
  // Strings: green (#a6e3a1)
  // Operators: cyan (#89b4fa)
  // ...
}
```

**Visual Highlighting:**

```
┌─────────────────────────────────────────────────────────────┐
│  Code Editor with Syntax Highlighting                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 1 │ int x = 5;                                      │  │
│  └─────────────────────────────────────────────────────┘  │
│     │                                                      │
│     ├─→ "int"   → Keyword (violet)                        │
│     ├─→ "x"     → Identifier (white)                      │
│     ├─→ "="     → Operator (cyan)                         │
│     ├─→ "5"     → Number (amber)                         │
│     └─→ ";"     → Delimiter (white)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### C. Error Visualization

Errors are highlighted with red backgrounds and borders:

```typescript
// Error highlighting
errorRanges.forEach(range => {
  // Apply red background: rgba(255, 0, 0, 0.2)
  // Apply red border: 2px solid red (bottom)
  // Add pulse animation
});
```

**Visual Error Display:**

```
┌─────────────────────────────────────────────────────────────┐
│  Code Editor with Error Highlighting                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 1 │ "Hello                                          │  │
│  └─────────────────────────────────────────────────────┘  │
│     │                                                      │
│     └─→ Red background + border                            │
│         Error: "Unterminated string literal"               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Field Mapping Details

The backend and frontend use different field names. The mapping happens in `api.ts`:

### Backend Format

```python
# Backend returns:
{
    "tokenName": "int",      # The actual text
    "tokenType": "int",       # Token category
    "tokenLine": 1,          # Line number (1-indexed)
    "tokenCol": 1            # Column number (1-indexed)
}
```

### Frontend Format

```typescript
// Frontend expects:
{
    lexeme: "int",           // tokenName → lexeme
    type: "int",             // tokenType → type
    line: 1,                 // tokenLine → line
    column: 1                // tokenCol → column
}
```

### Mapping Function

```typescript
const mappedTokens = response.tokens.map((token: any) => ({
  type: token.tokenType,      // Backend field → Frontend field
  lexeme: token.tokenName,
  line: token.tokenLine,
  column: token.tokenCol
}));
```

**Visual Mapping:**

```
┌─────────────────────────────────────────────────────────────┐
│  Field Mapping Process                                     │
│                                                             │
│  Backend Token:                                            │
│  {                                                         │
│    tokenName: "int",                                       │
│    tokenType: "int",                                       │
│    tokenLine: 1,                                           │
│    tokenCol: 1                                             │
│  }                                                         │
│       │                                                    │
│       │ map() transformation                              │
│       ▼                                                    │
│  Frontend Token:                                           │
│  {                                                         │
│    lexeme: "int",    ← tokenName                          │
│    type: "int",      ← tokenType                          │
│    line: 1,          ← tokenLine                          │
│    column: 1         ← tokenCol                           │
│  }                                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Error Handling Flow

### Backend Error Format

```python
# Backend returns errors as:
{
    "message": "Lexical Error: Unexpected character '@'",
    "line": 1,
    "column": 5,
    "start_index": 4,    # Character position in source
    "end_index": 5       # End position
}
```

### Frontend Error Processing

```typescript
// LexerPanel.tsx
function buildHighlightsFromTokens(src: string, toks: SimpleToken[], errs: LexError[]) {
  // Build error positions for highlighting
  const errorRanges: Array<{start: number, end: number}> = [];
  
  for (const err of errs) {
    // Use start_index/end_index if available (character position based)
    if (err.start_index !== undefined && err.end_index !== undefined) {
      errorRanges.push({ start: err.start_index, end: err.end_index });
    } else {
      // Fallback to line/column calculation
      // Calculate character position from line/column
    }
  }
  
  // Apply red highlighting to error ranges
}
```

**Error Flow Diagram:**

```
┌─────────────────────────────────────────────────────────────┐
│  Error Detection & Display                                 │
│                                                             │
│  Backend detects error:                                    │
│  {                                                          │
│    message: "Unexpected character '@'",                    │
│    line: 1,                                                │
│    column: 5,                                              │
│    start_index: 4,                                         │
│    end_index: 5                                            │
│  }                                                          │
│       │                                                    │
│       │ Sent in response                                  │
│       ▼                                                    │
│  Frontend receives error                                    │
│       │                                                    │
│       ├─→ setErrors([error])                               │
│       └─→ buildHighlightsFromTokens()                      │
│              │                                             │
│              ├─→ Extract start_index/end_index            │
│              └─→ Apply red highlighting                    │
│                     │                                       │
│                     ▼                                       │
│  Visual Error Display:                                      │
│  ┌─────────────────────────────────────┐                  │
│  │ int x @ 5;                          │                  │
│  │      └─┘                            │                  │
│  │    Red background                   │                  │
│  └─────────────────────────────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Real-Time Updates

The frontend updates in real-time as the user types:

### Update Flow

```
User Types Character
     │
     ▼
onChange Event
     │
     ▼
handleCodeChange(newCode)
     │
     ├─→ setCode(newCode)          // Update code state
     └─→ runLexWithCode(newCode)   // Trigger API call
              │
              ▼
         API Request
              │
              ▼
         Backend Processing
              │
              ▼
         Response Received
              │
              ├─→ setTokens(tokens)  // Update tokens
              └─→ setErrors(errors)  // Update errors
                     │
                     ▼
                React Re-render
                     │
                     ├─→ Token list updates
                     ├─→ Syntax highlighting updates
                     └─→ Error highlighting updates
```

**Timeline Visualization:**

```
Time →
│
├─ User types "i"
│  └─→ API call → Backend → Response → Update UI
│
├─ User types "n"
│  └─→ API call → Backend → Response → Update UI
│
├─ User types "t"
│  └─→ API call → Backend → Response → Update UI
│
└─ User types " "
   └─→ API call → Backend → Response → Update UI
       (Token "int" finalized)
```

## CORS Configuration

The backend must allow requests from the frontend origin:

```python
# main.py
origins = [
    "http://localhost:5173",  # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**CORS Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│  CORS Request Flow                                         │
│                                                             │
│  Frontend (localhost:5173)                                  │
│       │                                                     │
│       │ POST http://localhost:8000/lex                     │
│       │ Origin: http://localhost:5173                      │
│       │                                                     │
│       ▼                                                     │
│  Backend (localhost:8000)                                   │
│       │                                                     │
│       ├─→ CORS Middleware checks Origin                    │
│       ├─→ Matches "http://localhost:5173"                 │
│       ├─→ Allows request                                    │
│       └─→ Adds CORS headers to response                   │
│              │                                             │
│              ├─→ Access-Control-Allow-Origin: *            │
│              └─→ Access-Control-Allow-Methods: *           │
│                                                             │
│       ▼                                                     │
│  Response sent with CORS headers                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Complete Example Flow

Let's trace a complete example: `"int x = 5;"`

### Step-by-Step Flow

```
1. User Input
   ┌─────────────────────────────────────┐
   │ User types: "int x = 5;"           │
   └─────────────────────────────────────┘
              │
              ▼

2. Frontend API Call
   ┌─────────────────────────────────────┐
   │ api.ts: lexCode("int x = 5;")      │
   │ POST http://localhost:8000/lex    │
   │ Body: { "code": "int x = 5;" }    │
   └─────────────────────────────────────┘
              │
              ▼

3. Backend Processing
   ┌─────────────────────────────────────┐
   │ main.py: lex_code()                 │
   │   └─→ LexicalAnalyzer()             │
   │       └─→ transition("int x = 5;")  │
   │           ├─→ Process 'i'           │
   │           ├─→ Process 'n'           │
   │           ├─→ Process 't'           │
   │           ├─→ Process ' ' (delim)   │
   │           ├─→ Process 'x'           │
   │           ├─→ Process ' ' (delim)   │
   │           ├─→ Process '='           │
   │           ├─→ Process ' ' (delim)   │
   │           ├─→ Process '5'           │
   │           └─→ Process ';'           │
   └─────────────────────────────────────┘
              │
              ▼

4. Backend Response
   ┌─────────────────────────────────────┐
   │ {                                   │
   │   "tokens": [                       │
   │     { tokenName: "int", ... },     │
   │     { tokenName: "x", ... },       │
   │     { tokenName: "=", ... },       │
   │     { tokenName: "5", ... },        │
   │     { tokenName: ";", ... }         │
   │   ],                                │
   │   "errors": []                      │
   │ }                                   │
   └─────────────────────────────────────┘
              │
              ▼

5. Frontend Field Mapping
   ┌─────────────────────────────────────┐
   │ Map backend fields to frontend:     │
   │   tokenType → type                  │
   │   tokenName → lexeme                │
   │   tokenLine → line                  │
   │   tokenCol → column                 │
   └─────────────────────────────────────┘
              │
              ▼

6. State Update
   ┌─────────────────────────────────────┐
   │ setTokens([                        │
   │   { type: "int", lexeme: "int" },  │
   │   { type: "identifier", ... },    │
   │   ...                              │
   │ ])                                 │
   │ setErrors([])                      │
   └─────────────────────────────────────┘
              │
              ▼

7. Visual Rendering
   ┌─────────────────────────────────────┐
   │ Token List:                         │
   │   - int (keyword)                   │
   │   - x (identifier)                  │
   │   - = (operator)                    │
   │   - 5 (number)                      │
   │   - ; (delimiter)                   │
   │                                     │
   │ Syntax Highlighting:                │
   │   int x = 5;                        │
   │   └─┘ └─┘ └─┘ └─┘                  │
   │   violet white cyan amber           │
   └─────────────────────────────────────┘
```

## Component Interaction

### Component Hierarchy

```
App.tsx
  └─→ LexerPanel.tsx
        ├─→ Textarea (code input)
        ├─→ Pre (syntax highlighting overlay)
        ├─→ LineNumbers
        └─→ TokenList.tsx
              └─→ Token rows
```

### Data Flow Through Components

```
┌─────────────────────────────────────────────────────────────┐
│  Component Data Flow                                       │
│                                                             │
│  LexerPanel.tsx                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ State:                                              │  │
│  │   - code: string                                    │  │
│  │   - tokens: SimpleToken[]                           │  │
│  │   - errors: LexError[]                             │  │
│  │                                                     │  │
│  │ Functions:                                          │  │
│  │   - runLexWithCode() → calls lexCode()            │  │
│  │   - buildHighlightsFromTokens()                    │  │
│  │   - handleCodeChange()                             │  │
│  └──────────────────┬──────────────────────────────────┘  │
│                     │                                      │
│       ┌─────────────┼─────────────┐                        │
│       │             │             │                        │
│       ▼             ▼             ▼                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                   │
│  │ Textarea│  │ Pre     │  │TokenList│                   │
│  │         │  │(highlight)│  │         │                   │
│  │ code    │  │ tokens  │  │ tokens  │                   │
│  │         │  │ errors  │  │         │                   │
│  └─────────┘  └─────────┘  └─────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Performance Considerations

### Request Debouncing

The frontend makes a request on every keystroke. For production, consider debouncing:

```typescript
// Example debounced version
const debouncedLexCode = useMemo(
  () => debounce((code: string) => runLexWithCode(code), 300),
  []
);
```

### Response Caching

Consider caching responses for identical code inputs to reduce backend load.

### Error Recovery

The frontend maintains previous tokens/errors until new results arrive, ensuring smooth visual transitions:

```typescript
// Don't clear errors/tokens immediately
// Keep old highlighting until new results arrive
try {
  const resp = await lexCode(sourceCode);
  setTokens(resp.tokens);
  setErrors(resp.errors);
} catch (err) {
  // Handle error
}
```

## Summary

The data flow from lexer backend to frontend follows these steps:

1. **User Input** → Code typed in React textarea
2. **API Call** → HTTP POST to `/lex` endpoint
3. **Backend Processing** → FSA-based lexical analysis
4. **Response** → JSON with tokens and errors
5. **Field Mapping** → Transform backend fields to frontend format
6. **State Update** → Update React state
7. **Visual Rendering** → Display tokens, syntax highlighting, and errors

The entire process happens in real-time as the user types, providing immediate feedback through syntax highlighting and error visualization.

