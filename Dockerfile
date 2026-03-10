# Usar imagen oficial de Python ligera
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=web_panel/app.py
ENV FLASK_ENV=production

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema requeridas para compilación y base de datos
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo fuente
COPY . .

# Exponer el puerto
EXPOSE 5000

# Comando para iniciar la aplicacion usando Waitress
CMD ["python", "waitress_server.py"]
