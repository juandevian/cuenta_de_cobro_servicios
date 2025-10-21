#!/bin/bash
# Script de desarrollo para Git Bash en Windows

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para activar entorno virtual
activate_venv() {
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}Creando entorno virtual...${NC}"
        python -m venv .venv
    fi
    
    # Activar entorno virtual en Git Bash
    source .venv/Scripts/activate
}

# Función para instalar dependencias
install_deps() {
    echo -e "${YELLOW}Instalando dependencias...${NC}"
    python -m pip install --upgrade pip
    pip install -e .
    echo -e "${GREEN}✓ Dependencias instaladas${NC}"
}

# Función para ejecutar tests
run_tests() {
    echo -e "${YELLOW}Ejecutando tests...${NC}"
    pytest
}

# Función para ejecutar la aplicación
run_app() {
    echo -e "${YELLOW}Ejecutando aplicación...${NC}"
    
    # Cargar variables de entorno si existe .env.development
    if [ -f ".env.development" ]; then
        export $(grep -v '^#' .env.development | xargs)
        # Reemplazar ${PWD} con el directorio actual
        export PYTHONPATH="${PYTHONPATH/\$\{PWD\}/$(pwd)}"
    fi
    
    python -m src.main
}

# Menú principal
case "$1" in
    install)
        activate_venv
        install_deps
        ;;
    test)
        activate_venv
        run_tests
        ;;
    run)
        activate_venv
        run_app
        ;;
    *)
        echo -e "${YELLOW}Uso:${NC}"
        echo "  ./dev.sh install  # Instalar dependencias"
        echo "  ./dev.sh test     # Ejecutar tests"
        echo "  ./dev.sh run      # Ejecutar aplicación"
        ;;
esac
