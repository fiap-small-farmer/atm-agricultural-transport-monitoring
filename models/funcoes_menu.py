import json
import os
from models.procedimentos_menu import limpar_tela_e_exibir_titulo
from models.funcoes_registrar_transporte import exibicao_e_selecao_categoria, exibicao_e_selecao_produtos, quantidade_para_transporte, solicitar_e_exibir_cep, dados_produtora_ou_comprador_agricola, numero_endereco_localizacao, data_frame_dados


def registrar_transporte() -> None:
    # Captura o diretório atual
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    lista_produtos_json = os.path.join(
        dir_atual, '../data/lista_produtos_agro.json')

    # Carrega os dados do arquivo JSON e converte para tipo dict
    with open(lista_produtos_json, 'r', encoding='utf-8') as file:
        dados_categoria_produto_json = file.read()
        dados_categoria_produto = json.loads(dados_categoria_produto_json)

    # Exibi as categorias de produtos agropecuário e retorna os produtos da categoria selecionada
    produtos_selecao_categoria = exibicao_e_selecao_categoria(
        dados_categoria_produto)

    # Exibi os produtos da categoria selecionada e retorna os itens do produto selecionado
    itens_selecao_produtos = exibicao_e_selecao_produtos(
        produtos_selecao_categoria)

    # Altera estrutura de dados do produto para melhor exibição
    for produto, detalhes in itens_selecao_produtos.items():
        itens_selecao_produtos = {'produto': produto.replace("_", " ").upper()}
        itens_selecao_produtos.update(detalhes)

    # Captura a quantidade de itens do produto selecionado para transporte
    quantidade_item_transporte = quantidade_para_transporte(
        itens_selecao_produtos)

    # Adiciona a quantidade do produto a ser transportado no dicionário do produto
    itens_selecao_produtos['quantidade'] = quantidade_item_transporte 

    # Captura dados de Origem para Transporte
    endereco_origem = solicitar_e_exibir_cep('ORIGEM')

    # Capturar numero do endereço de origem:
    numero_endereco_origem = numero_endereco_localizacao()

    # Adiciona o numero da localizacao no dicionário de endereco de origem
    endereco_origem['numero'] = numero_endereco_origem

    # Capturar dados da produtora agricola
    nome_produtora_agricola = dados_produtora_ou_comprador_agricola(
        'PRODUTORA')

    # Criar um dicionario dados de ORIGEM com a localizacao e o nome do produtor
    dados_origem = {
        'localizacao': endereco_origem,
        'nome_produtora_agricola': nome_produtora_agricola
    }

    # Captura dados de Destino para Transporte
    endereco_destino = solicitar_e_exibir_cep('DESTINO')

    # Capturar numero do endereço de destino:
    numero_endereco_destino = numero_endereco_localizacao()

    # Adiciona o numero da localizacao no dicionário de endereco de destino
    endereco_destino['numero'] = numero_endereco_destino

    # Capturar dados do comprador agricola
    nome_comprador_agricola = dados_produtora_ou_comprador_agricola(
        'COMPRADOR')

    # Criar um dicionario dados de DESTINO com a localizacao e nome do comprador
    dados_destino = {
        'localizacao': endereco_destino,
        'nome_comprador_agricola': nome_comprador_agricola
    }

    # Exibição dos dados de registro de forma estruturada para confirmação
    data_frame_dados(itens_selecao_produtos, dados_origem, dados_destino)


def consultar_status_transporte() -> None:
    limpar_tela_e_exibir_titulo('--- 📝 CONSULTAR STATUS DE TRANSPORTES ---')


def consultar_todos_transportes() -> None:
    limpar_tela_e_exibir_titulo('--- 📑 CONSULTAR TODOS OS TRANSPORTES ---')
