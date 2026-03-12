# icg-backend/main.py
"""
PORTIA ICG Backend Server
=========================
FastAPI server for Intermediate Code Generation and execution.

Runs on port 8003 by default.

Usage:
    uvicorn main:app --reload --port 8003
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from icg.api import router as icg_router

app = FastAPI(
    title="PORTIA ICG Backend",
    description="Intermediate Code Generator for PORTIA language",
    version="1.0.0",
)

# CORS configuration - allow frontend and other backends
origins = [
    "http://localhost:5173",   # Vite dev server
    "http://localhost:8000",   # Lexer backend
    "http://localhost:8001",   # Parser backend
    "http://localhost:8002",   # Semantic backend
    "http://localhost:8003",   # ICG backend (self)
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
    "http://127.0.0.1:8003",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include ICG router
app.include_router(icg_router, prefix="")


@app.get("/")
def root():
    """Root endpoint - service info."""
    return {
        "service": "PORTIA ICG Backend",
        "version": "1.0.0",
        "endpoints": {
            "/generate": "POST - Generate TAC from AST",
            "/execute": "POST - Execute TAC",
            "/run": "POST - Generate and execute in one call",
            "/health": "GET - Health check",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
