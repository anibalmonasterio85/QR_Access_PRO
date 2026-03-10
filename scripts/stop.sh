#!/bin/bash
# ===========================================
# QR Access Control - Script de Apagado MEJORADO
# ===========================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="/home/admin/QR_Access_PRO"
PID_FILE="$PROJECT_DIR/web_panel.pid"
PORT=5000

echo -e "${BLUE}========================================${NC}"
echo -e "${RED}   QR ACCESS CONTROL - APAGANDO   ${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Función para detener todo
stop_everything() {
    local STOPPED=false
    
    # 1. Por PID file
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            echo -e "${YELLOW}Deteniendo PID $PID...${NC}"
            kill $PID 2>/dev/null
            sleep 2
            if ! kill -0 $PID 2>/dev/null; then
                echo -e "${GREEN}✅ PID $PID detenido${NC}"
                STOPPED=true
            fi
        fi
        rm -f "$PID_FILE"
    fi
    
    # 2. Por puerto
    PIDS=$(lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null)
    if [ ! -z "$PIDS" ]; then
        echo -e "${YELLOW}Deteniendo procesos en puerto $PORT: $PIDS${NC}"
        for PID in $PIDS; do
            kill $PID 2>/dev/null
        done
        sleep 2
        REMAINING=$(lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null)
        if [ -z "$REMAINING" ]; then
            echo -e "${GREEN}✅ Puerto $PORT liberado${NC}"
            STOPPED=true
        fi
    fi
    
    # 3. Por nombre
    PIDS=$(pgrep -f "python.*web_panel/app.py")
    if [ ! -z "$PIDS" ]; then
        echo -e "${YELLOW}Deteniendo procesos Python: $PIDS${NC}"
        kill $PIDS 2>/dev/null
        sleep 2
        STOPPED=true
    fi
    
    # 4. Forzar si es necesario
    PIDS=$(pgrep -f "python.*web_panel/app.py")
    if [ ! -z "$PIDS" ]; then
        echo -e "${RED}Forzando detención...${NC}"
        kill -9 $PIDS 2>/dev/null
        sleep 1
    fi
    
    if [ "$STOPPED" = true ]; then
        echo -e "${GREEN}✅ Sistema detenido${NC}"
    else
        echo -e "${YELLOW}⚠️  No había procesos del sistema${NC}"
    fi
}

# Ejecutar
stop_everything

# Verificación final
sleep 1
if pgrep -f "python.*web_panel/app.py" >/dev/null 2>&1; then
    echo -e "${RED}❌ Algunos procesos siguen activos${NC}"
    echo -e "${YELLOW}Ejecuta: sudo pkill -f web_panel/app.py${NC}"
else
    echo -e "${GREEN}✅ Todo detenido correctamente${NC}"
fi

echo -e "\n${BLUE}========================================${NC}"
