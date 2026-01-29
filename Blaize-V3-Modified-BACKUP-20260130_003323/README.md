# Blaize V3 Modified

Blaize V3 con panel de control web, drawboard interactivo y control de velocidad.

##  Modificaciones Implementadas

### 1. Password Bypass 
- **Eliminado**: Ya no es necesario introducir contraseña
- Acceso directo a todas las funcionalidades
- Inicio inmediato de Blaize

### 2. Fullscreen Toggle 
- **Tecla F**: Alternar pantalla completa
- **Doble clic**: Alternar pantalla completa
- Funciona en cualquier momento durante la ejecución

### 3. Panel de Control Web 
- Interfaz web completa en **http://localhost:8080**
- Servidor Python integrado (se inicia automáticamente con Blaize)
- Control total desde navegador (PC, tablet, móvil en la misma red)
- Sin necesidad de cables USB

### 4. Line Move Drawboard 
- Canvas interactivo de 400x400px para dibujar trayectorias
- Soporte para mouse y pantallas táctiles
- Throttling inteligente (100ms + 5px mínimo para suavidad)
- Botón Clear para borrar el dibujo
- Los puntos dibujados se envían al preset Line Move en tiempo real

### 5. Follow Speed Control 
- Slider de velocidad 0-100
- **0 = Completamente detenido** (pausa total)
- **50 = Velocidad normal**
- **100 = Velocidad máxima (3x más rápido)**
- Control preciso del movimiento del preset activo

### 6. Python Server Integrado 
- Servidor HTTP se inicia automáticamente con Blaize
- Bridge entre navegador web y Blaize vía TCP
- Sin necesidad de ejecutar scripts manualmente
- Se cierra automáticamente al cerrar Blaize

---

##  Estructura del Proyecto

\\\
Blaize_V3_Modificado/
 Blaize_V3.pde              # Código principal modificado
 data/
    blaize_server.py       # Servidor Python HTTPTCP bridge
    blaize_control.html    # Interfaz web completa
    web_presets/           # Imágenes de presets (30 PNG)
 windows-amd64/             # (No en Git - muy pesado)
    Blaize_V3_Modificado.exe
 README.md                  # Esta documentación
 DOWNLOAD_EXE.md           # Instrucciones para obtener el .exe
 .gitignore
\\\

---

##  Instalación y Uso

### Requisitos
- **Windows 64-bit**
- **Python 3** instalado ([Descargar aquí](https://www.python.org/downloads/))
- **Navegador web** moderno (Chrome, Firefox, Edge)

### Paso 1: Obtener el Ejecutable

**Opción A - Descargar compilado:**
- El .exe es muy grande para GitHub (>100MB)
- Compílalo tú mismo o solicita el archivo

**Opción B - Compilar desde código fuente:**
1. Descargar [Processing 3](https://processing.org/download)
2. Abrir \Blaize_V3.pde\ en Processing
3. File  Export Application  Windows 64-bit + Embed Java
4. El .exe se creará en \windows-amd64/\

### Paso 2: Ejecutar Blaize

1. **Ejecutar el programa:**
   \\\
   windows-amd64/Blaize_V3_Modificado.exe
   \\\

2. **Abrir Panel de Control Web:**
   - El servidor Python se inicia automáticamente
   - Abrir navegador en: **http://localhost:8080**
   - Desde otro dispositivo en la red: **http://TU_IP:8080**

3. **Controles Disponibles en la Web:**
   -  **IP Configuration**: Configurar IP del láser
   -  **Presets**: 32 presets con vista previa
   -  **Colors**: 8 colores predefinidos
   -  **Sliders**: H, S, V, ZOOM, BPM (0-255)
   -  **BPM Direct**: Entrada rápida de BPM
   -  **Drawboard**: Dibujar trayectorias para Line Move
   -  **Follow Speed**: Control de velocidad 0-100
   -  **Functions**: 8 botones de funciones especiales

---

##  Arquitectura Técnica

### Flujo de Comunicación

\\\

 Navegador Web    http://localhost:8080
 (puerto 8080)   

          HTTP (POST/GET)
         

 Python Server    blaize_server.py
 HTTPTCP Bridge 

          TCP (formato: {ID}V{VALUE}C)
         

 Blaize V3        Processing (puerto 12345)
 (Processing)    

\\\

### Protocolo de Comandos TCP

**Formato:** \{ID}V{VALUE}C\

| ID  | Comando | Rango | Descripción |
|-----|---------|-------|-------------|
| 100 | DRAW    | x*100+y | Dibuja punto en Line Move (x,y: 0-400) |
| 101 | CLEAR   | 0     | Limpia drawboard y reinicia contador |
| 102 | SPEED   | 0-100 | Velocidad (0=parado, 100=3x) |
| ... | ...     | ...   | (Otros comandos originales de Blaize) |

---

##  Ejemplos de Código

### En Blaize_V3.pde

\\\java
// Variables globales
Process serverProcess;
boolean serverRunning = false;
float translateSpeed = 1.0;

// Inicio del servidor Python
void setup() {
  String pythonCmd = "python";
  serverProcess = launch(pythonCmd, dataPath("blaize_server.py"));
  serverRunning = true;
}

// Comando 100: Dibujar punto en Line Move
if (_id == 100) {
  int x = _data / 100;
  int y = _data % 100;
  float mappedX = map(x, 0, 400, LMZ[0], LMZ[2]);
  float mappedY = map(y, 0, 400, LMZ[1], LMZ[3]);
  presetPos.add(new PVector(mappedX, mappedY));
}

// Comando 101: Limpiar drawboard
else if (_id == 101) {
  presetPos.clear();
  translateCounter = 0;
}

// Comando 102: Control de velocidad
else if (_id == 102) {
  translateSpeed = map(_data, 0, 100, 0.0, 3.0);
}

// Aplicar velocidad al contador
translateCounter += translateSpeed; // Antes era: += 1.0
\\\

### En blaize_control.html

\\\javascript
// Throttling de dibujo para suavidad
const DRAW_THROTTLE = 100;  // milisegundos
const MIN_DISTANCE = 5;      // píxeles

function sendDrawPoint(x, y) {
  const now = Date.now();
  
  // Throttling temporal
  if (now - lastDrawTime < DRAW_THROTTLE) return;
  
  // Throttling espacial
  const distance = Math.sqrt(
    Math.pow(x - lastDrawX, 2) + 
    Math.pow(y - lastDrawY, 2)
  );
  if (distance < MIN_DISTANCE) return;
  
  // Enviar punto al servidor
  fetch('/draw', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({x, y})
  });
  
  lastDrawTime = now;
  lastDrawX = x;
  lastDrawY = y;
}
\\\

---

##  Troubleshooting

### El servidor no inicia
- Verificar que Python 3 está instalado: \python --version\
- Verificar que el puerto 8080 no esté ocupado
- Cerrar Blaize y volver a abrirlo

### No se conecta al láser
- Verificar IP del láser en el panel web
- Asegurar que el láser está en la misma red
- Probar con \ping IP_DEL_LASER\

### El drawboard no responde
- Refrescar la página del navegador (F5)
- Verificar la consola del navegador (F12) para errores
- Asegurar que Blaize está ejecutándose

### La velocidad no cambia
- El slider afecta solo al preset activo (Line Move, etc.)
- Valor 0 detiene **completamente** el movimiento
- Reiniciar el preset para aplicar nueva velocidad

### El panel web no carga
- Verificar que Blaize está ejecutándose
- Abrir http://localhost:8080 en el navegador
- Verificar que Python 3 está instalado

---

##  Licencia

**GPL-3.0** (heredado de Blaize V3 original)

---

##  Créditos

- **Original**: Blaize V3 by AeroTrax
- **Modificaciones**: Panel web + Drawboard + Speed control
- **Año**: 2026

---

##  Contribuir

Si encuentras bugs o tienes ideas:
1. Abre un Issue en GitHub
2. Describe el problema o mejora
3. Incluye capturas si es posible
