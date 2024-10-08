from dotenv import load_dotenv
import os
import oracledb
from models.procedimentos_menu import limpar_terminal


def conexao_banco_de_dados() -> bool:
    load_dotenv()
    usuario = os.getenv('USER')
    senha = os.getenv('PASSWORD')
    dns = os.getenv('DNS')

    global conn, inst_registrar, inst_consultar, inst_atualizar, inst_deletar

    try:
        conn = oracledb.connect(
            user=usuario,
            password=senha,
            dsn=dns
        )

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
        print(f"➡️   Status conexão banco de dados ORACLE: {
              'Conectado ✅' if conexao == True else 'NÃO conectado 🚫'}\n")
