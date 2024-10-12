from prettytable import PrettyTable

from models.validacao_dados import verificar_valor_na_lista


def exibir_dados_estruturado_resumido(lista_transportes_produtos_origem_destino: list) -> None:
    # Definir o espaço fixo para as colunas
    espaco_fixo = 20

    # Criar uma nova tabela com os nomes das colunas
    table = PrettyTable()
    table.field_names = ['ID TRANSPORTE', 'STATUS', 'PRODUTO', 'QTD.', 'UND. TRANSPORTE',
                         'TEMP. MONITORADA ºC', 'PRODUTORA', 'COMPRADOR']

    # Definir alinhamento das colunas
    table.align = 'l'  # Alinhamento à esquerda

    for transporte_produto in lista_transportes_produtos_origem_destino:
        table.add_row([
            str(transporte_produto.get('id_transporte')).ljust(
                espaco_fixo)[:espaco_fixo],
            transporte_produto.get('status_transporte').ljust(
                espaco_fixo)[:espaco_fixo],
            transporte_produto.get('produto').ljust(espaco_fixo)[:espaco_fixo],
            str(transporte_produto.get('quantidade')).ljust(
                espaco_fixo)[:espaco_fixo],
            transporte_produto.get('und_transporte').ljust(
                espaco_fixo)[:espaco_fixo],
            str(transporte_produto.get('temp_monitorada'))if transporte_produto.get(
                'temp_monitorada') is not None else 'Não monitorado'.ljust(espaco_fixo)[:espaco_fixo],
            transporte_produto.get('nome_produtora').ljust(
                espaco_fixo)[:espaco_fixo],
            transporte_produto.get('nome_comprador').ljust(
                espaco_fixo)[:espaco_fixo]
        ])

    print(table)


def exibir_dados_estruturado_origem_destino(id_transporte: int, dados_detalhes: int, dados_origem: dict, dados_destino: dict) -> None:
    # Definir o espaço fixo para as colunas
    espaco_fixo = 20

    # Criar uma nova tabela com os nomes das colunas
    detalhes = PrettyTable()
    detalhes.field_names = ['TEMP. MÍNIMA', 'TEMP. MÁXIMA',
                            'INSTRUÇÕES', 'TIPO DE CAMINHÃO']
    detalhes.align = 'l'
    detalhes.add_row([
        dados_detalhes.get('temp_minima').ljust(espaco_fixo)[:espaco_fixo],
        dados_detalhes.get('temp_maxima').ljust(espaco_fixo)[:espaco_fixo],
        dados_detalhes.get('instrucoes').ljust(espaco_fixo)[:espaco_fixo],
        dados_detalhes.get('tipo_caminhao').ljust(espaco_fixo)[:espaco_fixo]
    ])

    # Criar uma nova tabela com os nomes das colunas
    origem = PrettyTable()
    origem.field_names = ['PRODUTORA', 'CEP',
                          'ENDEREÇO', 'NÚMERO', 'CIDADE', 'ESTADO']
    origem.align = 'l'
    origem.add_row([
        dados_origem.get('nome_produtora', '').ljust(
            espaco_fixo)[:espaco_fixo],
        dados_origem.get('cep_origem', '').ljust(espaco_fixo)[:espaco_fixo],
        dados_origem.get('endereco_origem', '').ljust(
            espaco_fixo)[:espaco_fixo],
        str(dados_origem.get('numero_origem', '')).ljust(
            espaco_fixo)[:espaco_fixo],
        dados_origem.get('cidade_origem', '').ljust(espaco_fixo)[:espaco_fixo],
        dados_origem.get('Estado_origem', '').ljust(espaco_fixo)[:espaco_fixo]
    ])

    # Criar uma nova tabela com os nomes das colunas
    destino = PrettyTable()
    destino.field_names = ['COMPRADOR', 'CEP',
                           'ENDEREÇO', 'NÚMERO', 'CIDADE', 'ESTADO']
    destino.align = 'l'
    destino.add_row([
        dados_destino.get('nome_comprador', '').ljust(
            espaco_fixo)[:espaco_fixo],
        dados_destino.get('cep_destino', '').ljust(espaco_fixo)[:espaco_fixo],
        dados_destino.get('endereco_destino', '').ljust(
            espaco_fixo)[:espaco_fixo],
        str(dados_destino.get('numero_destino', '')).ljust(
            espaco_fixo)[:espaco_fixo],
        dados_destino.get('cidade_destino', '').ljust(
            espaco_fixo)[:espaco_fixo],
        dados_destino.get('Estado_destino', '').ljust(
            espaco_fixo)[:espaco_fixo]
    ])

    print(f'\n\n🟠  DETALHES DO TRANSPORTE ID: {id_transporte}\n\n')
    print(f'🔴  INSTRUÇÕES PARA TRANSPORTE:\n')
    print(detalhes)
    print(f'\n🔵  INFORMAÇÕES DE ORIGEM:\n')
    print(origem)
    print(f'\n🟢  INFORMAÇÕES DE DESTINO:\n')
    print(destino)


def opcoes_apos_consulta(tipo: str) -> str:

    if tipo == 'Todos':
        # Exibi as opcoes para escolha
        print('\n↘️   Menu consulta:\n')
        lista_opcoes_menu = (
            ' 1 - Exibir mais detalhes',
            ' 2 - Sair',
        )

    elif tipo == 'Não iniciado':
        # Exibi as opcoes para escolha
        print('\n↘️   Menu transporte e monitoramento:\n')
        lista_opcoes_menu = (
            ' 1 - Exibir mais detalhes',
            ' 2 - Iniciar entrega e monitoramento',
            ' 3 - Sair',
        )

    elif tipo == 'Em andamento':
        # Exibi as opcoes para escolha
        print('\n↘️   Menu alterar status de transportes:\n')
        lista_opcoes_menu = (
            ' 1 - Exibir mais detalhes',
            ' 2 - Alterar status do transporte',
            ' 3 - Sair',
        )

    for opcao_menu in lista_opcoes_menu:
        print(opcao_menu)

    # Solicita ao usuário a opção de alterar o status para "Concluído" ou  "Cancelado"
    while True:
        try:
            opcao = int(input(f'\n➡️   Selecione uma opção: '))

        except:
            while True:
                opcao = input('\n⚠️   Digite uma opção válida: ')

                if opcao.isdigit():
                    opcao = int(opcao)
                    break
                else:
                    print('\n🚫  Por favor, insira apenas dígitos.')

        finally:
            if tipo == 'Todos':
                match opcao:
                    case 1:
                        return 'detalhes'
                    case 2:
                        return 'sair'
                    case _:
                        print(f'\n⚠️   Opção inválida, tente novamente.')

            elif tipo == 'Não iniciado':
                match opcao:
                    case 1:
                        return 'detalhes'
                    case 2:
                        return 'iniciar transporte'
                    case 3:
                        return 'sair'
                    case _:
                        print(f'\n⚠️   Opção inválida, tente novamente.')

            elif tipo == 'Em andamento':
                match opcao:
                    case 1:
                        return 'detalhes'
                    case 2:
                        return 'alterar status'
                    case 3:
                        return 'sair'
                    case _:
                        print(f'\n⚠️   Opção inválida, tente novamente.')


def selecionar_id_transporte_para_mais_detalhes(lista_ids_transportes: list) -> int:
    # Solicita e valida o ID do transporte para atualizar status
    while True:
        id_transporte = input(
            f'\n➡️   Informe o ID do transporte para exibir INSTRUÇÕES DE TRANSPORTE e INFORMAÇÕES de ORIGEM e DESTINO: ')

        # Verifica se a entrada não está vazia e se é um número
        if id_transporte.isdigit():
            id_transporte = int(id_transporte)
            id_valido = verificar_valor_na_lista(
                id_transporte, lista_ids_transportes)

            if id_valido:
                break
            else:
                print(f'\n⚠️   Id de transporte não encontrado, tente novamente.')
        else:
            print('\n🚫  Por favor, insira apenas dígitos e não deixe o campo vazio.')

    return id_transporte


def obter_detalhes_produtor_comprador(id_transporte: int, lista_transportes: list):
    for transporte in lista_transportes:
        if transporte['id_transporte'] == id_transporte:
            dados_origem = {
                'nome_produtora': transporte.get('nome_produtora'),
                'cep_origem': transporte.get('cep_origem'),
                'endereco_origem': transporte.get('endereco_origem'),
                'numero_origem': transporte.get('numero_origem'),
                'cidade_origem': transporte.get('cidade_origem'),
                'Estado_origem': transporte.get('Estado_origem')
            }

            dados_destino = {
                'nome_comprador': transporte.get('nome_comprador'),
                'cep_destino': transporte.get('cep_destino'),
                'endereco_destino': transporte.get('endereco_destino'),
                'numero_destino': transporte.get('numero_destino'),
                'cidade_destino': transporte.get('cidade_destino'),
                'Estado_destino': transporte.get('Estado_destino')
            }

            dados_detalhes = {
                'temp_minima': transporte.get('temp_minima'),
                'temp_maxima': transporte.get('temp_maxima'),
                'instrucoes': transporte.get('instrucoes'),
                'tipo_caminhao': transporte.get('tipo_caminhao'),
            }

    # Exibi os dados do produtor e comprador de forma estruturada
    exibir_dados_estruturado_origem_destino(
        id_transporte, dados_detalhes, dados_origem,  dados_destino)
