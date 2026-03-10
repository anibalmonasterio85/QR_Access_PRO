#!/usr/bin/env python3
"""
Script FINAL para arreglar todas las contraseñas
Este SÍ funciona - genera hash correcto para cada usuario
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash

def fix_all_passwords():
    print("=" * 70)
    print("🔧 ARREGLANDO CONTRASEÑAS - VERSIÓN FINAL QUE FUNCIONA")
    print("=" * 70)
    
    nueva_password = "hola123"
    
    with db.get_cursor(dictionary=True) as cursor:
        # Obtener todos los usuarios
        cursor.execute("SELECT id, nombre, correo FROM usuarios")
        usuarios = cursor.fetchall()
        
        print(f"\n📋 Procesando {len(usuarios)} usuarios...")
        
        # Actualizar cada usuario con su PROPIO hash (todos igual pero generado correctamente)
        for user in usuarios:
            # Generar hash NUEVO para cada usuario (aunque sea la misma password)
            nuevo_hash = generate_password_hash(nueva_password, method='pbkdf2:sha256')
            
            # Actualizar
            cursor.execute(
                "UPDATE usuarios SET password_hash = %s WHERE id = %s",
                (nuevo_hash, user['id'])
            )
            
            print(f"✅ ID {user['id']:3} | {user['correo']:30} | Hash actualizado")
        
        print("\n🔍 VERIFICANDO CONTRASEÑAS ACTUALIZADAS:")
        print("-" * 70)
        
        # Verificar cada usuario
        cursor.execute("SELECT id, correo, password_hash FROM usuarios")
        verificados = cursor.fetchall()
        
        todos_ok = True
        for user in verificados:
            if check_password_hash(user['password_hash'], nueva_password):
                print(f"✅ ID {user['id']:3} | {user['correo']:30} | CONTRASEÑA CORRECTA")
            else:
                print(f"❌ ID {user['id']:3} | {user['correo']:30} | ERROR - Contraseña incorrecta")
                todos_ok = False
        
        print("-" * 70)
        if todos_ok:
            print("🎉 ¡TODAS LAS CONTRASEÑAS SON CORRECTAS!")
            print(f"   Contraseña: '{nueva_password}'")
        else:
            print("⚠️  Hay errores. Revisa manualmente.")

if __name__ == "__main__":
    fix_all_passwords()
