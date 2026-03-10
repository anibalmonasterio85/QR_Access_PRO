#!/usr/bin/env python3
"""
Script para resetear TODAS las contraseñas a "hola123"
Versión corregida para Python 3.13
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash

def resetear_todas_passwords():
    print("=" * 60)
    print("🔄 RESETEANDO TODAS LAS CONTRASEÑAS A 'hola123'")
    print("=" * 60)
    
    nueva_password = "hola123"
    # Usar método pbkdf2:sha256 explícitamente para compatibilidad
    nueva_hash = generate_password_hash(nueva_password, method='pbkdf2:sha256')
    
    print(f"Hash generado: {nueva_hash}")
    print(f"Longitud del hash: {len(nueva_hash)}")
    
    with db.get_cursor(dictionary=True) as cursor:
        # Ver usuarios antes
        cursor.execute("SELECT id, nombre, correo, rol FROM usuarios ORDER BY id")
        usuarios_antes = cursor.fetchall()
        
        print("\n📋 USUARIOS ANTES DEL CAMBIO:")
        print("-" * 80)
        for u in usuarios_antes:
            print(f"ID: {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:8} | {u['nombre']}")
        
        # Actualizar todas las contraseñas
        cursor.execute("UPDATE usuarios SET password_hash = %s", (nueva_hash,))
        actualizados = cursor.rowcount
        
        print(f"\n✅ Contraseñas actualizadas: {actualizados} usuarios")
        
        # Verificar que se actualizaron
        cursor.execute("SELECT id, nombre, correo, rol, password_hash FROM usuarios ORDER BY id")
        usuarios_despues = cursor.fetchall()
        
        print("\n📋 VERIFICANDO CONTRASEÑAS ACTUALIZADAS:")
        print("-" * 80)
        
        todos_ok = True
        for u in usuarios_despues:
            if check_password_hash(u['password_hash'], nueva_password):
                print(f"✅ ID {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:8} | OK")
            else:
                print(f"❌ ID {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:8} | ERROR")
                todos_ok = False
        
        print("-" * 80)
        if todos_ok:
            print("🎉 TODAS LAS CONTRASEÑAS SON 'hola123'")
        else:
            print("⚠️  HUBO ERRORES EN ALGUNAS CONTRASEÑAS")

if __name__ == "__main__":
    resetear_todas_passwords()
