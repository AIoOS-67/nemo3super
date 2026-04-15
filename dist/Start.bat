@echo off
chcp 65001 >nul
title Nemotron 3 Super x Private KB
cd /d "%~dp0"

echo ============================================================
echo   Nemotron 3 Super x Your Private Knowledge Base
echo ============================================================
echo.

REM --- check python ---
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not detected. Please install Python 3.10+ first:
    echo    https://www.python.org/downloads/
    pause
    exit /b 1
)

REM --- first-run: create venv + install deps ---
if not exist ".venv\Scripts\python.exe" (
    echo [First launch] Creating virtual environment and installing dependencies...
    echo    (takes 3-5 min first time, only runs once^)
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip -q
    python -m pip install -r requirements.txt -q
    echo [Done] Dependencies installed.
    echo.
) else (
    call .venv\Scripts\activate.bat
)

REM --- check API key ---
if not exist ".env" (
    echo [Config] No .env found. Please enter your NVIDIA API Key:
    echo    ^(get one free at https://build.nvidia.com^)
    set /p NVKEY="NVIDIA_API_KEY="
    echo NVIDIA_API_KEY=%NVKEY%> .env
    echo [Saved] Written to .env
    echo.
)

REM --- ingest if chroma_db missing ---
if not exist "chroma_db" (
    if exist "docs\*" (
        echo [Indexing] Building knowledge base for the first time...
        cd rag
        python ingest.py
        cd ..
        echo.
    )
)

REM --- launch ---
echo [Launching] Starting Nemotron 3 Super Chat...
echo    Browser will open shortly. Ctrl+C to stop.
echo.
cd rag
python app.py
pause
