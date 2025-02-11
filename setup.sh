#!/bin/bash

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install python-telegram-bot telegram reportlab sendgrid

# Criar diretório para assets
mkdir -p attached_assets
echo "✅ Diretório attached_assets criado"

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "BOT_TOKEN=seu_token_do_telegram_bot
SENDGRID_API_KEY=sua_chave_api_do_sendgrid
SENDER_EMAIL=seu_email_remetente@dominio.com" > .env
    echo "Arquivo .env criado! Por favor, edite-o com suas credenciais."
fi

echo "✅ Instalação concluída!"
echo "⚠️  Importante: Edite o arquivo .env com suas credenciais antes de executar o bot."
echo "⚠️  Importante: Adicione os arquivos de logo na pasta attached_assets (opcional)"
echo "📝 Para mais informações, consulte o README.md"