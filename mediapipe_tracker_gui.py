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
        self.is_previewing = False
        self.camera_index = 0
        self.selected_resolution = "640x480"  # Resolución seleccionada desde el combo
        self.target_width = 970
        self.target_height = 1000
        
        # Configuración de seguimiento
        self.tracking_point = 'nose'  # Punto a seguir: nose, left_wrist, right_wrist, left_shoulder, right_shoulder
        self.draw_detail = 'full'  # Nivel de detalle: none, point, skeleton, full
        
        # ROI (Region of Interest) - Zona efectiva de seguimiento
        self.roi_enabled = False
        self.roi_x1 = 0
        self.roi_y1 = 0
        self.roi_x2 = 0
        self.roi_y2 = 0
        self.roi_selecting = False
        self.roi_start_x = 0
        self.roi_start_y = 0
        self.roi_current_x = 0  # Posición actual del mouse mientras arrastra
        self.roi_current_y = 0
        
        # Suavizado de movimiento (para evitar cambios bruscos)
        self.smoothing_factor = 0.3  # 0 = sin suavizado, 1 = máximo suavizado
        self.prev_nose_x = 0
        self.prev_nose_y = 0
        self.prev_left_wrist_x = 0
        self.prev_left_wrist_y = 0
        self.prev_right_wrist_x = 0
        self.prev_right_wrist_y = 0
        
        # Estadísticas
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        self.packets_sent = 0
        
        # Thread de preview
        self.preview_thread = None
        
        self.setup_gui()
        self.detect_cameras()
        
    def setup_gui(self):
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Section.TLabel', font=('Arial', 11, 'bold'), background='#3b3b3b')
        
        # Título principal
        header_frame = tk.Frame(self.root, bg='#1e1e1e', relief='raised', borderwidth=1)
        header_frame.pack(fill='x', padx=5, pady=(5, 0))
        
        title = ttk.Label(header_frame, text="🎥 MediaPipe Tracker - Blaize V3", style='Title.TLabel')
        title.pack(pady=5)
        
        ttk.Label(header_frame, text="⚡ PRESET 15 o 32", 
                 foreground='#4CAF50', font=('Arial', 9, 'bold')).pack(pady=(0, 5))
        
        # Contenedor para controles (no se expande)
        controls_container = tk.Frame(self.root, bg='#2b2b2b')
        controls_container.pack(fill='x', padx=5, pady=(3, 0))
        
        # Notebook con pestañas
        notebook = ttk.Notebook(controls_container)
        notebook.pack(fill='x', pady=0)
        
        # ===== PESTAÑA 1: CONFIGURACIÓN =====
        config_tab = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(config_tab, text='⚙️ Configuración')
        
        # Sección Cámara
        camera_section = tk.LabelFrame(config_tab, text="📹 Cámara", 
                                      bg='#3b3b3b', fg='white', font=('Arial', 9, 'bold'),
                                      relief='raised', borderwidth=1)
        camera_section.pack(fill='x', padx=5, pady=5)
        
        cam_grid = tk.Frame(camera_section, bg='#3b3b3b')
        cam_grid.pack(fill='x', padx=8, pady=6)
        
        ttk.Label(cam_grid, text="Dispositivo:", background='#3b3b3b').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.camera_combo = ttk.Combobox(cam_grid, width=45, state='readonly')
        self.camera_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew', columnspan=2)
        self.camera_combo.bind('<<ComboboxSelected>>', self.on_camera_change)
        
        ttk.Button(cam_grid, text="🔄", command=self.detect_cameras, width=3).grid(row=0, column=3, padx=5)
        
        cam_grid.columnconfigure(1, weight=1)
        
        # Sección MediaPipe
        mediapipe_section = tk.LabelFrame(config_tab, text="🤖 MediaPipe Settings", 
                                         bg='#3b3b3b', fg='white', font=('Arial', 9, 'bold'),
                                         relief='raised', borderwidth=1)
        mediapipe_section.pack(fill='x', padx=5, pady=5)
        
        mp_grid = tk.Frame(mediapipe_section, bg='#3b3b3b')
        mp_grid.pack(fill='x', padx=8, pady=6)
        
        # Punto de seguimiento
        ttk.Label(mp_grid, text="Seguir:", background='#3b3b3b').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.tracking_point_combo = ttk.Combobox(mp_grid, width=18, state='readonly',
                                                 values=[
                                                     '👃 Nariz (cabeza)',
                                                     '✋ Mano Izquierda',
                                                     '🤚 Mano Derecha',
                                                     '👆 Hombro Izquierdo',
                                                     '👆 Hombro Derecho',
                                                     '🦵 Cadera Centro'
                                                 ])
        self.tracking_point_combo.set('👃 Nariz (cabeza)')
        self.tracking_point_combo.bind('<<ComboboxSelected>>', self.on_tracking_point_change)
        self.tracking_point_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Nivel de visualización
        ttk.Label(mp_grid, text="Dibujar:", background='#3b3b3b').grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.draw_detail_combo = ttk.Combobox(mp_grid, width=15, state='readonly',
                                              values=[
                                                  '❌ Nada',
                                                  '🔵 Solo Punto',
                                                  '🦴 Esqueleto',
                                                  '⭐ Completo'
                                              ])
        self.draw_detail_combo.set('⭐ Completo')
        self.draw_detail_combo.bind('<<ComboboxSelected>>', self.on_draw_detail_change)
        self.draw_detail_combo.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        ttk.Label(mp_grid, text="Confianza Detección:", background='#3b3b3b').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.detection_scale = tk.Scale(mp_grid, from_=0.1, to=1.0, resolution=0.1,
                                       orient='horizontal', bg='#3b3b3b', fg='white',
                                       highlightbackground='#3b3b3b', length=150)
        self.detection_scale.set(0.5)
        self.detection_scale.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(mp_grid, text="50%", background='#3b3b3b', foreground='#FFC107').grid(row=1, column=2, padx=5)
        
        ttk.Label(mp_grid, text="Confianza Tracking:", background='#3b3b3b').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.tracking_scale = tk.Scale(mp_grid, from_=0.1, to=1.0, resolution=0.1,
                                      orient='horizontal', bg='#3b3b3b', fg='white',
                                      highlightbackground='#3b3b3b', length=150)
        self.tracking_scale.set(0.5)
        self.tracking_scale.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(mp_grid, text="50%", background='#3b3b3b', foreground='#FFC107').grid(row=2, column=2, padx=5)
        
        mp_grid.columnconfigure(1, weight=1)
        
        # ===== PESTAÑA 2: ROI Y SUAVIZADO =====
        advanced_tab = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(advanced_tab, text='🎯 ROI & Suavizado')
        
        # Sección ROI
        roi_section = tk.LabelFrame(advanced_tab, text="🎯 Zona de Seguimiento (ROI)", 
                                   bg='#3b3b3b', fg='white', font=('Arial', 9, 'bold'),
                                   relief='raised', borderwidth=1)
        roi_section.pack(fill='x', padx=5, pady=5)
        
        roi_content = tk.Frame(roi_section, bg='#3b3b3b')
        roi_content.pack(fill='x', padx=8, pady=6)
        
        roi_buttons = tk.Frame(roi_content, bg='#3b3b3b')
        roi_buttons.pack(pady=5)
        
        self.roi_select_btn = tk.Button(roi_buttons, text="📐 Seleccionar Área", 
                                        command=self.start_roi_selection, bg='#FF9800', fg='white',
                                        font=('Arial', 10, 'bold'), padx=15, pady=8)
        self.roi_select_btn.pack(side='left', padx=5)
        
        self.roi_clear_btn = tk.Button(roi_buttons, text="🗑️ Limpiar", 
                                       command=self.clear_roi, bg='#f44336', fg='white',
                                       font=('Arial', 10, 'bold'), padx=15, pady=8)
        self.roi_clear_btn.pack(side='left', padx=5)
        
        self.roi_status_label = ttk.Label(roi_content, text="Estado: Desactivado", 
                                         foreground='#888888', background='#3b3b3b',
                                         font=('Arial', 9))
        self.roi_status_label.pack(pady=5)
        
        ttk.Label(roi_content, text="💡 Click y arrastra en el video para delimitar", 
                 foreground='#FFC107', font=('Arial', 8), background='#3b3b3b').pack(pady=2)
        
        # Sección Suavizado
        smooth_section = tk.LabelFrame(advanced_tab, text="🎚️ Suavizado de Movimiento", 
                                      bg='#3b3b3b', fg='white', font=('Arial', 9, 'bold'),
                                      relief='raised', borderwidth=1)
        smooth_section.pack(fill='x', padx=5, pady=5)
        
        smooth_content = tk.Frame(smooth_section, bg='#3b3b3b')
        smooth_content.pack(fill='x', padx=8, pady=6)
        
        smooth_labels = tk.Frame(smooth_content, bg='#3b3b3b')
        smooth_labels.pack(fill='x', pady=5)
        
        ttk.Label(smooth_labels, text="Más Preciso", 
                 foreground='#FF5722', font=('Arial', 8), background='#3b3b3b').pack(side='left')
        
        self.smoothing_value_label = ttk.Label(smooth_labels, text="Nivel: 30%", 
                                              foreground='#FFC107', background='#3b3b3b',
                                              font=('Arial', 9, 'bold'))
        self.smoothing_value_label.pack(side='left', expand=True)
        
        ttk.Label(smooth_labels, text="Más Suave", 
                 foreground='#4CAF50', font=('Arial', 8), background='#3b3b3b').pack(side='right')
        
        self.smoothing_scale = tk.Scale(smooth_content, from_=0.0, to=0.9, resolution=0.05,
                                       orient='horizontal', bg='#3b3b3b', fg='white',
                                       highlightbackground='#3b3b3b', length=400,
                                       command=self.on_smoothing_change)
        self.smoothing_scale.set(0.3)
        self.smoothing_scale.pack(fill='x', pady=5)
        
        ttk.Label(smooth_content, text="💡 Reduce movimientos bruscos", 
                 foreground='#888888', font=('Arial', 8), background='#3b3b3b').pack(pady=5)
        
        # Botones de control principales (dentro del contenedor de controles)
        buttons_frame = tk.Frame(controls_container, bg='#2b2b2b')
        buttons_frame.pack(pady=5)
        
        self.preview_btn = tk.Button(buttons_frame, text="🎥 Preview", 
                                     command=self.toggle_preview, bg='#2196F3', fg='white',
                                     font=('Arial', 10, 'bold'), padx=15, pady=6)
        self.preview_btn.pack(side='left', padx=3)
        
        self.start_btn = tk.Button(buttons_frame, text="▶ Iniciar", 
                                   command=self.start_tracking, bg='#4CAF50', fg='white',
                                   font=('Arial', 10, 'bold'), padx=15, pady=6)
        self.start_btn.pack(side='left', padx=3)
        
        self.stop_btn = tk.Button(buttons_frame, text="⏹ Detener", 
                                  command=self.stop_tracking, bg='#f44336', fg='white',
                                  font=('Arial', 10, 'bold'), padx=15, pady=6, state='disabled')
        self.stop_btn.pack(side='left', padx=3)
        
        # Frame de video preview
        video_frame = tk.Frame(self.root, bg='black', relief='sunken', borderwidth=1)
        video_frame.pack(pady=(5, 2), padx=5, fill='both', expand=True)
        
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(fill='both', expand=True)
        
        # Eventos del mouse para selección de ROI
        self.video_label.bind('<Button-1>', self.on_video_click)
        self.video_label.bind('<B1-Motion>', self.on_video_drag)
        self.video_label.bind('<ButtonRelease-1>', self.on_video_release)
        
        # Estadísticas
        stats_frame = tk.Frame(self.root, bg='#1e1e1e', relief='sunken', borderwidth=1)
        stats_frame.pack(pady=(2, 5), padx=5, fill='x')
        
        self.status_label = ttk.Label(stats_frame, text="⏸ Detenido", foreground='#ff9800', font=('Arial', 8))
        self.status_label.pack(side='left', padx=8, pady=3)
        
        self.fps_label = ttk.Label(stats_frame, text="FPS: 0", foreground='#4CAF50', font=('Arial', 8))
        self.fps_label.pack(side='left', padx=8, pady=3)
        
        self.packets_label = ttk.Label(stats_frame, text="Enviados: 0", foreground='#2196F3', font=('Arial', 8))
        self.packets_label.pack(side='left', padx=8, pady=3)
        
        ttk.Label(stats_frame, text=f"📡 {self.host}:{self.port}", foreground='#888888', font=('Arial', 8)).pack(side='right', padx=8)
        
        ... (rest of file content continues)