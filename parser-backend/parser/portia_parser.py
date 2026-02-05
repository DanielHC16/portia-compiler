from typing import List, Dict, Any
from lark import Lark, UnexpectedInput, UnexpectedToken, Token, Tree, Transformer
from pathlib import Path

class PortiaLarkParser:
    def __init__(self):
        grammar_path = Path(__file__).parent / "portia.lark"
        with open(grammar_path, 'r', encoding='utf-8') as f:
            grammar = f.read()
        
        # Lark parses source code (we reconstruct from tokens)
        # Grammar terminals use actual source literals
        # Using Earley parser with explicit ambiguity handling for CFG compliance
        self.parser = Lark(
            grammar,
            parser='earley',
            ambiguity='explicit',
            start='program',
            propagate_positions=True,
            lexer='basic',
            keep_all_tokens=True
        )
        
        # Track ambiguities encountered during parsing
        self.ambiguities_found = []
        
        # Map Lark terminal names -> Lexer token types
        # This ensures error messages show lexer token types
        self.terminal_to_lexer_type = self._build_terminal_map()
        self.token_to_symbol = self._build_symbol_map()
    
    def _build_symbol_map(self) -> Dict[str, str]:
        """
        Map token names to their actual symbols for display in error messages.
        Only includes punctuation and operators - keywords and identifiers use their names.
        """
        return {
            "semicolon": ";", "comma": ",", "colon": ":", "dot": ".",
            "open_paren": "(", "close_paren": ")",
            "open_brace": "{", "close_brace": "}",
            "open_bracket": "[", "close_bracket": "]",
            "assign": "=", "add_assign": "+=", "minus_assign": "-=",
            "mult_assign": "*=", "div_assign": "/=", "modulo_assign": "%=",
            "equal": "==", "not_equal": "!=",
            "less_than": "<", "greater_than": ">",
            "less_equal": "<=", "greater_equal": ">=",
            "logical_and": "&&", "logical_or": "||", "logical_not": "!",
            "add": "+", "subtract": "-", "multiply": "*", "divide": "/",
            "modulo": "%", "increment": "++", "decrement": "--", "concat": "..",
        }
    
    def _build_terminal_map(self) -> Dict[str, str]:
        """
        Map Lark terminal names (uppercase) to lexer token types (lowercase).
        Used for CFG-compliant error messages.
        """
        return {
            "GLOBAL": "global", "LOCAL": "local", "FUNC": "func", "RETURN": "return",
            "IF": "if", "ELSE": "else", "SWITCH": "switch", "CASE": "case",
            "DEFAULT": "default", "FOR": "for", "WHILE": "while", "DO": "do",
            "BREAK": "break", "TRAP": "trap", "THREAD": "thread", "THREADLN": "threadln",
            "USING": "using", "WEAVE": "weave", "MAIN": "main",
            "INT": "int", "LONG": "long", "FLOAT": "float", "DOUBLE": "double",
            "CHAR": "char", "STRING": "string", "BOOL": "bool", "VOID": "void",
            "VAR": "var", "CONST": "const", "TRUE": "true", "FALSE": "false",
            "ASSIGN": "assign", "PLUSEQ": "add_assign", "MINUSEQ": "minus_assign",
            "STAREQ": "mult_assign", "SLASHEQ": "div_assign", "MODEQ": "modulo_assign",
            "EQ": "equal", "NEQ": "not_equal", "LT": "less_than",
            "GT": "greater_than", "LTE": "less_equal", "GTE": "greater_equal",
            "AND": "logical_and", "OR": "logical_or", "NOT": "logical_not",
            "PLUS": "add", "MINUS": "subtract", "STAR": "multiply", "SLASH": "divide",
            "MOD": "modulo", "INCR": "increment", "DECR": "decrement", "CONCAT": "concat",
            "LPAREN": "open_paren", "RPAREN": "close_paren", "LBRACE": "open_brace",
            "RBRACE": "close_brace", "LBRACK": "open_bracket", "RBRACK": "close_bracket",
            "SEMICOLON": "semicolon", "COMMA": "comma", "COLON": "colon", "DOT": "dot",
            "ID": "id", "INTLIT": "intlit", "LONGLIT": "longlit",
            "FLOATLIT": "floatlit", "DOUBLELIT": "doublelit",
            "CHARLIT": "charlit", "STRINGLIT": "stringlit",
        }
    
    def _format_token_for_display(self, token_name: str) -> str:
        """
        Format a token name for display in error messages.
        Uses actual symbols for punctuation/operators, names for keywords/identifiers.
        """
        return self.token_to_symbol.get(token_name, token_name)
    
    def _detect_ambiguities(self, trees: List) -> None:
        """
        Analyze multiple parse trees to identify ambiguous nonterminals.
        Collects ambiguity information for later cleanup.
        """
        if len(trees) < 2:
            return
        
        # Compare trees to find divergence points
        def get_rule_paths(tree, path=""):
            """Extract all rule application paths from a tree."""
            paths = set()
            if hasattr(tree, 'data'):
                current_path = f"{path}/{tree.data}" if path else tree.data
                paths.add(current_path)
                if hasattr(tree, 'children'):
                    for child in tree.children:
                        paths.update(get_rule_paths(child, current_path))
            return paths
        
        # Get paths for each tree
        tree_paths = [get_rule_paths(tree) for tree in trees]
        
        # Find divergent rules (present in some trees but not all)
        all_rules = set().union(*tree_paths)
        for rule_path in all_rules:
            # Count how many trees have this rule path
            count = sum(1 for paths in tree_paths if rule_path in paths)
            if count < len(trees):
                # This rule appears in some but not all trees - ambiguous
                rule_name = rule_path.split('/')[-1]
                if rule_name not in [a['nonterminal'] for a in self.ambiguities_found]:
                    self.ambiguities_found.append({
                        'nonterminal': rule_name,
                        'path': rule_path,
                        'tree_count': len(trees)
                    })
    
    def _build_source_from_tokens(self, tokens: List[Dict[str, Any]]) -> str:
        """
        Reconstruct source code from lexer tokens PRESERVING LINE STRUCTURE.
        CRITICAL: Must maintain line breaks so Lark's line numbers match original source.
        """
        # Store tokens for position lookup during error handling
        self._original_tokens = tokens
        self._tokens_by_line = {}
        for token in tokens:
            token_type = token.get("type", "")
            if token_type in ["space", "newline", "tab", "single_comment", "multi_comment"]:
                continue
            line_num = token.get("line", 1)
            if line_num not in self._tokens_by_line:
                self._tokens_by_line[line_num] = []
            self._tokens_by_line[line_num].append(token)
        
        # Group tokens by line number
        lines_dict = {}
        
        for token in tokens:
            token_type = token.get("type", "")
            lexeme = token.get("lexeme", "")
            line_num = token.get("line", 1)
            
            # Skip whitespace/comments - Lark will handle them via %ignore
            if token_type in ["space", "newline", "tab", "single_comment", "multi_comment"]:
                continue
            
            if lexeme:
                if line_num not in lines_dict:
                    lines_dict[line_num] = []
                lines_dict[line_num].append(lexeme)
        
        # Reconstruct source maintaining line structure
        max_line = max(lines_dict.keys()) if lines_dict else 1
        reconstructed_lines = []
        
        for line_num in range(1, max_line + 1):
            if line_num in lines_dict:
                # Join tokens on same line with spaces
                reconstructed_lines.append(" ".join(lines_dict[line_num]))
            else:
                # Empty line (all tokens were comments/whitespace)
                reconstructed_lines.append("")
        
        # Join lines with newlines - Lark now sees multi-line source
        return "\n".join(reconstructed_lines)
    
    def _lookup_original_token(self, line: int, lexeme: str, lark_column: int = None) -> Dict[str, Any]:
        """
        Look up the original token by line and lexeme value.
        If lark_column is provided, finds the token closest to that column position.
        Returns original token dict with correct column, or None if not found.
        """
        if not hasattr(self, '_tokens_by_line') or line not in self._tokens_by_line:
            return None
        
        # Find all tokens matching the lexeme on this line
        matching_tokens = [t for t in self._tokens_by_line[line] if t.get("lexeme") == lexeme]
        
        if not matching_tokens:
            return None
        
        if len(matching_tokens) == 1:
            return matching_tokens[0]
        
        # Multiple matches - use lark_column to find the closest one
        if lark_column is not None:
            # Find token with column closest to lark_column
            best_match = min(matching_tokens, key=lambda t: abs(t.get("column", 0) - lark_column))
            return best_match
        
        # Fallback to first match
        return matching_tokens[0]
    
    def parse(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse tokens using Lark with CFG compliance.
        Returns dict with success status, AST, and errors.
        """
        try:
            # Reconstruct source from tokens
            source = self._build_source_from_tokens(tokens)
            
            # Parse with Earley - may return multiple trees if ambiguous
            tree = self.parser.parse(source)
            
            # Check for ambiguity - Earley with ambiguity='explicit' returns _ambig object
            if hasattr(tree, 'data') and tree.data == '_ambig':
                # Ambiguous parse detected - tree.children contains all alternatives
                trees = list(tree.children)
                self._detect_ambiguities(trees)
                # Use first tree for now
                tree = trees[0]
            
            # Transform tree to AST with exact lexer token data
            transformer = ASTTransformer(tokens)
            ast_dict = transformer.transform(tree)
            
            result = {
                "success": True,
                "status": "success",
                "ast": ast_dict,
                "errors": [],
                "token_count": len(tokens)
            }
            
            # Include ambiguity warnings if any found
            if self.ambiguities_found:
                result["ambiguities"] = self.ambiguities_found
            
            return result
            
        except UnexpectedToken as e:
            # CFG-driven syntax error with PREDICT set expectations
            return self.handle_unexpected_token(e, tokens)
        
        except UnexpectedInput as e:
            # General Lark parsing error - find furthest failure
            return self.handle_unexpected_input(e, tokens)
        
        except Exception as e:
            # Unexpected error
            return {
                "success": False,
                "status": "error",
                "ast": None,
                "errors": [{
                    "message": f"Internal parser error: {str(e)}",
                    "line": 0,
                    "column": 0,
                    "token": "",
                    "type": "internal_error"
                }],
                "token_count": len(tokens)
            }
    
    def handle_unexpected_token(self, error: UnexpectedToken, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle UnexpectedToken error with CFG-compliant error reporting.
        Maps Lark terminal names to lexer token types.
        Filters expected tokens based on parse context for clearer errors.
        """
        unexpected_token = error.token
        expected = list(error.expected) if hasattr(error, 'expected') else []
        
        # Map Lark terminal names to lexer token types
        expected_lexer_types = []
        for lark_terminal in expected:
            lexer_type = self.terminal_to_lexer_type.get(lark_terminal, lark_terminal)
            expected_lexer_types.append(lexer_type)
        
        # Filter expected tokens based on context to reduce noise
        expected_lexer_types = self._filter_expected_tokens(expected_lexer_types, error)
        
        expected_lexer_types = sorted(set(expected_lexer_types))
        
        # Format expected tokens for display (symbols for punctuation, names for keywords)
        if not expected_lexer_types:
            # No expected tokens means EOF was expected (end of program)
            expected_str = "[ <EOF> (end of file) ]"
        else:
            expected_display = [self._format_token_for_display(t) for t in expected_lexer_types]
            expected_str = f"[ {', '.join(expected_display)} ]"
        
        # Get actual token info and map to lexer type
        token_type_lark = unexpected_token.type if hasattr(unexpected_token, 'type') else "unknown"
        token_type = self.terminal_to_lexer_type.get(token_type_lark, token_type_lark)
        token_type_display = self._format_token_for_display(token_type)
        token_value = unexpected_token.value if hasattr(unexpected_token, 'value') else ""
        lark_line = unexpected_token.line if hasattr(unexpected_token, 'line') else 0
        lark_column = unexpected_token.column if hasattr(unexpected_token, 'column') else 0
        token_length = len(token_value) if token_value else 1
        
        # Look up original token to get correct column position
        original_token = self._lookup_original_token(lark_line, token_value, lark_column)
        if original_token:
            line = original_token.get("line", lark_line)
            column = original_token.get("column", lark_column)
        else:
            line = lark_line
            column = lark_column
        
        # Format unexpected token: if display is a symbol matching the value, don't duplicate
        if token_type_display == token_value:
            unexpected_str = f"[ {token_value} ]"
        else:
            unexpected_str = f"{token_type_display} [ {token_value} ]"
        
        # Single-line format with Unexpected first, then Expected
        message = f"Syntax Error at line {line}, column {column}. Unexpected: {unexpected_str}. Expected: {expected_str}."
        
        return {
            "success": False,
            "status": "error",
            "ast": None,
            "errors": [{
                "message": message,
                "line": line,
                "column": column,
                "token": token_type,  # Use lexer token TYPE
                "token_length": token_length,  # Length for exact highlighting
                "type": "syntax_error"
            }],
            "token_count": len(tokens)
        }
    
    def _filter_expected_tokens(self, expected_tokens: List[str], error) -> List[str]:
        """
        Filter expected tokens based on parse context to provide clearer error messages.
        Prioritizes statement terminators and structural tokens over operators.
        """
        if not expected_tokens:
            return expected_tokens
        
        # Define priority groups (higher priority = more important to show)
        statement_terminators = {'semicolon', 'close_brace', 'close_paren', 'close_bracket'}
        structural_keywords = {'return', 'if', 'else', 'for', 'while', 'do', 'break', 'local', 'using'}
        operators = {'add', 'subtract', 'multiply', 'divide', 'modulo', 'equal', 'not_equal', 
                    'less_than', 'greater_than', 'less_equal', 'greater_equal', 
                    'logical_and', 'logical_or', 'logical_not'}
        
        # If statement terminators are in the expected list, prioritize them
        terminators_present = [t for t in expected_tokens if t in statement_terminators]
        if terminators_present:
            # If we have terminators + many operators, filter to just terminators
            operators_present = [t for t in expected_tokens if t in operators]
            if len(operators_present) >= 3 and len(terminators_present) >= 1:
                # Many operators + terminator = likely missing terminator
                # Keep only terminators and a few key tokens
                non_operators = [t for t in expected_tokens if t not in operators]
                return non_operators if non_operators else expected_tokens
        
        # If we have too many operators, group them
        if len([t for t in expected_tokens if t in operators]) > 5:
            # Keep non-operators and just mention "operator"
            filtered = [t for t in expected_tokens if t not in operators]
            if filtered:
                return filtered
        
        return expected_tokens
    
    def handle_unexpected_input(self, error: UnexpectedInput, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle general UnexpectedInput error.
        Reports the furthest failure point with expected tokens.
        """
        # Try to extract position information from error
        lark_line = getattr(error, 'line', 0)
        lark_column = getattr(error, 'column', 0)
        
        # Try to extract the problematic token
        token_value = ""
        token_type = "unknown"
        token_length = 1
        if hasattr(error, 'token'):
            token = error.token
            token_value = token.value if hasattr(token, 'value') else str(token)
            token_type_lark = token.type if hasattr(token, 'type') else "unknown"
            token_type = self.terminal_to_lexer_type.get(token_type_lark, token_type_lark)
            token_length = len(token_value) if token_value else 1
        
        # Look up original token to get correct column position
        original_token = self._lookup_original_token(lark_line, token_value, lark_column)
        if original_token:
            line = original_token.get("line", lark_line)
            column = original_token.get("column", lark_column)
        else:
            line = lark_line
            column = lark_column
        
        # Try to get expected tokens from parser state
        expected_str = "valid token"
        if hasattr(error, 'expected'):
            expected_lark = list(error.expected) if error.expected else []
            expected_lexer = [self.terminal_to_lexer_type.get(t, t) for t in expected_lark]
            # Apply same filtering
            expected_lexer = self._filter_expected_tokens(expected_lexer, error)
            # Format for display
            expected_display = [self._format_token_for_display(t) for t in sorted(set(expected_lexer))]
            expected_str = f"[ {', '.join(expected_display)} ]"
        
        # Format token type for display
        token_type_display = self._format_token_for_display(token_type)
        
        # Format unexpected token: if display is a symbol matching the value, don't duplicate
        if token_type_display == token_value:
            unexpected_str = f"[ {token_value} ]"
        else:
            unexpected_str = f"{token_type_display} [ {token_value} ]"
        
        # Single-line format with Unexpected first, then Expected
        message = f"Syntax Error at line {line}, column {column}. Unexpected: {unexpected_str}. Expected: {expected_str}."
        
        return {
            "success": False,
            "status": "error",
            "ast": None,
            "errors": [{
                "message": message,
                "line": line,
                "column": column,
                "token": token_type,
                "token_length": token_length,  # Length for exact highlighting
                "type": "syntax_error"
            }],
            "token_count": len(tokens)
        }


class ASTTransformer(Transformer):
    """
    Transforms Lark parse tree to AST.
    CRITICAL: Preserves EXACT lexer token data - no reconstruction.
    """
    
    def __init__(self, original_tokens: List[Dict[str, Any]]):
        super().__init__()
        self.original_tokens = original_tokens
        # Create lookup map: (line, column) -> token
        self.token_map = {}
        # Also create line-based lookup for fallback: line -> [tokens]
        self.line_tokens = {}
        for token in original_tokens:
            line = token.get("line")
            col = token.get("column")
            key = (line, col)
            self.token_map[key] = token
            
            # Build line-based index
            if line not in self.line_tokens:
                self.line_tokens[line] = []
            self.line_tokens[line].append(token)
        
        self._recursion_depth = 0
        self._max_recursion = 1000
    
    def _make_node(self, node_type: str, children: List[Any] = None, token: Token = None) -> Dict[str, Any]:
        """
        Create AST node with exact lexer token data.
        NO reconstruction, NO inference.
        """
        node = {
            "node_type": node_type,
            "children": children or []
        }
        
        # If this node corresponds to a lexer token, preserve ALL token data
        if token:
            # Try exact (line, column) lookup first
            original = self.token_map.get((token.line, token.column))
            
            # Fallback: search for token on same line with matching value
            if not original and token.line in self.line_tokens:
                for candidate in self.line_tokens[token.line]:
                    if candidate.get("lexeme") == token.value:
                        original = candidate
                        break
            
            if original:
                node["token_type"] = original.get("type")
                node["lexeme"] = original.get("lexeme")
                node["line"] = original.get("line")
                node["column"] = original.get("column")
            else:
                # Final fallback to Lark token
                node["token_type"] = token.type
                node["lexeme"] = token.value
                node["line"] = token.line if hasattr(token, 'line') else 0
                node["column"] = token.column if hasattr(token, 'column') else 0
        
        return node
    
    def _transform_children(self, children: List[Any]) -> List[Dict[str, Any]]:
        """Transform child nodes, preserving tokens."""
        self._recursion_depth += 1
        if self._recursion_depth > self._max_recursion:
            raise RecursionError(f"Maximum transformer recursion depth ({self._max_recursion}) exceeded")
        
        try:
            result = []
            for child in children:
                if isinstance(child, Token):
                    # Terminal - create node with exact token data
                    result.append(self._make_node("terminal", [], child))
                elif isinstance(child, Tree):
                    # Non-terminal - recursively call the appropriate transformer method
                    method_name = child.data
                    method = getattr(self, method_name, self.__default__)
                    transformed = method(child.children, child.meta if hasattr(child, 'meta') else None)
                    result.append(transformed)
                elif isinstance(child, dict):
                    # Already transformed
                    result.append(child)
                elif isinstance(child, list):
                    # Flatten lists
                    result.extend(self._transform_children(child))
            return result
        finally:
            self._recursion_depth -= 1
    
    def __default__(self, data: str, children: List[Any], meta):
        """
        Default transformation for any rule.
        Creates node with rule name and transformed children.
        Children are already transformed by Lark before being passed here.
        """
        # Don't call _transform_children - children are already processed
        processed_children = []
        for child in children:
            if isinstance(child, Token):
                processed_children.append(self._make_node("terminal", [], child))
            elif isinstance(child, dict):
                processed_children.append(child)
            else:
                # Shouldn't happen but handle it
                processed_children.append(child)
        
        return self._make_node(data, processed_children)
    
    # Specific transformers for key nodes - all must accept children and meta
    def program(self, children, meta=None):
        processed = [self._make_node("terminal", [], c) if isinstance(c, Token) else c for c in children]
        return self._make_node("program", processed)
    
    def global_dec(self, children, meta=None):
        processed = [self._make_node("terminal", [], c) if isinstance(c, Token) else c for c in children]
        return self._make_node("global_dec", processed)
    
    def function(self, children, meta=None):
        processed = [self._make_node("terminal", [], c) if isinstance(c, Token) else c for c in children]
        return self._make_node("function", processed)
    
    def main_func(self, children, meta=None):
        processed = [self._make_node("terminal", [], c) if isinstance(c, Token) else c for c in children]
        return self._make_node("main_func", processed)
    
    def statement_list(self, children, meta=None):
        processed = [self._make_node("terminal", [], c) if isinstance(c, Token) else c for c in children]
        return self._make_node("statement_list", processed)
    
    def expression(self, children, meta=None):
        # Expressions may be unwrapped by Lark's ?rule syntax
        if len(children) == 1 and isinstance(children[0], dict):
            return children[0]
        processed = [self._make_node("terminal", [], c) if isinstance(c, Token) else c for c in children]
        return self._make_node("expression", processed)
