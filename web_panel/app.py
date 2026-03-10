import sys
from pathlib import Path

# Agregar el directorio raiz al path de Python
BASE_DIR = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(BASE_DIR))

from flask import Flask, redirect, url_for, session, render_template
import logging
from logging.handlers import RotatingFileHandler
import sentry_sdk
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config.settings import config
from web_panel.models.user import ensure_admin_exists

from web_panel.routes.auth import auth_bp
from web_panel.routes.dashboard import dashboard_bp
from web_panel.routes.user import user_bp
from web_panel.routes.admin import admin_bp
from web_panel.routes.api import api_bp
from web_panel.routes.export import export_bp
from web_panel.routes.scanner import scanner_bp

def create_app():
    # Inicializar Sentry (solo si existe DSN en config, si no pasa en silencio)
    if hasattr(config, 'SENTRY_DSN') and config.SENTRY_DSN:
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )

    app = Flask(__name__)

    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG

    # Inicializar Rate Limiter para proteccion contra fuerza bruta
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

    # Inyectar el limiter en la app para ser usado en blueprints
    app.limiter = limiter

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
    app.register_blueprint(export_bp)
    app.register_blueprint(scanner_bp)

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

    app.logger.info("Aplicacion Flask iniciada")
    return app

app = create_app()

if __name__ == '__main__':
    # Forzar puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
