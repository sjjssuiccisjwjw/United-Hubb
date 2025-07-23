#!/bin/bash

echo "========================================"
echo "   UNITED HUB - Sistema de Monitoramento"
echo "========================================"
echo

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "Instale Python 3.8+ primeiro"
    exit 1
fi

echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

echo
echo "🚀 Iniciando UNITED HUB..."
echo "🔗 Acesse: http://localhost:5000"
echo

python3 run.py