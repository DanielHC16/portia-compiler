from portia_parser import PortiaLarkParser

p = PortiaLarkParser()
print('✓ Parser initialized')

tests = [
    ('Empty array', 'int main() { local const int x[3] = {}; return 0; }', False),
    ('Valid array', 'int main() { local const int x[3] = {1,2,3}; return 0; }', True),
    ('Expr rejected', 'int main() { local const int x = 1+2; return 0; }', False),
    ('Type mismatch', 'int main() { local const int x = 3.14; return 0; }', False),
    ('Uninitialized array OK', 'int main() { local const int x[5]; return 0; }', True),
]

passed = 0
for name, code, should_pass in tests:
    try:
        p.parser.parse(code)
        result = should_pass
    except:
        result = not should_pass
    if result:
        print(f'✓ {name}')
        passed += 1
    else:
        print(f'✗ {name}')

print(f'\nResult: {passed}/{len(tests)} tests passed')
if passed == len(tests):
    print('✓✓✓ ALL TESTS PASSED ✓✓✓')
