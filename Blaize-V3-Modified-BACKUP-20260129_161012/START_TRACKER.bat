@echo off
echo ================================================
echo  MediaPipe Tracker - Blaize V3
echo ================================================
echo.
echo Verificando modelo de MediaPipe...
if not exist "pose_landmarker_lite.task" (
    echo.
    echo [!] MODELO NO ENCONTRADO
    echo Descargando modelo de MediaPipe...
    python download_mediapipe_model.py
    echo.
)

echo.
echo Iniciando tracker...
echo.
echo INSTRUCCIONES:
echo 1. Selecciona tu camara de la lista
echo 2. Presiona "Iniciar Tracker"
echo 3. En Blaize V3, activa PRESET 32
echo 4. Ponte frente a la camara
echo.
python tracker_control_simple.py
pause
