#!/usr/bin/env python3
"""
Script para cambiar TODAS las contraseñas a "hola123"
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash

def cambiar_todas_passwords():
    print("=" * 60)
    print("🔑 CAMBIANDO TODAS LAS CONTRASEÑAS A 'hola123'")
    print("=" * 60)
    
    nueva_password = "hola123"
    nueva_hash = generate_password_hash(nueva_password)
    
    with db.get_cursor(dictionary=True) as cursor:
        # 1. Ver usuarios antes
        cursor.execute("SELECT id, nombre, correo, rol FROM usuarios ORDER BY id")
        usuarios = cursor.fetchall()
        
        print("\n📋 USUARIOS ANTES DEL CAMBIO:")
        print("-" * 60)
        for u in usuarios:
            print(f"ID: {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:10} | {u['nombre']}")
        
        # 2. Cambiar todas las contraseñas
        cursor.execute("UPDATE usuarios SET password_hash = %s", (nueva_hash,))
        actualizados = cursor.rowcount
        
        print(f"\n✅ Contraseñas actualizadas: {actualizados} usuarios")
        print(f"   Nueva contraseña: '{nueva_password}'")
        print(f"   Hash: {nueva_hash}")
        
        # 3. Verificar que se actualizaron
        cursor.execute("SELECT id, nombre, correo, rol FROM usuarios ORDER BY id")
        usuarios_despues = cursor.fetchall()
        
        print("\n📋 USUARIOS DESPUÉS DEL CAMBIO:")
        print("-" * 60)
        for u in usuarios_despues:
            print(f"ID: {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:10} | {u['nombre']}")
        
        # 4. Probar que la contraseña funciona para cada usuario
        print("\n🔍 VERIFICANDO CONTRASEÑA PARA CADA USUARIO:")
        print("-" * 60)
        
        for u in usuarios_despues:
            cursor.execute("SELECT password_hash FROM usuarios WHERE id = %s", (u['id'],))
            hash_actual = cursor.fetchone()['password_hash']
            
            if check_password_hash(hash_actual, nueva_password):
                print(f"✅ ID {u['id']}: {u['correo']} - Contraseña CORRECTA")
            else:
                print(f"❌ ID {u['id']}: {u['correo']} - ERROR en contraseña")

if __name__ == "__main__":
    cambiar_todas_passwords()
