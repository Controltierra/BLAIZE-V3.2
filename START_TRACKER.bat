@echo off
title MediaPipe Tracker - Blaize V3
echo.
echo ======================================
echo   MediaPipe Tracker - Blaize V3
echo ======================================
echo.
echo Iniciando tracker con interfaz grafica...
echo.

REM Ejecutar el tracker Python con GUI
python mediapipe_tracker_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: No se pudo iniciar el tracker.
    echo.
    echo Posibles causas:
    echo   - Python no esta instalado
    echo   - Falta instalar dependencias
    echo.
    echo Instala las dependencias con:
    echo   pip install opencv-python mediapipe numpy pillow
    echo.
    pause
)