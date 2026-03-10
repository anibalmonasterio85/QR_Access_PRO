# stop.ps1
# Script para apagar el Panel Web de QR_Access_PRO

Write-Host "Deteniendo el Servidor Web QR Access PRO..." -ForegroundColor Yellow

# Buscar todos los procesos de python corriendo waitress_server.py y terminarlos
Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -match 'waitress_server.py' } | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force
}

Write-Host "Servidor Web Apagado." -ForegroundColor Green
