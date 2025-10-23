# parser-backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parser.api import router as parser_router

app = FastAPI(title="PORTIA Parser Backend (TBA)")

# Allow local frontend dev server and other backends by default during development
origins = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parser_router, prefix="")

@app.get("/")
def root():
    return {"message": "PORTIA Parser backend (TBA) is running"}
