"""
Verification script for Long Integer FSA states (s298-s313)
Tests states for 11-17 digit long integers
"""

import sys
sys.path.append('app')

from lexer.portia_lexer import LexicalAnalyzer

def test_long_integers():
    """Test long integer literal states (11-17 digits)"""
    lexer = LexicalAnalyzer()
    
    print("="*60)
    print("TESTING LONG INTEGER STATES (s298-s313)")
    print("="*60)
    
    test_cases = [
        # (input, expected_token_type, description)
        ("12345678901", "long_lit", "11-digit long (minimum)"),
        ("123456789012", "long_lit", "12-digit long"),
        ("1234567890123", "long_lit", "13-digit long"),
        ("12345678901234", "long_lit", "14-digit long"),
        ("123456789012345", "long_lit", "15-digit long"),
        ("1234567890123456", "long_lit", "16-digit long"),
        ("12345678901234567", "long_lit", "17-digit long (maximum)"),
        
        # Test transition from int to long
        ("1234567890", "int_lit", "10-digit int (not long yet)"),
        ("12345678901", "long_lit", "11-digit transitions to long"),
        
        # Test with delimiters
        ("12345678901;", "long_lit", "11-digit long with semicolon"),
        ("12345678901 ", "long_lit", "11-digit long with space"),
        
        # Test decimal point transition
        ("12345678901.5", "float_lit", "11-digit long becomes float"),
        ("12345678901234567.0", "float_lit", "17-digit long becomes float"),
    ]
    
    passed = 0
    failed = 0
    
    for code, expected_type, description in test_cases:
        try:
            result = lexer.transition(code)
            tokens = result.get('tokens', [])
            
            if not tokens:
                print(f"❌ FAIL: {description}")
                print(f"   Input: {code}")
                print(f"   Expected: {expected_type}, Got: No tokens")
                print(f"   Errors: {result.get('errors', [])}")
                failed += 1
                continue
            
            actual_type = tokens[0]['tokenType']
            
            if actual_type == expected_type:
                print(f"✅ PASS: {description}")
                passed += 1
            else:
                print(f"❌ FAIL: {description}")
                print(f"   Input: {code}")
                print(f"   Expected: {expected_type}, Got: {actual_type}")
                print(f"   Full token: {tokens[0]}")
                failed += 1
        except Exception as e:
            print(f"❌ ERROR: {description}")
            print(f"   Input: {code}")
            print(f"   Exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0

def verify_state_transitions():
    """Verify that all long integer states are properly connected"""
    lexer = LexicalAnalyzer()
    
    print("\n" + "="*60)
    print("VERIFYING STATE TRANSITIONS (s298-s313)")
    print("="*60)
    
    # Test building state transitions (even states)
    building_states = [
        ('s298', 'numbers', 's300'),  # 11 → 12 digits
        ('s300', 'numbers', 's302'),  # 12 → 13 digits
        ('s302', 'numbers', 's304'),  # 13 → 14 digits
        ('s304', 'numbers', 's306'),  # 14 → 15 digits
        ('s306', 'numbers', 's308'),  # 15 → 16 digits
        ('s308', 'numbers', 's310'),  # 16 → 17 digits
        ('s310', 'numbers', 's312'),  # 17 → s312
        ('s312', '.', 's314'),         # s312 → decimal
    ]
    
    # Test finalization transitions (ANY = nbl_delim)
    finalization_states = [
        ('s298', 'ANY', 's299'),
        ('s300', 'ANY', 's301'),
        ('s302', 'ANY', 's303'),
        ('s304', 'ANY', 's305'),
        ('s306', 'ANY', 's307'),
        ('s308', 'ANY', 's309'),
        ('s310', 'ANY', 's311'),
        ('s312', 'ANY', 's313'),
    ]
    
    # Test decimal point transitions
    decimal_states = [
        ('s298', '.', 's314'),
        ('s300', '.', 's314'),
        ('s302', '.', 's314'),
        ('s304', '.', 's314'),
        ('s306', '.', 's314'),
        ('s308', '.', 's314'),
        ('s310', '.', 's314'),
        ('s312', '.', 's314'),
    ]
    
    # Test final states return DEFINED
    final_states = [
        ('s299', 'ANY', 'DEFINED'),
        ('s301', 'ANY', 'DEFINED'),
        ('s303', 'ANY', 'DEFINED'),
        ('s305', 'ANY', 'DEFINED'),
        ('s307', 'ANY', 'DEFINED'),
        ('s309', 'ANY', 'DEFINED'),
        ('s311', 'ANY', 'DEFINED'),
        ('s313', 'ANY', 'DEFINED'),
    ]
    
    all_tests = [
        ("Building states (digit→digit)", building_states),
        ("Finalization (ANY→final)", finalization_states),
        ("Decimal point (→s314)", decimal_states),
        ("Final states (→DEFINED)", final_states),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for category, tests in all_tests:
        print(f"\n{category}:")
        passed = 0
        failed = 0
        
        for state, char, expected in tests:
            # Use actual digit for 'numbers'
            test_char = '5' if char == 'numbers' else char
            result = lexer.lex_transition(state, test_char)
            
            if result == expected:
                print(f"  ✅ {state} + {char:8s} → {expected}")
                passed += 1
            else:
                print(f"  ❌ {state} + {char:8s} → Expected: {expected}, Got: {result}")
                failed += 1
        
        total_passed += passed
        total_failed += failed
    
    print("\n" + "="*60)
    print(f"STATE VERIFICATION: {total_passed} passed, {total_failed} failed")
    print("="*60)
    
    return total_failed == 0

if __name__ == "__main__":
    print("\n🔍 PORTIA LONG INTEGER STATES VERIFICATION\n")
    
    transitions_ok = verify_state_transitions()
    print()
    tokens_ok = test_long_integers()
    
    if transitions_ok and tokens_ok:
        print("\n✅ ALL LONG INTEGER STATES VERIFIED SUCCESSFULLY!")
    else:
        print("\n⚠️  SOME TESTS FAILED - Review above")
