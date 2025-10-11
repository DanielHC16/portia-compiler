# app/lexer/lexer.py

from .tokens import Token, LexError

def lex(code: str):
    """
    Minimal stub for the PORTIA lexer.
    Right now it just returns a single dummy token and no errors.
    Replace this with the full scanning logic later.
    """
    tokens = []
    errors = []

    # Example: if code is not empty, return a dummy IDENTIFIER token
    if code.strip():
        tokens.append(Token(
            type="IDENTIFIER",
            lexeme=code.strip(),
            line=1,
            column=1,
            endLine=1,
            endColumn=len(code.strip()) + 1
        ))

    return {
        "tokens": [t.__dict__ for t in tokens],
        "errors": [e.__dict__ for e in errors],
    }
