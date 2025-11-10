#!/usr/bin/env python3
"""Debug script to test string and number literal handling."""

import sys
sys.path.insert(0, 'app')

from lexer.portia_lexer import LexicalAnalyzer

def test_case(description: str, code: str):
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"CODE: {repr(code)}")
    print(f"{'='*60}")
    
    lexer = LexicalAnalyzer()
    result = lexer.transition(code)
    
    print("\nTOKENS:")
    for i, token in enumerate(result['tokens']):
        print(f"  [{i}] {token['tokenType']:20s} | {repr(token['tokenName']):30s} | Line {token['tokenLine']}, Col {token['tokenCol']}")
    
    if result['errors']:
        print("\nERRORS:")
        for error in result['errors']:
            print(f"  Line {error['line']}, Col {error['column']}: {error['message']}")
    else:
        print("\nNo errors!")
    
    return result

# Test string literals
test_case("Simple string", '"hello"')
test_case("String with spaces", '"hello world"')
test_case("String in function call", 'thread("hello world")')
test_case("String with semicolon", '"hello";')

# Test number literals
test_case("Integer", '123')
test_case("Float", '123.45')
test_case("Number with semicolon", '123;')

# Test combined cases
test_case("Function with string", 'threadln("hello world");')
test_case("Assignment with number", 'int x = 5;')

print("\n" + "="*60)
print("TESTS COMPLETE")
print("="*60)

