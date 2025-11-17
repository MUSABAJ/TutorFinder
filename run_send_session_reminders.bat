@echo off
REM Wrapper to run Django management command send_session_reminders
REM Place this file in the project root (D:\P1). It will try to use a local venv if present.

:: Switch to the directory where this script lives
cd /d "%~dp0"

:: Prefer virtualenv Python if present at ./venv/Scripts/python.exe
set VENV_PY=%~dp0venv\Scripts\python.exe

if exist "%VENV_PY%" (
    echo Using virtualenv python: %VENV_PY%
    "%VENV_PY%" "%~dp0manage.py" send_session_reminders %*
    EXIT /B %ERRORLEVEL%
) else (
    echo Virtualenv not found at %~dp0venv\Scripts\python.exe
    echo Falling back to system python in PATH
    where python >nul 2>&1
    if %ERRORLEVEL%==0 (
        python "%~dp0manage.py" send_session_reminders %*
        EXIT /B %ERRORLEVEL%
    ) else (
        echo ERROR: No python executable found. Activate your venv or install Python.
        EXIT /B 1
    )
)
