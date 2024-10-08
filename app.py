import sys
from models.validacao_entrada_dados import validacao_opcoes_menu
from models.procedimentos_menu import voltar_menu, limpar_terminal
from models.funcoes_menu import registrar_transporte, consultar_status_transporte, consultar_todos_transportes


def menu() -> None:
    print(' --- 🚚 SMALL FARMER TRACKING 🚚 ---\n')

    lista_opcoes_menu = (
        ' 1 - Registrar transporte',
        ' 2 - Consultar status de transporte',
        ' 3 - Consultar todos os transportes',
        ' 4 - SAIR'
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
                voltar_menu(consultar_status_transporte)

            case 3:
                voltar_menu(consultar_todos_transportes)

            case 4:
                limpar_terminal()
                print('⚠️   SMALL FARMER TRACKING encerrado com sucesso!\n')
                sys.exit()

            case _:
                input('\n🚫  Opção inválida, tecle ENTER e tente novamente.')
                limpar_terminal()


def main():
    limpar_terminal()
    opcoes_menu()


if __name__ == "__main__":
    main()
