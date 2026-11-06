@echo off
setlocal
title ViralHunter - Buscador de Outliers de YouTube
cls

echo =========================================================================
echo    VIRALHUNTER 2.0 - MOTOR DE OUTLIERS DE YOUTUBE
echo    Arbitraje de Nichos - Clonador de Miniaturas - Transcripciones
echo =========================================================================
echo.
echo [*] Enlace en tu PC:       http://localhost:8500
echo [*] Enlace para tu CELULAR: http://192.168.1.54:8500
echo [*] Boveda de Obsidian:     %~dp0vaul\buscar nicho\
echo.
echo Conectate desde tu celular (estando en el mismo Wi-Fi) abriendo:
echo http://192.168.1.54:8500
echo.

cd /d "%~dp0backend"

:: Abrir navegador en la PC
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8500"

:: Ejecutar servidor escuchando en todas las interfaces (0.0.0.0)
python -m uvicorn server:app --host 0.0.0.0 --port 8500

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] No se pudo iniciar con 'python'.
    echo Intentando con ruta directa...
    "%LOCALAPPDATA%\Python\bin\python.exe" -m uvicorn server:app --host 0.0.0.0 --port 8500
)

pause