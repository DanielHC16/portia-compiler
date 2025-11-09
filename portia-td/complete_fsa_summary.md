# PORTIA Transition Diagram - Complete FSA Summary

This document provides a complete overview of all FSAs extracted from the PORTIA Transition Diagrams.

## Overview

The PORTIA lexical analyzer is composed of multiple FSAs:

### Keywords FSAs
1. **Keywords Part 1** (`keywords1_fsa`): States 0-62
2. **Keywords Part 2** (`keywords2_fsa`): States 0, 127-151
3. **Keywords Part 3** (`keywords3_fsa`): States 0-126

### Symbols FSAs
4. **Symbols Part 1** (`symbols1_fsa`): States 0-189 (Operators)
5. **Symbols Part 2** (`symbols2_fsa`): States 0, 190-219 (Delimiters)

### Literals and Comments FSAs
6. **Comments** (`comments_fsa`): States 168, 271-276 (Single-line and multi-line comments)
7. **String Literals** (`strings_fsa`): States 0, 277-278 (String literals)
8. **Integer Literals** (`numlit_int_fsa`): States 0, 279-298 (Integer literals)
9. **Long Literals** (`numlit_long_fsa`): States 297-336 (Long numerical literals)
10. **Float Literals** (`numlit_float_fsa`): States 337-351 (Float literals)
11. **Double Literals** (`numlit_double_fsa`): States 350-367 (Double literals)
12. **Numerical Continuation** (`numlit_continuation_fsa`): States 366-383 (Extended numerical literals)

**Note**: Most FSAs share state 0 as the initial state, suggesting they may be combined or used in parallel. Comments FSA starts at state 168.

## Complete Keyword List (31 keywords)

### Part 1 Keywords (13 keywords)
- `bool`, `break`, `case`, `char`, `const`, `default`, `do`, `double`, `else`, `false`, `float`, `for`, `func`

### Part 2 Keywords (5 keywords)
- `using`, `var`, `void`, `weave`, `while`

### Part 3 Keywords (13 keywords)
- `global`, `if`, `int`, `local`, `long`, `main`, `return`, `string`, `switch`, `thread`, `threadln`, `trap`, `true`

## Complete Symbols List (33 symbols)

### Part 1 Symbols - Operators (18 symbols)
- Arithmetic: `-`, `--`, `-=`, `+`, `++`, `+=`, `*`, `*=`, `/`, `/=`, `%`, `%=`
- Logical: `&&`, `||`, `!`, `!=`
- Assignment/Comparison: `=`, `==`

### Part 2 Symbols - Delimiters (15 symbols)
- Comparison: `<`, `<=`, `>`, `>=`
- Grouping: `(`, `)`, `{`, `}`, `[`, `]`
- Punctuation: `;`, `,`, `.`, `..`, `:`

## Delimiter Types Summary

### Keyword Delimiters
| Delimiter Type | Used By Keywords | Description |
|----------------|------------------|-------------|
| `whitespace` | bool, case, char, const, double, float, func, using, var, void, weave, global, int, local, long, string | Space, tab, or newline characters |
| `loop_delim` | for, while, if, switch | Loop delimiter (likely `(` or whitespace) |
| `block_delim` | do, else | Block delimiter (likely `{` or whitespace) |
| `nbl_delim` | false, true | Non-block literal delimiter |
| `default_delim` | default | Default delimiter |
| `return_delim` | return | Return delimiter |
| `;` | break | Semicolon |
| `(` | main, thread, threadln, trap | Opening parenthesis |

### Symbol Delimiters
| Delimiter Type | Symbols | Description |
|----------------|---------|-------------|
| `negative_delim` | `-` | Negative/unary minus operator |
| `decrement_delim` | `--` | Decrement operator |
| `sign_delim` | `-=`, `+=`, `*=`, `/=`, `%=`, `!=`, `==`, `<=`, `>=` | Assignment or comparison operator |
| `marithmetic_delim` | `*` | Multiplication operator |
| `slash_delim` | `/` | Division operator |
| `modulo_delim` | `%` | Modulo operator |
| `logical_delim` | `&&`, `||` | Logical operator |
| `exclamation_delim` | `!` | Logical NOT operator |
| `equal_delim` | `=` | Assignment operator |
| `asign_delim` | `<`, `<=`, `>`, `>=` | Assignment or comparison delimiter |
| `open_paren_delim` | `(` | Opening parenthesis delimiter |
| `closing_delim` | `)` | Closing parenthesis delimiter |
| `open_curly_delim` | `{` | Opening curly brace delimiter |
| `close_curly_delim` | `}` | Closing curly brace delimiter |
| `open_bracket_delim` | `[` | Opening bracket delimiter |
| `iden_delim` | `]` | Identifier delimiter (closing bracket) |
| `semicolon_delim` | `;` | Semicolon delimiter |
| `comma_delim` | `,` | Comma delimiter |
| `alphanum` | `.` | Alphanumeric delimiter (dot) |
| `concat_delim` | `..` | Concatenation operator |
| `newline` | `:` | Newline delimiter (colon) |

## State Ranges

### Keywords
- **Part 1**: States 0-62 (63 states)
- **Part 2**: States 0, 127-151 (25 states, note the gap)
- **Part 3**: States 0-126 (127 states)

### Symbols
- **Part 1**: States 0-189 (190 states)
- **Part 2**: States 0, 190-219 (220 states)

### Literals and Comments
- **Comments**: States 168, 271-276 (7 states)
- **String Literals**: States 0, 277-278 (3 states)
- **Integer Literals**: States 0, 279-298 (20 states)
- **Long Literals**: States 297-336 (40 states)
- **Float Literals**: States 337-351 (15 states)
- **Double Literals**: States 350-367 (18 states)
- **Numerical Continuation**: States 366-383 (18 states)

## Final States Summary

### Keywords Part 1 Final States
5, 10, 15, 19, 24, 32, 34, 39, 44, 50, 55, 58, 62

### Keywords Part 2 Final States
132, 136, 140, 146, 151

### Keywords Part 3 Final States
69, 72, 75, 81, 84, 89, 96, 103, 109, 116, 119, 123, 126

### Symbols Part 1 Final States
153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 178, 181, 183, 185, 187, 189

### Symbols Part 2 Final States
191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 219

## Files Created

### Keywords Part 1
- `keywords1_fsa.json` - JSON representation
- `keywords1_fsa.py` - Python module with helper functions
- `keywords1_fsa.md` - Detailed documentation

### Keywords Part 2
- `keywords2_fsa.json` - JSON representation
- `keywords2_fsa.py` - Python module with helper functions
- `keywords2_fsa.md` - Detailed documentation

### Keywords Part 3
- `keywords3_fsa.json` - JSON representation
- `keywords3_fsa.py` - Python module with helper functions
- `keywords3_fsa.md` - Detailed documentation

### Symbols Part 1
- `symbols1_fsa.json` - JSON representation
- `symbols1_fsa.py` - Python module with helper functions
- `symbols1_fsa.md` - Detailed documentation

### Symbols Part 2
- `symbols2_fsa.json` - JSON representation
- `symbols2_fsa.py` - Python module with helper functions
- `symbols2_fsa.md` - Detailed documentation

### Comments
- `comments_fsa.json` - JSON representation
- `comments_fsa.py` - Python module with helper functions
- `comments_fsa.md` - Detailed documentation

### String Literals
- `strings_fsa.json` - JSON representation
- `strings_fsa.py` - Python module with helper functions
- `strings_fsa.md` - Detailed documentation

### Integer Literals
- `numlit_int_fsa.json` - JSON representation
- `numlit_int_fsa.py` - Python module with helper functions
- `numlit_int_fsa.md` - Detailed documentation

### Long Literals
- `numlit_long_fsa.json` - JSON representation
- `numlit_long_fsa.py` - Python module with helper functions
- `numlit_long_fsa.md` - Detailed documentation

### Float Literals
- `numlit_float_fsa.json` - JSON representation
- `numlit_float_fsa.py` - Python module with helper functions
- `numlit_float_fsa.md` - Detailed documentation

### Double Literals
- `numlit_double_fsa.json` - JSON representation
- `numlit_double_fsa.py` - Python module with helper functions
- `numlit_double_fsa.md` - Detailed documentation

### Numerical Continuation
- `numlit_continuation_fsa.json` - JSON representation
- `numlit_continuation_fsa.py` - Python module with helper functions
- `numlit_continuation_fsa.md` - Detailed documentation

## Usage Notes

Each Python module provides:

- `FINAL_STATES` - Dictionary mapping final states to (token, delimiter_type) tuples
- `TRANSITIONS` - Dictionary mapping states to their character transitions
- `KEYWORDS` or `SYMBOLS` - List of all tokens recognized by the FSA
- `recognize_keyword(input_string)` or `recognize_symbol(input_string)` - Function to simulate token recognition
- `is_final_state(state)` - Check if a state is final
- `get_keyword_from_state(state)` or `get_symbol_from_state(state)` - Get token from final state
- `get_delimiter_from_state(state)` - Get delimiter type from final state
- `get_next_state(current_state, char)` - Get next state given current state and character

## Integration Considerations

When integrating these FSAs into a lexer:

1. **State Management**: All FSAs start from state 0, so you'll need to track which FSA is active or combine them into a single unified FSA.

2. **Delimiter Validation**: After recognizing a keyword or symbol, validate that the next character matches the expected delimiter type for that token.

3. **State Numbering**: The state numbers suggest these may be part of a larger system. Note the gaps and overlaps:
   - Keywords Part 2 uses states 127-151 (gap after Part 1's 0-62)
   - Keywords Part 3 uses states 0-126 (overlaps with Part 2's range)
   - Symbols Part 1 uses states 0-189 (overlaps with all keyword ranges)
   - Symbols Part 2 uses states 190-219 (continues from Symbols Part 1)

4. **Combined FSA**: You may want to create a unified FSA that combines all parts, ensuring no state number conflicts and maintaining the transition logic. This would require:
   - Renumbering states to avoid conflicts
   - Merging initial state transitions
   - Handling delimiter validation consistently

5. **Epsilon Transitions**: Symbols Part 1 uses epsilon (empty string) transitions for immediate acceptance. These need special handling in the lexer implementation.

6. **Delimiter Transitions**: Some transitions use delimiter types (like `asign_delim`, `open_paren_delim`) rather than characters. These represent validation steps that need to check the next character matches the delimiter set.

## Literals and Comments Summary

### Comments
- **Single-line comments**: `// ... newline`
- **Multi-line comments**: `/* ... */`
- Final states: 272 (single-line), 276 (multi-line)

### String Literals
- **String literals**: `" ... "`
- Supports escape sequences: `\n`, `\t`, `\"`, `\'`, `\\`
- Final state: 278

### Integer Literals
- **Integer literals**: Sequences of digits
- Final states: 280, 282, 284, 286, 288, 290, 292, 294, 296, 298
- Supports integers of varying lengths

### Long Literals
- **Long literals**: Extended sequences of digits, optionally with decimal points and fractional parts
- Final states: 300, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322, 324, 326, 328, 330, 332, 334, 336
- Connects from integer FSA at state 297
- Supports very long numerical sequences with optional decimal notation

### Float Literals
- **Float literals**: Sequences of digits for float precision
- Final states: 339, 341, 343, 345, 347, 349, 351
- Initial state: 337
- State 350 may connect to Double FSA

### Double Literals
- **Double literals**: Extended sequences of digits for double precision
- Final states: 353, 355, 357, 359, 361, 363, 365, 367
- Initial state: 350 (may connect from Float FSA)
- State 366 may connect to continuation FSA

### Numerical Continuation
- **Continuation literals**: Extended numerical sequences beyond double precision
- Final states: 369, 371, 373, 375, 377, 379, 381, 383
- Initial state: 366 (may connect from Double FSA)
- Supports very long numerical sequences

## Next Steps

Additional FSAs may exist for:
- Identifiers
- Character literals
- Whitespace

These would complete the full lexical analyzer for the PORTIA language.

## FSA Connection Points

The FSAs are connected at specific states:
- **Integer → Long**: State 297 connects integer FSA to long FSA
- **Float → Double**: State 350 connects float FSA to double FSA
- **Double → Continuation**: State 366 connects double FSA to continuation FSA

These connections allow the lexer to transition between different numerical literal types based on the length and precision requirements.

