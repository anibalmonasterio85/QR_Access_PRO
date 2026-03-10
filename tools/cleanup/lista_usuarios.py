#!/usr/bin/env python3
"""
Listar todos los usuarios con sus datos
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from web_panel.models.user import User

def listar_usuarios():
    print("=" * 70)
    print("📋 LISTA DE USUARIOS EN EL SISTEMA")
    print("=" * 70)
    
    usuarios = User.get_all()
    
    print(f"\nID  | EMAIL                                   | NOMBRE              | ROL")
    print("-" * 70)
    
    for user in usuarios:
        print(f"{user.id:3} | {user.correo:38} | {user.nombre:20} | {user.rol}")
    
    print("-" * 70)
    print(f"Total: {len(usuarios)} usuarios")
    print("\n🔑 TODOS TIENEN CONTRASEÑA: hola123")

if __name__ == "__main__":
    listar_usuarios()
