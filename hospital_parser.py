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
            # Try parsing as simple percentage format first
            lines = [line.strip() for line in message.split('\n') if line.strip()]
            if any('leitos' in line and '%' in line for line in lines):
                print("Parsing message in simple percentage format...")
                return parse_simple_format(message)

            # If not simple format, try detailed format
            print("Attempting to parse detailed format...")
            return extract_hospital_data(message)

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
        print(f"Validating data structure: {data.keys()}")

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
        print("Validating detailed format...")
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
        print("Validating simple format...")
        for unit in data['units']:
            required = {'name', 'total_beds', 'occupancy_rate'} 
            if not required.issubset(unit.keys()):
                print(f"Missing required fields in unit: {unit.keys()}")
                return False
        return True