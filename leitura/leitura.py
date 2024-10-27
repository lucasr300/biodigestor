import serial
import time
import csv
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import os

# Configurações
arquivo_csv = 'leituras.csv'
porta_http = 8000

# Função para obter o último ID do arquivo CSV
def obter_ultimo_id(arquivo):
    try:
        with open(arquivo, mode='r') as file:
            linhas = list(csv.reader(file))
            if len(linhas) > 1:  # Verifica se há linhas além do cabeçalho
                ultimo_id = int(linhas[-1][0])
                return ultimo_id + 1
            else:
                return 1
    except FileNotFoundError:
        return 1

# Função para iniciar o servidor HTTP em uma thread separada
def iniciar_servidor_http():
    os.chdir('.')  # Define o diretório atual para servir arquivos
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("", porta_http), handler)
    print(f"Servidor HTTP rodando na porta {porta_http}")
    httpd.serve_forever()

# Iniciar o servidor HTTP em uma thread separada
servidor_thread = threading.Thread(target=iniciar_servidor_http)
servidor_thread.daemon = True
servidor_thread.start()

# Configuração da porta serial
ser = serial.Serial('/dev/ttyACM0', 9600)  # Altere a taxa de transmissão se necessário
temperatura = None
umidade = None
id_sequencial = obter_ultimo_id(arquivo_csv)

# Criar o arquivo CSV com o cabeçalho, se não existir
with open(arquivo_csv, mode='a', newline='') as file:
    writer = csv.writer(file)
    if file.tell() == 0:  # Verifica se o arquivo está vazio
        writer.writerow(['ID', 'DataHora', 'Temperatura', 'Umidade'])  # Cabeçalho

try:
    while True:
        if ser.in_waiting > 0:
            # Ler uma linha da porta serial
            linha = ser.readline().decode('latin1', errors='ignore').strip()

            # Verificar se a linha começa com 'T' para temperatura ou 'U' para umidade
            if linha.startswith('T'):
                temperatura = float(linha[1:])
            elif linha.startswith('U'):
                umidade = float(linha[1:])

            # Gravar no CSV apenas se ambos os valores estiverem disponíveis
            if temperatura is not None and umidade is not None:
                # Obter a data e hora atual no formato desejado
                timestamp = datetime.now().strftime('%Y%m%d%H%M')

                # Gravar os dados no arquivo CSV
                with open(arquivo_csv, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([id_sequencial, timestamp, temperatura, umidade])

                # Imprimir para referência
                print(f"ID: {id_sequencial}, Data e Hora: {timestamp}, Temperatura: {temperatura}°C, Umidade: {umidade}%")

                # Incrementar o ID sequencial
                id_sequencial += 1

                # Resetar as variáveis para esperar uma nova leitura de ambos
                temperatura = None
                umidade = None

        # Atualizar uma vez por segundo
        time.sleep(1)

except KeyboardInterrupt:
    print("Leitura interrompida pelo usuário.")
finally:
    ser.close()
