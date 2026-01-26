# Stop all PORTIA compiler servers
# Terminates lexer backend, parser backend, frontend development server, and closes their windows

Write-Host "Stopping PORTIA Compiler Servers..." -ForegroundColor Cyan
Write-Host ""

# Function to stop process on a specific port and close its window
function Stop-ProcessOnPort {
    param (
        [int]$Port,
        [string]$ServiceName
    )
    
    try {
        $process = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | 
                   Select-Object -ExpandProperty OwningProcess -First 1
        
        if ($process) {
            # Get the process object to access MainWindowHandle
            $processObj = Get-Process -Id $process -ErrorAction SilentlyContinue
            
            # Stop the process
            Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
            
            # Close the window if it exists
            if ($processObj -and $processObj.MainWindowHandle -ne 0) {
                # Send close message to window
                $null = [System.Windows.Forms.SendKeys]::SendWait("%{F4}")
            }
            
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

# Additionally, close any PowerShell windows that might be running the services
Write-Host ""
Write-Host "Closing terminal windows..." -ForegroundColor Yellow

# Get all PowerShell windows with PORTIA-related titles
$windows = Get-Process powershell -ErrorAction SilentlyContinue | Where-Object { 
    $_.MainWindowTitle -match "LEXER|PARSER|FRONTEND|SEMANTIC" 
}

foreach ($window in $windows) {
    try {
        Stop-Process -Id $window.Id -Force -ErrorAction SilentlyContinue
        Write-Host "[OK] Closed terminal window: $($window.MainWindowTitle)" -ForegroundColor Green
    }
    catch {
        # Ignore errors for windows that already closed
    }
}

Write-Host ""
Write-Host "Summary: Stopped $stopped service(s)" -ForegroundColor Cyan
Write-Host ""
Write-Host "All PORTIA servers and terminal windows have been shut down." -ForegroundColor Green
