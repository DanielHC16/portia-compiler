#!/usr/bin/env python3
"""
Debug test to see what states identifiers transition through
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from lexer.portia_lexer import LexicalAnalyzer

# Simple test: single identifier followed by newline
code = "abc\ndef"

print("Input:", repr(code))
print("Display:")
print(code)
print()

lexer = LexicalAnalyzer()

# Manually trace transitions
state = 's0'
lexeme = ''

for i, ch in enumerate(code):
    next_state = lexer.lex_transition(state, ch)
    print(f"Char {i}: {repr(ch):5s} | State: {state:5s} → {next_state:10s} | Lexeme so far: {repr(lexeme + ch)}")
    
    if next_state not in ['UNDEFINED', 'DEFINED']:
        lexeme += ch
        state = next_state
    elif next_state == 'DEFINED':
        print(f"         → FINAL STATE REACHED")
        break
    else:
        print(f"         → UNDEFINED (rejected)")
        break

print()
print("Now run full lexer:")
result = lexer.transition(code)
print(f"Tokens: {len(result['tokens'])}")
for token in result['tokens']:
    print(f"  - {token['tokenType']:15s} = {repr(token['tokenName'])}")
print(f"Errors: {len(result['errors'])}")
for error in result['errors']:
    print(f"  - {error['message']}")
