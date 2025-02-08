"""Utility functions for parsing hospital data."""

import re
from typing import Dict, List, Tuple
from datetime import datetime

def parse_percentage(text: str) -> float:
    """Extract percentage value from text."""
    text = text.replace(',', '.')
    match = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
    return float(match.group(1)) if match else 0.0

def parse_beds(text: str) -> Tuple[int, int]:
    """Extract total beds count from text in parentheses."""
    match = re.search(r'\((\d+)\s*(?:leitos?)?\)', text)
    return (int(match.group(1)), 0) if match else (0, 0)

def clean_text(text: str) -> str:
    """Clean and normalize text by removing extra whitespace."""
    return ' '.join(text.split())

def parse_simple_format(text: str) -> Dict:
    """Parse simplified format with unit names and percentages."""
    units = []
    stats = {
        'clinical_beds': 0,
        'icu_beds': 0,
        'occupied_clinical': 0,
        'occupied_icu': 0
    }

    lines = [line.strip() for line in text.split('\n') if line.strip()]

    for line in lines:
        # Extrair nome da unidade e porcentagem
        parts = line.split('-')
        if len(parts) != 2:
            continue

        name = parts[0].strip()
        # Assumir 10 leitos como padrão se não especificado
        total_beds = 10

        # Extrair porcentagem
        occupancy_rate = parse_percentage(parts[1])
        occupied_beds = int(round(total_beds * occupancy_rate / 100))

        unit = {
            'name': name,
            'total_beds': total_beds,
            'occupancy_rate': occupancy_rate,
            'occupied_beds': occupied_beds,
            'available_beds': total_beds - occupied_beds
        }

        # Atualizar estatísticas
        if 'UTI' in name or 'UCI' in name:
            stats['icu_beds'] += total_beds
            stats['occupied_icu'] += occupied_beds
        else:
            stats['clinical_beds'] += total_beds
            stats['occupied_clinical'] += occupied_beds

        units.append(unit)

    return {
        'units': units,
        'date': datetime.now().strftime('%d/%m/%Y'),
        'summary': _generate_summary(stats)
    }

def _generate_summary(stats: Dict) -> Dict:
    """Generate summary statistics from collected data."""
    total_beds = stats['clinical_beds'] + stats['icu_beds']
    total_occupied = stats['occupied_clinical'] + stats['occupied_icu']

    return {
        'clinical_beds': stats['clinical_beds'],
        'occupied_clinical': stats['occupied_clinical'],
        'available_clinical': stats['clinical_beds'] - stats['occupied_clinical'],
        'icu_beds': stats['icu_beds'],
        'occupied_icu': stats['occupied_icu'],
        'available_icu': stats['icu_beds'] - stats['occupied_icu'],
        'total_beds': total_beds,
        'total_occupied': total_occupied,
        'total_available': total_beds - total_occupied
    }

def extract_hospital_data(text: str) -> Dict:
    """Extract structured hospital data from text."""
    hospitals = []

    for section in (s.strip() for s in text.split('🏥') if s.strip()):
        lines = section.split('\n')
        hospital = {
            'name': clean_text(lines[0]),
            'units': _parse_hospital_units(lines[1:])
        }
        hospitals.append(hospital)

    return {'hospitals': hospitals}

def _parse_hospital_units(lines: List[str]) -> List[Dict]:
    """Parse hospital unit information from lines of text."""
    units = []
    current_unit = None

    for line in (l.strip() for l in lines if l.strip()):
        if '🟢' in line:
            if current_unit:
                units.append(current_unit)
            current_unit = _create_new_unit(line)
        elif current_unit:
            _update_unit_stats(current_unit, line)

    if current_unit:
        units.append(current_unit)

    return units

def _create_new_unit(line: str) -> Dict:
    """Create new unit dictionary from unit header line."""
    total_beds, _ = parse_beds(line)
    return {
        'name': clean_text(line.replace('🟢', '')),
        'total_beds': total_beds,
        'occupied_beds': 0,
        'available_beds': 0,
        'blocked_beds': 0,
        'details': []
    }

def _update_unit_stats(unit: Dict, line: str) -> None:
    """Update unit statistics based on detail line."""
    line_lower = line.lower()
    match = re.search(r'(\d+)', line)

    if not match:
        return

    value = int(match.group(1))

    if any(x in line_lower for x in ['internados', 'ocupados']):
        unit['occupied_beds'] = value
    elif 'vaga' in line_lower:
        unit['available_beds'] = value
    elif 'bloqueado' in line_lower:
        unit['blocked_beds'] = value

    unit['details'].append(line)