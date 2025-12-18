@echo off
REM ============================================
REM KrishiMitra - Agricultural AI ChatBot
REM Start Full Stack Application
REM ============================================

title KrishiMitra Launcher
color 0A

echo.
echo  ============================================
echo   KrishiMitra - Agricultural AI ChatBot
echo  ============================================
echo.
echo  Starting Full Stack Application...
echo.

REM Set project root directory
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

echo  Project Root: %PROJECT_ROOT%
echo.

REM ============================================
REM Check if conda is available
REM ============================================
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo  [ERROR] Conda not found in PATH!
    echo  Please install Anaconda/Miniconda or add it to PATH.
    pause
    exit /b 1
)

REM ============================================
REM Start Backend Server (FastAPI)
REM ============================================
echo  [1/3] Starting Backend Server (Port 5000)...
start "KrishiMitra Backend" cmd /k "cd /d "%PROJECT_ROOT%" && conda activate agri-llm && python -m uvicorn chatbot_backend.main:app --host 0.0.0.0 --port 5000 --reload"

REM Wait for backend to initialize
echo  Waiting for backend to initialize (8 seconds)...
timeout /t 8 /nobreak > nul

REM ============================================
REM Start Frontend Server (React + Vite)
REM ============================================
echo  [2/3] Starting Frontend Server (Port 5173)...
start "KrishiMitra Frontend" cmd /k "cd /d "%PROJECT_ROOT%chatbot-frontend\AGRI-BOT" && npm run dev"

REM Wait for frontend to initialize
echo  Waiting for frontend to initialize (5 seconds)...
timeout /t 5 /nobreak > nul

REM ============================================
REM Open Browser
REM ============================================
echo  [3/3] Opening browser...
timeout /t 2 /nobreak > nul
start "" "http://localhost:5173"

echo.
echo  ============================================
echo   KrishiMitra is now running!
echo  ============================================
echo.
echo   Frontend:  http://localhost:5173
echo   Backend:   http://localhost:5000
echo   API Docs:  http://localhost:5000/docs
echo.
echo   Two terminal windows are now open:
echo   - KrishiMitra Backend (Python/FastAPI)
echo   - KrishiMitra Frontend (Node.js/Vite)
echo.
echo   To stop: Close both terminal windows
echo   or run stop_krishimitra.bat
echo.
echo   Press any key to close this launcher...
echo  ============================================
echo.

pause > nul
