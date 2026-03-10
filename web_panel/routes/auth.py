#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/routes/auth.py - Rutas de autenticación
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
import re
from web_panel.models.user import User
from web_panel.services.qr_service import qr_service
from web_panel.utils.security import generate_2fa_secret, generate_2fa_qr, verify_2fa_token
from config.settings import config
from config.database import db

auth_bp = Blueprint('auth', __name__)
EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Aplicar el limitador asumiendo que esta en current_app.limiter
    if request.method == 'POST':
        try:
            current_app.limiter.limit("5 per minute")(lambda: None)()
        except Exception as e:
            flash("Demasiados intentos fallidos. Intente de nuevo en 1 minuto.", "error")
            return render_template('login.html', system_name=config.SYSTEM_NAME), 429

    if request.method == 'POST':
        email = request.form.get('correo', '').strip()
        password = request.form.get('password', '').strip()
        
        user = User.get_by_email(email)
        
        
        if user and user.is_active() and user.check_password(password):
            # Login normal sin 2FA para todos
            session['user_id'] = user.id
            session['nombre'] = user.nombre
            session['rol'] = user.rol
            flash(f'¡Bienvenido {user.nombre}!', 'success')
            
            if user.rol in ['admin', 'guardia']:
                return redirect(url_for('dashboard.index'))
            else:
                return redirect(url_for('user.panel'))
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html', system_name=config.SYSTEM_NAME)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        rut = request.form.get('rut', '').strip()
        correo = request.form.get('correo', '').strip()
        empresa = request.form.get('empresa', '').strip()
        password = request.form.get('password', '').strip()
        password2 = request.form.get('password2', '').strip()
        
        if not all([nombre, rut, correo, empresa, password]):
            flash('Todos los campos son obligatorios', 'error')
        elif not EMAIL_REGEX.match(correo):
            flash('Correo inválido', 'error')
        elif password != password2:
            flash('Las contraseñas no coinciden', 'error')
        elif len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
        elif User.get_by_email(correo) or User.get_by_rut(rut):
            flash('Ya existe un usuario con ese RUT o correo', 'error')
        else:
            user = User(
                nombre=nombre, rut=rut, correo=correo,
                empresa=empresa, rol='usuario', activo=True
            )
            user.set_password(password)
            user.save()
            
            try:
                qr_service.generate_for_user(user.id, user.nombre, user.correo)
                flash('✅ Registro exitoso. Revisa tu correo', 'success')
            except Exception as e:
                flash('⚠️ Registro exitoso pero error al generar QR', 'warning')
            
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', system_name=config.SYSTEM_NAME)
