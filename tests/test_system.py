#!/usr/bin/env python3
"""
Script de prueba del sistema
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Configurar encoding
import locale
try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    pass

from config.database import test_connection
from web_panel.models.user import User, ensure_admin_exists
from web_panel.models.access_log import AccessLog
from web_panel.services.qr_service import qr_service

def test_all():
    print("\n[TEST] Probando conexion BD...")
    if not test_connection():
        print("[ERROR] Error en BD")
        return False

    print("\n[TEST] Probando usuario admin...")
    admin = ensure_admin_exists()
    print(f"   Admin: {admin}")

    print("\n[TEST] Probando estadisticas...")
    stats = AccessLog.get_stats()
    print(f"   Stats: {stats}")

    print("\n[TEST] Probando generacion QR...")
    token = qr_service.generate_token()
    print(f"   Token: {token}")

    print("\n[OK] Todas las pruebas pasaron")
    return True

if __name__ == "__main__":
    test_all()
