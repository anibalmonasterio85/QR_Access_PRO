#!/usr/bin/env python3
"""
Verificar que todos los usuarios tienen contraseña "hola123"
Versión corregida para Python 3.13
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import db
from werkzeug.security import check_password_hash, generate_password_hash

def verificar_passwords():
    print("=" * 60)
    print("🔍 VERIFICANDO CONTRASEÑAS")
    print("=" * 60)

    password_prueba = "hola123"
    
    # Generar un hash de ejemplo para verificar el método
    hash_ejemplo = generate_password_hash(password_prueba, method='pbkdf2:sha256')
    print(f"Hash de ejemplo generado: {hash_ejemplo[:50]}...")

    with db.get_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id, nombre, correo, rol, password_hash FROM usuarios ORDER BY id")
        usuarios = cursor.fetchall()

        print(f"\nProbando contraseña: '{password_prueba}'")
        print("-" * 80)

        todos_ok = True
        for u in usuarios:
            try:
                if check_password_hash(u['password_hash'], password_prueba):
                    print(f"✅ ID {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:8} | OK")
                else:
                    print(f"❌ ID {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:8} | ERROR - Contraseña incorrecta")
                    todos_ok = False
            except Exception as e:
                print(f"⚠️ ID {u['id']:3} | {u['correo']:30} | ERROR al verificar: {e}")
                todos_ok = False

        print("-" * 80)
        if todos_ok:
            print("🎉 TODOS los usuarios tienen la contraseña 'hola123'")
        else:
            print("⚠️  Algunos usuarios NO tienen la contraseña correcta")

if __name__ == "__main__":
    verificar_passwords()
