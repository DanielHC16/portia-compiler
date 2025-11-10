#!/usr/bin/env python3
"""Trace FSA transitions step-by-step for string literal."""

import sys
sys.path.insert(0, 'app')

from lexer.portia_lexer import LexicalAnalyzer

# Manual step-through simulation
lexer = LexicalAnalyzer()

code = '"hello"'
states = []
currState = 's0'

for i, ch in enumerate(code):
    nextState = lexer.lex_transition(currState, ch)
    is_final = lexer.is_final_state(currState)
    states.append({
        'pos': i,
        'char': ch,
        'currState': currState,
        'nextState': nextState,
        'is_final': is_final
    })
    currState = nextState if nextState not in ['UNDEFINED', 'DEFINED'] else currState

print("Step-by-step FSA transitions for: '\"hello\"'")
print("="*80)
for s in states:
    print(f"Pos {s['pos']}: '{s['char']}' | State: {s['currState']} -> {s['nextState']} | Final: {s['is_final']}")

print("\n" + "="*80)
print("Final state:", currState)
print("Is final?", lexer.is_final_state(currState))
if lexer.is_final_state(currState):
    token_type = lexer.get_token_type(currState, code)
    print("Token type:", token_type)

