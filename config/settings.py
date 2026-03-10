#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config/settings.py - Configuración centralizada del sistema
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).parent.parent.absolute()

# Cargar variables de entorno
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"[OK] Configuracion cargada desde: {env_path}")
else:
    print(f"[WARN] Archivo .env no encontrado en {env_path}")

class Config:
    """Clase de configuración centralizada"""

    # Directorios
    BASE_DIR = BASE_DIR
    STATIC_DIR = BASE_DIR / 'web_panel' / 'static'
    QR_DIR = STATIC_DIR / 'qrcodes'
    LOG_DIR = BASE_DIR / 'logs'

    # Crear directorios
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    QR_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-no-usa-en-produccion')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SYSTEM_NAME = os.getenv('SYSTEM_NAME', 'QR Access Control')

    # Base de datos
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'database': os.getenv('DB_NAME', 'qr_access'),
        'pool_size': int(os.getenv('DB_POOL_SIZE', '5')),
        'charset': 'utf8mb4',
        'use_unicode': True,
        'autocommit': False,
    }

    # Email
    MAIL_CONFIG = {
        'server': os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
        'port': int(os.getenv('MAIL_PORT', '587')),
        'use_tls': os.getenv('MAIL_USE_TLS', 'True').lower() == 'true',
        'username': os.getenv('MAIL_USERNAME'),
        'password': os.getenv('MAIL_PASSWORD'),
    }

    # Hardware
    HARDWARE_CONFIG = {
        'arduino_port': os.getenv('ARDUINO_PORT', '/dev/ttyUSB0'),
        'camera_id': int(os.getenv('CAMERA_ID', '0')),
        'servo_pin': int(os.getenv('SERVO_PIN', '22')),
        'led_pins': {
            'green': int(os.getenv('LED_GREEN_PIN', '17')),
            'red': int(os.getenv('LED_RED_PIN', '27')),
        }
    }

    # Admin por defecto
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@localhost')
    ADMIN_DEFAULT_PASS = os.getenv('ADMIN_DEFAULT_PASS', 'Admin123!')

    # QR
    QR_EXPIRY_HOURS = int(os.getenv('QR_EXPIRY_HOURS', '24'))

    @classmethod
    def validate(cls):
        """Valida la configuración"""
        issues = []
        if not cls.DB_CONFIG['user'] or not cls.DB_CONFIG['password']:
            issues.append("DB_USER y DB_PASS deben estar definidos")
        if issues:
            print("[WARN] Problemas de configuracion:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        return True

# Instancia de configuración
config = Config()
config.validate()
