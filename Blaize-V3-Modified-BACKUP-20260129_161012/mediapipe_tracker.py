"""
MediaPipe Pose Tracker for Blaize V3
Detects body pose and sends coordinates to Processing via socket
"""
import cv2
import mediapipe as mp
import socket
import json
import time

class PoseTracker:
    def __init__(self, camera_index=0, host='localhost', port=12346):
        # MediaPipe setup
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Socket setup para comunicación con Processing
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        
        # Camera setup
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Target dimensions (ajusta según tu pantalla)
        self.target_width = 970  # frameSizeX from Processing
        self.target_height = 1000  # frameSizeY from Processing
        
    def run(self):
        print(f"MediaPipe Tracker iniciado. Enviando datos a {self.host}:{self.port}")
        print("Presiona 'q' para salir")
        
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                print("Error al capturar frame")
                continue
            
            # Convertir a RGB para MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Procesar pose
            results = self.pose.process(image)
            
            # Convertir de vuelta a BGR para visualización
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.pose_landmarks:
                # Dibujar landmarks en la visualización
                self.mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
                
                # Extraer coordenadas clave y enviar a Processing
                landmarks = results.pose_landmarks.landmark
                
                # Puntos de interés (formato compatible con Processing)
                points = {
                    'nose': {'x': self._get_scaled_coords(landmarks[0])[0], 'y': self._get_scaled_coords(landmarks[0])[1]},
                    'left_wrist': {'x': self._get_scaled_coords(landmarks[15])[0], 'y': self._get_scaled_coords(landmarks[15])[1]},
                    'right_wrist': {'x': self._get_scaled_coords(landmarks[16])[0], 'y': self._get_scaled_coords(landmarks[16])[1]},
                    'left_shoulder': {'x': self._get_scaled_coords(landmarks[11])[0], 'y': self._get_scaled_coords(landmarks[11])[1]},
                    'right_shoulder': {'x': self._get_scaled_coords(landmarks[12])[0], 'y': self._get_scaled_coords(landmarks[12])[1]},
                    'left_hip': {'x': self._get_scaled_coords(landmarks[23])[0], 'y': self._get_scaled_coords(landmarks[23])[1]},
                    'right_hip': {'x': self._get_scaled_coords(landmarks[24])[0], 'y': self._get_scaled_coords(landmarks[24])[1]}
                }
                
                # Enviar datos via socket
                self._send_data(points)
                
                # Mostrar coordenadas en pantalla
                cv2.putText(image, f"Nose: ({points['nose']['x']}, {points['nose']['y']})", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # Mostrar preview
            cv2.imshow('MediaPipe Pose Tracker', image)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        
        self.cleanup()
    
    def _get_scaled_coords(self, landmark):
        """Convierte coordenadas normalizadas (0-1) a coordenadas de pantalla"""
        x = int(landmark.x * self.target_width)
        y = int(landmark.y * self.target_height)
        return (x, y)
    
    def _send_data(self, points):
        """Envía datos via UDP socket a Processing"""
        try:
            data = json.dumps(points)
            self.sock.sendto(data.encode(), (self.host, self.port))
        except Exception as e:
            print(f"Error enviando datos: {e}")
    
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.sock.close()

if __name__ == "__main__":
    import sys
    
    # Obtener índice de cámara desde argumentos o usar default 0
    camera_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    print(f"Usando cámara {camera_index}")
    tracker = PoseTracker(camera_index=camera_index)
    tracker.run()
