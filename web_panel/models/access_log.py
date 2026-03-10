#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/models/access_log.py - Modelo de Log de Accesos
"""

from datetime import datetime
from config.database import db

class AccessLog:
    """Registro de intentos de acceso"""
    
    def __init__(self, id=None, qr_texto=None, resultado=None, fecha_hora=None, **kwargs):
        self.id = id
        self.qr_texto = qr_texto
        self.resultado = resultado
        self.fecha_hora = fecha_hora or datetime.now()
        # Absorber cualquier columna extra que la BD tenga configurada
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def from_db_row(cls, row):
        if not row:
            return None
        return cls(**row)
    
    @classmethod
    def create(cls, qr_texto, resultado):
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO accesos_log (qr_texto, resultado)
                VALUES (%s, %s)
            """, (qr_texto, resultado))
            return cursor.lastrowid
    
    @classmethod
    def create_permitido(cls, qr_texto, user=None):
        detalle = f"{user.nombre} ({user.empresa})" if user else qr_texto
        return cls.create(detalle, "PERMITIDO")
    
    @classmethod
    def create_denegado(cls, qr_texto, motivo, user=None):
        detalle = f"{user.nombre} ({user.empresa})" if user else qr_texto
        return cls.create(detalle, f"DENEGADO - {motivo}")
    
    @classmethod
    def get_recent(cls, limit=50):
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT * FROM accesos_log 
                ORDER BY fecha_hora DESC 
                LIMIT %s
            """, (limit,))
            return [cls.from_db_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_filtered(cls, fecha_inicio, fecha_fin, resultado, busqueda, limit=200):
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT * FROM accesos_log 
                WHERE fecha_hora BETWEEN %s AND %s
                  AND resultado LIKE %s
                  AND qr_texto LIKE %s
                ORDER BY fecha_hora DESC
                LIMIT %s
            """, (fecha_inicio, fecha_fin, resultado, busqueda, limit))
            return [cls.from_db_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_stats(cls):
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN resultado = 'PERMITIDO' THEN 1 ELSE 0 END) as permitidos,
                    SUM(CASE WHEN resultado LIKE 'DENEGADO%' THEN 1 ELSE 0 END) as denegados
                FROM accesos_log
            """)
            row = cursor.fetchone()
            return {
                'total': int(row[0] or 0),
                'permitidos': int(row[1] or 0),
                'denegados': int(row[2] or 0)
            }
    
    @classmethod
    def get_weekly_stats(cls):
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    DATE(fecha_hora) as fecha,
                    SUM(CASE WHEN resultado = 'PERMITIDO' THEN 1 ELSE 0 END) as permitidos,
                    SUM(CASE WHEN resultado LIKE 'DENEGADO%' THEN 1 ELSE 0 END) as denegados
                FROM accesos_log
                WHERE fecha_hora >= NOW() - INTERVAL 7 DAY
                GROUP BY DATE(fecha_hora)
                ORDER BY DATE(fecha_hora)
            """)
            results = []
            for row in cursor.fetchall():
                results.append({
                    'fecha': row[0],
                    'permitidos': int(row[1] or 0),
                    'denegados': int(row[2] or 0)
                })
            return results
    
    @classmethod
    def get_by_qr(cls, qr_texto, limit=50):
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT * FROM accesos_log 
                WHERE qr_texto LIKE %s
                ORDER BY fecha_hora DESC
                LIMIT %s
            """, (f"%{qr_texto}%", limit))
            return [cls.from_db_row(row) for row in cursor.fetchall()]
    
    def is_permitido(self):
        return 'PERMITIDO' in self.resultado
    
    def __repr__(self):
        return f"<AccessLog {self.id}: {self.resultado}>"
