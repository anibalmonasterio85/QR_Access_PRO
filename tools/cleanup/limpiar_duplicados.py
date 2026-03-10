#!/usr/bin/env python3
"""
Eliminar usuarios duplicados, mantener solo uno por email
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import db
from werkzeug.security import generate_password_hash

def limpiar_duplicados():
    print("=" * 70)
    print("🧹 LIMPIANDO USUARIOS DUPLICADOS")
    print("=" * 70)
    
    with db.get_cursor(dictionary=True) as cursor:
        # Encontrar emails duplicados
        cursor.execute("""
            SELECT correo, COUNT(*) as count, GROUP_CONCAT(id) as ids
            FROM usuarios
            GROUP BY correo
            HAVING count > 1
        """)
        
        duplicados = cursor.fetchall()
        
        if not duplicados:
            print("✅ No hay usuarios duplicados")
            return
        
        print(f"\n📋 EMAILS DUPLICADOS ENCONTRADOS:")
        print("-" * 70)
        
        for dup in duplicados:
            ids = dup['ids'].split(',')
            print(f"Email: {dup['correo']}")
            print(f"   IDs: {', '.join(ids)}")
            print(f"   Total: {dup['count']} usuarios")
            
            # Mantener el ID más bajo, eliminar los demás
            mantener = min(ids)
            eliminar = [id for id in ids if id != mantener]
            
            print(f"   Mantener ID: {mantener}")
            print(f"   Eliminar IDs: {', '.join(eliminar)}")
            
            # Eliminar duplicados
            for id_eliminar in eliminar:
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_eliminar,))
                print(f"      ✅ Eliminado ID {id_eliminar}")
        
        print("\n✅ Limpieza completada")

if __name__ == "__main__":
    limpiar_duplicados()
