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

# Função de segurança para substituir valores null ou string vazia por 'N/A'
def verificar_valores_nulos(dados: dict) -> dict:
    for chave, valor in dados.items():
        if isinstance(valor, dict):  # Verifica se o valor também é um dicionário
            # Chamada recursiva para dicionários aninhados
            verificar_valores_nulos(valor)
        
        elif valor is None or valor == '':
            dados[chave] = 'N/A'
            
    return dados


