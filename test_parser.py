from hospital_parser import HospitalDataParser

def test_simple_format():
    parser = HospitalDataParser()
    test_message = """Clínica Médica - 80%
Enfermaria Pediátrica - 60%
Geriatria - 45%
UCI Pediátrica - 70%
UTI Fundhacrê - 85%
UTI HSJ - 75%
UTI HUERB 1 - 65%
UTI HUERB 2 - 90%
UTI INTO - 55%
UTI Pediátrica - 80%"""

    try:
        data = parser.parse_message(test_message)
        print("Parsed data:", data)
        print("\nUnits found:", len(data['units']))

        print("\nDistribuição dos leitos por unidade:")
        for unit in data['units']:
            print(f"\nUnidade: {unit['name']}")
            print(f"Total de leitos: {unit['total_beds']}")
            print(f"Taxa de ocupação: {unit['occupancy_rate']}%")
            print(f"Leitos ocupados: {unit['occupied_beds']}")
            print(f"Leitos disponíveis: {unit['available_beds']}")

        print("\nValidation result:", parser.validate_data(data))

        # Verificar totais
        summary = data['summary']
        print("\nResumo:")
        print(f"Total de leitos clínicos: {summary['clinical_beds']} (deve ser 123)")
        print(f"Total de leitos UTI: {summary['icu_beds']} (deve ser 84)")
        print(f"Total geral de leitos: {summary['total_beds']} (deve ser 207)")

        return True
    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_simple_format()
    print("\nResultado do teste:", "PASSOU" if success else "FALHOU")