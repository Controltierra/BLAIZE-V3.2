"""
MediaPipe Tracker Control - Con Preview Integrado
Panel de control con miniatura de video en tiempo real
Compatible con MediaPipe 0.10+
"""
import cv2
import socket
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time
import subprocess
import sys
import subprocess
import platform

# Intentar importar MediaPipe con nueva API
try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    MEDIAPIPE_AVAILABLE = True
    print("✓ MediaPipe cargado correctamente (nueva API tasks)")
except (ImportError, AttributeError) as e:
    MEDIAPIPE_AVAILABLE = False
    print(f"✗ MediaPipe no disponible: {e}")

class TrackerControlWithPreview:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MediaPipe Tracker Control - Blaize V3")
        self.root.geometry("700x750")
        self.root.configure(bg='#2b2b2b')
        
        # Estado
        self.cap = None
        self.is_running = False
        self.tracking_thread = None
        self.tracker_process = None
        self.available_cameras = []
        
        # MediaPipe
        self.pose = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = 'localhost'
        self.port = 12346
        self.target_width = 970
        self.target_height = 1000
        
        # Estadísticas
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        self.packets_sent = 0
        
        self.setup_gui()
        # Detectar cámaras en background al iniciar
        threading.Thread(target=self.detect_cameras_background, daemon=True).start()
        
    def setup_gui(self):
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        
        # Título
        title = ttk.Label(self.root, text="🎥 MediaPipe Tracker - Con Preview", style='Title.TLabel')
        title.pack(pady=10)
        
        # Subtítulo
        subtitle = ttk.Label(self.root, text="Control para Blaize V3", 
                            foreground='#FFC107', font=('Arial', 10))
        subtitle.pack(pady=2)
        
        # Instrucción importante
        instruction = ttk.Label(self.root, text="⚡ En Blaize V3: Selecciona PRESET 32", 
                               foreground='#4CAF50', font=('Arial', 11, 'bold'))
        instruction.pack(pady=5)
        
        # Preview de video
        video_frame = tk.Frame(self.root, bg='black', relief='sunken', borderwidth=2)
        video_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.video_label = tk.Label(video_frame, bg='black', text='📷 Video Preview\n\nClick "Iniciar" para ver la cámara',
                                    fg='#888888', font=('Arial', 12))
        self.video_label.pack(fill='both', expand=True)
        
        # Frame de controles
        controls_frame = tk.Frame(self.root, bg='#3b3b3b', relief='raised', borderwidth=2)
        controls_frame.pack(pady=10, padx=20, fill='x')
        
        # Título de selección
        ttk.Label(controls_frame, text="Selecciona tu Cámara:", 
                 font=('Arial', 11, 'bold')).pack(pady=(10,5))
        
        # Listbox con scroll para cámaras
        list_frame = tk.Frame(controls_frame, bg='#3b3b3b')
        list_frame.pack(pady=5, padx=20, fill='x')
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.camera_listbox = tk.Listbox(list_frame, height=4, 
                                         font=('Arial', 10),
                                         yscrollcommand=scrollbar.set,
                                         selectmode='single',
                                         bg='white', fg='black')
        self.camera_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.camera_listbox.yview)
        
        # Botón refrescar
        refresh_btn = tk.Button(controls_frame, text="🔄 Refrescar Dispositivos", 
                               command=self.refresh_cameras, bg='#2196F3', fg='white',
                               font=('Arial', 10, 'bold'), padx=15, pady=5)
        refresh_btn.pack(pady=5)
        
        # Label de estado de búsqueda
        self.search_label = ttk.Label(controls_frame, text="Buscando cámaras...", 
                                     foreground='#FFC107')
        self.search_label.pack(pady=3)
        
        # Botones principales
        buttons_frame = tk.Frame(controls_frame, bg='#3b3b3b')
        buttons_frame.pack(pady=10)
        
        self.start_btn = tk.Button(buttons_frame, text="▶ Iniciar", 
                                   command=self.start_tracking, bg='#4CAF50', fg='white',
                                   font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(buttons_frame, text="⏹ Detener", 
                                  command=self.stop_tracking, bg='#f44336', fg='white',
                                  font=('Arial', 12, 'bold'), padx=20, pady=10, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        # Estadísticas
        stats_frame = tk.Frame(self.root, bg='#1e1e1e', relief='sunken', borderwidth=2)
        stats_frame.pack(pady=5, padx=20, fill='x')
        
        self.status_label = ttk.Label(stats_frame, text="Estado: Detenido", foreground='#ff9800')
        self.status_label.pack(side='left', padx=10, pady=5)
        
        self.fps_label = ttk.Label(stats_frame, text="FPS: 0", foreground='#4CAF50')
        self.fps_label.pack(side='left', padx=10, pady=5)
        
        self.packets_label = ttk.Label(stats_frame, text="Enviados: 0", foreground='#2196F3')
        self.packets_label.pack(side='left', padx=10, pady=5)
        
    def get_camera_names_windows(self):
        """Obtener nombres reales de cámaras en Windows usando múltiples métodos"""
        camera_names = {}
        try:
            if platform.system() == 'Windows':
                # Método 1: WMI con índices
                try:
                    result = subprocess.run(
                        ['powershell', '-Command', 
                         "Get-CimInstance Win32_PnPEntity | Where-Object {$_.PNPClass -eq 'Camera' -or $_.PNPClass -eq 'Image'} | Select-Object -ExpandProperty Caption"],
                        capture_output=True, text=True, timeout=5
                    )
                    if result.returncode == 0:
                        names = [n.strip() for n in result.stdout.strip().split('\n') if n.strip()]
                        for idx, name in enumerate(names):
                            camera_names[idx] = name
                except:
                    pass
                
                # Método 2: Fallback con Get-PnpDevice
                if not camera_names:
                    try:
                        result = subprocess.run(
                            ['powershell', '-Command', 
                             "Get-PnpDevice -Class Camera | Select-Object -Property FriendlyName | ForEach-Object { $_.FriendlyName }"],
                            capture_output=True, text=True, timeout=5
                        )
                        if result.returncode == 0:
                            names = [n.strip() for n in result.stdout.strip().split('\n') if n.strip()]
                            for idx, name in enumerate(names):
                                camera_names[idx] = name
                    except:
                        pass
        except:
            pass
        return camera_names
    
    def detect_cameras_background(self):
        """Detectar cámaras en background"""
        self.root.after(0, lambda: self.search_label.configure(text="🔍 Buscando cámaras..."))
        
        # Obtener nombres reales de cámaras en Windows
        camera_names = self.get_camera_names_windows()
        
        cameras = []
        detected_count = 0  # Contador de cámaras detectadas realmente
        
        for i in range(10):  # Buscar hasta 10 cámaras
            try:
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # DirectShow para Windows
                if cap.isOpened():
                    ret, frame = cap.read()
                    
                    # Obtener información básica
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    
                    # Intentar obtener nombre real de la cámara
                    # Primero del diccionario de nombres Windows
                    device_name = camera_names.get(detected_count, None)
                    
                    # Si no hay nombre, buscar por índice de dispositivo
                    if not device_name:
                        device_name = camera_names.get(i, f"Cámara USB {i}")
                    
                    # Añadir "icatchtek" si se detecta en las propiedades
                    if "icatch" in str(device_name).lower():
                        device_name = f"iCatchTek {device_name}"
                    
                    # Verificar si está recibiendo señal
                    is_active = ret and frame is not None
                    
                    cameras.append({
                        'index': i,
                        'name': device_name,
                        'resolution': f"{width}x{height}",
                        'fps': fps,
                        'active': is_active
                    })
                    
                    detected_count += 1  # Incrementar contador de cámaras encontradas
                    cap.release()
            except:
                pass
        
        self.available_cameras = cameras
        self.root.after(0, self.update_camera_list)
        
    def update_camera_list(self):
        """Actualizar la lista de cámaras en el UI"""
        self.camera_listbox.delete(0, tk.END)
        
        if not self.available_cameras:
            self.camera_listbox.insert(tk.END, "❌ No se encontraron cámaras")
            self.search_label.configure(text="⚠️ No hay cámaras disponibles")
        else:
            for cam in self.available_cameras:
                status_icon = "🟢" if cam['active'] else "🔴"
                display_text = f"{status_icon} [{cam['index']}] {cam['name']} • {cam['resolution']} @ {cam['fps']}fps"
                self.camera_listbox.insert(tk.END, display_text)
                
                # Colorear según estado
                idx = self.camera_listbox.size() - 1
                if cam['active']:
                    self.camera_listbox.itemconfig(idx, {'fg': '#4CAF50'})  # Verde para activas
                else:
                    self.camera_listbox.itemconfig(idx, {'fg': '#FF5722'})  # Rojo para inactivas
            
            # Seleccionar la primera por defecto
            self.camera_listbox.selection_set(0)
            self.search_label.configure(text=f"✅ {len(self.available_cameras)} cámara(s) encontrada(s)")
    
    def refresh_cameras(self):
        """Refrescar lista de cámaras"""
        if self.is_running:
            messagebox.showwarning("Advertencia", "Detén el tracking antes de refrescar")
            return
        
        self.search_label.configure(text="🔍 Buscando...")
        threading.Thread(target=self.detect_cameras_background, daemon=True).start()
        
    def start_tracking(self):
        """Iniciar tracking con preview"""
        if self.is_running:
            return
        
        # Obtener cámara seleccionada
        selection = self.camera_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Selecciona una cámara de la lista")
            return
        
        if not self.available_cameras:
            messagebox.showerror("Error", "No hay cámaras disponibles")
            return
        
        camera_index = self.available_cameras[selection[0]]['index']
        camera_name = self.available_cameras[selection[0]]['name']
        
        # Intentar abrir cámara con diferentes backends
        self.cap = None
        backends = [
            (cv2.CAP_DSHOW, "DirectShow"),
            (cv2.CAP_MSMF, "Media Foundation"),
            (cv2.CAP_ANY, "Auto")
        ]
        
        for backend, backend_name in backends:
            try:
                print(f"Intentando abrir '{camera_name}' con {backend_name}...")
                cap = cv2.VideoCapture(camera_index, backend)
                if cap.isOpened():
                    # Probar lectura
                    ret, test_frame = cap.read()
                    if ret and test_frame is not None:
                        print(f"✓ Cámara abierta exitosamente con {backend_name}")
                        self.cap = cap
                        break
                    else:
                        print(f"✗ {backend_name}: Cámara abierta pero no devuelve frames")
                        cap.release()
                else:
                    print(f"✗ {backend_name}: No se pudo abrir")
            except Exception as e:
                print(f"✗ {backend_name}: Error - {e}")
        
        if not self.cap or not self.cap.isOpened():
            messagebox.showerror(
                "Error", 
                f"No se pudo abrir la cámara '{camera_name}' (Dispositivo {camera_index})\n\n"
                f"Probado con: DirectShow, Media Foundation, Auto\n\n"
                "Verifica:\n"
                "- Que la cámara no esté siendo usada por otra aplicación\n"
                "- Los permisos de Windows\n"
                "- Prueba con OBS Virtual Camera si está disponible"
            )
            return
        
        # Configurar cámara para mejor rendimiento
        try:
            # Intentar configurar resolución preferida
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Buffer mínimo para reducir latencia
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except:
            pass
        
        # Inicializar MediaPipe si está disponible
        self.pose_detector = None
        if MEDIAPIPE_AVAILABLE:
            try:
                # Verificar que existe el modelo
                import os
                model_path = 'pose_landmarker_lite.task'
                if not os.path.exists(model_path):
                    print(f"✗ MODELO NO ENCONTRADO: {model_path}")
                    print("   Ejecuta: python download_mediapipe_model.py")
                    raise FileNotFoundError(f"Modelo no encontrado: {model_path}")
                
                print(f"✓ Modelo encontrado: {model_path} ({os.path.getsize(model_path) / (1024*1024):.1f} MB)")
                
                # Crear PoseLandmarker con nueva API
                base_options = python.BaseOptions(model_asset_path=model_path)
                options = vision.PoseLandmarkerOptions(
                    base_options=base_options,
                    running_mode=vision.RunningMode.VIDEO,
                    min_pose_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                self.pose_detector = vision.PoseLandmarker.create_from_options(options)
                print("✓ PoseLandmarker inicializado correctamente")
            except Exception as e:
                print(f"✗ Error iniciando MediaPipe: {e}")
                import traceback
                traceback.print_exc()
                print("   Intentando con proceso externo...")
                self.pose_detector = None
        
        # Si MediaPipe no está disponible, usar proceso externo
        if not self.pose_detector:
            try:
                script_path = os.path.join(os.path.dirname(__file__), 'mediapipe_tracker.py')
                self.tracker_process = subprocess.Popen(
                    [sys.executable, script_path, str(camera_index)],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                print(f"✓ Tracker externo iniciado (PID: {self.tracker_process.pid})")
            except Exception as e:
                print(f"✗ No se pudo iniciar tracker externo: {e}")
        
        # Estado
        self.is_running = True
        self.fps_start_time = time.time()
        self.packets_sent = 0
        
        # UI
        self.start_btn['state'] = 'disabled'
        self.stop_btn['state'] = 'normal'
        self.status_label['text'] = "Estado: ▶ ACTIVO"
        self.status_label['foreground'] = '#4CAF50'
        
        # Iniciar thread de preview
        self.tracking_thread = threading.Thread(target=self.preview_loop, daemon=True)
        self.tracking_thread.start()
        
    def stop_tracking(self):
        """Detener tracking"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        if self.pose_detector:
            self.pose_detector.close()
            self.pose_detector = None
        
        if self.tracker_process:
            self.tracker_process.terminate()
            try:
                self.tracker_process.wait(timeout=2)
            except:
                self.tracker_process.kill()
            self.tracker_process = None
        
        # UI
        self.start_btn['state'] = 'normal'
        self.stop_btn['state'] = 'disabled'
        self.status_label['text'] = "Estado: ⏹ Detenido"
        self.status_label['foreground'] = '#ff9800'
        self.video_label.configure(image='', text='📷 Video Preview\n\nClick "Iniciar" para ver la cámara',
                                   fg='#888888')
        
    def preview_loop(self):
        """Loop de preview de video con detección de pose"""
        frame_count = 0
        error_count = 0
        max_errors = 10  # Máximo de errores consecutivos antes de abortar
        
        while self.is_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    error_count += 1
                    if error_count >= max_errors:
                        print(f"✗ Demasiados errores consecutivos ({error_count}), deteniendo...")
                        self.root.after(0, lambda: messagebox.showerror(
                            "Error de cámara",
                            "La cámara dejó de enviar frames.\n\n"
                            "Posibles causas:\n"
                            "- La cámara se desconectó\n"
                            "- Otra aplicación tomó control\n"
                            "- Problema de drivers\n\n"
                            "Prueba con OBS Virtual Camera si está disponible."
                        ))
                        break
                    # Pequeña espera antes de reintentar
                    time.sleep(0.1)
                    continue
                
                # Reset contador de errores si se lee correctamente
                error_count = 0
                
                # Validar que el frame tenga contenido
                if frame.size == 0:
                    print("✗ Frame vacío recibido")
                    continue
                
                # Convertir a RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_count += 1
                
                # Debug: Verificar estado de MediaPipe
                if frame_count == 1:
                    if self.pose_detector:
                        print("✓ MediaPipe PoseLandmarker ACTIVO")
                        print("  Esperando detección de persona en frame...")
                    else:
                        print("⚠️ MediaPipe NO disponible")
                        print("  Usando proceso externo (los puntos no aparecerán en miniatura)")
                
                # Procesar con MediaPipe si está disponible
                pose_detected = False
                if self.pose_detector:
                    try:
                        # Convertir a MediaPipe Image
                        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
                        
                        # Detectar pose
                        timestamp_ms = int(time.time() * 1000)
                        detection_result = self.pose_detector.detect_for_video(mp_image, timestamp_ms)
                        
                        # Dibujar landmarks si se detectaron
                        if detection_result.pose_landmarks:
                            pose_detected = True
                            for pose_landmarks in detection_result.pose_landmarks:
                                # Dibujar puntos en la imagen
                                self.draw_pose_landmarks(image, pose_landmarks)
                                
                                # Enviar datos a Blaize
                                self.send_pose_data_new_api(pose_landmarks)
                                
                                if frame_count % 30 == 1:  # Log cada segundo
                                    print(f"✓ POSE DETECTADA - Dibujando puntos (frame {frame_count})")
                        else:
                            # No se detectó persona
                            if frame_count % 60 == 1:  # Log cada 2 segundos
                                print(f"⚠️ No se detectó persona en frame {frame_count}")
                    except Exception as e:
                        if frame_count % 30 == 1:
                            print(f"✗ Error procesando pose: {e}")
                            import traceback
                            traceback.print_exc()
                
                # Actualizar preview (siempre, aunque falle MediaPipe)
                self.update_preview(image)
                
                # Actualizar FPS
                self.update_fps()
                
                # Pequeño delay
                time.sleep(0.01)
                
            except Exception as e:
                print(f"✗ Error en preview loop: {e}")
                break
            
        self.stop_tracking()
    
    def draw_pose_landmarks(self, image, pose_landmarks):
        """Dibujar landmarks de pose en la imagen"""
        try:
            h, w = image.shape[:2]
            
            # Puntos clave que nos interesan
            NOSE = 0
            LEFT_SHOULDER = 11
            RIGHT_SHOULDER = 12
            LEFT_WRIST = 15
            RIGHT_WRIST = 16
            
            points_drawn = 0
            
            # Dibujar círculos en puntos clave
            for idx in [NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_WRIST, RIGHT_WRIST]:
                if idx < len(pose_landmarks):
                    landmark = pose_landmarks[idx]
                    
                    # Validar que el landmark tenga las propiedades correctas
                    if hasattr(landmark, 'x') and hasattr(landmark, 'y'):
                        x = int(landmark.x * w)
                        y = int(landmark.y * h)
                        
                        # Validar que las coordenadas estén dentro del frame
                        if 0 <= x < w and 0 <= y < h:
                            # Color según el punto
                            if idx == NOSE:
                                color = (255, 255, 0)  # Amarillo para nariz (corregido BGR a RGB)
                                radius = 10
                            elif idx in [LEFT_SHOULDER, RIGHT_SHOULDER]:
                                color = (0, 255, 0)  # Verde para hombros
                                radius = 8
                            else:
                                color = (255, 0, 255)  # Magenta para muñecas
                                radius = 8
                            
                            # Dibujar círculo relleno
                            cv2.circle(image, (x, y), radius, color, -1)
                            # Dibujar borde blanco
                            cv2.circle(image, (x, y), radius + 2, (255, 255, 255), 2)
                            points_drawn += 1
            
            # Log de puntos dibujados (solo primera vez)
            if points_drawn > 0:
                # Añadir texto indicador en la imagen
                cv2.putText(image, f"Puntos: {points_drawn}/5", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Dibujar líneas de conexión
            if len(pose_landmarks) > RIGHT_WRIST:
                def get_point(idx):
                    return (int(pose_landmarks[idx].x * w), int(pose_landmarks[idx].y * h))
                
                # Líneas del torso
                cv2.line(image, get_point(LEFT_SHOULDER), get_point(RIGHT_SHOULDER), (255, 255, 255), 2)
                cv2.line(image, get_point(LEFT_SHOULDER), get_point(NOSE), (255, 255, 255), 2)
                cv2.line(image, get_point(RIGHT_SHOULDER), get_point(NOSE), (255, 255, 255), 2)
                
                # Líneas a muñecas
                cv2.line(image, get_point(LEFT_SHOULDER), get_point(LEFT_WRIST), (0, 255, 0), 2)
                cv2.line(image, get_point(RIGHT_SHOULDER), get_point(RIGHT_WRIST), (0, 255, 0), 2)
                
        except Exception as e:
            print(f"Error dibujando landmarks: {e}")
    
    def send_pose_data_new_api(self, pose_landmarks):
        """Enviar datos de pose a Blaize (nueva API)"""
        try:
            # Índices de landmarks en MediaPipe Pose
            NOSE = 0
            LEFT_SHOULDER = 11
            RIGHT_SHOULDER = 12
            LEFT_WRIST = 15
            RIGHT_WRIST = 16
            
            points = {
                'nose': {
                    'x': int(pose_landmarks[NOSE].x * self.target_width),
                    'y': int(pose_landmarks[NOSE].y * self.target_height)
                },
                'left_wrist': {
                    'x': int(pose_landmarks[LEFT_WRIST].x * self.target_width),
                    'y': int(pose_landmarks[LEFT_WRIST].y * self.target_height)
                },
                'right_wrist': {
                    'x': int(pose_landmarks[RIGHT_WRIST].x * self.target_width),
                    'y': int(pose_landmarks[RIGHT_WRIST].y * self.target_height)
                },
                'left_shoulder': {
                    'x': int(pose_landmarks[LEFT_SHOULDER].x * self.target_width),
                    'y': int(pose_landmarks[LEFT_SHOULDER].y * self.target_height)
                },
                'right_shoulder': {
                    'x': int(pose_landmarks[RIGHT_SHOULDER].x * self.target_width),
                    'y': int(pose_landmarks[RIGHT_SHOULDER].y * self.target_height)
                }
            }
            
            data = json.dumps(points)
            self.sock.sendto(data.encode(), (self.host, self.port))
            self.packets_sent += 1
            
            # Actualizar UI cada 30 paquetes
            if self.packets_sent % 30 == 0:
                self.root.after(0, lambda: self.packets_label.configure(
                    text=f"Enviados: {self.packets_sent}"
                ))
            
        except Exception as e:
            print(f"✗ Error enviando datos: {e}")
        
    def send_pose_data(self, landmarks):
        """Enviar datos de pose a Blaize (API antigua - fallback)"""
        try:
            points = {
                'nose': {
                    'x': int(landmarks[0].x * self.target_width),
                    'y': int(landmarks[0].y * self.target_height)
                },
                'left_wrist': {
                    'x': int(landmarks[15].x * self.target_width),
                    'y': int(landmarks[15].y * self.target_height)
                },
                'right_wrist': {
                    'x': int(landmarks[16].x * self.target_width),
                    'y': int(landmarks[16].y * self.target_height)
                },
                'left_shoulder': {
                    'x': int(landmarks[11].x * self.target_width),
                    'y': int(landmarks[11].y * self.target_height)
                },
                'right_shoulder': {
                    'x': int(landmarks[12].x * self.target_width),
                    'y': int(landmarks[12].y * self.target_height)
                }
            }
            
            data = json.dumps(points)
            self.sock.sendto(data.encode(), (self.host, self.port))
            self.packets_sent += 1
            
            # Actualizar UI cada 30 paquetes para no saturar
            if self.packets_sent % 30 == 0:
                self.root.after(0, lambda: self.packets_label.configure(
                    text=f"Enviados: {self.packets_sent}"
                ))
            
        except Exception as e:
            print(f"Error enviando datos: {e}")
            
    def update_preview(self, image):
        """Actualizar preview de video"""
        # Redimensionar para UI
        h, w = image.shape[:2]
        max_width = 660
        max_height = 400
        
        scale = min(max_width/w, max_height/h)
        new_w, new_h = int(w*scale), int(h*scale)
        
        image_resized = cv2.resize(image, (new_w, new_h))
        
        # Convertir a ImageTk
        image_pil = Image.fromarray(image_resized)
        image_tk = ImageTk.PhotoImage(image_pil)
        
        # Actualizar label
        self.video_label.configure(image=image_tk, text='')
        self.video_label.image = image_tk
        
    def update_fps(self):
        """Actualizar contador de FPS"""
        self.fps_counter += 1
        elapsed = time.time() - self.fps_start_time
        
        if elapsed >= 1.0:
            self.current_fps = self.fps_counter / elapsed
            self.fps_counter = 0
            self.fps_start_time = time.time()
            
            # Actualizar UI
            self.root.after(0, lambda: self.fps_label.configure(
                text=f"FPS: {self.current_fps:.1f}"
            ))
        
    def run(self):
        """Ejecutar aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Cerrar aplicación"""
        self.stop_tracking()
        self.sock.close()
        self.root.destroy()

if __name__ == "__main__":
    app = TrackerControlWithPreview()
    app.run()
