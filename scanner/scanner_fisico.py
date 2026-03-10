"""
Escáner Físico QR Access Control - VERSIÓN CORREGIDA
Para usar con cámara integrada de laptop
"""

import cv2
import mysql.connector
from pyzbar.pyzbar import decode
import datetime
import os
from dotenv import load_dotenv
import time
import numpy as np

# Cargar configuración del archivo .env
load_dotenv()

# Configuración de base de datos
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'flaskuser'),
    'password': os.getenv('DB_PASS', 'flask123'),
    'database': os.getenv('DB_NAME', 'qr_access')
}

def validar_qr(qr_texto):
    """Valida el QR contra la base de datos y registra el acceso"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Buscar usuario por qr_code
        cursor.execute("""
            SELECT id, nombre, empresa_id, activo, fecha_expiracion 
            FROM usuarios 
            WHERE qr_code = %s
        """, (qr_texto,))
        
        user = cursor.fetchone()
        
        # Determinar resultado
        if not user:
            resultado = "DENEGADO - QR no registrado"
            user_id = None
        elif not user['activo']:
            resultado = "DENEGADO - Usuario inactivo"
            user_id = user['id']
        elif user['fecha_expiracion'] and user['fecha_expiracion'] < datetime.datetime.now():
            resultado = "DENEGADO - QR expirado"
            user_id = user['id']
        else:
            resultado = "PERMITIDO"
            user_id = user['id']
            
        # Registrar en accesos_log
        cursor.execute("""
            INSERT INTO accesos_log (qr_texto, resultado, user_id, fecha_hora)
            VALUES (%s, %s, %s, %s)
        """, (qr_texto, resultado, user_id, datetime.datetime.now()))
        conn.commit()
        
        # Mostrar en consola
        print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] QR DETECTADO")
        print(f"  Código: {qr_texto[:30]}..." if len(qr_texto) > 30 else f"  Código: {qr_texto}")
        print(f"  Resultado: {resultado}")
        if user:
            print(f"  Usuario: {user['nombre']}")
        print("-" * 50)
        
        cursor.close()
        conn.close()
        return resultado, user
        
    except Exception as e:
        print(f"Error al validar QR: {e}")
        return "ERROR", None

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