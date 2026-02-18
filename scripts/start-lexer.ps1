# scripts/start-lexer.ps1
# Start the lexer backend with hot-reload using watchfiles
Set-Location "$PSScriptRoot\..\lexer-backend"
Write-Host "Starting Lexer Backend with hot-reload..." -ForegroundColor Blue
Write-Host "Watching for changes in *.py files" -ForegroundColor Yellow
Write-Host ""
& .\.venv-py312\Scripts\watchfiles.exe ".venv-py312\Scripts\python.exe -m uvicorn app.main:app --port 8000" .
