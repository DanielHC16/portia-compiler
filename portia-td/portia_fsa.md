# PORTIA Language - Complete Finite State Automata

This document contains all FSAs extracted from the PORTIA Transition Diagrams. Each FSA is organized in its own section with state transition tables for manual verification.

---

## Keywords FSA - Part 1

**Keywords**: `bool`, `break`, `case`, `char`, `const`, `default`, `do`, `double`, `else`, `false`, `float`, `for`, `func`  
**State Range**: 0-62  
**Initial State**: 0

### Final States

| State | Keyword | Delimiter Type |
|-------|---------|----------------|
| 5 | `bool` | `whitespace` |
| 10 | `break` | `;` |
| 15 | `case` | `whitespace` |
| 19 | `char` | `whitespace` |
| 24 | `const` | `whitespace` |
| 32 | `default` | `default_delim` |
| 34 | `do` | `block_delim` |
| 39 | `double` | `whitespace` |
| 44 | `else` | `block_delim` |
| 50 | `false` | `nbl_delim` |
| 55 | `float` | `whitespace` |
| 58 | `for` | `loop_delim` |
| 62 | `func` | `whitespace` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 0 | `b` | 1 | Start of `bool` or `break` |
| 0 | `c` | 11 | Start of `case`, `char`, or `const` |
| 0 | `d` | 25 | Start of `default`, `do`, or `double` |
| 0 | `e` | 40 | Start of `else` |
| 0 | `f` | 45 | Start of `false`, `float`, `for`, or `func` |
| 1 | `o` | 2 | Continue `bool` |
| 1 | `r` | 6 | Continue `break` |
| 2 | `o` | 3 | Continue `bool` |
| 3 | `l` | 4 | Continue `bool` |
| 4 | `whitespace` | 5 | **Final: `bool`** |
| 6 | `e` | 7 | Continue `break` |
| 7 | `a` | 8 | Continue `break` |
| 8 | `k` | 9 | Continue `break` |
| 9 | `;` | 10 | **Final: `break`** |
| 11 | `a` | 12 | Continue `case` |
| 11 | `h` | 16 | Continue `char` |
| 11 | `o` | 20 | Continue `const` |
| 12 | `s` | 13 | Continue `case` |
| 13 | `e` | 14 | Continue `case` |
| 14 | `whitespace` | 15 | **Final: `case`** |
| 16 | `a` | 17 | Continue `char` |
| 17 | `r` | 18 | Continue `char` |
| 18 | `whitespace` | 19 | **Final: `char`** |
| 20 | `n` | 21 | Continue `const` |
| 21 | `s` | 22 | Continue `const` |
| 22 | `t` | 23 | Continue `const` |
| 23 | `whitespace` | 24 | **Final: `const`** |
| 25 | `e` | 26 | Continue `default` |
| 25 | `o` | 33 | Continue `do` or `double` |
| 26 | `f` | 27 | Continue `default` |
| 27 | `a` | 28 | Continue `default` |
| 28 | `u` | 29 | Continue `default` |
| 29 | `l` | 30 | Continue `default` |
| 30 | `t` | 31 | Continue `default` |
| 31 | `default_delim` | 32 | **Final: `default`** |
| 33 | `block_delim` | 34 | **Final: `do`** |
| 33 | `u` | 35 | Continue `double` |
| 35 | `b` | 36 | Continue `double` |
| 36 | `l` | 37 | Continue `double` |
| 37 | `e` | 38 | Continue `double` |
| 38 | `whitespace` | 39 | **Final: `double`** |
| 40 | `l` | 41 | Continue `else` |
| 41 | `s` | 42 | Continue `else` |
| 42 | `e` | 43 | Continue `else` |
| 43 | `block_delim` | 44 | **Final: `else`** |
| 45 | `a` | 46 | Continue `false` |
| 45 | `l` | 51 | Continue `float` |
| 45 | `o` | 56 | Continue `for` |
| 45 | `u` | 59 | Continue `func` |
| 46 | `l` | 47 | Continue `false` |
| 47 | `s` | 48 | Continue `false` |
| 48 | `e` | 49 | Continue `false` |
| 49 | `nbl_delim` | 50 | **Final: `false`** |
| 51 | `o` | 52 | Continue `float` |
| 52 | `a` | 53 | Continue `float` |
| 53 | `t` | 54 | Continue `float` |
| 54 | `whitespace` | 55 | **Final: `float`** |
| 56 | `r` | 57 | Continue `for` |
| 57 | `loop_delim` | 58 | **Final: `for`** |
| 59 | `n` | 60 | Continue `func` |
| 60 | `c` | 61 | Continue `func` |
| 61 | `whitespace` | 62 | **Final: `func`** |

---

## Keywords FSA - Part 2

**Keywords**: `using`, `var`, `void`, `weave`, `while`  
**State Range**: 0, 127-151  
**Initial State**: 0

### Final States

| State | Keyword | Delimiter Type |
|-------|---------|----------------|
| 132 | `using` | `whitespace` |
| 136 | `var` | `whitespace` |
| 140 | `void` | `whitespace` |
| 146 | `weave` | `whitespace` |
| 151 | `while` | `loop_delim` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 0 | `u` | 127 | Start of `using` |
| 0 | `v` | 133 | Start of `var` or `void` |
| 0 | `w` | 141 | Start of `weave` or `while` |
| 127 | `s` | 128 | Continue `using` |
| 128 | `i` | 129 | Continue `using` |
| 129 | `n` | 130 | Continue `using` |
| 130 | `g` | 131 | Continue `using` |
| 131 | `whitespace` | 132 | **Final: `using`** |
| 133 | `a` | 134 | Continue `var` |
| 133 | `o` | 137 | Continue `void` |
| 134 | `r` | 135 | Continue `var` |
| 135 | `whitespace` | 136 | **Final: `var`** |
| 137 | `i` | 138 | Continue `void` |
| 138 | `d` | 139 | Continue `void` |
| 139 | `whitespace` | 140 | **Final: `void`** |
| 141 | `e` | 142 | Continue `weave` |
| 141 | `h` | 147 | Continue `while` |
| 142 | `a` | 143 | Continue `weave` |
| 143 | `v` | 144 | Continue `weave` |
| 144 | `e` | 145 | Continue `weave` |
| 145 | `whitespace` | 146 | **Final: `weave`** |
| 147 | `i` | 148 | Continue `while` |
| 148 | `l` | 149 | Continue `while` |
| 149 | `e` | 150 | Continue `while` |
| 150 | `loop_delim` | 151 | **Final: `while`** |

---

## Keywords FSA - Part 3

**Keywords**: `global`, `if`, `int`, `local`, `long`, `main`, `return`, `string`, `switch`, `thread`, `threadln`, `trap`, `true`  
**State Range**: 0-126  
**Initial State**: 0

### Final States

| State | Keyword | Delimiter Type |
|-------|---------|----------------|
| 69 | `global` | `whitespace` |
| 72 | `if` | `loop_delim` |
| 75 | `int` | `whitespace` |
| 81 | `local` | `whitespace` |
| 84 | `long` | `whitespace` |
| 89 | `main` | `(` |
| 96 | `return` | `return_delim` |
| 103 | `string` | `whitespace` |
| 109 | `switch` | `loop_delim` |
| 116 | `thread` | `(` |
| 119 | `threadln` | `(` |
| 123 | `trap` | `(` |
| 126 | `true` | `nbl_delim` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 0 | `g` | 63 | Start of `global` |
| 0 | `i` | 70 | Start of `if` or `int` |
| 0 | `l` | 76 | Start of `local` or `long` |
| 0 | `m` | 85 | Start of `main` |
| 0 | `r` | 90 | Start of `return` |
| 0 | `s` | 97 | Start of `string` or `switch` |
| 0 | `t` | 110 | Start of `thread`, `threadln`, `trap`, or `true` |
| 63 | `l` | 64 | Continue `global` |
| 64 | `o` | 65 | Continue `global` |
| 65 | `b` | 66 | Continue `global` |
| 66 | `a` | 67 | Continue `global` |
| 67 | `l` | 68 | Continue `global` |
| 68 | `whitespace` | 69 | **Final: `global`** |
| 70 | `f` | 71 | Continue `if` |
| 70 | `n` | 73 | Continue `int` |
| 71 | `loop_delim` | 72 | **Final: `if`** |
| 73 | `t` | 74 | Continue `int` |
| 74 | `whitespace` | 75 | **Final: `int`** |
| 76 | `o` | 77 | Continue `local` or `long` |
| 77 | `c` | 78 | Continue `local` |
| 77 | `n` | 82 | Continue `long` |
| 78 | `a` | 79 | Continue `local` |
| 79 | `l` | 80 | Continue `local` |
| 80 | `whitespace` | 81 | **Final: `local`** |
| 82 | `g` | 83 | Continue `long` |
| 83 | `whitespace` | 84 | **Final: `long`** |
| 85 | `a` | 86 | Continue `main` |
| 86 | `i` | 87 | Continue `main` |
| 87 | `n` | 88 | Continue `main` |
| 88 | `(` | 89 | **Final: `main`** |
| 90 | `e` | 91 | Continue `return` |
| 91 | `t` | 92 | Continue `return` |
| 92 | `u` | 93 | Continue `return` |
| 93 | `r` | 94 | Continue `return` |
| 94 | `n` | 95 | Continue `return` |
| 95 | `return_delim` | 96 | **Final: `return`** |
| 97 | `t` | 98 | Continue `string` |
| 97 | `w` | 104 | Continue `switch` |
| 98 | `r` | 99 | Continue `string` |
| 99 | `i` | 100 | Continue `string` |
| 100 | `n` | 101 | Continue `string` |
| 101 | `g` | 102 | Continue `string` |
| 102 | `whitespace` | 103 | **Final: `string`** |
| 104 | `i` | 105 | Continue `switch` |
| 105 | `t` | 106 | Continue `switch` |
| 106 | `c` | 107 | Continue `switch` |
| 107 | `h` | 108 | Continue `switch` |
| 108 | `loop_delim` | 109 | **Final: `switch`** |
| 110 | `h` | 111 | Continue `thread` or `threadln` |
| 110 | `r` | 120 | Continue `trap` or `true` |
| 111 | `r` | 112 | Continue `thread` or `threadln` |
| 112 | `e` | 113 | Continue `thread` or `threadln` |
| 113 | `a` | 114 | Continue `thread` or `threadln` |
| 114 | `d` | 115 | Continue `thread` or `threadln` |
| 115 | `(` | 116 | **Final: `thread`** |
| 115 | `l` | 117 | Continue `threadln` |
| 117 | `n` | 118 | Continue `threadln` |
| 118 | `(` | 119 | **Final: `threadln`** |
| 120 | `a` | 121 | Continue `trap` |
| 120 | `u` | 124 | Continue `true` |
| 121 | `p` | 122 | Continue `trap` |
| 122 | `(` | 123 | **Final: `trap`** |
| 124 | `e` | 125 | Continue `true` |
| 125 | `nbl_delim` | 126 | **Final: `true`** |

---

## Symbols FSA - Part 1 (Operators)

**Symbols**: `-`, `--`, `-=`, `+`, `++`, `+=`, `*`, `*=`, `/`, `/=`, `%`, `%=`, `&&`, `||`, `!`, `!=`, `=`, `==`  
**State Range**: 0-189  
**Initial State**: 0

### Final States

| State | Symbol | Delimiter Type |
|-------|--------|----------------|
| 153 | `-` | `negative_delim` |
| 155 | `--` | `decrement_delim` |
| 157 | `-=` | `sign_delim` |
| 159 | `+` | `sign_delim` |
| 161 | `++` | `increment_delim` |
| 163 | `+=` | `sign_delim` |
| 165 | `*` | `marithmetic_delim` |
| 167 | `*=` | `sign_delim` |
| 169 | `/` | `slash_delim` |
| 171 | `/=` | `sign_delim` |
| 173 | `%` | `modulo_delim` |
| 175 | `%=` | `sign_delim` |
| 178 | `&&` | `logical_delim` |
| 181 | `||` | `logical_delim` |
| 183 | `!` | `exclamation_delim` |
| 185 | `!=` | `sign_delim` |
| 187 | `=` | `equal_delim` |
| 189 | `==` | `sign_delim` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 0 | `-` | 152 | Start of `-`, `--`, or `-=` |
| 0 | `+` | 158 | Start of `+`, `++`, or `+=` |
| 0 | `*` | 164 | Start of `*` or `*=` |
| 0 | `/` | 168 | Start of `/` or `/=` |
| 0 | `%` | 172 | Start of `%` or `%=` |
| 0 | `&` | 176 | Start of `&&` |
| 0 | `\|` | 179 | Start of `\|\|` |
| 0 | `!` | 182 | Start of `!` or `!=` |
| 0 | `=` | 186 | Start of `=` or `==` |
| 152 | `negative_delim` | 153 | **Final: `-`** |
| 152 | `-` | 154 | Continue `--` |
| 152 | `=` | 156 | Continue `-=` |
| 154 | `decrement_delim` | 155 | **Final: `--`** |
| 156 | `sign_delim` | 157 | **Final: `-=`** |
| 158 | `sign_delim` | 159 | **Final: `+`** |
| 158 | `+` | 160 | Continue `++` |
| 158 | `=` | 162 | Continue `+=` |
| 160 | `increment_delim` | 161 | **Final: `++`** |
| 162 | `sign_delim` | 163 | **Final: `+=`** |
| 164 | `marithmetic_delim` | 165 | **Final: `*`** |
| 164 | `=` | 166 | Continue `*=` |
| 166 | `sign_delim` | 167 | **Final: `*=`** |
| 168 | `slash_delim` | 169 | **Final: `/`** |
| 168 | `=` | 170 | Continue `/=` |
| 170 | `sign_delim` | 171 | **Final: `/=`** |
| 172 | `modulo_delim` | 173 | **Final: `%`** |
| 172 | `=` | 174 | Continue `%=` |
| 174 | `sign_delim` | 175 | **Final: `%=`** |
| 176 | `&` | 177 | Continue `&&` |
| 177 | `logical_delim` | 178 | **Final: `&&`** |
| 179 | `\|` | 180 | Continue `\|\|` |
| 180 | `logical_delim` | 181 | **Final: `\|\|`** |
| 182 | `exclamation_delim` | 183 | **Final: `!`** |
| 182 | `=` | 184 | Continue `!=` |
| 184 | `sign_delim` | 185 | **Final: `!=`** |
| 186 | `equal_delim` | 187 | **Final: `=`** |
| 186 | `=` | 188 | Continue `==` |
| 188 | `sign_delim` | 189 | **Final: `==`** |

**Note**: Delimiter types determine when a symbol token is complete. The lexer checks if the next character matches the delimiter type before accepting the symbol.

---

## Symbols FSA - Part 2 (Delimiters)

**Symbols**: `<`, `<=`, `>`, `>=`, `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`, `.`, `..`, `:`  
**State Range**: 0, 190-219  
**Initial State**: 0

### Final States

| State | Symbol | Delimiter Type |
|-------|--------|----------------|
| 191 | `<` | `asign_delim` |
| 193 | `<=` | `asign_delim` |
| 195 | `>` | `asign_delim` |
| 197 | `>=` | `asign_delim` |
| 199 | `(` | `open_paren_delim` |
| 201 | `)` | `closing_delim` |
| 203 | `{` | `open_curly_delim` |
| 205 | `}` | `close_curly_delim` |
| 207 | `[` | `open_bracket_delim` |
| 209 | `]` | `iden_delim` |
| 211 | `;` | `semicolon_delim` |
| 213 | `,` | `comma_delim` |
| 215 | `.` | `alphanum` |
| 217 | `..` | `concat_delim` |
| 219 | `:` | `newline` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 0 | `<` | 190 | Start of `<` or `<=` |
| 0 | `>` | 194 | Start of `>` or `>=` |
| 0 | `(` | 198 | Start of `(` |
| 0 | `)` | 200 | Start of `)` |
| 0 | `{` | 202 | Start of `{` |
| 0 | `}` | 204 | Start of `}` |
| 0 | `[` | 206 | Start of `[` |
| 0 | `]` | 208 | Start of `]` |
| 0 | `;` | 210 | Start of `;` |
| 0 | `,` | 212 | Start of `,` |
| 0 | `.` | 214 | Start of `.` or `..` |
| 0 | `:` | 218 | Start of `:` |
| 190 | `asign_delim` | 191 | **Final: `<`** |
| 190 | `=` | 192 | Continue `<=` |
| 192 | `asign_delim` | 193 | **Final: `<=`** |
| 194 | `asign_delim` | 195 | **Final: `>`** |
| 194 | `=` | 196 | Continue `>=` |
| 196 | `asign_delim` | 197 | **Final: `>=`** |
| 198 | `open_paren_delim` | 199 | **Final: `(`** |
| 200 | `closing_delim` | 201 | **Final: `)`** |
| 202 | `open_curly_delim` | 203 | **Final: `{`** |
| 204 | `close_curly_delim` | 205 | **Final: `}`** |
| 206 | `open_bracket_delim` | 207 | **Final: `[`** |
| 208 | `iden_delim` | 209 | **Final: `]`** |
| 210 | `semicolon_delim` | 211 | **Final: `;`** |
| 212 | `comma_delim` | 213 | **Final: `,`** |
| 214 | `alphanum` | 215 | **Final: `.`** |
| 214 | `.` | 216 | Continue `..` |
| 216 | `concat_delim` | 217 | **Final: `..`** |
| 218 | `newline` | 219 | **Final: `:`** |

---

## Comments FSA

**Comment Types**: Single-line (`// ... newline`), Multi-line (`/* ... */`)  
**State Range**: 168, 271-276  
**Initial State**: 168

### Final States

| State | Comment Type | Delimiter Type |
|-------|--------------|----------------|
| 272 | `single_line` | `single_line_comment` |
| 276 | `multi_line` | `multi_line_comment` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 168 | `/` | 271 | Start of comment |
| 271 | `ascii` | 271 | Self-loop (any ASCII except newline or `*`) |
| 271 | `lambda` | 271 | Self-loop (any other char except newline or `*`) |
| 271 | `newline` | 272 | **Final: Single-line comment** |
| 271 | `*` | 273 | Start multi-line comment |
| 273 | `ascii` | 273 | Self-loop (any ASCII except `*`) |
| 273 | `\n` | 273 | Self-loop (newline allowed in multi-line) |
| 273 | `lambda` | 273 | Self-loop (any other char except `*`) |
| 273 | `*` | 274 | Potential end sequence |
| 274 | `*` | 273 | Handle `***` pattern (back to comment body) |
| 274 | `/` | 275 | Complete `*/` sequence |
| 275 | `multi_delim` | 276 | **Final: Multi-line comment** |

---

## String Literals FSA

**String Literals**: `" ... "`  
**State Range**: 0, 277-278  
**Initial State**: 0

### Final States

| State | Literal Type | Delimiter Type |
|-------|--------------|----------------|
| 278 | `string` | `string_literal` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 0 | `"` | 277 | Opening quote |
| 277 | `ascii` | 277 | Self-loop (any ASCII character) |
| 277 | `whitespace` | 277 | Self-loop (space, tab, newline, etc.) |
| 277 | `escape_seq` | 277 | Self-loop (valid escape sequences) |
| 277 | `"` | 277 | Self-loop (escaped quote or content) |
| 277 | `lambda` | 277 | Self-loop (any other character) |
| 277 | `str_lit_delim` | 278 | **Final: String literal** (unescaped closing quote) |

---

## Integer Literals FSA

**Integer Literals**: Sequences of digits  
**State Range**: 0, 279-298 (states: 0, 279-298)  
**Initial State**: 0  
**Accepts**: 1-10 digits (states 280, 282, 284, 286, 288, 290, 292, 294, 296, 298 are final states for 1-10 digits respectively)

### Final States

| State | Literal Type | Delimiter Type |
|-------|--------------|----------------|
| 280 | `int` | `int_literal` |
| 282 | `int` | `int_literal` |
| 284 | `int` | `int_literal` |
| 286 | `int` | `int_literal` |
| 288 | `int` | `int_literal` |
| 290 | `int` | `int_literal` |
| 292 | `int` | `int_literal` |
| 294 | `int` | `int_literal` |
| 296 | `int` | `int_literal` |
| 298 | `int` | `int_literal` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 0 | `numbers` | 279 | Start of integer literal |
| 279 | `nbl_delim` | 280 | **Final: int** |
| 279 | `numbers` | 281 | Continue |
| 281 | `nbl_delim` | 282 | **Final: int** |
| 281 | `numbers` | 283 | Continue |
| 283 | `nbl_delim` | 284 | **Final: int** |
| 283 | `numbers` | 285 | Continue |
| 285 | `nbl_delim` | 286 | **Final: int** |
| 285 | `numbers` | 287 | Continue |
| 287 | `nbl_delim` | 288 | **Final: int** |
| 287 | `numbers` | 289 | Continue |
| 289 | `nbl_delim` | 290 | **Final: int** |
| 289 | `numbers` | 291 | Continue |
| 291 | `nbl_delim` | 292 | **Final: int** |
| 291 | `numbers` | 293 | Continue |
| 293 | `nbl_delim` | 294 | **Final: int** |
| 293 | `numbers` | 295 | Continue |
| 295 | `nbl_delim` | 296 | **Final: int** |
| 295 | `numbers` | 297 | Continue (may connect to Long FSA) |
| 297 | `nbl_delim` | 298 | **Final: int** |

---

## Long Literals FSA

**Long Literals**: Extended sequences of digits, optionally with decimal points and fractional parts  
**State Range**: 297-336 (states: 297, 299-336, including intermediate decimal states 300, 302, 304, 306, 308, 310, 312)  
**Initial State**: 297 (connects from Integer FSA)  
**Accepts**: 11-29 digits (continues from Integer's 10 digits; states 300, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322, 324, 326, 328, 330, 332, 334, 336 are final states)

### Final States

| State | Literal Type | Delimiter Type |
|-------|--------------|----------------|
| 300 | `long` | `long_literal` |
| 302 | `long` | `long_literal` |
| 304 | `long` | `long_literal` |
| 306 | `long` | `long_literal` |
| 308 | `long` | `long_literal` |
| 310 | `long` | `long_literal` |
| 312 | `long` | `long_literal` |
| 314 | `long` | `long_literal` |
| 316 | `long` | `long_literal` |
| 318 | `long` | `long_literal` |
| 320 | `long` | `long_literal` |
| 322 | `long` | `long_literal` |
| 324 | `long` | `long_literal` |
| 326 | `long` | `long_literal` |
| 328 | `long` | `long_literal` |
| 330 | `long` | `long_literal` |
| 332 | `long` | `long_literal` |
| 334 | `long` | `long_literal` |
| 336 | `long` | `long_literal` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 297 | `numbers` | 299 | Start of long literal |
| 299 | `numbers` | 301 | Continue |
| 299 | `.` | 300 | **Final: long** (via decimal point path) |
| 301 | `numbers` | 303 | Continue |
| 301 | `.` | 302 | **Final: long** (via decimal point path) |
| 303 | `numbers` | 305 | Continue |
| 303 | `.` | 304 | **Final: long** (via decimal point path) |
| 305 | `numbers` | 307 | Continue |
| 305 | `.` | 306 | **Final: long** (via decimal point path) |
| 307 | `numbers` | 309 | Continue |
| 307 | `.` | 308 | **Final: long** (via decimal point path) |
| 309 | `numbers` | 311 | Continue |
| 309 | `.` | 310 | **Final: long** (via decimal point path) |
| 311 | `numbers` | 313 | Continue |
| 311 | `.` | 312 | **Final: long** (via decimal point path) |
| 313 | `numbers` | 315 | Continue |
| 313 | `.` | 314 | **Final: long** (via decimal point path) |
| 313 | `nbl_delim` | 330 | **Final: long** |
| 315 | `numbers` | 317 | Continue |
| 315 | `nbl_delim` | 316 | **Final: long** |
| 317 | `numbers` | 319 | Continue |
| 317 | `nbl_delim` | 318 | **Final: long** |
| 319 | `numbers` | 321 | Continue |
| 319 | `nbl_delim` | 320 | **Final: long** |
| 321 | `numbers` | 323 | Continue |
| 321 | `nbl_delim` | 322 | **Final: long** |
| 323 | `numbers` | 325 | Continue |
| 323 | `nbl_delim` | 324 | **Final: long** |
| 325 | `numbers` | 327 | Continue |
| 325 | `nbl_delim` | 326 | **Final: long** |
| 327 | `numbers` | 329 | Continue |
| 327 | `nbl_delim` | 328 | **Final: long** |
| 329 | `numbers` | 331 | Continue |
| 329 | `nbl_delim` | 330 | **Final: long** |
| 331 | `numbers` | 333 | Continue |
| 331 | `nbl_delim` | 332 | **Final: long** |
| 333 | `numbers` | 335 | Continue |
| 333 | `nbl_delim` | 334 | **Final: long** |
| 335 | `nbl_delim` | 336 | **Final: long** |

**Note**: Decimal point paths (299→300, 301→302, etc.) go through intermediate states that handle fractional parts.

---

## Float Literals FSA

**Float Literals**: Sequences of digits for float precision  
**State Range**: 337-351 (states: 337-351)  
**Initial State**: 337  
**Accepts**: 1-7 digits (states 339, 341, 343, 345, 347, 349, 351 are final states for 1-7 digits respectively)

### Final States

| State | Literal Type | Delimiter Type |
|-------|--------------|----------------|
| 339 | `float` | `float_literal` |
| 341 | `float` | `float_literal` |
| 343 | `float` | `float_literal` |
| 345 | `float` | `float_literal` |
| 347 | `float` | `float_literal` |
| 349 | `float` | `float_literal` |
| 351 | `float` | `float_literal` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 337 | `numbers` | 338 | Start of float literal |
| 338 | `nbl_delim` | 339 | **Final: float** |
| 338 | `numbers` | 340 | Continue |
| 340 | `nbl_delim` | 341 | **Final: float** |
| 340 | `numbers` | 342 | Continue |
| 342 | `nbl_delim` | 343 | **Final: float** |
| 342 | `numbers` | 344 | Continue |
| 344 | `nbl_delim` | 345 | **Final: float** |
| 344 | `numbers` | 346 | Continue |
| 346 | `nbl_delim` | 347 | **Final: float** |
| 346 | `numbers` | 348 | Continue |
| 348 | `nbl_delim` | 349 | **Final: float** |
| 348 | `numbers` | 350 | Continue (may connect to Double FSA) |
| 350 | `nbl_delim` | 351 | **Final: float** |

---

## Double Literals FSA

**Double Literals**: Extended sequences of digits for double precision  
**State Range**: 350-367 (states: 350, 352-367)  
**Initial State**: 350 (may connect from Float FSA)  
**Accepts**: 1-8 digits (continues from Float's 7 digits; states 353, 355, 357, 359, 361, 363, 365, 367 are final states for 1-8 additional digits respectively)

### Final States

| State | Literal Type | Delimiter Type |
|-------|--------------|----------------|
| 353 | `double` | `double_literal` |
| 355 | `double` | `double_literal` |
| 357 | `double` | `double_literal` |
| 359 | `double` | `double_literal` |
| 361 | `double` | `double_literal` |
| 363 | `double` | `double_literal` |
| 365 | `double` | `double_literal` |
| 367 | `double` | `double_literal` |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 350 | `numbers` | 352 | Start of double literal |
| 352 | `nbl_delim` | 353 | **Final: double** |
| 352 | `numbers` | 354 | Continue |
| 354 | `nbl_delim` | 355 | **Final: double** |
| 354 | `numbers` | 356 | Continue |
| 356 | `nbl_delim` | 357 | **Final: double** |
| 356 | `numbers` | 358 | Continue |
| 358 | `nbl_delim` | 359 | **Final: double** |
| 358 | `numbers` | 360 | Continue |
| 360 | `nbl_delim` | 361 | **Final: double** |
| 360 | `numbers` | 362 | Continue |
| 362 | `nbl_delim` | 363 | **Final: double** |
| 362 | `numbers` | 364 | Continue |
| 364 | `nbl_delim` | 365 | **Final: double** |
| 364 | `numbers` | 366 | Continue |
| 366 | `nbl_delim` | 367 | **Final: double** |

---

## Identifier Literals FSA

**Identifier Literals**: Sequences of letters, digits, and underscores for variable/function names  
**State Range**: 0, 220-270 (states: 0, 220-270)  
**Initial State**: 0  
**Accepts**: 1-25 characters (maximum 25 characters; first character must be alphabetic, subsequent characters can be alphanumeric or underscore)

### Final States

| State | Literal Type | Delimiter Type | Length(s) Accepted |
|-------|--------------|----------------|-------------------|
| 221 | `identifier` | `iden_delim` | 1 character |
| 223 | `identifier` | `iden_delim` | 2 characters |
| 225 | `identifier` | `iden_delim` | 3 characters |
| 227 | `identifier` | `iden_delim` | 4 characters |
| 229 | `identifier` | `iden_delim` | 5 characters |
| 231 | `identifier` | `iden_delim` | 6-7 characters |
| 233 | `identifier` | `iden_delim` | 8 characters |
| 235 | `identifier` | `iden_delim` | 9 characters |
| 237 | `identifier` | `iden_delim` | 10 characters |
| 239 | `identifier` | `iden_delim` | 11 characters |
| 241 | `identifier` | `iden_delim` | 12-13 characters |
| 243 | `identifier` | `iden_delim` | 14 characters |
| 245 | `identifier` | `iden_delim` | 15 characters |
| 247 | `identifier` | `iden_delim` | 16 characters |
| 249 | `identifier` | `iden_delim` | 17 characters |
| 251 | `identifier` | `iden_delim` | 18-19 characters |
| 254 | `identifier` | `iden_delim` | 20 characters |
| 256 | `identifier` | `iden_delim` | 21 characters |
| 258 | `identifier` | `iden_delim` | 22 characters |
| 260 | `identifier` | `iden_delim` | 23 characters |
| 262 | `identifier` | `iden_delim` | 24-25 characters (maximum) |

### State Transitions

| From State | Input | To State | Notes |
|------------|-------|----------|-------|
| 0 | `alphabetics` | 220 | Start of identifier (first character must be alphabetic) |
| 220 | `iden_delim` | 221 | **Final: identifier** (1 character) |
| 220 | `alphanum/_` | 222 | Continue identifier |
| 222 | `iden_delim` | 223 | **Final: identifier** (2 characters) |
| 222 | `alphanum/_` | 224 | Continue identifier |
| 224 | `iden_delim` | 225 | **Final: identifier** (3 characters) |
| 224 | `alphanum/_` | 226 | Continue identifier |
| 226 | `iden_delim` | 227 | **Final: identifier** (4 characters) |
| 226 | `alphanum/_` | 228 | Continue identifier |
| 228 | `iden_delim` | 229 | **Final: identifier** (5 characters) |
| 228 | `alphanum/_` | 229 | Continue identifier |
| 229 | `iden_delim` | 231 | **Final: identifier** (6 characters) |
| 229 | `alphanum/_` | 230 | Continue identifier |
| 230 | `iden_delim` | 231 | **Final: identifier** (7 characters) |
| 230 | `alphanum/_` | 232 | Continue identifier |
| 232 | `iden_delim` | 233 | **Final: identifier** (8 characters) |
| 232 | `alphanum/_` | 234 | Continue identifier |
| 234 | `iden_delim` | 235 | **Final: identifier** (9 characters) |
| 234 | `alphanum/_` | 236 | Continue identifier |
| 236 | `iden_delim` | 237 | **Final: identifier** (10 characters) |
| 236 | `alphanum/_` | 238 | Continue identifier |
| 238 | `iden_delim` | 239 | **Final: identifier** (11 characters) |
| 238 | `alphanum/_` | 239 | Continue identifier |
| 239 | `iden_delim` | 241 | **Final: identifier** (12 characters) |
| 239 | `alphanum/_` | 240 | Continue identifier |
| 240 | `iden_delim` | 241 | **Final: identifier** (13 characters) |
| 240 | `alphanum/_` | 242 | Continue identifier |
| 242 | `iden_delim` | 243 | **Final: identifier** (14 characters) |
| 242 | `alphanum/_` | 244 | Continue identifier |
| 244 | `iden_delim` | 245 | **Final: identifier** (15 characters) |
| 244 | `alphanum/_` | 246 | Continue identifier |
| 246 | `iden_delim` | 247 | **Final: identifier** (16 characters) |
| 246 | `alphanum/_` | 248 | Continue identifier |
| 248 | `iden_delim` | 249 | **Final: identifier** (17 characters) |
| 248 | `alphanum/_` | 249 | Continue identifier |
| 249 | `iden_delim` | 251 | **Final: identifier** (18 characters) |
| 249 | `alphanum/_` | 250 | Continue identifier |
| 250 | `iden_delim` | 251 | **Final: identifier** (19 characters) |
| 250 | `alphanum/_` | 253 | Continue identifier |
| 253 | `iden_delim` | 254 | **Final: identifier** (20 characters) |
| 253 | `alphanum/_` | 255 | Continue identifier |
| 255 | `iden_delim` | 256 | **Final: identifier** (21 characters) |
| 255 | `alphanum/_` | 257 | Continue identifier |
| 257 | `iden_delim` | 258 | **Final: identifier** (22 characters) |
| 257 | `alphanum/_` | 259 | Continue identifier |
| 259 | `iden_delim` | 260 | **Final: identifier** (23 characters) |
| 259 | `alphanum/_` | 260 | Continue identifier |
| 260 | `iden_delim` | 262 | **Final: identifier** (24 characters) |
| 260 | `alphanum/_` | 261 | Continue identifier |
| 261 | `iden_delim` | 262 | **Final: identifier** (25 characters - maximum length) |

---

## FSA Connection Points

The FSAs are connected at specific states:

- **Integer → Long**: State 297 connects integer FSA to long FSA
- **Float → Double**: State 350 connects float FSA to double FSA

**Note**: Identifier FSA starts independently at state 0 and does not connect to numerical literal FSAs. The lexer determines which FSA to use based on the first character encountered (alphabetic for identifiers, digit for numerical literals).
