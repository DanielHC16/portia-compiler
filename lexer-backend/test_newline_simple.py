"""
Simple test to confirm newlines delimit numbers correctly
"""
import sys
sys.path.append('app')
from lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

print("Testing newline delimiter for numbers:\n")

# Test: Multiple numbers on separate lines
code = """123
456
12345678901
98765432109
789"""

result = lexer.transition(code)

print(f"Input code:")
print(code)
print(f"\nTokens found: {len(result['tokens'])}")
for i, token in enumerate(result['tokens'], 1):
    print(f"  {i}. {token['tokenType']:12s} = {token['tokenName']:15s} (line {token['tokenLine']})")

print(f"\nErrors: {len(result['errors'])}")
for error in result['errors']:
    print(f"  - {error['message']}")

# Verify
assert len(result['tokens']) == 5, f"Expected 5 tokens, got {len(result['tokens'])}"
assert result['tokens'][0]['tokenName'] == '123'
assert result['tokens'][1]['tokenName'] == '456'
assert result['tokens'][2]['tokenName'] == '12345678901'
assert result['tokens'][3]['tokenName'] == '98765432109'
assert result['tokens'][4]['tokenName'] == '789'
assert len(result['errors']) == 0, "Should have no errors"

print("\n✅ SUCCESS! Newlines properly delimit numerical literals")
