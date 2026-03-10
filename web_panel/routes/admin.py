#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/routes/admin.py - Panel de administración
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from web_panel.models.user import User
from web_panel.services.qr_service import qr_service
from web_panel.utils.decorators import role_required
from config.settings import config

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/usuarios', methods=['GET', 'POST'])
@role_required('admin')
def usuarios():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        rut = request.form.get('rut', '').strip()
        correo = request.form.get('correo', '').strip()
        empresa = request.form.get('empresa', '').strip()
        rol = request.form.get('rol', 'usuario')
        password = request.form.get('password', '').strip()
        password2 = request.form.get('password2', '').strip()
        activo = request.form.get('activo') == 'on'
        
        if not all([nombre, rut, correo, empresa, password]):
            flash('Todos los campos son obligatorios', 'error')
        elif password != password2:
            flash('Las contraseñas no coinciden', 'error')
        elif len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
        elif User.get_by_email(correo) or User.get_by_rut(rut):
            flash('Ya existe un usuario con ese RUT o correo', 'error')
        else:
            user = User(
                nombre=nombre, rut=rut, correo=correo,
                empresa=empresa, rol=rol, activo=activo
            )
            user.set_password(password)
            user.save()
            
            try:
                qr_service.generate_for_user(user.id, user.nombre, user.correo)
                flash('✅ Usuario creado y QR enviado', 'success')
            except:
                flash('⚠️ Usuario creado pero error al enviar QR', 'warning')
            
            return redirect(url_for('admin.usuarios'))
    
    users = User.get_all()
    return render_template('admin_usuarios.html', users=users)

@admin_bp.route('/usuarios/<int:user_id>/toggle')
@role_required('admin')
def toggle_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        nuevo = user.toggle_active()
        flash(f'Usuario {"activado" if nuevo else "desactivado"}', 'success')
    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/usuarios/<int:user_id>/resend_qr')
@role_required('admin')
def resend_qr(user_id):
    user = User.get_by_id(user_id)
    if user:
        try:
            qr_service.generate_for_user(user.id, user.nombre, user.correo)
            flash('✅ QR reenviado', 'success')
        except:
            flash('⚠️ Error al reenviar QR', 'error')
    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/usuarios/<int:user_id>/edit', methods=['GET', 'POST'])
@role_required('admin')
def edit_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('admin.usuarios'))
    
    if request.method == 'POST':
        user.nombre = request.form.get('nombre', '').strip()
        user.rut = request.form.get('rut', '').strip()
        user.correo = request.form.get('correo', '').strip()
        user.empresa = request.form.get('empresa', '').strip()
        user.rol = request.form.get('rol', 'usuario')
        user.activo = request.form.get('activo') == 'on'
        user.save()
        
        flash('✅ Usuario actualizado', 'success')
        return redirect(url_for('admin.usuarios'))
    
    return render_template('edit_user.html', user=user)
