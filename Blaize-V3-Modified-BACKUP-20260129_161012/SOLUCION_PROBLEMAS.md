# 🔧 Solución de Problemas - MediaPipe Tracker

## Problema: No se ven los puntos de tracking en la previsualización

### ✅ SOLUCIONADO

El problema era que MediaPipe 0.10+ usa una API completamente diferente:
- **Versión antigua**: `mediapipe.solutions.pose` (deprecada)
- **Versión nueva**: `mediapipe.tasks.python.vision`

### Qué se hizo:

1. **Actualicé el código para usar la nueva API**
   - Se usa `PoseLandmarker` en lugar de `Pose()`
   - Requiere un archivo de modelo: `pose_landmarker_lite.task`
   - El modelo se descargó automáticamente (5.5 MB)

2. **Añadí visualización de puntos**
   - Círculos de colores en puntos clave:
     - 🟡 Amarillo: Nariz
     - 🟢 Verde: Hombros
     - 🟣 Magenta: Muñecas
   - Líneas blancas conectando el torso
   - Líneas verdes a las muñecas

3. **Añadí mensajes de debug**
   - Python muestra: "✓ Pose detectada y datos enviados"
   - Processing muestra: "✓ Paquetes UDP recibidos: X"
   - Verás un log cada segundo aproximadamente

## Problema: El Preset 32 no responde a MediaPipe

### Diagnóstico:

El Preset 32 **SÍ está funcionando**, lo que pasa es que sigue al ratón cuando no hay datos de MediaPipe. Esto es el comportamiento normal hasta que llegan los primeros datos.

### Cómo verificar que funciona:

1. **Ejecuta Blaize V3** (Processing)
   - Verás en la consola: "✓ UDP Receiver iniciado en puerto 12346"

2. **Activa Preset 32**
   - Verás el mensaje: "Waiting for MediaPipe..."

3. **Ejecuta el tracker** (Python)
   - Selecciona la cámara
   - Presiona "Iniciar Tracker"

4. **Ponte frente a la cámara**
   - En la miniatura verás los puntos de colores apareciendo
   - En Processing verás: "✓ PRIMER dato MediaPipe recibido!"
   - El spot cambiará del ratón a seguir tu cuerpo

## Cómo usar Preset 32

### Paso 1: Verifica que Processing esté recibiendo
```
✓ UDP Receiver iniciado en puerto 12346
✓ Paquetes UDP recibidos: 30
✓ Paquetes UDP recibidos: 60
✓ PRIMER dato MediaPipe recibido!
  Nariz: (485, 320)
```

### Paso 2: Verifica que Python esté enviando
```
✓ MediaPipe cargado correctamente (nueva API tasks)
✓ PoseLandmarker inicializado
✓ Pose detectada y datos enviados (frame 30)
✓ Pose detectada y datos enviados (frame 60)
```

### Paso 3: ¡Muévete!
Cuando todo funciona:
- Los círculos aparecen en tu cuerpo en la miniatura
- Los spots en Blaize siguen tu movimiento
- Ambos programas muestran contadores incrementándose

## Puntos de tracking

El sistema detecta 5 puntos de tu cuerpo:

1. **Nariz** → Centro del spot principal
2. **Hombro izquierdo** → Spot con glow
3. **Hombro derecho** → Spot con glow  
4. **Muñeca izquierda** → Spot mediano
5. **Muñeca derecha** → Spot mediano

## Controles en Blaize

Cuando Preset 32 está activo puedes modificar:

- **presetSize** (0-100): Tamaño de los spots
- **presetBrightness** (0-100): Brillo
- **multiColor**: Activar para múltiples colores
- **presetColor**: Color principal
- **multiColorclr**: Color secundario

## Troubleshooting

### "MediaPipe no disponible"
- Reinstala: `pip install mediapipe opencv-python`
- Verifica versión: `pip show mediapipe` (debe ser >= 0.10)

### "No se pudo iniciar MediaPipe"
- Verifica que existe: `pose_landmarker_lite.task`
- Si no existe, ejecuta: `python download_mediapipe_model.py`

### "El video se congela"
- Verifica que la cámara no esté siendo usada por otra app
- Cierra Zoom, Teams, OBS u otros programas de cámara
- Prueba con otra cámara de la lista

### "Los spots no se mueven"
- Verifica que veas: "✓ PRIMER dato MediaPipe recibido!" en Processing
- Verifica que veas: "✓ Pose detectada..." en Python
- Asegúrate de estar EN ESCENA frente a la cámara
- Prueba con más luz en la habitación

### "Los puntos no se ven en la miniatura"
- Esto es NORMAL si MediaPipe no se pudo cargar
- En ese caso, el proceso externo sigue funcionando
- Los datos se envían igual a Blaize aunque no veas los puntos

## Archivos importantes

- `tracker_control_simple.py` - GUI principal con cámara
- `mediapipe_tracker.py` - Proceso externo (fallback)
- `pose_landmarker_lite.task` - Modelo de MediaPipe (5.5MB)
- `Blaize_V3.pde` - Processing con Preset 32

## ¿Necesitas ayuda?

1. Verifica la consola de Processing para mensajes de UDP
2. Verifica la consola de Python para mensajes de detección
3. Ambos deberían mostrar contadores incrementándose
4. Si no, revisa el firewall de Windows (puerto 12346 UDP)
