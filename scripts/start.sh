#!/bin/bash
# ===========================================
# QR Access Control - Script de Inicio CORREGIDO
# ===========================================

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_DIR="/home/admin/QR_Access_PRO"
LOG_DIR="$PROJECT_DIR/logs"
PID_FILE="$PROJECT_DIR/web_panel.pid"
PORT=5000

mkdir -p "$LOG_DIR"

show_banner() {
    clear
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}   QR ACCESS CONTROL - PANEL WEB   ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "${CYAN}   Sistema Profesional de Control de Acceso${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Matar procesos existentes
clean_processes() {
    echo -e "${YELLOW}🧹 Limpiando procesos existentes...${NC}"
    
    # Matar por PID file
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if kill -0 $OLD_PID 2>/dev/null; then
            echo -e "   Deteniendo PID $OLD_PID"
            kill $OLD_PID 2>/dev/null
            sleep 1
        fi
        rm -f "$PID_FILE"
    fi
    
    # Matar por puerto
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "   Liberando puerto $PORT"
        fuser -k $PORT/tcp 2>/dev/null
        sleep 1
    fi
    
    # Matar procesos Python
    PIDS=$(pgrep -f "python.*web_panel/app.py")
    if [ ! -z "$PIDS" ]; then
        echo -e "   Deteniendo procesos Python: $PIDS"
        kill $PIDS 2>/dev/null
        sleep 2
    fi
    
    echo -e "${GREEN}✅ Procesos limpiados${NC}"
}

check_database() {
    echo -e "${YELLOW}🔍 Verificando base de datos...${NC}"
    
    source "$PROJECT_DIR/venv/bin/activate"
    python -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')
from config.database import test_connection
if not test_connection():
    sys.exit(1)
" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Base de datos OK${NC}"
    else
        echo -e "${RED}❌ Error en base de datos${NC}"
        exit 1
    fi
}

start_server() {
    echo -e "${YELLOW}🚀 Iniciando servidor web en puerto $PORT...${NC}"
    
    cd "$PROJECT_DIR"
    source venv/bin/activate
    export PYTHONPATH="${PYTHONPATH}:$PROJECT_DIR"
    
    # Iniciar y capturar PID
    nohup python web_panel/app.py > "$LOG_DIR/web_panel.log" 2>&1 &
    echo $! > "$PID_FILE"
    
    # Esperar a que inicie
    echo -e "   Esperando 3 segundos..."
    sleep 3
    
    # Verificar
    if kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo -e "${GREEN}✅ Servidor iniciado (PID: $(cat "$PID_FILE"))${NC}"
        
        IP=$(hostname -I | awk '{print $1}')
        echo -e "${GREEN}📱 URL: http://$IP:$PORT${NC}"
        echo -e "${GREEN}📱 Local: http://localhost:$PORT${NC}"
        
        echo -e "\n${CYAN}📝 Últimos logs:${NC}"
        tail -n 5 "$LOG_DIR/web_panel.log"
        echo -e "\n${YELLOW}Logs: tail -f $LOG_DIR/web_panel.log${NC}"
    else
        echo -e "${RED}❌ Error al iniciar servidor${NC}"
        cat "$LOG_DIR/web_panel.log"
        exit 1
    fi
}

# Main
show_banner
clean_processes
check_database
start_server

echo -e "\n${GREEN}✨ Sistema listo!${NC}"
echo -e "${YELLOW}Para detener: ./stop.sh${NC}"
