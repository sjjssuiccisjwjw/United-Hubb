# 🔑 UNITED HUB - Sistema Completo de Monitoramento

## ✅ STATUS: FUNCIONANDO PERFEITAMENTE

Sistema Flask completo para monitoramento de IP e verificação de keys com integração Discord/Roblox.

### 🌐 Funcionalidades Principais

#### 1. **Sistema de Verificação de Keys**
- ✅ **Key MASTER**: `SEMNEXO134` (sempre aceita)
- ✅ Keys do banco de dados com expiração de 24h
- ✅ Interface web responsiva com Bootstrap
- ✅ Feedback visual: verde para sucesso, vermelho para falha
- ✅ Todas as tentativas são logadas no Discord

#### 2. **Monitoramento Completo de Acesso** 
- ✅ Detecta quando alguém acessa o site
- ✅ **Localização DETALHADA**: Cidade, Estado, País, CEP, Coordenadas GPS
- ✅ **ISP/Provedor**: Nome do provedor, organização, AS Network
- ✅ **Device Info**: Sistema, navegador, tipo, fingerprint único
- ✅ Sistema anti-spam: máximo 1 notificação por IP a cada 5 minutos

#### 3. **API Segura para Discord Bot**
- ✅ Endpoint: `/api/generate-private-key`
- ✅ Autenticação: `Bearer your-secret-api-key-here`
- ✅ Keys únicas de 16 caracteres
- ✅ Expiração automática: 24 horas

#### 4. **Integração Roblox Completa**
- ✅ Endpoint: `/api/roblox-execution`
- ✅ **Dados do Jogador**: Nome, ID, idade da conta, membership
- ✅ **Dados do Jogo**: ID, nome, server, região
- ✅ **Hardware/Performance**: Plataforma, dispositivos, qualidade gráfica
- ✅ **Localização**: Mesmos dados detalhados do site

### 🚀 Como Usar

#### Para Deploy no Replit:
1. Clone este repositório
2. Configure as variáveis de ambiente:
   - `DATABASE_URL`: PostgreSQL database URL
   - `SESSION_SECRET`: Chave secreta para sessões
   - `API_SECRET_KEY`: Chave para API do Discord bot
3. Execute: `python main.py`
4. Acesse via porta 5000

#### Para Usuários:
1. **Verificação**: Acesse `/` e digite sua key
2. **Gerar key pública**: Acesse `/generate-key`
3. **Admin panel**: Acesse `/admin`

#### Para Discord Bot:
1. Configure o bot usando `discord_bot_example.py`
2. Use comando `/gerarkey` no canal #keys
3. Keys são enviadas por DM

#### Para Roblox:
1. Use o script `roblox_tracker.lua`
2. Comando: `loadstring(game:HttpGet("SUA_URL_GITHUB"))()` 
3. Dados são enviados automaticamente para Discord

### 📊 Webhooks Discord Organizados

1. **Chat Geral**: Notificações de acesso ao site (quem visitou)
2. **verificação-correta**: Quando alguém acerta a senha
3. **verificação-erro**: Quando alguém erra a senha
4. **Key Generator**: Notificações de keys públicas geradas
5. **DM Notifications**: Notificações privadas para admins

### 🔒 Segurança

- ✅ Keys expiran automaticamente (24h)
- ✅ API protegida com Bearer token
- ✅ Sistema anti-spam implementado
- ✅ Logs completos para auditoria
- ✅ Nunca mostra keys capturadas para usuários

### 📱 Tecnologias Usadas

**Backend:**
- Flask (Python web framework)
- SQLAlchemy (ORM database)
- PostgreSQL (Database)
- Requests (HTTP client)
- User-Agents (Device detection)

**Frontend:**
- Bootstrap 5 (CSS framework)
- Font Awesome (Icons)
- Vanilla JavaScript
- Responsive design

**APIs Externas:**
- IP-API (Geolocalização)
- IPInfo (Geolocalização backup)
- Discord Webhooks (Notificações)

### 🌍 Dados Coletados

**Localização:**
- IP público real
- Cidade, Estado, País
- CEP/Código postal
- Coordenadas GPS (lat/long)
- Timezone
- ISP/Provedor
- Organização
- AS Network

**Dispositivo:**
- Sistema operacional + versão
- Navegador + versão
- Tipo de dispositivo (Desktop/Mobile/Tablet)
- Device fingerprint único
- Idioma do navegador
- Headers HTTP importantes

**Roblox (adicional):**
- Dados do jogador (nome, ID, idade da conta)
- Informações do jogo (ID, nome, server)
- Hardware (plataforma, dispositivos de entrada)
- Performance (qualidade gráfica, uso de memória)

### ⚡ Features Especiais

- **Interface Dark Theme**: Design moderno e responsivo
- **Real-time Monitoring**: Notificações instantâneas no Discord
- **Anti-Spam System**: Cooldown de 5 minutos por IP
- **Multiple API Fallback**: Máxima precisão de geolocalização
- **Automatic Cleanup**: Remoção automática de keys expiradas
- **Admin Dashboard**: Painel completo para gestão de keys
- **Bot Integration**: Sistema completo de Discord bot
- **Roblox Tracking**: Monitoramento completo de execuções

### 📞 Suporte

Sistema 100% funcional e testado. Para dúvidas sobre configuração, consulte os arquivos de documentação incluídos.

---

**🎉 SISTEMA PRONTO PARA PRODUÇÃO!**
