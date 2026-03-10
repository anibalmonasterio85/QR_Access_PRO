#!/bin/bash
BACKUP_DIR="/home/admin/QR_Access_PRO/backups"
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u flaskuser -pflask123 qr_access > $BACKUP_DIR/backup_$DATE.sql
echo "✅ Backup creado: $BACKUP_DIR/backup_$DATE.sql"
# Mantener solo últimos 7 backups
ls -t $BACKUP_DIR/backup_*.sql | tail -n +8 | xargs -r rm
