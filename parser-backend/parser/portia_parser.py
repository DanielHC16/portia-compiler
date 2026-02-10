"""
PORTIA Parser - CFG-Transparent Implementation
==============================================

This parser is a TRANSPARENT MIRROR of the Lark grammar (portia.lark).
It performs NO filtering, NO context detection, and NO error message manipulation.

All syntax errors report the EXACT PREDICT set from the grammar.
If an unexpected token appears in the expected list, the FIX is in the CFG,
not in Python code.

Architecture Rules:
- The CFG (Lark grammar) is the single source of truth
- Parser does NOT alter, filter, rewrite, or post-process error messages
- All expected tokens come directly from Lark's parser state
- No semantic assistance during parsing (purely syntactic)
"""

from typing import List, Dict, Any
from lark import Lark, UnexpectedInput, UnexpectedToken, Token, Tree, Transformer
from lark.exceptions import UnexpectedEOF
from pathlib import Path


class PortiaLarkParser:
    """
    LALR(1) parser for PORTIA language.
    Wraps Lark parser with transparent error reporting.
    """
    
    def __init__(self):
        grammar_path = Path(__file__).parent / "portia.lark"
        with open(grammar_path, 'r', encoding='utf-8') as f:
            grammar = f.read()
        
        # LALR(1) parser - deterministic, parses all LL(1) grammars
        self.parser = Lark(
            grammar,
            parser='lalr',
            start='start',
            lexer='basic',
            propagate_positions=True
        )
        
        # Terminal name mappings (Lark uppercase -> lexer lowercase)
        self.terminal_to_lexer_type = self._build_terminal_map()
        self.token_to_symbol = self._build_symbol_map()
    
    def _build_symbol_map(self) -> Dict[str, str]:
        """
        Map token names to their actual symbols for display.
        Only punctuation and operators - keywords use their names.
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
            "$END": "EOF",
        }
    
    def _build_terminal_map(self) -> Dict[str, str]:
        """
        Map Lark terminal names (uppercase) to lexer token types (lowercase).
        This is purely cosmetic for error messages - NO filtering.
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
            "$END": "$END",
        }
    
    def _format_token_for_display(self, token_name: str) -> str:
        """Format token name for display (symbols for operators, names for keywords)."""
        return self.token_to_symbol.get(token_name, token_name)
    
    def _build_source_from_tokens(self, tokens: List[Dict[str, Any]]) -> str:
        """
        Reconstruct source code from lexer tokens PRESERVING LINE STRUCTURE.
        Maintains line breaks so Lark's line numbers match original source.
        Also builds a column-to-token mapping for accurate error position lookup.
        """
        self._original_tokens = tokens
        self._tokens_by_line = {}
        # Map (line, reconstructed_col) -> original_token for error lookup
        self._reconstructed_col_to_token = {}
        
        for token in tokens:
            token_type = token.get("type", "")
            if token_type in ["space", "newline", "tab", "single_comment", "multi_comment"]:
                continue
            line_num = token.get("line", 1)
            if line_num not in self._tokens_by_line:
                self._tokens_by_line[line_num] = []
            self._tokens_by_line[line_num].append(token)
        
        # Group tokens by line and track reconstructed positions
        lines_dict = {}
        for token in tokens:
            token_type = token.get("type", "")
            lexeme = token.get("lexeme", "")
            line_num = token.get("line", 1)
            
            if token_type in ["space", "newline", "tab", "single_comment", "multi_comment"]:
                continue
            
            if lexeme:
                if line_num not in lines_dict:
                    lines_dict[line_num] = []
                lines_dict[line_num].append((lexeme, token))
        
        # Reconstruct maintaining line structure and track column mappings
        max_line = max(lines_dict.keys()) if lines_dict else 1
        reconstructed_lines = []
        
        for line_num in range(1, max_line + 1):
            if line_num in lines_dict:
                lexemes = []
                col = 1  # Reconstructed column starts at 1
                for lexeme, token in lines_dict[line_num]:
                    # Map range of columns for this token
                    for offset in range(len(lexeme)):
                        self._reconstructed_col_to_token[(line_num, col + offset)] = token
                    lexemes.append(lexeme)
                    col += len(lexeme) + 1  # +1 for space separator
                reconstructed_lines.append(" ".join(lexemes))
            else:
                reconstructed_lines.append("")
        
        return "\n".join(reconstructed_lines)
    
    def _lookup_original_token(self, line: int, lexeme: str, lark_column: int = None) -> Dict[str, Any]:
        """
        Look up original token by line and Lark's column from reconstructed source.
        Uses the column-to-token mapping built during source reconstruction.
        """
        # First try the direct column mapping
        if lark_column is not None and hasattr(self, '_reconstructed_col_to_token'):
            token = self._reconstructed_col_to_token.get((line, lark_column))
            if token and token.get("lexeme") == lexeme:
                return token
        
        # Fallback to line-based lookup
        if not hasattr(self, '_tokens_by_line') or line not in self._tokens_by_line:
            return None
        
        matching_tokens = [t for t in self._tokens_by_line[line] if t.get("lexeme") == lexeme]
        
        if not matching_tokens:
            return None
        
        if len(matching_tokens) == 1:
            return matching_tokens[0]
        
        # Multiple matches - find closest to lark_column using reconstructed position
        if lark_column is not None and hasattr(self, '_reconstructed_col_to_token'):
            # Find which token lark_column maps to
            token_at_col = self._reconstructed_col_to_token.get((line, lark_column))
            if token_at_col in matching_tokens:
                return token_at_col
        
        return matching_tokens[0]
    
    def parse(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse tokens using Lark LALR(1) parser.
        Returns dict with success status, AST, and errors.
        
        NO post-parse validation - all checking is done by the CFG.
        """
        try:
            source = self._build_source_from_tokens(tokens)
            tree = self.parser.parse(source)
            
            # Transform to AST - no validation, just structure transformation
            transformer = ASTTransformer(tokens)
            ast_dict = transformer.transform(tree)
            
            return {
                "success": True,
                "status": "success",
                "ast": ast_dict,
                "errors": [],
                "token_count": len(tokens)
            }
            
        except UnexpectedEOF as e:
            return self._handle_unexpected_eof(e, tokens)
        
        except UnexpectedToken as e:
            return self._handle_unexpected_token(e, tokens)
        
        except UnexpectedInput as e:
            return self._handle_unexpected_input(e, tokens)
        
        except Exception as e:
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
    
    def _handle_unexpected_token(self, error: UnexpectedToken, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle UnexpectedToken with TRANSPARENT error reporting.
        Reports EXACT expected tokens from Lark - NO FILTERING.
        """
        unexpected_token = error.token
        expected = list(error.expected) if hasattr(error, 'expected') else []
        
        # Map Lark terminals to lexer types (cosmetic only, not filtering)
        expected_lexer_types = []
        for lark_terminal in expected:
            lexer_type = self.terminal_to_lexer_type.get(lark_terminal, lark_terminal)
            expected_lexer_types.append(lexer_type)
        
        # Get token info
        token_type_lark = unexpected_token.type if hasattr(unexpected_token, 'type') else "unknown"
        token_type = self.terminal_to_lexer_type.get(token_type_lark, token_type_lark)
        token_type_display = self._format_token_for_display(token_type)
        token_value = unexpected_token.value if hasattr(unexpected_token, 'value') else ""
        lark_line = unexpected_token.line if hasattr(unexpected_token, 'line') else 0
        lark_column = unexpected_token.column if hasattr(unexpected_token, 'column') else 0
        token_length = len(token_value) if token_value else 1
        
        # Get accurate position from original tokens
        original_token = self._lookup_original_token(lark_line, token_value, lark_column)
        if original_token:
            line = original_token.get("line", lark_line)
            column = original_token.get("column", lark_column)
        else:
            line = lark_line
            column = lark_column
        
        # Format expected tokens - NO FILTERING, exact PREDICT set
        expected_lexer_types = sorted(set(expected_lexer_types))
        
        if not expected_lexer_types:
            expected_str = "[ <EOF> (end of file) ]"
        elif expected_lexer_types == ['$END']:
            expected_str = "[ <EOF> (end of file) ]"
        else:
            expected_display = []
            for t in expected_lexer_types:
                if t == '$END':
                    expected_display.append("<EOF> (end of file)")
                else:
                    expected_display.append(self._format_token_for_display(t))
            expected_str = f"[ {', '.join(expected_display)} ]"
        
        # Format unexpected token
        if token_type_display == token_value:
            unexpected_str = f"[ {token_value} ]"
        else:
            unexpected_str = f"{token_type_display} [ {token_value} ]"
        
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
                "token_length": token_length,
                "type": "syntax_error"
            }],
            "token_count": len(tokens)
        }
    
    def _handle_unexpected_eof(self, error: UnexpectedEOF, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle UnexpectedEOF with TRANSPARENT error reporting.
        Reports EXACT expected tokens from Lark - NO FILTERING.
        """
        # Get last token position
        last_token = None
        for token in reversed(tokens):
            if token.get("type") not in ["space", "newline", "tab", "single_comment", "multi_comment"]:
                last_token = token
                break
        
        if last_token:
            line = last_token.get("line", 1)
            column = last_token.get("column", 1) + len(last_token.get("lexeme", ""))
        else:
            line = 1
            column = 1
        
        # Get expected tokens - NO FILTERING
        if hasattr(error, 'expected') and error.expected:
            expected_lark = list(error.expected)
            expected_lexer = [self.terminal_to_lexer_type.get(t, t) for t in expected_lark]
            expected_lexer = sorted(set(expected_lexer))
            expected_display = [self._format_token_for_display(t) for t in expected_lexer]
            expected_str = f"[ {', '.join(expected_display)} ]"
        else:
            expected_str = "[ valid token to complete program ]"
        
        message = f"Syntax Error at line {line}, column {column}. Unexpected: <EOF>. Expected: {expected_str}."
        
        return {
            "success": False,
            "status": "error",
            "ast": None,
            "errors": [{
                "message": message,
                "line": line,
                "column": column,
                "token": "$END",
                "token_length": 1,
                "type": "syntax_error"
            }],
            "token_count": len(tokens)
        }
    
    def _handle_unexpected_input(self, error: UnexpectedInput, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle general UnexpectedInput with TRANSPARENT error reporting.
        Reports EXACT expected tokens from Lark - NO FILTERING.
        """
        lark_line = getattr(error, 'line', 0)
        lark_column = getattr(error, 'column', 0)
        
        # Extract token info
        token_value = ""
        token_type = "unknown"
        token_length = 1
        if hasattr(error, 'token'):
            token = error.token
            token_value = token.value if hasattr(token, 'value') else str(token)
            token_type_lark = token.type if hasattr(token, 'type') else "unknown"
            token_type = self.terminal_to_lexer_type.get(token_type_lark, token_type_lark)
            token_length = len(token_value) if token_value else 1
        
        # Get accurate position
        original_token = self._lookup_original_token(lark_line, token_value, lark_column)
        if original_token:
            line = original_token.get("line", lark_line)
            column = original_token.get("column", lark_column)
        else:
            line = lark_line
            column = lark_column
        
        # Get expected tokens - NO FILTERING
        if hasattr(error, 'expected') and error.expected:
            expected_lark = list(error.expected)
            expected_lexer = [self.terminal_to_lexer_type.get(t, t) for t in expected_lark]
            expected_lexer = sorted(set(expected_lexer))
            
            if expected_lexer == ['$END']:
                expected_str = "[ <EOF> (end of file) ]"
            else:
                expected_display = []
                for t in expected_lexer:
                    if t == '$END':
                        expected_display.append("<EOF> (end of file)")
                    else:
                        expected_display.append(self._format_token_for_display(t))
                expected_str = f"[ {', '.join(expected_display)} ]"
        else:
            expected_str = "[ valid token ]"
        
        # Format token
        token_type_display = self._format_token_for_display(token_type)
        if token_type_display == token_value:
            unexpected_str = f"[ {token_value} ]"
        else:
            unexpected_str = f"{token_type_display} [ {token_value} ]"
        
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
                "token_length": token_length,
                "type": "syntax_error"
            }],
            "token_count": len(tokens)
        }
    
    # Legacy method names for backward compatibility
    def handle_unexpected_token(self, error, tokens):
        return self._handle_unexpected_token(error, tokens)
    
    def handle_unexpected_eof(self, error, tokens):
        return self._handle_unexpected_eof(error, tokens)
    
    def handle_unexpected_input(self, error, tokens):
        return self._handle_unexpected_input(error, tokens)


class ASTTransformer(Transformer):
    """
    Transforms Lark parse tree to AST.
    Preserves EXACT lexer token data - no reconstruction.
    """
    
    def __init__(self, original_tokens: List[Dict[str, Any]]):
        super().__init__()
        self.original_tokens = original_tokens
        self.token_map = {}
        self.line_tokens = {}
        
        for token in original_tokens:
            line = token.get("line")
            col = token.get("column")
            key = (line, col)
            self.token_map[key] = token
            
            if line not in self.line_tokens:
                self.line_tokens[line] = []
            self.line_tokens[line].append(token)
        
        self._recursion_depth = 0
        self._max_recursion = 1000
    
    def _make_node(self, node_type: str, children: List[Any] = None, token: Token = None) -> Dict[str, Any]:
        """Create AST node with exact lexer token data."""
        node = {
            "node_type": node_type,
            "children": children or []
        }
        
        if token:
            original = self.token_map.get((token.line, token.column))
            
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
                    result.append(self._make_node("terminal", [], child))
                elif isinstance(child, Tree):
                    method_name = child.data
                    method = getattr(self, method_name, self.__default__)
                    transformed = method(child.children, child.meta if hasattr(child, 'meta') else None)
                    result.append(transformed)
                elif isinstance(child, dict):
                    result.append(child)
                elif isinstance(child, list):
                    result.extend(self._transform_children(child))
            return result
        finally:
            self._recursion_depth -= 1
    
    def __default__(self, data: str, children: List[Any], meta):
        """Default transformation - creates node with rule name and children."""
        processed_children = []
        for child in children:
            if isinstance(child, Token):
                processed_children.append(self._make_node("terminal", [], child))
            elif isinstance(child, dict):
                processed_children.append(child)
            else:
                processed_children.append(child)
        
        return self._make_node(data, processed_children)
    
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
        if len(children) == 1 and isinstance(children[0], dict):
            return children[0]
        processed = [self._make_node("terminal", [], c) if isinstance(c, Token) else c for c in children]
        return self._make_node("expression", processed)
