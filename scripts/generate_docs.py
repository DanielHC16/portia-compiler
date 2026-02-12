#!/usr/bin/env python3
"""
Generate documentation files from portia.lark grammar.
Creates portia-cfg.md, portia-first.md, and portia-predict.md.
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Set

# Terminal mapping: Lark uppercase -> display form
TERMINAL_MAP = {
    'GLOBAL': 'global', 'LOCAL': 'local', 'FUNC': 'func', 'RETURN': 'return',
    'IF': 'if', 'ELSE': 'else', 'SWITCH': 'switch', 'CASE': 'case',
    'DEFAULT': 'default', 'FOR': 'for', 'WHILE': 'while', 'DO': 'do',
    'BREAK': 'break', 'TRAP': 'trap', 'THREAD': 'thread', 'THREADLN': 'threadln',
    'USING': 'using', 'WEAVE': 'weave', 'MAIN': 'main',
    'INT': 'int', 'LONG': 'long', 'FLOAT': 'float', 'DOUBLE': 'double',
    'CHAR': 'char', 'STRING': 'string', 'BOOL': 'bool', 'VOID': 'void',
    'VAR': 'var', 'CONST': 'const', 'TRUE': 'true', 'FALSE': 'false',
    'ASSIGN': '=', 'PLUSEQ': '+=', 'MINUSEQ': '-=',
    'STAREQ': '*=', 'SLASHEQ': '/=', 'MODEQ': '%=',
    'EQ': '==', 'NEQ': '!=', 'LT': '<', 'GT': '>', 'LTE': '<=', 'GTE': '>=',
    'AND': '&&', 'OR': '||', 'NOT': '!',
    'PLUS': '+', 'MINUS': '-', 'STAR': '*', 'SLASH': '/', 'MOD': '%',
    'INCR': '++', 'DECR': '--', 'CONCAT': '..',
    'LPAREN': '(', 'RPAREN': ')', 'LBRACE': '{', 'RBRACE': '}',
    'LBRACK': '[', 'RBRACK': ']', 'SEMICOLON': ';', 'COMMA': ',',
    'COLON': ':', 'DOT': '.',
    'ID': 'id', 'INTLIT': 'intlit', 'LONGLIT': 'longlit',
    'FLOATLIT': 'floatlit', 'DOUBLELIT': 'doublelit',
    'CHARLIT': 'charlit', 'STRINGLIT': 'stringlit',
}

def parse_lark_grammar(content: str) -> List[Tuple[str, List[str]]]:
    """Parse Lark grammar and extract all productions."""
    productions = []
    
    # Remove comments
    content = re.sub(r'//[^\n]*', '', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    lines = content.split('\n')
    current_rule = None
    current_body_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines, terminal definitions, and special lines
        if not stripped or stripped.startswith('%') or stripped.startswith('?'):
            i += 1
            continue
            
        # Check for terminal definition (UPPERCASE: "...")
        if re.match(r'^[A-Z][A-Z_0-9]*\s*:', stripped):
            # Save previous rule
            if current_rule is not None:
                prods = parse_rule_body(current_rule, current_body_lines)
                productions.extend(prods)
            current_rule = None
            current_body_lines = []
            i += 1
            continue
            
        # Check for rule definition start (lowercase: ...)
        rule_match = re.match(r'^([a-z][a-z0-9_]*)\s*:\s*(.*)', stripped)
        if rule_match:
            # Save previous rule
            if current_rule is not None:
                prods = parse_rule_body(current_rule, current_body_lines)
                productions.extend(prods)
            
            current_rule = rule_match.group(1)
            rest = rule_match.group(2)
            current_body_lines = [rest] if rest else []
            i += 1
            continue
        
        # Check for continuation of current rule (| alternative or continued line)
        if current_rule is not None:
            current_body_lines.append(stripped)
        
        i += 1
    
    # Save last rule
    if current_rule is not None:
        prods = parse_rule_body(current_rule, current_body_lines)
        productions.extend(prods)
    
    return productions

def parse_rule_body(rule_name: str, body_lines: List[str]) -> List[Tuple[str, str]]:
    """Parse rule body lines into individual productions."""
    productions = []
    
    # Join all lines and split by |
    full_body = ' '.join(body_lines)
    
    # Split alternatives by | at top level (respecting parentheses)
    alts = split_alternatives(full_body)
    
    for alt in alts:
        alt = alt.strip()
        # Empty alternative = epsilon production
        if not alt:
            productions.append((rule_name, 'EPSILON'))
        else:
            productions.append((rule_name, alt))
    
    return productions

def split_alternatives(body: str) -> List[str]:
    """Split a rule body by | while respecting parentheses."""
    alts = []
    current = []
    depth = 0
    
    tokens = body.split()
    for token in tokens:
        depth += token.count('(') - token.count(')')
        depth += token.count('[') - token.count(']')
        depth += token.count('{') - token.count('}')
        
        if token == '|' and depth == 0:
            # Always add an alternative when we see |
            # This includes empty alternatives (epsilon)
            alts.append(' '.join(current) if current else '')
            current = []
        else:
            current.append(token)
    
    # Add the last alternative
    alts.append(' '.join(current) if current else '')
    
    return alts

def format_symbol(symbol: str) -> str:
    """Format a symbol for display."""
    if symbol in TERMINAL_MAP:
        return TERMINAL_MAP[symbol]
    elif symbol.islower() or '_' in symbol:
        return f'`<{symbol}>`'
    return symbol

def format_production(symbols: List[str]) -> str:
    """Format a production body for display."""
    result = []
    for sym in symbols:
        if sym in TERMINAL_MAP:
            result.append(TERMINAL_MAP[sym])
        elif sym.islower() or (sym[0].islower() and '_' in sym):
            result.append(f'`<{sym}>`')
        else:
            result.append(sym.lower())
    return ' '.join(result)

def escape_pipe(s: str) -> str:
    """Escape pipe characters for markdown tables."""
    return s.replace('|', '\\|')

def parse_production_body(body: str) -> List[str]:
    """Parse production body into tokens."""
    # Handle empty production
    if not body.strip() or body == 'EPSILON':
        return ['λ']
    
    tokens = body.split()
    return tokens

def extract_first_symbol(tokens: List[str]) -> str:
    """Extract the FIRST symbol from a production."""
    if not tokens or tokens == ['λ']:
        return 'λ'
    return format_symbol(tokens[0]) if tokens[0] in TERMINAL_MAP else f'`<{tokens[0]}>`'

def is_terminal(symbol: str) -> bool:
    """Check if a symbol is a terminal."""
    return symbol in TERMINAL_MAP or symbol == 'EPSILON'

def compute_all_first_sets(productions: List[Tuple[str, str]]) -> Dict[str, Set[str]]:
    """Compute FIRST sets for all nonterminals using fixed-point iteration."""
    # Build production map
    prod_map = {}
    for rule, body in productions:
        if rule not in prod_map:
            prod_map[rule] = []
        tokens = parse_production_body(body)
        prod_map[rule].append(tokens)
    
    nonterminals = set(prod_map.keys())
    first_sets = {nt: set() for nt in nonterminals}
    
    # Fixed-point iteration
    changed = True
    iterations = 0
    while changed and iterations < 100:
        changed = False
        iterations += 1
        
        for nt, alternatives in prod_map.items():
            for tokens in alternatives:
                if tokens == ['λ']:
                    if 'λ' not in first_sets[nt]:
                        first_sets[nt].add('λ')
                        changed = True
                else:
                    # Process each symbol in the production
                    for tok in tokens:
                        if tok in TERMINAL_MAP:
                            # Terminal - add it to FIRST set
                            term = TERMINAL_MAP[tok]
                            if term not in first_sets[nt]:
                                first_sets[nt].add(term)
                                changed = True
                            break  # Stop after first terminal
                        elif tok in nonterminals:
                            # Non-terminal - add its FIRST set (except λ)
                            for sym in first_sets[tok]:
                                if sym != 'λ' and sym not in first_sets[nt]:
                                    first_sets[nt].add(sym)
                                    changed = True
                            # If ε not in FIRST(tok), stop
                            if 'λ' not in first_sets[tok]:
                                break
                        else:
                            # Unknown symbol - treat as terminal
                            if tok not in first_sets[nt]:
                                first_sets[nt].add(tok)
                                changed = True
                            break
                    else:
                        # All symbols can derive ε
                        if 'λ' not in first_sets[nt]:
                            first_sets[nt].add('λ')
                            changed = True
    
    return first_sets

def get_first_of_production(tokens: List[str], first_sets: Dict[str, Set[str]]) -> Set[str]:
    """Get FIRST set of a specific production."""
    if tokens == ['λ']:
        return {'λ'}
    
    result = set()
    nonterminals = set(first_sets.keys())
    
    for tok in tokens:
        if tok in TERMINAL_MAP:
            result.add(TERMINAL_MAP[tok])
            return result
        elif tok in nonterminals:
            result.update(first_sets[tok] - {'λ'})
            if 'λ' not in first_sets[tok]:
                return result
        else:
            result.add(tok)
            return result
    
    # All can derive ε
    result.add('λ')
    return result

def compute_all_follow_sets(productions: List[Tuple[str, str]], first_sets: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """Compute FOLLOW sets for all nonterminals."""
    # Build production map
    prod_map = {}
    for rule, body in productions:
        if rule not in prod_map:
            prod_map[rule] = []
        tokens = parse_production_body(body)
        prod_map[rule].append(tokens)
    
    nonterminals = set(prod_map.keys())
    follow_sets = {nt: set() for nt in nonterminals}
    
    # Start symbol gets $END
    start = 'program'
    if start in follow_sets:
        follow_sets[start].add('$END')
    
    # Fixed-point iteration
    changed = True
    iterations = 0
    while changed and iterations < 100:
        changed = False
        iterations += 1
        
        for rule, alternatives in prod_map.items():
            for tokens in alternatives:
                if tokens == ['λ']:
                    continue
                
                for i, tok in enumerate(tokens):
                    if tok not in nonterminals:
                        continue
                    
                    # Get β (everything after this nonterminal)
                    beta = tokens[i+1:]
                    
                    if beta:
                        # Add FIRST(β) - {ε} to FOLLOW(tok)
                        first_beta = get_first_of_list(beta, first_sets, nonterminals)
                        for sym in first_beta:
                            if sym != 'λ' and sym not in follow_sets[tok]:
                                follow_sets[tok].add(sym)
                                changed = True
                        
                        # If ε in FIRST(β), add FOLLOW(rule) to FOLLOW(tok)
                        if 'λ' in first_beta:
                            for sym in follow_sets[rule]:
                                if sym not in follow_sets[tok]:
                                    follow_sets[tok].add(sym)
                                    changed = True
                    else:
                        # Nothing after tok, add FOLLOW(rule) to FOLLOW(tok)
                        for sym in follow_sets[rule]:
                            if sym not in follow_sets[tok]:
                                follow_sets[tok].add(sym)
                                changed = True
    
    return follow_sets

def get_first_of_list(tokens: List[str], first_sets: Dict[str, Set[str]], nonterminals: Set[str]) -> Set[str]:
    """Get FIRST set of a list of symbols."""
    result = set()
    
    for tok in tokens:
        if tok in TERMINAL_MAP:
            result.add(TERMINAL_MAP[tok])
            return result
        elif tok in nonterminals:
            result.update(first_sets[tok] - {'λ'})
            if 'λ' not in first_sets[tok]:
                return result
        else:
            result.add(tok)
            return result
    
    result.add('λ')
    return result

def generate_cfg_doc(productions: List[Tuple[str, str]]) -> str:
    """Generate portia-cfg.md content."""
    lines = [
        "## Context-Free Grammar",
        "",
        "| # | Production | -> | Production Set |",
        "|---|------------|-----|----------------|",
    ]
    
    for i, (rule, body) in enumerate(productions, 1):
        tokens = parse_production_body(body)
        if tokens == ['λ']:
            prod_str = 'λ'
        else:
            prod_str = escape_pipe(format_production(tokens))
        
        lines.append(f"| {i} | `<{rule}>` | -> | {prod_str} |")
    
    return '\n'.join(lines)

def generate_first_doc(productions: List[Tuple[str, str]], first_sets: Dict[str, Set[str]]) -> str:
    """Generate portia-first.md content."""
    lines = [
        "## FIRST Set",
        "",
        "| # | Production | -> | FIRST Set |",
        "|---|------------|-----|-----------|",
    ]
    
    for i, (rule, body) in enumerate(productions, 1):
        tokens = parse_production_body(body)
        first_set = get_first_of_production(tokens, first_sets)
        first_str = escape_pipe('{ ' + ', '.join(sorted(first_set)) + ' }')
        
        lines.append(f"| {i} | `<{rule}>` | -> | {first_str} |")
    
    return '\n'.join(lines)

def generate_follow_doc(productions: List[Tuple[str, str]], follow_sets: Dict[str, Set[str]]) -> str:
    """Generate portia-follow.md content."""
    lines = [
        "## FOLLOW Set",
        "",
        "| # | Nonterminal | FOLLOW Set |",
        "|---|-------------|------------|",
    ]
    
    # Get unique nonterminals in order
    seen = set()
    nonterminals = []
    for rule, _ in productions:
        if rule not in seen:
            seen.add(rule)
            nonterminals.append(rule)
    
    for i, nt in enumerate(nonterminals, 1):
        follow_set = follow_sets.get(nt, set())
        follow_str = escape_pipe('{ ' + ', '.join(sorted(follow_set)) + ' }') if follow_set else '{ }'
        lines.append(f"| {i} | `<{nt}>` | {follow_str} |")
    
    return '\n'.join(lines)

def generate_predict_doc(productions: List[Tuple[str, str]], first_sets: Dict[str, Set[str]], follow_sets: Dict[str, Set[str]]) -> str:
    """Generate portia-predict.md content."""
    lines = [
        "## PREDICT Set",
        "",
        "| # | Production | Calculation | PREDICT Set |",
        "|---|------------|-------------|-------------|",
    ]
    
    for i, (rule, body) in enumerate(productions, 1):
        tokens = parse_production_body(body)
        if tokens == ['λ']:
            prod_str = 'λ'
            calc = f'FOLLOW(`<{rule}>`)'
            # PREDICT = FOLLOW for epsilon productions
            predict_set = follow_sets.get(rule, set())
        else:
            prod_str = escape_pipe(format_production(tokens))
            first_token = tokens[0]
            if first_token in TERMINAL_MAP:
                calc = escape_pipe(f'FIRST({TERMINAL_MAP[first_token]})')
            else:
                calc = f'FIRST(`<{first_token}>`)'
            
            # PREDICT = FIRST for non-epsilon productions
            predict_set = get_first_of_production(tokens, first_sets)
            # If FIRST contains ε, add FOLLOW
            if 'λ' in predict_set:
                predict_set = predict_set - {'λ'}
                predict_set.update(follow_sets.get(rule, set()))
        
        predict_str = escape_pipe('{ ' + ', '.join(sorted(predict_set)) + ' }') if predict_set else '{ λ }'
        
        lines.append(f"| {i} | `<{rule}>` → {prod_str} | {calc} | {predict_str} |")
    
    return '\n'.join(lines)

def main():
    script_dir = Path(__file__).parent.parent
    lark_path = script_dir / 'parser-backend' / 'parser' / 'portia.lark'
    doc_dir = script_dir / 'parser-backend' / 'parser' / 'documentation'
    
    print(f"Reading grammar from: {lark_path}")
    with open(lark_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Parsing grammar...")
    productions = parse_lark_grammar(content)
    print(f"Found {len(productions)} productions")
    
    print("Computing FIRST sets...")
    first_sets = compute_all_first_sets(productions)
    
    print("Computing FOLLOW sets...")
    follow_sets = compute_all_follow_sets(productions, first_sets)
    
    # Generate and save documentation
    print("Generating portia-cfg.md...")
    cfg_content = generate_cfg_doc(productions)
    with open(doc_dir / 'portia-cfg.md', 'w', encoding='utf-8') as f:
        f.write(cfg_content)
    
    print("Generating portia-first.md...")
    first_content = generate_first_doc(productions, first_sets)
    with open(doc_dir / 'portia-first.md', 'w', encoding='utf-8') as f:
        f.write(first_content)
    
    print("Generating portia-follow.md...")
    follow_content = generate_follow_doc(productions, follow_sets)
    with open(doc_dir / 'portia-follow.md', 'w', encoding='utf-8') as f:
        f.write(follow_content)
    
    print("Generating portia-predict.md...")
    predict_content = generate_predict_doc(productions, first_sets, follow_sets)
    with open(doc_dir / 'portia-predict.md', 'w', encoding='utf-8') as f:
        f.write(predict_content)
    
    print("Done!")
    print(f"Total productions: {len(productions)}")
    print(f"Total nonterminals: {len(first_sets)}")

if __name__ == '__main__':
    main()
