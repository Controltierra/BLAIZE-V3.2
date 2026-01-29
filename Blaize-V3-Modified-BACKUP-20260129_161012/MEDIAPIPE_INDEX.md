# 📚 MediaPipe Integration - Índice de Documentación

## 🚀 Inicio Rápido

**Si es tu primera vez**, comienza aquí:
1. [MEDIAPIPE_QUICKSTART.md](MEDIAPIPE_QUICKSTART.md) - Guía de inicio en 3 pasos

## 📖 Documentación

### Para Usuarios
- [MEDIAPIPE_QUICKSTART.md](MEDIAPIPE_QUICKSTART.md) - Inicio rápido (3 minutos)
- [MEDIAPIPE_SETUP.md](MEDIAPIPE_SETUP.md) - Instalación y configuración completa
- [MEDIAPIPE_TROUBLESHOOTING.md](MEDIAPIPE_TROUBLESHOOTING.md) - Solución de problemas

### Para Desarrolladores
- [MEDIAPIPE_TECHNICAL.md](MEDIAPIPE_TECHNICAL.md) - Arquitectura y detalles técnicos
- [README.md](README.md) - Documentación general del proyecto

## 🛠️ Archivos del Proyecto

### Scripts Python
- `mediapipe_tracker.py` - Tracker principal con webcam
- `test_mediapipe_connection.py` - Test de conexión sin cámara

### Scripts Windows
- `start_mediapipe.bat` - Iniciar tracker (doble clic)
- `test_connection.bat` - Test de conexión (doble clic)

### Código Processing
- `Blaize_V3.pde` - Código principal con integración MediaPipe (Preset 32)

## 📝 Flujo de Trabajo Recomendado

### Primera Vez
1. Lee [MEDIAPIPE_QUICKSTART.md](MEDIAPIPE_QUICKSTART.md)
2. Instala dependencias: `pip install mediapipe opencv-python`
3. Ejecuta `test_connection.bat` para verificar
4. Si funciona, ejecuta `start_mediapipe.bat` para tracking real

### Uso Regular
1. Abre Blaize V3
2. Doble clic en `start_mediapipe.bat`
3. Selecciona Preset 32
4. ¡Disfruta!

### Solución de Problemas
1. Revisa [MEDIAPIPE_TROUBLESHOOTING.md](MEDIAPIPE_TROUBLESHOOTING.md)
2. Ejecuta `test_connection.bat` primero
3. Verifica logs en consola de Processing y terminal Python

### Personalización Avanzada
1. Lee [MEDIAPIPE_TECHNICAL.md](MEDIAPIPE_TECHNICAL.md)
2. Modifica `mediapipe_tracker.py` según tus necesidades
3. Ajusta parámetros en `Blaize_V3.pde` (caso 32)

## 🎯 Casos de Uso por Documento

| Quiero... | Lee este documento |
|-----------|-------------------|
| Empezar rápido | [MEDIAPIPE_QUICKSTART.md](MEDIAPIPE_QUICKSTART.md) |
| Instalar todo correctamente | [MEDIAPIPE_SETUP.md](MEDIAPIPE_SETUP.md) |
| Resolver un error | [MEDIAPIPE_TROUBLESHOOTING.md](MEDIAPIPE_TROUBLESHOOTING.md) |
| Entender cómo funciona | [MEDIAPIPE_TECHNICAL.md](MEDIAPIPE_TECHNICAL.md) |
| Modificar el código | [MEDIAPIPE_TECHNICAL.md](MEDIAPIPE_TECHNICAL.md) |
| Ver todas las funciones | [README.md](README.md) |

## 🆘 Soporte Rápido

### Problema: No funciona nada
→ [MEDIAPIPE_TROUBLESHOOTING.md](MEDIAPIPE_TROUBLESHOOTING.md) sección "Verificación de Sistema"

### Problema: Funciona pero mal
→ [MEDIAPIPE_TROUBLESHOOTING.md](MEDIAPIPE_TROUBLESHOOTING.md) sección "Problemas Comunes"

### Pregunta: ¿Cómo personalizo X?
→ [MEDIAPIPE_SETUP.md](MEDIAPIPE_SETUP.md) sección "Personalización"

### Pregunta: ¿Cómo funciona internamente?
→ [MEDIAPIPE_TECHNICAL.md](MEDIAPIPE_TECHNICAL.md) todas las secciones

## 📦 Resumen de Archivos

```
Blaize-V3-Modified-main/
├── 📄 README.md                          # Documentación principal
├── 📄 MEDIAPIPE_INDEX.md                 # Este archivo
├── 📄 MEDIAPIPE_QUICKSTART.md            # Inicio rápido
├── 📄 MEDIAPIPE_SETUP.md                 # Instalación completa
├── 📄 MEDIAPIPE_TECHNICAL.md             # Detalles técnicos
├── 📄 MEDIAPIPE_TROUBLESHOOTING.md       # Solución de problemas
├── 🐍 mediapipe_tracker.py               # Tracker principal
├── 🐍 test_mediapipe_connection.py       # Test de conexión
├── 🦇 start_mediapipe.bat                # Inicio rápido Windows
├── 🦇 test_connection.bat                # Test rápido Windows
└── 🎨 Blaize_V3.pde                      # Código Processing
```

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] `pip install mediapipe opencv-python`
- [ ] Webcam conectada y funcionando
- [ ] Blaize V3 ejecutándose en Processing
- [ ] Test de conexión exitoso (`test_connection.bat`)
- [ ] Preset 32 seleccionado
- [ ] Tracker iniciado (`start_mediapipe.bat`)
- [ ] Spots siguiendo movimientos ✨

---

**¿Listo para empezar?** → [MEDIAPIPE_QUICKSTART.md](MEDIAPIPE_QUICKSTART.md)
