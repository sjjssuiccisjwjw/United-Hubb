# UNITED HUB - Sistema Completo de Monitoramento

## Overview

This is a comprehensive Flask-based monitoring and verification system designed for Discord integration and Roblox script management. The application serves as both an IP monitoring system and a secure key verification platform, providing detailed tracking of user access and device information with real-time Discord notifications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework) with ProxyFix middleware for reverse proxy environments
- **Database**: PostgreSQL with SQLAlchemy ORM for key management and expiration tracking
- **Session Management**: Flask's built-in session handling with configurable secret keys
- **API Security**: Bearer token authentication for private API endpoints
- **Logging**: Python's built-in logging module with comprehensive error tracking

### Frontend Architecture
- **Template Engine**: Jinja2 with responsive HTML templates
- **CSS Framework**: Bootstrap 5 with custom dark theme styling
- **Icons**: Font Awesome 6.0.0 for consistent UI elements
- **Responsive Design**: Mobile-first approach with fluid container layouts

## Key Components

### Core Application (app.py)
- **Multi-Service Monitoring**: Combines IP logging, geolocation tracking, and key verification
- **Discord Integration**: Multiple webhook endpoints for different notification types
- **Geolocation Services**: Integration with multiple IP APIs (ipapi.co, IPInfo) for location accuracy
- **Device Detection**: Advanced user-agent parsing for OS, browser, and device identification
- **Anti-Spam System**: Rate limiting with 5-minute cooldown periods per IP address
- **Key Management**: Automated 24-hour expiration system with unique key generation
- **Roblox Integration**: Dedicated API endpoint for receiving Lua script data

### Database Models (models.py)
- **PrivateKey Model**: Stores generated keys with user association and expiration timestamps
- **Automatic Cleanup**: Built-in expiration checking and validation methods

### Templates System
- **hub.html**: Clean verification interface for key input
- **verified.html**: Success confirmation page with animated feedback
- **denied.html**: Error handling page with troubleshooting guidance
- **admin.html**: Administrative dashboard for key management
- **index.html**: Main landing page with system overview

## Data Flow

### User Access Monitoring
1. User visits any page → IP detection and geolocation lookup
2. Device fingerprinting and user-agent analysis
3. Anti-spam check (5-minute cooldown per IP)
4. Discord webhook notification with comprehensive data package
5. Session tracking and logging

### Key Verification Process
1. User submits key via web form
2. Master key check (`SEMNEXO134`) or database validation
3. Expiration verification for database keys
4. Discord logging of verification attempts
5. Redirect to success or denial page

### Private Key Generation
1. Discord bot or API client sends authenticated request
2. Bearer token validation against configured secret
3. Unique 16-character key generation
4. Database storage with 24-hour expiration
5. Webhook notification to key generator channel

## External Dependencies

### Third-Party Services
- **Discord Webhooks**: Five separate endpoints organized by function:
  - Chat Geral: Site access notifications (who visited)
  - verificação-correta: Successful key verification attempts
  - verificação-erro: Failed key verification attempts  
  - Key Generator: Public key generation notifications
  - DM Notifications: Private admin notifications
- **IP Geolocation APIs**: ipapi.co and IPInfo for location data
- **PostgreSQL**: Database hosting (configured via DATABASE_URL environment variable)

### Python Packages
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and management
- **user-agents**: Device and browser detection
- **requests**: HTTP client for external API calls
- **werkzeug**: WSGI utilities and proxy handling

### Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework from CDN
- **Font Awesome 6.0.0**: Icon library from CDN
- **Custom CSS**: Dark theme styling in static/style.css

## Deployment Strategy

### Environment Configuration
- **DATABASE_URL**: PostgreSQL connection string (required)
- **SESSION_SECRET**: Flask session encryption key (fallback to dev key)
- **API_SECRET_KEY**: Bearer token for API authentication (fallback to default)
- **DISCORD_WEBHOOK_URL**: Main webhook endpoint (hardcoded with fallback)

### Replit Deployment
- **Host Binding**: Configured for 0.0.0.0:5000 for external access
- **Proxy Configuration**: ProxyFix middleware for proper IP detection behind Replit's proxy
- **Debug Mode**: Enabled for development environment
- **Database Initialization**: Automatic table creation on first run

### Security Considerations
- **API Authentication**: Bearer token protection for sensitive endpoints
- **Rate Limiting**: Built-in anti-spam protection with IP-based cooldowns
- **Session Security**: Configurable secret keys for session encryption
- **Input Validation**: Form validation and sanitization for key verification

### Monitoring and Logging
- **Comprehensive Logging**: All access attempts, verification tries, and errors logged
- **Discord Integration**: Real-time notifications for all system events
- **Error Handling**: Graceful fallbacks for external service failures
- **Database Health**: Connection pooling and automatic reconnection handling