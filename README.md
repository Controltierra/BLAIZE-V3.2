# BLAIZE-V3.2
# 🎥 Blaize V3 con MediaPipe - Versión Ejecutable

**Versión standalone - No requiere Processing**

---

## 📜 Basado en Blaize V3 Original

Este proyecto es una **versión modificada** de [Blaize V3](https://github.com/bodgedbutworks/Blaize_V3) creado por [bodgedbutworks](https://github.com/bodgedbutworks).

### 🎯 Proyecto Original
- **Repositorio:** [bodgedbutworks/Blaize_V3](https://github.com/bodgedbutworks/Blaize_V3)
- **Autor:** bodgedbutworks
- **Descripción:** Software to turn your projector into a safe disco laser
- **Licencia:** GNU General Public License v3.0

### ✨ Modificaciones en esta Versión (V3.2)
- ✅ Integración con **MediaPipe** para tracking de pose corporal
- ✅ Interfaz gráfica (GUI) en Python para control del tracker
- ✅ Sistema de tracking por UDP en tiempo real
- ✅ Selección de puntos de seguimiento (nariz, manos, hombros)
- ✅ Scripts `.bat` para ejecución simplificada en Windows
- ✅ Versión ejecutable standalone

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

---

## 📄 Licencia

Este proyecto mantiene la licencia **GNU General Public License v3.0** del proyecto original.

- Este es software libre bajo GPL v3
- Puedes redistribuir y/o modificarlo bajo los términos de la GPL v3
- Ver el archivo LICENSE para más detalles
- Proyecto original: [bodgedbutworks/Blaize_V3](https://github.com/bodgedbutworks/Blaize_V3)

---

## 🙏 Agradecimientos

Agradecimiento especial a [bodgedbutworks](https://github.com/bodgedbutworks) por crear el proyecto original Blaize V3.

**Enlaces al proyecto original:**
- 📺 [Demo Video](https://www.youtube.com/watch?v=ziG_0-8F9Vg)
- 📚 [Tutorial Video](https://www.youtube.com/watch?v=TjnYWlusAS8)