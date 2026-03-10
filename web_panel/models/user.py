#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/models/user.py - Modelo de Usuario adaptado a tu BD
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db
from config.settings import config

class User:
    """Representa un usuario del sistema - Adaptado a tu esquema BD"""

    def __init__(self, id: Optional[int] = None, nombre: Optional[str] = None, rut: Optional[str] = None, correo: Optional[str] = None,
                 empresa_id: Optional[int] = None, password_hash: Optional[str] = None, rol: str = 'usuario',
                 activo: Union[int, bool] = 1, qr_code: Optional[str] = None, fecha_expiracion: Optional[datetime] = None,
                 fecha_registro: Optional[datetime] = None, **kwargs: Any):
        """
        Inicializador flexible que acepta cualquier campo extra
        y solo usa los que necesitamos
        """
        self.id = id
        self.nombre = nombre
        self.rut = rut
        self.correo = correo
        self.empresa_id = empresa_id
        self.empresa = self._get_empresa_nombre(empresa_id) if empresa_id else "Sin empresa"
        self.rol = rol
        self.activo = bool(activo)
        self.qr_code = qr_code
        self.fecha_expiracion = fecha_expiracion
        self.password_hash = password_hash
        self.fecha_registro = fecha_registro

    def _get_empresa_nombre(self, empresa_id):
        """Obtiene el nombre de la empresa desde la tabla empresas"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute("SELECT nombre FROM empresas WHERE id = %s", (empresa_id,))
                result = cursor.fetchone()
                return result[0] if result else "Desconocida"
        except:
            return f"Empresa #{empresa_id}"

    @classmethod
    def from_db_row(cls, row):
        """Crea un usuario desde una fila de base de datos"""
        if not row:
            return None
        # Convertir tupla a diccionario si es necesario
        if isinstance(row, dict):
            return cls(**row)
        else:
            # Si es tupla, asumimos orden estándar
            fields = ['id', 'nombre', 'rut', 'correo', 'empresa_id', 
                     'password_hash', 'rol', 'activo', 'qr_code', 
                     'fecha_expiracion', 'fecha_registro']
            data = dict(zip(fields, row[:len(fields)]))
            return cls(**data)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def is_active(self) -> bool:
        return self.activo

    def has_qr(self) -> bool:
        return bool(self.qr_code and self.fecha_expiracion)

    def is_qr_valid(self) -> bool:
        if not self.has_qr():
            return False
        if not self.fecha_expiracion:
            return False
        return self.fecha_expiracion > datetime.now()

    def qr_status(self) -> str:
        if not self.has_qr():
            return "Sin QR"
        if self.is_qr_valid() and self.fecha_expiracion:
            return f"Válido hasta {self.fecha_expiracion.strftime('%d/%m/%Y %H:%M')}"
        if self.fecha_expiracion:
            return f"Expirado el {self.fecha_expiracion.strftime('%d/%m/%Y %H:%M')}"
        return "Estado Desconocido"

    def save(self) -> 'User':
        with db.get_cursor() as cursor:
            if self.id:
                cursor.execute("""
                    UPDATE usuarios SET
                        nombre=%s, rut=%s, correo=%s, empresa_id=%s,
                        rol=%s, activo=%s, qr_code=%s, fecha_expiracion=%s
                    WHERE id=%s
                """, (self.nombre, self.rut, self.correo, self.empresa_id,
                      self.rol, self.activo, self.qr_code,
                      self.fecha_expiracion, self.id))
            else:
                cursor.execute("""
                    INSERT INTO usuarios 
                    (nombre, rut, correo, empresa_id, password_hash, rol, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (self.nombre, self.rut, self.correo, self.empresa_id,
                      self.password_hash, self.rol, self.activo))
                self.id = cursor.lastrowid
        return self

    def update_qr(self, qr_code: str, expiry_hours: Optional[int] = None) -> None:
        if expiry_hours is None:
            expiry_hours = config.QR_EXPIRY_HOURS

        self.qr_code = qr_code
        self.fecha_expiracion = datetime.now() + timedelta(hours=expiry_hours)

        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE usuarios 
                SET qr_code=%s, fecha_expiracion=%s 
                WHERE id=%s
            """, (qr_code, self.fecha_expiracion, self.id))

    def toggle_active(self) -> bool:
        self.activo = not self.activo
        with db.get_cursor() as cursor:
            cursor.execute("UPDATE usuarios SET activo=%s WHERE id=%s",
                          (self.activo, self.id))
        return self.activo

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id=%s", (user_id,))
            return cls.from_db_row(cursor.fetchone())

    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (email,))
            return cls.from_db_row(cursor.fetchone())

    @classmethod
    def get_by_qr(cls, qr_code: str) -> Optional['User']:
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE qr_code=%s", (qr_code,))
            return cls.from_db_row(cursor.fetchone())

    @classmethod
    def get_by_rut(cls, rut: str) -> Optional['User']:
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE rut=%s", (rut,))
            return cls.from_db_row(cursor.fetchone())

    @classmethod
    def get_all(cls) -> List['User']:
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")
            results = []
            for row in cursor.fetchall():
                user = cls.from_db_row(row)
                if user is not None:
                    results.append(user)
            return results

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.nombre}>"

def ensure_admin_exists() -> Optional[User]:
    """Crea el admin por defecto si no existe"""
    admin = User.get_by_email(config.ADMIN_EMAIL)

    if admin:
        if admin.rol != 'admin' or not admin.activo:
            admin.rol = 'admin'
            admin.activo = True
            admin.save()
            print(f"[OK] Admin actualizado: {config.ADMIN_EMAIL}")
    else:
        # Necesitamos un empresa_id válido - por defecto usamos 1
        # Asumimos que existe una empresa con ID 1
        admin = User(
            nombre="Administrador",
            rut="ADMIN-QR",
            correo=config.ADMIN_EMAIL,
            empresa_id=1,  # ID de empresa por defecto
            rol="admin",
            activo=True
        )
        admin.set_password(config.ADMIN_DEFAULT_PASS)
        admin.save()
        print(f"[OK] Admin creado: {config.ADMIN_EMAIL}")

    return admin
