"""Module for handling email sending functionality."""
import os
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition

class EmailSender:
    """Handles email sending functionality using SendGrid."""
    
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        if not self.api_key:
            raise ValueError("SENDGRID_API_KEY não configurada")
        self.sg = SendGridAPIClient(self.api_key)
        self.from_email = os.getenv('SENDER_EMAIL', 'noreply@cieges.acre.gov.br')

    def send_report(self, to_email: str, pdf_data: bytes, filename: str = "relatorio_hospitalar.pdf") -> bool:
        """
        Send PDF report via email.
        
        Args:
            to_email: Recipient email address
            pdf_data: PDF file content in bytes
            filename: Name of the PDF file
            
        Returns:
            bool: True if email was sent successfully
        """
        try:
            import base64
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject='Relatório de Ocupação Hospitalar',
                plain_text_content='Segue em anexo o relatório de ocupação hospitalar.'
            )

            encoded_file = base64.b64encode(pdf_data).decode()
            attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(filename),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            message.attachment = attachedFile

            response = self.sg.send(message)
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False
