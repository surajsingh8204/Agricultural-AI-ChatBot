@echo off
REM ============================================
REM KrishiMitra - Stop All Servers
REM ============================================

title KrishiMitra - Stopping Servers
color 0C

echo.
echo  ============================================
echo   🛑 Stopping KrishiMitra Servers
echo  ============================================
echo.

REM Kill Node.js processes (frontend)
echo  Stopping Frontend (Node.js)...
taskkill /F /IM node.exe 2>nul
if %errorlevel%==0 (
    echo   ✅ Frontend stopped
) else (
    echo   ⚠️ Frontend was not running
)

REM Kill Python/Uvicorn processes (backend)
echo  Stopping Backend (Python/Uvicorn)...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq KrishiMitra Backend*" 2>nul
if %errorlevel%==0 (
    echo   ✅ Backend stopped
) else (
    echo   ⚠️ Backend was not running
)

echo.
echo  ============================================
echo   ✅ All servers stopped!
echo  ============================================
echo.

timeout /t 3
