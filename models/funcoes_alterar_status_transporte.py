from models.validacao_dados import verificar_valor_na_lista


def selecionar_id_transporte_atualizar_status(lista_ids_transportes: list) -> int:
    # Solicita e válida o ID do transporte para atualizar status
    try:
        while True:
            id_transporte = int(input(
                f'\n➡️   Informe o ID do transporte para alterar o status: '))

            id_valido = verificar_valor_na_lista(
                id_transporte, lista_ids_transportes)

            if id_valido:
                break
            else:
                print(f'\n⚠️   Id de transporte não encontrado, tente novamente.')

    except:
        while True:
            if id_valido != 'not found':
                id_transporte = input('\n⚠️   Digite uma opção válida: ')

            else:
                id_transporte = (input(
                    f'\n➡️   Informe o ID do transporte para alterar o status: '))

            if id_transporte.isdigit():
                id_transporte = int(id_transporte)

                id_valido = verificar_valor_na_lista(
                    id_transporte, lista_ids_transportes)

                if id_valido:
                    break
                else:
                    print(f'\n⚠️   Id de transporte não encontrado, tente novamente.')
                    id_valido = 'not found'

            else:
                print('\n🚫  Por favor, insira apenas dígitos.')

    return id_transporte


def opcoes_status() -> str:
    # Exibi as opcoes para escolha
    print('\n↘️   Escolha uma opção para alterar o status:\n')
    lista_opcoes_menu = (
        ' 1 - Cancelado',
        ' 2 - Concluído',
    )

    for opcao_menu in lista_opcoes_menu:
        print(opcao_menu)

    # Solicita ao usuário a opção de alterar o status para "Concluído" ou  "Cancelado"
    while True:
        try:
            opcao = int(input(f'\n➡️   Selecione um opção de status: '))

        except:
            while True:
                opcao = input('\n⚠️   Digite uma opção válida: ')

                if opcao.isdigit():
                    opcao = int(opcao)
                    break
                else:
                    print('\n🚫  Por favor, insira apenas dígitos.')

        finally:
            match opcao:
                case 1:
                    return 'Cancelado'
                case 2:
                    return 'Concluído'
                case _:
                    print(f'\n⚠️   Opção inválida, tente novamente.')
