from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.lexer.portia_lexer import LexicalAnalyzer

app = FastAPI()

# Allow your frontend dev server
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

@app.get("/")
def root():
    return {"message": "PORTIA Lexer backend is running"}

@app.post("/lex")
def lex_code(req: CodeRequest):
    lexer = LexicalAnalyzer()
    return lexer.scan(req.code)

