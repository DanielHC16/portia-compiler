#!/usr/bin/env python3
"""Simple debug to trace FSA state transitions for string literals."""

import sys
sys.path.insert(0, 'app')

from lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

# Test what state we get when we transition from s0 with '"'
result = lexer.lex_transition('s0', '"')
print(f"Transition from s0 with '\"': {result}")

# Test if s277 is recognized as final
is_final = lexer.is_final_state('s277')
print(f"Is s277 a final state? {is_final}")

# Test what happens with the full string
print("\n" + "="*60)
print("Testing full string: '\"hello\"'")
print("="*60)

code = '"hello"'
result = lexer.transition(code)

print("\nTOKENS:")
for token in result['tokens']:
    print(f"  {token}")

print("\nERRORS:")
for error in result['errors']:
    print(f"  {error}")

