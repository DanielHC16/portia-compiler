"""
Comprehensive test showing int → long → float transitions
"""
import sys
sys.path.append('app')
from lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

print("="*70)
print("COMPREHENSIVE NUMERICAL LITERAL TEST")
print("="*70)

code = """
123
12345678901
3.14
123.456
9876543210.1234567
"""

result = lexer.transition(code)

print(f"\nInput code:")
print(code)

print(f"\nTokens found: {len(result['tokens'])}")
print("\n{:<5} {:<15} {:<20} {:<10}".format("No.", "Type", "Value", "Line"))
print("-" * 70)
for i, token in enumerate(result['tokens'], 1):
    print("{:<5} {:<15} {:<20} {:<10}".format(
        i, 
        token['tokenType'], 
        token['tokenName'], 
        token['tokenLine']
    ))

print(f"\nErrors: {len(result['errors'])}")
if result['errors']:
    for error in result['errors']:
        print(f"  - {error['message']}")

# Verify all expected tokens
expected = [
    ('123', 'int_lit'),
    ('12345678901', 'long_lit'),
    ('3.14', 'float_lit'),
    ('123.456', 'float_lit'),
    ('9876543210.1234567', 'float_lit'),
]

print("\n" + "="*70)
print("VERIFICATION:")
print("="*70)

all_match = True
for i, (expected_val, expected_type) in enumerate(expected):
    if i < len(result['tokens']):
        actual_val = result['tokens'][i]['tokenName']
        actual_type = result['tokens'][i]['tokenType']
        
        if actual_val == expected_val and actual_type == expected_type:
            print(f"✅ Token {i+1}: {expected_type:12s} '{expected_val}'")
        else:
            print(f"❌ Token {i+1}: Expected {expected_type} '{expected_val}', got {actual_type} '{actual_val}'")
            all_match = False
    else:
        print(f"❌ Token {i+1}: Missing!")
        all_match = False

if all_match and len(result['tokens']) == len(expected) and len(result['errors']) == 0:
    print("\n" + "="*70)
    print("✅ SUCCESS! All numerical literal types working correctly!")
    print("   - Integers (1-10 digits)")
    print("   - Long integers (11-17 digits)")
    print("   - Floats (1-7 fractional digits)")
    print("="*70)
else:
    print("\n❌ Some issues found")
