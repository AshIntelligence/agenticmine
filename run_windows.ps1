$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "Ash Intelligence - Product & AI Systems" -ForegroundColor Cyan
Write-Host "Deterministic local launcher" -ForegroundColor DarkGray
Write-Host ""

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not on PATH. Install Python 3.11 or 3.12, then run this script again."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[1/3] Creating virtual environment..."
    python -m venv .venv
}

Write-Host "[2/3] Installing/updating dependencies..."
& .\.venv\Scripts\python.exe -m pip install -q --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -q -r requirements.txt

$env:AGENT_MODE = "mock"
Write-Host "[3/3] Starting demo: http://localhost:8501" -ForegroundColor Green
& .\.venv\Scripts\python.exe -m streamlit run app.py
