# scripts/start-semantic.ps1
# Start the semantic backend with hot-reload using watchfiles
Set-Location "$PSScriptRoot\..\semantic-backend"
Write-Host "Starting Semantic Backend with hot-reload..." -ForegroundColor Cyan
Write-Host "Watching for changes in *.py files" -ForegroundColor Yellow
Write-Host ""
& .\.venv-py312\Scripts\watchfiles.exe ".venv-py312\Scripts\python.exe -m uvicorn main:app --port 8002" .
