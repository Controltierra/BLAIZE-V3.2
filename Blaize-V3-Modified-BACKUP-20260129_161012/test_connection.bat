@echo off
echo ==========================================
echo  Test de Conexion MediaPipe - Blaize V3
echo ==========================================
echo.
echo Este script envia datos de prueba sin usar la camara
echo Para verificar que la conexion funciona correctamente
echo.
echo INSTRUCCIONES:
echo 1. Asegurate de tener Blaize V3 abierto
echo 2. Selecciona el Preset 32
echo 3. Los spots deberian moverse automaticamente
echo 4. Presiona Ctrl+C para detener
echo.
echo ==========================================
echo.

python test_mediapipe_connection.py

pause
