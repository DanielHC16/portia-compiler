# scripts/start-lexer.ps1
# Start the lexer backend with uvicorn --reload (auto-restarts on .py changes)
Set-Location "$PSScriptRoot\..\lexer-backend"
Write-Host "LEXER BACKEND - Port 8000 (uvicorn --reload)" -ForegroundColor Blue
Write-Host "Restarts automatically when *.py files change" -ForegroundColor Yellow
Write-Host ""
& ".venv-py312\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8000
