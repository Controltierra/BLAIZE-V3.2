# 🎯 MediaPipe Spot Follower - Solución de Problemas

## Problemas Comunes y Soluciones

### ❌ "Waiting for MediaPipe..." no desaparece

**Causa**: El script de Python no está enviando datos o hay un problema de conexión

**Soluciones**:
1. Verifica que el script esté corriendo:
   ```bash
   python mediapipe_tracker.py
   ```
2. Primero prueba con el test de conexión:
   ```bash
   python test_mediapipe_connection.py
   ```
3. Verifica que el puerto 12346 no esté bloqueado:
   - Cierra otros programas que puedan usar ese puerto
   - Revisa el firewall de Windows

### ❌ Webcam no detectada

**Causa**: OpenCV no encuentra la cámara

**Soluciones**:
1. Verifica que la cámara esté conectada y funcionando
2. Si tienes múltiples cámaras, edita `mediapipe_tracker.py`:
   ```python
   self.cap = cv2.VideoCapture(1)  # Prueba 0, 1, 2...
   ```
3. Verifica permisos de cámara en Windows:
   - Configuración → Privacidad → Cámara

### ❌ Los spots se mueven muy rápido o muy lento

**Causa**: Resolución mal configurada

**Solución**: Edita `mediapipe_tracker.py` y ajusta:
```python
self.target_width = 970   # Tu ancho de pantalla
self.target_height = 1000 # Tu alto de pantalla
```

### ❌ Los spots están desplazados

**Causa**: Mapeo de coordenadas incorrecto

**Solución**: Asegúrate de que `target_width` y `target_height` en Python coincidan con `frameSizeX` y `frameSizeY` en Processing

### ❌ Error "ModuleNotFoundError: No module named 'mediapipe'"

**Causa**: MediaPipe no instalado

**Solución**:
```bash
pip install mediapipe opencv-python
```

### ❌ El tracking es muy inestable

**Causas y soluciones**:
1. **Mala iluminación**: Mejora la luz en la habitación
2. **Demasiada sensibilidad**: Edita `mediapipe_tracker.py`:
   ```python
   self.pose = self.mp_pose.Pose(
       min_detection_confidence=0.7,  # Aumenta (0.5 → 0.7)
       min_tracking_confidence=0.7    # Aumenta (0.5 → 0.7)
   )
   ```
3. **Mucho ruido de fondo**: Usa un fondo simple y uniforme

### ❌ Alta latencia (delay notable)

**Causas y soluciones**:
1. **CPU sobrecargado**: Cierra otros programas
2. **Resolución muy alta**: Edita `mediapipe_tracker.py`:
   ```python
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Reduce (640 → 320)
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # Reduce (480 → 240)
   ```
3. **Framerate muy alto**: Agrega más delay:
   ```python
   time.sleep(0.05)  # 20 FPS en vez de 30
   ```

### ❌ "Socket already in use" o error de puerto

**Causa**: El puerto 12346 ya está siendo usado

**Soluciones**:
1. Cierra Blaize V3 completamente y vuelve a abrirlo
2. Busca procesos que usen el puerto:
   ```powershell
   netstat -ano | findstr :12346
   ```
3. Cambia el puerto en ambos archivos:
   - `mediapipe_tracker.py`: `port=12347`
   - `Blaize_V3.pde`: `DatagramSocket(12347)`

### ❌ Los spots parpadean

**Causa**: Pérdida temporal de tracking

**Soluciones**:
1. Mantente dentro del encuadre de la cámara
2. Aumenta la confianza de tracking:
   ```python
   min_tracking_confidence=0.8
   ```
3. Agrega smoothing (próxima actualización)

## Verificación de Sistema

### Test 1: Conexión UDP
```bash
python test_mediapipe_connection.py
```
✅ Deberías ver spots moviéndose en Blaize V3 (Preset 32)

### Test 2: Detección de Pose
```bash
python mediapipe_tracker.py
```
✅ Deberías ver tu esqueleto dibujado en la ventana de OpenCV

### Test 3: Coordenadas
Mueve tu cuerpo y verifica que:
- Movimiento a la izquierda → Spots van a la izquierda
- Movimiento a la derecha → Spots van a la derecha
- Brazos arriba → Spots arriba
- Brazos abajo → Spots abajo

## Información de Debug

### Activar logs en Python
Agrega al inicio de `mediapipe_tracker.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Ver datos UDP en Processing
Agrega en `parseMediaPipeData()`:
```java
println("Received: Nose X=" + mpNoseX + " Y=" + mpNoseY);
```

## Requerimientos del Sistema

### Mínimo
- **CPU**: Intel i3 / AMD Ryzen 3
- **RAM**: 4 GB
- **Webcam**: 640x480 @ 30fps
- **OS**: Windows 10+

### Recomendado
- **CPU**: Intel i5 / AMD Ryzen 5
- **RAM**: 8 GB
- **Webcam**: 1280x720 @ 60fps
- **OS**: Windows 11

## Soporte

Si ninguna solución funciona:

1. Revisa los logs de Processing (consola)
2. Revisa los logs de Python (terminal)
3. Verifica versiones:
   ```bash
   python --version  # 3.8+
   pip show mediapipe
   pip show opencv-python
   ```

## Configuración Óptima

Para mejor rendimiento y estabilidad:

```python
# mediapipe_tracker.py
min_detection_confidence=0.6
min_tracking_confidence=0.6
CAP_PROP_FRAME_WIDTH=640
CAP_PROP_FRAME_HEIGHT=480
time.sleep(0.033)  # 30 FPS
```

---

**¿Aún tienes problemas?** Revisa [MEDIAPIPE_TECHNICAL.md](MEDIAPIPE_TECHNICAL.md) para más detalles técnicos.
