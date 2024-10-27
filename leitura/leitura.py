import serial
import time
from datetime import datetime

# Configure a porta serial para Linux
ser = serial.Serial('/dev/ttyACM0', 9600)  # Altere a taxa de transmissão (9600) se necessário

temperatura = None
umidade = None
id_sequencial = 1

try:
    while True:
        if ser.in_waiting > 0:
            # Ler uma linha da porta serial com codificação alternativa ou ignorando erros
            linha = ser.readline().decode('latin1', errors='ignore').strip()

            # Verificar se a linha começa com 'T' para temperatura ou 'U' para umidade
            if linha.startswith('T'):
                temperatura = float(linha[1:])
            elif linha.startswith('U'):
                umidade = float(linha[1:])

            # Imprimir apenas se ambos os valores estiverem disponíveis
            if temperatura is not None and umidade is not None:
                # Obter a data e hora atual no formato desejado
                timestamp = datetime.now().strftime('%Y%m%d%H%M')

                # Imprimir o ID sequencial, data e hora, temperatura e umidade
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
