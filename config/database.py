#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config/database.py - Pool de conexiones a MariaDB
"""

import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
import time
from .settings import config

class DatabasePool:
    """Singleton pool de conexiones"""

    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self, retries=3):
        """Inicializa el pool con reintentos"""
        pool_config = {
            'pool_name': 'qr_pool',
            'pool_size': config.DB_CONFIG['pool_size'],
            'pool_reset_session': True,
            'host': config.DB_CONFIG['host'],
            'port': config.DB_CONFIG['port'],
            'user': config.DB_CONFIG['user'],
            'password': config.DB_CONFIG['password'],
            'database': config.DB_CONFIG['database'],
            'charset': 'utf8mb4',
            'use_unicode': True,
            'autocommit': False,
            'connection_timeout': 30,
        }

        for attempt in range(retries):
            try:
                self._pool = pooling.MySQLConnectionPool(**pool_config)
                # Probar conexión
                test_conn = self._pool.get_connection()
                test_conn.close()
                print(f"[OK] Pool de BD creado en {config.DB_CONFIG['host']}")
                return
            except Exception as e:
                print(f"[WARN] Intento {attempt + 1} fallo: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    print("[ERROR] No se pudo conectar a BD")
                    raise

    @contextmanager
    def get_connection(self):
        """Obtiene conexión del pool"""
        conn = None
        try:
            conn = self._pool.get_connection()
            yield conn
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_cursor(self, dictionary=False, buffered=True):
        """Obtiene cursor para consultas"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=dictionary, buffered=buffered)
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise
            finally:
                cursor.close()

# Instancia global
db = DatabasePool()

def test_connection():
    """Prueba la conexión a BD"""
    try:
        with db.get_cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("[OK] Conexion a BD verificada")
                
                # Mostrar tablas
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                if tables:
                    print(f"   Tablas: {', '.join(t[0] for t in tables)}")
                return True
    except Exception as e:
        print(f"[ERROR] Error en BD: {e}")
        return False

if __name__ == "__main__":
    test_connection()
