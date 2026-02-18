# scripts/start-parser.ps1
# Start the parser backend with hot-reload using watchfiles
Set-Location "$PSScriptRoot\..\parser-backend"
Write-Host "Starting Parser Backend with hot-reload..." -ForegroundColor Magenta
Write-Host "Watching for changes in *.py files" -ForegroundColor Yellow
Write-Host ""
& .\.venv-py312\Scripts\watchfiles.exe ".venv-py312\Scripts\python.exe -m uvicorn main:app --port 8001" .
