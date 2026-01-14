# Start PORTIA Compiler - All Services
# Runs the lexer backend, parser backend, and frontend in a single terminal

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

# Function to start a service in the background
function Start-Service {
    param(
        [string]$Name,
        [string]$Path,
        [string]$Command,
        [int]$Port
    )
    
    Write-Host "Starting $Name on port $Port..." -ForegroundColor Yellow
    
    $job = Start-Job -ScriptBlock {
        param($path, $cmd)
        Set-Location $path
        Invoke-Expression $cmd
    } -ArgumentList $Path, $Command
    
    return $job
}

# Start services
Write-Host ""
$lexerJob = Start-Service -Name "Lexer Backend" -Path $lexerPath -Command ".\.venv-py312\Scripts\python.exe -m uvicorn app.main:app --port 8000" -Port 8000
Start-Sleep -Seconds 2

$parserJob = Start-Service -Name "Parser Backend" -Path $parserPath -Command ".\.venv-py312\Scripts\python.exe -m uvicorn main:app --port 8001" -Port 8001
Start-Sleep -Seconds 2

$frontendJob = Start-Service -Name "Frontend" -Path $frontendPath -Command "npm run dev" -Port 5173
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   PORTIA Services Running" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Lexer Backend:    http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Parser Backend:   http://localhost:8001" -ForegroundColor Cyan
Write-Host "  Frontend:         http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop all services..." -ForegroundColor Yellow
Write-Host ""

# Monitor jobs and display output
try {
    while ($true) {
        # Check if any job has output
        $lexerJob | Receive-Job | ForEach-Object { Write-Host "[LEXER] $_" -ForegroundColor Blue }
        $parserJob | Receive-Job | ForEach-Object { Write-Host "[PARSER] $_" -ForegroundColor Magenta }
        $frontendJob | Receive-Job | ForEach-Object { Write-Host "[FRONTEND] $_" -ForegroundColor Green }
        
        # Check if any job has failed
        if ($lexerJob.State -eq "Failed") {
            Write-Host "Lexer Backend failed!" -ForegroundColor Red
            break
        }
        if ($parserJob.State -eq "Failed") {
            Write-Host "Parser Backend failed!" -ForegroundColor Red
            break
        }
        if ($frontendJob.State -eq "Failed") {
            Write-Host "Frontend failed!" -ForegroundColor Red
            break
        }
        
        Start-Sleep -Milliseconds 500
    }
}
finally {
    # Cleanup - stop all jobs
    Write-Host ""
    Write-Host "Stopping all services..." -ForegroundColor Yellow
    
    Stop-Job $lexerJob -ErrorAction SilentlyContinue
    Stop-Job $parserJob -ErrorAction SilentlyContinue
    Stop-Job $frontendJob -ErrorAction SilentlyContinue
    
    Remove-Job $lexerJob -Force -ErrorAction SilentlyContinue
    Remove-Job $parserJob -Force -ErrorAction SilentlyContinue
    Remove-Job $frontendJob -Force -ErrorAction SilentlyContinue
    
    Write-Host "All services stopped." -ForegroundColor Green
}
