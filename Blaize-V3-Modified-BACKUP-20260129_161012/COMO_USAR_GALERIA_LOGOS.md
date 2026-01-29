# 🎨 Galería de Logos - Guía de Uso

## ✅ Sistema Implementado

Tu Preset 15 ahora puede usar **cualquier imagen** que añadas a través del botón en el menú de Blaize o manualmente a la carpeta especial.

---

## 🎯 Método 1: Botón de Carga en Blaize (RECOMENDADO)

### Pasos:
1. **Abre Blaize V3**
2. **Navega a la página inferior 1**:
   - Haz clic derecho en la zona inferior del panel de control
   - O presiona el botón central del ratón en la zona inferior
3. **Verás el botón azul**: "CARGAR IMÁGENES A GALERÍA"
   - Muestra cuántos logos tienes actualmente
4. **Haz clic en el botón**
5. **Selecciona una imagen** (PNG, JPG, JPEG o GIF)
6. **¡Listo!** La imagen se copia automáticamente y la galería se recarga

### Ventajas:
- ✅ No necesitas buscar carpetas manualmente
- ✅ Las imágenes se copian automáticamente
- ✅ La galería se actualiza sin reiniciar Blaize
- ✅ Muestra el número de logos disponibles
- ✅ Si el archivo ya existe, lo renombra automáticamente

---

## 📁 Método 2: Copiar Archivos Manualmente

1. Abre la carpeta del proyecto: `Blaize-V3-Modified-main`
2. Ve a la carpeta: **`data/logos/`**
3. **Copia** tus imágenes allí
4. **Reinicia Blaize** para cargar las nuevas imágenes

### Formatos Soportados:
- ✅ PNG (con transparencia)
- ✅ JPG / JPEG
- ✅ GIF

---

## 🎮 Cómo Cambiar de Logo

Cuando estés en **Preset 15**:

### Método 1: Teclado
- Presiona **tecla 1** → Logo anterior
- Presiona **tecla 2** → Logo siguiente

### El Logo Cambiará Automáticamente
- El nombre del logo aparece en pantalla
- En la consola de Processing verás: `"➡️ Logo: nombre_archivo.png"`

---

## 🖼️ Ejemplo de Uso con el Botón

1. **Abre Blaize V3**
2. **Clic derecho en la zona inferior** → vas a lowerPage 1
3. **Clic en "CARGAR IMÁGENES A GALERÍA"**
4. **Selecciona** `mi_logo.png`
5. En la consola verás:
   ```
   ✓ Imagen copiada: mi_logo.png
   ✓ Galería recargada. Total de logos: 2
   ```
6. **Presiona teclas 1 o 2** para cambiar entre logos

---

## 📊 Información en Pantalla

### Con MediaPipe Activo (persona detectada):
```
MediaPipe: ON | Logo: mi_logo.png
```
- El logo sigue tu cabeza
- Spots azules en tus manos

### Sin MediaPipe (solo ratón):
```
Logo: mi_logo.png
[1] Anterior | [2] Siguiente
```
- El logo sigue el cursor del ratón
- Instrucciones de navegación

---

## 🔧 Tips

### Tamaño de Imágenes
- **Recomendado**: 500x500 px o similar (cuadradas)
- **Máximo**: 2000x2000 px (para mejor rendimiento)
- Si son muy grandes, Processing puede tardar en cargarlas

### Transparencia
- Las imágenes **PNG con transparencia** se verán correctamente
- El fondo transparente mostrará el efecto de luz debajo

### Cantidad
- Puedes tener **ilimitadas** imágenes
- Se cargan todas al inicio de Blaize
- Navegas entre ellas con las teclas 1 y 2

### Ubicación del Botón
El botón "CARGAR IMÁGENES A GALERÍA" se encuentra en:
- Panel de control derecho de Blaize
- **Página inferior 1** (lowerPage == 1)
- Parte inferior del panel, debajo de los controles

---

## 🐛 Solución de Problemas

### "No veo el botón"
- Asegúrate de estar en **lowerPage 1**
- Haz clic derecho en la zona inferior del panel
- El botón está en la parte baja, es azul y dice "CARGAR IMÁGENES A GALERÍA"

### "Solo veo el logo AeroTrax"
- Usa el botón para añadir imágenes
- O verifica que las imágenes estén en `data/logos/`
- Revisa la consola de Processing para ver qué logos se cargaron

### "No cambia de logo al presionar 1 o 2"
- Asegúrate de que Blaize no esté en la pantalla de login
- Verifica que estés en Preset 15
- Mira la consola para confirmar que hay múltiples logos

### "Error al cargar imagen"
- Verifica que el archivo no esté corrupto
- Intenta con otro formato (PNG en vez de JPG)
- Revisa que el nombre no tenga caracteres especiales

---

## 📝 Mensajes en Consola

Cuando Blaize inicia, verás:
```
✓ Logo cargado: logo1.png
✓ Logo cargado: foto2.jpg
✓ Logo cargado: icono3.png
✓ Galería cargada: 4 logos
```

Al navegar:
```
➡️ Logo: foto2.jpg
⬅️ Logo: logo1.png
```

---

## 🎯 Resumen Rápido

1. **Pon imágenes** en `data/logos/`
2. **Reinicia Blaize**
3. **Activa Preset 15**
4. **Presiona 1 ó 2** para cambiar
5. **¡Disfruta!** 🎉
