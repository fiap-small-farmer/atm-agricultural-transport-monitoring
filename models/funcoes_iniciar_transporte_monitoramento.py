from prettytable import PrettyTable

from models.funcoes_dataBase import consultar_produto, consultar_origem, consultar_destino
from models.validacao_dados import verificar_valor_na_lista


def consultar_dados_produto(lista_transportes: list) -> list:
   # Através do Id do produto vinculado ao transporte efetua uma busca no banco de dados do produto transportado
    lista_produtos = []
    for dados_transporte in lista_transportes:
        id_produto = dados_transporte.get('id_produto')
        id_produto = int(id_produto)

        # Roda a função consultar_produto com o id_produto
        dados_produto = consultar_produto(id_produto)
        dados_produto = dados_produto[0]

        lista_produtos.append(dados_produto)

    return lista_produtos


def consultar_dados_origem(lista_transportes: list) -> list:
   # Através do Id de origem vinculado ao transporte efetua uma busca no banco de dados da origem do transporte
    lista_origem = []
    for dados_transporte in lista_transportes:
        id_origem = dados_transporte.get('id_origem')
        id_origem = int(id_origem)

        # Roda a função consultar_destino com o id_origem
        dados_origem = consultar_origem(id_origem)
        dados_origem = dados_origem[0]

        lista_origem.append(dados_origem)

    return lista_origem


def consultar_dados_destino(lista_transportes: list) -> list:
   # Através do Id de destino vinculado ao transporte efetua uma busca no banco de dados do destino onde será transportado o produto
    lista_destino = []
    for dados_transporte in lista_transportes:
        id_destino = dados_transporte.get('id_destino')
        id_destino = int(id_destino)

        # Roda a função consultar_destino com o id_destino
        dados_destino = consultar_destino(id_destino)
        dados_destino = dados_destino[0]

        lista_destino.append(dados_destino)

    return lista_destino


def combinar_dados(lista_transportes: list, lista_produtos: list, lista_origem: list, lista_destino: list) -> list:
    # Combina as listas de transportes com a lista de produtos, origem e destino
    # Prepara os dados para combinação
    produtos_por_id = {produto['id_produto']: produto for produto in lista_produtos}
    origens_por_id = {origem['id_origem']: origem for origem in lista_origem}
    destinos_por_id = {destino['id_destino']: destino for destino in lista_destino}

    lista_transportes_produtos_origem_destino = []

    # Loop para executar a combinação
    for transporte in lista_transportes:
        id_produto = transporte['id_produto']
        id_origem = transporte['id_origem']
        id_destino = transporte['id_destino']

        # Combina os dados do produto se disponível
        if id_produto in produtos_por_id:
            combinado = {**transporte, **produtos_por_id[id_produto]}

        # Adiciona os dados de origem se disponíveis
        if id_origem in origens_por_id:
            combinado = {**combinado, **origens_por_id[id_origem]}

        # Adiciona os dados de destino se disponíveis
        if id_destino in destinos_por_id:
            combinado = {**combinado, **destinos_por_id[id_destino]}

        # Adiciona o combinado à lista final
        lista_transportes_produtos_origem_destino.append(combinado)

    return lista_transportes_produtos_origem_destino


def selecionar_id_transporte(lista_ids_transportes: list) -> int:
    # Solicita e valida o ID do transporte para atualizar status
    while True:
        try:
            id_transporte = int(input(
                f'\n➡️   Informe o ID do transporte para iniciar a entrega e o monitoramento: '))
        except ValueError:
            print('\n🚫  Por favor, insira apenas dígitos.')
            continue

        id_valido = verificar_valor_na_lista(
            id_transporte, lista_ids_transportes)

        if id_valido:
            break
        else:
            print(f'\n⚠️   Id de transporte não encontrado, tente novamente.')

    return id_transporte
