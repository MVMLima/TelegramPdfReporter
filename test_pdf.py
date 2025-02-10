from pdf_generator import PDFGenerator
from datetime import datetime

def test_pdf_generation():
    # Test data from the provided message
    test_message = """UTI 1 (17 leitos) -  94,11%
UTI 2 (10 leitos) - 80,00%
UTI INTO (17 leitos) - 64,70%
UTI HSJ (20 leitos) - 100,00%
UTI FUNDAÇÃO (10 leitos) - 100,00%
UTI Pediátrica (10 leitos) - 50,00%
UCI Pediátrica (10 leitos) - 80,00%
Enf. Pediátrica (50 leitos) -70,00%
Geriatria (33 leitos) -  87,87%
Clinica médica (30 leitos)- 90,90%"""

    # Parse the message using HospitalDataParser
    from hospital_parser import HospitalDataParser
    parser = HospitalDataParser()
    data = parser.parse_message(test_message)

    # Initialize PDF generator
    pdf_gen = PDFGenerator()

    # Generate PDF
    pdf_buffer = pdf_gen.generate_pdf(data)

    # Save to file for testing
    with open('test_report.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())

    print("PDF generated successfully!")

if __name__ == '__main__':
    test_pdf_generation()