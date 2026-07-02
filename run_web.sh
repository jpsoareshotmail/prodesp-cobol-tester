#!/bin/bash
# Script para iniciar a interface web de testes

echo "========================================"
echo "Sistema de Testes COBOL - Interface Web"
echo "========================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não encontrado!"
    echo "Instale Python 3 de: https://www.python.org/"
    exit 1
fi

# Verificar/criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "[*] Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "[*] Ativando ambiente virtual..."
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

# Instalar dependências
echo "[*] Instalando dependências..."
pip install -q -r requirements.txt

# Iniciar servidor
echo ""
echo "✓ Ambiente pronto!"
echo ""
echo "========================================"
echo "🌐 Abrindo interface web..."
echo "========================================"
echo ""
echo "URL: http://localhost:5000"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

# Abrir navegador automaticamente
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000 &
elif command -v open &> /dev/null; then
    open http://localhost:5000 &
elif command -v start &> /dev/null; then
    start http://localhost:5000 &
fi

# Iniciar servidor Flask
python3 web_app.py
