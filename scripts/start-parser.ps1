# scripts/start-parser.ps1
# Activate venv if you use one, then run uvicorn
# Example: .\.venv\Scripts\Activate.ps1
uvicorn parser-backend.main:app --reload --port 8001
