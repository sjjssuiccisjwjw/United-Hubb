# 🚀 UNITED HUB - Guia de Instalação Completa

## 📋 Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL (banco de dados)
- Conta Discord (para webhooks)

## 🔧 Instalação

### 1. Instalar dependências

```bash
pip install flask flask-sqlalchemy gunicorn psycopg2-binary requests user-agents werkzeug
```

### 2. Configurar Banco de Dados PostgreSQL

- Crie um banco PostgreSQL
- Anote a URL de conexão (ex: `postgresql://usuario:senha@localhost:5432/united_hub`)

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` ou configure as seguintes variáveis:

```bash
# Banco de dados (OBRIGATÓRIO)
DATABASE_URL=postgresql://usuario:senha@localhost:5432/united_hub

# Chave secreta da sessão
SESSION_SECRET=sua-chave-secreta-aleatoria

# Chave da API para bot Discord
API_SECRET_KEY=sua-api-key-para-bot

# Discord Webhooks
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/SEU_WEBHOOK_CHAT_GERAL
VERIFICACAO_CORRETA_WEBHOOK=https://discord.com/api/webhooks/SEU_WEBHOOK_CORRETO
VERIFICACAO_ERRO_WEBHOOK=https://discord.com/api/webhooks/SEU_WEBHOOK_ERRO
```

### 4. Executar o Sistema

```bash
# Modo desenvolvimento
python main.py

# Modo produção
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## 🎯 URLs e Endpoints

- **Site Principal**: `http://localhost:5000/`
- **Verificação**: `http://localhost:5000/hub`
- **Admin Panel**: `http://localhost:5000/admin`
- **API Gerar Key**: `POST /api/generate-key`
- **API Roblox**: `POST /api/roblox-data`

## 📊 Funcionalidades

✅ **Monitoramento de IP** - Detecta e loga todos os acessos
✅ **Geolocalização** - Localização completa via APIs
✅ **Verificação de Keys** - Sistema de chaves com expiração
✅ **Discord Webhooks** - Notificações organizadas por canal
✅ **Admin Panel** - Gerenciamento de chaves
✅ **Bot Discord** - API para integração
✅ **Roblox Integration** - Endpoint para scripts Lua

## 🔑 Keys do Sistema

- **Master Key**: `SEMNEXO134` (sempre válida)
- **Keys Temporárias**: Geradas via API/Admin (24h de validade)

## 🎮 Discord Bot

Use o arquivo `discord_bot_example.py` como base para seu bot.

## 🎲 Roblox Integration

Use o arquivo `roblox_tracker.lua` no seu jogo Roblox.

## 🔒 Segurança

- Rate limiting automático (5 minutos por IP)
- Validação de tokens para API
- Criptografia de sessões
- Logs completos de acesso

## 📞 Suporte

Sistema desenvolvido para monitoramento completo com Discord/Roblox integration.

---
**UNITED HUB** - Sistema Completo de Monitoramento