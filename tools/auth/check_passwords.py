#!/usr/bin/env python3
"""
Verificar contraseñas y mostrar resumen
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from web_panel.models.user import User
from werkzeug.security import check_password_hash

def check_all():
    print("=" * 70)
    print("🔍 VERIFICACIÓN FINAL DE CONTRASEÑAS")
    print("=" * 70)
    
    password = "hola123"
    usuarios = User.get_all()
    
    print(f"\n📊 TOTAL DE USUARIOS: {len(usuarios)}")
    print("-" * 70)
    
    correctas = 0
    incorrectas = 0
    
    for user in usuarios:
        if user.check_password(password):
            print(f"✅ ID {user.id:3} | {user.correo:30} | {user.nombre:15} | Rol: {user.rol:8} | OK")
            correctas += 1
        else:
            print(f"❌ ID {user.id:3} | {user.correo:30} | {user.nombre:15} | Rol: {user.rol:8} | FALLÓ")
            incorrectas += 1
    
    print("-" * 70)
    print(f"✅ Correctas: {correctas}")
    print(f"❌ Incorrectas: {incorrectas}")
    
    if incorrectas == 0:
        print("\n🎉 ¡TODAS LAS CONTRASEÑAS FUNCIONAN!")
        print("   Ahora puedes hacer login con 'hola123' para todos los usuarios")
    else:
        print("\n⚠️  Aún hay usuarios con problemas")

if __name__ == "__main__":
    check_all()
