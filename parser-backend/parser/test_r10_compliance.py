"""
R10 — Strict Return Type Enforcement Tests
Verifies that return statements are syntactically restricted to declared return type category.
"""

from portia_parser import PortiaLarkParser

parser = PortiaLarkParser()

def test_parse(code, should_pass, description):
    """Test if code parses as expected."""
    # Create minimal token list from source
    tokens = tokenize_minimal(code)
    result = parser.parse(tokens)
    passed = result['success'] == should_pass
    status = 'PASS' if passed else 'FAIL'
    outcome = 'parsed' if result['success'] else 'rejected'
    print(f"[{status}] {description}: {outcome}")
    if not passed:
        if result.get('errors'):
            print(f"    Error: {result['errors'][0].get('message', 'Unknown')[:80]}")
    return passed

def tokenize_minimal(code):
    """Minimal tokenizer for testing - maps source to token dicts."""
    import re
    
    # Token patterns in priority order
    patterns = [
        ('longlit', r'-?\d{11,19}'),
        ('doublelit', r'-?\d+\.\d{8,16}'),
        ('floatlit', r'-?\d+\.\d{1,7}'),
        ('intlit', r'-?\d{1,10}'),
        ('charlit', r"'[^']'"),
        ('stringlit', r'"[^"]*"'),
        
        # Keywords
        ('global', r'\bglobal\b'), ('local', r'\blocal\b'), ('func', r'\bfunc\b'),
        ('return', r'\breturn\b'), ('if', r'\bif\b'), ('else', r'\belse\b'),
        ('switch', r'\bswitch\b'), ('case', r'\bcase\b'), ('default', r'\bdefault\b'),
        ('for', r'\bfor\b'), ('while', r'\bwhile\b'), ('do', r'\bdo\b'),
        ('break', r'\bbreak\b'), ('trap', r'\btrap\b'), ('thread', r'\bthread\b'),
        ('threadln', r'\bthreadln\b'), ('using', r'\busing\b'), ('weave', r'\bweave\b'),
        ('main', r'\bmain\b'), ('int', r'\bint\b'), ('long', r'\blong\b'),
        ('float', r'\bfloat\b'), ('double', r'\bdouble\b'), ('char', r'\bchar\b'),
        ('string', r'\bstring\b'), ('bool', r'\bbool\b'), ('void', r'\bvoid\b'),
        ('var', r'\bvar\b'), ('const', r'\bconst\b'), ('true', r'\btrue\b'),
        ('false', r'\bfalse\b'),
        
        # Multi-char operators
        ('add_assign', r'\+='), ('minus_assign', r'-='), ('mult_assign', r'\*='),
        ('div_assign', r'/='), ('modulo_assign', r'%='),
        ('equal', r'=='), ('not_equal', r'!='), ('less_equal', r'<='),
        ('greater_equal', r'>='), ('logical_and', r'&&'), ('logical_or', r'\|\|'),
        ('increment', r'\+\+'), ('decrement', r'--'), ('concat', r'\.\.'),
        
        # Single-char operators
        ('assign', r'='), ('less_than', r'<'), ('greater_than', r'>'),
        ('logical_not', r'!'), ('add', r'\+'), ('subtract', r'-'),
        ('multiply', r'\*'), ('divide', r'/'), ('modulo', r'%'),
        ('open_paren', r'\('), ('close_paren', r'\)'),
        ('open_brace', r'\{'), ('close_brace', r'\}'),
        ('open_bracket', r'\['), ('close_bracket', r'\]'),
        ('semicolon', r';'), ('comma', r','), ('colon', r':'), ('dot', r'\.'),
        
        # Identifier
        ('id', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        
        # Whitespace (skip)
        ('space', r'[ \t]+'),
        ('newline', r'\n'),
    ]
    
    combined = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
    regex = re.compile(combined)
    
    tokens = []
    line = 1
    col = 1
    
    for match in regex.finditer(code):
        kind = match.lastgroup
        value = match.group()
        
        if kind == 'newline':
            line += 1
            col = 1
            continue
        elif kind == 'space':
            col += len(value)
            continue
        
        tokens.append({
            'type': kind,
            'lexeme': value,
            'line': line,
            'column': col
        })
        col += len(value)
    
    return tokens


def main():
    print("=" * 60)
    print("R10 — Strict Return Type Enforcement Tests")
    print("=" * 60)
    
    results = []
    
    # ========================================
    # 1. SCALAR RETURNS - VALID CASES
    # ========================================
    print("\n1. Scalar Returns - Valid Cases:")
    
    # Int function returning int literal
    results.append(test_parse(
        "func int foo() { return 42; } int main() { return 0; }",
        True, "int func returns intlit"))
    
    # Int function returning identifier
    results.append(test_parse(
        "func int foo() { return x; } int main() { return 0; }",
        True, "int func returns id"))
    
    # Int function returning expression
    results.append(test_parse(
        "func int foo() { return x + 1; } int main() { return 0; }",
        True, "int func returns expression"))
    
    # Int function returning int cast
    results.append(test_parse(
        "func int foo() { return int(x); } int main() { return 0; }",
        True, "int func returns int cast"))
    
    # Bool function returning true
    results.append(test_parse(
        "func bool foo() { return true; } int main() { return 0; }",
        True, "bool func returns true"))
    
    # Bool function returning false
    results.append(test_parse(
        "func bool foo() { return false; } int main() { return 0; }",
        True, "bool func returns false"))
    
    # String function returning stringlit
    results.append(test_parse(
        'func string foo() { return "hello"; } int main() { return 0; }',
        True, "string func returns stringlit"))
    
    # Float function returning floatlit
    results.append(test_parse(
        "func float foo() { return 3.14; } int main() { return 0; }",
        True, "float func returns floatlit"))
    
    # Double function returning doublelit
    results.append(test_parse(
        "func double foo() { return 3.14159265; } int main() { return 0; }",
        True, "double func returns doublelit"))
    
    # Char function returning charlit
    results.append(test_parse(
        "func char foo() { return 'a'; } int main() { return 0; }",
        True, "char func returns charlit"))
    
    # Long function returning longlit  
    results.append(test_parse(
        "func long foo() { return 12345678901; } int main() { return 0; }",
        True, "long func returns longlit"))
    
    # ========================================
    # 2. SCALAR RETURNS - INVALID CASES (wrong literal category)
    # ========================================
    print("\n2. Scalar Returns - Invalid Cases (wrong literal):")
    
    # Int function returning floatlit - SHOULD FAIL
    results.append(test_parse(
        "func int foo() { return 3.14; } int main() { return 0; }",
        False, "int func rejects floatlit"))
    
    # Int function returning true - SHOULD FAIL
    results.append(test_parse(
        "func int foo() { return true; } int main() { return 0; }",
        False, "int func rejects true"))
    
    # Int function returning stringlit - SHOULD FAIL
    results.append(test_parse(
        'func int foo() { return "hello"; } int main() { return 0; }',
        False, "int func rejects stringlit"))
    
    # Bool function returning intlit - SHOULD FAIL
    results.append(test_parse(
        "func bool foo() { return 42; } int main() { return 0; }",
        False, "bool func rejects intlit"))
    
    # Float function returning intlit - SHOULD FAIL
    results.append(test_parse(
        "func float foo() { return 42; } int main() { return 0; }",
        False, "float func rejects intlit"))
    
    # String function returning intlit - SHOULD FAIL
    results.append(test_parse(
        "func string foo() { return 42; } int main() { return 0; }",
        False, "string func rejects intlit"))
    
    # ========================================
    # 3. ARRAY RETURNS - identifier only
    # ========================================
    print("\n3. Array Returns - identifier only:")
    
    # Array function returning identifier - VALID
    results.append(test_parse(
        "func int[5] foo() { return arr; } int main() { return 0; }",
        True, "int array func returns id"))
    
    # Array function returning intlit - SHOULD FAIL
    results.append(test_parse(
        "func int[5] foo() { return 42; } int main() { return 0; }",
        False, "int array func rejects intlit"))
    
    # Array function returning expression - SHOULD FAIL
    results.append(test_parse(
        "func int[5] foo() { return arr[0]; } int main() { return 0; }",
        False, "int array func rejects element access"))
    
    # 2D array function returning identifier - VALID
    results.append(test_parse(
        "func int[3][3] foo() { return matrix; } int main() { return 0; }",
        True, "2D int array func returns id"))
    
    # ========================================
    # 4. WEAVE RETURNS - identifier only
    # ========================================
    print("\n4. Weave Returns - identifier only:")
    
    # Weave function returning identifier - VALID
    results.append(test_parse(
        "weave Point { int x; int y; }; func Point foo() { return p; } int main() { return 0; }",
        True, "weave func returns id"))
    
    # Weave function returning field access - SHOULD FAIL
    results.append(test_parse(
        "weave Point { int x; int y; }; func Point foo() { return p.x; } int main() { return 0; }",
        False, "weave func rejects field access"))
    
    # Weave function returning literal - SHOULD FAIL
    results.append(test_parse(
        "weave Point { int x; int y; }; func Point foo() { return 42; } int main() { return 0; }",
        False, "weave func rejects intlit"))
    
    # ========================================
    # 5. VOID RETURNS - bare return only
    # ========================================
    print("\n5. Void Returns - bare return only:")
    
    # Void function with bare return - VALID
    results.append(test_parse(
        "func void foo() { return; } int main() { return 0; }",
        True, "void func bare return"))
    
    # Void function returning value - SHOULD FAIL  
    results.append(test_parse(
        "func void foo() { return 42; } int main() { return 0; }",
        False, "void func rejects return value"))
    
    # ========================================
    # 6. { ... } NEVER REACHABLE IN RETURNS
    # ========================================
    print("\n6. Brace literals unreachable in returns:")
    
    # Return with braces - SHOULD FAIL for all types
    results.append(test_parse(
        "func int foo() { return {1, 2, 3}; } int main() { return 0; }",
        False, "int func rejects brace literal"))
    
    results.append(test_parse(
        "func int[3] foo() { return {1, 2, 3}; } int main() { return 0; }",
        False, "array func rejects brace literal"))
    
    # ========================================
    # 7. FUNCTION BODY STATEMENTS WORK
    # ========================================
    print("\n7. Function body statements work:")
    
    # Full function with local, using, statements
    results.append(test_parse(
        """func int foo() {
            local var int x = 5;
            x = x + 1;
            return x;
        }
        int main() { return 0; }""",
        True, "full int func with locals"))
    
    results.append(test_parse(
        """func bool test() {
            local var bool flag = true;
            if (flag) { flag = false; }
            return flag;
        }
        int main() { return 0; }""",
        True, "full bool func with control"))
    
    # ========================================
    # Summary
    # ========================================
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("*** ALL R10 COMPLIANCE TESTS PASSED ***")
        return 0
    else:
        print(f"*** {total - passed} TESTS FAILED ***")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
