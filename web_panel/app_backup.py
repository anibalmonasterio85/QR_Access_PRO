#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/app.py - AplicaciÃ³n Flask principal
"""

import sys
from pathlib import Path

# Agregar el directorio raÃ­z al path de Python
BASE_DIR = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(BASE_DIR))

from flask import Flask, redirect, url_for, session, render_template
import logging
from logging.handlers import RotatingFileHandler

from config.settings import config
from web_panel.models.user import ensure_admin_exists

from web_panel.routes.auth import auth_bp
from web_panel.routes.dashboard import dashboard_bp
from web_panel.routes.user import user_bp
from web_panel.routes.admin import admin_bp
from web_panel.routes.api import api_bp

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG

    # Configurar logging
    log_file = config.LOG_DIR / 'web_panel.log'
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        if 'user_id' in session:
            if session.get('rol') in ['admin', 'guardia']:
                return redirect(url_for('dashboard.index'))
            return redirect(url_for('user.panel'))
        return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # Asegurar admin
    with app.app_context():
        ensure_admin_exists()

    app.logger.info("âœ… AplicaciÃ³n Flask iniciada")
    return app

app = create_app()

if __name__ == '__main__':
    # Forzar puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)

from flask import send_file
from io import BytesIO
import qrcode

@app.route('/generar_mi_qr')
def generar_mi_qr():
    # Usamos el ID de usuario de la sesion actual
    if 'user_id' not in session:
        return "No autorizado", 403
    
    user_data = f"ACCESO_PRO_{session['user_id']}"
    qr = qrcode.make(user_data)
    
    buf = BytesIO()
    qr.save(buf, 'PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/panel', methods=['POST'])
def generar_qr_post():
    import qrcode
    from io import BytesIO
    from flask import send_file, session
    
    # Aquí podrías validar al usuario Anibal Monasterio
    # Por ahora generamos un QR con un token simple
    data = "ACCESO_PRO_ANIBAL_ADMIN"
    qr = qrcode.make(data)
    
    buf = BytesIO()
    qr.save(buf, 'PNG')
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

@app.route('/panel', methods=['POST'])
def generar_qr_post():
    import qrcode
    from io import BytesIO
    from flask import send_file, session
    
    # Aquí podrías validar al usuario Anibal Monasterio
    # Por ahora generamos un QR con un token simple
    data = "ACCESO_PRO_ANIBAL_ADMIN"
    qr = qrcode.make(data)
    
    buf = BytesIO()
    qr.save(buf, 'PNG')
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')
@app.route('/panel', methods=['GET', 'POST'])
def panel():
    from flask import render_template, request, session, send_file
    import qrcode
    from io import BytesIO

    if request.method == 'POST':
        # Generar QR dinámico para el usuario actual
        data = "USER:Anibal_Monasterio|ROLE:ADMIN|STATUS:ACTIVE"
        qr = qrcode.make(data)
        buf = BytesIO()
        qr.save(buf, 'PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    
    return render_template('panel.html')
