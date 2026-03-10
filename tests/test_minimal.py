#!/usr/bin/env python3
"""
Script de prueba mínimo
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("1. Probando import config...")
try:
    from config.settings import config
    print("   ✅ config.settings OK")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n2. Probando import database...")
try:
    from config.database import db, test_connection
    print("   ✅ config.database OK")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n3. Probando conexión BD...")
test_connection()

print("\n4. Probando import models...")
try:
    from web_panel.models.user import User, ensure_admin_exists
    print("   ✅ models.user OK")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n5. Probando crear admin...")
try:
    admin = ensure_admin_exists()
    print(f"   ✅ Admin: {admin}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n✅ Pruebas completadas")
