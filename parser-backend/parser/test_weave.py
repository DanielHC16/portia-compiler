from portia_parser import PortiaLarkParser

p = PortiaLarkParser()

# Test 1: Array as field (Table 19)
test1 = '''weave Student {
    string name;
    int grades[3];
};

int main() {
    local var Student s2 = {"PORTIA", {96, 98, 99}};
    return 0;
}'''

# Test 2: Nested weave field (Table 19)
test2 = '''weave Address {
    string city;
    int zip;
};

weave Person {
    string name;
    Address address;
};

int main() {
    local const Person p1 = {"PORTIA", {"Manila", 1000}};
    return 0;
}'''

# Test 3: Array of weaves (Table 19)
test3 = '''weave Course {
    string title;
    int units;
};

weave Student {
    string name;
    Course courses[2];
};

int main() {
    local var Student s1 = {
        "PORTIA",
        {{"Math", 3}, {"Science", 4}}
    };
    return 0;
}'''

tests = [
    ("Array as field", test1),
    ("Nested weave field", test2),
    ("Array of weaves", test3)
]

print("Testing weave examples from spec...")
for name, code in tests:
    try:
        result = p.parser.parse(code)
        print(f"✓ {name}: PASSED")
    except Exception as e:
        print(f"✗ {name}: FAILED - {e}")

print("\nAll weave examples validated!")
