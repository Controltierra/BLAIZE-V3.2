"""
MediaPipe Tracker con GUI - Selección de cámara y monitoreo
Versión mejorada con interfaz gráfica para Blaize V3
Compatible con MediaPipe 0.10+
"""
import cv2
import mediapipe as mp
import socket
import json
import time
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import numpy as np

class MediaPipeTrackerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MediaPipe Tracker - Blaize V3")
        self.root.geometry("800x700")
        self.root.configure(bg='#2b2b2b')
        
        # MediaPipe setup - Compatible con nueva API
        try:
            # Intentar API antigua (mediapipe < 0.10)
            self.mp_pose = mp.solutions.pose
            self.mp_drawing = mp.solutions.drawing_utils
            self.use_new_api = False
        except AttributeError:
            # Usar API nueva (mediapipe >= 0.10)
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision
            self.mp_vision = vision
            self.mp_python = python
            self.use_new_api = True
            
        self.pose = None
        
        # Socket setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = 'localhost'
        self.port = 12346
        
        # Estado
        self.cap = None
        self.is_running = False
        self.camera_index = 0
        self.target_width = 970
        self.target_height = 1000
        
        # Estadísticas
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        self.packets_sent = 0
        
        self.setup_gui()
        self.detect_cameras()
        
    def setup_gui(self):
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        
        # Título
        title = ttk.Label(self.root, text="🎥 MediaPipe Tracker - Blaize V3", style='Title.TLabel')
        title.pack(pady=10)
        
        # Frame de controles
        controls_frame = tk.Frame(self.root, bg='#2b2b2b')
        controls_frame.pack(pady=10, padx=20, fill='x')
        
        # Selección de cámara
        ttk.Label(controls_frame, text="Cámara:").grid(row=0, column=0, padx=5, sticky='w')
        self.camera_combo = ttk.Combobox(controls_frame, width=40, state='readonly')
        self.camera_combo.grid(row=0, column=1, padx=5)
        self.camera_combo.bind('<<ComboboxSelected>>', self.on_camera_change)
        
        # Botón refrescar cámaras
        ttk.Button(controls_frame, text="🔄 Refrescar", 
                  command=self.detect_cameras).grid(row=0, column=2, padx=5)
        
        # Resolución
        ttk.Label(controls_frame, text="Resolución:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.res_combo = ttk.Combobox(controls_frame, width=20, state='readonly',
                                       values=['640x480', '1280x720', '1920x1080', '320x240'])
        self.res_combo.set('640x480')
        self.res_combo.grid(row=1, column=1, padx=5, sticky='w')
        
        # Confianza de detección
        ttk.Label(controls_frame, text="Confianza detección:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.detection_scale = tk.Scale(controls_frame, from_=0.1, to=1.0, resolution=0.1,
                                        orient='horizontal', bg='#2b2b2b', fg='white',
                                        highlightbackground='#2b2b2b')
        self.detection_scale.set(0.5)
        self.detection_scale.grid(row=2, column=1, padx=5, sticky='w')
        
        # Confianza de tracking
        ttk.Label(controls_frame, text="Confianza tracking:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.tracking_scale = tk.Scale(controls_frame, from_=0.1, to=1.0, resolution=0.1,
                                       orient='horizontal', bg='#2b2b2b', fg='white',
                                       highlightbackground='#2b2b2b')
        self.tracking_scale.set(0.5)
        self.tracking_scale.grid(row=3, column=1, padx=5, sticky='w')
        
        # Botones de control
        buttons_frame = tk.Frame(self.root, bg='#2b2b2b')
        buttons_frame.pack(pady=10)
        
        self.start_btn = tk.Button(buttons_frame, text="▶ Iniciar Tracking", 
                                   command=self.start_tracking, bg='#4CAF50', fg='white',
                                   font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(buttons_frame, text="⏹ Detener", 
                                  command=self.stop_tracking, bg='#f44336', fg='white',
                                  font=('Arial', 12, 'bold'), padx=20, pady=10, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        # Frame de video preview
        video_frame = tk.Frame(self.root, bg='black', relief='sunken', borderwidth=2)
        video_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(fill='both', expand=True)
        
        # Estadísticas
        stats_frame = tk.Frame(self.root, bg='#1e1e1e', relief='sunken', borderwidth=2)
        stats_frame.pack(pady=5, padx=20, fill='x')
        
        self.status_label = ttk.Label(stats_frame, text="Estado: Detenido", foreground='#ff9800')
        self.status_label.pack(side='left', padx=10, pady=5)
        
        self.fps_label = ttk.Label(stats_frame, text="FPS: 0", foreground='#4CAF50')
        self.fps_label.pack(side='left', padx=10, pady=5)
        
        self.packets_label = ttk.Label(stats_frame, text="Paquetes enviados: 0", foreground='#2196F3')
        self.packets_label.pack(side='left', padx=10, pady=5)
        
        # Info de conexión
        info_frame = tk.Frame(self.root, bg='#2b2b2b')
        info_frame.pack(pady=5)
        
        ttk.Label(info_frame, text=f"📡 Enviando a: {self.host}:{self.port}").pack()
        ttk.Label(info_frame, text="💡 Selecciona Preset 32 en Blaize V3", 
                 foreground='#FFC107').pack()
        
    def detect_cameras(self):
        """Detecta todas las cámaras disponibles"""
        self.camera_combo['values'] = []
        cameras = []
        
        for i in range(10):  # Buscar hasta 10 cámaras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    # Obtener info de la cámara
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cameras.append(f"Cámara {i} ({width}x{height})")
                cap.release()
        
        if cameras:
            self.camera_combo['values'] = cameras
            self.camera_combo.current(0)
        else:
            messagebox.showerror("Error", "No se detectaron cámaras")
            
    def on_camera_change(self, event):
        """Cambiar cámara seleccionada"""
        if self.is_running:
            messagebox.showwarning("Advertencia", "Detén el tracking antes de cambiar de cámara")
            return
        
        selection = self.camera_combo.get()
        if selection:
            self.camera_index = int(selection.split()[1])
            
    def start_tracking(self):
        """Iniciar tracking"""
        if self.is_running:
            return
            
        # Obtener resolución
        res = self.res_combo.get().split('x')
        width, height = int(res[0]), int(res[1])
        
        # Abrir cámara
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara")
            return
        
        # Inicializar MediaPipe
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=self.detection_scale.get(),
            min_tracking_confidence=self.tracking_scale.get()
        )
        
        # Estado
        self.is_running = True
        self.packets_sent = 0
        self.fps_start_time = time.time()
        
        # UI
        self.start_btn['state'] = 'disabled'
        self.stop_btn['state'] = 'normal'
        self.status_label['text'] = "Estado: ▶ Tracking Activo"
        self.status_label['foreground'] = '#4CAF50'
        
        # Iniciar thread de procesamiento
        self.tracking_thread = threading.Thread(target=self.tracking_loop, daemon=True)
        self.tracking_thread.start()
        
    def stop_tracking(self):
        """Detener tracking"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
            
        if self.pose:
            self.pose.close()
            self.pose = None
        
        # UI
        self.start_btn['state'] = 'normal'
        self.stop_btn['state'] = 'disabled'
        self.status_label['text'] = "Estado: ⏹ Detenido"
        self.status_label['foreground'] = '#ff9800'
        self.video_label.configure(image='')
        
    def tracking_loop(self):
        """Loop principal de tracking"""
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Procesar con MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.pose.process(image)
            image.flags.writeable = True
            
            # Dibujar landmarks
            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
                
                # Enviar datos
                self.send_pose_data(results.pose_landmarks.landmark)
            
            # Actualizar preview
            self.update_preview(image)
            
            # Actualizar FPS
            self.update_fps()
            
        self.stop_tracking()
        
    def send_pose_data(self, landmarks):
        """Enviar datos de pose a Blaize"""
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
            
            # Actualizar UI
            self.root.after(0, lambda: self.packets_label.configure(
                text=f"Paquetes enviados: {self.packets_sent}"
            ))
            
        except Exception as e:
            print(f"Error enviando datos: {e}")
            
    def update_preview(self, image):
        """Actualizar preview de video"""
        # Redimensionar para UI (mantener aspecto)
        h, w = image.shape[:2]
        max_width = 760
        max_height = 400
        
        scale = min(max_width/w, max_height/h)
        new_w, new_h = int(w*scale), int(h*scale)
        
        image_resized = cv2.resize(image, (new_w, new_h))
        
        # Convertir a ImageTk
        image_pil = Image.fromarray(image_resized)
        image_tk = ImageTk.PhotoImage(image_pil)
        
        # Actualizar label
        self.video_label.configure(image=image_tk)
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
    app = MediaPipeTrackerGUI()
    app.run()
