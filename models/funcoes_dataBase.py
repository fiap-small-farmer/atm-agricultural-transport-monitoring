from dotenv import load_dotenv
import os
import oracledb

from models.procedimentos_menu import limpar_terminal
from models.validacao_dados import verificar_valores_nulos

def conexao_banco_de_dados() -> bool:
    load_dotenv()
    usuario = os.getenv('USER')
    senha = os.getenv('PASSWORD')
    dns = os.getenv('DNS')

    global conn, cursor, inst_registrar, inst_consultar, inst_atualizar, inst_deletar

    try:
        conn = oracledb.connect(
            user=usuario,
            password=senha,
            dsn=dns
        )

        cursor = conn.cursor()
        inst_registrar = conn.cursor()
        inst_consultar = conn.cursor()
        inst_atualizar = conn.cursor()
        inst_deletar = conn.cursor()

    except Exception as Erro:
        input(
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO CONEXÃO ORACLE DATABASE {Erro}')
        conexao = False
        return conexao

    else:
        conexao = True
        return conexao

    finally:
        limpar_terminal()
        print(f"📡  Status conexão banco de dados ORACLE: {
              'Conectado ✅' if conexao else 'NÃO conectado 🚫'}\n")


def registro_dados(produto: dict, origem: dict, destino: dict) -> bool:
    # Limpa e ajusta os valores nulos para "N/A"
    produto = verificar_valores_nulos(produto)
    origem = verificar_valores_nulos(origem)
    destino = verificar_valores_nulos(destino)

    try:
        # Instrução SQL para a tabela Produto com retorno do ID
        registro_produto = """
        INSERT INTO Produto
        (Produto, Quantidade, Unidade_Transporte, Temperatura_Minima,
         Temperatura_Maxima, Instrucoes, Tipo_Caminhao)
        VALUES (
            :produto,
            :quantidade,
            :unidade_transporte,
            :min,
            :max,
            :instrucoes,
            :tipo_caminhao
        )
        RETURNING ID_Produto INTO :id_produto
        """

        # Instrução SQL para a tabela Origem com retorno do ID
        registro_origem = """
        INSERT INTO Origem
        (Nome_Produtora, CEP, Endereco, Numero,
         Bairro, Cidade, Estado)
        VALUES (
            :nome_produtora,
            :cep,
            :endereco,
            :numero,
            :bairro,
            :cidade,
            :estado
        )
        RETURNING ID_Origem INTO :id_origem
        """

        # Instrução SQL para a tabela Destino com retorno do ID
        registro_destino = """
        INSERT INTO Destino
        (Nome_Comprador, CEP, Endereco, Numero,
         Bairro, Cidade, Estado)
        VALUES (
            :nome_comprador,
            :cep,
            :endereco,
            :numero,
            :bairro,
            :cidade,
            :estado
        )
        RETURNING ID_Destino INTO :id_destino
        """

        # Instrução SQL para a tabela Transporte com todos os IDs retornados
        registro_transporte = """
        INSERT INTO Transporte
        (ID_Produto, ID_Origem, ID_Destino, Status_Transporte, Temperatura_Monitorada)
        VALUES (
            :id_produto,
            :id_origem,
            :id_destino,
            :status_transporte,
            NULL  -- Temperatura iniciando como null
        )
        """

        # Preparando as variáveis para armazenar o ID gerado
        id_produto = cursor.var(oracledb.NUMBER)
        id_origem = cursor.var(oracledb.NUMBER)
        id_destino = cursor.var(oracledb.NUMBER)

        # Executando a instrução SQL para a tabela produto com retorno do ID e confirmando registro
        inst_registrar.execute(registro_produto, {
            'produto': produto.get('produto'),
            'quantidade': produto.get('quantidade'),
            'unidade_transporte': produto.get('unidade_transporte'),
            'min': str(produto.get('min')),
            'max': str(produto.get('max')),
            'instrucoes': produto.get('instruções'),
            'tipo_caminhao': produto.get('tipo_caminhao'),
            'id_produto': id_produto
        })
        conn.commit()

        # Executando a instrução SQL para a tabela origem com retorno do ID e confirmando registro
        inst_registrar.execute(registro_origem, {
            'nome_produtora': origem.get('nome_produtora_agricola'),
            'cep': origem.get('localizacao').get('cep'),
            'endereco': origem.get('localizacao').get('endereco'),
            'numero': origem.get('localizacao').get('numero'),
            'bairro': origem.get('localizacao').get('bairro'),
            'cidade': origem.get('localizacao').get('cidade'),
            'estado': origem.get('localizacao').get('estado'),
            'id_origem': id_origem
        })
        conn.commit()

        # Executando a instrução SQL para a tabela destino com retorno do ID e confirmando registro
        inst_registrar.execute(registro_destino, {
            'nome_comprador': destino.get('nome_comprador_agricola'),
            'cep': destino.get('localizacao').get('cep'),
            'endereco': destino.get('localizacao').get('endereco'),
            'numero': destino.get('localizacao').get('numero'),
            'bairro': destino.get('localizacao').get('bairro'),
            'cidade': destino.get('localizacao').get('cidade'),
            'estado': destino.get('localizacao').get('estado'),
            'id_destino': id_destino
        })
        conn.commit()

        # Recuperando os IDs gerados ao criar as tabelas (produto, origem e destino) e convertendo para tipo int
        id_inserido_produto = id_produto.getvalue()
        id_inserido_produto = int(id_inserido_produto[0])

        id_inserido_origem = id_origem.getvalue()
        id_inserido_origem = int(id_inserido_origem[0])

        id_inserido_destino = id_destino.getvalue()
        id_inserido_destino = int(id_inserido_destino[0])

        # Executando a instrução SQL para a tabela Transporte com todos os IDs recuperados das tabelas (produto, origem e destino)
        inst_registrar.execute(registro_transporte, {
            'id_produto': id_inserido_produto,
            'id_origem': id_inserido_origem,
            'id_destino': id_inserido_destino,
            'status_transporte': 'Não iniciado'
        })
        conn.commit()

        return True

    except Exception as erro:
        input(
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO DE REGISTRO DE DADOS ORACLE DATABASE {erro}')

        return False


def consultar_transporte_por_status(status: str) -> list:
    try:
        # Instrução SQL para consultar dados do transporte mediante ao status
        if status == 'todos':
            registro = """
                SELECT * FROM Transporte
                """
            # Consulta na tabela transporte todos os dados
            inst_consultar.execute(registro)

        else:
            registro = f"""
            SELECT * FROM Transporte
            WHERE Status_Transporte = :status
            """
            # Consulta na tabela transporte de todos os dados que atende a condição da instrução
            inst_consultar.execute(registro, {"status": status})

        # Recupera todos os dados que atendem à condição
        dados_consulta = inst_consultar.fetchall()

        # Transforma a lista de tuplas em uma lista de dicionários
        dados_consulta = [
            {
                'id_transporte': tupla[0],
                'id_produto': tupla[1],
                'id_origem': tupla[2],
                'id_destino': tupla[3],
                'status_transporte': tupla[4],
                'temp_monitorada': tupla[5]
            }
            for tupla in dados_consulta
        ]

        # retorna os dados consultados
        return dados_consulta

    except Exception as erro:
        input(
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO DE CONSULTA TRANSPORTES ORACLE DATABASE {erro}')


def consultar_produto(produto_id: int) -> list:
    try:
        # Instrução SQL para consultar dados do Produto mediante ao Id do Produto
        registro = f"""SELECT * FROM Produto WHERE ID_Produto = :id_produto"""

        # Consulta na tabela produto, retorna todos os dados que atende a condição da instrução
        inst_consultar.execute(registro, {"id_produto": produto_id})

        # Recupera todos os dados que atendem à condição
        dados_consulta = inst_consultar.fetchall()

        # Transforma a lista de tuplas em uma lista de dicionários
        dados_consulta = [
            {
                'id_produto': tupla[0],
                'produto': tupla[1],
                'quantidade': tupla[2],
                'und_transporte': tupla[3],
                'temp_minima': tupla[4],
                'temp_maxima': tupla[5],
                'instrucoes': tupla[6],
                'tipo_caminhao': tupla[7]
            }
            for tupla in dados_consulta
        ]

    except Exception as erro:
        input(
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO DE CONSULTA PRODUTOS ORACLE DATABASE {erro}')

    finally:
        # retorna os dados consultados
        return dados_consulta


def consultar_origem(id_origem: int) -> list:
    try:
        # Instrução SQL para consultar dados de Origem mediante ao Id da origem
        registro_consulta = f"""SELECT * FROM Origem WHERE ID_Origem = :id_origem"""

        # Consulta na tabela Origem, retorna todos os dados que atende a condição da instrução
        inst_consultar.execute(registro_consulta, {"id_origem": id_origem})

        # Recupera todos os dados que atendem à condição
        dados_consulta = inst_consultar.fetchall()

        # Transforma a lista de tuplas em uma lista de dicionários
        dados_consulta = [
            {
                'id_origem': tupla[0],
                'nome_produtora': tupla[1],
                'cep_origem': tupla[2],
                'endereco_origem': tupla[3],
                'numero_origem': tupla[4],
                'cidade_origem': tupla[6],
                'Estado_origem': tupla[7]
            }
            for tupla in dados_consulta
        ]

    except Exception as erro:
        input(
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO DE CONSULTA ORIGEM ORACLE DATABASE {erro}')

    finally:
        # retorna os dados consultados
        return dados_consulta


def consultar_destino(id_destino: int) -> list:
    try:
        # Instrução SQL para consultar dados de Destino mediante ao Id do destino
        registro = f"""SELECT * FROM Destino WHERE ID_Destino = :id_destino"""

        # Consulta na tabela Destino, retorna todos os dados que atende a condição da instrução
        inst_consultar.execute(registro, {"id_destino": id_destino})

        # Recupera todos os dados que atendem à condição
        dados_consulta = inst_consultar.fetchall()

        # Transforma a lista de tuplas em uma lista de dicionários
        dados_consulta = [
            {
                'id_destino': tupla[0],
                'nome_comprador': tupla[1],
                'cep_destino': tupla[2],
                'endereco_destino': tupla[3],
                'numero_destino': tupla[4],
                'cidade_destino': tupla[6],
                'Estado_destino': tupla[7]
            }
            for tupla in dados_consulta
        ]

    except Exception as erro:
        input(
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO DE CONSULTA DESTINO ORACLE DATABASE {erro}')

    finally:
        # retorna os dados consultados
        return dados_consulta


def atualizar_status_transporte(id_transporte: int, status: str) -> bool:
    # Atualiza o status do transporte mediante ao status passado como parâmetro
    try:
        # Instrução SQL para atualizar o status pelo Id do transporte
        registro = f"""
            UPDATE Transporte
            SET Status_Transporte = :status
            WHERE ID_Transporte = :id_transporte
            """

        # Executa a atualização com as instruções do registro
        inst_atualizar.execute(
            registro, {"status": status, "id_transporte": id_transporte})
        conn.commit()

        return True

    except Exception as erro:
        input(
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO DE ATUALIZAÇÃO STATUS ORACLE DATABASE {erro}')

        return False


def atualizar_temperatura_monitorada_banco_dados(lista_temp_monitorada: list) -> bool:
    # Captura os dados para atualização
    id_transporte = lista_temp_monitorada.get('id_transporte')
    temperatura_Monitorada = lista_temp_monitorada.get('temp_media_monitorada')


    # Atualiza a média da temperatura
    try:
        # Instrução SQL para atualizar o status pelo Id do transporte
        registro = f"""
            UPDATE Transporte
            SET Temperatura_Monitorada = :temp_media
            WHERE ID_Transporte = :id_transporte
            """

        # Executa a atualização com as instruções do registro
        inst_atualizar.execute(registro, {"temp_media": temperatura_Monitorada, "id_transporte": id_transporte})
        conn.commit()

        return True

    except Exception as erro:
        input(
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO DE ATUALIZAÇÃO TEMPERATURA DE MONITORAMENTO ORACLE DATABASE {erro}')

        return False
