#!/usr/bin/env python3
"""
More detailed debug to trace the full scan loop
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from lexer.portia_lexer import LexicalAnalyzer

# Patch the transition method to add debug output
original_transition = LexicalAnalyzer.transition

def debug_transition(self, code):
    print(f"=== STARTING SCAN OF: {repr(code)} ===\n")
    
    # Simple manual trace
    i = 0
    state = 's0'
    lexeme = ''
    
    while i < len(code):
        ch = code[i]
        next_state = self.lex_transition(state, ch)
        
        print(f"[{i:2d}] ch={repr(ch):5s} state={state:6s} → next={next_state:10s} lexeme={repr(lexeme):20s}", end='')
        
        # Check if we're hitting whitespace handler
        if ch in [' ', '\t', '\n', '\r'] and state not in ['s277', 's279']:
            print("  [WHITESPACE HANDLER]")
        else:
            print()
        
        # Simulate what the lexer does
        if next_state not in ['UNDEFINED', 'DEFINED']:
            lexeme += ch
            state = next_state
            i += 1
        elif next_state == 'DEFINED':
            print(f"     → Would finalize token at delimiter {repr(ch)}")
            state = 's0'
            lexeme = ''
            # Don't consume the delimiter
        elif next_state == 'UNDEFINED':
            if state != 's0':
                print(f"     → UNDEFINED with lexeme={repr(lexeme)}, checking handlers...")
            state = 's0'
            lexeme = ''
            i += 1
        else:
            i += 1
    
    print(f"\n=== END MANUAL TRACE ===\n")
    
    # Now run the real lexer
    result = original_transition(self, code)
    
    print(f"=== REAL LEXER RESULTS ===")
    print(f"Tokens: {len(result['tokens'])}")
    for token in result['tokens']:
        print(f"  - {token['tokenType']:15s} = {repr(token['tokenName']):20s} at line {token['tokenLine']}, col {token['tokenCol']}")
    print(f"Errors: {len(result['errors'])}")
    for error in result['errors']:
        print(f"  - {error['message']}")
    
    return result

LexicalAnalyzer.transition = debug_transition

# Test
lexer = LexicalAnalyzer()
lexer.transition("abc\ndef")
