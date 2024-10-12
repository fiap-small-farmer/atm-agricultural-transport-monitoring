import os

from datetime import datetime
from models.funcoes_dataBase import consultar_transporte_por_status
from models.funcoes_iniciar_transporte_monitoramento import consultar_dados_produto


def consulta_dados() -> list:
  # Busca no banco de dados todos os transportes com status "Em andamento"
    lista_transportes = consultar_transporte_por_status('Em andamento')

    # Efetua a consulta de todos os produtos, origens e destinos vinculados aos transportes criados e retorna uma lista dos mesmos
    lista_produtos = consultar_dados_produto(lista_transportes)

    # Prepara os dados para combinação
    produtos_por_id = {produto['id_produto']: produto for produto in lista_produtos}

    lista_transportes_produtos = []

    # Loop para executar a combinação de Transportes e produtos
    for transporte in lista_transportes:
        id_produto = transporte['id_produto']

        # Combina os dados do produto se disponível
        if id_produto in produtos_por_id:
            combinado = {**transporte, **produtos_por_id[id_produto]}

        # Adiciona o combinado à lista final
        lista_transportes_produtos.append(combinado)

    return lista_transportes_produtos


def data_hora_ptbr() -> str:
    # Captura a data e hora atuais
    agora = datetime.now()

    # Formata a data e hora no formato pt-BR
    data_hora_formatada = agora.strftime('%d/%m/%Y - %H:%M:%S')

    return data_hora_formatada


def registrar_log_monitoramento(dados_monitorados: dict) -> None:
    # Nome do arquivo de log
    nome_arquivo = "log_monitoramento_transporte.txt"

    # Verifica se o arquivo já existe; se não, cria o cabeçalho
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(
                "LOG DE MONITORAMENTO DE TRANSPORTE SMALL FARMER TRACKING\n")
            arquivo.write("="*150 + "\n")

    # Abre o arquivo em modo de append
    with open(nome_arquivo, 'a') as arquivo:

        # Formata a linha com os dados monitorados
        linha = (f"id_transporte: {dados_monitorados['id_transporte']}, "
                 f"temp_minima: {dados_monitorados['temp_minima']} C, "
                 f"temp_maxima: {dados_monitorados['temp_maxima']} C, "
                 f"temp_monitorada: {
                     dados_monitorados['temp_monitorada']:.2f} C, "
                 f"dentro_do_intervalo: {
                     dados_monitorados['dentro_intervalo']}, "
                 f"data_hora: {dados_monitorados['data_hora']}\n")

        # Escreve a linha no arquivo
        arquivo.write(linha)


def calcular_media_temperatura_por_id(id_transporte, nome_arquivo):
    # Inicializa variáveis para armazenar temperaturas e contagem
    temperaturas = []
    count = 0

    # Abre o arquivo de log para leitura
    with open(nome_arquivo, 'r') as file:
        # Lê cada linha do arquivo
        for line in file:
            # Ignora a linha de cabeçalho
            if "Log de Monitoramento" in line or "=" in line:
                continue

            # Verifica se a linha contém o id_transporte
            if f"id_transporte: {id_transporte}" in line:
                # Divide a linha em partes usando ', ' como delimitador
                parts = line.split(', ')

                # Verifica se a linha tem pelo menos 4 partes (para acessar a temperatura)
                if len(parts) >= 4:
                    try:
                        # A parte da temperatura monitorada está no formato 'temp_monitorada: 19.12 C'
                        temp_str = parts[3].split(': ')[1].strip()
                        # Converte para float (removendo o ' C' no final)
                        temperatura = float(temp_str[:-2])

                        # Adiciona a temperatura à lista
                        temperaturas.append(temperatura)
                        count += 1
                    except (IndexError, ValueError) as e:
                        # Ignora a linha se houver erro ao processá-la
                        print(f"Erro ao processar a linha: {
                              line.strip()} - Erro: {e}")
                        continue

    # Calcula a média das temperaturas, se houver temperaturas capturadas
    if count > 0:
        media_temperatura = round(sum(temperaturas) / count, 1)
        return {'id_transporte': id_transporte, 'temp_media_monitorada': media_temperatura, 'quant_logs_registrados': count}
    else:
        return None
