# Start PORTIA Compiler - All Services
# Opens separate terminals for lexer, parser, and frontend with hot reload

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PORTIA Compiler - Starting Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory (scripts folder)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# Get the project root (parent of scripts folder)
$projectRoot = Split-Path -Parent $scriptDir

# Define paths
$lexerPath = Join-Path $projectRoot "lexer-backend"
$parserPath = Join-Path $projectRoot "parser-backend"
$frontendPath = Join-Path $projectRoot "app-frontend"

Write-Host "Starting Lexer Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$lexerPath'; Write-Host 'LEXER BACKEND - Port 8000' -ForegroundColor Blue; & .venv-py312\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

Start-Sleep -Seconds 2

Write-Host "Starting Parser Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$parserPath'; Write-Host 'PARSER BACKEND - Port 8001' -ForegroundColor Magenta; & .venv-py312\Scripts\python.exe -m uvicorn main:app --reload --port 8001"

Start-Sleep -Seconds 2

Write-Host "Starting Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'FRONTEND - Port 5173' -ForegroundColor Green; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   PORTIA Services Started" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Lexer Backend:    http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Parser Backend:   http://localhost:8001" -ForegroundColor Cyan
Write-Host "  Frontend:         http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Each service is running in its own terminal window." -ForegroundColor Yellow
Write-Host "Close each terminal window to stop the respective service." -ForegroundColor Yellow
