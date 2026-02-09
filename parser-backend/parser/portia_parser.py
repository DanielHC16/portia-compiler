from typing import List, Dict, Any, Optional
from lark import Lark, UnexpectedInput, UnexpectedToken, Token, Tree, Transformer
from lark.exceptions import UnexpectedEOF
from pathlib import Path

class PortiaLarkParser:
    def __init__(self):
        grammar_path = Path(__file__).parent / "portia.lark"
        with open(grammar_path, 'r', encoding='utf-8') as f:
            grammar = f.read()
        
        # Lark parses source code (we reconstruct from tokens)
        # Grammar terminals use actual source literals
        # LALR(1) parser - deterministic, no ambiguity
        # Note: Lark doesn't have LL(1) mode; LALR(1) parses all LL(1) grammars
        self.parser = Lark(
            grammar,
            parser='lalr',
            start='start',
            lexer='basic',
            propagate_positions=True
        )
        
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
            "$END": "EOF",
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
            "$END": "$END",
        }
    
    def _format_token_for_display(self, token_name: str) -> str:
        """
        Format a token name for display in error messages.
        Uses actual symbols for punctuation/operators, names for keywords/identifiers.
        """
        return self.token_to_symbol.get(token_name, token_name)
    
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
        When there's a tie, prefers the token appearing later (larger column).
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
        # On ties, prefer the later token (larger column) since parsing is left-to-right
        if lark_column is not None:
            # Sort by distance, then by column descending (to prefer later tokens on tie)
            best_match = min(matching_tokens, 
                           key=lambda t: (abs(t.get("column", 0) - lark_column), -t.get("column", 0)))
            return best_match
        
        # Fallback to first match
        return matching_tokens[0]
    
    def _get_previous_token(self, target_token: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find the token immediately before the target token in the token stream.
        Skips whitespace/comment tokens.
        Returns the previous significant token, or None if target is the first token.
        """
        if not hasattr(self, '_original_tokens'):
            return None
        
        target_line = target_token.get("line", 0)
        target_column = target_token.get("column", 0)
        
        # Skip types that don't produce visible tokens
        skip_types = {"space", "newline", "tab", "single_comment", "multi_comment"}
        
        prev_token = None
        for token in self._original_tokens:
            if token.get("type") in skip_types:
                continue
            
            token_line = token.get("line", 0)
            token_column = token.get("column", 0)
            
            # Check if this token is before the target
            if (token_line < target_line or 
                (token_line == target_line and token_column < target_column)):
                prev_token = token
            elif token_line > target_line or token_column >= target_column:
                # We've passed the target, return the previous token
                break
        
        return prev_token
    
    def _validate_condition_expressions(self, tree: Tree) -> Optional[Dict[str, Any]]:
        """
        Post-parse validation: detect forbidden assignment operators in conditions.
        
        Scans the parse tree for assignment operators (=, +=, -=, *=, /=, %=) inside:
        - if-condition (condition after IF)
        - while-condition (condition after WHILE)
        - do-while-condition (condition after DO...WHILE)
        - for_cond
        
        Returns error dict if violation found, None if valid.
        """
        # Assignment operator terminals in Lark grammar
        assign_ops = {'ASSIGN', 'PLUSEQ', 'MINUSEQ', 'STAREQ', 'SLASHEQ', 'MODEQ'}
        
        # Condition context rule names (updated for strict condition grammar)
        condition_contexts = {'condition', 'cond_or', 'cond_and', 'cond_not', 
                             'cond_atom', 'cond_after_id', 'cond_after_call',
                             'cond_after_id_no_call', 'cond_postfix_no_call',
                             'cond_arith_final', 'mul_arith', 'add_arith', 
                             'comp_op', 'for_cond'}
        
        def find_assignment_in_condition(node, in_condition=False):
            """
            Recursively search for assignment operators inside condition contexts.
            Returns (Token, context_name) if found, None otherwise.
            """
            if isinstance(node, Token):
                # Check if this token is an assignment operator inside a condition
                if in_condition and node.type in assign_ops:
                    return (node, 'condition')
                return None
            
            if isinstance(node, Tree):
                # Check if entering a condition context
                entering_condition = node.data in condition_contexts
                new_in_condition = in_condition or entering_condition
                
                # Search children
                for child in node.children:
                    result = find_assignment_in_condition(child, new_in_condition)
                    if result:
                        return result
            
            return None
        
        # Search the entire tree
        violation = find_assignment_in_condition(tree)
        
        if violation:
            token, context = violation
            
            # Map Lark terminal to lexer type
            token_type = self.terminal_to_lexer_type.get(token.type, token.type.lower())
            token_display = self._format_token_for_display(token_type)
            
            # Look up original token for accurate position
            original = self._lookup_original_token(token.line, token.value, token.column)
            if original:
                line = original.get("line", token.line)
                column = original.get("column", token.column)
            else:
                line = token.line
                column = token.column
            
            # Expected tokens in condition context (comparison/logical only)
            expected_tokens = ['==', '!=', '<', '>', '<=', '>=', '&&', '||', ')']
            expected_str = f"[ {', '.join(expected_tokens)} ]"
            
            message = (f"Syntax Error at line {line}, column {column}. "
                      f"Unexpected: [ {token.value} ]. "
                      f"Assignment operators are not allowed in conditions. "
                      f"Expected: {expected_str}.")
            
            return {
                "success": False,
                "status": "error",
                "ast": None,
                "errors": [{
                    "message": message,
                    "line": line,
                    "column": column,
                    "token": token_type,
                    "token_length": len(token.value),
                    "type": "syntax_error"
                }],
                "token_count": len(self._original_tokens)
            }
        
        return None
    
    def parse(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse tokens using Lark LL(1) parser.
        Returns dict with success status, AST, and errors.
        """
        try:
            # Reconstruct source from tokens
            source = self._build_source_from_tokens(tokens)
            
            # Parse with LL(1) - deterministic, single parse tree
            tree = self.parser.parse(source)
            
            # Post-parse validation: check for forbidden constructs in conditions
            validation_error = self._validate_condition_expressions(tree)
            if validation_error:
                return validation_error
            
            # Transform tree to AST with exact lexer token data
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
            # EOF reached unexpectedly - input ended before complete program
            return self.handle_unexpected_eof(e, tokens)
        
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
        
        # Detect context BEFORE filtering for position adjustment
        context = self._detect_parse_context(expected_lexer_types, error)
        
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
        
        # For_cond position fix: when unexpected is `;` and context is for_cond,
        # the actual error is at the SECOND semicolon (where condition is required)
        # Only adjust if we're at the FIRST semicolon (prev token is not a semicolon)
        if (context == 'for_cond' and token_value == ';' and 
            token_type in ('semicolon', ';') and original_token):
            # Check if there's a semicolon BEFORE this one - if so, we're already at the second one
            prev_token = self._get_previous_token(original_token)
            if not (prev_token and prev_token.get("type") == ";"):
                # At the first semicolon, find the next one
                next_semicolon = self._get_next_token_of_type(
                    original_token.get("line", 0),
                    original_token.get("column", 0),
                    ";"
                )
                if next_semicolon:
                    # Adjust error position to the second semicolon
                    line = next_semicolon.get("line", line)
                    column = next_semicolon.get("column", column)
        
        # Filter expected tokens based on context to reduce noise
        expected_lexer_types = self._filter_expected_tokens(expected_lexer_types, error)
        
        expected_lexer_types = sorted(set(expected_lexer_types))
        
        # Format expected tokens for display (symbols for punctuation, names for keywords)
        if not expected_lexer_types:
            # No expected tokens means EOF was expected (end of program)
            expected_str = "[ <EOF> (end of file) ]"
        elif expected_lexer_types == ['$END']:
            # Only EOF expected - use descriptive format
            expected_str = "[ <EOF> (end of file) ]"
        else:
            # Format each token, replacing $END with descriptive EOF
            expected_display = []
            for t in expected_lexer_types:
                if t == '$END':
                    expected_display.append("<EOF> (end of file)")
                else:
                    expected_display.append(self._format_token_for_display(t))
            expected_str = f"[ {', '.join(expected_display)} ]"
        
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
    
    def handle_unexpected_eof(self, error: UnexpectedEOF, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle UnexpectedEOF error - input ended before program was complete.
        Uses last token position for error reporting.
        """
        # Get the last non-whitespace token for position
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
        
        # Try to get expected tokens from the error
        expected_str = "valid token"
        if hasattr(error, 'expected') and error.expected:
            expected_lark = list(error.expected)
            expected_lexer = [self.terminal_to_lexer_type.get(t, t) for t in expected_lark]
            expected_display = [self._format_token_for_display(t) for t in sorted(set(expected_lexer))]
            expected_str = f"[ {', '.join(expected_display)} ]"
        else:
            # Default expected message when expected is not populated
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
    
    def _detect_parse_context(self, expected_tokens: List[str], error) -> str:
        """
        Detect the parsing context from expected tokens using grammar-rule analysis.
        Returns: 'array_index', 'condition', 'function_body', or 'general'
        
        Key insight: The PORTIA grammar uses separate expression hierarchies:
        - General expressions: expression -> assign_expr -> concat_expr -> ... (allows =, +=, etc.)
        - Condition expressions: condition -> cond_or -> cond_and -> ... (strict boolean only)
        - Function body: func_content_* requires return as the ONLY terminal exit
        
        We detect condition context by the ABSENCE of assignment operators in expected tokens,
        combined with the PRESENCE of condition-specific operators.
        """
        token_set = set(expected_tokens)
        
        # Function body context: when 'return' is expected along with function content
        # starters (using, local, statement starters), this is the mandatory return point
        # Grammar: func_content_* → using... | local... | statement_non_return... | return...
        if 'return' in token_set:
            # Function body indicators from the recursive func_content rules
            func_body_indicators = {'using', 'local'}
            # Statement starters that appear in func_content alternatives
            statement_indicators = {'if', 'while', 'for', 'do', 'switch', 'break',
                                    'trap', 'thread', 'threadln'}
            # If we have return + function body indicators, this is function body context
            if (token_set & func_body_indicators) or (token_set & statement_indicators):
                return 'function_body'
        
        # Array index context: expects only intlit, id, and possibly close_bracket
        array_index_tokens = {'intlit', 'id', 'close_bracket'}
        if token_set and token_set.issubset(array_index_tokens):
            return 'array_index'
        
        # Condition context detection based on grammar structure:
        # In condition hierarchy, the grammar NEVER includes assignment operators.
        assignment_ops = {'assign', 'add_assign', 'minus_assign', 'mult_assign', 'div_assign', 'modulo_assign'}
        
        # Check if unexpected token is an assignment operator
        unexpected_is_assign = False
        if hasattr(error, 'token') and hasattr(error.token, 'type'):
            unexpected_type = self.terminal_to_lexer_type.get(error.token.type, error.token.type.lower())
            unexpected_is_assign = unexpected_type in assignment_ops
        
        # Condition context detection:
        # 1. Assignment operators are NOT in expected tokens (grammar prohibits them)
        # 2. AND either: unexpected token is assignment, OR close_paren expected without semicolon
        has_assignment_expected = bool(token_set & assignment_ops)
        
        # Tokens that indicate condition expression context
        condition_ops = {'logical_and', 'logical_or', 'equal', 'not_equal', 
                        'less_than', 'greater_than', 'less_equal', 'greater_equal'}
        has_condition_ops = bool(token_set & condition_ops)
        
        # If assignment ops are NOT expected AND unexpected token IS assignment -> condition context
        # This catches `if (x = 3)` where `=` is unexpected
        if not has_assignment_expected and unexpected_is_assign:
            return 'condition'
        
        # Condition context: has condition operators but NO assignment operators expected
        if has_condition_ops and not has_assignment_expected:
            return 'condition'
        
        # Also detect condition when we expect close_paren (end of condition)
        # but assignment operators are not expected
        if 'close_paren' in token_set and not has_assignment_expected and 'semicolon' not in token_set:
            return 'condition'
        
        # For_init context: semicolon expected along with expression operators
        # but no statement keywords (we're inside for loop initializer)
        # for_init_expr uses concat_expr, so expression ops like concat/or/and may appear
        if 'semicolon' in token_set:
            expr_ops = {'concat', 'logical_or', 'logical_and', 'add', 'subtract', 
                       'multiply', 'divide', 'modulo'}
            statement_keywords = {'if', 'while', 'for', 'do', 'switch', 'break',
                                 'trap', 'thread', 'threadln', 'return', 'using', 'local'}
            has_expr_ops = bool(token_set & expr_ops)
            has_stmt_keywords = bool(token_set & statement_keywords)
            # Inside for_init: has expression operators but no statement keywords
            if has_expr_ops and not has_stmt_keywords:
                return 'for_init'
        
        # For_cond context: expecting condition-starting tokens
        # This is the mandatory condition slot in a for loop
        # Since for_cond is non-nullable, expected tokens are ONLY condition starters
        cond_starters = {'true', 'false', 'id', 'open_paren', 'logical_not',
                        'intlit', 'longlit', 'floatlit', 'doublelit', 'charlit', 'stringlit',
                        'int', 'long', 'float', 'double', 'char', 'string', 'bool'}
        has_cond_starters = bool(token_set & cond_starters)
        has_close_paren = 'close_paren' in token_set
        
        # For_cond detection: has condition starters, NOT close_paren or semicolon
        # (close_paren would mean end of condition in if/while, semicolon in original nullable for_cond)
        # Also no statement keywords (we're inside for control structure, not statement list)
        statement_keywords = {'if', 'while', 'for', 'do', 'switch', 'break',
                             'trap', 'thread', 'threadln', 'return', 'using', 'local'}
        if has_cond_starters and not has_close_paren and not (token_set & statement_keywords):
            # Additional check: make sure most expected tokens are condition starters
            # This distinguishes for_cond from other contexts with id/intlit expected
            cond_starter_count = len(token_set & cond_starters)
            if cond_starter_count >= len(token_set) * 0.5:  # At least half are condition starters
                return 'for_cond'
        
        return 'general'
    
    def _filter_expected_tokens(self, expected_tokens: List[str], error) -> List[str]:
        """
        Filter expected tokens based on parse context to provide clearer error messages.
        
        For function body context: The CFG requires 'return' as the only valid exit.
        Using, local, and statement_non_return are optional precursors but 'return' is mandatory.
        
        For condition context: STRICTLY limit to condition-valid tokens only.
        This ensures errors like 'if (x = 3)' show only: == != < > <= >= && || )
        """
        if not expected_tokens:
            return expected_tokens
        
        # 2D Array initialization: when { is expected, exclude } from expected tokens
        # For 2D arrays like int grid[2][3] = {1,2,3}, the parser expects nested braces {{...}}
        # When flat init is given, we should only suggest { not }
        if 'open_brace' in expected_tokens and 'close_brace' in expected_tokens:
            expected_tokens = [t for t in expected_tokens if t != 'close_brace']
        
        # Detect parsing context
        context = self._detect_parse_context(expected_tokens, error)
        
        # Function body context: only 'return' is the mandatory terminal
        # Grammar: func_content_* → ... | return ...
        # All other alternatives (using, local, statement) are optional precursors
        if context == 'function_body':
            return ['return']
        
        # Array index context: only show intlit, id, close_bracket
        if context == 'array_index':
            array_valid = {'intlit', 'id', 'close_bracket'}
            return [t for t in expected_tokens if t in array_valid]
        
        # Condition context: STRICTLY limit to condition-valid tokens
        # Per grammar: condition hierarchy only allows these operators
        # User requirement: Expected tokens must be limited to: == != < > <= >= && || )
        if context == 'condition':
            # Valid tokens in condition expressions - strict subset for error messages
            condition_valid = {
                # Comparison operators
                'equal', 'not_equal',
                'less_than', 'greater_than', 'less_equal', 'greater_equal',
                # Logical operators
                'logical_and', 'logical_or',
                # Closing delimiter (end of condition)
                'close_paren',
            }
            filtered = [t for t in expected_tokens if t in condition_valid]
            # Return filtered list, ensuring we have at least something useful
            return filtered if filtered else ['close_paren']
        
        # For_init context: only semicolon is valid terminator
        if context == 'for_init':
            return ['semicolon']
        
        # For_cond context: condition is required, filter out semicolon and close_paren
        # This occurs when parser is at for loop's condition slot (now mandatory)
        if context == 'for_cond':
            # Condition-starting tokens only
            cond_starters = {
                'true', 'false', 'id', 'open_paren', 'logical_not',
                'intlit', 'longlit', 'floatlit', 'doublelit', 'charlit', 'stringlit',
                'int', 'long', 'float', 'double', 'char', 'string', 'bool'
            }
            filtered = [t for t in expected_tokens if t in cond_starters]
            return filtered if filtered else expected_tokens
        
        # General context: apply standard filtering (but never filter $END)
        statement_terminators = {'semicolon', 'close_brace', 'close_paren', 'close_bracket', '$END'}
        operators = {'add', 'subtract', 'multiply', 'divide', 'modulo', 'equal', 'not_equal', 
                    'less_than', 'greater_than', 'less_equal', 'greater_equal', 
                    'logical_and', 'logical_or', 'logical_not'}
        
        # If statement terminators are in the expected list, prioritize them
        terminators_present = [t for t in expected_tokens if t in statement_terminators]
        if terminators_present:
            operators_present = [t for t in expected_tokens if t in operators]
            if len(operators_present) >= 3 and len(terminators_present) >= 1:
                non_operators = [t for t in expected_tokens if t not in operators]
                return non_operators if non_operators else expected_tokens
        
        # If we have too many operators, filter them
        if len([t for t in expected_tokens if t in operators]) > 5:
            filtered = [t for t in expected_tokens if t not in operators]
            if filtered:
                return filtered
        
        return expected_tokens
    
    def _get_next_token_of_type(self, after_line: int, after_column: int, token_type: str) -> Optional[Dict[str, Any]]:
        """
        Find the next token of the specified type that appears after the given position.
        Returns the token dict or None if not found.
        """
        if not hasattr(self, '_original_tokens'):
            return None
        
        skip_types = {"space", "newline", "tab", "single_comment", "multi_comment"}
        
        for token in self._original_tokens:
            if token.get("type") in skip_types:
                continue
            
            token_line = token.get("line", 0)
            token_column = token.get("column", 0)
            
            # Check if this token is after the target position
            if (token_line > after_line or 
                (token_line == after_line and token_column > after_column)):
                # Check if it matches the requested type
                if token.get("type") == token_type:
                    return token
        
        return None
    
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
        expected_lexer = []
        if hasattr(error, 'expected') and error.expected:
            expected_lark = list(error.expected)
            expected_lexer = [self.terminal_to_lexer_type.get(t, t) for t in expected_lark]
            # Check context BEFORE filtering for position adjustment
            context = self._detect_parse_context(expected_lexer, error)
            
            # For_cond position fix: when unexpected is `;` and context is for_cond,
            # the actual error is at the SECOND semicolon (where condition is required)
            # Only adjust if we're at the FIRST semicolon (prev token is not a semicolon)
            if (context == 'for_cond' and token_value == ';' and 
                token_type in ('semicolon', ';') and original_token):
                # Check if there's a semicolon BEFORE this one - if so, we're already at the second one
                prev_token = self._get_previous_token(original_token)
                if not (prev_token and prev_token.get("type") == ";"):
                    # At the first semicolon, find the next one
                    next_semicolon = self._get_next_token_of_type(
                        original_token.get("line", 0),
                        original_token.get("column", 0),
                        ";"
                    )
                    if next_semicolon:
                        # Adjust error position to the second semicolon
                        line = next_semicolon.get("line", line)
                        column = next_semicolon.get("column", column)
            
            # Apply filtering for expected tokens
            expected_lexer = self._filter_expected_tokens(expected_lexer, error)
            expected_lexer = sorted(set(expected_lexer))
            
            # Handle EOF specially
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
