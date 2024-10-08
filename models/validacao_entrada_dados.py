def validacao_opcoes_menu() -> int:
    try:
        opcao = int(input(f'\n➡️   Selecione um opção: '))
    except:
        while True:
            opcao = input('\n⚠️   Digite uma opção válida: ')

            if opcao.isdigit():
                opcao = int(opcao)
                break
            else:
                print('\n🚫  Por favor, insira apenas dígitos.')

    return opcao

# Função de segurança para substituir valores None por 'N/A'
def verificar_valores_nulos(dados: dict) -> dict:
    # Substitui valores None por 'N/A' em um dicionário.
    for chave, valor in dados.items():
        if isinstance(valor, dict):  # Verifica se o valor também é um dicionário
            verificar_valores_nulos(valor)  # Chamada recursiva para dicionários aninhados

        elif valor is None:
            dados[chave] = 'N/A'
            
    return dados