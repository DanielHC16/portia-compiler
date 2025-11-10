#!/usr/bin/env python3
"""Comprehensive test of the lexer with real PORTIA code."""

import sys
sys.path.insert(0, 'app')

from lexer.portia_lexer import LexicalAnalyzer

# Test complex PORTIA code
code = '''int main() {
    thread("hello world");
    threadln("test");
    int x = 5;
    float y = 3.14;
    long z = 12345678901;
    double w = 0.123456789;
    string s = "foo bar";
    
    if (x > 0) {
        x = x + 1;
    }
    
    return 0;
}'''

print("Testing comprehensive PORTIA code:")
print("="*60)
print(code)
print("="*60)

lexer = LexicalAnalyzer()
result = lexer.transition(code)

print(f"\nTokens generated: {len(result['tokens'])}")
print(f"Errors found: {len(result['errors'])}")

if result['errors']:
    print("\nERRORS:")
    for error in result['errors']:
        print(f"  Line {error['line']}, Col {error['column']}: {error['message']}")
else:
    print("\n[OK] No errors - lexer working correctly!")

print("\nFirst 20 tokens:")
for i, token in enumerate(result['tokens'][:20]):
    print(f"  [{i:2d}] {token['tokenType']:20s} | {repr(token['tokenName']):25s}")

print(f"\n... (showing first 20 of {len(result['tokens'])} tokens)")

