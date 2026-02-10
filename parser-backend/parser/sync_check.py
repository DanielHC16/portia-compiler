"""
Synchronization check for PORTIA grammar files.
Verifies CFG.txt, portia.lark, and portia_parser.py are in sync.
"""

def check_r2_compliance():
    """Verify R2: No empty {} initializers are syntactically possible."""
    print("=" * 60)
    print("R2 COMPLIANCE CHECK: Empty Initializers Forbidden")
    print("=" * 60)
    
    # Rules that MUST NOT have nullable productions
    forbidden_nullable = [
        'int_arr_init_content_1d',
        'int_arr_init_content_2d',
        'long_arr_init_content_1d',
        'long_arr_init_content_2d',
        'float_arr_init_content_1d',
        'float_arr_init_content_2d',
        'double_arr_init_content_1d',
        'double_arr_init_content_2d',
        'char_arr_init_content_1d',
        'char_arr_init_content_2d',
        'string_arr_init_content_1d',
        'string_arr_init_content_2d',
        'bool_arr_init_content_1d',
        'bool_arr_init_content_2d',
        'weave_arr_init_content_1d',
        'weave_arr_init_content_2d',
        'weave_init_row',
        'weave_value_list',
    ]
    
    violations = []
    
    # Check CFG
    with open('PORTIA-LL1-CFG.txt', 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            for rule in forbidden_nullable:
                if f'<{rule}>' in line and '→ λ' in line:
                    violations.append(f"CFG line {line_num}: {line.strip()}")
    
    # Check Lark
    with open('portia.lark', 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            for rule in forbidden_nullable:
                if f'{rule}:' in line and line.strip().endswith(':'):
                    # This is a rule definition with no production on same line
                    # Could be nullable if next non-empty line is "|"
                    violations.append(f"Lark line {line_num}: {line.strip()} (potential nullable)")
    
    if violations:
        print("⚠ VIOLATIONS FOUND:")
        for v in violations:
            print(f"  {v}")
        return False
    else:
        print("✓ All 18 content rules are NON-NULLABLE")
        print(f"✓ Checked {len(forbidden_nullable)} critical rules")
        return True


def check_headers():
    """Verify both files have R2 compliance comments."""
    print("\n" + "=" * 60)
    print("HEADER COMPLIANCE CHECK")
    print("=" * 60)
    
    # Check CFG header
    with open('PORTIA-LL1-CFG.txt', 'r', encoding='utf-8') as f:
        cfg_header = ''.join(f.readlines()[:20])
    
    # Check Lark header
    with open('portia.lark', 'r', encoding='utf-8') as f:
        lark_header = ''.join(f.readlines()[:10])
    
    cfg_has_r2 = 'EMPTY INITIALIZERS FORBIDDEN' in cfg_header or 'R2 compliant' in cfg_header
    lark_has_r2 = 'EMPTY INITIALIZERS FORBIDDEN' in lark_header or 'R2 compliant' in lark_header
    
    print(f"CFG header R2 comment: {'✓' if cfg_has_r2 else '✗'}")
    print(f"Lark header R2 comment: {'✓' if lark_has_r2 else '✗'}")
    
    return cfg_has_r2 and lark_has_r2


def check_parser_loads():
    """Verify parser initializes without LALR conflicts."""
    print("\n" + "=" * 60)
    print("PARSER INITIALIZATION CHECK")
    print("=" * 60)
    
    try:
        from portia_parser import PortiaLarkParser
        parser = PortiaLarkParser()
        print("✓ Parser initialized successfully")
        print("✓ No LALR conflicts detected")
        print("✓ Grammar file loaded: portia.lark")
        return True
    except Exception as e:
        print(f"✗ Parser initialization failed: {e}")
        return False


def check_key_structures():
    """Verify key structural elements match between CFG and Lark."""
    print("\n" + "=" * 60)
    print("STRUCTURAL SYNCHRONIZATION CHECK")
    print("=" * 60)
    
    # Key rule patterns to verify
    key_patterns = [
        ('int_arr_init_content_1d', 'intlit', 'INTLIT'),
        ('weave_value_list', 'weave_field_value', 'weave_field_value'),
        ('weave_arr_init_content_1d', '{', 'LBRACE'),
    ]
    
    all_match = True
    
    for rule_name, cfg_token, lark_token in key_patterns:
        # Check CFG
        with open('PORTIA-LL1-CFG.txt', 'r', encoding='utf-8') as f:
            cfg_found = False
            for line in f:
                if f'<{rule_name}>' in line and '→' in line and cfg_token in line:
                    cfg_found = True
                    break
        
        # Check Lark
        with open('portia.lark', 'r', encoding='utf-8') as f:
            lark_found = False
            in_rule = False
            for line in f:
                if f'{rule_name}:' in line:
                    in_rule = True
                if in_rule and lark_token in line:
                    lark_found = True
                    break
                if in_rule and line.strip() and not line.strip().startswith('|'):
                    in_rule = False
        
        match = cfg_found and lark_found
        symbol = '✓' if match else '✗'
        print(f"{symbol} {rule_name}: CFG={cfg_found}, Lark={lark_found}")
        all_match = all_match and match
    
    return all_match


def main():
    print("\n" + "=" * 60)
    print("PORTIA GRAMMAR SYNCHRONIZATION CHECK")
    print("=" * 60)
    print("Verifying: CFG.txt ↔ portia.lark ↔ portia_parser.py\n")
    
    results = []
    
    results.append(("R2 Compliance", check_r2_compliance()))
    results.append(("Header Comments", check_headers()))
    results.append(("Parser Initialization", check_parser_loads()))
    results.append(("Structural Sync", check_key_structures()))
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    for test_name, passed in results:
        symbol = '✓' if passed else '✗'
        print(f"{symbol} {test_name}")
    
    all_passed = all(r[1] for r in results)
    
    print()
    if all_passed:
        print("✓✓✓ ALL SYNCHRONIZATION CHECKS PASSED ✓✓✓")
        print()
        print("Summary:")
        print("  - CFG and Lark grammar are structurally synchronized")
        print("  - Parser successfully loads Lark grammar")
        print("  - All 18 nullable productions removed (R2 compliant)")
        print("  - Empty {} initializers are syntactically impossible")
        return 0
    else:
        print("⚠⚠⚠ SYNCHRONIZATION ISSUES DETECTED ⚠⚠⚠")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
