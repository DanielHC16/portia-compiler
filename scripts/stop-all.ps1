# Stop all PORTIA compiler servers
# Terminates lexer backend, parser backend, and frontend development server

Write-Host "Stopping PORTIA Compiler Servers..." -ForegroundColor Cyan
Write-Host ""

# Function to stop process on a specific port
function Stop-ProcessOnPort {
    param (
        [int]$Port,
        [string]$ServiceName
    )
    
    try {
        $process = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | 
                   Select-Object -ExpandProperty OwningProcess -First 1
        
        if ($process) {
            Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
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

# Stop all services
$stopped = 0

# Stop Lexer Backend (port 8000)
if (Stop-ProcessOnPort -Port 8000 -ServiceName "Lexer Backend") {
    $stopped++
}

# Stop Parser Backend (port 8001)
if (Stop-ProcessOnPort -Port 8001 -ServiceName "Parser Backend") {
    $stopped++
}

# Stop Semantic Backend (port 8002)
if (Stop-ProcessOnPort -Port 8002 -ServiceName "Semantic Backend") {
    $stopped++
}

# Stop Frontend Dev Server (port 5173)
if (Stop-ProcessOnPort -Port 5173 -ServiceName "Frontend Dev Server") {
    $stopped++
}

Write-Host ""
Write-Host "Summary: Stopped $stopped service(s)" -ForegroundColor Cyan
Write-Host ""
Write-Host "All PORTIA servers have been shut down." -ForegroundColor Green
