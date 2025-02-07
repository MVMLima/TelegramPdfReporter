from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from datetime import datetime
import io
from config import *
from templates.template_manager import TemplateManager
from typing import Dict, Optional


class PDFGenerator:
    def __init__(self):
        self.template_manager = TemplateManager()

    def generate_pdf(self, data: Dict, template_name: Optional[str] = None) -> io.BytesIO:
        """Generate PDF using the specified template."""
        template = self.template_manager.get_template(template_name)
        return template.generate_pdf(data)

    def list_templates(self) -> Dict[str, str]:
        """List available templates."""
        return self.template_manager.list_templates()

    def register_template(self, name: str, template) -> None:
        """Register a new template."""
        self.template_manager.register_template(name, template)

    def set_default_template(self, name: str) -> bool:
        """Set the default template."""
        return self.template_manager.set_default_template(name)