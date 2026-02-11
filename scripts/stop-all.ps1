# Stop all PORTIA compiler servers
# Terminates lexer, parser, semantic backends, frontend dev server, and watchfiles processes

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Stopping PORTIA Compiler Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$stopped = 0

# Function to stop process on a specific port
function Stop-ProcessOnPort {
    param (
        [int]$Port,
        [string]$ServiceName
    )
    
    try {
        $processId = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | 
                     Select-Object -ExpandProperty OwningProcess -First 1
        
        if ($processId) {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            Write-Host "[OK] Stopped $ServiceName (Port $Port)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "[--] $ServiceName not running (Port $Port)" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "[!!] Error stopping $ServiceName : $_" -ForegroundColor Red
        return $false
    }
}

# Stop services by port
if (Stop-ProcessOnPort -Port 8000 -ServiceName "Lexer Backend") { $stopped++ }
if (Stop-ProcessOnPort -Port 8001 -ServiceName "Parser Backend") { $stopped++ }
if (Stop-ProcessOnPort -Port 8002 -ServiceName "Semantic Backend") { $stopped++ }
if (Stop-ProcessOnPort -Port 5173 -ServiceName "Frontend Dev Server") { $stopped++ }

# Stop watchfiles processes spawned by PORTIA scripts
Write-Host ""
Write-Host "Stopping watchfiles processes..." -ForegroundColor Yellow

$watchfilesProcs = Get-Process -Name "watchfiles" -ErrorAction SilentlyContinue
foreach ($proc in $watchfilesProcs) {
    try {
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        Write-Host "[OK] Stopped watchfiles process (PID: $($proc.Id))" -ForegroundColor Green
        $stopped++
    }
    catch {
        # Ignore if already stopped
    }
}

# Stop any lingering Python processes from PORTIA backends
Write-Host ""
Write-Host "Stopping lingering Python uvicorn processes..." -ForegroundColor Yellow

$pythonProcs = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
    try {
        $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)" -ErrorAction SilentlyContinue).CommandLine
        $cmdLine -match "uvicorn" -and ($cmdLine -match "8000|8001|8002")
    } catch { $false }
}

foreach ($proc in $pythonProcs) {
    try {
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        Write-Host "[OK] Stopped Python process (PID: $($proc.Id))" -ForegroundColor Green
        $stopped++
    }
    catch {
        # Ignore if already stopped
    }
}

# Close any PowerShell windows running PORTIA services
Write-Host ""
Write-Host "Closing terminal windows..." -ForegroundColor Yellow

$windows = Get-Process powershell -ErrorAction SilentlyContinue | Where-Object { 
    $_.MainWindowTitle -match "LEXER|PARSER|FRONTEND|SEMANTIC" 
}

foreach ($window in $windows) {
    try {
        Stop-Process -Id $window.Id -Force -ErrorAction SilentlyContinue
        Write-Host "[OK] Closed terminal: $($window.MainWindowTitle)" -ForegroundColor Green
    }
    catch {
        # Ignore errors for windows that already closed
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Stopped $stopped process(es)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "All PORTIA services have been shut down." -ForegroundColor Green
