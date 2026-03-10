#!/bin/bash
# ===========================================
# QR Access Control - Script de Reinicio
# ===========================================

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}   QR ACCESS CONTROL - REINICIANDO   ${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Detener
echo -e "${YELLOW}🛑 Deteniendo sistema...${NC}"
./stop.sh

# Esperar
echo -e "\n${YELLOW}⏳ Esperando 3 segundos...${NC}"
sleep 3

# Iniciar
echo -e "\n${GREEN}🚀 Iniciando sistema...${NC}"
./start.sh
