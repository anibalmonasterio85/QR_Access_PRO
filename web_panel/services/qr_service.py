#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/services/qr_service.py - Servicio de QR
"""

import secrets
import qrcode
from pathlib import Path
import logging
import logging
from typing import Optional, Tuple, Any
from datetime import datetime
from config.settings import config
from web_panel.services.email_service import email_service
from web_panel.models.user import User

logger = logging.getLogger(__name__)

class QRService:
    """Servicio para generación de QR"""
    
    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(16)
    
    @staticmethod
    def generate_qr_image(token: str, user_id: int) -> Path:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(token)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        filename = f"user_{user_id}.png"
        filepath = Path(__file__).parent.parent / "static" / "qrcodes" / filename
        img.save(filepath)
        
        logger.info(f"✅ QR generado: {filepath}")
        return filepath
    
    @classmethod
    def generate_for_user(cls, user_id: int, nombre: str, correo: str, send_email: bool = True) -> Tuple[str, Optional[datetime]]:
        """Genera QR para un usuario"""
        token = cls.generate_token()
        
        user = User.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario {user_id} no encontrado")
        
        user.update_qr(token, config.QR_EXPIRY_HOURS)
        qr_path = cls.generate_qr_image(token, user_id)
        
        if send_email and email_service.enabled:
            email_service.send_qr_email(correo, nombre, qr_path)
        
        return token, user.fecha_expiracion
    
    @staticmethod
    def validate_qr(qr_code: str) -> Tuple[Optional[User], str, str]:
        """Valida un QR contra BD"""
        user = User.get_by_qr(qr_code)
        
        if not user:
            return None, "NO_REGISTRADO", "Código no registrado"
        
        if not user.is_active():
            return user, "INACTIVO", "Usuario desactivado"
        
        if not user.is_qr_valid():
            return user, "EXPIRADO", "QR expirado"
        
        return user, "OK", "Acceso permitido"
    
    @staticmethod
    def get_qr_path(user_id: int) -> Path:
        # Asume que config.QR_DIR devuelve un objeto Path
        return Path(config.QR_DIR) / f"user_{user_id}.png"

qr_service = QRService()
