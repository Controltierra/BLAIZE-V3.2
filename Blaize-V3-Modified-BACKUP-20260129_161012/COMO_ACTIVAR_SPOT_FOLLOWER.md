# 🎯 Cómo Activar el Spot Follower con MediaPipe

## Paso a Paso

### 1. Ejecuta Blaize V3
- Abre el archivo `Blaize_V3.pde` en Processing
- Haz clic en el botón **Run** (▶️)
- Se abrirá la ventana fullscreen con los efectos

### 2. Ejecuta el Tracker
- Abre `tracker_control_simple.py`
- O usa el archivo `START_TRACKER.bat`
- Selecciona la cámara y presiona **Iniciar Tracker**

### 3. Activa el Preset 32 en Blaize

El **Preset 32** es el modo MediaPipe Spot Follower con el logo AeroTrax.

#### ¿Cómo sé que está activo?
Cuando Preset 32 está activo verás:
1. El **logo AeroTrax** (esfera) siguiendo el ratón
2. Mensaje discreto abajo: "Esperando MediaPipe..."
3. Cuando lleguen datos: El logo seguirá tu nariz + spots en muñecas y hombros

## 🔧 Solución de Problemas

### "No veo el Preset 32"
- Verifica que modificaste correctamente `Blaize_V3.pde`
- Busca `case 32:` en el código
- Recompila y ejecuta de nuevo

### "El video desaparece cuando me muevo"
Acabo de arreglar esto añadiendo mejor manejo de errores. El video ahora debería seguir mostrándose incluso si MediaPipe falla temporalmente.

### "El spot no sigue mi movimiento"
1. Verifica que el tracker muestre "Paquetes enviados: X" incrementándose
2. Revisa la consola de Processing - debe mostrar "Received MediaPipe data"
3. Asegúrate de que ambos programas (Python y Processing) están en ejecución

## 🎮 Controles

### En el Tracker (Python)
- **Seleccionar cámara**: Elige de la lista
- **Iniciar**: Comienza envío de datos
- **Detener**: Para el tracker
- **Actualizar Cámaras**: Refresca la lista

### En Blaize (Processing)
- **Cambiar Preset**: Botones numerados o teclas
- **Salir**: Presiona ESC

## 📊 Datos Técnicos

**Preset 32 procesa:**
- Nariz (punto central)
- Hombros (izquierdo y derecho)
- Muñecas (izquierda y derecha)

**Resolución de referencia:**
- Cámara: Puede ser cualquiera (reescalada a 640x480)
- Blaize: 970x1000 píxeles (frameSizeX x frameSizeY)

**Puerto UDP:** 12346 (localhost)
