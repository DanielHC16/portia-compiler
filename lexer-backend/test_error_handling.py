"""Test error handling in lexer"""
from app.lexer.lexer import lex

def test_unterminated_string():
    """Unterminated string should error and NOT generate token"""
    code = '"hello'
    result = lex(code)
    assert len(result['errors']) == 1
    assert 'Unterminated string literal' in result['errors'][0]['message']
    # Should NOT generate STRING_LIT token
    assert len(result['tokens']) == 0

def test_unterminated_char():
    """Unterminated char should error and NOT generate token"""
    code = "'a"
    result = lex(code)
    assert len(result['errors']) == 1
    assert 'Unterminated character literal' in result['errors'][0]['message']
    # Should NOT generate CHAR_LIT token
    assert len(result['tokens']) == 0

def test_invalid_char_literal():
    """Invalid char literal (multiple chars) should error and NOT generate token"""
    code = "'abc'"
    result = lex(code)
    assert len(result['errors']) == 1
    assert 'exactly one character' in result['errors'][0]['message']
    # Should NOT generate CHAR_LIT token
    assert len(result['tokens']) == 0

def test_empty_char_literal():
    """Empty char literal should error and NOT generate token"""
    code = "''"
    result = lex(code)
    assert len(result['errors']) == 1
    assert 'Empty character literal' in result['errors'][0]['message']
    # Should NOT generate CHAR_LIT token
    assert len(result['tokens']) == 0

def test_invalid_escape_in_string():
    """Invalid escape sequence should error and NOT generate token"""
    code = r'"hello\x"'
    result = lex(code)
    assert len(result['errors']) == 1
    assert 'Invalid escape sequence' in result['errors'][0]['message']
    # Should NOT generate STRING_LIT token
    assert len(result['tokens']) == 0

def test_invalid_escape_in_char():
    """Invalid escape in char should error and NOT generate token"""
    code = r"'\x'"
    result = lex(code)
    assert len(result['errors']) == 1
    assert 'Invalid escape sequence' in result['errors'][0]['message']
    # Should NOT generate CHAR_LIT token
    assert len(result['tokens']) == 0

def test_identifier_too_long():
    """Identifier > 25 chars should error and NOT generate token"""
    code = 'a' * 26
    result = lex(code)
    assert len(result['errors']) == 1
    assert 'exceeds maximum length' in result['errors'][0]['message']
    # Should NOT generate IDENTIFIER token
    assert len(result['tokens']) == 0

def test_invalid_fractional_literal():
    """Fractional literal with no digits should error and NOT generate token"""
    code = '.'
    result = lex(code)
    # This should be treated as DELIM_DOT
    tokens = result['tokens']
    assert len(tokens) == 1
    assert tokens[0]['type'] == 'DELIM_DOT'

def test_single_ampersand():
    """Single & should error and NOT generate token"""
    code = 'a & b'
    result = lex(code)
    assert len(result['errors']) == 1
    assert "Invalid operator '&'" in result['errors'][0]['message']
    # Should have tokens for 'a' and 'b' but NOT for '&'
    tokens = result['tokens']
    token_types = [t['type'] for t in tokens]
    assert 'IDENTIFIER' in token_types
    assert 'OP_AND' not in token_types

def test_single_pipe():
    """Single | should error and NOT generate token"""
    code = 'a | b'
    result = lex(code)
    assert len(result['errors']) == 1
    assert "Invalid operator '|'" in result['errors'][0]['message']
    # Should have tokens for 'a' and 'b' but NOT for '|'
    tokens = result['tokens']
    token_types = [t['type'] for t in tokens]
    assert 'IDENTIFIER' in token_types
    assert 'OP_OR' not in token_types

def test_valid_string():
    """Valid string should generate token with no errors"""
    code = '"hello"'
    result = lex(code)
    assert len(result['errors']) == 0
    assert len(result['tokens']) == 1
    assert result['tokens'][0]['type'] == 'STRING_LIT'

def test_valid_char():
    """Valid char should generate token with no errors"""
    code = "'a'"
    result = lex(code)
    assert len(result['errors']) == 0
    assert len(result['tokens']) == 1
    assert result['tokens'][0]['type'] == 'CHAR_LIT'

def test_valid_escape_in_string():
    """Valid escape sequences should work"""
    code = r'"hello\nworld"'
    result = lex(code)
    assert len(result['errors']) == 0
    assert len(result['tokens']) == 1
    assert result['tokens'][0]['type'] == 'STRING_LIT'

def test_valid_escape_in_char():
    """Valid escape in char should work"""
    code = r"'\n'"
    result = lex(code)
    assert len(result['errors']) == 0
    assert len(result['tokens']) == 1
    assert result['tokens'][0]['type'] == 'CHAR_LIT'

if __name__ == '__main__':
    # Run tests
    test_unterminated_string()
    test_unterminated_char()
    test_invalid_char_literal()
    test_empty_char_literal()
    test_invalid_escape_in_string()
    test_invalid_escape_in_char()
    test_identifier_too_long()
    test_invalid_fractional_literal()
    test_single_ampersand()
    test_single_pipe()
    test_valid_string()
    test_valid_char()
    test_valid_escape_in_string()
    test_valid_escape_in_char()
    
    print("✅ All error handling tests passed!")
