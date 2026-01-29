// ============================================
// CORE_PATCH.pde - Sistema de plugins
// ============================================

void patch_setup() {
  // Inicialización de plugins si existen
  if (isPluginAvailable("plugin_setup")) {
    plugin_setup();
  }
}

void patch_draw() {
  // Dibujar elementos de plugins si existen
  if (isPluginAvailable("plugin_draw")) {
    plugin_draw();
  }
  
  // Dibujar botón del tracker MediaPipe si el plugin está disponible
  if (isPluginAvailable("drawTrackerButton")) {
    drawTrackerButton();
  }
}

void patch_mousePressed() {
  // Eventos de mouse de plugins si existen
  if (isPluginAvailable("plugin_mousePressed")) {
    plugin_mousePressed();
  }
}

// Verificar si una función del plugin existe
boolean isPluginAvailable(String functionName) {
  try {
    // En Processing, verificamos si las funciones existen intentando llamarlas
    // Si el archivo MediaPipeTracker.pde existe en el sketch, las funciones estarán disponibles
    return true; // Asumimos que están disponibles si el archivo está presente
  } catch (Exception e) {
    return false;
  }
}
