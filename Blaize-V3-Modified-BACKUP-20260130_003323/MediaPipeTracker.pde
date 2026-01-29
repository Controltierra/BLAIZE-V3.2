// ============================================
// PLUGIN: MediaPipe Tracker
// ============================================
// Tracking de pose en tiempo real con MediaPipe
// Galería de logos dinámica
// Control de visualización de hand spots

// VARIABLES DEL PLUGIN
// ============================================
// NOTA IMPORTANTE: Todas las variables ya están declaradas en Blaize_V3.pde
// (líneas 16-17, 105-118)
// No se redeclaran aquí para evitar errores "duplicate field"
//
// Variables disponibles desde Blaize_V3.pde:
//   - DatagramSocket udpSocket
//   - Thread udpThread
//   - int mpNoseX, mpNoseY
//   - int mpLeftWristX, mpLeftWristY, mpRightWristX, mpRightWristY
//   - int mpLeftShoulderX, mpLeftShoulderY, mpRightShoulderX, mpRightShoulderY
//   - boolean mediaPipeDataReceived
//   - int udpPacketsReceived
//   - boolean showHandSpots
//   - PImage[] logoGallery
//   - String[] logoNames
//   - int currentLogoIndex
//   - int totalLogos


// VARIABLES DEL BOTÓN TRACKER
Process trackerProcess = null;
boolean trackerIsRunning = false;
int trackerCheckCounter = 0;

void plugin_setup() {
  println("========================================");
  println("Plugin MediaPipe Tracker - Inicializando");
  println("========================================");
  
  // Inicializar UDP para MediaPipe
  try {
    udpSocket = new DatagramSocket(12346);
    println("✓ UDP MediaPipe listener iniciado en puerto 12346");
    
    udpThread = new Thread(new Runnable() {
      public void run() {
        receiveUDP();
      }
    });
    udpThread.start();
  } catch(Exception e) {
    println("✗ Error iniciando UDP: " + e.getMessage());
  }
  
  // Cargar galería de logos
  loadLogoGallery();
  
  // Crear botón Hand Spots si no existe
  if (O.length < 9) {
    println("⚠️ Array O[] muy pequeño para botón Hand Spots");
  } else {
    O[8] = new onoffbutton(color(255, 0, 0), 3*155+5, 5*85+5, 150, 80, 0, "Hand Spots");
  }
  
  println("✓ Plugin MediaPipe Tracker cargado");
}

void plugin_draw() {
  // El código del preset 15 ya maneja el dibujo
  // Aquí podemos agregar debug info si es necesario
}

void drawTrackerButton() {
  // Solo dibujar en lowerPage 1 (Hand Spots)
  if (lowerPage != 1 || hideControlWindow) return;
  
  int panelX = getControlPanelX();
  int btnX = panelX + 470;
  int btnY = 340;
  int btnW = 150;
  int btnH = 80;
  
  // Verificar estado del tracker periódicamente
  trackerCheckCounter++;
  if (trackerCheckCounter > 60) { // Cada segundo aprox
    checkTrackerStatus();
    trackerCheckCounter = 0;
  }
  
  // Detectar si el mouse está sobre el botón
  boolean mouseOver = mouseX > btnX && mouseX < btnX + btnW && 
                      mouseY > btnY && mouseY < btnY + btnH;
  
  // Color del botón según estado
  int btnColor;
  String btnText;
  String statusText;
  
  if (trackerIsRunning) {
    if (mediaPipeDataReceived) {
      btnColor = color(0, 180, 0); // Verde - datos OK
      btnText = "⏹ DETENER";
      statusText = "● DATOS OK";
    } else {
      btnColor = color(200, 150, 0); // Amarillo - sin pose
      btnText = "⏹ DETENER";
      statusText = "⚠ SIN POSE";
    }
  } else {
    btnColor = color(50, 50, 150); // Azul oscuro - inactivo
    btnText = "▶ INICIAR";
    statusText = "○ INACTIVO";
  }
  
  // Hover effect
  if (mouseOver) {
    btnColor = color(red(btnColor) + 30, green(btnColor) + 30, blue(btnColor) + 30);
  }
  
  // Dibujar botón
  fill(btnColor);
  stroke(255);
  strokeWeight(2);
  rect(btnX, btnY, btnW, btnH, 5);
  
  // Texto del botón
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(16);
  text(btnText, btnX + btnW/2, btnY + btnH/2 - 12);
  
  textSize(11);
  text("TRACKER", btnX + btnW/2, btnY + btnH/2 + 8);
  
  // Estado
  textSize(10);
  fill(mediaPipeDataReceived ? color(0, 255, 0) : color(255, 200, 0));
  text(statusText, btnX + btnW/2, btnY + btnH/2 + 25);
  
  // Detectar clic (sin depender de flag)
  if (mouseOver && mousePressed && mouseButton == LEFT) {
    // Usar delay para evitar múltiples clics
    if (trackerIsRunning) {
      stopTracker();
    } else {
      startTracker();
    }
    delay(200); // Pequeña pausa para evitar clics múltiples
  }
}

void startTracker() {
  // Verificar si ya está corriendo
  if (trackerProcess != null && trackerProcess.isAlive()) {
    println("⚠ Tracker ya está en ejecución. Cerrando instancia anterior...");
    stopTracker();
    delay(500);
  }
  
  try {
    String batchPath = sketchPath("START_TRACKER.bat");
    File batchFile = new File(batchPath);
    
    if (!batchFile.exists()) {
      println("✗ No se encuentra START_TRACKER.bat en: " + batchPath);
      return;
    }
    
    println("✓ Iniciando tracker desde: " + batchPath);
    
    ProcessBuilder pb = new ProcessBuilder("cmd.exe", "/c", "start", "/min", "cmd.exe", "/c", batchPath);
    pb.directory(new File(sketchPath("")));
    trackerProcess = pb.start();
    trackerIsRunning = true;
    
    println("✓ Tracker iniciado");
  } catch (Exception e) {
    println("✗ Error iniciando tracker: " + e.getMessage());
    trackerIsRunning = false;
  }
}

void stopTracker() {
  try {
    if (trackerProcess != null && trackerProcess.isAlive()) {
      // Usar taskkill para cerrar el proceso y sus hijos
      long pid = trackerProcess.pid();
      ProcessBuilder pb = new ProcessBuilder("taskkill", "/F", "/T", "/PID", String.valueOf(pid));
      pb.start();
      
      trackerProcess.destroy();
      println("✓ Tracker detenido");
    }
    trackerIsRunning = false;
    trackerProcess = null;
  } catch (Exception e) {
    println("✗ Error deteniendo tracker: " + e.getMessage());
  }
}

void checkTrackerStatus() {
  if (trackerProcess != null) {
    if (!trackerProcess.isAlive()) {
      trackerIsRunning = false;
      trackerProcess = null;
    }
  } else {
    trackerIsRunning = false;
  }
}

void plugin_mousePressed() {
  // Click derecho en slots de logos maneja la carga
}

void plugin_keyPressed() {
  // Navegación de galería de logos
  if (lockscreen == false && key == '1') {
    prevLogo();
  } else if (lockscreen == false && key == '2') {
    nextLogo();
  }
}

// FUNCIONES DEL PLUGIN
// ============================================

// FUNCIONES PRINCIPALES
// ============================================
// NOTA: Las siguientes funciones ya están definidas en Blaize_V3.pde
// y NO deben redeclararse aquí:
//
// void loadLogoGallery()      - línea 1872
// void nextLogo()             - línea 1934
// void prevLogo()             - línea 1939
// PImage getCurrentLogo()     - línea 1944
// void drawLoadLogosButton()  - línea 2020
// void filesSelected()        - línea 2049
// void receiveUDP()           - línea 2099
// void parseMediaPipeData()   - línea 2125

// Cleanup
void plugin_exit() {
  try {
    if (udpSocket != null && !udpSocket.isClosed()) {
      udpSocket.close();
      println("Socket UDP cerrado");
    }
    if (udpThread != null) {
      udpThread.interrupt();
    }
  } catch (Exception e) {
    println("Error cerrando recursos: " + e.getMessage());
  }
}
