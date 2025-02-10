from pdf_generator import PDFGenerator
from datetime import datetime

def test_pdf_generation():
    # Test data with actual occupancy rates
    test_data = {
        'units': [
            {'name': 'UTI 1', 'total_beds': 17, 'occupancy_rate': 94.11},
            {'name': 'UTI 2', 'total_beds': 10, 'occupancy_rate': 80.00},
            {'name': 'UTI INTO', 'total_beds': 17, 'occupancy_rate': 64.70},
            {'name': 'UTI HSJ', 'total_beds': 20, 'occupancy_rate': 100.00},
            {'name': 'UTI FUNDAÇÃO', 'total_beds': 10, 'occupancy_rate': 100.00},
            {'name': 'UTI Pediátrica', 'total_beds': 10, 'occupancy_rate': 50.00},
            {'name': 'UCI Pediátrica', 'total_beds': 10, 'occupancy_rate': 80.00},
            {'name': 'Enf. Pediátrica', 'total_beds': 50, 'occupancy_rate': 70.00},
            {'name': 'Geriatria', 'total_beds': 33, 'occupancy_rate': 87.87},
            {'name': 'Clinica médica', 'total_beds': 30, 'occupancy_rate': 90.90}
        ]
    }

    print("\n=== Starting PDF Generation Test ===")
    print(f"Test data: {test_data}")

    # Initialize PDF generator
    pdf_gen = PDFGenerator()

    # Generate PDF
    try:
        pdf_buffer = pdf_gen.generate_pdf(test_data)

        # Save to file for testing
        with open('test_report.pdf', 'wb') as f:
            f.write(pdf_buffer.getvalue())

        print("PDF generated successfully!")
        print("Saved as: test_report.pdf")
        return True
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_pdf_generation()
    print("\nTest result:", "PASSED" if success else "FAILED")