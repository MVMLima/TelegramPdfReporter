from hospital_parser import HospitalDataParser

def test_simple_format():
    parser = HospitalDataParser()
    test_message = """UTI - 80%
Enfermaria - 60%
Centro Cirúrgico - 45%"""

    try:
        data = parser.parse_message(test_message)
        print("Parsed data:", data)
        print("\nUnits found:", len(data['units']))
        for unit in data['units']:
            print(f"\nUnit: {unit['name']}")
            print(f"Total beds: {unit['total_beds']}")
            print(f"Occupancy rate: {unit['occupancy_rate']}%")
            print(f"Occupied beds: {unit['occupied_beds']}")
            print(f"Available beds: {unit['available_beds']}")

        print("\nValidation result:", parser.validate_data(data))
        return True
    except Exception as e:
        print(f"Error parsing message: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_simple_format()
    print("\nTest result:", "PASSED" if success else "FAILED")