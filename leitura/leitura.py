import serial
import time
import csv
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import os
from previsor import prever_proxima_temperatura


class LeitorSerialCSV:
    def __init__(self, porta_serial, taxa_transmissao, arquivo_csv):
        self.porta_serial = porta_serial
        self.taxa_transmissao = taxa_transmissao
        self.arquivo_csv = arquivo_csv
        self.temperatura = None
        self.umidade = None
        self.metano = None
        self.monoxido_de_carbono = None
        self.hidrogenio = None
        self.id_sequencial = self.obter_ultimo_id()
        self.serial = serial.Serial(self.porta_serial, self.taxa_transmissao)
        self.configurar_arquivo_csv()

    def obter_ultimo_id(self):
        try:
            with open(self.arquivo_csv, mode='r') as file:
                linhas = list(csv.reader(file))
                return int(linhas[-1][0]) + 1 if len(linhas) > 1 else 1
        except FileNotFoundError:
            return 1

    def configurar_arquivo_csv(self):
        with open(self.arquivo_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['ID', 'DataHora', 'TemperaturaAtual', 'TemperaturaPrevista', 'Umidade',
                                                    'Metano', 'MonoxidoDeCarbono', 'Hidrogenio'])

    def ler_dados_serial(self):
        if self.serial.in_waiting > 0:
            linha = self.serial.readline().decode('latin1', errors='ignore').strip()
            print(linha)
            if linha.startswith('TEMP'):
                self.temperatura = float(linha[4:])
            elif linha.startswith('UMID'):
                self.umidade = float(linha[4:])
            elif linha.startswith('META'):
                self.metano = float(linha[4:])
            elif linha.startswith('MONO'):
                self.monoxido_de_carbono = float(linha[4:])
            elif linha.startswith('HIDR'):
                self.hidrogenio = float(linha[4:])
            self.registrar_dados()

    def registrar_dados(self):
        if self.temperatura is not None and self.umidade is not None and self.metano is not None:
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

            with open(self.arquivo_csv, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.id_sequencial,
                                timestamp,
                                self.temperatura,
                                prever_proxima_temperatura() or self.temperatura,
                                self.umidade,
                                self.metano,
                                self.monoxido_de_carbono,
                                self.hidrogenio])


            self.id_sequencial += 1
            self.temperatura = None
            self.umidade = None
            self.metano = None

    def iniciar(self):
        try:
            while True:
                self.ler_dados_serial()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Leitura interrompida pelo usuário.")
        finally:
            self.serial.close()

def iniciar_servidor_http(porta):
    os.chdir('.')
    httpd = HTTPServer(("", porta), SimpleHTTPRequestHandler)
    print(f"Servidor HTTP rodando na porta {porta}")
    httpd.serve_forever()

# Configurações
porta_http = 8000
leitor = LeitorSerialCSV('/dev/ttyACM0', 9600, 'leituras.csv')

servidor_thread = threading.Thread(target=iniciar_servidor_http, args=(porta_http,))
servidor_thread.daemon = True
servidor_thread.start()

leitor.iniciar()
