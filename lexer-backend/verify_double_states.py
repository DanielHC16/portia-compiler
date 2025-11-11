"""
Verification script for double literal FSA states (s327-s360)
Tests transitions and tokenization for 8-23 fractional digit doubles
"""

import sys
sys.path.append('app')

from app.lexer.portia_lexer import LexicalAnalyzer

def test_double_state_transitions():
    """Test that all double states transition correctly"""
    lexer = LexicalAnalyzer()
    
    print("Testing double literal state transitions (s329-s360)...")
    print("=" * 60)
    
    # Test transition from s327 (7 frac) to s329 (8 frac) - becomes double
    print("\n1. Testing s327 → s329 transition (float becomes double):")
    assert lexer.lex_transition('s327', '5') == 's329', "s327 + digit should → s329"
    print("   ✓ s327 + digit → s329")
    
    # Test s329 (8 fractional digits - first double state)
    print("\n2. Testing s329 (8 fractional digits):")
    assert lexer.lex_transition('s329', '5') == 's331', "s329 + digit should → s331"
    assert lexer.lex_transition('s329', 'ANY') == 's330', "s329 + delimiter should → s330"
    print("   ✓ s329 + digit → s331")
    print("   ✓ s329 + delimiter → s330 (final)")
    
    # Test all building states (odd) transition to next building state
    building_states = [
        ('s329', 's331'), ('s331', 's333'), ('s333', 's335'), ('s335', 's337'),
        ('s337', 's339'), ('s339', 's341'), ('s341', 's343'), ('s343', 's345'),
        ('s345', 's347'), ('s347', 's349'), ('s349', 's351'), ('s351', 's353'),
        ('s353', 's355'), ('s355', 's357'), ('s357', 's359')
    ]
    
    print("\n3. Testing building state digit transitions:")
    for current, next_state in building_states:
        result = lexer.lex_transition(current, '5')
        assert result == next_state, f"{current} + digit should → {next_state}, got {result}"
        print(f"   ✓ {current} + digit → {next_state}")
    
    # Test all building states (odd) finalize correctly
    print("\n4. Testing building state delimiter transitions:")
    for current, _ in building_states:
        final_state = f"s{int(current[1:]) + 1}"
        result = lexer.lex_transition(current, 'ANY')
        assert result == final_state, f"{current} + delimiter should → {final_state}, got {result}"
        print(f"   ✓ {current} + delimiter → {final_state}")
    
    # Test s359 (23 fractional - maximum double)
    print("\n5. Testing s359 (23 fractional digits - maximum):")
    assert lexer.lex_transition('s359', 'ANY') == 's360', "s359 + delimiter should → s360"
    assert lexer.lex_transition('s359', '5') == 'UNDEFINED', "s359 + digit should → UNDEFINED (max reached)"
    print("   ✓ s359 + delimiter → s360 (final)")
    print("   ✓ s359 + digit → UNDEFINED (maximum reached)")
    
    # Test all final states (even) return DEFINED
    print("\n6. Testing final states return DEFINED:")
    final_states = [f"s{n}" for n in range(330, 361, 2)]  # s330, s332, ..., s360
    for state in final_states:
        result = lexer.lex_transition(state, 'ANY')
        assert result == 'DEFINED', f"{state} should return DEFINED, got {result}"
        print(f"   ✓ {state} + ANY → DEFINED")
    
    print("\n" + "=" * 60)
    print("All double state transitions verified! ✓")
    print("=" * 60)

def test_double_tokenization():
    """Test that double literals are correctly tokenized"""
    lexer = LexicalAnalyzer()
    
    print("\n\nTesting double literal tokenization...")
    print("=" * 60)
    
    test_cases = [
        # (input, expected_tokens)
        ("1.12345678", [("1.12345678", "double_lit")]),  # 8 fractional digits
        ("1.123456789", [("1.123456789", "double_lit")]),  # 9 fractional digits
        ("1.1234567890", [("1.1234567890", "double_lit")]),  # 10 fractional digits
        ("1.12345678901234567", [("1.12345678901234567", "double_lit")]),  # 17 fractional digits
        ("1.123456789012345678901234", [("1.123456789012345678901234", "double_lit")]),  # 23 fractional (max)
        
        # Test with delimiters
        ("1.12345678 ", [("1.12345678", "double_lit")]),
        ("1.12345678\n", [("1.12345678", "double_lit")]),
        ("1.12345678;", [("1.12345678", "double_lit"), (";", "semicolon")]),
        
        # Multiple doubles
        ("1.12345678 2.123456789", [
            ("1.12345678", "double_lit"),
            ("2.123456789", "double_lit")
        ]),
        
        # Test transition from float (7 frac) to double (8 frac)
        ("1.1234567", [("1.1234567", "float_lit")]),  # 7 fractional = float
        ("1.12345678", [("1.12345678", "double_lit")]),  # 8 fractional = double
    ]
    
    for i, (input_str, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{input_str}'")
        result = lexer.transition(input_str)
        tokens = result['tokens']
        errors = result['errors']
        
        if errors:
            print(f"   ✗ FAILED: Got errors: {errors}")
            continue
        
        # Extract (lexeme, type) pairs
        actual = [(t['tokenName'], t['tokenType']) for t in tokens]
        
        if actual == expected:
            print(f"   ✓ PASSED")
            for token in tokens:
                print(f"      {token['tokenName']:30} → {token['tokenType']}")
        else:
            print(f"   ✗ FAILED")
            print(f"      Expected: {expected}")
            print(f"      Got:      {actual}")
    
    print("\n" + "=" * 60)
    print("Double tokenization tests completed!")
    print("=" * 60)

def test_fractional_digit_boundaries():
    """Test the boundaries between int, long, float, and double"""
    lexer = LexicalAnalyzer()
    
    print("\n\nTesting fractional digit boundaries...")
    print("=" * 60)
    
    test_cases = [
        # Fractional digits: 1-7 = float, 8-23 = double
        ("1.1", "float_lit", "1 fractional digit"),
        ("1.12", "float_lit", "2 fractional digits"),
        ("1.123", "float_lit", "3 fractional digits"),
        ("1.1234", "float_lit", "4 fractional digits"),
        ("1.12345", "float_lit", "5 fractional digits"),
        ("1.123456", "float_lit", "6 fractional digits"),
        ("1.1234567", "float_lit", "7 fractional digits (max for float)"),
        ("1.12345678", "double_lit", "8 fractional digits (min for double)"),
        ("1.123456789", "double_lit", "9 fractional digits"),
        ("1.1234567890", "double_lit", "10 fractional digits"),
        ("1.12345678901", "double_lit", "11 fractional digits"),
        ("1.123456789012", "double_lit", "12 fractional digits"),
        ("1.1234567890123", "double_lit", "13 fractional digits"),
        ("1.12345678901234", "double_lit", "14 fractional digits"),
        ("1.123456789012345", "double_lit", "15 fractional digits"),
        ("1.1234567890123456", "double_lit", "16 fractional digits"),
        ("1.12345678901234567", "double_lit", "17 fractional digits"),
        ("1.123456789012345678", "double_lit", "18 fractional digits"),
        ("1.1234567890123456789", "double_lit", "19 fractional digits"),
        ("1.12345678901234567890", "double_lit", "20 fractional digits"),
        ("1.123456789012345678901", "double_lit", "21 fractional digits"),
        ("1.1234567890123456789012", "double_lit", "22 fractional digits"),
        ("1.12345678901234567890123", "double_lit", "23 fractional digits (max for double)"),
    ]
    
    all_passed = True
    for input_str, expected_type, description in test_cases:
        result = lexer.transition(input_str)
        tokens = result['tokens']
        errors = result['errors']
        
        if errors:
            print(f"✗ {description}: Got errors: {errors}")
            all_passed = False
            continue
        
        if len(tokens) != 1:
            print(f"✗ {description}: Expected 1 token, got {len(tokens)}")
            all_passed = False
            continue
        
        actual_type = tokens[0]['tokenType']
        if actual_type == expected_type:
            print(f"✓ {description}: {input_str} → {actual_type}")
        else:
            print(f"✗ {description}: Expected {expected_type}, got {actual_type}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All boundary tests passed! ✓")
    else:
        print("Some boundary tests failed!")
    print("=" * 60)

if __name__ == "__main__":
    test_double_state_transitions()
    test_double_tokenization()
    test_fractional_digit_boundaries()
    print("\n✓ All double literal verification tests completed!")
