#!/bin/bash
# ===========================================
# QR Access Control - Script de Estado
# ===========================================

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_DIR="/home/admin/QR_Access_PRO"
PID_FILE="$PROJECT_DIR/web_panel.pid"
LOG_DIR="$PROJECT_DIR/logs"
PORT=5000

echo -e "${BLUE}========================================${NC}"
echo -e "${CYAN}   QR ACCESS CONTROL - ESTADO   ${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Verificar proceso por PID
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 $PID 2>/dev/null; then
        echo -e "${GREEN}✅ PROCESO ACTIVO (PID: $PID)${NC}"
        
        # Uptime
        UPTIME=$(ps -o etimes= -p $PID | xargs)
        UPTIME_HUMAN=$(printf '%02d:%02d:%02d' $((UPTIME/3600)) $((UPTIME%3600/60)) $((UPTIME%60)))
        echo -e "   Uptime: $UPTIME_HUMAN"
        
        # CPU y memoria
        PS_OUTPUT=$(ps -o %cpu,%mem,cmd -p $PID | tail -n1)
        CPU=$(echo $PS_OUTPUT | awk '{print $1}')
        MEM=$(echo $PS_OUTPUT | awk '{print $2}')
        echo -e "   CPU: $CPU% | MEM: $MEM%"
    else
        echo -e "${RED}❌ PID file existe pero proceso no corre${NC}"
        rm -f "$PID_FILE"
    fi
else
    echo -e "${YELLOW}⚠️  No hay PID file${NC}"
fi

# Verificar puerto
echo -e "\n${CYAN}🔍 Puerto $PORT:${NC}"
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    PIDS=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
    echo -e "${GREEN}✅ Puerto $PORT en uso por PIDs: $PIDS${NC}"
else
    echo -e "${RED}❌ Puerto $PORT libre${NC}"
fi

# Verificar procesos por nombre
echo -e "\n${CYAN}🔍 Procesos Python:${NC}"
PYS=$(pgrep -f "python.*web_panel/app.py")
if [ ! -z "$PYS" ]; then
    for PID in $PYS; do
        echo -e "${GREEN}✅ Python PID: $PID${NC}"
    done
else
    echo -e "${RED}❌ No hay procesos Python del panel${NC}"
fi

# Últimos logs
echo -e "\n${CYAN}📝 Últimos logs:${NC}"
if [ -f "$LOG_DIR/web_panel.log" ]; then
    tail -n 5 "$LOG_DIR/web_panel.log"
    echo -e "\n${YELLOW}Log completo: $LOG_DIR/web_panel.log${NC}"
else
    echo -e "${RED}No hay archivo de log${NC}"
fi

# Base de datos
echo -e "\n${CYAN}🗄️  Base de datos:${NC}"
DB_SIZE=$(mysql -u flaskuser -pflask123 -e "SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) FROM information_schema.tables WHERE table_schema='qr_access';" 2>/dev/null | tail -n1)
USER_COUNT=$(mysql -u flaskuser -pflask123 -e "SELECT COUNT(*) FROM qr_access.usuarios;" 2>/dev/null | tail -n1)
echo -e "   Tamaño: ${DB_SIZE:-0} MB"
echo -e "   Usuarios: ${USER_COUNT:-0}"

echo -e "\n${BLUE}========================================${NC}"
echo -e "${YELLOW}Comandos útiles:${NC}"
echo -e "  ./start.sh    - Iniciar sistema"
echo -e "  ./stop.sh     - Detener sistema"
echo -e "  ./restart.sh  - Reiniciar sistema"
echo -e "  tail -f logs/web_panel.log - Ver logs en tiempo real"
echo -e "${BLUE}========================================${NC}"
