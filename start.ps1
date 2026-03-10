# start.ps1
# Script para encender el Panel Web de QR_Access_PRO en modo Produccion

Write-Host "Iniciando Servidor Web QR Access PRO..." -ForegroundColor Green
Write-Host "Cargando Entorno Virtual y Waitress..." -ForegroundColor Cyan

# Ejecutar el servidor con el python de venv para que las variables y modulos carguen
.\venv\Scripts\python.exe waitress_server.py
