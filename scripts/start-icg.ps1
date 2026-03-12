# scripts/start-icg.ps1
# Start the ICG backend with uvicorn --reload (auto-restarts on .py changes)
Set-Location "$PSScriptRoot\..\icg-backend"
Write-Host "ICG BACKEND - Port 8003 (uvicorn --reload)" -ForegroundColor Cyan
Write-Host "Restarts automatically when *.py files change" -ForegroundColor Yellow
Write-Host ""

# Use shared venv from lexer-backend (has uvicorn, fastapi installed)
$venvPython = "$PSScriptRoot\..\lexer-backend\.venv-py312\Scripts\python.exe"
if (Test-Path $venvPython) {
    & $venvPython -m uvicorn main:app --reload --port 8003
} else {
    Write-Host "ERROR: Virtual environment not found at $venvPython" -ForegroundColor Red
    Write-Host "Please create a virtual environment in lexer-backend first." -ForegroundColor Yellow
    exit 1
}
