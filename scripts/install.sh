#!/bin/bash

echo "🔄 Instalando QR Access Control PRO..."

# Actualizar sistema
sudo apt update
sudo apt install -y python3-dev python3-pip python3-venv \
    libjpeg-dev zlib1g-dev libfreetype6-dev \
    mariadb-server mariadb-client

# Crear estructura
cd ~
rm -rf ~/QR_Access_PRO
mkdir -p ~/QR_Access_PRO
cd ~/QR_Access_PRO

# Crear directorios
mkdir -p config web_panel/{models,routes,services,templates,static/{css,js,qrcodes},utils} \
         scanner/{hardware,validators,services} scripts systemd logs

# Entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias en orden
pip install --upgrade pip setuptools wheel
pip install mysql-connector-python==8.1.0
pip install Pillow==10.1.0
pip install Flask==2.3.3 Werkzeug==2.3.7 Jinja2==3.1.2
pip install qrcode[pil]==7.4.2
pip install python-dotenv==1.0.0

echo "✅ Instalación completada"
echo "➡️  Ahora ejecuta: cd ~/QR_Access_PRO && source venv/bin/activate && python test_system.py"
