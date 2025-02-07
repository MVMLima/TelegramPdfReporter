import re
from typing import Dict, List, Tuple

def parse_percentage(text: str) -> float:
    """Extract percentage from text."""
    match = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
    if match:
        return float(match.group(1))
    return 0.0

def parse_beds(text: str) -> Tuple[int, int]:
    """Extract total beds from text in parentheses."""
    match = re.search(r'\((\d+)\s*(?:leitos)?\)', text)
    if match:
        return int(match.group(1)), 0
    return 0, 0

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    return text.strip().replace('\n', ' ').replace('  ', ' ')

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
