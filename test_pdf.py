from pdf_generator import PDFGenerator
from datetime import datetime

def test_pdf_generation():
    # Test data
    test_data = {
        'units': [
            {
                'name': 'UTI',
                'total_beds': 10,
                'occupied_beds': 6,
                'available_beds': 4,
                'occupancy_rate': 60.0
            },
            {
                'name': 'Enfermaria',
                'total_beds': 20,
                'occupied_beds': 15,
                'available_beds': 5,
                'occupancy_rate': 75.0
            }
        ]
    }
    
    # Initialize PDF generator
    pdf_gen = PDFGenerator()
    
    # Generate PDF
    pdf_buffer = pdf_gen.generate_pdf(test_data)
    
    # Save to file for testing
    with open('test_report.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())
    
    print("PDF generated successfully!")

if __name__ == '__main__':
    test_pdf_generation()
