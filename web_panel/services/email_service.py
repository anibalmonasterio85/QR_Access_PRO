#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/services/email_service.py - Servicio de correo
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path
from config.settings import config

logger = logging.getLogger(__name__)

class EmailService:
    """Servicio para envío de emails"""
    
    def __init__(self):
        self.enabled = bool(config.MAIL_CONFIG['username'])
        self.smtp_server = config.MAIL_CONFIG['server']
        self.smtp_port = config.MAIL_CONFIG['port']
        self.use_tls = config.MAIL_CONFIG['use_tls']
        self.username = config.MAIL_CONFIG['username']
        self.password = config.MAIL_CONFIG['password']
        
        if self.enabled:
            logger.info(f"📧 Email configurado: {self.username}")
    
    def send_email(self, to_addr, subject, body, html_body=None, attachments=None):
        """Envía un correo electrónico"""
        if not self.enabled:
            logger.warning(f"Email no enviado a {to_addr}: servicio deshabilitado")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_addr if isinstance(to_addr, str) else ', '.join(to_addr)
        
        msg.attach(MIMEText(body, 'plain'))
        
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))
        
        if attachments:
            for name, content, mime_type in attachments:
                if mime_type.startswith('image/'):
                    img = MIMEImage(content)
                    img.add_header('Content-Disposition', 'attachment', filename=name)
                    msg.attach(img)
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"✅ Email enviado a {to_addr}")
            return True
        except Exception as e:
            logger.error(f"❌ Error enviando email: {e}")
            return False
    
    def send_qr_email(self, to_addr, nombre, qr_path):
        """Envía QR por email"""
        if not Path(qr_path).exists():
            logger.error(f"QR no encontrado: {qr_path}")
            return False
        
        subject = f"{config.SYSTEM_NAME} - Tu código QR"
        
        body = f"""Hola {nombre},

Se ha generado tu código QR de acceso.

📱 Instrucciones:
1. Guarda el QR adjunto
2. Preséntalo frente al escáner
3. Válido por {config.QR_EXPIRY_HOURS} horas

🔐 Código personal e intransferible.

Saludos,
{config.SYSTEM_NAME}
"""
        
        with open(qr_path, 'rb') as f:
            qr_content = f.read()
        
        attachments = [('qr_code.png', qr_content, 'image/png')]
        return self.send_email(to_addr, subject, body, None, attachments)

# Instancia global
email_service = EmailService()
