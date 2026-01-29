"""
Script para descargar el modelo de MediaPipe Pose Landmarker
"""
import urllib.request
import os

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
MODEL_FILE = "pose_landmarker_lite.task"

def download_model():
    """Descargar modelo si no existe"""
    if os.path.exists(MODEL_FILE):
        print(f"✓ Modelo ya existe: {MODEL_FILE}")
        return True
    
    try:
        print(f"Descargando modelo desde {MODEL_URL}...")
        print("Esto puede tardar un minuto...")
        
        urllib.request.urlretrieve(MODEL_URL, MODEL_FILE)
        
        # Verificar tamaño
        size_mb = os.path.getsize(MODEL_FILE) / (1024 * 1024)
        print(f"✓ Modelo descargado: {MODEL_FILE} ({size_mb:.1f} MB)")
        return True
        
    except Exception as e:
        print(f"✗ Error descargando modelo: {e}")
        return False

if __name__ == "__main__":
    success = download_model()
    if success:
        print("\n✓ ¡Listo! Ya puedes usar el tracker con MediaPipe.")
    else:
        print("\n✗ No se pudo descargar el modelo.")
        print("   Descárgalo manualmente desde:")
        print(f"   {MODEL_URL}")
    
    input("\nPresiona Enter para salir...")
