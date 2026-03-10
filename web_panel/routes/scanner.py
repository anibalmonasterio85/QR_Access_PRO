#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/routes/scanner.py - Interfaz Web de Escaneo
"""

from flask import Blueprint, render_template, request, jsonify
from web_panel.utils.decorators import role_required
from web_panel.models.user import User
from web_panel.models.access_log import AccessLog
from web_panel.utils.security import require_api_key
from config.settings import config
from datetime import datetime

scanner_bp = Blueprint('scanner', __name__, url_prefix='/scanner')

@scanner_bp.route('/')
@role_required('admin', 'guardia')
def scanner_view():
    """Renderiza la vista del escáner web basado en HTML5"""
    return render_template('scanner.html')

@scanner_bp.route('/validate', methods=['POST'])
@require_api_key
def validate_qr():
    """Recibe código QR y simula el funcionamiento del módulo físico"""
    data = request.get_json()
    if not data or 'qr_code' not in data:
        return jsonify({"status": "error", "message": "No se recibió código QR"}), 400
        
    qr_code = data['qr_code']
    
    # Simular la lógica de validación de Raspberry
    user = User.get_by_qr(qr_code)
    
    estado_resultado = "OK"
    mensaje = "Acceso Permitido"
    
    if not user:
        estado_resultado = "DENEGADO - NO REGISTRADO"
        mensaje = "Código no registrado en el sistema."
    elif not user.is_active():
        estado_resultado = "DENEGADO - INACTIVO"
        mensaje = "Usuario desactivado."
    elif not user.is_qr_valid():
        estado_resultado = "DENEGADO - EXPIRADO"
        mensaje = "Código QR ha expirado."
    else:
        estado_resultado = "PERMITIDO"
        mensaje = f"Acceso concedido para {user.nombre}"
    
    # Registrar el acceso en la DB
    if "PERMITIDO" in estado_resultado:
        AccessLog.create_permitido(qr_code, user)
    else:
        # Extraer el motivo del estado
        motivo = estado_resultado.replace("DENEGADO - ", "")
        AccessLog.create_denegado(qr_code, motivo, user)
    
    # Retornar estado visual al Frontend
    return jsonify({
        "status": "success" if "PERMITIDO" in estado_resultado else "error",
        "message": mensaje,
        "user_name": user.nombre if user else "Desconocido",
        "company": user.empresa if user else ""
    })
