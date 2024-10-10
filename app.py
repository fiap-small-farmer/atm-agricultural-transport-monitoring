import sys
from models.validacao_dados import validacao_opcoes_menu
from models.procedimentos_menu import voltar_menu, limpar_terminal
from models.funcoes_menu import registrar_transporte, iniciar_transporte_monitoramento ,alterar_status_transporte, consultar_todos_transportes
from models.funcoes_dataBase import conexao_banco_de_dados


def menu() -> None:
    print(' --- 🚚 SMALL FARMER TRACKING 🚚 ---\n')

    lista_opcoes_menu = (
        ' 1 - Registrar transporte',
        ' 2 - Iniciar transporte e monitoramento',
        ' 3 - Alterar status de transporte',
        ' 4 - Consultar todos os transportes',
        ' 5 - SAIR'
    )

    for opcao_menu in lista_opcoes_menu:
        print(opcao_menu)


def opcoes_menu() -> None:
    while True:
        menu()
        opcoes = validacao_opcoes_menu()

        match opcoes:
            case 1:
                voltar_menu(registrar_transporte)

            case 2:
                voltar_menu(iniciar_transporte_monitoramento)

            case 3:
                voltar_menu(alterar_status_transporte)

            case 4:
                voltar_menu(consultar_todos_transportes)

            case 5:
                limpar_terminal()
                print('⚠️   SMALL FARMER TRACKING encerrado com sucesso!\n')
                sys.exit()

            case _:
                input('\n🚫  Opção inválida, tecle ENTER e tente novamente.')
                limpar_terminal()


def main():
    conexao_db = conexao_banco_de_dados()

    if conexao_db:
        opcoes_menu()
    else:
        input('⚠️   Verifique a conexão com o banco de dados e tente novamente.')
        limpar_terminal()
        sys.exit()


if __name__ == "__main__":
    main()
