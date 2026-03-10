import os
from pathlib import Path
from waitress import serve
from web_panel.app import app
from config.settings import config
import logging

def run_production_server():
    # Asegurar que estamos en el directorio base
    base_dir = Path(__file__).parent.absolute()
    os.chdir(str(base_dir))
    
    # Configurar puerto y host
    # Se expone por omision en 0.0.0.0
    host = '0.0.0.0'
    port = getattr(config, 'PORT', 5000)

    # Logging robusto
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    print(f"=== INICIANDO QR ACCESS PRO EN MODO DE PRODUCCION (WAITRESS) ===")
    print(f"-> Servidor escuchando en: http://{host}:{port}")
    print(f"-> Ctrl+C para detener")
    print(f"================================================================")
    
    # Configurar waitress (soporta multiples hilos nativos para web server en windows/raspberry)
    serve(app, host=host, port=port, threads=8, connection_limit=1000)

if __name__ == '__main__':
    run_production_server()
