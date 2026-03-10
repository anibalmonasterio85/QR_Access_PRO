"""
web_panel/utils/security.py - Utilidades de Seguridad Empresarial
"""
import pyotp
import qrcode
import io
from flask import request, jsonify, current_app
from functools import wraps
from config.settings import config
import os

def generate_2fa_secret():
    """Genera un nuevo secreto TOTP puro."""
    return pyotp.random_base32()

def generate_2fa_qr(secret, email):
    """Genera la imagen URI en base64 para que el usuario escanee con Google Authenticator."""
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(name=email, issuer_name=config.SYSTEM_NAME)
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    import base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def verify_2fa_token(secret, token):
    """Verifica si el token ingresado es válido en la ventana de tiempo."""
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

def require_api_key(f):
    """
    Decorador para proteger endpoints que no usan sesion web normal 
    (Ej: el escaner de la raspberry).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        # Leer de entorno (por defecto un valor de test si no esta)
        expected_key = os.environ.get('SCANNER_API_KEY', 'default-scanner-secret-key-2026')
        
        if not api_key or api_key != expected_key:
            return jsonify({
                "status": "error",
                "message": "Acceso Denegado. API Key Inválida o faltante en cabecera 'X-API-Key'."
            }), 403
            
        return f(*args, **kwargs)
    return decorated_function
