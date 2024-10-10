import json
import os

from models.procedimentos_menu import limpar_tela_e_exibir_titulo
from models.funcoes_registrar_transporte import exibicao_e_selecao_categoria, exibicao_e_selecao_produtos, quantidade_para_transporte, solicitar_e_exibir_cep, dados_produtora_ou_comprador_agricola, numero_endereco_localizacao, data_frame_dados
from models.funcoes_iniciar_transporte_monitoramento import consultar_dados_produto, consultar_dados_origem, consultar_dados_destino, exibir_dados_estruturado, combinar_dados, selecionar_id_transporte
from models.funcoes_dataBase import registro_dados, listar_dados_transporte_monitoramento, atualizar_status_transporte


def registrar_transporte() -> None:
    while True:
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
            itens_selecao_produtos = {
                'produto': produto.replace("_", " ").upper()}
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

        # Confirmação dos dados para registro no banco de dados
        while True:
            confirmar_registro_dados = input(
                '\n\n⚠️   OS DADOS PARA REGISTRO ESTÃO CORRETOS? (S/N): ').upper()

            if confirmar_registro_dados == 'S':
                # Função para salvar dados no banco de dados
                confirmacao_registro = registro_dados(
                    itens_selecao_produtos, dados_origem, dados_destino)

                # Verifica se não ocorreu nenhum erro ao salvar dados no banco de dados
                if confirmacao_registro:
                    print(
                        '\n✅  Dados registrados com SUCESSO')
                    confirmar_registro_dados = True
                    break

                else:
                    confirmar_registro_dados = False
                    break

            elif confirmar_registro_dados == 'N':
                input(
                    '\n⚠️   Dados NÃO registrados, clique [ENTER] para efetuar um novo registro.')
                break

            else:
                print('\n🚫  Por favor, insira [S] para SIM ou [N] para NÃO.')

        # Verifica se dados foram salvos no banco de dados, qualquer opcao diferente de TRUE retorna o Loop para iniciar novo registro
        if confirmar_registro_dados == True:
            break

        elif confirmar_registro_dados == False:
            input(
                '\n🚫  Erro ao salvar registro no banco de dados, clique [ENTER] para efetuar um novo registro.')


def iniciar_transporte_monitoramento() -> None:
    limpar_tela_e_exibir_titulo('--- 📝 INICIAR TRANSPORTE E MONITORAMENTO ---')

    # Busca no banco de dados todos os transportes com status "Não iniciado"
    lista_transportes = listar_dados_transporte_monitoramento()

    # Se o retorno de transportes do banco de dados for vazio, informa ao usuário uma mensagem
    if len(lista_transportes) > 0:
        # Efetua a consulta de todos os produtos, origens e destinos vinculados aos transportes criados e retorna uma lista dos mesmos
        lista_produtos = consultar_dados_produto(lista_transportes)
        lista_origem = consultar_dados_origem(lista_transportes)
        lista_destino = consultar_dados_destino(lista_transportes)

        # Combina os dados da Lista de transporte, produto, origem e destino em uma único dicionário
        lista_transportes_produtos_origem_destino = combinar_dados(
            lista_transportes, lista_produtos, lista_origem, lista_destino)

        # Exibi os dados de forma estruturada usando pandas
        exibir_dados_estruturado(lista_transportes_produtos_origem_destino)

        # Cria uma lista de Ids dos transportes que consta com status "Não iniciado"
        lista_ids_transportes = []
        for transporte in lista_transportes:
            transporte_id = transporte.get("id_transporte")
            lista_ids_transportes.append(transporte_id)

        # Solicita e valida o ID do transporte para atualizar status
        id_transporte = selecionar_id_transporte(lista_ids_transportes)

        # Alteração do status do transporte para Em andamento
        status_transporte = 'Em andamento'

        # Atualiza o status no banco de dados
        confirmacao_atualizacao_status = atualizar_status_transporte(
            id_transporte, status_transporte)

        if confirmacao_atualizacao_status:
            print(f"""\n✅   Status do transporte com o ID número {
                  id_transporte} atualizado para '{status_transporte}'""")
            
        else:
            print(f'\n🚫  Status não atualizado, tente novamente.')

    else:
        return print('↘️   Nenhum transporte "registrado" ou com status "Não iniciado".')


def consultar_status_transporte() -> None:
    limpar_tela_e_exibir_titulo('--- 📝 CONSULTAR STATUS DE TRANSPORTES ---')


def consultar_todos_transportes() -> None:
    limpar_tela_e_exibir_titulo('--- 📝 CONSULTAR TODOS OS TRANSPORTES ---')
