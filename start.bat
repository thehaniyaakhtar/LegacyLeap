@echo off
echo Starting AS/400 Legacy Modernization Assistant...
echo.

echo [1/3] Starting Backend Server...
cd backend
start "Backend Server" cmd /k "python main.py"
timeout /t 3 /nobreak > nul

echo [2/3] Starting Frontend Server...
cd ..\my-legacy-modernizer
start "Frontend Server" cmd /k "npm run dev"
timeout /t 3 /nobreak > nul

echo [3/3] Opening Browser...
start http://localhost:3000

echo.
echo ✅ System started successfully!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
