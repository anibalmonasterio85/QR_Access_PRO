#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   QR Access Control - Panel Web   ${NC}"
echo -e "${GREEN}========================================${NC}"

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Creando entorno virtual...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Archivo .env no encontrado${NC}"
    exit 1
fi

echo -e "${YELLOW}🔍 Verificando base de datos...${NC}"
python -c "from config.database import test_connection; test_connection()" || exit 1

echo -e "${GREEN}✅ Todo listo${NC}"
echo -e "${GREEN}🚀 Servidor en http://localhost:5000${NC}"
echo -e "${YELLOW}Presiona Ctrl+C para detener${NC}\n"

python web_panel/app.py
