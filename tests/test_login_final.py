#!/usr/bin/env python3
"""
Probar login para todos los usuarios
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from web_panel.models.user import User
from werkzeug.security import check_password_hash

def test_logins():
    print("=" * 60)
    print("🔐 PROBANDO LOGIN PARA TODOS LOS USUARIOS")
    print("=" * 60)
    
    password = "hola123"
    
    usuarios = User.get_all()
    
    print(f"\nProbando contraseña: '{password}'")
    print("-" * 80)
    
    for user in usuarios:
        try:
            if user.check_password(password):
                print(f"✅ {user.correo:30} | {user.nombre:20} | Rol: {user.rol:8} | LOGIN OK")
            else:
                print(f"❌ {user.correo:30} | {user.nombre:20} | Rol: {user.rol:8} | LOGIN FALLÓ")
                
                # Mostrar el hash para depuración
                print(f"   Hash: {user.password_hash[:50]}...")
        except Exception as e:
            print(f"⚠️ {user.correo:30} | ERROR: {e}")

if __name__ == "__main__":
    test_logins()
