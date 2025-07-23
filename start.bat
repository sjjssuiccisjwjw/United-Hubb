@echo off
echo ========================================
echo    UNITED HUB - Sistema de Monitoramento
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ primeiro
    pause
    exit /b 1
)

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando UNITED HUB...
echo Acesse: http://localhost:5000
echo.

python run.py

pause