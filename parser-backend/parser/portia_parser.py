"""
PORTIA Parser - Recursive Descent Implementation
=================================================
"""

from typing import List, Dict, Any, Optional, Set
from .grammar import FIRST, EPSILON


def first_of(nonterminal: str) -> str:
    """Get comma-separated list of terminals in FIRST(nonterminal)."""
    tokens = FIRST.get(nonterminal, set()) - {EPSILON}
    return ", ".join(sorted(tokens))


class ParseTreeNode:
    """
    Node in the parse tree.
    
    Attributes:
        type: Node type (non-terminal name or "terminal")
        value: For terminals, the token value; for non-terminals, None
        children: List of child nodes
        token: Original token dict for terminals
    """
    
    def __init__(self, node_type: str, value: Any = None, token: Dict = None):
        self.type = node_type
        self.value = value
        self.children: List["ParseTreeNode"] = []
        self.token = token
    
    def add_child(self, child: "ParseTreeNode") -> "ParseTreeNode":
        """Add a child node and return it."""
        self.children.append(child)
        return child
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {"type": self.type}
        if self.value is not None:
            result["value"] = self.value
        if self.token:
            result["line"] = self.token.get("line", 0)
            result["column"] = self.token.get("column", 0)
        if self.children:
            result["children"] = [c.to_dict() for c in self.children]
        return result
    
    def __repr__(self):
        if self.value is not None:
            return f"ParseTreeNode({self.type}, {self.value!r})"
        return f"ParseTreeNode({self.type}, children={len(self.children)})"


class ParseError(Exception):
    """Raised when a syntax error is encountered."""
    
    def __init__(self, message: str, token: Dict = None):
        self.message = message
        self.token = token or {}
        self.line = self.token.get("line", 0)
        self.column = self.token.get("column", 0)
        super().__init__(message)


# Type keywords and literal types
TYPE_KEYWORDS = {"int", "long", "float", "double", "char", "string", "bool"}
LITERAL_TYPES = {"INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT", "CHARLIT", "STRINGLIT"}


class PortiaParser:
    """
    Recursive descent parser for PORTIA language.
    
    Usage:
        parser = PortiaParser(tokens)
        tree = parser.parse()
    """
    
    def __init__(self, tokens: List[Dict[str, Any]]):
        """
        Initialize the parser with a token stream.
        
        Args:
            tokens: List of token dictionaries from the lexer.
                   Each token has: type, value, line, column
        """
        self.tokens = tokens
        self.pos = 0
    
    # =========================================================================
    # Token Stream Navigation
    # =========================================================================
    
    def peek(self, offset: int = 0) -> Optional[Dict[str, Any]]:
        """Look at a token without consuming it."""
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def peek_type(self, offset: int = 0) -> Optional[str]:
        """Get the type of a token without consuming it (normalized to uppercase)."""
        tok = self.peek(offset)
        t = tok.get("type") if tok else None
        return t.upper() if t else None
    
    def peek_value(self, offset: int = 0) -> Optional[str]:
        """Get the value/lexeme of a token without consuming it."""
        tok = self.peek(offset)
        if tok is None:
            return None
        # Support both 'value' and 'lexeme' fields
        return tok.get("value") or tok.get("lexeme")
    
    def at_end(self) -> bool:
        """Check if we've consumed all tokens."""
        return self.pos >= len(self.tokens)
    
    def advance(self) -> Optional[Dict[str, Any]]:
        """Consume and return the current token."""
        if not self.at_end():
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None
    
    def match(self, expected_type: str) -> Dict[str, Any]:
        """Verify current token type and consume it (case-insensitive)."""
        current = self.peek()
        if current is None:
            raise ParseError(
                f"Unexpected: end of input\nExpected: {expected_type.lower()}",
                {"line": 0, "column": 0, "type": "EOF", "value": ""}
            )
        actual_type = current.get("type", "").upper()
        if actual_type != expected_type.upper():
            raise ParseError(
                f"Unexpected: {current.get('type')}\nExpected: {expected_type.lower()}",
                current
            )
        return self.advance()
    
    def match_value(self, expected_value: str) -> Dict[str, Any]:
        """Verify current token value and consume it."""
        current = self.peek()
        if current is None:
            raise ParseError(
                f"Unexpected: end of input\nExpected: {expected_value}",
                {"line": 0, "column": 0, "type": "EOF", "value": ""}
            )
        actual_value = current.get("value") or current.get("lexeme")
        if actual_value != expected_value:
            raise ParseError(
                f"Unexpected: {actual_value}\nExpected: {expected_value}",
                current
            )
        return self.advance()
    
    # =========================================================================
    # Helper Methods
    # =========================================================================
    
    def make_terminal(self, token: Dict[str, Any]) -> ParseTreeNode:
        """Create a terminal node from a token."""
        val = token.get("value") or token.get("lexeme")
        return ParseTreeNode("terminal", val, token)
    
    def check(self, *values: str) -> bool:
        """Check if current token value is one of the given values."""
        tok = self.peek()
        if tok is None:
            return False
        val = tok.get("value") or tok.get("lexeme")
        return val in values
    
    def check_type(self, *types: str) -> bool:
        """Check if current token type is one of the given types (case-insensitive)."""
        tok = self.peek()
        if tok is None:
            return False
        actual = tok.get("type", "").upper()
        return actual in {t.upper() for t in types}
    
    def error(self, expected: str) -> ParseError:
        """Create a ParseError with current token context."""
        tok = self.peek() or {"line": 0, "column": 0, "type": "EOF", "value": ""}
        return ParseError(
            f"Unexpected: {tok.get('type')}\nExpected: {expected}",
            tok
        )
    
    # =========================================================================
    # Main Entry Point
    # =========================================================================
    
    def parse(self) -> ParseTreeNode:
        """Parse the token stream and return a parse tree."""
        tree = self.parse_program()
        
        if not self.at_end():
            remaining = self.peek()
            val = remaining.get("value") or remaining.get("lexeme") or ""
            raise ParseError(
                f"Unexpected: {val!r} ({remaining.get('type')})\nExpected: end of program",
                remaining
            )
        return tree
    
    # =========================================================================
    # Grammar Rules - Top Level
    # =========================================================================
    
    def parse_program(self) -> ParseTreeNode:
        """program → global_section"""
        node = ParseTreeNode("program")
        node.add_child(self.parse_global_section())
        return node
    
    def parse_global_section(self) -> ParseTreeNode:
        """
        global_section → global_decl global_section
                       | type id array_with_init ; global_section
                       | weave id { field_list } global_section
                       | id weave_inst_decl global_section
                       | function_decl func_and_main
                       | int main ( ) { main_body }
                       | ε
        """
        node = ParseTreeNode("global_section")
        
        if self.at_end():
            return node  # epsilon
        
        val = self.peek_value()
        
        if val == "global":
            # global_decl global_section
            node.add_child(self.parse_global_decl())
            node.add_child(self.parse_global_section())
            
        elif val == "weave":
            # weave id { field_list } global_section
            node.add_child(self.make_terminal(self.advance()))  # weave
            node.add_child(self.make_terminal(self.match("ID")))  # id
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_field_list())
            node.add_child(self.make_terminal(self.match_value("}")))
            node.add_child(self.parse_global_section())
            
        elif val == "func":
            # function_decl func_and_main
            node.add_child(self.parse_function_decl())
            node.add_child(self.parse_func_and_main())
            
        elif val == "int":
            # Disambiguate: int main() vs int id array_with_init
            if self.peek_value(1) == "main":
                # int main ( ) { main_body }
                node.add_child(self.make_terminal(self.advance()))  # int
                node.add_child(self.make_terminal(self.advance()))  # main
                node.add_child(self.make_terminal(self.match_value("(")))
                node.add_child(self.make_terminal(self.match_value(")")))
                node.add_child(self.make_terminal(self.match_value("{")))
                node.add_child(self.parse_main_body())
                node.add_child(self.make_terminal(self.match_value("}")))
            else:
                # int id int_array_with_init ; global_section
                node.add_child(self.make_terminal(self.advance()))  # int
                node.add_child(self.make_terminal(self.match("ID")))
                node.add_child(self.parse_array_with_init())
                node.add_child(self.make_terminal(self.match_value(";")))
                node.add_child(self.parse_global_section())
                
        elif val in ("long", "float", "double", "char", "string", "bool"):
            # type id array_with_init ; global_section
            node.add_child(self.make_terminal(self.advance()))  # type
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_array_with_init())
            node.add_child(self.make_terminal(self.match_value(";")))
            node.add_child(self.parse_global_section())
            
        elif self.check_type("ID"):
            # id (weave type) weave_inst_decl global_section
            node.add_child(self.make_terminal(self.advance()))  # weave type id
            node.add_child(self.parse_weave_inst_decl())
            node.add_child(self.parse_global_section())
        
        # else: epsilon production
        return node
    
    def parse_func_and_main(self) -> ParseTreeNode:
        """
        func_and_main → function_decl func_and_main
                      | int main ( ) { main_body }
        """
        node = ParseTreeNode("func_and_main")
        
        if self.check("func"):
            node.add_child(self.parse_function_decl())
            node.add_child(self.parse_func_and_main())
        elif self.check("int") and self.peek_value(1) == "main":
            node.add_child(self.make_terminal(self.advance()))  # int
            node.add_child(self.make_terminal(self.advance()))  # main
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_main_body())
            node.add_child(self.make_terminal(self.match_value("}")))
        
        return node
    
    # =========================================================================
    # Global Declarations
    # =========================================================================
    
    def parse_global_decl(self) -> ParseTreeNode:
        """
        global_decl → global mutability type id = literal global_cont ;
        """
        node = ParseTreeNode("global_decl")
        node.add_child(self.make_terminal(self.match_value("global")))
        node.add_child(self.parse_mutability())
        
        # Type determines which literal to expect
        type_val = self.peek_value()
        node.add_child(self.make_terminal(self.advance()))  # type
        node.add_child(self.make_terminal(self.match("ID")))  # id
        node.add_child(self.make_terminal(self.match_value("=")))
        
        # Match appropriate literal or bool value
        if type_val == "bool":
            node.add_child(self.parse_bool_lit())
        else:
            node.add_child(self.make_terminal(self.advance()))  # literal
        
        node.add_child(self.parse_global_cont())
        node.add_child(self.make_terminal(self.match_value(";")))
        return node
    
    def parse_mutability(self) -> ParseTreeNode:
        """mutability → var | const"""
        node = ParseTreeNode("mutability")
        if self.check("var", "const"):
            node.add_child(self.make_terminal(self.advance()))
        else:
            raise self.error(first_of("mutability"))
        return node
    
    def parse_global_cont(self) -> ParseTreeNode:
        """global_cont → , id = literal global_cont | ε"""
        node = ParseTreeNode("global_cont")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))  # ,
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.make_terminal(self.match_value("=")))
            # literal or bool
            if self.check("true", "false"):
                node.add_child(self.parse_bool_lit())
            else:
                node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_global_cont())
        return node
    
    def parse_bool_lit(self) -> ParseTreeNode:
        """bool_lit → true | false"""
        node = ParseTreeNode("bool_lit")
        if self.check("true", "false"):
            node.add_child(self.make_terminal(self.advance()))
        else:
            raise self.error(first_of("bool_lit"))
        return node
    
    # =========================================================================
    # Weave (Struct) Declarations
    # =========================================================================
    
    def parse_field_list(self) -> ParseTreeNode:
        """field_list → field_dec field_list | ε"""
        node = ParseTreeNode("field_list")
        # field_dec starts with a type (keyword or ID)
        if self.peek_value() in TYPE_KEYWORDS or self.check_type("ID"):
            if not self.check("}"):
                node.add_child(self.parse_field_dec())
                node.add_child(self.parse_field_list())
        return node
    
    def parse_field_dec(self) -> ParseTreeNode:
        """field_dec → field_type id field_arr_opt field_cont ;"""
        node = ParseTreeNode("field_dec")
        node.add_child(self.parse_field_type())
        node.add_child(self.make_terminal(self.match("ID")))
        node.add_child(self.parse_field_arr_opt())
        node.add_child(self.parse_field_cont())
        node.add_child(self.make_terminal(self.match_value(";")))
        return node
    
    def parse_field_type(self) -> ParseTreeNode:
        """field_type → int | long | float | double | char | string | bool | id"""
        node = ParseTreeNode("field_type")
        if self.peek_value() in TYPE_KEYWORDS or self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))
        else:
            raise self.error(first_of("field_type"))
        return node
    
    def parse_field_arr_opt(self) -> ParseTreeNode:
        """field_arr_opt → array_dims | ε"""
        node = ParseTreeNode("field_arr_opt")
        if self.check("["):
            node.add_child(self.parse_array_dims())
        return node
    
    def parse_field_cont(self) -> ParseTreeNode:
        """field_cont → , id field_arr_opt field_cont | ε"""
        node = ParseTreeNode("field_cont")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))  # ,
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_field_arr_opt())
            node.add_child(self.parse_field_cont())
        return node
    
    def parse_weave_inst_decl(self) -> ParseTreeNode:
        """weave_inst_decl → id weave_inst_tail weave_inst_cont ;
                          | weave_array_with_init weave_arr_cont ;"""
        node = ParseTreeNode("weave_inst_decl")
        
        if self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))  # instance id
            node.add_child(self.parse_weave_inst_tail())
            node.add_child(self.parse_weave_inst_cont())
            node.add_child(self.make_terminal(self.match_value(";")))
        elif self.check("["):
            node.add_child(self.parse_weave_array_with_init())
            node.add_child(self.parse_weave_arr_cont())
            node.add_child(self.make_terminal(self.match_value(";")))
        else:
            raise self.error(first_of("weave_inst_decl"))
        return node
    
    def parse_weave_inst_tail(self) -> ParseTreeNode:
        """weave_inst_tail → = { weave_field_value weave_field_list_tail }
                          | weave_array_with_init"""
        node = ParseTreeNode("weave_inst_tail")
        if self.check("="):
            node.add_child(self.make_terminal(self.advance()))  # =
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_weave_field_value())
            node.add_child(self.parse_weave_field_list_tail())
            node.add_child(self.make_terminal(self.match_value("}")))
        elif self.check("["):
            node.add_child(self.parse_weave_array_with_init())
        return node
    
    def parse_weave_field_value(self) -> ParseTreeNode:
        """weave_field_value → literal | true | false | { weave_value_list }"""
        node = ParseTreeNode("weave_field_value")
        if self.check("{"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_weave_value_list())
            node.add_child(self.make_terminal(self.match_value("}")))
        elif self.check("true", "false"):
            node.add_child(self.make_terminal(self.advance()))
        elif self.check_type("INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT", "CHARLIT", "STRINGLIT"):
            node.add_child(self.make_terminal(self.advance()))
        else:
            raise self.error(first_of("weave_field_value"))
        return node
    
    def parse_weave_value_list(self) -> ParseTreeNode:
        """weave_value_list → weave_field_value weave_value_tail"""
        node = ParseTreeNode("weave_value_list")
        node.add_child(self.parse_weave_field_value())
        node.add_child(self.parse_weave_value_tail())
        return node
    
    def parse_weave_value_tail(self) -> ParseTreeNode:
        """weave_value_tail → , weave_field_value weave_value_tail | ε"""
        node = ParseTreeNode("weave_value_tail")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_weave_field_value())
            node.add_child(self.parse_weave_value_tail())
        return node
    
    def parse_weave_field_list_tail(self) -> ParseTreeNode:
        """weave_field_list_tail → , weave_field_value weave_field_list_tail | ε"""
        node = ParseTreeNode("weave_field_list_tail")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_weave_field_value())
            node.add_child(self.parse_weave_field_list_tail())
        return node
    
    def parse_weave_inst_cont(self) -> ParseTreeNode:
        """weave_inst_cont → , id weave_inst_tail weave_inst_cont | ε"""
        node = ParseTreeNode("weave_inst_cont")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_weave_inst_tail())
            node.add_child(self.parse_weave_inst_cont())
        return node
    
    def parse_weave_arr_cont(self) -> ParseTreeNode:
        """weave_arr_cont → , id weave_array_with_init weave_arr_cont | ε"""
        node = ParseTreeNode("weave_arr_cont")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_weave_array_with_init())
            node.add_child(self.parse_weave_arr_cont())
        return node
    
    def parse_weave_array_with_init(self) -> ParseTreeNode:
        """weave_array_with_init → [ size ] weave_array_init_tail"""
        node = ParseTreeNode("weave_array_with_init")
        node.add_child(self.make_terminal(self.match_value("[")))
        node.add_child(self.parse_size())
        node.add_child(self.make_terminal(self.match_value("]")))
        node.add_child(self.parse_array_init_tail())
        return node
    
    # =========================================================================
    # Array Declarations and Initialization
    # =========================================================================
    
    def parse_array_dims(self) -> ParseTreeNode:
        """array_dims → [ size ] array_dim2_opt"""
        node = ParseTreeNode("array_dims")
        node.add_child(self.make_terminal(self.match_value("[")))
        node.add_child(self.parse_size())
        node.add_child(self.make_terminal(self.match_value("]")))
        node.add_child(self.parse_array_dim2_opt())
        return node
    
    def parse_array_dim2_opt(self) -> ParseTreeNode:
        """array_dim2_opt → [ size ] | ε"""
        node = ParseTreeNode("array_dim2_opt")
        if self.check("["):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_size())
            node.add_child(self.make_terminal(self.match_value("]")))
        return node
    
    def parse_size(self) -> ParseTreeNode:
        """size → intlit | id"""
        node = ParseTreeNode("size")
        if self.check_type("INTLIT"):
            node.add_child(self.make_terminal(self.advance()))
        elif self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))
        else:
            raise self.error(first_of("size"))
        return node
    
    def parse_array_with_init(self) -> ParseTreeNode:
        """array_with_init → [ size ] array_init_tail | ε (for simple vars)"""
        node = ParseTreeNode("array_with_init")
        if self.check("["):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_size())
            node.add_child(self.make_terminal(self.match_value("]")))
            node.add_child(self.parse_array_init_tail())
        return node
    
    def parse_array_init_tail(self) -> ParseTreeNode:
        """array_init_tail → [ size ] array_init_opt_2d | array_init_opt_1d"""
        node = ParseTreeNode("array_init_tail")
        if self.check("["):
            # 2D array
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_size())
            node.add_child(self.make_terminal(self.match_value("]")))
            node.add_child(self.parse_array_init_opt())
        else:
            # 1D array or no init
            node.add_child(self.parse_array_init_opt())
        return node
    
    def parse_array_init_opt(self) -> ParseTreeNode:
        """array_init_opt → = { ... } | ε"""
        node = ParseTreeNode("array_init_opt")
        if self.check("="):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_array_init_content())
            node.add_child(self.make_terminal(self.match_value("}")))
        return node
    
    def parse_array_init_content(self) -> ParseTreeNode:
        """Parse array initializer content (elements or nested arrays)"""
        node = ParseTreeNode("array_init_content")
        # Simplified: consume until matching }
        depth = 1
        while not self.at_end() and depth > 0:
            if self.check("}"):
                depth -= 1
                if depth == 0:
                    break
            elif self.check("{"):
                depth += 1
            node.add_child(self.make_terminal(self.advance()))
        return node
    
    # =========================================================================
    # Function Declarations
    # =========================================================================
    
    def parse_function_decl(self) -> ParseTreeNode:
        """
        function_decl → func return_type func_signature { function_body }
        """
        node = ParseTreeNode("function_decl")
        node.add_child(self.make_terminal(self.match_value("func")))
        
        # Return type
        ret_type = self.peek_value()
        if ret_type == "void":
            node.add_child(self.make_terminal(self.advance()))  # void
            node.add_child(self.make_terminal(self.match("ID")))  # name
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_param_list())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_function_body_void())
            node.add_child(self.make_terminal(self.match_value("}")))
        elif ret_type in TYPE_KEYWORDS:
            node.add_child(self.make_terminal(self.advance()))  # type
            # Check for array return type
            if self.check("["):
                node.add_child(self.parse_array_dims())
            node.add_child(self.make_terminal(self.match("ID")))  # name
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_param_list())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_function_body())
            node.add_child(self.make_terminal(self.match_value("}")))
        elif self.check_type("ID"):
            # Weave return type
            node.add_child(self.make_terminal(self.advance()))  # weave type
            # Could be: id ( ... ) or . id id ( ... ) or [ ] id ( ... )
            if self.check("."):
                node.add_child(self.make_terminal(self.advance()))  # .
                node.add_child(self.make_terminal(self.match("ID")))  # namespace
            elif self.check("["):
                node.add_child(self.parse_array_dims())
            node.add_child(self.make_terminal(self.match("ID")))  # name
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_param_list())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_function_body())
            node.add_child(self.make_terminal(self.match_value("}")))
        else:
            raise self.error(first_of("param_type") + ", void")
        
        return node
    
    def parse_param_list(self) -> ParseTreeNode:
        """param_list → param_type id param_arr_opt param_cont | ε"""
        node = ParseTreeNode("param_list")
        if self.peek_value() in TYPE_KEYWORDS or self.check_type("ID"):
            if not self.check(")"):
                node.add_child(self.parse_param_type())
                node.add_child(self.make_terminal(self.match("ID")))
                node.add_child(self.parse_param_arr_opt())
                node.add_child(self.parse_param_cont())
        return node
    
    def parse_param_type(self) -> ParseTreeNode:
        """param_type → int | long | float | double | char | string | bool | id"""
        node = ParseTreeNode("param_type")
        if self.peek_value() in TYPE_KEYWORDS or self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))
        else:
            raise self.error(first_of("param_type"))
        return node
    
    def parse_param_arr_opt(self) -> ParseTreeNode:
        """param_arr_opt → array_dims | ε"""
        node = ParseTreeNode("param_arr_opt")
        if self.check("["):
            node.add_child(self.parse_array_dims())
        return node
    
    def parse_param_cont(self) -> ParseTreeNode:
        """param_cont → , param_type id param_arr_opt param_cont | ε"""
        node = ParseTreeNode("param_cont")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_param_type())
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_param_arr_opt())
            node.add_child(self.parse_param_cont())
        return node
    
    def parse_function_body(self) -> ParseTreeNode:
        """Generic function body with return"""
        node = ParseTreeNode("function_body")
        node.add_child(self.parse_func_content())
        return node
    
    def parse_function_body_void(self) -> ParseTreeNode:
        """Function body without mandatory return"""
        node = ParseTreeNode("function_body_void")
        node.add_child(self.parse_func_content_void())
        return node
    
    def parse_func_content(self) -> ParseTreeNode:
        """func_content → using ... | local ... | statement | return ..."""
        node = ParseTreeNode("func_content")
        
        if self.check("using"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_using_cont())
            node.add_child(self.make_terminal(self.match_value(";")))
            node.add_child(self.parse_func_content())
        elif self.check("local"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_mutability())
            node.add_child(self.parse_local_dec_body())
            node.add_child(self.parse_func_content())
        elif self.check("return"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value(";")))
        elif not self.check("}"):
            node.add_child(self.parse_statement_non_return())
            node.add_child(self.parse_func_content())
        
        return node
    
    def parse_func_content_void(self) -> ParseTreeNode:
        """func_content_void → using ... | local ... | statement | return ;"""
        node = ParseTreeNode("func_content_void")
        
        if self.check("using"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_using_cont())
            node.add_child(self.make_terminal(self.match_value(";")))
            node.add_child(self.parse_func_content_void())
        elif self.check("local"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_mutability())
            node.add_child(self.parse_local_dec_body())
            node.add_child(self.parse_func_content_void())
        elif self.check("return"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match_value(";")))
        elif not self.check("}"):
            node.add_child(self.parse_statement_non_return())
            node.add_child(self.parse_func_content_void())
        
        return node
    
    def parse_using_cont(self) -> ParseTreeNode:
        """using_cont → , id using_cont | ε"""
        node = ParseTreeNode("using_cont")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_using_cont())
        return node
    
    def parse_local_dec_body(self) -> ParseTreeNode:
        """local_dec_body → type id local_tail"""
        node = ParseTreeNode("local_dec_body")
        # Type
        if self.peek_value() in TYPE_KEYWORDS:
            node.add_child(self.make_terminal(self.advance()))
        elif self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))
        else:
            raise self.error(first_of("param_type"))
        
        node.add_child(self.make_terminal(self.match("ID")))
        node.add_child(self.parse_local_tail())
        return node
    
    def parse_local_tail(self) -> ParseTreeNode:
        """local_tail → array_with_init ; | = expr local_cont ;"""
        node = ParseTreeNode("local_tail")
        if self.check("["):
            node.add_child(self.parse_array_with_init())
            node.add_child(self.make_terminal(self.match_value(";")))
        elif self.check("="):
            node.add_child(self.make_terminal(self.advance()))
            # Could be literal or expression or { } for weave
            if self.check("{"):
                node.add_child(self.make_terminal(self.advance()))
                node.add_child(self.parse_weave_value_list())
                node.add_child(self.make_terminal(self.match_value("}")))
            else:
                node.add_child(self.parse_expression())
            node.add_child(self.parse_local_cont())
            node.add_child(self.make_terminal(self.match_value(";")))
        else:
            node.add_child(self.make_terminal(self.match_value(";")))
        return node
    
    def parse_local_cont(self) -> ParseTreeNode:
        """local_cont → , id = expr local_cont | ε"""
        node = ParseTreeNode("local_cont")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.make_terminal(self.match_value("=")))
            if self.check("{"):
                node.add_child(self.make_terminal(self.advance()))
                node.add_child(self.parse_weave_value_list())
                node.add_child(self.make_terminal(self.match_value("}")))
            else:
                node.add_child(self.parse_expression())
            node.add_child(self.parse_local_cont())
        return node
    
    # =========================================================================
    # Main Function
    # =========================================================================
    
    def parse_main_body(self) -> ParseTreeNode:
        """main_body → main_content"""
        node = ParseTreeNode("main_body")
        node.add_child(self.parse_main_content())
        return node
    
    def parse_main_content(self) -> ParseTreeNode:
        """
        main_content → using id using_cont ; main_content
                     | local mutability local_dec_body main_content
                     | statement_non_return main_content
                     | return intlit ;
        """
        node = ParseTreeNode("main_content")
        
        if self.check("using"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_using_cont())
            node.add_child(self.make_terminal(self.match_value(";")))
            node.add_child(self.parse_main_content())
        elif self.check("local"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_mutability())
            node.add_child(self.parse_local_dec_body())
            node.add_child(self.parse_main_content())
        elif self.check("return"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("INTLIT")))
            node.add_child(self.make_terminal(self.match_value(";")))
        elif not self.check("}"):
            # statement_non_return
            node.add_child(self.parse_statement_non_return())
            node.add_child(self.parse_main_content())
        
        return node
    
    # =========================================================================
    # Statements
    # =========================================================================
    
    def parse_statement_non_return(self) -> ParseTreeNode:
        """
        statement_non_return → effect_stmt ;
                             | io_stmt
                             | ctrl_struct
        """
        node = ParseTreeNode("statement_non_return")
        
        if self.check("trap", "thread", "threadln"):
            node.add_child(self.parse_io_stmt())
        elif self.check("if", "switch", "for", "while", "do"):
            node.add_child(self.parse_ctrl_struct())
        else:
            # effect_stmt (assignments, calls, ++/--)
            node.add_child(self.parse_effect_stmt())
            node.add_child(self.make_terminal(self.match_value(";")))
        
        return node
    
    def parse_io_stmt(self) -> ParseTreeNode:
        """
        io_stmt → trap ( trap_target ) ;
                | thread ( print_args ) ;
                | threadln ( print_args ) ;
        """
        node = ParseTreeNode("io_stmt")
        
        if self.check("trap"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_trap_target())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value(";")))
        elif self.check("thread", "threadln"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_print_args())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value(";")))
        else:
            raise self.error(first_of("io_stmt"))
        
        return node
    
    def parse_trap_target(self) -> ParseTreeNode:
        """trap_target → id | id [ expr ]"""
        node = ParseTreeNode("trap_target")
        node.add_child(self.make_terminal(self.match("ID")))
        if self.check("["):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value("]")))
        return node
    
    def parse_print_args(self) -> ParseTreeNode:
        """print_args → expression print_args_tail | ε"""
        node = ParseTreeNode("print_args")
        if not self.check(")"):
            node.add_child(self.parse_expression())
            node.add_child(self.parse_print_args_tail())
        return node
    
    def parse_print_args_tail(self) -> ParseTreeNode:
        """print_args_tail → , expression print_args_tail | ε"""
        node = ParseTreeNode("print_args_tail")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.parse_print_args_tail())
        return node
    
    # =========================================================================
    # Control Structures
    # =========================================================================
    
    def parse_ctrl_struct(self) -> ParseTreeNode:
        """
        ctrl_struct → if ( condition ) { stmt_list } else_opt
                    | switch ( arg_expr ) { case_list default_opt }
                    | for ( for_init ; for_cond ; for_update ) { stmt_list }
                    | while ( condition ) { stmt_list }
                    | do { stmt_list } while ( condition ) ;
        """
        node = ParseTreeNode("ctrl_struct")
        
        if self.check("if"):
            node.add_child(self.make_terminal(self.advance()))  # if
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_condition())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_stmt_list())
            node.add_child(self.make_terminal(self.match_value("}")))
            node.add_child(self.parse_else_opt())
            
        elif self.check("switch"):
            node.add_child(self.make_terminal(self.advance()))  # switch
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_case_list())
            node.add_child(self.parse_default_opt())
            node.add_child(self.make_terminal(self.match_value("}")))
            
        elif self.check("for"):
            node.add_child(self.make_terminal(self.advance()))  # for
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_for_init())
            node.add_child(self.make_terminal(self.match_value(";")))
            node.add_child(self.parse_for_cond())
            node.add_child(self.make_terminal(self.match_value(";")))
            node.add_child(self.parse_for_update())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_loop_stmt_list())
            node.add_child(self.make_terminal(self.match_value("}")))
            
        elif self.check("while"):
            node.add_child(self.make_terminal(self.advance()))  # while
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_condition())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_loop_stmt_list())
            node.add_child(self.make_terminal(self.match_value("}")))
            
        elif self.check("do"):
            node.add_child(self.make_terminal(self.advance()))  # do
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_loop_stmt_list())
            node.add_child(self.make_terminal(self.match_value("}")))
            node.add_child(self.make_terminal(self.match_value("while")))
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_condition())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value(";")))
        else:
            raise self.error("do, for, if, switch, while")
        
        return node
    
    def parse_else_opt(self) -> ParseTreeNode:
        """else_opt → else else_body | ε"""
        node = ParseTreeNode("else_opt")
        if self.check("else"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_else_body())
        return node
    
    def parse_else_body(self) -> ParseTreeNode:
        """else_body → { stmt_list } | if ( condition ) { stmt_list } else_opt"""
        node = ParseTreeNode("else_body")
        if self.check("{"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_stmt_list())
            node.add_child(self.make_terminal(self.match_value("}")))
        elif self.check("if"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match_value("(")))
            node.add_child(self.parse_condition())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.make_terminal(self.match_value("{")))
            node.add_child(self.parse_stmt_list())
            node.add_child(self.make_terminal(self.match_value("}")))
            node.add_child(self.parse_else_opt())
        else:
            raise self.error("{, if")
        return node
    
    def parse_stmt_list(self) -> ParseTreeNode:
        """stmt_list → statement stmt_list | ε"""
        node = ParseTreeNode("stmt_list")
        while not self.check("}") and not self.at_end():
            node.add_child(self.parse_statement_non_return())
        return node
    
    def parse_loop_stmt_list(self) -> ParseTreeNode:
        """loop_stmt_list → loop_statement loop_stmt_list | ε"""
        node = ParseTreeNode("loop_stmt_list")
        while not self.check("}") and not self.at_end():
            if self.check("break"):
                node.add_child(self.make_terminal(self.advance()))
                node.add_child(self.make_terminal(self.match_value(";")))
            else:
                node.add_child(self.parse_statement_non_return())
        return node
    
    def parse_case_list(self) -> ParseTreeNode:
        """case_list → case case_val : stmt_list break_opt case_list | ε"""
        node = ParseTreeNode("case_list")
        while self.check("case"):
            node.add_child(self.make_terminal(self.advance()))  # case
            node.add_child(self.parse_case_val())
            node.add_child(self.make_terminal(self.match_value(":")))
            node.add_child(self.parse_case_stmt_list())
            node.add_child(self.parse_break_opt())
        return node
    
    def parse_case_val(self) -> ParseTreeNode:
        """case_val → intlit | longlit | charlit | true | false"""
        node = ParseTreeNode("case_val")
        if self.check_type("INTLIT", "LONGLIT", "CHARLIT") or self.check("true", "false"):
            node.add_child(self.make_terminal(self.advance()))
        else:
            raise self.error(first_of("case_val"))
        return node
    
    def parse_case_stmt_list(self) -> ParseTreeNode:
        """Statements within a case block"""
        node = ParseTreeNode("case_stmt_list")
        while not self.check("case", "default", "}", "break") and not self.at_end():
            node.add_child(self.parse_statement_non_return())
        return node
    
    def parse_break_opt(self) -> ParseTreeNode:
        """break_opt → break ; | ε"""
        node = ParseTreeNode("break_opt")
        if self.check("break"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match_value(";")))
        return node
    
    def parse_default_opt(self) -> ParseTreeNode:
        """default_opt → default : stmt_list break_opt | ε"""
        node = ParseTreeNode("default_opt")
        if self.check("default"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match_value(":")))
            node.add_child(self.parse_case_stmt_list())
            node.add_child(self.parse_break_opt())
        return node
    
    def parse_for_init(self) -> ParseTreeNode:
        """for_init → local mutability type id = expr | id = expr | ε"""
        node = ParseTreeNode("for_init")
        if self.check("local"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_mutability())
            node.add_child(self.make_terminal(self.advance()))  # type
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.make_terminal(self.match_value("=")))
            node.add_child(self.parse_expression())
        elif self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))  # id
            node.add_child(self.make_terminal(self.match_value("=")))
            node.add_child(self.parse_expression())
        # else: epsilon
        return node
    
    def parse_for_cond(self) -> ParseTreeNode:
        """for_cond → condition | ε"""
        node = ParseTreeNode("for_cond")
        if not self.check(";"):
            node.add_child(self.parse_condition())
        return node
    
    def parse_for_update(self) -> ParseTreeNode:
        """for_update → id for_update_tail | ++id | --id | ε"""
        node = ParseTreeNode("for_update")
        if self.check("++"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
        elif self.check("--"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
        elif self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_for_update_tail())
        return node
    
    def parse_for_update_tail(self) -> ParseTreeNode:
        """for_update_tail → ++ | -- | assign_op expr"""
        node = ParseTreeNode("for_update_tail")
        if self.check("++", "--"):
            node.add_child(self.make_terminal(self.advance()))
        elif self.check("=", "+=", "-=", "*=", "/=", "%="):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
        return node
    
    # =========================================================================
    # Effect Statements (side effects: assignments, calls, ++/--)
    # =========================================================================
    
    def parse_effect_stmt(self) -> ParseTreeNode:
        """
        effect_stmt → ++id effect_chain
                    | --id effect_chain
                    | id effect_id_cont
        """
        node = ParseTreeNode("effect_stmt")
        
        if self.check("++"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_effect_chain())
        elif self.check("--"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_effect_chain())
        elif self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_effect_id_cont())
        else:
            raise self.error(first_of("effect_stmt"))
        
        return node
    
    def parse_effect_chain(self) -> ParseTreeNode:
        """effect_chain → [ expr ] effect_chain | . id effect_chain | ε"""
        node = ParseTreeNode("effect_chain")
        if self.check("["):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value("]")))
            node.add_child(self.parse_effect_chain())
        elif self.check("."):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_effect_chain())
        return node
    
    def parse_effect_id_cont(self) -> ParseTreeNode:
        """
        effect_id_cont → = expr
                       | += expr | -= expr | *= expr | /= expr | %= expr
                       | ++ | --
                       | ( arg_list ) effect_call_cont
                       | [ expr ] effect_arr_cont
                       | . id effect_member_cont
        """
        node = ParseTreeNode("effect_id_cont")
        
        if self.check("="):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
        elif self.check("+=", "-=", "*=", "/=", "%="):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
        elif self.check("++", "--"):
            node.add_child(self.make_terminal(self.advance()))
        elif self.check("("):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_arg_list())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.parse_effect_call_cont())
        elif self.check("["):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value("]")))
            node.add_child(self.parse_effect_arr_cont())
        elif self.check("."):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_effect_member_cont())
        else:
            raise self.error(first_of("assign_op") + ", ++, --, (, [, .")
        
        return node
    
    def parse_effect_call_cont(self) -> ParseTreeNode:
        """Continue after function call in effect stmt"""
        node = ParseTreeNode("effect_call_cont")
        if self.check("."):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_effect_member_cont())
        elif self.check("["):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value("]")))
            node.add_child(self.parse_effect_arr_cont())
        return node
    
    def parse_effect_arr_cont(self) -> ParseTreeNode:
        """Continue after array access in effect stmt"""
        node = ParseTreeNode("effect_arr_cont")
        if self.check("["):
            # 2D array
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value("]")))
            node.add_child(self.parse_effect_simple_cont())
        else:
            node.add_child(self.parse_effect_simple_cont())
        return node
    
    def parse_effect_simple_cont(self) -> ParseTreeNode:
        """Simple continuation: assignment or postfix"""
        node = ParseTreeNode("effect_simple_cont")
        if self.check("=", "+=", "-=", "*=", "/=", "%="):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
        elif self.check("++", "--"):
            node.add_child(self.make_terminal(self.advance()))
        elif self.check("."):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_effect_member_cont())
        elif self.check("("):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_arg_list())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.parse_effect_call_cont())
        return node
    
    def parse_effect_member_cont(self) -> ParseTreeNode:
        """Continue after member access"""
        node = ParseTreeNode("effect_member_cont")
        if self.check("=", "+=", "-=", "*=", "/=", "%="):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
        elif self.check("++", "--"):
            node.add_child(self.make_terminal(self.advance()))
        elif self.check("("):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_arg_list())
            node.add_child(self.make_terminal(self.match_value(")")))
            node.add_child(self.parse_effect_call_cont())
        elif self.check("["):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value("]")))
            node.add_child(self.parse_effect_arr_cont())
        elif self.check("."):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.make_terminal(self.match("ID")))
            node.add_child(self.parse_effect_member_cont())
        return node
    
    def parse_arg_list(self) -> ParseTreeNode:
        """arg_list → expression arg_tail | ε"""
        node = ParseTreeNode("arg_list")
        if not self.check(")"):
            node.add_child(self.parse_expression())
            node.add_child(self.parse_arg_tail())
        return node
    
    def parse_arg_tail(self) -> ParseTreeNode:
        """arg_tail → , expression arg_tail | ε"""
        node = ParseTreeNode("arg_tail")
        if self.check(","):
            node.add_child(self.make_terminal(self.advance()))
            node.add_child(self.parse_expression())
            node.add_child(self.parse_arg_tail())
        return node
    
    # =========================================================================
    # Expressions - Precedence-Based Recursive Descent
    # =========================================================================
    #
    # Precedence (lowest to highest):
    #   1. Assignment: =, +=, -=, *=, /=, %= (right-associative)
    #   2. Logical OR: || (left-associative)
    #   3. Logical AND: && (left-associative)
    #   4. Equality: ==, != (left-associative)
    #   5. Relational: <, >, <=, >= (left-associative)
    #   6. Additive: +, -, .. (left-associative)
    #   7. Multiplicative: *, /, % (left-associative)
    #   8. Unary: !, -, ++, -- (right-associative, prefix)
    #   9. Postfix: (), [], ., ++, -- (left-associative)
    #  10. Primary: literals, identifiers, parenthesized, type casts
    #
    # =========================================================================
    
    # Assignment operators (right-associative)
    ASSIGN_OPS = {"=", "+=", "-=", "*=", "/=", "%="}
    
    def parse_expression(self) -> ParseTreeNode:
        """
        expression → assignment
        
        Entry point for expression parsing.
        """
        return self.parse_assignment()
    
    def parse_assignment(self) -> ParseTreeNode:
        """
        assignment → logical_or ( assign_op assignment )?
        
        Right-associative: a = b = c parses as a = (b = c)
        """
        left = self.parse_logical_or()
        
        if self.peek_value() in self.ASSIGN_OPS:
            node = ParseTreeNode("assignment")
            node.add_child(left)
            node.add_child(self.make_terminal(self.advance()))  # operator
            node.add_child(self.parse_assignment())  # right-recursive for right-associativity
            return node
        
        return left
    
    def parse_logical_or(self) -> ParseTreeNode:
        """
        logical_or → logical_and ( '||' logical_and )*
        
        Left-associative: a || b || c parses as (a || b) || c
        """
        left = self.parse_logical_and()
        
        while self.check("||"):
            node = ParseTreeNode("logical_or")
            node.add_child(left)
            node.add_child(self.make_terminal(self.advance()))  # ||
            node.add_child(self.parse_logical_and())
            left = node
        
        return left
    
    def parse_logical_and(self) -> ParseTreeNode:
        """
        logical_and → equality ( '&&' equality )*
        
        Left-associative: a && b && c parses as (a && b) && c
        """
        left = self.parse_equality()
        
        while self.check("&&"):
            node = ParseTreeNode("logical_and")
            node.add_child(left)
            node.add_child(self.make_terminal(self.advance()))  # &&
            node.add_child(self.parse_equality())
            left = node
        
        return left
    
    def parse_equality(self) -> ParseTreeNode:
        """
        equality → relational ( ('==' | '!=') relational )*
        
        Left-associative: a == b != c parses as (a == b) != c
        """
        left = self.parse_relational()
        
        while self.check("==", "!="):
            node = ParseTreeNode("equality")
            node.add_child(left)
            node.add_child(self.make_terminal(self.advance()))  # == or !=
            node.add_child(self.parse_relational())
            left = node
        
        return left
    
    def parse_relational(self) -> ParseTreeNode:
        """
        relational → additive ( ('<' | '>' | '<=' | '>=') additive )*
        
        Left-associative: a < b > c parses as (a < b) > c
        """
        left = self.parse_additive()
        
        while self.check("<", ">", "<=", ">="):
            node = ParseTreeNode("relational")
            node.add_child(left)
            node.add_child(self.make_terminal(self.advance()))  # operator
            node.add_child(self.parse_additive())
            left = node
        
        return left
    
    def parse_additive(self) -> ParseTreeNode:
        """
        additive → multiplicative ( ('+' | '-' | '..') multiplicative )*
        
        Left-associative: a + b - c parses as (a + b) - c
        '..' is string concatenation in PORTIA
        """
        left = self.parse_multiplicative()
        
        while self.check("+", "-", ".."):
            node = ParseTreeNode("additive")
            node.add_child(left)
            node.add_child(self.make_terminal(self.advance()))  # operator
            node.add_child(self.parse_multiplicative())
            left = node
        
        return left
    
    def parse_multiplicative(self) -> ParseTreeNode:
        """
        multiplicative → unary ( ('*' | '/' | '%') unary )*
        
        Left-associative: a * b / c parses as (a * b) / c
        """
        left = self.parse_unary()
        
        while self.check("*", "/", "%"):
            node = ParseTreeNode("multiplicative")
            node.add_child(left)
            node.add_child(self.make_terminal(self.advance()))  # operator
            node.add_child(self.parse_unary())
            left = node
        
        return left
    
    def parse_unary(self) -> ParseTreeNode:
        """
        unary → ('!' | '-' | '++' | '--') unary
              | postfix
        
        Right-associative (prefix): --++x parses as --(++x)
        """
        if self.check("!", "-", "++", "--"):
            node = ParseTreeNode("unary")
            node.add_child(self.make_terminal(self.advance()))  # operator
            node.add_child(self.parse_unary())  # right-recursive
            return node
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ParseTreeNode:
        """
        postfix → primary postfix_chain
        
        postfix_chain → '(' arg_list ')' postfix_chain    (function call)
                      | '[' expression ']' postfix_chain  (array subscript)
                      | '.' ID postfix_chain              (member access)
                      | '++'                              (postfix increment)
                      | '--'                              (postfix decrement)
                      | ε
        
        Left-associative: a.b[c](d) parses as ((a.b)[c])(d)
        """
        left = self.parse_primary()
        
        while True:
            if self.check("("):
                # Function call: expr(args)
                node = ParseTreeNode("call")
                node.add_child(left)
                node.add_child(self.make_terminal(self.advance()))  # (
                node.add_child(self.parse_arg_list())
                node.add_child(self.make_terminal(self.match_value(")")))
                left = node
                
            elif self.check("["):
                # Array subscript: expr[index]
                node = ParseTreeNode("subscript")
                node.add_child(left)
                node.add_child(self.make_terminal(self.advance()))  # [
                node.add_child(self.parse_expression())
                node.add_child(self.make_terminal(self.match_value("]")))
                left = node
                
            elif self.check("."):
                # Member access: expr.field
                node = ParseTreeNode("member_access")
                node.add_child(left)
                node.add_child(self.make_terminal(self.advance()))  # .
                node.add_child(self.make_terminal(self.match("ID")))
                left = node
                
            elif self.check("++"):
                # Postfix increment: expr++
                node = ParseTreeNode("postfix_inc")
                node.add_child(left)
                node.add_child(self.make_terminal(self.advance()))  # ++
                left = node
                
            elif self.check("--"):
                # Postfix decrement: expr--
                node = ParseTreeNode("postfix_dec")
                node.add_child(left)
                node.add_child(self.make_terminal(self.advance()))  # --
                left = node
                
            else:
                break
        
        return left
    
    def parse_primary(self) -> ParseTreeNode:
        """
        primary → INTLIT | LONGLIT | FLOATLIT | DOUBLELIT | CHARLIT | STRINGLIT
                | 'true' | 'false'
                | ID
                | '(' expression ')'
                | type '(' expression ')'   (type cast)
        """
        node = ParseTreeNode("primary")
        
        # Literals
        if self.check_type("INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT", "CHARLIT", "STRINGLIT"):
            node.add_child(self.make_terminal(self.advance()))
            return node
        
        # Boolean literals
        if self.check("true", "false"):
            node.add_child(self.make_terminal(self.advance()))
            return node
        
        # Parenthesized expression
        if self.check("("):
            node.add_child(self.make_terminal(self.advance()))  # (
            node.add_child(self.parse_expression())
            node.add_child(self.make_terminal(self.match_value(")")))
            return node
        
        # Type cast: int(expr), string(expr), etc.
        if self.peek_value() in TYPE_KEYWORDS:
            cast_node = ParseTreeNode("type_cast")
            cast_node.add_child(self.make_terminal(self.advance()))  # type
            cast_node.add_child(self.make_terminal(self.match_value("(")))
            cast_node.add_child(self.parse_expression())
            cast_node.add_child(self.make_terminal(self.match_value(")")))
            return cast_node
        
        # Identifier
        if self.check_type("ID"):
            node.add_child(self.make_terminal(self.advance()))
            return node
        
        # Error: unexpected token
        raise self.error(first_of("expression"))
    
    def parse_condition(self) -> ParseTreeNode:
        """
        condition → expression
        
        Conditions are just expressions that evaluate to boolean.
        """
        node = ParseTreeNode("condition")
        node.add_child(self.parse_expression())
        return node