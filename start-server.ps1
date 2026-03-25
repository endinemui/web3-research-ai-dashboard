# PowerShell script to start local development server
Write-Host "Starting local development server..." -ForegroundColor Green
Write-Host ""
Write-Host "If Python is not available, install it from: https://python.org" -ForegroundColor Yellow
Write-Host ""

try {
    # Try Python 3 first
    python -m http.server 8000
} catch {
    try {
        # Try Python 2 as fallback
        python -m SimpleHTTPServer 8000
    } catch {
        Write-Host "Python not found. Please install Python or use Node.js alternative." -ForegroundColor Red
        Write-Host "Node.js alternative: npx http-server -p 8000" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Server started at: http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray