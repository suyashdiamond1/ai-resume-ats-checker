@echo off
REM Start the API Backend Server
cd /d C:\Users\suyas\CODES\resume
echo Starting AI Resume ATS Checker API Server...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
call .venv\Scripts\python.exe -c "^
import warnings; warnings.filterwarnings('ignore'); ^
from backend.main import app; ^
import uvicorn; ^
uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"
pause
