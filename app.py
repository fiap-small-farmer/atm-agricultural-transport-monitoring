import sys
import threading
import time
import signal
from models.validacao_dados import validacao_opcoes_menu
from models.procedimentos_menu import voltar_menu, limpar_terminal
from models.funcoes_menu import registrar_transporte, iniciar_transporte_monitoramento, alterar_status_transporte, consultar_todos_transportes
from models.funcoes_dataBase import conexao_banco_de_dados, atualizar_temperatura_monitorada_banco_dados
from models.funcoes_monitoramento_temperatura import consulta_dados, data_hora_ptbr, registrar_log_monitoramento, calcular_media_temperatura_por_id
from models.simulador_sensor_temperatura.simulador import sensor_temperatura

# Evento para controlar o loop de monitoramento
monitoramento_event = threading.Event()

# Função para monitoramento da temperatura simulando sensor de temperatura
def monitoramento_temperatura():
    while not monitoramento_event.is_set():  # Verifica se o evento foi sinalizado
        time.sleep(3)  # Espera 3 segundos antes de imprimir novamente

        # Valor em porcentagem (%) que pode sair fora dos limites mínimos e máximo de temperatura
        tolerancia_desvio_sensor_temperatura = 10
        
        #Função que consulta os IDs de transporte em Andamento e retorna uma lista desses ids combinado com os produtos on consta as informações de temp min e max
        lista_transportes_produtos = consulta_dados()

        # Loop para executar as ações de monitoramento mediante a lista retornada
        for transporte in lista_transportes_produtos:

            ############## -> SIMULADOR <- SENSOR DE TEMPERATURA ###############
            temp_monitorada = round(sensor_temperatura(float(transporte.get(
                'temp_minima')), float(transporte.get('temp_maxima')), tolerancia_desvio_sensor_temperatura), 2)

            # Retorna data e hora local em formato pt-br para constar no log
            data_hora = data_hora_ptbr()

            temp_max = transporte.get('temp_maxima')
            temp_min = transporte.get('temp_minima')
            
            #Analisa se a temperatura esta dento dos limites cadastrados para transporte
            if temp_monitorada > float(temp_max) or temp_monitorada < float(temp_min):
                limite_temp = False
            else:
                limite_temp = True

            #Dicionário com os dados para gerar log
            dados_monitoramento = {
                'id_transporte': transporte.get('id_transporte'),
                'temp_minima': transporte.get('temp_minima'),
                'temp_maxima': transporte.get('temp_maxima'),
                'temp_monitorada': temp_monitorada,
                'dentro_intervalo': limite_temp,
                'data_hora': data_hora
            }
            
            # Cria um arquivo txt com os dados monitorados
            registrar_log_monitoramento(dados_monitoramento)

            # Ler o arquivo de log gerado e efetua uma média das temperaturas monitoradas mediante ao id informado
            lista_temp_monitorada = calcular_media_temperatura_por_id(transporte.get('id_transporte'), "log_monitoramento_transporte.txt")
            
            #Atualiza a temperatura monitorada no banco de dados
            atualizar_temperatura_monitorada_banco_dados(lista_temp_monitorada)


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
                monitoramento_event.set()  # Sinaliza para parar o monitoramento
                limpar_terminal()
                print('⚠️   SMALL FARMER TRACKING encerrado com sucesso!\n')
                sys.exit()

            case _:
                input('\n🚫  Opção inválida, tecle ENTER e tente novamente.')
                limpar_terminal()


def manipulador_de_sinal(sig, frame):
    print('\n\n🚩  Monitoramento temperatura interrompido')
    monitoramento_event.set()  # Sinaliza para parar o monitoramento


def main():
    # Configura o manipulador de sinal para SIGINT (Ctrl + C)
    signal.signal(signal.SIGINT, manipulador_de_sinal)

    conexao_db = conexao_banco_de_dados()

    if conexao_db:

        # Inicia a thread de monitoramento de temperatura
        monitor_thread = threading.Thread(target=monitoramento_temperatura)
        monitor_thread.start()

        # Inicia o menu principal
        try:
            opcoes_menu()
        except SystemExit:
            pass  # Ignora a exceção de saída para permitir o encerramento do programa

        # Aguarda a finalização da thread de monitoramento
        monitor_thread.join()

    else:
        input('⚠️   Verifique a conexão com o banco de dados e tente novamente.')
        limpar_terminal()
        sys.exit()


if __name__ == "__main__":
    main()
