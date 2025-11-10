#!/usr/bin/env python3
"""Test dot and concat operators."""

import sys
sys.path.insert(0, 'app')

from lexer.portia_lexer import LexicalAnalyzer

def test(desc, code):
    print(f"\n{desc}")
    print(f"Code: {repr(code)}")
    lexer = LexicalAnalyzer()
    result = lexer.transition(code)
    
    print("Tokens:")
    for t in result['tokens']:
        print(f"  {t['tokenType']:15s} | {repr(t['tokenName'])}")
    
    if result['errors']:
        print("Errors:")
        for e in result['errors']:
            print(f"  Line {e['line']}, Col {e['column']}: {e['message']}")
    else:
        print("  [OK] No errors")

# Test cases
test("Single dot (member access)", "obj.field")
test("Double dot (concat)", '"hello" .. "world"')
test("Dot with numbers", "3.14")
test("Multiple dots", "a.b.c")
test("Concat in expression", 'x = "a" .. "b";')

print("\n" + "="*60)
print("DONE")

