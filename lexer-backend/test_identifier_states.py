"""Test identifier FSA states 220-249"""
from app.lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

# Test identifiers of various lengths
test_cases = [
    ("1 char", "x", True),
    ("2 chars", "xy", True),
    ("3 chars", "abc", True),
    ("5 chars", "hello", True),
    ("10 chars", "tenLetters", True),
    ("15 chars", "fifteenLetterID", True),
    ("20 chars", "twentyCharIdentifier", True),
    ("25 chars (max)", "twentyFiveCharIdentifier", True),  # Exactly 25 chars - should work
    ("26 chars (over)", "twentySixCharIdentifierXX", False),  # 26 chars - should fail
    ("With underscore", "my_var_name", True),
    ("Starts with underscore", "_private", True),
    ("With numbers", "var123", True),
]

print("="*70)
print(" "*15 + "IDENTIFIER FSA STATES 220-249 TEST")
print("="*70)

passed = 0
failed = 0

for name, code, should_pass in test_cases:
    result = lexer.transition(code)
    has_errors = len(result['errors']) > 0
    
    # should_pass=True means we expect 0 errors
    # should_pass=False means we expect errors
    success = (not has_errors) == should_pass
    
    if success:
        status = "✅ PASS"
        passed += 1
    else:
        status = "❌ FAIL"
        failed += 1
    
    print(f"\n{status} {name} (len={len(code)})")
    print(f"   Input: '{code}'")
    print(f"   Expected: {'success' if should_pass else 'error'}")
    print(f"   Got: {len(result['errors'])} error(s)")
    
    if result['tokens']:
        print(f"   Token: {result['tokens'][0]['tokenType']} = '{result['tokens'][0]['tokenName']}'")
    
    if result['errors']:
        for e in result['errors']:
            print(f"   Error: {e['message']}")

print("\n" + "="*70)
print(f"SUMMARY: {passed} passed, {failed} failed")
print("="*70)
