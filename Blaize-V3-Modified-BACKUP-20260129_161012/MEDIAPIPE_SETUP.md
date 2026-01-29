# MediaPipe Spot Follower - Instalación y Uso

## Instalación

### 1. Instalar dependencias de Python
```bash
pip install mediapipe opencv-python
```

## Uso Rápido

### Opción 1: Test de Conexión (Recomendado primero)
```bash
python test_mediapipe_connection.py
```
Este script envía datos de prueba para verificar que la conexión funciona.

### Opción 2: Tracking Real con MediaPipe
```bash
python mediapipe_tracker.py
```
Esto abrirá una ventana con la detección de pose en tiempo real desde tu webcam.

## Configuración en Blaize V3

1. **Abre Blaize V3** en Processing
2. **Selecciona el Preset 32** (última página de presets)
3. Deberías ver el mensaje "Waiting for MediaPipe..."
4. **Ejecuta el tracker de Python** (ver arriba)
5. Los spots ahora seguirán tus movimientos automáticamente!

## Puntos de Tracking

El sistema detecta y sigue estos puntos del cuerpo:
- **Nariz** 🔴 - tracking de cabeza (spot grande)
- **Muñecas** ⚪ - izquierda/derecha (spots medianos)
- **Hombros** 🟡 - izquierda/derecha (spots con efecto glow)

## Controles

- **Speed Slider**: Controla el suavizado del tracking
- **Size Slider**: Tamaño de los spots
- **Brightness Slider**: Brillo de los spots
- **Multicolor**: Alterna colores en diferentes puntos del cuerpo
- Presiona **'q'** en la ventana de MediaPipe para detener el tracking

## Personalización

### Cambiar puerto de comunicación
Edita ambos archivos con el mismo puerto:
- `mediapipe_tracker.py`: línea con `port=12346`
- `Blaize_V3.pde`: línea con `DatagramSocket(12346)`

### Agregar más puntos de tracking
Edita `mediapipe_tracker.py` y agrega landmarks adicionales según la [documentación de MediaPipe](https://google.github.io/mediapipe/solutions/pose.html)

### Ajustar sensibilidad
En `mediapipe_tracker.py`:
```python
self.pose = self.mp_pose.Pose(
    min_detection_confidence=0.5,  # Aumenta para menos falsos positivos
    min_tracking_confidence=0.5    # Aumenta para tracking más estable
)
```

## Resolución de Problemas

### "Waiting for MediaPipe..." no desaparece
- Verifica que el script Python esté corriendo
- Verifica que el puerto 12346 no esté siendo usado por otro programa
- Ejecuta primero `test_mediapipe_connection.py` para verificar la conexión

### Los spots se mueven de forma extraña
- Ajusta `target_width` y `target_height` en `mediapipe_tracker.py` para que coincidan con tu resolución
- Asegúrate de tener buena iluminación para la cámara
- Aumenta `min_tracking_confidence` para mayor estabilidad

### Webcam no detectada
- Verifica que la webcam esté conectada
- Cambia el índice de cámara: `cv2.VideoCapture(0)` a `cv2.VideoCapture(1)` si tienes múltiples cámaras

## Tecnologías Utilizadas

- **MediaPipe Pose** - Detección de pose en tiempo real
- **OpenCV** - Captura y procesamiento de video
- **UDP Sockets** - Comunicación entre Python y Processing
- **JSON** - Formato de datos para coordenadas
