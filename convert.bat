@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM  MarkItDown Batch Converter  (MIT License)
REM  Converts documents to Markdown (.md)
REM
REM  One-time setup:  pip install markitdown[all]
REM  Usage:
REM    Double-click to convert all files in current folder
REM    Or drag-and-drop a file/folder onto this .bat file
REM ============================================================

REM Unset broken proxy (may interfere with markitdown)
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=

REM Find Python: prefer .venv, fall back to system python
set "PYTHON="
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON=%~dp0.venv\Scripts\python.exe"
) else (
    where python >nul 2>&1
    if !errorlevel! equ 0 set "PYTHON=python"
)

if "%PYTHON%"=="" (
    echo [ERROR] Python is not installed or not in PATH.
    echo Install Python from https://python.org, then run: pip install markitdown[all]
    pause
    exit /b 1
)

REM Find script: next to this .bat, or alongside it
set "SCRIPT=%~dp0scripts\batch_convert.py"

REM Source: first argument, or current directory
set "SRC=%~1"
if "%SRC%"=="" set "SRC=%CD%"

REM Output: second argument, or md_output under source
set "OUT=%~2"
if "%OUT%"=="" set "OUT=%SRC%\md_output"

REM === Check markitdown installed ===
"%PYTHON%" -c "import markitdown" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] markitdown is not installed.
    echo Run: pip install markitdown[all]
    echo.
    choice /c yn /m "Install now with pip?"
    if errorlevel 2 exit /b 1
    echo Installing markitdown...
    "%PYTHON%" -m pip install markitdown[all]
    if errorlevel 1 (
        echo [ERROR] Installation failed. Please install manually.
        pause
        exit /b 1
    )
)

echo ============================================================
echo   MarkItDown - Convert Files to Markdown
echo   Source: %SRC%
echo   Output: %OUT%
echo ============================================================
echo.

if not exist "%SCRIPT%" (
    echo [ERROR] Script not found: %SCRIPT%
    pause
    exit /b 1
)

"%PYTHON%" "%SCRIPT%" "%SRC%" --out "%OUT%" --recursive

echo.
echo Done. Check the output folder.
pause
