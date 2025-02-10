from hospital_parser import HospitalDataParser

def test_simple_format():
    parser = HospitalDataParser()
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