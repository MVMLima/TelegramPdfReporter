import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram import Update
from hospital_parser import HospitalDataParser
from pdf_generator import PDFGenerator
from config import BOT_TOKEN
import traceback

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class HospitalBot:
    def __init__(self):
        self.parser = HospitalDataParser()
        self.pdf_generator = PDFGenerator()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = (
            "👋 Olá! Eu sou o bot de relatórios hospitalares.\n\n"
            "Envie uma mensagem com os dados de ocupação hospitalar e "
            "eu irei gerar um relatório PDF formatado.\n\n"
            "A mensagem deve conter os dados de ocupação no formato padrão."
        )
        await update.message.reply_text(welcome_message)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = (
            "📋 Instruções de uso:\n\n"
            "1. Envie uma mensagem com os dados hospitalares\n"
            "2. Aguarde o processamento\n"
            "3. Receba o relatório em PDF\n\n"
            "A mensagem deve conter:\n"
            "- Nome do hospital\n"
            "- Dados de ocupação por unidade\n"
            "- Taxas de ocupação"
        )
        await update.message.reply_text(help_message)

    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process incoming messages and generate PDF reports."""
        try:
            # Send processing message
            processing_message = await update.message.reply_text(
                "🔄 Processando sua mensagem... Por favor, aguarde."
            )

            # Parse message
            data = self.parser.parse_message(update.message.text)

            if not self.parser.validate_data(data):
                await processing_message.edit_text(
                    "❌ Erro: Formato da mensagem inválido. "
                    "Certifique-se de que a mensagem está no formato correto."
                )
                return

            # Generate PDF
            pdf_buffer = self.pdf_generator.generate_pdf(data)

            # Send PDF
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=pdf_buffer,
                filename='relatorio_hospitalar.pdf',
                caption="📊 Aqui está seu relatório de ocupação hospitalar."
            )

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

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update:
        await update.message.reply_text(
            "❌ Ocorreu um erro inesperado. Por favor, tente novamente mais tarde."
        )

def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Create bot instance
    hospital_bot = HospitalBot()

    # Add handlers
    application.add_handler(CommandHandler("start", hospital_bot.start))
    application.add_handler(CommandHandler("help", hospital_bot.help))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        hospital_bot.process_message
    ))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start bot
    application.run_polling()

if __name__ == '__main__':
    main()