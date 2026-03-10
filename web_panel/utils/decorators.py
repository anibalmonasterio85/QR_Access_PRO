#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/utils/decorators.py - Decoradores para rutas
"""

from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify

def login_required(f):
    """Requiere que el usuario esté logueado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Requiere que el usuario tenga cierto rol"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debes iniciar sesión', 'error')
                return redirect(url_for('auth.login'))
            if session.get('rol') not in roles:
                flash('No tienes permisos para acceder', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def ajax_required(f):
    """Protección contra acceso directo o scraping a las APIs"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return jsonify({'status': 'error', 'message': 'Solicitud no autorizada o directa bloqueada'}), 403
        return f(*args, **kwargs)
    return decorated_function
