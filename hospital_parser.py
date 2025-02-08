
from typing import Dict, Optional
from utils import extract_hospital_data, parse_simple_format

class HospitalDataParser:
    """Parser for hospital occupancy data from text messages."""
    
    @staticmethod
    def parse_message(message: str) -> Dict:
        """
        Parse hospital occupancy message into structured data.
        
        Args:
            message: Raw message text containing hospital data
            
        Returns:
            Dict containing parsed hospital data
            
        Raises:
            ValueError: If message cannot be parsed
        """
        try:
            # Check for simple percentage format
            if all(line.strip().endswith('%') for line in message.split('\n') if line.strip()):
                return parse_simple_format(message)

            # Parse detailed format
            data = extract_hospital_data(message)
            
            # Extract occupancy rates section
            occupancy_section = message.split('🔴Taxa de ocupação')[-1]
            occupancy_rates = {}

            for line in occupancy_section.split('\n'):
                if '- ' not in line or '%' not in line:
                    continue
                    
                unit_name, rate_part = line.strip().split('-')
                rate = float(rate_part.replace('%', '').strip())
                occupancy_rates[unit_name.strip()] = rate

            data['occupancy_rates'] = occupancy_rates
            return data

        except Exception as e:
            raise ValueError(f"Failed to parse hospital data: {str(e)}")

    @staticmethod
    def validate_data(data: Dict) -> bool:
        """
        Validate parsed hospital data structure.
        
        Args:
            data: Parsed hospital data dictionary
            
        Returns:
            bool indicating if data is valid
        """
        if not data:
            return False

        if 'hospitals' in data:
            return HospitalDataParser._validate_detailed_format(data)
        elif 'units' in data:
            return HospitalDataParser._validate_simple_format(data)
            
        return False

    @staticmethod
    def _validate_detailed_format(data: Dict) -> bool:
        """Validate detailed format data structure."""
        for hospital in data['hospitals']:
            if not {'name', 'units'}.issubset(hospital.keys()):
                return False

            for unit in hospital['units']:
                required = {'name', 'total_beds', 'occupied_beds', 'available_beds'}
                if not required.issubset(unit.keys()):
                    return False
        return True

    @staticmethod
    def _validate_simple_format(data: Dict) -> bool:
        """Validate simple format data structure."""
        for unit in data['units']:
            required = {'name', 'total_beds', 'occupancy_rate'} 
            if not required.issubset(unit.keys()):
                return False
        return True
