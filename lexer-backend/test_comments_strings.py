"""Comprehensive test for comment and string literal FSA states 270-277"""
from app.lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

print("="*80)
print(" "*15 + "COMMENT AND STRING LITERAL FSA STATES 270-277 VERIFICATION")
print("="*80)

# ============================================================================
# SINGLE-LINE COMMENT TESTS (s270-s271)
# ============================================================================
print("\n" + "="*80)
print("SINGLE-LINE COMMENT TESTS (s270 → s271)")
print("="*80)

single_line_tests = [
    ("Basic single-line comment", "// this is a comment\n"),
    ("Single-line with code after", "// comment\nvar x"),
    ("Single-line at EOF", "// comment at end"),
    ("Empty single-line comment", "//\n"),
    ("Single-line with special chars", "// !@#$%^&*()_+-=[]{}|;':,.<>?"),
    ("Single-line with ASCII chars", "// ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"),
]

for idx, (description, code) in enumerate(single_line_tests, 1):
    print(f"\n[Test {idx}] {description}")
    print(f"Input: {repr(code)}")
    result = lexer.transition(code)
    
    has_comment = any(t['tokenType'] == 'single_comment' for t in result['tokens'])
    has_errors = len(result['errors']) > 0
    
    status = "✅" if has_comment and not has_errors else "❌"
    print(f"{status} Result: {'PASS' if has_comment and not has_errors else 'FAIL'}")
    
    # Show tokens
    if result['tokens']:
        print(f"  Tokens ({len(result['tokens'])}):")
        for token in result['tokens']:
            print(f"    - {token['tokenType']}: '{token['tokenName']}'")
    
    # Show errors
    if result['errors']:
        print(f"  Errors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"    - {error['message']}")

# ============================================================================
# MULTI-LINE COMMENT TESTS (s272-s275)
# ============================================================================
print("\n" + "="*80)
print("MULTI-LINE COMMENT TESTS (s272 → s273 → s274 → s275)")
print("="*80)

multi_line_tests = [
    ("Basic multi-line comment", "/* this is a comment */"),
    ("Multi-line with newlines", "/* line 1\nline 2\nline 3 */"),
    ("Multi-line with code after", "/* comment */ var x"),
    ("Empty multi-line comment", "/**/"),
    ("Multi-line with special chars", "/* !@#$%^&*()_+-=[]{}|;':,.<>? */"),
    ("Multi-line with asterisks", "/* * * * * */"),
    ("Multi-line spanning multiple lines", "/* start\nmiddle\nend */"),
    ("Nested-like comment (not actually nested)", "/* outer /* inner */ outer */"),
]

for idx, (description, code) in enumerate(multi_line_tests, 1):
    print(f"\n[Test {idx}] {description}")
    print(f"Input: {repr(code)}")
    result = lexer.transition(code)
    
    has_comment = any(t['tokenType'] == 'multi_comment' for t in result['tokens'])
    has_errors = len(result['errors']) > 0
    
    status = "✅" if has_comment and not has_errors else "❌"
    print(f"{status} Result: {'PASS' if has_comment and not has_errors else 'FAIL'}")
    
    # Show tokens
    if result['tokens']:
        print(f"  Tokens ({len(result['tokens'])}):")
        for token in result['tokens']:
            preview = token['tokenName'][:40] + '...' if len(token['tokenName']) > 40 else token['tokenName']
            print(f"    - {token['tokenType']}: '{preview}'")
    
    # Show errors
    if result['errors']:
        print(f"  Errors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"    - {error['message']}")

# ============================================================================
# ERROR CASES FOR COMMENTS
# ============================================================================
print("\n" + "="*80)
print("COMMENT ERROR CASES")
print("="*80)

comment_error_tests = [
    ("Unterminated multi-line comment", "/* this comment never closes"),
    ("Unterminated multi-line at EOF", "/* comment"),
    ("Multi-line with only opening", "/*"),
    ("Multi-line with only closing star", "/* *"),
]

for idx, (description, code) in enumerate(comment_error_tests, 1):
    print(f"\n[Test {idx}] {description}")
    print(f"Input: {repr(code)}")
    result = lexer.transition(code)
    
    has_errors = len(result['errors']) > 0
    status = "✅" if has_errors else "❌"
    print(f"{status} Result: {'PASS (error detected)' if has_errors else 'FAIL (no error)'}")
    
    # Show errors
    if result['errors']:
        print(f"  Errors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"    - {error['message']}")

# ============================================================================
# STRING LITERAL TESTS (s276-s277)
# ============================================================================
print("\n" + "="*80)
print("STRING LITERAL TESTS (s276 → s277)")
print("="*80)

string_tests = [
    ("Basic string", '"hello"'),
    ("Empty string", '""'),
    ("String with spaces", '"hello world"'),
    ("String with numbers", '"abc123"'),
    ("String with special chars", '"!@#$%^&*()"'),
    ("String with escape sequences", '"hello\\nworld"'),
    ("String with tab escape", '"tab\\there"'),
    ("String with quote escape", '"He said \\"hi\\""'),
    ("Long string", '"' + 'a' * 100 + '"'),
]

for idx, (description, code) in enumerate(string_tests, 1):
    print(f"\n[Test {idx}] {description}")
    print(f"Input: {repr(code)}")
    result = lexer.transition(code)
    
    has_string = any(t['tokenType'] == 'string_lit' for t in result['tokens'])
    has_errors = len(result['errors']) > 0
    
    status = "✅" if has_string and not has_errors else "❌"
    print(f"{status} Result: {'PASS' if has_string and not has_errors else 'FAIL'}")
    
    # Show tokens
    if result['tokens']:
        print(f"  Tokens ({len(result['tokens'])}):")
        for token in result['tokens']:
            preview = token['tokenName'][:40] + '...' if len(token['tokenName']) > 40 else token['tokenName']
            print(f"    - {token['tokenType']}: '{preview}'")
    
    # Show errors
    if result['errors']:
        print(f"  Errors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"    - {error['message']}")

# ============================================================================
# ERROR CASES FOR STRINGS
# ============================================================================
print("\n" + "="*80)
print("STRING ERROR CASES")
print("="*80)

string_error_tests = [
    ("Unterminated string", '"hello'),
    ("String with newline (invalid)", '"hello\nworld"'),
    ("String at EOF unterminated", '"unclosed'),
]

for idx, (description, code) in enumerate(string_error_tests, 1):
    print(f"\n[Test {idx}] {description}")
    print(f"Input: {repr(code)}")
    result = lexer.transition(code)
    
    has_errors = len(result['errors']) > 0
    status = "✅" if has_errors else "❌"
    print(f"{status} Result: {'PASS (error detected)' if has_errors else 'FAIL (no error)'}")
    
    # Show errors
    if result['errors']:
        print(f"  Errors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"    - {error['message']}")

# ============================================================================
# MIXED CODE TESTS
# ============================================================================
print("\n" + "="*80)
print("MIXED CODE TESTS (comments + strings + other tokens)")
print("="*80)

mixed_tests = [
    ("Code with single-line comment", 'var x // comment\nvar y'),
    ("Code with multi-line comment", 'var x /* comment */ var y'),
    ("Code with string", 'var x = "hello"'),
    ("All three types", '// comment\nvar x = "hello" /* block */'),
    ("Multiple strings and comments", '"str1" /* c1 */ "str2" // c2'),
]

for idx, (description, code) in enumerate(mixed_tests, 1):
    print(f"\n[Test {idx}] {description}")
    print(f"Input: {repr(code)}")
    result = lexer.transition(code)
    
    has_errors = len(result['errors']) > 0
    status = "✅" if not has_errors else "❌"
    print(f"{status} Result: {'PASS' if not has_errors else 'FAIL'}")
    
    # Show tokens
    if result['tokens']:
        print(f"  Tokens ({len(result['tokens'])}):")
        for token in result['tokens']:
            preview = token['tokenName'][:40] + '...' if len(token['tokenName']) > 40 else token['tokenName']
            print(f"    - {token['tokenType']}: '{preview}'")
    
    # Show errors
    if result['errors']:
        print(f"  Errors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"    - {error['message']}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)

total_tests = (
    len(single_line_tests) + 
    len(multi_line_tests) + 
    len(comment_error_tests) + 
    len(string_tests) + 
    len(string_error_tests) + 
    len(mixed_tests)
)

print(f"""
Total Test Categories:
  - Single-line comments: {len(single_line_tests)} tests
  - Multi-line comments: {len(multi_line_tests)} tests
  - Comment error cases: {len(comment_error_tests)} tests
  - String literals: {len(string_tests)} tests
  - String error cases: {len(string_error_tests)} tests
  - Mixed code tests: {len(mixed_tests)} tests
  
Total: {total_tests} tests

Please review the output above to verify all states 270-277 work correctly.
""")

print("="*80)
