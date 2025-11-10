# FastAPI backend for PORTIA Lexer
# Exposes REST API endpoint for lexical analysis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.lexer.portia_lexer import LexicalAnalyzer

app = FastAPI()

# CORS configuration for frontend integration
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    # Request model for code submission
    code: str

@app.get("/")
def root():
    # Health check endpoint
    return {"message": "PORTIA Lexer backend is running"}

@app.post("/lex")
def lex_code(req: CodeRequest):
    # Main lexical analysis endpoint
    # Takes source code and returns tokens and errors
    lexer = LexicalAnalyzer()
    return lexer.transition(req.code)

