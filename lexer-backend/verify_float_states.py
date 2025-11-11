"""
Verification script for Float FSA states (s314-s328)
Tests states for 1-7 fractional digit floats
"""

import sys
sys.path.append('app')

from lexer.portia_lexer import LexicalAnalyzer

def test_float_states():
    """Test float literal states (1-7 fractional digits)"""
    lexer = LexicalAnalyzer()
    
    print("="*60)
    print("TESTING FLOAT STATES (s314-s328)")
    print("="*60)
    
    test_cases = [
        # (input, expected_token_type, description)
        ("1.5", "float_lit", "Float with 1 fractional digit"),
        ("1.25", "float_lit", "Float with 2 fractional digits"),
        ("1.125", "float_lit", "Float with 3 fractional digits"),
        ("1.0625", "float_lit", "Float with 4 fractional digits"),
        ("1.03125", "float_lit", "Float with 5 fractional digits"),
        ("1.015625", "float_lit", "Float with 6 fractional digits"),
        ("1.0078125", "float_lit", "Float with 7 fractional digits (max)"),
        
        # Test with different integer parts
        ("42.5", "float_lit", "Two-digit int with 1 fractional"),
        ("123.456", "float_lit", "Three-digit int with 3 fractional"),
        ("9876543210.1234567", "float_lit", "Long int (10 digits) with 7 fractional"),
        
        # Test with newline delimiter
        ("3.14\n", "float_lit", "Float with newline delimiter"),
        
        # Test transition from int to float
        ("5.0", "float_lit", "Integer becomes float with .0"),
        ("12345678901.5", "float_lit", "Long becomes float"),
        
        # Edge case: just decimal point (should error)
        ("5.", "ERROR", "Decimal point without fractional digit"),
    ]
    
    passed = 0
    failed = 0
    
    for code, expected_type, description in test_cases:
        try:
            result = lexer.transition(code)
            tokens = result.get('tokens', [])
            errors = result.get('errors', [])
            
            if expected_type == "ERROR":
                # Should have error, no tokens
                if errors and not tokens:
                    print(f"✅ PASS: {description}")
                    print(f"   Input: {repr(code)}")
                    print(f"   Error: {errors[0]['message']}")
                    passed += 1
                else:
                    print(f"❌ FAIL: {description}")
                    print(f"   Input: {repr(code)}")
                    print(f"   Expected error but got: {tokens}")
                    failed += 1
                continue
            
            if not tokens:
                print(f"❌ FAIL: {description}")
                print(f"   Input: {repr(code)}")
                print(f"   Expected: {expected_type}, Got: No tokens")
                print(f"   Errors: {errors}")
                failed += 1
                continue
            
            actual_type = tokens[0]['tokenType']
            
            if actual_type == expected_type:
                print(f"✅ PASS: {description}")
                passed += 1
            else:
                print(f"❌ FAIL: {description}")
                print(f"   Input: {repr(code)}")
                print(f"   Expected: {expected_type}, Got: {actual_type}")
                print(f"   Full token: {tokens[0]}")
                failed += 1
        except Exception as e:
            print(f"❌ ERROR: {description}")
            print(f"   Input: {repr(code)}")
            print(f"   Exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0

def verify_state_transitions():
    """Verify that all float states are properly connected"""
    lexer = LexicalAnalyzer()
    
    print("\n" + "="*60)
    print("VERIFYING STATE TRANSITIONS (s314-s328)")
    print("="*60)
    
    # Test s314 entry (must have digit after decimal)
    entry_tests = [
        ('s314', '5', 's315'),  # First fractional digit
        ('s314', ' ', 'UNDEFINED'),  # No digit after decimal = error
    ]
    
    # Test building state transitions (odd states)
    building_states = [
        ('s315', 'numbers', 's317'),  # 1 → 2 fractional digits
        ('s317', 'numbers', 's319'),  # 2 → 3 fractional digits
        ('s319', 'numbers', 's321'),  # 3 → 4 fractional digits
        ('s321', 'numbers', 's323'),  # 4 → 5 fractional digits
        ('s323', 'numbers', 's325'),  # 5 → 6 fractional digits
        ('s325', 'numbers', 's327'),  # 6 → 7 fractional digits
        ('s327', 'ANY', 's328'),       # 7 fractional (max) → finalize
    ]
    
    # Test finalization transitions (ANY = nbl_delim)
    finalization_states = [
        ('s315', 'ANY', 's316'),
        ('s317', 'ANY', 's318'),
        ('s319', 'ANY', 's320'),
        ('s321', 'ANY', 's322'),
        ('s323', 'ANY', 's324'),
        ('s325', 'ANY', 's326'),
        ('s327', 'ANY', 's328'),
    ]
    
    # Test final states return DEFINED
    final_states = [
        ('s316', 'ANY', 'DEFINED'),
        ('s318', 'ANY', 'DEFINED'),
        ('s320', 'ANY', 'DEFINED'),
        ('s322', 'ANY', 'DEFINED'),
        ('s324', 'ANY', 'DEFINED'),
        ('s326', 'ANY', 'DEFINED'),
        ('s328', 'ANY', 'DEFINED'),
    ]
    
    all_tests = [
        ("Entry state s314", entry_tests),
        ("Building states (digit→digit)", building_states),
        ("Finalization (ANY→final)", finalization_states),
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
    print("\n🔍 PORTIA FLOAT STATES VERIFICATION\n")
    
    transitions_ok = verify_state_transitions()
    print()
    tokens_ok = test_float_states()
    
    if transitions_ok and tokens_ok:
        print("\n✅ ALL FLOAT STATES VERIFIED SUCCESSFULLY!")
    else:
        print("\n⚠️  SOME TESTS FAILED - Review above")
