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
    echo +- Opening README.txt -+
    notepad "%~dp0README.txt"
)

:CONTINUE
:: Reset to normal colors
color 07
cls

echo +- Installer Started -+
set "BASEDIR=%~dp0"
set "APPDIR=%BASEDIR%"
cd /d "%APPDIR%"
timeout /t 1 >nul

:: ===============================================
:: Step 1 - Check Python
:: ===============================================
echo.
echo +- [Step 1] Checking for Python -+
timeout /t 1 >nul
python --version >nul 2>&1
if %errorlevel%==0 (
    echo +- Python already installed -+
    timeout /t 2 >nul
) else (
    echo +- ⚠️ Python not found -+
    echo Choose installer:
    echo 1 - Install Python 64-bit
    echo 2 - Install Python 32-bit
    echo 3 - Skip installation
    choice /c 123 /n /m "Enter choice: "
    if errorlevel 3 (
        echo +- Skipping Python installation -+
        timeout /t 2 >nul
    ) else if errorlevel 2 (
        echo +- Installing Python 32-bit... -+
        timeout /t 1 >nul
        if exist "%APPDIR%\Installers\Python86.exe" (
            start /wait "" "%APPDIR%\Installers\Python86.exe" PrependPath=1 /quiet
            echo +- Python 32-bit installed -+
        ) else (
            echo +- Python86.exe not found! -+
        )
        timeout /t 2 >nul
    ) else if errorlevel 1 (
        echo +- Installing Python 64-bit... -+
        timeout /t 1 >nul
        if exist "%APPDIR%\Installers\Python64.exe" (
            start /wait "" "%APPDIR%\Installers\Python64.exe" PrependPath=1 /quiet
            echo +- Python 64-bit installed -+
        ) else (
            echo +- Python64.exe not found! -+
        )
        timeout /t 2 >nul
    )
)

:: ===============================================
:: Step 2 - Set up Python requirements
:: ===============================================
cls
echo.
echo +- [Step 2] Setting up Python requirements -+
timeout /t 1 >nul
echo +- Upgrading pip... -+
pip install --upgrade pip --quiet
echo +- Installing required Python packages... -+
pip install psutil --quiet
echo +- Python setup complete -+
timeout /t 2 >nul

:: ===============================================
:: Step 3 - Launch CleanupApp
:: ===============================================
cls
echo.
echo +- [Step 3] Launching CleanupApp -+
timeout /t 1 >nul

if exist "%APPDIR%\app.pyw" (
    start "" pythonw "%APPDIR%\app.pyw"
    echo +- app.pyw started successfully -+
) else (
    echo +- ⚠️ app.pyw not found! -+
)

cls
echo +- Installer Finished -+
echo +- All done! Enjoy CleanupApp -+
timeout /t 2 >nul
