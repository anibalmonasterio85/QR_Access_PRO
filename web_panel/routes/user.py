#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/routes/user.py - Panel de usuario
"""

from flask import Blueprint, render_template, session, request, flash, redirect, url_for
import time
from web_panel.models.user import User
from web_panel.services.qr_service import qr_service
from web_panel.utils.decorators import login_required
from config.settings import config

user_bp = Blueprint('user', __name__)

@user_bp.route('/panel', methods=['GET', 'POST'])
@login_required
def panel():
    user = User.get_by_id(session['user_id'])
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        try:
            qr_service.generate_for_user(user.id, user.nombre, user.correo, send_email=True)
            flash('✅ QR regenerado y enviado a tu correo', 'success')
        except Exception as e:
            flash('⚠️ Error al regenerar QR', 'error')
        return redirect(url_for('user.panel'))
    
    qr_activo = False
    qr_url = ""
    exp_text = "Sin QR generado"
    timestamp = int(time.time())
    
    if user.has_qr():
        if user.is_qr_valid():
            qr_activo = True
            exp_text = f"Válido hasta: {user.fecha_expiracion.strftime('%d/%m/%Y %H:%M')}"
            if qr_service.get_qr_path(user.id).exists():
                qr_url = f"/static/qrcodes/user_{user.id}.png?t={timestamp}"
        else:
            exp_text = f"⚠️ Expirado: {user.fecha_expiracion.strftime('%d/%m/%Y %H:%M')}"
    
    return render_template(
        'user_panel.html',
        system_name=config.SYSTEM_NAME,
        user=user,
        qr_activo=qr_activo,
        qr_url=qr_url,
        exp_text=exp_text
    )
