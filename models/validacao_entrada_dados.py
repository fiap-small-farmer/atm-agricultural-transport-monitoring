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