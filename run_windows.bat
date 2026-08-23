@echo off
setlocal
cd /d "%~dp0"

echo.
echo ================================================
echo   Ash Intelligence - Product ^& AI Systems
echo ================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found on PATH.
  echo Install Python 3.11 or 3.12, check Add Python to PATH, then run this file again.
  pause
  exit /b 1
)

if not exist .venv\Scripts\python.exe (
  echo [1/3] Creating local Python environment...
  python -m venv .venv
  if errorlevel 1 goto :fail
)

echo [2/3] Installing/updating dependencies...
.venv\Scripts\python.exe -m pip install -q --upgrade pip
.venv\Scripts\python.exe -m pip install -q -r requirements.txt
if errorlevel 1 goto :fail

echo [3/3] Starting deterministic local demo at http://localhost:8501
set AGENT_MODE=mock
.venv\Scripts\python.exe -m streamlit run app.py
exit /b 0

:fail
echo.
echo Setup failed. See the error above.
pause
exit /b 1
