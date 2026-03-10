"""
Escáner Físico QR Access Control - VERSIÓN CORREGIDA
Para usar con cámara integrada de laptop
"""

import cv2
import requests
from pyzbar.pyzbar import decode
import datetime
import os
from dotenv import load_dotenv
import time
import numpy as np

# Cargar configuración del archivo .env
load_dotenv()

# Configuración de Servidor API
API_URL = os.getenv('PANEL_URL', 'http://localhost:5000/scanner/validate')
API_KEY = os.getenv('SCANNER_API_KEY', 'default-scanner-secret-key-2026')

def validar_qr(qr_texto):
    """Valida el QR enviando una petición HTTP segura al Panel Web"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        }
        payload = {'qr_code': qr_texto}
        
        response = requests.post(API_URL, json=payload, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            resultado = "PERMITIDO" if data.get('status') == 'success' else f"DENEGADO - {data.get('message')}"
            user_name = data.get('user_name')
        else:
            # Error de autenticación o servidor
            resultado = f"ERROR HTTP {response.status_code}"
            user_name = None
            
        # Mostrar en consola
        print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] QR DETECTADO")
        print(f"  Código: {qr_texto[:30]}..." if len(qr_texto) > 30 else f"  Código: {qr_texto}")
        print(f"  Resultado: {resultado}")
        if user_name:
            print(f"  Usuario: {user_name}")
        print("-" * 50)
        
        return resultado, {'nombre': user_name}
        
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con el Servidor API: {e}")
        return "ERROR_CONEXION", None

def dibujar_rectangulo_qr(frame, qr):
    """Dibuja un rectángulo alrededor del QR detectado"""
    try:
        points = qr.polygon
        if points:
            # Convertir puntos a numpy array
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
    except Exception as e:
        # Si falla con polylines, usar rectángulo simple
        x, y, w, h = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

def main():
    print("=" * 60)
    print("   ESCÁNER QR ACCESS CONTROL - VERSIÓN LAPTOP")
    print("=" * 60)
    print("🔍 Buscando cámara...")
    
    # Probar diferentes índices de cámara
    cap = None
    for i in range(3):
        print(f"  Probando cámara {i}...")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"  ✅ Cámara {i} conectada correctamente")
            break
        cap.release()
        cap = None
    
    if not cap:
        print("❌ No se pudo conectar a ninguna cámara")
        print("   Verifica que la cámara esté conectada y no esté siendo usada por otra aplicación")
        return
    
    # Configurar resolución
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("\n📷 Cámara lista. Acerca un código QR para escanear.")
    print("   Presiona 'q' para salir, 's' para guardar captura")
    print("-" * 60)
    
    ultimo_qr = ""
    tiempo_ultimo = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al leer de la cámara")
            break
        
        # Decodificar QR en el frame
        qr_codes = decode(frame)
        
        for qr in qr_codes:
            qr_text = qr.data.decode('utf-8')
            
            # Dibujar rectángulo alrededor del QR usando función segura
            dibujar_rectangulo_qr(frame, qr)
            
            # Mostrar texto del QR
            x, y, w, h = qr.rect
            cv2.putText(frame, qr_text[:20], (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Validar QR (evitar validar el mismo QR repetidamente)
            tiempo_actual = time.time()
            if qr_text != ultimo_qr or (tiempo_actual - tiempo_ultimo) > 5:
                resultado, user = validar_qr(qr_text)
                ultimo_qr = qr_text
                tiempo_ultimo = tiempo_actual
        
        # Mostrar instrucciones en pantalla
        cv2.putText(frame, "q: salir | s: capturar", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Mostrar video
        cv2.imshow('QR Scanner - Laptop (Presiona q para salir)', frame)
        
        # Teclas de control
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Guardar captura
            filename = f"captura_qr_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(filename, frame)
            print(f"📸 Captura guardada como {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n👋 Escáner detenido")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Escáner detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()