git clone https://github.com/seu-usuario/hospital-report-bot.git
cd hospital-report-bot
```

2. Execute o script de instalação:
```bash
chmod +x setup.sh
./setup.sh
```

3. Configure as variáveis de ambiente:
   Edite o arquivo `.env` criado na raiz do projeto:

```env
BOT_TOKEN=seu_token_do_telegram_bot
SENDGRID_API_KEY=sua_chave_api_do_sendgrid
SENDER_EMAIL=seu_email_remetente@dominio.com
```

## Arquivos de Logo

O projeto utiliza dois arquivos de logo para os relatórios PDF:

1. Crie a pasta `attached_assets` na raiz do projeto:
```bash
mkdir -p attached_assets
```

2. Adicione seus arquivos de logo na pasta:
- `attached_assets/image_1739196996707.png` (logo do cabeçalho)
- `attached_assets/image_1739197036571.png` (logo do rodapé)

Nota: O sistema funcionará mesmo sem os arquivos de logo, mas os relatórios não incluirão as imagens.

## Como Obter as Credenciais

### Token do Bot Telegram:
1. Abra o Telegram e procure por [@BotFather](https://t.me/BotFather)
2. Envie o comando `/newbot`
3. Siga as instruções para criar seu bot
4. Copie o token fornecido para o arquivo `.env`

### SendGrid API Key:
1. Crie uma conta no [SendGrid](https://signup.sendgrid.com/)
2. Acesse Settings > API Keys
3. Crie uma nova API key
4. Copie a chave fornecida para o arquivo `.env`

## Executando o Bot

1. Ative o ambiente virtual:
```bash
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

2. Execute o bot:
```bash
python bot.py
```

3. No Telegram, inicie uma conversa com seu bot e envie o comando `/start`

## Formato da Mensagem

Envie mensagens no seguinte formato:
```
UTI 1 (17 leitos) - 94,11%
UTI 2 (10 leitos) - 80,00%
UTI INTO (17 leitos) - 64,70%
...
```

## Comandos Disponíveis

- `/start` - Inicia o bot
- `/help` - Mostra instruções detalhadas
- `/template` - Lista e seleciona modelos de relatório
- `/share` - Compartilha o último relatório por email

## Estrutura do Projeto

```
├── attached_assets/      # Logos e imagens
├── templates/           # Templates para geração de PDF
├── bot.py              # Código principal do bot
├── config.py           # Configurações do projeto
├── email_sender.py     # Módulo de envio de email
├── hospital_parser.py  # Parser de mensagens
└── pdf_generator.py    # Gerador de PDF
```

## Testes

Execute os testes para verificar se tudo está funcionando corretamente:
```bash
python test_parser.py  # Testa o parser de mensagens
python test_pdf.py     # Testa a geração de PDF