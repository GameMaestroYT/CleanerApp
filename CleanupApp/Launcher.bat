@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

:: Quick splash for authorship
color 0A
echo ==================================================
echo         CleanupApp Installer
echo     Officially created by GameMaestroYT ^& ChatGPT
echo ==================================================
timeout /t 3 /nobreak >nul
cls

:: === RED WARNING ===
color 0C
echo ==================================================
echo   WARNING: If you haven't already, read the README!
echo ==================================================
echo.
choice /c YN /n /m "Do you want to open README.txt now? (Y/N): "
if errorlevel 2 goto CONTINUE
if errorlevel 1 (
    echo Opening README.txt...
    notepad "%~dp0README.txt"
)

:CONTINUE
:: Reset to normal colors
color 07
cls


echo ==== CleanupApp Installer Started ====
set "BASEDIR=%~dp0"
set "APPDIR=%BASEDIR%"

cd /d "%APPDIR%"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel%==0 (
    echo Python is already installed!
) else (
    echo Python not found. Choose an installer:
    echo 1. Install Python 64-bit
    echo 2. Install Python 32-bit
    echo 3. Skip installation
    choice /c 123 /n /m "Enter choice: "
    if errorlevel 3 (
        echo Skipping Python installation.
    ) else if errorlevel 2 (
        if exist "%APPDIR%\Installers\Python86.exe" (
            echo Installing Python 32-bit...
            start /wait "" "%APPDIR%\Installers\Python86.exe" PrependPath=1
        ) else (
            echo Python86.exe not found!
        )
    ) else if errorlevel 1 (
        if exist "%APPDIR%\Installers\Python64.exe" (
            echo Installing Python 64-bit...
            start /wait "" "%APPDIR%\Installers\Python64.exe" PrependPath=1
        ) else (
            echo Python64.exe not found!
        )
    )
)

:: Make sure pip is available and install requirements
echo.
echo === Setting up Python requirements ===
python -m ensurepip --upgrade >nul 2>&1
python -m pip install --upgrade pip
python -m pip install psutil

:: Run CleanupApp
echo.
echo Running CleanupApp...
python "%APPDIR%\app.py"

echo.
echo ==== Installer Finished ====
pause
