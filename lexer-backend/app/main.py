from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.lexer.lexer import lex

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LexRequest(BaseModel):
    code: str

@app.post("/lex")
def lex_endpoint(req: LexRequest):
    return lex(req.code)
