from abc import ABC, abstractmethod
from typing import Dict, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime
import io
from config import *

class BaseTemplate(ABC):
    """Base class for PDF report templates."""
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Setup custom styles for the PDF."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=FONT_SIZE_TITLE,
            spaceAfter=30,
            alignment=1,
            textColor=colors.HexColor(COLORS['white'])
        ))

        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=FONT_SIZE_SUBTITLE,
            spaceAfter=20,
            textColor=colors.HexColor(COLORS['primary'])
        ))

        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=FONT_SIZE_BODY,
            spaceAfter=12
        ))

    @abstractmethod
    def generate_pdf(self, data: Dict) -> io.BytesIO:
        """Generate PDF based on the template."""
        pass

    def create_document(self) -> SimpleDocTemplate:
        """Create a basic document with standard settings."""
        buffer = io.BytesIO()
        return SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=MARGIN,
            leftMargin=MARGIN,
            topMargin=MARGIN,
            bottomMargin=MARGIN
        ), buffer
