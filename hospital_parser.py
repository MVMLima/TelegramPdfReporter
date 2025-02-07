from typing import Dict
import re
from utils import extract_hospital_data

class HospitalDataParser:
    @staticmethod
    def parse_message(message: str) -> Dict:
        """
        Parse the hospital occupancy message and return structured data.
        """
        try:
            # Extract main hospital data
            data = extract_hospital_data(message)
            
            # Extract occupancy rates
            occupancy_section = message.split('🔴Taxa de ocupação')[-1]
            occupancy_rates = {}
            
            for line in occupancy_section.split('\n'):
                line = line.strip()
                if '- ' in line and '%' in line:
                    unit_name = line.split('-')[0].strip()
                    rate = float(line.split('-')[1].replace('%', '').strip())
                    occupancy_rates[unit_name] = rate
            
            data['occupancy_rates'] = occupancy_rates
            return data
            
        except Exception as e:
            raise ValueError(f"Error parsing hospital data: {str(e)}")

    @staticmethod
    def validate_data(data: Dict) -> bool:
        """
        Validate the parsed data structure.
        """
        if not data or 'hospitals' not in data:
            return False
            
        for hospital in data['hospitals']:
            if 'name' not in hospital or 'units' not in hospital:
                return False
                
            for unit in hospital['units']:
                required_fields = ['name', 'total_beds', 'occupied_beds', 'available_beds']
                if not all(field in unit for field in required_fields):
                    return False
                    
        return True
