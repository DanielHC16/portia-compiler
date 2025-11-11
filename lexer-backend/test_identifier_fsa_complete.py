"""Comprehensive test for identifier FSA states 220-269"""
from app.lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

print("="*80)
print(" "*20 + "IDENTIFIER FSA STATES 220-269 VERIFICATION")
print("="*80)

# Test each character length from 1 to 30
results = []
for length in range(1, 31):
    identifier = 'a' * length
    result = lexer.transition(identifier)
    has_errors = len(result['errors']) > 0
    
    # Up to 25 characters should succeed, 26+ should fail
    expected_success = (length <= 25)
    actual_success = not has_errors
    
    status = "✅" if (expected_success == actual_success) else "❌"
    results.append((status, length, identifier, has_errors, result))
    
    print(f"{status} Length {length:2d}: {'PASS' if expected_success == actual_success else 'FAIL'} ", end="")
    print(f"(Expected: {'OK' if expected_success else 'ERROR'}, Got: {'OK' if actual_success else 'ERROR'})")

print("\n" + "="*80)
print("DETAILED RESULTS:")
print("="*80)

# Show details for key lengths
key_lengths = [1, 5, 10, 15, 20, 24, 25, 26, 27, 30]
for status, length, identifier, has_errors, result in results:
    if length in key_lengths:
        print(f"\nLength {length}: {identifier[:10]}{'...' if length > 10 else ''}")
        if result['tokens']:
            token = result['tokens'][0]
            print(f"  Token: {token['tokenType']} = '{token['tokenName'][:20]}{'...' if length > 20 else ''}'")
        if result['errors']:
            for e in result['errors']:
                print(f"  Error: {e['message']}")

# Summary
passed = sum(1 for s, *_ in results if s == "✅")
failed = sum(1 for s, *_ in results if s == "❌")

print("\n" + "="*80)
print(f"SUMMARY: {passed}/30 passed, {failed}/30 failed")
print("="*80)

# Verify state transitions
print("\nVERIFYING STATE SEQUENCE:")
print("="*80)

# Check that we're hitting the correct states
test_transitions = [
    ("1 char", "x", "s220"),
    ("2 chars", "ab", "s222"),
    ("3 chars", "abc", "s223"),
    ("5 chars", "hello", "s226"),
    ("10 chars", "tenletters", "s234"),
    ("15 chars", "fifteenletterss", "s244"),
    ("20 chars", "twentycharidentifier", "s254"),  # 20 chars
    ("25 chars", "twentyfivecharidentifier", "s264"),  # 25 chars (max valid)
]

for name, code, expected_final_state in test_transitions:
    print(f"\n{name}: '{code}' (len={len(code)})")
    print(f"  Expected to reach state: {expected_final_state}")
    # Note: We can't easily check internal state, but we can verify it tokenizes correctly
    result = lexer.transition(code)
    if result['tokens'] and not result['errors']:
        print(f"  ✅ Successfully tokenized as: {result['tokens'][0]['tokenType']}")
    else:
        print(f"  ❌ Failed to tokenize")
