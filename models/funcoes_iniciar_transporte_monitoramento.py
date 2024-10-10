from models.funcoes_dataBase import consultar_produto, consultar_origem, consultar_destino
import pandas as pd


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


def exibir_dados_estruturado(lista_transportes_produtos_origem_destino: list) -> None:
    for transporte_produto in lista_transportes_produtos_origem_destino:
        dados_transporte_produto = {
            'Parâmetro': ['ID TRANSPORTE', 'Status', 'Temperatura de Monitoramento ºc', 'Produto', 'Quantidade', 'Unidade de Transporte', 'Tipo de Caminhão', 'Instruções de Transporte'],
            'Valor': [
                transporte_produto.get('id_transporte'),
                transporte_produto.get('status_transporte'),
                transporte_produto.get('temp_monitorada') if transporte_produto.get(
                    'temp_monitorada') is not None else 'N/A',
                transporte_produto.get('produto'),
                transporte_produto.get('quantidade'),
                transporte_produto.get('und_transporte'),
                transporte_produto.get('tipo_caminhao'),
                transporte_produto.get('instrucoes')
            ]
        }

        dados_transporte_origem = {
            'Parâmetro': ['Nome Produtor', 'Cep', 'Endereço', 'Número', 'Cidade', 'Estado'],
            'Valor': [
                transporte_produto.get('nome_produtora'),
                transporte_produto.get('cep_origem'),
                transporte_produto.get('endereco_origem'),
                transporte_produto.get('numero_origem'),
                transporte_produto.get('cidade_origem'),
                transporte_produto.get('Estado_origem')
            ]
        }

        dados_transporte_destino = {
            'Parâmetro': ['Nome Comprador', 'Cep', 'Endereço', 'Número', 'Cidade', 'Estado'],
            'Valor': [
                transporte_produto.get('nome_comprador'),
                transporte_produto.get('cep_destino'),
                transporte_produto.get('endereco_destino'),
                transporte_produto.get('numero_destino'),
                transporte_produto.get('cidade_destino'),
                transporte_produto.get('Estado_destino')
            ]
        }

        # Estruturando os dados com pandas
        transporte_produto_df = pd.DataFrame(dados_transporte_produto)
        transporte_origem_df = pd.DataFrame(dados_transporte_origem)
        transporte_destino_df = pd.DataFrame(dados_transporte_destino)

        # Ajustar a largura para exibição completa
        pd.set_option('display.width', 500)

        # Exibindo os DataFrames em formato de tabela com alinhamento à esquerda
        print(f"\n🟠  DADOS DE TRANSPORTE:\n")
        for index, row in transporte_produto_df.iterrows():
            print(f"{row['Parâmetro']:<35} {row['Valor']:<35}")

        print(f"\n🔵  LOCAL DE ORIGEM:\n")
        for index, row in transporte_origem_df.iterrows():
            print(f"{row['Parâmetro']:<35} {row['Valor']:<35}")

        print(f"\n🟢  LOCAL DESTINO:\n")
        for index, row in transporte_destino_df.iterrows():
            print(f"{row['Parâmetro']:<35} {row['Valor']:<35}")

        print('\n----------------------------------------------------------')


def combinar_dados(lista_transportes: list, lista_produtos: list, lista_origem: list, lista_destino: list) -> list:
    # Combina as listas de transportes com a lista de produtos, origem e destino
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