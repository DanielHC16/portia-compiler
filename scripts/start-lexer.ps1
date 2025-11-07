# scripts/start-lexer.ps1
# Start the lexer backend with Python 3.12 venv
Set-Location "$PSScriptRoot\..\lexer-backend"
& .\.venv-py312\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
