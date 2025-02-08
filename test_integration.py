from bot import HospitalBot
import asyncio
from telegram import Update
from telegram.ext import CallbackContext

async def test_pdf_generation():
    """Test PDF generation through the bot's message processing."""
    bot = HospitalBot()
    
    # Simular uma mensagem com dados de teste
    test_message = """UTI - 80%
Enfermaria - 60%
Centro Cirúrgico - 45%"""
    
    class MockMessage:
        def __init__(self, text):
            self.text = text
            
        async def reply_text(self, text):
            print(f"Bot response: {text}")
    
    class MockUpdate:
        def __init__(self, message):
            self.message = message
            self.effective_chat = type('obj', (object,), {'id': 123456})
            self.effective_user = type('obj', (object,), {'id': 789012})
    
    try:
        # Criar mensagem e update simulados
        mock_message = MockMessage(test_message)
        mock_update = MockUpdate(mock_message)
        mock_context = None  # Context não é necessário para este teste
        
        # Processar mensagem
        await bot.process_message(mock_update, mock_context)
        print("Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return False

if __name__ == '__main__':
    asyncio.run(test_pdf_generation())
