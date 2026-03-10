#!/usr/bin/env python3
"""
Script para resetear el usuario administrador
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import db
from werkzeug.security import generate_password_hash

def reset_admin():
    print("🔄 Resetando usuario administrador...")
    
    email = "anibalmonas124@gmail.com"
    password = "Admin123!"
    password_hash = generate_password_hash(password)
    
    with db.get_cursor() as cursor:
        # Verificar si existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (email,))
        existe = cursor.fetchone()
        
        if existe:
            # Actualizar
            cursor.execute("""
                UPDATE usuarios 
                SET nombre = 'Administrador',
                    rut = 'ADMIN-QR',
                    empresa_id = 1,
                    password_hash = %s,
                    rol = 'admin',
                    activo = 1
                WHERE correo = %s
            """, (password_hash, email))
            print(f"✅ Admin actualizado: {email}")
        else:
            # Insertar
            cursor.execute("""
                INSERT INTO usuarios 
                (nombre, rut, correo, empresa_id, password_hash, rol, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, ("Administrador", "ADMIN-QR", email, 1, password_hash, "admin", 1))
            print(f"✅ Admin creado: {email}")
        
        # Verificar
        cursor.execute("SELECT id, nombre, rol FROM usuarios WHERE correo = %s", (email,))
        admin = cursor.fetchone()
        print(f"   ID: {admin[0]}, Nombre: {admin[1]}, Rol: {admin[2]}")

if __name__ == "__main__":
    reset_admin()
