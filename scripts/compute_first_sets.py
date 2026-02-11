"""
Compute FIRST sets for the Portia grammar and generate documentation.
"""
import re
from collections import defaultdict

def parse_lark_grammar(filepath):
    """Parse the lark grammar file and extract all rules."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rules = defaultdict(list)
    current_rule = None
    
    for line in content.split('\n'):
        line = line.strip()
        
        # Skip empty lines, comments, directives
        if not line or line.startswith('//') or line.startswith('%'):
            continue
        
        # Check for rule definition
        match = re.match(r'^([a-z_]+)\s*:\s*(.*)$', line)
        if match:
            current_rule = match.group(1)
            rhs = match.group(2).strip()
            if rhs:
                rules[current_rule].append(rhs)
            continue
        
        # Check for alternative
        if line.startswith('|') and current_rule:
            rhs = line[1:].strip()
            if rhs:
                rules[current_rule].append(rhs)
    
    return dict(rules)

def tokenize_rhs(rhs):
    """Tokenize a production RHS into symbols."""
    # Remove comments
    if '//' in rhs:
        rhs = rhs[:rhs.index('//')]
    
    tokens = []
    i = 0
    while i < len(rhs):
        # Skip whitespace
        if rhs[i].isspace():
            i += 1
            continue
        
        # Handle quoted strings (terminals)
        if rhs[i] == '"':
            j = i + 1
            while j < len(rhs) and rhs[j] != '"':
                if rhs[j] == '\\':
                    j += 2
                else:
                    j += 1
            token = rhs[i+1:j]
            tokens.append(('TERMINAL', token))
            i = j + 1
            continue
        
        # Handle identifiers (nonterminals or terminal names)
        if rhs[i].isalnum() or rhs[i] == '_':
            j = i
            while j < len(rhs) and (rhs[j].isalnum() or rhs[j] == '_'):
                j += 1
            token = rhs[i:j]
            tokens.append(('SYMBOL', token))
            i = j
            continue
        
        # Handle operators (multi-char first)
        multi_ops = ['++', '--', '+=', '-=', '*=', '/=', '%=', '==', '!=', '<=', '>=', '&&', '||', '<<', '>>', '->']
        found = False
        for op in multi_ops:
            if rhs[i:i+len(op)] == op:
                tokens.append(('TERMINAL', op))
                i += len(op)
                found = True
                break
        if found:
            continue
        
        # Single char operators/delimiters
        if rhs[i] in '+-*/%=<>!&|^~(){}[];,.:?':
            tokens.append(('TERMINAL', rhs[i]))
            i += 1
            continue
        
        i += 1
    
    return tokens

def compute_first_sets(rules):
    """Compute FIRST sets for all nonterminals."""
    nonterminals = set(rules.keys())
    
    # Known terminal keywords
    terminal_keywords = {
        'int', 'long', 'float', 'double', 'char', 'string', 'bool', 'void', 'weave',
        'global', 'local', 'func', 'main', 'return', 'if', 'else', 'while', 'do', 'for',
        'switch', 'case', 'default', 'break', 'thread', 'threadln', 'trap', 'using',
        'var', 'const', 'true', 'false', 'null',
        'intlit', 'longlit', 'floatlit', 'doublelit', 'charlit', 'stringlit', 'id',
    }
    
    # Initialize FIRST sets
    first = defaultdict(set)
    
    # Iterate until no changes
    changed = True
    iterations = 0
    max_iterations = 100
    
    while changed and iterations < max_iterations:
        changed = False
        iterations += 1
        
        for nt, productions in rules.items():
            for prod in productions:
                tokens = tokenize_rhs(prod)
                
                if not tokens:
                    # Empty production (epsilon)
                    if 'λ' not in first[nt]:
                        first[nt].add('λ')
                        changed = True
                    continue
                
                # Process first symbol
                for tok_type, tok_val in tokens:
                    if tok_type == 'TERMINAL':
                        if tok_val not in first[nt]:
                            first[nt].add(tok_val)
                            changed = True
                        break
                    else:  # SYMBOL
                        if tok_val in terminal_keywords:
                            # It's a terminal keyword
                            if tok_val not in first[nt]:
                                first[nt].add(tok_val)
                                changed = True
                            break
                        elif tok_val in nonterminals:
                            # It's a nonterminal
                            for sym in first[tok_val]:
                                if sym != 'λ' and sym not in first[nt]:
                                    first[nt].add(sym)
                                    changed = True
                            # If epsilon in FIRST of this nonterminal, continue to next symbol
                            if 'λ' not in first[tok_val]:
                                break
                        else:
                            # Unknown symbol - treat as terminal
                            if tok_val not in first[nt]:
                                first[nt].add(tok_val)
                                changed = True
                            break
                else:
                    # All symbols can derive epsilon
                    if 'λ' not in first[nt]:
                        first[nt].add('λ')
                        changed = True
    
    return dict(first)

def get_first_of_production(prod, first_sets, terminal_keywords, nonterminals):
    """Get FIRST set of a specific production."""
    tokens = tokenize_rhs(prod)
    
    if not tokens:
        return {'λ'}
    
    result = set()
    
    for tok_type, tok_val in tokens:
        if tok_type == 'TERMINAL':
            result.add(tok_val)
            return result
        else:  # SYMBOL
            if tok_val in terminal_keywords:
                result.add(tok_val)
                return result
            elif tok_val in nonterminals:
                result.update(first_sets.get(tok_val, set()) - {'λ'})
                if 'λ' not in first_sets.get(tok_val, set()):
                    return result
            else:
                result.add(tok_val)
                return result
    
    # All symbols can derive epsilon
    result.add('λ')
    return result

def format_rhs_for_markdown(prod, nonterminals):
    """Format production RHS for markdown display."""
    tokens = tokenize_rhs(prod)
    
    if not tokens:
        return 'λ'
    
    parts = []
    for tok_type, tok_val in tokens:
        if tok_type == 'TERMINAL':
            parts.append(tok_val)
        else:
            if tok_val in nonterminals:
                parts.append(f'`<{tok_val}>`')
            else:
                parts.append(tok_val)
    
    return ' '.join(parts)

def generate_first_md(rules, first_sets, output_path):
    """Generate the FIRST set markdown documentation."""
    terminal_keywords = {
        'int', 'long', 'float', 'double', 'char', 'string', 'bool', 'void', 'weave',
        'global', 'local', 'func', 'main', 'return', 'if', 'else', 'while', 'do', 'for',
        'switch', 'case', 'default', 'break', 'thread', 'threadln', 'trap', 'using',
        'var', 'const', 'true', 'false', 'null',
        'intlit', 'longlit', 'floatlit', 'doublelit', 'charlit', 'stringlit', 'id',
    }
    nonterminals = set(rules.keys())
    
    lines = [
        '## FIRST Set',
        '',
        '| # | Production | -> | FIRST Set |',
        '|---|------------|-----|-----------|',
    ]
    
    prod_num = 1
    for nt in rules.keys():
        for prod in rules[nt]:
            first_of_prod = get_first_of_production(prod, first_sets, terminal_keywords, nonterminals)
            formatted_rhs = format_rhs_for_markdown(prod, nonterminals)
            first_str = '{ ' + ', '.join(sorted(first_of_prod)) + ' }'
            lines.append(f'| {prod_num} | `<{nt}>` | -> | {first_str} |')
            prod_num += 1
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return prod_num - 1

if __name__ == '__main__':
    lark_path = r'C:/Users/Hardy/OneDrive/Desktop/portia-compiler/parser-backend/parser/portia.lark'
    output_path = r'C:/Users/Hardy/OneDrive/Desktop/portia-compiler/parser-backend/parser/documentation/portia-first.md'
    
    print('Parsing grammar...')
    rules = parse_lark_grammar(lark_path)
    print(f'Found {len(rules)} nonterminals')
    
    print('Computing FIRST sets...')
    first_sets = compute_first_sets(rules)
    
    print('Generating documentation...')
    num_prods = generate_first_md(rules, first_sets, output_path)
    print(f'Generated {num_prods} productions in portia-first.md')
