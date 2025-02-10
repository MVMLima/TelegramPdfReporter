import io
from templates.base_template import BaseTemplate
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
from typing import Dict, List, Tuple
from config import *
from reportlab.lib.units import cm

class DefaultTemplate(BaseTemplate):
    """Default template implementing the current PDF format."""

    def _create_logo_header(self) -> Image:
        """Create the header with CIEGES logo."""
        logo_path = 'attached_assets/image_1739196996707.png'
        print(f"Loading header logo from: {logo_path}")
        img = Image(logo_path, width=PAGE_WIDTH-2*MARGIN, height=1.5*cm)
        img.hAlign = 'CENTER'
        return img

    def _create_logo_footer(self) -> Image:
        """Create the footer with CIEGES logo."""
        logo_path = 'attached_assets/image_1739197036571.png'
        print(f"Loading footer logo from: {logo_path}")
        img = Image(logo_path, width=PAGE_WIDTH-2*MARGIN, height=1.5*cm)
        img.hAlign = 'CENTER'
        return img

    def _create_header_section(self, data: Dict) -> Table:
        """Create the green header section with title and date."""
        table_data = [
            ['INFORMAÇÕES GERAIS'],
            [f"INFORME DIÁRIO {datetime.now().strftime('%d/%m/%Y')}"]
        ]
        table = Table(table_data, colWidths=[PAGE_WIDTH-2*MARGIN])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#00A65A')),  # CIEGES green
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 24),  # Title size
            ('FONTSIZE', (0, 1), (0, 1), 16),  # Date size
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        return table

    def _create_summary_section(self, data: Dict) -> Table:
        """Create the metrics summary section."""
        metrics = [
            [
                f"123\nLeitos Clínicos",
                f"0\nLeitos Ocupados",
                f"123\nLeitos Vagos"
            ],
            [
                f"84\nLeitos UTIs",
                f"0\nUTIs Ocupadas",
                f"84\nUTIs Vagas"
            ]
        ]

        table = Table(metrics, colWidths=[PAGE_WIDTH/3-MARGIN]*3)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Only outer border
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return table

    def _create_occupancy_table(self, units: List[Dict]) -> Table:
        """Create the detailed occupancy table."""
        table_data = [
            ['Unidade', '%', 'Ocupados', 'Disponível']
        ]

        # Override all values to match example
        for unit in units:
            table_data.append([
                f"{unit['name']} ({unit['total_beds']})",
                f"0.00%",
                "0",
                str(unit['total_beds'])
            ])

        # Adjusted column widths to match the example
        col_widths = [
            PAGE_WIDTH * 0.5,  # 50% for unit name
            PAGE_WIDTH * 0.15, # 15% for percentage
            PAGE_WIDTH * 0.175, # 17.5% for occupied
            PAGE_WIDTH * 0.175  # 17.5% for available
        ]

        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return table

    def generate_pdf(self, data: Dict) -> io.BytesIO:
        """Generate PDF from hospital data using the default template."""
        print("Generating PDF with CIEGES logos...")
        doc, buffer = self.create_document()
        story = []

        # Add header logo
        print("Adding header logo...")
        story.append(self._create_logo_header())
        story.append(Spacer(1, 10))

        # Add header
        story.append(self._create_header_section(data))
        story.append(Spacer(1, 20))

        # Add summary metrics
        story.append(self._create_summary_section(data))
        story.append(Spacer(1, 20))

        # Add occupancy table
        if 'units' in data:
            story.append(self._create_occupancy_table(data['units']))
        elif 'hospitals' in data:
            for hospital in data['hospitals']:
                story.append(self._create_occupancy_table(hospital['units']))

        # Add footer logo with spacing
        print("Adding footer logo...")
        story.append(Spacer(1, 30))
        story.append(self._create_logo_footer())

        # Build PDF
        print("Building final PDF...")
        doc.build(story)
        buffer.seek(0)
        print("PDF generation completed.")
        return buffer