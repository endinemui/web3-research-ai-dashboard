@echo off
echo Starting local development server...
echo.
echo If Python is not available, install it from: https://python.org
echo.
python -m http.server 8000
echo.
echo Server started at: http://localhost:8000
echo Press Ctrl+C to stop the server
pause