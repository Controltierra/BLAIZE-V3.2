"""
Test simple para verificar envío de datos desde MediaPipe a Processing
Este script envía datos de prueba para verificar la conexión
"""
import socket
import json
import time

def test_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = 'localhost'
    port = 12346
    
    print(f"Enviando datos de prueba a {host}:{port}")
    print("Presiona Ctrl+C para detener")
    
    try:
        while True:
            # Datos de prueba que simulan movimiento
            t = time.time()
            
            test_data = {
                'nose': {'x': int(485 + 200 * abs(0.5 - (t % 2) / 2)), 'y': 300},
                'left_wrist': {'x': 200, 'y': 500},
                'right_wrist': {'x': 770, 'y': 500},
                'left_shoulder': {'x': 350, 'y': 400},
                'right_shoulder': {'x': 620, 'y': 400}
            }
            
            data = json.dumps(test_data)
            sock.sendto(data.encode(), (host, port))
            
            print(f"Enviado: Nose X={test_data['nose']['x']}", end='\r')
            time.sleep(0.033)  # ~30 FPS
            
    except KeyboardInterrupt:
        print("\n\nTest detenido")
    finally:
        sock.close()

if __name__ == "__main__":
    test_connection()
