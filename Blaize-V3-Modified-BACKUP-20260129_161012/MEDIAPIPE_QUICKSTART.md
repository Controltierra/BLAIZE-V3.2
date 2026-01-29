# 🎯 MediaPipe Spot Follower - Guía Rápida

## ¿Qué hace?

Integra **detección de pose en tiempo real** con MediaPipe para que los spots de Blaize V3 sigan automáticamente tus movimientos corporales. ¡Perfecto para shows en vivo y actuaciones interactivas!

## Instalación Express ⚡

```bash
pip install mediapipe opencv-python
```

## Uso en 3 Pasos 🚀

### 1️⃣ Abre Blaize V3
Ejecuta el proyecto en Processing

### 2️⃣ Selecciona Preset 32
Ve a la última página de presets y selecciona el preset **32** (MediaPipe Follower)

### 3️⃣ Inicia el Tracker
```bash
python mediapipe_tracker.py
```

**¡Listo!** Los spots ahora siguen tu cuerpo en tiempo real 🎉

## Test de Conexión 🧪

Para verificar que todo funciona antes de usar la cámara:
```bash
python test_mediapipe_connection.py
```

## Puntos Detectados 📍

- 🔴 **Nariz** - Centro de la cabeza
- 🔵 **Muñecas** - Manos izquierda/derecha  
- 🟡 **Hombros** - Con efecto glow
- 📏 **Líneas de conexión** - Esqueleto visual

## Controles 🎛️

| Control | Efecto |
|---------|--------|
| **Size** | Tamaño de los spots |
| **Brightness** | Brillo/intensidad |
| **Multicolor** | Alterna colores por punto |
| **'q'** | Detener tracking |

## Documentación Completa 📖

Ver [MEDIAPIPE_SETUP.md](MEDIAPIPE_SETUP.md) para personalización y troubleshooting.

---

**Nota**: Requiere webcam y buena iluminación para mejor detección.
