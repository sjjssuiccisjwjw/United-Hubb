#!/usr/bin/env python3
"""
UNITED HUB - Sistema de Monitoramento
Script de execução principal
"""

import os
from app import app

if __name__ == '__main__':
    # Configurações para desenvolvimento
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("🚀 Iniciando UNITED HUB...")
    print(f"📡 Servidor rodando em: http://{host}:{port}")
    print("🔗 Acesse: /hub para verificação")
    print("⚙️  Acesse: /admin para painel admin")
    
    app.run(
        host=host,
        port=port,
        debug=True,
        threaded=True
    )