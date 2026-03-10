#!/usr/bin/env python3
"""
Script para limpiar usuarios - Mantiene solo admin, guardia y usuario normal
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import db
from werkzeug.security import generate_password_hash

def limpiar_usuarios():
    print("=" * 60)
    print("🧹 LIMPIANDO BASE DE DATOS DE USUARIOS")
    print("=" * 60)
    
    # Lista de correos a mantener
    correos_mantener = [
        'anibalmonas124@gmail.com',    # Admin
        'anibalmj090@gmail.com',        # Guardia
        'anibalmonasterio85@gmail.com'  # Usuario normal
    ]
    
    with db.get_cursor(dictionary=True) as cursor:
        # 1. Ver todos los usuarios antes
        cursor.execute("SELECT id, nombre, correo, rol FROM usuarios ORDER BY id")
        todos = cursor.fetchall()
        
        print("\n📋 USUARIOS ACTUALES:")
        print("-" * 60)
        for u in todos:
            print(f"ID: {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:10} | {u['nombre']}")
        
        # 2. Contar cuántos vamos a eliminar
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_inicial = cursor.fetchone()['total']
        
        # 3. Eliminar usuarios que NO están en la lista
        placeholders = ','.join(['%s'] * len(correos_mantener))
        query = f"DELETE FROM usuarios WHERE correo NOT IN ({placeholders})"
        cursor.execute(query, correos_mantener)
        eliminados = cursor.rowcount
        
        print(f"\n🗑️  Usuarios eliminados: {eliminados}")
        
        # 4. Verificar/crear los usuarios que deben existir
        for correo in correos_mantener:
            cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
            existe = cursor.fetchone()
            
            if existe:
                print(f"✅ {correo} - Ya existe (ID: {existe['id']})")
            else:
                # Crear usuario según su rol
                if correo == 'anibalmonas124@gmail.com':
                    nombre = "Administrador"
                    rut = "ADMIN-QR"
                    rol = "admin"
                    password = "Admin123!"
                elif correo == 'anibalmj090@gmail.com':
                    nombre = "Guardia"
                    rut = "GUARDIA-QR"
                    rol = "guardia"
                    password = "Guardia123!"
                else:  # anibalmonasterio85@gmail.com
                    nombre = "Usuario Normal"
                    rut = "USER-QR"
                    rol = "usuario"
                    password = "User123!"
                
                password_hash = generate_password_hash(password)
                
                cursor.execute("""
                    INSERT INTO usuarios 
                    (nombre, rut, correo, empresa_id, password_hash, rol, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (nombre, rut, correo, 1, password_hash, rol, 1))
                
                print(f"✨ CREADO: {correo} - Rol: {rol}")
        
        # 5. Verificar resultado final
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_final = cursor.fetchone()['total']
        
        print("\n" + "=" * 60)
        print(f"📊 RESUMEN:")
        print(f"   Usuarios iniciales: {total_inicial}")
        print(f"   Usuarios eliminados: {eliminados}")
        print(f"   Usuarios finales: {total_final}")
        print("=" * 60)
        
        # 6. Mostrar usuarios finales
        cursor.execute("SELECT id, nombre, correo, rol FROM usuarios ORDER BY id")
        finales = cursor.fetchall()
        
        print("\n👥 USUARIOS MANTENIDOS:")
        print("-" * 60)
        for u in finales:
            print(f"ID: {u['id']:3} | {u['correo']:30} | Rol: {u['rol']:10} | {u['nombre']}")
        
        print("\n🔑 CONTRASEÑAS:")
        print("   Admin:  Admin123!")
        print("   Guardia: Guardia123!")
        print("   Usuario: User123!")

if __name__ == "__main__":
    limpiar_usuarios()
