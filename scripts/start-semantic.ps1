# scripts/start-semantic.ps1
# Start the semantic backend with uvicorn --reload (auto-restarts on .py changes)
Set-Location "$PSScriptRoot\..\semantic-backend"
Write-Host "SEMANTIC BACKEND - Port 8002 (uvicorn --reload)" -ForegroundColor Cyan
Write-Host "Restarts automatically when *.py files change" -ForegroundColor Yellow
Write-Host ""
& ".venv-py312\Scripts\python.exe" -m uvicorn main:app --reload --port 8002
