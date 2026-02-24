# Start PORTIA Compiler - All Services
# Opens separate terminals for lexer, parser, semantic, and frontend.
# Uses uvicorn --reload for Python backends (auto-restarts on .py changes).
# Works on any Windows device regardless of path spaces or venv contents.

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PORTIA Compiler - Starting Services" -ForegroundColor Cyan
Write-Host "   (uvicorn --reload + Vite HMR)"       -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Resolve the project root from the scripts folder location
$scriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Resolve absolute paths (handles spaces in OneDrive / user paths)
$lexerPath    = Join-Path $projectRoot "lexer-backend"
$parserPath   = Join-Path $projectRoot "parser-backend"
$semanticPath = Join-Path $projectRoot "semantic-backend"
$frontendPath = Join-Path $projectRoot "app-frontend"

# Helper: verify a venv python exists before launching
function Assert-Venv {
    param([string]$ServicePath, [string]$ServiceName)
    $py = Join-Path $ServicePath ".venv-py312\Scripts\python.exe"
    if (-not (Test-Path $py)) {
        Write-Host "[!!] $ServiceName venv not found at: $py" -ForegroundColor Red
        Write-Host "     Run: cd $ServicePath; python -m venv .venv-py312; .venv-py312\Scripts\pip install fastapi uvicorn pydantic watchfiles" -ForegroundColor Yellow
        return $false
    }
    return $true
}

# ── Lexer (port 8000) ────────────────────────────────────────────────────────
if (Assert-Venv -ServicePath $lexerPath -ServiceName "Lexer") {
    Write-Host "Starting Lexer Backend...    (port 8000, --reload)" -ForegroundColor Blue
    $lexerCmd = "Set-Location '$lexerPath'; " +
                "Write-Host 'LEXER BACKEND - Port 8000 (--reload)' -ForegroundColor Blue; " +
                "& '.venv-py312\Scripts\python.exe' -m uvicorn app.main:app --reload --port 8000"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $lexerCmd
    Start-Sleep -Seconds 1
}

# ── Parser (port 8001) ───────────────────────────────────────────────────────
if (Assert-Venv -ServicePath $parserPath -ServiceName "Parser") {
    Write-Host "Starting Parser Backend...   (port 8001, --reload)" -ForegroundColor Magenta
    $parserCmd = "Set-Location '$parserPath'; " +
                 "Write-Host 'PARSER BACKEND - Port 8001 (--reload)' -ForegroundColor Magenta; " +
                 "& '.venv-py312\Scripts\python.exe' -m uvicorn main:app --reload --port 8001"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $parserCmd
    Start-Sleep -Seconds 1
}

# ── Semantic (port 8002) ─────────────────────────────────────────────────────
if (Assert-Venv -ServicePath $semanticPath -ServiceName "Semantic") {
    Write-Host "Starting Semantic Backend... (port 8002, --reload)" -ForegroundColor Cyan
    $semanticCmd = "Set-Location '$semanticPath'; " +
                   "Write-Host 'SEMANTIC BACKEND - Port 8002 (--reload)' -ForegroundColor Cyan; " +
                   "& '.venv-py312\Scripts\python.exe' -m uvicorn main:app --reload --port 8002"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $semanticCmd
    Start-Sleep -Seconds 1
}

# ── Frontend (port 5173) ─────────────────────────────────────────────────────
$nodeModules = Join-Path $frontendPath "node_modules"
if (-not (Test-Path $nodeModules)) {
    Write-Host "[!!] Frontend node_modules not found." -ForegroundColor Red
    Write-Host "     Run: cd app-frontend; npm install" -ForegroundColor Yellow
} else {
    Write-Host "Starting Frontend...         (port 5173, Vite HMR)" -ForegroundColor Green
    $frontendCmd = "Set-Location '$frontendPath'; " +
                   "Write-Host 'FRONTEND - Port 5173 (Vite HMR)' -ForegroundColor Green; " +
                   "npm run dev"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   PORTIA Services Launched"             -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Lexer Backend:    http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Parser Backend:   http://localhost:8001" -ForegroundColor Cyan
Write-Host "  Semantic Backend: http://localhost:8002" -ForegroundColor Cyan
Write-Host "  Frontend:         http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Hot-reload: Python backends restart on *.py file changes." -ForegroundColor Yellow
Write-Host "Run .\scripts\stop-all.ps1 to stop all services."          -ForegroundColor Yellow
