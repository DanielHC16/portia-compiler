# scripts/start-parser.ps1
# Start the parser backend with Python 3.12 venv
Set-Location "$PSScriptRoot\..\parser-backend"
& .\.venv-py312\Scripts\python.exe -m uvicorn main:app --reload --port 8001
