from .tokens import Token

def advance_pos(ch, line, col):
    if ch == "\n":
        return line + 1, 1
    return line, col + 1

def make_token(ttype, lexeme, sl, sc, el, ec):
    return Token(type=ttype, lexeme=lexeme, line=sl, column=sc, endLine=el, endColumn=ec)
