@echo off
setlocal enableextensions

REM =============================================
REM AI Resume ATS Checker - Start Frontend & Backend
REM =============================================

REM Resolve repository root (this script's directory)
set "REPO_DIR=%~dp0"
REM Remove trailing backslash if needed
if "%REPO_DIR:~-1%"=="\" set "REPO_DIR=%REPO_DIR:~0,-1%"

REM Check Python venv
if not exist "%REPO_DIR%\.venv\Scripts\python.exe" (
  echo [ERROR] Python venv not found at %REPO_DIR%\.venv\Scripts\python.exe
  echo         Create it and install deps:
  echo         python -m venv .venv
  echo         .venv\Scripts\pip.exe install -r backend\requirements.txt
  goto :maybe_frontend_only
) else (
  echo [INFO] Using Python venv: %REPO_DIR%\.venv\Scripts\python.exe
)

REM Start Backend (Uvicorn FastAPI) in a new window
set "BACKEND_CMD=-m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"
echo [INFO] Starting Backend on http://127.0.0.1:8000 ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%REPO_DIR%\.venv\Scripts\python.exe' -ArgumentList '%BACKEND_CMD%' -WorkingDirectory '%REPO_DIR%' -WindowStyle Minimized"

REM Small wait to let backend boot
powershell -NoProfile -Command "Start-Sleep -Seconds 2" >nul 2>&1

:maybe_frontend_only
REM Check npm availability
where npm >nul 2>&1
if errorlevel 1 (
  echo [WARN] npm not found in PATH. Skipping frontend start.
  goto :open_browser
)

REM Start Frontend (Vite) in a new window
set "FRONTEND_DIR=%REPO_DIR%\frontend"
if not exist "%FRONTEND_DIR%\package.json" (
  echo [WARN] Frontend directory not found or missing package.json: %FRONTEND_DIR%
  goto :open_browser
)

echo [INFO] Starting Frontend (Vite) on http://localhost:3000 ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath 'npm' -ArgumentList 'run dev' -WorkingDirectory '%FRONTEND_DIR%' -WindowStyle Minimized"

:open_browser
REM Open browser to the app
powershell -NoProfile -Command "Start-Process 'http://localhost:3000'" >nul 2>&1

echo.
echo [DONE] Backend and Frontend started in separate windows.
echo       Keep those windows open while using the app.
echo.
endlocal
exit /b 0
