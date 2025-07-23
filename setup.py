#!/usr/bin/env python3
"""
UNITED HUB - Script de Configuração Automática
"""

import os
import sys
import subprocess

def instalar_dependencias():
    """Instala todas as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def criar_env_exemplo():
    """Cria arquivo .env de exemplo"""
    env_content = """# UNITED HUB - Configuração de Ambiente

# Banco de dados PostgreSQL (OBRIGATÓRIO)
DATABASE_URL=postgresql://usuario:senha@localhost:5432/united_hub

# Chave secreta para sessões Flask
SESSION_SECRET=minha-chave-secreta-super-segura-123

# Chave da API para Discord Bot
API_SECRET_KEY=minha-api-key-discord-bot

# Discord Webhooks
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/SEU_WEBHOOK_CHAT_GERAL
VERIFICACAO_CORRETA_WEBHOOK=https://discord.com/api/webhooks/SEU_WEBHOOK_CORRETO  
VERIFICACAO_ERRO_WEBHOOK=https://discord.com/api/webhooks/SEU_WEBHOOK_ERRO

# Webhooks adicionais (opcionais)
KEY_GENERATOR_WEBHOOK_URL=https://discord.com/api/webhooks/SEU_WEBHOOK_KEYS
DM_NOTIFICATION_WEBHOOK_URL=https://discord.com/api/webhooks/SEU_WEBHOOK_DM
"""
    
    with open(".env.exemplo", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("📝 Arquivo .env.exemplo criado!")
    print("   Renomeie para .env e configure suas URLs")

def main():
    print("🚀 UNITED HUB - Configuração Automática")
    print("=" * 50)
    
    # Verificar se está no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script na pasta do UNITED HUB")
        sys.exit(1)
    
    # Instalar dependências
    if not instalar_dependencias():
        sys.exit(1)
    
    # Criar arquivo de exemplo
    criar_env_exemplo()
    
    print("\n✅ Configuração concluída!")
    print("\n📋 Próximos passos:")
    print("1. Configure seu banco PostgreSQL")
    print("2. Renomeie .env.exemplo para .env")
    print("3. Configure seus webhooks Discord")
    print("4. Execute: python run.py")
    print("\n🎯 Sistema estará em: http://localhost:5000")

if __name__ == "__main__":
    main()