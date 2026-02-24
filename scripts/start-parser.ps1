# scripts/start-parser.ps1
# Start the parser backend with uvicorn --reload (auto-restarts on .py changes)
Set-Location "$PSScriptRoot\..\parser-backend"
Write-Host "PARSER BACKEND - Port 8001 (uvicorn --reload)" -ForegroundColor Magenta
Write-Host "Restarts automatically when *.py files change" -ForegroundColor Yellow
Write-Host ""
& ".venv-py312\Scripts\python.exe" -m uvicorn main:app --reload --port 8001
