"""
MediaPipe Tracker GUI Simplificado - Compatible con versiones nuevas
Usa la versión anterior del tracker con GUI básica
"""
import cv2
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys

class SimpleTrackerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MediaPipe Tracker Control - Blaize V3")
        self.root.geometry("500x600")
        self.root.configure(bg='#2b2b2b')
        
        self.process = None
        
        self.setup_gui()
        
    def setup_gui(self):
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        
        # Título
        title = ttk.Label(self.root, text="🎥 MediaPipe Tracker", style='Title.TLabel')
        title.pack(pady=20)
        
        # Subtítulo
        subtitle = ttk.Label(self.root, text="Control para Blaize V3 - Preset 32", 
                            foreground='#FFC107')
        subtitle.pack(pady=5)
        
        # Frame de controles
        controls_frame = tk.Frame(self.root, bg='#3b3b3b', relief='raised', borderwidth=2)
        controls_frame.pack(pady=20, padx=30, fill='both', expand=True)
        
        # Selección de cámara
        ttk.Label(controls_frame, text="Selecciona el índice de tu cámara:").pack(pady=(20,5))
        
        camera_frame = tk.Frame(controls_frame, bg='#3b3b3b')
        camera_frame.pack(pady=5)
        
        ttk.Label(camera_frame, text="Índice de cámara (0, 1, 2...):").pack(side='left', padx=5)
        self.camera_spinbox = tk.Spinbox(camera_frame, from_=0, to=5, width=10, 
                                         font=('Arial', 12), bg='white')
        self.camera_spinbox.pack(side='left', padx=5)
        
        # Info sobre cámaras
        info_text = tk.Label(controls_frame, 
                            text="💡 Normalmente: 0 = webcam integrada, 1 = externa",
                            bg='#3b3b3b', fg='#FFC107', font=('Arial', 9))
        info_text.pack(pady=5)
        
        # Separador
        ttk.Separator(controls_frame, orient='horizontal').pack(fill='x', pady=20, padx=20)
        
        # Botones principales
        self.start_btn = tk.Button(controls_frame, text="▶ INICIAR TRACKING", 
                                   command=self.start_tracking, bg='#4CAF50', fg='white',
                                   font=('Arial', 14, 'bold'), padx=30, pady=15,
                                   cursor='hand2')
        self.start_btn.pack(pady=10)
        
        self.stop_btn = tk.Button(controls_frame, text="⏹ DETENER", 
                                  command=self.stop_tracking, bg='#f44336', fg='white',
                                  font=('Arial', 14, 'bold'), padx=30, pady=15,
                                  state='disabled', cursor='hand2')
        self.stop_btn.pack(pady=10)
        
        # Separador
        ttk.Separator(controls_frame, orient='horizontal').pack(fill='x', pady=20, padx=20)
        
        # Estado
        self.status_label = ttk.Label(controls_frame, text="Estado: Detenido", 
                                      foreground='#ff9800', font=('Arial', 11, 'bold'))
        self.status_label.pack(pady=10)
        
        # Info
        info_frame = tk.Frame(self.root, bg='#1e1e1e', relief='sunken', borderwidth=2)
        info_frame.pack(pady=10, padx=30, fill='x')
        
        ttk.Label(info_frame, text="📡 Puerto UDP: 12346", 
                 foreground='#2196F3').pack(pady=5)
        ttk.Label(info_frame, text="💡 Asegúrate de seleccionar Preset 32 en Blaize", 
                 foreground='#FFC107').pack(pady=5)
        
        # Instrucciones
        instructions = tk.Text(self.root, height=6, width=50, bg='#2b2b2b', fg='white',
                              font=('Arial', 9), relief='flat', wrap='word')
        instructions.pack(pady=10, padx=30)
        instructions.insert('1.0', """
📌 INSTRUCCIONES:
1. Abre Blaize V3 en Processing
2. Selecciona el Preset 32
3. Elige tu cámara arriba
4. Click en "INICIAR TRACKING"
5. Una ventana mostrará tu pose detectada
6. Los spots seguirán tus movimientos
        """)
        instructions.config(state='disabled')
        
    def detect_cameras(self):
        """Detecta cámaras disponibles"""
        self.cameras = []
        cameras_list = []
        
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cameras_list.append(f"Cámara {i} ({width}x{height})")
                    self.cameras.append(i)
                cap.release()
        
        if cameras_list:
            self.camera_combo['values'] = cameras_list
            self.camera_combo.current(0)
        else:
            messagebox.showerror("Error", "No se detectaron cámaras.\nVerifica que tu webcam esté conectada.")
            
    def start_tracking(self):
        """Iniciar tracking en ventana separada"""
        if self.process and self.process.poll() is None:
            messagebox.showwarning("Advertencia", "El tracking ya está activo")
            return
        
        try:
            camera_index = int(self.camera_spinbox.get())
        except ValueError:
            messagebox.showerror("Error", "Índice de cámara inválido")
            return
        
        # Iniciar el tracker original en proceso separado
        try:
            self.process = subprocess.Popen(
                [sys.executable, 'mediapipe_tracker.py', str(camera_index)],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            # Actualizar UI
            self.start_btn['state'] = 'disabled'
            self.stop_btn['state'] = 'normal'
            self.status_label['text'] = "Estado: ▶ TRACKING ACTIVO"
            self.status_label['foreground'] = '#4CAF50'
            
            # Monitorear proceso
            self.monitor_thread = threading.Thread(target=self.monitor_process, daemon=True)
            self.monitor_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el tracking:\n{e}")
            
    def monitor_process(self):
        """Monitorear si el proceso sigue activo"""
        while self.process and self.process.poll() is None:
            time.sleep(1)
        
        # Proceso terminado
        self.root.after(0, self.on_process_ended)
        
    def on_process_ended(self):
        """Proceso terminó"""
        self.start_btn['state'] = 'normal'
        self.stop_btn['state'] = 'disabled'
        self.status_label['text'] = "Estado: ⏹ Detenido"
        self.status_label['foreground'] = '#ff9800'
        
    def stop_tracking(self):
        """Detener tracking"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except:
                self.process.kill()
        
        self.process = None
        self.on_process_ended()
        
    def run(self):
        """Ejecutar aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Cerrar aplicación"""
        self.stop_tracking()
        self.root.destroy()

if __name__ == "__main__":
    import time
    app = SimpleTrackerGUI()
    app.run()
