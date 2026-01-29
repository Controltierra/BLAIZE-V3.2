@echo off
echo ==========================================
echo  MediaPipe Spot Follower - Blaize V3
echo ==========================================
echo.
echo Iniciando tracker de MediaPipe...
echo.
echo INSTRUCCIONES:
echo 1. Asegurate de tener Blaize V3 abierto
echo 2. Selecciona el Preset 32
echo 3. Espera a que se abra la ventana de la camara
echo 4. Presiona 'q' en la ventana para detener
echo.
echo ==========================================
echo.

python mediapipe_tracker.py

pause
