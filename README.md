# BLAIZE-V3.2
# 🎥 Blaize V3 con MediaPipe - Versión Ejecutable

**Versión standalone - No requiere Processing**

---

## 🚀 Inicio Rápido

### Primera vez (instalar dependencias):

1. Ejecuta: **`INSTALAR_DEPENDENCIAS.bat`**
   - Instala las librerías Python necesarias
   - Solo necesitas hacer esto una vez

### Uso normal:

2. Ejecuta: **`EJECUTAR_BLAIZE_MEDIAPIPE.bat`**
   - Abre automáticamente el tracker y Blaize V3
   - ¡Listo para usar!

---

## 📂 Archivos Incluidos

```
windows-amd64/
│
├── 🎯 EJECUTAR_BLAIZE_MEDIAPIPE.bat  ← EJECUTAR ESTO (después de instalar)
├── 🔧 INSTALAR_DEPENDENCIAS.bat      ← EJECUTAR ESTO PRIMERO
├── 📊 START_TRACKER.bat              (Abre solo el tracker)
│
├── 🎮 Blaize-V3-Modified-main.exe    (Programa principal)
├── 🤖 mediapipe_tracker_gui.py       (Tracker con interfaz)
├── 📦 pose_landmarker_lite.task      (Modelo MediaPipe 5.5MB)
│
├── data/                              (Logos e imágenes)
├── java/                              (Java embebido)
└── lib/                               (Librerías Processing)
```

---

## 🎮 Cómo Usar

### 1️⃣ Configurar el Tracker
   - Selecciona tu **cámara** y **resolución**
   - Elige el **punto de seguimiento** (nariz, mano, etc.)
   - Ajusta la **visualización** (esqueleto, punto, nada)

### 2️⃣ Conectar con Blaize V3
   - En Blaize V3, selecciona **PRESET 15** o **PRESET 32**
   - En el tracker, haz clic en **"Iniciar Tracking"**
   - ¡El logo seguirá tu movimiento!

### 3️⃣ Controles de Blaize
   - **Doble clic** o **F**: Pantalla completa
   - **D**: Mostrar/ocultar info debug
   - **1/2**: Cambiar logo (en PRESET 15/32)
   - **Clic derecho en logo**: Cargar logo personalizado

---

## 📋 Requisitos

- ✅ Windows 10/11
- ✅ Python 3.8+ ([Descargar](https://www.python.org/downloads/))
- ✅ Webcam USB u OBS Virtual Camera

---

## ⚠️ Solución de Problemas

### Python no encontrado
→ Descarga desde [python.org](https://www.python.org/downloads/)  
→ Durante instalación, marca **"Add Python to PATH"**

### Error al instalar dependencias
→ Abre CMD como administrador:
```cmd
pip install opencv-python mediapipe numpy pillow
```

### Tracker no abre
→ Ejecuta solo: `START_TRACKER.bat` para ver errores

### Cámara no aparece
→ Verifica que funcione en otras apps  
→ Reinicia el tracker  
→ Prueba diferentes resoluciones

### Lag o lentitud
→ Reduce resolución a 640x480  
→ Cambia visualización a "Nada" o "Solo Punto"

---

## 📊 Configuración Recomendada

| Resolución | Rendimiento | Precisión |
|------------|-------------|-----------|
| 640x480    | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| 1280x720   | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |

💡 **Tip**: Mejor iluminación = mejor tracking

---

## 📦 Distribución

Este paquete contiene:
- **Blaize V3**: Versión modificada con soporte MediaPipe
- **MediaPipe Tracker**: Sistema de seguimiento corporal
- **Todo incluido**: No necesitas instalar Processing

**Tamaño total**: ~110 MB

---

**Desarrollado para Blaize V3**  
MediaPipe Plugin - Versión Standalone  
Febrero 2026

