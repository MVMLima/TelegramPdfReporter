import io
from templates.base_template import BaseTemplate
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
from typing import Dict, List, Tuple
from config import *
from reportlab.lib.units import cm
import os

class DefaultTemplate(BaseTemplate):
    """Default template implementing the current PDF format."""

    def _create_logo_header(self) -> Image:
        """Create the header with CIEGES logo."""
        logo_path = 'attached_assets/image_1739196996707.png'
        try:
            if os.path.exists(logo_path):
                img = Image(logo_path, width=PAGE_WIDTH-2*MARGIN, height=1.5*cm)
                img.hAlign = 'CENTER'
                return img
            else:
                print(f"Warning: Header logo file not found at {logo_path}")
                return None
        except Exception as e:
            print(f"Error loading header logo: {str(e)}")
            return None

    def _create_logo_footer(self) -> Image:
        """Create the footer with CIEGES logo."""
        logo_path = 'attached_assets/image_1739197036571.png'
        try:
            if os.path.exists(logo_path):
                img = Image(logo_path, width=PAGE_WIDTH-2*MARGIN, height=1.5*cm)
                img.hAlign = 'CENTER'
                return img
            else:
                print(f"Warning: Footer logo file not found at {logo_path}")
                return None
        except Exception as e:
            print(f"Error loading footer logo: {str(e)}")
            return None

    def _create_header_section(self, data: Dict) -> Table:
        """Create the green header section with title and date."""
        print("Creating header section...")
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
        print("Creating summary section...")
        # Calculate totals from the units data
        clinical_beds = 123  # Total fixed
        icu_beds = 84  # Total fixed

        occupied_clinical = 0
        occupied_icu = 0

        print(f"Processing {len(data['units'])} units for summary...")
        for unit in data['units']:
            is_icu = 'UTI' in unit['name']
            beds_occupied = int(round(unit['total_beds'] * unit['occupancy_rate'] / 100))

            print(f"Unit: {unit['name']}")
            print(f"Total beds: {unit['total_beds']}")
            print(f"Occupancy rate: {unit['occupancy_rate']}%")
            print(f"Calculated occupied beds: {beds_occupied}")

            if is_icu:
                occupied_icu += beds_occupied
            else:
                occupied_clinical += beds_occupied

        print(f"Final totals - Clinical: {occupied_clinical}/{clinical_beds}, ICU: {occupied_icu}/{icu_beds}")

        metrics = [
            [
                f"{clinical_beds}\nLeitos Clínicos",
                f"{occupied_clinical}\nLeitos Ocupados",
                f"{clinical_beds - occupied_clinical}\nLeitos Vagos"
            ],
            [
                f"{icu_beds}\nLeitos UTIs",
                f"{occupied_icu}\nUTIs Ocupadas",
                f"{icu_beds - occupied_icu}\nUTIs Vagas"
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
        print("Creating occupancy table...")
        table_data = [
            ['Unidade', '%', 'Ocupados', 'Disponível']
        ]

        print(f"Processing {len(units)} units for table...")
        # Ordenar unidades por taxa de ocupação (decrescente)
        sorted_units = sorted(units, key=lambda x: float(x['occupancy_rate']), reverse=True)

        for unit in sorted_units:
            # Calculate the number of occupied beds based on occupancy rate
            total_beds = unit['total_beds']
            occupancy_rate = unit['occupancy_rate']
            occupied_beds = int(round(total_beds * occupancy_rate / 100))
            available_beds = total_beds - occupied_beds

            print(f"Unit: {unit['name']}")
            print(f"Total beds: {total_beds}")
            print(f"Occupancy rate: {occupancy_rate}%")
            print(f"Occupied beds: {occupied_beds}")
            print(f"Available beds: {available_beds}")

            table_data.append([
                f"{unit['name']} ({total_beds} leitos)",
                f"{occupancy_rate:.2f}%",
                str(occupied_beds),
                str(available_beds)
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
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center all text
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular text for data
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
            ('FONTSIZE', (0, 1), (-1, -1), 10),  # Data font size
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return table

    def _create_overview_section(self, data: Dict) -> Table:
        """Create the overview section with total occupancy percentages."""
        print("Creating overview section...")

        # Calculate total occupancy percentage
        total_beds = 0
        total_occupied = 0

        for unit in data['units']:
            total_beds += unit['total_beds']
            occupied = int(round(unit['total_beds'] * unit['occupancy_rate'] / 100))
            total_occupied += occupied

        occupied_percentage = (total_occupied / total_beds) * 100 if total_beds > 0 else 0
        available_percentage = 100 - occupied_percentage

        # Create table with overview information
        table_data = [
            ['Visão Geral'],
            [f'Leitos Ocupados: {occupied_percentage:.1f}% dos leitos estão ocupados'],
            [f'Leitos Vagos: {available_percentage:.1f}% dos leitos estão vagos']
        ]

        table = Table(table_data, colWidths=[PAGE_WIDTH-2*MARGIN])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),  # Header
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Content
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Content text
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left align all text
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header
            ('FONTSIZE', (0, 0), (-1, 0), 14),  # Header size
            ('FONTSIZE', (0, 1), (-1, -1), 12),  # Content size
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        return table

    def generate_pdf(self, data: Dict) -> io.BytesIO:
        """Generate PDF from hospital data using the default template."""
        print("\n=== Starting PDF Generation ===")
        print(f"Received data: {data}")

        doc, buffer = self.create_document()
        story = []

        # Add header logo if available
        print("Adding header logo...")
        header_logo = self._create_logo_header()
        if header_logo:
            story.append(header_logo)
            story.append(Spacer(1, 10))

        # Add header
        print("Creating header section...")
        story.append(self._create_header_section(data))
        story.append(Spacer(1, 20))

        # Add summary metrics
        print("Creating summary section...")
        story.append(self._create_summary_section(data))
        story.append(Spacer(1, 20))

        # Add overview section
        print("Adding overview section...")
        story.append(self._create_overview_section(data))
        story.append(Spacer(1, 20))

        # Add occupancy table
        print("Adding occupancy table...")
        if 'units' in data and data['units']:
            story.append(self._create_occupancy_table(data['units']))
        else:
            print("Warning: No units found in data!")
            print(f"Available keys in data: {data.keys()}")
            print(f"Data content: {data}")

        # Add footer logo if available
        print("Adding footer logo...")
        footer_logo = self._create_logo_footer()
        if footer_logo:
            story.append(Spacer(1, 30))
            story.append(footer_logo)

        # Build PDF
        print("Building final PDF...")
        doc.build(story)
        buffer.seek(0)
        print("PDF generation completed.")
        return buffer