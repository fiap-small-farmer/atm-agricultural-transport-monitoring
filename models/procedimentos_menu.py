import os
from typing import Callable


def limpar_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def voltar_menu(opcao_selecionada: Callable) -> None:
    opcao_selecionada()
    input('\n⚠️   Digite qualquer tecla para retornar ao menu')
    limpar_terminal()


def limpar_tela_e_exibir_titulo(titulo: str) -> None:
    limpar_terminal()
    print(f'{titulo}\n')
