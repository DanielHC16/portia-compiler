# scripts/start-semantic.ps1
# Start the semantic backend with Python 3.12 venv
Set-Location "$PSScriptRoot\..\semantic-backend"
& .\.venv-py312\Scripts\python.exe -m uvicorn main:app --reload --port 8002
