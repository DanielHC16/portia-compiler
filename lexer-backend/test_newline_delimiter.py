"""
Test that numerical literals are properly delimited by newlines
"""
import sys
sys.path.append('app')
from lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

print("="*60)
print("Testing numerical literals with newline delimiters")
print("="*60)

# Test 1: Integer on new line
code1 = """123
456"""

result1 = lexer.transition(code1)
print("\nTest 1: Two integers on separate lines")
print(f"Code: {repr(code1)}")
print(f"Tokens: {result1['tokens']}")
print(f"Errors: {result1['errors']}")
assert len(result1['tokens']) == 2, f"Expected 2 tokens, got {len(result1['tokens'])}"
assert result1['tokens'][0]['tokenName'] == '123', f"Expected '123', got {result1['tokens'][0]['tokenName']}"
assert result1['tokens'][1]['tokenName'] == '456', f"Expected '456', got {result1['tokens'][1]['tokenName']}"
print("✅ PASS")

# Test 2: Long integers on new lines
code2 = """12345678901
98765432109"""

result2 = lexer.transition(code2)
print("\nTest 2: Two long integers on separate lines")
print(f"Code: {repr(code2)}")
print(f"Tokens: {result2['tokens']}")
print(f"Errors: {result2['errors']}")
assert len(result2['tokens']) == 2, f"Expected 2 tokens, got {len(result2['tokens'])}"
assert result2['tokens'][0]['tokenType'] == 'long_lit', f"Expected 'long_lit', got {result2['tokens'][0]['tokenType']}"
assert result2['tokens'][1]['tokenType'] == 'long_lit', f"Expected 'long_lit', got {result2['tokens'][1]['tokenType']}"
print("✅ PASS")

# Test 3: Mixed numbers with newlines
code3 = """123
12345678901
456"""

result3 = lexer.transition(code3)
print("\nTest 3: Mixed int and long on separate lines")
print(f"Code: {repr(code3)}")
print(f"Tokens: {result3['tokens']}")
print(f"Errors: {result3['errors']}")
assert len(result3['tokens']) == 3, f"Expected 3 tokens, got {len(result3['tokens'])}"
assert result3['tokens'][0]['tokenType'] == 'int_lit', f"Expected 'int_lit', got {result3['tokens'][0]['tokenType']}"
assert result3['tokens'][1]['tokenType'] == 'long_lit', f"Expected 'long_lit', got {result3['tokens'][1]['tokenType']}"
assert result3['tokens'][2]['tokenType'] == 'int_lit', f"Expected 'int_lit', got {result3['tokens'][2]['tokenType']}"
print("✅ PASS")

# Test 4: Numbers with other delimiters
code4 = """123;
456 789
12345678901"""

result4 = lexer.transition(code4)
print("\nTest 4: Numbers with various delimiters")
print(f"Code: {repr(code4)}")
print(f"Tokens: {result4['tokens']}")
print(f"Errors: {result4['errors']}")
# Should have: 123, semicolon, 456, 789, 12345678901
token_names = [t['tokenName'] for t in result4['tokens']]
print(f"Token names: {token_names}")
assert '123' in token_names, "Should tokenize 123"
assert '456' in token_names, "Should tokenize 456"
assert '789' in token_names, "Should tokenize 789"
assert '12345678901' in token_names, "Should tokenize 12345678901"
print("✅ PASS")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED - Newlines properly delimit numbers!")
print("="*60)
