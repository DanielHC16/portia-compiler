#!/usr/bin/env python3
"""Debug script to see what tokens and AST are produced"""
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lexer-backend"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "parser-backend"))

from app.lexer.portia_lexer import LexicalAnalyzer
from parser.portia_parser import PortiaParser

source = '''int main() {
    local var int x = y;
    return 0;
}'''

lexer = LexicalAnalyzer()
result = lexer.transition(source)
tokens = result.get('tokens', [])
print(f"Total tokens: {len(tokens)}")

parser = PortiaParser(tokens)
tree = parser.parse()
ast = tree.to_dict()

def print_ast(node, indent=0):
    prefix = "  " * indent
    if isinstance(node, dict):
        ntype = node.get("type", "?")
        nval = node.get("value", "")
        children = node.get("children", [])
        if nval:
            print(f"{prefix}{ntype}: {nval!r}")
        else:
            print(f"{prefix}{ntype}")
        for c in children:
            print_ast(c, indent + 1)
    else:
        print(f"{prefix}???{node}")

print("\nAST:")
print_ast(ast)
