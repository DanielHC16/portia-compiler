"""Test delimiter validation"""
from app.lexer.lexer import lex

def test_incomplete_addition():
    """a+ should error - + has no right operand"""
    code = 'a+'
    result = lex(code)
    print("Code:", repr(code))
    print("Tokens:", result['tokens'])
    print("Errors:", result['errors'])
    print()
    
    # Should have error for incomplete +
    assert len(result['errors']) > 0
    # Should have token for 'a'
    assert any(t['type'] == 'IDENTIFIER' and t['lexeme'] == 'a' for t in result['tokens'])
    # Should NOT have token for '+'
    assert not any(t['type'] == 'OP_ADD' for t in result['tokens'])

def test_addition_with_semicolon():
    """a+; should error - + followed by ; is invalid"""
    code = 'a+;'
    result = lex(code)
    print("Code:", repr(code))
    print("Tokens:", result['tokens'])
    print("Errors:", result['errors'])
    print()
    
    # Should have error
    assert len(result['errors']) > 0
    # Should have token for 'a'
    assert any(t['type'] == 'IDENTIFIER' and t['lexeme'] == 'a' for t in result['tokens'])
    # Should NOT have token for '+'
    assert not any(t['type'] == 'OP_ADD' for t in result['tokens'])

def test_valid_addition():
    """a+b should work - valid operands"""
    code = 'a+b'
    result = lex(code)
    print("Code:", repr(code))
    print("Tokens:", result['tokens'])
    print("Errors:", result['errors'])
    print()
    
    # Should have no errors
    assert len(result['errors']) == 0
    # Should have all tokens
    assert any(t['type'] == 'IDENTIFIER' and t['lexeme'] == 'a' for t in result['tokens'])
    assert any(t['type'] == 'OP_ADD' for t in result['tokens'])
    assert any(t['type'] == 'IDENTIFIER' and t['lexeme'] == 'b' for t in result['tokens'])

def test_valid_addition_with_semicolon():
    """a+b; should work - complete expression"""
    code = 'a+b;'
    result = lex(code)
    print("Code:", repr(code))
    print("Tokens:", result['tokens'])
    print("Errors:", result['errors'])
    print()
    
    # Should have no errors
    assert len(result['errors']) == 0
    # Should have all tokens
    token_types = [t['type'] for t in result['tokens']]
    assert 'IDENTIFIER' in token_types
    assert 'OP_ADD' in token_types
    assert 'DELIM_SEMICOLON' in token_types

if __name__ == '__main__':
    print("Testing delimiter validation...\n")
    test_incomplete_addition()
    test_addition_with_semicolon()
    test_valid_addition()
    test_valid_addition_with_semicolon()
    print("✅ All delimiter validation tests passed!")
