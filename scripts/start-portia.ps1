# Start PORTIA Compiler - All Services
# Opens separate terminals for lexer, parser, semantic, and frontend with hot reload via watchfiles

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PORTIA Compiler - Starting Services" -ForegroundColor Cyan
Write-Host "   (Hot-Reload via watchfiles)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory (scripts folder)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# Get the project root (parent of scripts folder)
$projectRoot = Split-Path -Parent $scriptDir

# Define paths
$lexerPath = Join-Path $projectRoot "lexer-backend"
$parserPath = Join-Path $projectRoot "parser-backend"
$semanticPath = Join-Path $projectRoot "semantic-backend"
$frontendPath = Join-Path $projectRoot "app-frontend"

Write-Host "Starting Lexer Backend with hot-reload..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$lexerPath'; Write-Host 'LEXER BACKEND - Port 8000 (watchfiles)' -ForegroundColor Blue; Write-Host 'Watching for *.py changes...' -ForegroundColor Yellow; & .venv-py312\Scripts\watchfiles.exe '.venv-py312\Scripts\python.exe -m uvicorn app.main:app --port 8000' ."

Start-Sleep -Seconds 2

Write-Host "Starting Parser Backend with hot-reload..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$parserPath'; Write-Host 'PARSER BACKEND - Port 8001 (watchfiles)' -ForegroundColor Magenta; Write-Host 'Watching for *.py changes...' -ForegroundColor Yellow; & .venv-py312\Scripts\watchfiles.exe '.venv-py312\Scripts\python.exe -m uvicorn main:app --port 8001' ."

Start-Sleep -Seconds 2

Write-Host "Starting Semantic Backend with hot-reload..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$semanticPath'; Write-Host 'SEMANTIC BACKEND - Port 8002 (watchfiles)' -ForegroundColor Cyan; Write-Host 'Watching for *.py changes...' -ForegroundColor Yellow; & .venv-py312\Scripts\watchfiles.exe '.venv-py312\Scripts\python.exe -m uvicorn main:app --port 8002' ."

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
Write-Host "  Semantic Backend: http://localhost:8002" -ForegroundColor Cyan
Write-Host "  Frontend:         http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Hot-reload enabled: Services restart on *.py changes." -ForegroundColor Yellow
Write-Host "Run ./scripts/stop-all.ps1 to stop all services." -ForegroundColor Yellow
