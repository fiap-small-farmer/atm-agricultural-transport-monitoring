from dotenv import load_dotenv
import os
import oracledb
from models.procedimentos_menu import limpar_terminal
from models.validacao_entrada_dados import verificar_valores_nulos


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
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO ORACLE DATABASE {Erro}')
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
            f'\n☛  Aperte [ENTER] para continuar\n\nERRO DE REGISTRO ORACLE DATABASE {erro}')
        
        return False
