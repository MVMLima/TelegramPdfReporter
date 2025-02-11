import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)
from hospital_parser import HospitalDataParser
from pdf_generator import PDFGenerator
from email_sender import EmailSender
from config import BOT_TOKEN
import traceback
import re

# Update logging section to be more verbose
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

class HospitalBot:
    def __init__(self):
        self.parser = HospitalDataParser()
        self.pdf_generator = PDFGenerator()
        self.email_sender = EmailSender()
        self.user_templates = {}
        self.user_reports = {}  # Store generated reports temporarily
        logger.info("HospitalBot initialized")

    async def start(self, update: Update, context: CallbackContext):
        """Handle /start command."""
        logger.info(f"Start command received from user {update.effective_user.id}")
        welcome_message = (
            "👋 Olá! Eu sou o bot de relatórios hospitalares.\n\n"
            "Envie uma mensagem com os dados de ocupação hospitalar e "
            "eu irei gerar um relatório PDF formatado.\n\n"
            "Comandos disponíveis:\n"
            "/template - Lista e seleciona modelos de relatório\n"
            "/help - Mostra instruções detalhadas\n"
            "/share - Compartilha o último relatório por email"
        )
        await update.message.reply_text(welcome_message)

    async def help(self, update: Update, context: CallbackContext):
        """Handle /help command."""
        help_message = (
            "📋 Instruções de uso:\n\n"
            "1. Envie uma mensagem com os dados hospitalares\n"
            "2. Aguarde o processamento\n"
            "3. Receba o relatório em PDF\n"
            "4. Use /share para compartilhar o relatório por email\n\n"
            "A mensagem deve conter:\n"
            "- Nome do hospital\n"
            "- Dados de ocupação por unidade\n"
            "- Taxas de ocupação\n\n"
            "Exemplo de formato:\n"
            "UTI 1 (17 leitos) - 94,11%\n"
            "UTI 2 (10 leitos) - 80,00%\n"
            "...\n\n"
            "Comandos:\n"
            "/template - Gerencia modelos de relatório\n"
            "/template list - Lista modelos disponíveis\n"
            "/template set <nome> - Define modelo padrão\n"
            "/share <email> - Compartilha o último relatório por email"
        )
        await update.message.reply_text(help_message)

    async def share_report(self, update: Update, context: CallbackContext):
        """Handle /share command to share the latest report via email."""
        user_id = str(update.effective_user.id)

        if user_id not in self.user_reports:
            await update.message.reply_text(
                "❌ Nenhum relatório disponível para compartilhar. "
                "Por favor, gere um relatório primeiro."
            )
            return

        # Check if email was provided
        if not context.args:
            await update.message.reply_text(
                "Por favor, forneça um endereço de email após o comando.\n"
                "Exemplo: /share email@exemplo.com"
            )
            return

        email = context.args[0]
        # Basic email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            await update.message.reply_text("❌ Endereço de email inválido.")
            return

        pdf_data = self.user_reports[user_id]

        # Send processing message
        processing_msg = await update.message.reply_text(
            "🔄 Enviando relatório por email... Por favor, aguarde."
        )

        if self.email_sender.send_report(email, pdf_data):
            await processing_msg.edit_text(
                "✅ Relatório enviado com sucesso para " + email
            )
        else:
            await processing_msg.edit_text(
                "❌ Erro ao enviar o relatório. Por favor, tente novamente."
            )

    async def process_message(self, update: Update, context: CallbackContext):
        """Process incoming messages and generate PDF reports."""
        try:
            logger.info(f"Processing message from user {update.effective_user.id}")
            logger.debug(f"Message content: {update.message.text[:100]}...")

            # Send processing message
            processing_message = await update.message.reply_text(
                "🔄 Processando sua mensagem... Por favor, aguarde."
            )

            # Parse message
            logger.info("Attempting to parse message...")
            data = self.parser.parse_message(update.message.text)
            logger.info(f"Message parsed successfully. Data structure: {data.keys()}")
            logger.info(f"Number of units: {len(data.get('units', []))}")

            if not self.parser.validate_data(data):
                logger.warning("Invalid message format")
                await processing_message.edit_text(
                    "❌ Erro: Formato da mensagem inválido. "
                    "Certifique-se de que a mensagem está no formato correto."
                )
                return

            # Generate PDF
            logger.info("Starting PDF generation with data:")
            pdf_buffer = self.pdf_generator.generate_pdf(data,
                self.user_templates.get(str(update.effective_user.id)))

            # Store the PDF data for sharing
            self.user_reports[str(update.effective_user.id)] = pdf_buffer.getvalue()

            # Send PDF
            logger.info("Sending PDF to user...")
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=pdf_buffer,
                filename='relatorio_hospitalar.pdf',
                caption=(
                    "📊 Aqui está seu relatório de ocupação hospitalar.\n"
                    "Use /share email@exemplo.com para compartilhar por email."
                )
            )
            logger.info("PDF sent successfully")

            # Delete processing message
            await processing_message.delete()

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            logger.error(traceback.format_exc())
            error_message = (
                "❌ Ocorreu um erro ao processar sua mensagem.\n"
                "Por favor, verifique se o formato está correto e tente novamente."
            )
            await update.message.reply_text(error_message)

    async def handle_template(self, update: Update, context: CallbackContext):
        """Handle /template command."""
        if not context.args:
            templates = self.pdf_generator.list_templates()
            message = "📋 Modelos disponíveis:\n\n"
            for name, desc in templates.items():
                message += f"• {name}: {desc}\n"
            message += "\nUse /template set <nome> para selecionar um modelo"
            await update.message.reply_text(message)
            return

        command = context.args[0].lower()
        if command == "list":
            templates = self.pdf_generator.list_templates()
            message = "📋 Modelos disponíveis:\n\n"
            for name, desc in templates.items():
                message += f"• {name}: {desc}\n"
            await update.message.reply_text(message)

        elif command == "set" and len(context.args) > 1:
            template_name = context.args[1]
            user_id = str(update.effective_user.id)
            if self.pdf_generator.set_default_template(template_name):
                self.user_templates[user_id] = template_name
                await update.message.reply_text(f"✅ Modelo '{template_name}' selecionado com sucesso!")
            else:
                await update.message.reply_text(f"❌ Modelo '{template_name}' não encontrado.")

def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Create bot instance
    hospital_bot = HospitalBot()

    # Add handlers
    application.add_handler(CommandHandler("start", hospital_bot.start))
    application.add_handler(CommandHandler("help", hospital_bot.help))
    application.add_handler(CommandHandler("template", hospital_bot.handle_template))
    application.add_handler(CommandHandler("share", hospital_bot.share_report))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        hospital_bot.process_message
    ))

    # Start bot
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == '__main__':
    main()