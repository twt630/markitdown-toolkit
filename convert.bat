@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM  MarkItDown Batch Converter
REM  Converts documents to Markdown (.md)
REM
REM  Usage:
REM    Double-click to convert all supported files in current folder
REM    Or drag-and-drop a file/folder onto this .bat file
REM ============================================================

REM Unset broken proxy (required for markitdown to work)
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=

REM Absolute paths (do NOT modify these)
set "PYTHON=G:\markitdown\.venv\Scripts\python.exe"
set "SCRIPT=G:\markitdown\scripts\batch_convert.py"

REM Source: first argument, or current directory
set "SRC=%~1"
if "%SRC%"=="" set "SRC=%CD%"

REM Output: second argument, or same as source
set "OUT=%~2"
if "%OUT%"=="" set "OUT=%SRC%\md_output"

echo ============================================================
echo   MarkItDown - Convert Files to Markdown
echo   Source: %SRC%
echo   Output: %OUT%
echo ============================================================
echo.

if not exist "%PYTHON%" (
    echo [ERROR] Python not found: %PYTHON%
    echo Ensure markitdown is installed in the project .venv.
    pause
    exit /b 1
)

if not exist "%SCRIPT%" (
    echo [ERROR] Script not found: %SCRIPT%
    pause
    exit /b 1
)

"%PYTHON%" "%SCRIPT%" "%SRC%" --out "%OUT%" --recursive

echo.
echo Done. Check the output folder.
pause
