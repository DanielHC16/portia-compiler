#!/usr/bin/env python3
"""
Test script for PORTIA Semantic Analyzer.
Tests the full lexer -> parser -> semantic pipeline.
"""
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lexer-backend"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "parser-backend"))

# Import the components
from app.lexer.portia_lexer import LexicalAnalyzer
from parser.portia_parser import PortiaParser
from semantic.semantic_analyzer import SemanticAnalyzer

def run_test(name: str, source: str, expect_errors: bool = False):
    """Run a test case through all three phases."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"Source:\n{source.strip()}")
    print("-" * 40)
    
    # Phase 1: Lexical Analysis
    lexer = LexicalAnalyzer()
    lex_result = lexer.transition(source)
    tokens = lex_result.get("tokens", [])
    lex_errors = lex_result.get("errors", [])
    
    if lex_errors:
        print(f"LEXER ERRORS: {lex_errors}")
        if not expect_errors:
            print("FAIL: Unexpected lexer errors")
            return False
        return True
    
    print(f"Tokens: {len(tokens)} tokens generated")
    
    # Phase 2: Parsing
    try:
        parser = PortiaParser(tokens)
        tree = parser.parse()
        ast = tree.to_dict()
        print(f"Parser: AST generated successfully")
    except Exception as e:
        print(f"PARSER ERROR: {e}")
        if not expect_errors:
            print("FAIL: Unexpected parser error")
            return False
        return True
    
    # Phase 3: Semantic Analysis
    try:
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        
        print(f"\nSemantic Analysis Result:")
        print(f"  Success: {result['success']}")
        print(f"  Errors: {len(result['errors'])}")
        for err in result['errors']:
            print(f"    - Line {err['line']}: {err['message']}")
        print(f"  Warnings: {len(result['warnings'])}")
        for warn in result['warnings']:
            print(f"    - Line {warn['line']}: {warn['message']}")
        
        # Print symbol table
        if result.get('symbol_table'):
            st = result['symbol_table']
            if st.get('global_scope'):
                print(f"\n  Symbol Table:")
                for sym_name, info in st.get('global_scope', {}).items():
                    print(f"    {sym_name}: {info['kind']} ({info['type']})")
        
        if expect_errors and result['success']:
            print("FAIL: Expected errors but got success")
            return False
        if not expect_errors and not result['success']:
            print(f"FAIL: Expected success but got errors")
            return False
            
        print("PASS")
        return True
        
    except Exception as e:
        import traceback
        print(f"SEMANTIC ERROR: {e}")
        traceback.print_exc()
        print("FAIL: Exception during semantic analysis")
        return False


# Test cases
def run_all_tests():
    results = []
    
    # Test 1: Basic valid program
    results.append(run_test("Basic Valid Program", """
global var int gx = 10;

int main() {
    return 0;
}
"""))
    
    # Test 2: Function with parameters
    results.append(run_test("Function with Parameters", """
func int add(int a, int b) {
    return a + b;
}

int main() {
    return 0;
}
"""))
    
    # Test 3: Local variable declaration
    results.append(run_test("Local Variables", """
int main() {
    local var int x = 5;
    local const int y = 10;
    return 0;
}
"""))
    
    # Test 4: Undefined variable (should have error)
    results.append(run_test("Undefined Variable", """
int main() {
    local var int x = y;
    return 0;
}
""", expect_errors=True))
    
    # Test 5: Weave type definition
    results.append(run_test("Weave Type Definition", """
weave Point {
    int x;
    int y;
}

int main() {
    return 0;
}
"""))
    
    # Test 6: Control structures (note: PORTIA doesn't allow local declarations inside blocks)
    results.append(run_test("Control Structures", """
int main() {
    local var int x = 5;
    local var int y = 0;
    if (x > 0) {
        y = 10;
    }
    return 0;
}
"""))
    
    # Test 7: While loop (without increment operators)
    results.append(run_test("While Loop", """
int main() {
    local var int i = 0;
    while (i < 10) {
        i = i + 1;
    }
    return 0;
}
"""))
    
    # Test 8: For loop (skip increment operators for now)
    results.append(run_test("For Loop", """
int main() {
    for (local var int i = 0; i < 10; i = i + 1) {
        thread(i);
    }
    return 0;
}
"""))
    
    # Test 9: I/O statements
    results.append(run_test("I/O Statements", """
int main() {
    local var int x = 0;
    trap(x);
    thread(x);
    threadln(x);
    return 0;
}
"""))
    
    # Test 10: Function call
    results.append(run_test("Function Call", """
func void greet() {
    threadln("Hello");
}

int main() {
    greet();
    return 0;
}
"""))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    if passed == total:
        print("ALL TESTS PASSED!")
    else:
        print(f"FAILED: {total - passed} tests")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
