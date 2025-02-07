from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import io
from config import *

class PDFGenerator:
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
            alignment=1
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

    def generate_pdf(self, data):
        """Generate PDF from hospital data."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=MARGIN,
            leftMargin=MARGIN,
            topMargin=MARGIN,
            bottomMargin=MARGIN
        )

        story = []
        
        # Title
        title = Paragraph(
            f"Relatório de Ocupação Hospitalar<br/>Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self.styles['CustomTitle']
        )
        story.append(title)
        
        # Add hospital sections
        for hospital in data['hospitals']:
            story.append(Paragraph(hospital['name'], self.styles['CustomSubtitle']))
            
            for unit in hospital['units']:
                # Create unit table data
                table_data = [
                    ['Indicador', 'Valor'],
                    ['Total de Leitos', str(unit['total_beds'])],
                    ['Leitos Ocupados', str(unit['occupied_beds'])],
                    ['Leitos Disponíveis', str(unit['available_beds'])],
                ]
                
                if unit['blocked_beds']:
                    table_data.append(['Leitos Bloqueados', str(unit['blocked_beds'])])
                
                # Calculate occupancy rate
                if unit['total_beds'] > 0:
                    occupancy_rate = (unit['occupied_beds'] / unit['total_beds']) * 100
                    table_data.append(['Taxa de Ocupação', f"{occupancy_rate:.1f}%"])
                
                # Create and style table
                table = Table(table_data, colWidths=[200, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['primary'])),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(COLORS['white'])),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ]))
                
                story.append(Paragraph(unit['name'], self.styles['CustomSubtitle']))
                story.append(table)
                story.append(Spacer(1, 20))
            
            story.append(Spacer(1, 30))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
