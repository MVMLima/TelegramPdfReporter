import re
from typing import Dict, List, Tuple
from datetime import datetime

def parse_percentage(text: str) -> float:
    """Extract percentage from text."""
    # Convert comma to dot for decimal numbers
    text = text.replace(',', '.')
    match = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
    if match:
        return float(match.group(1))
    return 0.0

def parse_beds(text: str) -> Tuple[int, int]:
    """Extract total beds from text in parentheses."""
    match = re.search(r'\((\d+)\s*(?:leitos?)?\)', text)
    if match:
        return int(match.group(1)), 0
    return 0, 0

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    return text.strip().replace('\n', ' ').replace('  ', ' ')

def parse_simple_format(text: str) -> Dict:
    """Parse the simplified format with just unit names, beds, and percentages."""
    units = []
    clinical_beds = 0
    icu_beds = 0
    occupied_clinical = 0
    occupied_icu = 0

    # Split by double newlines to handle extra spacing
    lines = [line.strip() for line in text.split('\n\n')]

    # Process each non-empty line
    for line in lines:
        if not line.strip():
            continue

        # Extract unit name, total beds and occupancy rate
        # Updated pattern to be more flexible with spaces and decimal separators
        match = re.match(r'(.*?)\s*\((\d+)\s*leitos?\)\s*-\s*(\d+[,.]\d+|\d+)\s*%', line.replace('\n', ' ').strip())

        if match:
            unit_name = match.group(1).strip()
            total_beds = int(match.group(2))
            # Convert comma to dot for decimal numbers
            occupancy_rate = float(match.group(3).replace(',', '.'))

            # Calculate occupied beds
            occupied_beds = int(round(total_beds * occupancy_rate / 100))

            unit = {
                'name': unit_name,
                'total_beds': total_beds,
                'occupancy_rate': occupancy_rate,
                'occupied_beds': occupied_beds,
                'available_beds': total_beds - occupied_beds
            }

            # Classify as ICU or Clinical
            if 'UTI' in unit_name or 'UCI' in unit_name:
                icu_beds += total_beds
                occupied_icu += occupied_beds
            else:
                clinical_beds += total_beds
                occupied_clinical += occupied_beds

            units.append(unit)

    return {
        'units': units,
        'date': datetime.now().strftime('%d/%m/%Y'),
        'summary': {
            'clinical_beds': clinical_beds,
            'occupied_clinical': occupied_clinical,
            'available_clinical': clinical_beds - occupied_clinical,
            'icu_beds': icu_beds,
            'occupied_icu': occupied_icu,
            'available_icu': icu_beds - occupied_icu,
            'total_beds': clinical_beds + icu_beds,
            'total_occupied': occupied_clinical + occupied_icu,
            'total_available': (clinical_beds + icu_beds) - (occupied_clinical + occupied_icu)
        }
    }

def extract_hospital_data(text: str) -> Dict:
    """Extract hospital section data from text."""
    sections = text.split('🏥')
    hospitals = []

    for section in sections:
        if not section.strip():
            continue

        hospital = {
            'name': '',
            'units': []
        }

        lines = section.strip().split('\n')
        hospital['name'] = clean_text(lines[0])

        current_unit = None
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            if '🟢' in line:
                if current_unit:
                    hospital['units'].append(current_unit)
                current_unit = {
                    'name': clean_text(line.replace('🟢', '')),
                    'total_beds': 0,
                    'occupied_beds': 0,
                    'available_beds': 0,
                    'blocked_beds': 0,
                    'details': []
                }
                total_beds, _ = parse_beds(line)
                current_unit['total_beds'] = total_beds

            elif current_unit and any(x in line.lower() for x in ['internados', 'ocupados']):
                match = re.search(r'(\d+)', line)
                if match:
                    current_unit['occupied_beds'] = int(match.group(1))
                current_unit['details'].append(line)

            elif current_unit and 'vaga' in line.lower():
                match = re.search(r'(\d+)', line)
                if match:
                    current_unit['available_beds'] = int(match.group(1))
                current_unit['details'].append(line)

            elif current_unit and 'bloqueado' in line.lower():
                match = re.search(r'(\d+)', line)
                if match:
                    current_unit['blocked_beds'] = int(match.group(1))
                current_unit['details'].append(line)

        if current_unit:
            hospital['units'].append(current_unit)

        hospitals.append(hospital)

    return {'hospitals': hospitals}