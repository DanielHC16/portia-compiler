from .tokens import LexError

def make_error(msg, lexeme, sl, sc, el, ec):
    return LexError(message=msg, lexeme=lexeme, line=sl, column=sc, endLine=el, endColumn=ec)
