# semantic-backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from semantic.api import router as semantic_router

app = FastAPI(title="PORTIA Semantic Backend (TBA)")

# Only the local frontend/dev servers are allowed to call the semantic API.
# Keeping the list explicit avoids opening the compiler service broadly during
# development.
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

app.include_router(semantic_router, prefix="")

@app.get("/")
def root():
    # Lightweight health endpoint used to confirm that the semantic service is up.
    return {"message": "PORTIA Semantic backend (TBA) is running"}
