import requests
import pandas as pd
from prettytable import PrettyTable

from models.procedimentos_menu import limpar_tela_e_exibir_titulo
from models.validacao_dados import validacao_opcoes_menu, verificar_valores_nulos


def exibicao_e_selecao_categoria(dados_categoria_produto: dict) -> dict:
    # Cria uma lista de categorias de produtos para seleção
    limpar_tela_e_exibir_titulo('--- 📦 REGISTRAR TRANSPORTE ---')
    print('Selecione uma categoria:\n')

    # Cria uma lista em ordem alfabética das categorias
    categorias = sorted(dados_categoria_produto.keys())

    # Exibi a lista das categorias agro
    for index, categoria in enumerate(categorias):
        print(f'{index:2} - {categoria.replace("_", " ").upper()}')

    # Captura a seleção da categoria com validação
    while True:
        # Valida se a opção é um dígito
        selecao_categoria = validacao_opcoes_menu()

        # Verifica se a seleção está dentro do intervalo válido
        if 0 <= selecao_categoria < len(categorias):
            selecao_categoria = categorias[selecao_categoria]
            break
        else:
            print('\n⚠️   Seleção fora do intervalo, tente novamente.')

    # Armazena os produtos baseado na categoria selecionada
    itens_selecao_categoria = dados_categoria_produto.get(selecao_categoria)

    return itens_selecao_categoria


def exibicao_e_selecao_produtos(produtos_selecao_categoria: dict) -> dict:
    # Cria uma lista de produtos da categoria selecionada
    limpar_tela_e_exibir_titulo('--- 📦 REGISTRAR TRANSPORTE ---')
    print('Selecione um produto:\n')

    # Cria uma lista em ordem alfabética dos produtos da categoria selecionada
    produtos = sorted(produtos_selecao_categoria)

    # Exibi a lista dos produtos agro
    for index, produto in enumerate(produtos):
        print(f'{index:2} - {produto.replace("_", " ").upper()}')

    # Captura a seleção do produto com validação
    while True:
        # Valida se a opção é um dígito
        selecao_produto = validacao_opcoes_menu()

        # Verifica se a seleção está dentro do intervalo válido
        if 0 <= selecao_produto < len(produtos):
            selecao_produto = produtos[selecao_produto]
            break
        else:
            print('\n⚠️   Seleção fora do intervalo, tente novamente.')

    # Armazena os itens do produto baseado na seleção em um dict com o nome do produto
    selecao_produto = {
        selecao_produto: produtos_selecao_categoria.get(selecao_produto)
    }

    return selecao_produto


def quantidade_para_transporte(produto: dict) -> int:
    # Captura dentro do dicionario o produto e a unidade de transporte
    nome_produto = produto.get('produto')
    unidade_transporte = produto.get('unidade_transporte')

    limpar_tela_e_exibir_titulo('--- 📦 REGISTRAR TRANSPORTE ---')

    # Valida e captura o valor da quantidade exibindo sua respectiva unidade
    try:
        quantidade_item_para_transporte = int(
            input(f'Informe a quantidade de {nome_produto.replace("_", " ").upper()} para transporte em sua unidade  ☛  {unidade_transporte.upper()}: '))

    except:
        while True:
            quantidade_item_para_transporte = input(
                '\n⚠️   Digite uma opção válida: ')

            if quantidade_item_para_transporte.isdigit():
                quantidade_item_para_transporte = int(
                    quantidade_item_para_transporte)
                break

            else:
                print('\n🚫  Por favor, insira apenas dígitos.')

    return quantidade_item_para_transporte


def busca_cep(cep: str) -> dict:
    # URL da API via cep para requisição
    url = f'https://viacep.com.br/ws/{cep}/json/'

    # Valida a requisição, se nao houver erro retorna o dicionario com os dados da localização
    try:
        response = requests.get(url)
        response.raise_for_status()
        endereco = response.json()

        if 'erro' in endereco:
            return None

        return endereco

    # Se ocorrer erro de requisição exibi o erro em tela para tratamento
    except Exception as error:
        print(f'\nOcorreu um erro ao consultar o CEP: {error}')
        return None


def solicitar_e_exibir_cep(tipo: str) -> dict:
    # Solicita o CEP até que um válido seja fornecido, encontrado e confirmado
    limpar_tela_e_exibir_titulo('--- 📦 REGISTRAR TRANSPORTE ---')

    # Loop para confirmar se a localização está correta
    while True:
        cep = input(f'Informe o CEP de {tipo} (8 dígitos): ')

        # Verifica se o cep digitado tem 8 dígitos e é somente digito
        if cep.isdigit() and len(cep) == 8:
            endereco = busca_cep(cep)

            # Verifica se o retorno da API via cep localizou o cep digitado
            if endereco:
                # Criar uma nova tabela com os nomes das colunas
                table_cep = PrettyTable()
                table_cep.field_names = [
                    'CEP', 'ENDEREÇO', 'BAIRRO', 'CIDADE', 'ESTADO']

                # Definir alinhamento das colunas
                table_cep.align = 'l'  # Alinhamento à esquerda

                table_cep.add_row([
                    endereco.get('cep'),
                    endereco.get('logradouro'),
                    endereco.get('bairro'),
                    endereco.get('localidade'),
                    endereco.get('uf')
                ])

                # Deixando o título dinâmico
                if tipo == 'ORIGEM':
                    ponto = '🔵'
                elif tipo == 'DESTINO':
                    ponto = '🟢'

                # Exibindo dados em formato tabela para melhor visualização
                print(f"\n\n{ponto}  LOCALIZAÇÃO DE {
                      tipo} PARA CONFIRMAÇÃO:\n")
                print(table_cep)

                # Validação para confirmar se o cep encontrado é o correto
                while True:
                    confirmacao = input(
                        '\nO endereço está correto? (S/N): ').strip().upper()

                    if confirmacao == 'S':
                        endereco = {
                            'cep': endereco["cep"],
                            'endereco': endereco["logradouro"],
                            'bairro': endereco["bairro"],
                            'cidade': endereco["localidade"],
                            'estado': endereco["uf"]
                        }

                        return endereco

                    elif confirmacao == 'N':
                        print(
                            '\n⚠️   Por favor, tente novamente com um CEP correto.\n')
                        break
                    else:
                        print(
                            '\n🚫  Por favor, digite [S] para sim ou [N] para não.')

                if confirmacao == 'S':
                    break

            else:
                print('\n🚫  CEP não encontrado. Por favor, insira um CEP válido.\n')

        else:
            print('\n🚫  Por favor, insira um CEP válido com 8 dígitos apenas.\n')


def numero_endereco_localizacao() -> int:
    try:
        numero_endereco = int(input(f'\nInforme o número do endereço: '))

    except:
        while True:
            numero_endereco = input('\n⚠️   Digite uma opção válida: ')

            if numero_endereco.isdigit():
                numero_endereco = int(numero_endereco)
                break
            else:
                print('\n🚫  Por favor, insira apenas dígitos.')

    return numero_endereco


def dados_produtora_ou_comprador_agricola(tipo: str) -> str:
    # Solicita o CEP até que um válido seja fornecido, encontrado e confirmado
    limpar_tela_e_exibir_titulo('--- 📦 REGISTRAR TRANSPORTE ---')

    # Captura e valida o nome do produtor
    while True:
        nome_produtor = input(f'Informe o nome d{'a' if tipo == 'PRODUTORA' else 'o'} {
                              tipo} AGRÍCOLA: ').strip()

        # Verifica se o nome está vazio
        if not nome_produtor:
            print('\n🚫  O nome não pode estar vazio. Por favor, insira um nome válido.\n')

        # Verifica se o nome tem mais de 10 caracteres
        elif len(nome_produtor) > 30:
            print('\n🚫  O nome não pode ter mais que 10 caracteres.')

        else:
            return nome_produtor


def data_frame_dados1(produto: dict, origem: dict, destino: dict) -> None:
    # Limpa e ajusta os valores nulos para "N/A"
    produto = verificar_valores_nulos(produto)
    origem = verificar_valores_nulos(origem)
    destino = verificar_valores_nulos(destino)

    limpar_tela_e_exibir_titulo('--- 📦 REGISTRAR TRANSPORTE ---')

    # Dados de entrada do produto
    produto_data = {
        'Parâmetro': ['Produto', 'Quantidade', 'Unidade de Transporte', 'Temperatura Mínima ºc', 'Temperatura Máxima ºc', 'Instruções', 'Tipo de Caminhão'],
        'Valor': [
            produto.get('produto', 'N/A'),
            produto.get('quantidade', 'N/A'),
            produto.get('unidade_transporte', 'N/A'),
            produto.get('min', 'N/A'),
            produto.get('max', 'N/A'),
            produto.get('instruções', 'N/A'),
            produto.get('tipo_caminhao', 'N/A')
        ]
    }

    # Dados de origem (produtora)
    produtora_data = {
        'Parâmetro': ['Nome da produtora', 'CEP', 'Endereço', 'Número', 'Bairro', 'Cidade', 'Estado'],
        'Valor': [
            origem.get('nome_produtora_agricola', 'N/A'),
            origem.get('localizacao', {}).get('cep', 'N/A'),
            origem.get('localizacao', {}).get('endereco', 'N/A'),
            origem.get('localizacao', {}).get('numero', 'N/A'),
            origem.get('localizacao', {}).get('bairro', 'N/A'),
            origem.get('localizacao', {}).get('cidade', 'N/A'),
            origem.get('localizacao', {}).get('estado', 'N/A')
        ]
    }

    # Dados de destino (comprador)
    comprador_data = {
        'Parâmetro': ['Nome do comprador', 'CEP', 'Endereço', 'Número', 'Bairro', 'Cidade', 'Estado'],
        'Valor': [
            destino.get('nome_comprador_agricola', 'N/A'),
            destino.get('localizacao', {}).get('cep', 'N/A'),
            destino.get('localizacao', {}).get('endereco', 'N/A'),
            destino.get('localizacao', {}).get('numero', 'N/A'),
            destino.get('localizacao', {}).get('bairro', 'N/A'),
            destino.get('localizacao', {}).get('cidade', 'N/A'),
            destino.get('localizacao', {}).get('estado', 'N/A')
        ]
    }

    # Estruturando os dados com pandas
    produto_df = pd.DataFrame(produto_data)
    produtora_df = pd.DataFrame(produtora_data)
    comprador_df = pd.DataFrame(comprador_data)

    # Ajustar a largura para exibição completa
    pd.set_option('display.width', 500)

    # Exibindo os DataFrames em formato de tabela com alinhamento à esquerda
    print("📝 DADOS PRODUTO:\n")
    for index, row in produto_df.iterrows():
        print(f"{row['Parâmetro']:<30} {row['Valor']:<30}")

    print("\n📝 DADOS ORIGEM:\n")
    for index, row in produtora_df.iterrows():
        print(f"{row['Parâmetro']:<30} {row['Valor']:<30}")

    print("\n📝 DADOS DESTINO:\n")
    for index, row in comprador_df.iterrows():
        print(f"{row['Parâmetro']:<30} {row['Valor']:<30}")


def data_frame_dados(produto: dict, origem: dict, destino: dict) -> None:
    # Limpa e ajusta os valores nulos para "N/A"
    produto = verificar_valores_nulos(produto)
    origem = verificar_valores_nulos(origem)
    destino = verificar_valores_nulos(destino)

    limpar_tela_e_exibir_titulo('--- 📦 REGISTRAR TRANSPORTE ---')

    # Criar uma nova tabela com os nomes das colunas
    table_produto = PrettyTable()
    table_origem = PrettyTable()
    table_destino = PrettyTable()

    table_produto.field_names = ['PRODUTO', 'QTD.', 'UND. DE TRANSPORTE','TEMP. MÍNIMA ºC', 'TEMP. MÁXIMA ºC', 'INSTRUÇÕES', 'TIPO DE CAMINHÃO']
    table_origem.field_names = ['NOME DA PRODUTORA', 'CEP','ENDEREÇO', 'NÚMERO', 'BAIRRO', 'CIDADE', 'ESTADO']
    table_destino.field_names = ['NOME COMPRADOR', 'CEP','ENDEREÇO', 'NÚMERO', 'BAIRRO', 'CIDADE', 'ESTADO']

    # Definir alinhamento das colunas
    table_produto.align = 'l'  # Alinhamento à esquerda
    table_origem.align = 'l'  # Alinhamento à esquerda
    table_destino.align = 'l'  # Alinhamento à esquerda

    # Dados de entrada do produto
    table_produto.add_row([
        produto.get('produto'),
        str(produto.get('quantidade')),
        produto.get('unidade_transporte'),
        str(produto.get('min')),
        str(produto.get('max')),
        produto.get('instruções'),
        produto.get('tipo_caminhao')
    ])

    # Dados de origem (produtora)
    table_origem.add_row([
        origem.get('nome_produtora_agricola'),
        origem.get('localizacao', {}).get('cep'),
        origem.get('localizacao', {}).get('endereco'),
        str(origem.get('localizacao', {}).get('numero')),
        origem.get('localizacao', {}).get('bairro'),
        origem.get('localizacao', {}).get('cidade'),
        origem.get('localizacao', {}).get('estado')
    ])

    # Dados de destino (comprador)
    table_destino.add_row([
        destino.get('nome_comprador_agricola'),
            destino.get('localizacao', {}).get('cep'),
            destino.get('localizacao', {}).get('endereco'),
            str(destino.get('localizacao', {}).get('numero')),
            destino.get('localizacao', {}).get('bairro'),
            destino.get('localizacao', {}).get('cidade'),
            destino.get('localizacao', {}).get('estado')
    ])

    # Exibindo os DataFrames em formato de tabela com alinhamento à esquerda
    print("\n🟡  DADOS PRODUTO:\n")
    print(table_produto)

    print("\n🔵  DADOS ORIGEM:\n")
    print(table_origem)

    print("\n🟢  DADOS DESTINO:\n")
    print(table_destino)

