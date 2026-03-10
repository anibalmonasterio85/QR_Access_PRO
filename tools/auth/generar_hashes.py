#!/usr/bin/env python3
from werkzeug.security import generate_password_hash, check_password_hash

passwords = {
    'Admin123!': 'anibalmonas124@gmail.com (Admin)',
    'Guardia123!': 'anibalmj090@gmail.com (Guardia)',
    'User123!': 'anibalmonasterio85@gmail.com (Usuario)'
}

print("🔑 HASHES DE CONTRASEÑAS:")
print("=" * 60)

for password, desc in passwords.items():
    hash_pass = generate_password_hash(password)
    print(f"\n{desc}")
    print(f"Password: {password}")
    print(f"Hash: {hash_pass}")
    print(f"Verificación: {check_password_hash(hash_pass, password)}")

print("\n" + "=" * 60)
print("GUARDA ESTOS HASHES PARA REFERENCIA")
