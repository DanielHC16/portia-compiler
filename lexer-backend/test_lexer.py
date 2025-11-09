"""
Test script for PORTIA Lexer - Spec Compliance Testing
Tests all PORTIA language features
"""

from app.lexer.portia_lexer import LexicalAnalyzer

# Comprehensive test cases covering all PORTIA language features
test_cases = [
    {
        "name": "1. All 38 Reserved Words",
        "code": """local global using main int bool string float double long char void weave
const var trap thread threadln func return if else switch case default
while do for break"""
    },
    {
        "name": "2. Boolean Literals",
        "code": """true false"""
    },
    {
        "name": "3. Integer Literals (int)",
        "code": """0 123 007 2147483647 1234567890"""
    },
    {
        "name": "4. Long Literals (long)",
        "code": """12345678901 9223372036854775807 1234567890123456789"""
    },
    {
        "name": "5. Float Literals (float)",
        "code": """3.14 0.5 123.456 3.1415926"""
    },
    {
        "name": "6. Double Literals (double)",
        "code": """12345678.12345678 3.14159265358979 1.234567890123456"""
    },
    {
        "name": "7. String Literals",
        "code": r'''"Hello World" "PORTIA" "" "Line1\nLine2" "Tab\there" "Quote\"test"'''
    },
    {
        "name": "8. Character Literals",
        "code": r"""'a' 'Z' '5' ' ' '\n' '\t' '\'' '\"'"""
    },
    {
        "name": "9. Valid Identifiers",
        "code": """myVar _temp x count123 myVeryLongVariableName studentID user_name"""
    },
    {
        "name": "10. Arithmetic Operators",
        "code": """+ - * / %"""
    },
    {
        "name": "11. Relational Operators",
        "code": """== != < > <= >="""
    },
    {
        "name": "12. Logical Operators",
        "code": """&& || !"""
    },
    {
        "name": "13. Assignment Operators",
        "code": """= += -= *= /= %="""
    },
    {
        "name": "14. Unary Operators",
        "code": """++ -- ! -"""
    },
    {
        "name": "15. String Concatenation",
        "code": """name .. " " .. surname"""
    },
    {
        "name": "16. Delimiters",
        "code": """( ) [ ] { } ; , : ."""
    },
    {
        "name": "17. Single-line Comments",
        "code": """// This is a comment
int x = 5; // inline comment
// Another comment"""
    },
    {
        "name": "18. Multi-line Comments",
        "code": """/* Simple comment */
/* Multi
   line
   comment */
int y = 10; /* inline */ int z = 20;"""
    },
    {
        "name": "19. Complete Variable Declaration",
        "code": """global var int count = 0;
local var string name = "Hardy";
global const float PI = 3.14159;"""
    },
    {
        "name": "20. Function Declaration",
        "code": """func int add(int a, int b) {
    return a + b;
}"""
    },
    {
        "name": "21. Main Block",
        "code": """int main() {
    local var int x = 10;
    thread("Hello World");
    return 0;
}"""
    },
    {
        "name": "22. If-Else Statement",
        "code": """if (x > 0) {
    thread("Positive");
} else {
    thread("Non-positive");
}"""
    },
    {
        "name": "23. Switch-Case Statement",
        "code": """switch (grade) {
    case 90:
        thread("A");
        break;
    case 80:
        thread("B");
        break;
    default:
        thread("Other");
}"""
    },
    {
        "name": "24. For Loop",
        "code": """for (local var int i = 0; i < 10; i++) {
    thread(i);
}"""
    },
    {
        "name": "25. While Loop",
        "code": """while (count < 100) {
    count++;
}"""
    },
    {
        "name": "26. Do-While Loop",
        "code": """do {
    thread(x);
    x--;
} while (x > 0);"""
    },
    {
        "name": "27. Array Declaration",
        "code": """global var int numbers[5] = {1, 2, 3, 4, 5};
local var string names[3] = {"Alice", "Bob", "Charlie"};"""
    },
    {
        "name": "28. Weave Declaration",
        "code": """weave Student {
    int id;
    string name;
    float grade;
}"""
    },
    {
        "name": "29. I/O Statements",
        "code": """trap(userInput);
thread("Enter value: ");
threadln("Result: " .. result);"""
    },
    {
        "name": "30. Complex Expression",
        "code": """local var int result = (a + b) * c - d / e % f;
local var bool flag = (x >= 10) && (y <= 20) || !z;"""
    },
    {
        "name": "31. Type Casting",
        "code": """local var float f = (float)intValue;
local var int i = (int)floatValue;"""
    },
    {
        "name": "32. Error - Identifier Too Long",
        "code": """thisIsAnExtremelyLongIdentifierNameThatExceedsTheLimit = 10;"""
    },
    {
        "name": "33. Error - Unterminated String",
        "code": '''"This string has no end'''
    },
    {
        "name": "34. Error - Unterminated Comment",
        "code": """/* This comment never closes
int x = 5;"""
    },
    {
        "name": "35. Error - Invalid Character",
        "code": """int x = 5 @ 10;"""
    },
    {
        "name": "36. Error - Invalid Escape Sequence",
        "code": r'''"Bad escape \b here"'''
    },
    {
        "name": "37. Mixed Valid Code",
        "code": """// PORTIA Program Example
global var int counter = 0;
global const string GREETING = "Hello, PORTIA!";

func void increment() {
    counter++;
    return;
}

int main() {
    using counter;
    local var int limit = 10;
    
    for (local var int i = 0; i < limit; i++) {
        increment();
    }
    
    threadln(GREETING);
    threadln("Counter: " .. counter);
    
    return 0;
}"""
    },
]

def run_tests():
    lexer = LexicalAnalyzer()
    
    print("=" * 80)
    print(" " * 20 + "PORTIA LEXER - SPEC COMPLIANCE TEST SUITE")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"TEST: {test_case['name']}")
        print(f"{'='*80}")
        print(f"INPUT CODE:")
        print("-" * 80)
        print(test_case['code'])
        print("-" * 80)
        
        try:
            result = lexer.scan(test_case['code'])
            
            print(f"\n[TOKENS] ({len(result['tokens'])}):")
            print(f"{'#':<4} {'TYPE':<20} {'LEXEME':<25} {'LINE':<6} {'COL':<6}")
            print("-" * 80)
            for i, token in enumerate(result['tokens'][:50], 1):  # Limit display to first 50
                lexeme = token['tokenName'][:22] + '...' if len(token['tokenName']) > 25 else token['tokenName']
                print(f"{i:<4} {token['tokenType']:<20} {lexeme:<25} {token['tokenLine']:<6} {token['tokenCol']:<6}")
            
            if len(result['tokens']) > 50:
                print(f"... and {len(result['tokens']) - 50} more tokens")
            
            if result['errors']:
                print(f"\n[ERROR] ({len(result['errors'])}):")
                for error in result['errors']:
                    print(f"  - {error['message']}")
                    print(f"    Location: Line {error['line']}, Column {error['column']}")
                failed += 1
            else:
                print(f"\n[PASS] No errors detected")
                passed += 1
        
        except Exception as e:
            print(f"\n[EXCEPTION] during lexical analysis:")
            print(f"  {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        
        print()
    
    print("=" * 80)
    print(f" " * 30 + "TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(test_cases)}")
    print(f"[PASS] Passed: {passed}")
    print(f"[FAIL] Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
